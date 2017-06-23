from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import reduceAngle, fitSrcAngle2Dest
from direct.showbase.PythonUtil import clampScalar, getSetter
from direct.showbase.PythonUtil import ParamObj
from direct.task import Task
from otp.otpbase import OTPGlobals
from pirates.pirate import CameraMode
from pirates.piratesbase import PiratesGlobals
import math

class OrbitCamera(CameraMode.CameraMode, NodePath, ParamObj):
    notify = DirectNotifyGlobal.directNotify.newCategory('OrbitCamera')

    class ParamSet(ParamObj.ParamSet):
        Params = {'lookAtOffset': Vec3(0, 0, 0),'escapement': 10.0,'rotation': 0.0,'fadeGeom': False,'idealDistance': 25.0,'minDistance': 3.0,'maxDistance': 40.0,'minEsc': -20.0,'maxEsc': 25.0,'minDomeEsc': 0.0,'maxCamtiltEsc': 0.0,'autoFaceForward': True,'autoFaceForwardMaxDur': 14.0}

    UpdateTaskName = 'OrbitCamUpdateTask'
    CollisionCheckTaskName = 'OrbitCamCollisionTask'
    GeomFadeLerpDur = 1.0
    PullFwdDist = 2.0

    def __init__(self, subject, params=None):
        ParamObj.__init__(self)
        NodePath.__init__(self, self._getTopNodeName())
        CameraMode.CameraMode.__init__(self)
        self.setSubject(subject)
        self.lookAtNode = NodePath('orbitCamLookAt')
        self.escapementNode = self.attachNewNode('orbitCamEscapement')
        self.camParent = self.escapementNode.attachNewNode('orbitCamParent')
        self._paramStack = []
        if params is None:
            self.setDefaultParams()
        else:
            params.applyTo(self)
        self._isAtRear = True
        self._rotateToRearIval = None
        self._lockAtRear = False
        return

    def destroy(self):
        self._paramStack = None
        self.escapemntNode = None
        self.camParent = None
        self.lookAtNode.removeNode()
        del self.subject
        CameraMode.CameraMode.destroy(self)
        NodePath.removeNode(self)
        ParamObj.destroy(self)
        return

    def getName(self):
        return 'Orbit'

    def _getTopNodeName(self):
        return 'OrbitCam'

    def setSubject(self, subject=None):
        self.subject = subject

    def getSubject(self):
        return self.subject

    def pushParams(self):
        self._paramStack.append(self.ParamSet(self))

    def popParams(self):
        curParams = self.ParamSet(self)
        if len(self._paramStack):
            self._paramStack.pop().applyTo(self)
        else:
            OrbitCamera.notify.warning('param stack underflow')
        return curParams

    def getLookAtOffset(self):
        return self.lookAtOffset

    def setLookAtOffset(self, lookAtOffset):
        self.lookAtOffset = Vec3(lookAtOffset)

    def applyLookAtOffset(self):
        if self.isActive():
            self.lookAtNode.setPos(self.lookAtOffset)
            self.setFluidPos(render, self.lookAtNode.getPos(render))
            camera.lookAt(self.lookAtNode)

    def getEscapement(self):
        return self.escapement

    def setEscapement(self, escapement):
        self.escapement = escapement

    def applyEscapement(self):
        if self.isActive():
            if self.escapement >= self._minDomeEsc:
                domeEsc = self.escapement
                camEsc = 0.0
            elif self.escapement <= self._maxCamtiltEsc:
                domeEsc = self._minDomeEsc
                camEsc = self._maxCamtiltEsc - self.escapement
            else:
                domeEsc = self._minDomeEsc
                camEsc = 0.0
            self.escapementNode.setP(-domeEsc)
            self.camParent.setP(camEsc)

    def _lerpEscapement(self, escapement, duration=None):
        curEsc = self.getEscapement()
        escapement = clampScalar(escapement, self._minEsc, self._maxEsc)
        if duration is None:
            diff = abs(curEsc - escapement)
            speed = (max(curEsc, self._maxEsc) - min(curEsc, self._minEsc)) * 0.025
            duration = diff / speed
        self._stopEscapementLerp()
        self._escLerpIval = LerpFunctionInterval(self.setEscapement, fromData=curEsc, toData=escapement, duration=duration, blendType='easeOut', name='OrbitCamera.escapementLerp')
        self._escLerpIval.start()
        return

    def _stopEscapementLerp(self):
        if self._escLerpIval is not None and self._escLerpIval.isPlaying():
            self._escLerpIval.pause()
            self._escLerpIval = None
        return

    def getRotation(self):
        return self.getH(self.subject)

    def setRotation(self, rotation):
        self._rotation = rotation
        if self.subject:
            self.setH(self.subject, rotation)

    def getFadeGeom(self):
        return self._fadeGeom

    def setFadeGeom(self, fadeGeom):
        self._fadeGeom = fadeGeom

    def applyFadeGeom(self):
        if self.isActive():
            if not self._fadeGeom and self.getPriorValue():
                if hasattr(self, '_hiddenGeoms'):
                    for np in self._hiddenGeoms.keys():
                        self._unfadeGeom(np)

                    self._hiddenGeoms = {}

    def getIdealDistance(self):
        return self.idealDistance

    def setIdealDistance(self, idealDistance):
        self.idealDistance = idealDistance

    def applyIdealDistance(self):
        if self.isActive():
            self.idealDistance = clampScalar(self.idealDistance, self._minDistance, self._maxDistance)
            if self._practicalDistance is None:
                self._zoomToDistance(self.idealDistance)
        return

    def popToIdealDistance(self):
        self._setCurDistance(self.idealDistance)

    def setPracticalDistance(self, practicalDistance):
        if practicalDistance is not None and practicalDistance > self.idealDistance:
            practicalDistance = None
        if self._practicalDistance is None:
            if practicalDistance is None:
                return
            self._stopZoomIval()
            self._setCurDistance(practicalDistance)
        else:
            self._stopZoomIval()
            if practicalDistance is None:
                self._zoomToDistance(self.idealDistance)
            else:
                self._setCurDistance(practicalDistance)
        self._practicalDistance = practicalDistance
        return

    def getMinDistance(self):
        return self._minDistance

    def setMinDistance(self, minDistance):
        self._minDistance = minDistance

    def applyMinDistance(self):
        if self.isActive():
            self.setIdealDistance(self.idealDistance)

    def getMaxDistance(self):
        return self._maxDistance

    def setMaxDistance(self, maxDistance):
        self._maxDistance = maxDistance

    def applyMaxDistance(self):
        if self.isActive():
            self.setIdealDistance(self.idealDistance)
            if hasattr(self, '_collSolid'):
                self._collSolid.setPointB(0, -(self._maxDistance + OrbitCamera.PullFwdDist), 0)

    def getMinEsc(self):
        return self._minEsc

    def getMaxEsc(self):
        return self._maxEsc

    def getMinDomeEsc(self):
        return self._minDomeEsc

    def getMaxCamtiltEsc(self):
        return self._maxCamtiltEsc

    def setMinEsc(self, minEsc):
        self._minEsc = minEsc

    def setMaxEsc(self, maxEsc):
        self._maxEsc = maxEsc

    def setMinDomeEsc(self, minDomeEsc):
        self._minDomeEsc = minDomeEsc

    def setMaxCamtiltEsc(self, maxCamtiltEsc):
        self._maxCamtiltEsc = maxCamtiltEsc

    def enterActive(self):
        CameraMode.CameraMode.enterActive(self)
        self.reparentTo(render)
        self.clearTransform()
        self.setH(self.subject, self._rotation)
        self.setP(0)
        self.setR(0)
        self.camParent.clearTransform()
        camera.reparentTo(self.camParent)
        camera.clearTransform()
        base.camNode.setLodCenter(self.subject)
        if base.wantEnviroDR:
            base.enviroCamNode.setLodCenter(self.subject)
        self.lookAtNode.reparentTo(self.subject)
        self.lookAtNode.clearTransform()
        self.lookAtNode.setPos(self.lookAtOffset)
        self.setFluidPos(render, self.lookAtNode.getPos(render))
        self.escapementNode.setP(-self.escapement)
        self._setCurDistance(self.idealDistance)
        camera.lookAt(self.lookAtNode)
        self._disableRotateToRear()
        self._isAtRear = True
        self._rotateToRearIval = None
        self._lockAtRear = False
        self._zoomIval = None
        self._escLerpIval = None
        self._practicalDistance = None
        self._startUpdateTask()
        self._startCollisionCheck()
        return

    def exitActive(self):
        taskMgr.remove(OrbitCamera.UpdateTaskName)
        self.ignoreAll()
        self._stopZoomIval()
        self._stopEscapementLerp()
        self._stopRotateToRearIval()
        self._stopCollisionCheck()
        self._stopUpdateTask()
        self.lookAtNode.detachNode()
        self.detachNode()
        base.camNode.setLodCenter(NodePath())
        if base.wantEnviroDR:
            base.enviroCamNode.setLodCenter(NodePath())
        CameraMode.CameraMode.exitActive(self)

    def _startUpdateTask(self):
        self.lastSubjectH = self.subject.getH(render)
        taskMgr.add(self._updateTask, OrbitCamera.UpdateTaskName, priority=40)
        self._updateTask()

    def _updateTask(self, task=None):
        self.setFluidPos(render, self.lookAtNode.getPos(render))
        curSubjectH = self.subject.getH(render)
        if self._lockAtRear:
            self.setRotation(0.0)
        elif self._rotateToRearEnabled and self.getAutoFaceForward():
            relH = reduceAngle(self.getH(self.subject))
            absRelH = abs(relH)
            if absRelH < 0.1:
                self.setRotation(0.0)
                self._stopRotateToRearIval()
                self._lockAtRear = True
            else:
                ivalPlaying = self._rotateToRearIvalIsPlaying()
                if ivalPlaying and curSubjectH == self.lastSubjectH:
                    pass
                else:
                    self._stopRotateToRearIval()
                    duration = self._autoFaceForwardMaxDur * absRelH / 180.0
                    targetH = curSubjectH
                    startH = fitSrcAngle2Dest(self.getH(render), targetH)
                    self._rotateToRearIval = LerpHprInterval(self, duration, Point3(targetH, 0, 0), startHpr=Point3(startH, 0, 0), other=render, blendType='easeOut')
                    self._rotateToRearIval.start()
        self.lastSubjectH = curSubjectH
        self.setP(0)
        self.setR(0)
        camera.clearMat()
        return Task.cont

    def _stopUpdateTask(self):
        taskMgr.remove(OrbitCamera.UpdateTaskName)

    def setAutoFaceForward(self, autoFaceForward):
        if not autoFaceForward:
            self._stopRotateToRearIval()
        self._autoFaceForward = autoFaceForward

    def getAutoFaceForward(self):
        return self._autoFaceForward

    def setAutoFaceForwardMaxDur(self, autoFaceForwardMaxDur):
        self._autoFaceForwardMaxDur = autoFaceForwardMaxDur

    def getAutoFaceForwardMaxDur(self):
        return self._autoFaceForwardMaxDur

    def _enableRotateToRear(self):
        self._rotateToRearEnabled = True

    def _disableRotateToRear(self):
        self._stopRotateToRearIval()
        self._rotateToRearEnabled = False

    def _rotateToRearIvalIsPlaying(self):
        return self._rotateToRearIval is not None and self._rotateToRearIval.isPlaying()

    def _stopRotateToRearIval(self):
        if self._rotateToRearIval is not None and self._rotateToRearIval.isPlaying():
            self._rotateToRearIval.pause()
            self._rotateToRearIval = None
        return

    def _getCurDistance(self):
        return -self.camParent.getY()

    def _setCurDistance(self, distance):
        self.camParent.setY(-distance)

    def _zoomToDistance(self, distance):
        curDistance = self._getCurDistance()
        diff = abs(curDistance - distance)
        if diff < 0.01:
            self._setCurDistance(distance)
            return
        speed = (max(curDistance, self._maxDistance) - min(curDistance, self._minDistance)) * 0.5
        duration = diff / speed
        self._stopZoomIval()
        self._zoomIval = LerpPosInterval(self.camParent, duration, Point3(0, -distance, 0), blendType='easeOut', name='orbitCamZoom', fluid=1)
        self._zoomIval.start()

    def _stopZoomIval(self):
        if self._zoomIval is not None and self._zoomIval.isPlaying():
            self._zoomIval.pause()
            self._zoomIval = None
        return

    def _startCollisionCheck(self, shipBarrier=0):
        self._collSolid = CollisionSegment(0, 0, 0, 0, -(self._maxDistance + OrbitCamera.PullFwdDist), 0)
        collSolidNode = CollisionNode('OrbitCam.CollSolid')
        collSolidNode.addSolid(self._collSolid)
        if shipBarrier:
            collSolidNode.setFromCollideMask(PiratesGlobals.ShipCameraBarrierBitmask)
        else:
            collSolidNode.setFromCollideMask(OTPGlobals.CameraBitmask | OTPGlobals.CameraTransparentBitmask | OTPGlobals.FloorBitmask)
        collSolidNode.setIntoCollideMask(BitMask32.allOff())
        self._collSolidNp = self.escapementNode.attachNewNode(collSolidNode)
        self._cHandlerQueue = CollisionHandlerQueue()
        self._cTrav = CollisionTraverser('OrbitCam.cTrav')
        self._cTrav.addCollider(self._collSolidNp, self._cHandlerQueue)
        self._hiddenGeoms = {}
        self._fadeOutIvals = {}
        self._fadeInIvals = {}
        taskMgr.add(self._collisionCheckTask, OrbitCamera.CollisionCheckTaskName, priority=45)

    def _collisionCheckTask(self, task=None):
        self._cTrav.traverse(render)
        self.cTravOnFloor.traverse(render)
        if self._fadeGeom:
            nonObstrGeoms = dict(self._hiddenGeoms)
            numEntries = self._cHandlerQueue.getNumEntries()
            if numEntries > 0:
                self._cHandlerQueue.sortEntries()
                i = 0
                while i < numEntries:
                    collEntry = self._cHandlerQueue.getEntry(i)
                    intoNode = collEntry.getIntoNodePath()
                    cMask = intoNode.node().getIntoCollideMask()
                    if not (cMask & OTPGlobals.CameraTransparentBitmask).isZero():
                        if intoNode in nonObstrGeoms:
                            del nonObstrGeoms[intoNode]
                        self._fadeGeom(intoNode)
                    else:
                        cPoint = collEntry.getSurfacePoint(self.escapementNode)
                        distance = Vec3(cPoint).length()
                        self.setPracticalDistance(distance - OrbitCamera.PullFwdDist)
                        break
                    i += 1

            else:
                self.setPracticalDistance(None)
            for np in nonObstrGeoms.keys():
                self._unfadeGeom(np)

        else:
            if self._cHandlerQueue.getNumEntries() > 0:
                self._cHandlerQueue.sortEntries()
                collEntry = self._cHandlerQueue.getEntry(0)
                cPoint = collEntry.getSurfacePoint(self.escapementNode)
                distance = Vec3(cPoint).length()
                self.setPracticalDistance(distance - OrbitCamera.PullFwdDist)
            self.setPracticalDistance(None)
        distance = self._getCurDistance()
        return Task.cont

    def _stopCollisionCheck(self):
        while len(self._hiddenGeoms):
            self._unfadeGeom(self._hiddenGeoms.keys()[0])

        del self._hiddenGeoms
        del self._fadeOutIvals
        del self._fadeInIvals
        taskMgr.remove(OrbitCamera.CollisionCheckTaskName)
        self._cTrav.removeCollider(self._collSolidNp)
        del self._cHandlerQueue
        del self._cTrav
        self._collSolidNp.detachNode()
        del self._collSolidNp

    def _fadeGeom(self, np):
        if np in self._fadeInIvals:
            self._fadeInIvals[np].finish()
            del self._fadeInIvals[np]
        if np not in self._hiddenGeoms:
            hadTransparency = np.getTransparency()
            fadeIval = Sequence(Func(np.setTransparency, 1), LerpColorScaleInterval(np, OrbitCamera.GeomFadeLerpDur, VBase4(1, 1, 1, 0), blendType='easeInOut'), name='OrbitCamFadeGeomOut')
            self._hiddenGeoms[np] = hadTransparency
            self._fadeOutIvals[np] = fadeIval
            fadeIval.start()

    def _unfadeGeom(self, np):
        if np in self._hiddenGeoms:
            if np in self._fadeOutIvals:
                self._fadeOutIvals[np].pause()
                del self._fadeOutIvals[np]
            fadeIval = Sequence(LerpColorScaleInterval(np, OrbitCamera.GeomFadeLerpDur, VBase4(1, 1, 1, 1), blendType='easeInOut'), Func(np.setTransparency, self._hiddenGeoms[np]), name='OrbitCamFadeGeomIn')
            del self._hiddenGeoms[np]
            self._fadeInIvals[np] = fadeIval
            fadeIval.start()