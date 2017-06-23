from direct.showbase import DirectObject
from direct.fsm import ClassicFSM, State
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import reduceAngle, fitSrcAngle2Dest, clampScalar, lerp, Functor
from direct.showbase.InputStateGlobal import inputState
from pandac.PandaModules import *
from otp.otpbase import OTPGlobals
from pirates.pirate.OrbitCamera import OrbitCamera
import math
from direct.task import Task

class ShipCamera(OrbitCamera):

    class ParamSet(OrbitCamera.ParamSet):
        Params = {}

    def __init__(self, subject, params=None):
        OrbitCamera.__init__(self, subject, params)
        self.lastFrameTime = None
        self.camTimer = 0.0
        self.correctionAmount = 0.5
        self.recoverySpeed = 0.25
        self.smoothSecs = 4.0
        self.lastHeading = None
        self.smoothProjectedTarget = 0.0
        self.shipSpeed = 0.0
        self.speedAcceptName = None
        base.shipCam = self
        return

    def recordShipSpeed(self, speed, maxSpeed):
        self.shipSpeed = speed

    def destroy(self):
        OrbitCamera.destroy(self)

    def getName(self):
        return 'Orbit'

    def _getTopNodeName(self):
        return 'ShipCam'

    def _handleWheelUp(self):
        self.setIdealDistance(self.idealDistance - (self._maxDistance - self._minDistance) * 0.2)
        self.applyIdealDistance()

    def _handleWheelDown(self):
        self.setIdealDistance(self.idealDistance + (self._maxDistance - self._minDistance) * 0.2)
        self.applyIdealDistance()

    def _startCollisionCheck(self):
        OrbitCamera._startCollisionCheck(self, shipBarrier=1)

    def enterActive(self):
        OrbitCamera.enterActive(self)
        self.accept('wheel_up', self._handleWheelUp)
        self.accept('wheel_down', self._handleWheelDown)
        self._scInputState = ScratchPad()
        self._scInputState.rmbPressed = False
        self._scInputState.fwdPressed = False
        self._scInputListener = DirectObject.DirectObject()
        self._scInputListener.accept(inputState.getEventName('RMB'), self._handleRmbEvent)
        self._handleRmbEvent(inputState.isSet('RMB'))
        self._scInputListener.accept(inputState.getEventName('forward'), self._handleForwardEvent)
        self._handleForwardEvent(inputState.isSet('forward'))
        if hasattr(self.subject, 'doId'):
            self.speedAcceptName = 'setShipSpeed-%s' % self.subject.doId
            self.accept(self.speedAcceptName, self.recordShipSpeed)

    def exitActive(self):
        OrbitCamera.exitActive(self)
        if self.speedAcceptName:
            self.ignore(self.speedAcceptName)
        self.ignore('wheel_up')
        self.ignore('wheel_down')
        self._scInputListener.ignoreAll()
        del self._scInputListener
        del self._scInputState

    def _startMouseControlTasks(self):
        OrbitCamera._startMouseControlTasks(self)
        if self.mouseControl:
            self._lockAtRear = False

    def _handleRmbEvent(self, pressed):
        if pressed and not self._scInputState.rmbPressed:
            self._disableRotateToRear()
        self._scInputState.rmbPressed = pressed

    def _handleForwardEvent(self, pressed):
        if pressed and not self._scInputState.fwdPressed:
            if not self._scInputState.rmbPressed:
                self._enableRotateToRear()
        self._scInputState.fwdPressed = pressed

    def _stopMouseControlTasks(self):
        OrbitCamera._stopMouseControlTasks(self)

    def _mouseUpdateTask(self, task):
        if OrbitCamera._mouseUpdateTask(self, task) == task.cont and self.mouseDelta[0] or self.mouseDelta[1]:
            sensitivity = 0.5
            self.camTimer = -1.0
            self.setRotation(self.getRotation() - self.mouseDelta[0] * sensitivity)
            self.setEscapement(clampScalar(self.escapement + self.mouseDelta[1] * sensitivity * 0.6, self._minEsc, self._maxEsc))
        return task.cont

    def _updateTask(self, task=None):
        if not base.shipLookAhead:
            return OrbitCamera._updateTask(self, task)
        self.setFluidPos(render, self.lookAtNode.getPos(render))
        if self.lastHeading == None:
            self.lastHeading = reduceAngle(self.subject.getH())
        fittedAngle = fitSrcAngle2Dest(self.subject.getH(), self.lastHeading)
        headingDif = fittedAngle - self.lastHeading
        self.lastHeading = self.subject.getH()
        if self.lastFrameTime != None:
            lastFrameTime = self.lastFrameTime
            newFrameTime = globalClock.getFrameTime()
            timeDelta = min(self.smoothSecs, newFrameTime - lastFrameTime)
            self.lastFrameTime = newFrameTime
        else:
            self.lastFrameTime = globalClock.getFrameTime()
            timeDelta = 0.0
        if self._rotateToRearEnabled and self.getAutoFaceForward() and self.camTimer < 0.0:
            self.camTimer = 0.0
        if self.camTimer >= 0.0:
            self.camTimer = min(timeDelta * self.recoverySpeed + self.camTimer, 1.0)
            camTimer = max(0, self.camTimer)
        if self.mouseControl or self.camTimer < 0:
            self.smoothProjectedTarget = self.getH(self.subject)
        else:
            if timeDelta == 0.0:
                headingVelocity = 0.0
            else:
                headingVelocity = headingDif / timeDelta
            projectedTarget = headingVelocity
            if self.shipSpeed < 0.0:
                projectedTarget = -1.0 * projectedTarget
            if projectedTarget < 0:
                projectedTarget = -3.5 * math.pow(abs(projectedTarget), 0.6)
            else:
                projectedTarget = 3.5 * math.pow(abs(projectedTarget), 0.6)
            readjustSpeed = 1.0
            if abs(headingVelocity) < 1.0:
                readjustSpeed = 0.5
            readjustTime = self.smoothSecs * readjustSpeed
            self.smoothProjectedTarget = (self.smoothProjectedTarget * (readjustTime - timeDelta * self.camTimer) + projectedTarget * (timeDelta * self.camTimer)) / readjustTime
            curSubjectH = self.subject.getH(render)
            relH = reduceAngle(self.getH(self.subject))
            self.setRotation(self.smoothProjectedTarget)
            self.setP(0)
            self.setR(0)
            camera.clearMat()
        return Task.cont