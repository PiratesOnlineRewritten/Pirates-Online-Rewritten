from pandac.PandaModules import *
from direct.showbase.InputStateGlobal import inputState
from direct.fsm import ClassicFSM, State
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import reduceAngle, fitSrcAngle2Dest
from direct.showbase.PythonUtil import clampScalar, getSetter
from direct.showbase.PythonUtil import ParamObj
from direct.task import Task
from otp.otpbase import OTPGlobals
from pirates.pirate import CameraMode
from pirates.piratesbase import PiratesGlobals

class CannonCamera(CameraMode.CameraMode, NodePath, ParamObj):
    notify = DirectNotifyGlobal.directNotify.newCategory('CannonCamera')

    class ParamSet(ParamObj.ParamSet):
        Params = {'minH': -60.0,'maxH': 60.0,'minP': -12.0,'maxP': 24,'sensitivityH': 0.07,'sensitivityP': 0.03}

    CamParentPos = (
     Vec3(0, -6, 3), Vec3(0, -2, 0))

    def __init__(self, params=None):
        ParamObj.__init__(self)
        NodePath.__init__(self, self._getTopNodeName())
        CameraMode.CameraMode.__init__(self)
        self.camParent = self.attachNewNode('cannonCamParent')
        self.inputStateTokens = []
        self._paramStack = []
        self.keyboardDelta = (0, 0)
        self.keyboardRate = 1000
        if params is None:
            self.setDefaultParams()
        else:
            params.applyTo(self)
        return

    def destroy(self):
        self._paramStack = None
        self.camParent = None
        self.cannonProp = None
        CameraMode.CameraMode.destroy(self)
        NodePath.removeNode(self)
        ParamObj.destroy(self)
        return

    def _getTopNodeName(self):
        return 'CannonCam'

    def start(self, cannonProp):
        self.cannonProp = cannonProp
        CameraMode.CameraMode.start(self)

    def getName(self):
        return 'Cannon'

    def pushParams(self):
        self._paramStack.append(self.ParamSet(self))

    def popParams(self):
        if len(self._paramStack):
            self._paramStack.pop().applyTo(self)
        else:
            CannonCamera.notify.warning('param stack underflow')

    def getMinH(self):
        return self.minH

    def setMinH(self, minH):
        self.minH = minH

    def getMaxH(self):
        return self.maxH

    def setMaxH(self, maxH):
        self.maxH = maxH

    def getMinP(self):
        return self.minP

    def setMinP(self, minP):
        self.minP = minP

    def getMaxP(self):
        return self.maxP

    def setMaxP(self, maxP):
        self.maxP = maxP

    def getSensitivityH(self):
        return self.sensitivityH

    def setSensitivityH(self, sensitivityH):
        self.sensitivityH = sensitivityH

    def getSensitivityP(self):
        return self.sensitivityP

    def setSensitivityP(self, sensitivityP):
        self.sensitivityP = sensitivityP

    def enterActive(self):
        CameraMode.CameraMode.enterActive(self)
        base.camLens.setMinFov(PiratesGlobals.CannonCameraFov)
        base.camNode.setLodCenter(self)
        if base.wantEnviroDR:
            base.enviroCamNode.setLodCenter(self)
        if self.cannonProp.ship:
            self.reparentTo(self.cannonProp.ship.avCannonView)
        else:
            self.reparentTo(self.cannonProp.hNode)
        camera.reparentTo(self.camParent)
        self.camParent.clearTransform()
        self.clearTransform()
        camera.clearTransform()
        self.camParent.setPosHpr(*self.CamParentPos)
        self.camParent.setR(render, 0.0)

    def _startKeyboardUpdateTask(self):
        self._stopKeyboardUpdateTask()
        self.inputStateTokens = []
        ist = self.inputStateTokens
        ist.append(inputState.watchWithModifiers('forward', 'arrow_up', inputSource=inputState.ArrowKeys))
        ist.append(inputState.watchWithModifiers('reverse', 'arrow_down', inputSource=inputState.ArrowKeys))
        ist.append(inputState.watchWithModifiers('turnLeft', 'arrow_left', inputSource=inputState.ArrowKeys))
        ist.append(inputState.watchWithModifiers('turnRight', 'arrow_right', inputSource=inputState.ArrowKeys))
        ist.append(inputState.watchWithModifiers('forward', 'w', inputSource=inputState.WASD))
        ist.append(inputState.watchWithModifiers('reverse', 's', inputSource=inputState.WASD))
        ist.append(inputState.watchWithModifiers('turnLeft', 'a', inputSource=inputState.WASD))
        ist.append(inputState.watchWithModifiers('turnRight', 'd', inputSource=inputState.WASD))
        ist.append(inputState.watchWithModifiers('turnLeft', 'q', inputSource=inputState.QE))
        ist.append(inputState.watchWithModifiers('turnRight', 'e', inputSource=inputState.QE))
        taskMgr.add(self._keyboardUpdateTask, '%s-KeyboardUpdate' % self._getTopNodeName(), priority=40)

    def _stopKeyboardUpdateTask(self):
        taskMgr.remove('%s-KeyboardUpdate' % self._getTopNodeName())
        for token in self.inputStateTokens:
            token.release()

        self.inputStateTokens = []

    def exitActive(self):
        self.cannonProp = None
        base.camNode.setLodCenter(NodePath())
        if base.wantEnviroDR:
            base.enviroCamNode.setLodCenter(NodePath())
        self.disableInput()
        CameraMode.CameraMode.exitActive(self)
        return

    def _keyboardUpdateTask(self, task):
        if inputState.isSet('forward'):
            dy = -self.keyboardRate
        else:
            if inputState.isSet('reverse'):
                dy = self.keyboardRate
            else:
                dy = 0
            if inputState.isSet('turnRight'):
                dx = self.keyboardRate
            else:
                if inputState.isSet('turnLeft'):
                    dx = -self.keyboardRate
                dx = 0
        dt = globalClock.getDt()
        dx *= dt
        dy *= dt
        self.keyboardDelta = (dx, dy)
        self.__moveCamera(dx, dy)
        return Task.cont

    def _mouseUpdateTask(self, task):
        dx, dy = self.mouseDelta
        self.__moveCamera(dx, dy)
        return Task.cont

    def __moveCamera(self, dx, dy):
        if base.options.mouse_look:
            dy = -dy
        ship = self.cannonProp.ship
        if ship:
            curH = self.cannonProp.currentHpr[0]
            curP = ship.avCannonRotate.getP()
            shipH = (self.cannonProp.ship.getH(self.cannonProp) + 360) % 360
            if self.cannonProp.oldShipH >= 270 and shipH < 90:
                self.cannonProp.shipH += shipH
            else:
                if self.cannonProp.oldShipH < 90 and shipH >= 270:
                    self.cannonProp.shipH += 360 - shipH
                else:
                    self.cannonProp.shipH += shipH - self.cannonProp.oldShipH
                self.cannonProp.oldShipH = shipH
                newH = min(max(curH + -dx * self.sensitivityH, self.minH + self.cannonProp.shipH), self.maxH + self.cannonProp.shipH)
                newP = min(max(curP + -dy * self.sensitivityP, self.minP), self.maxP)
                relH = newH - self.cannonProp.shipH
                ship.avCannonRotate.setH(relH)
                ship.avCannonRotate.setP(newP)
                ship.avCannonRotate.setR(render, 0)
                if localAvatar.cannon:
                    cannonDressingNode = localAvatar.cannon.cannonDressingNode
                    cannonDressingNode.setPos(self.cannonProp.cannonExitPoint.getPos())
                    cannonDressingNode.setHpr(self.cannonProp.cannonExitPoint.getHpr())
            self.cannonProp.pivot.setH(0.0)
            self.cannonProp.pivot.setP(newP)
            self.cannonProp.pivot.setR(render, 0.0)
            self.cannonProp.hNode.setH(relH)
            p = self.cannonProp.pivot.getP(render)
            self.cannonProp.currentHpr = (newH, p, 0)
        else:
            curH = self.cannonProp.hNode.getH(render)
            curP = self.cannonProp.currentHpr[1]
            newH = curH + -dx * self.sensitivityH
            newP = min(max(curP + -dy * self.sensitivityP, self.minP), self.maxP)
            self.setRotation(newH, newP)

    def setRotation(self, newH, newP):
        self.cannonProp.hNode.setH(render, newH)
        h = self.cannonProp.hNode.getH()
        h = min(max(h, self.minH), self.maxH)
        self.cannonProp.hNode.setH(h)
        self.camParent.setP(-2.0 + newP / 2.0)
        self.camParent.setR(render, 0.0)
        self.cannonProp.pivot.setH(0.0)
        self.cannonProp.pivot.setP(newP)
        self.cannonProp.currentHpr = (
         newH, newP, 0)

    def enableInput(self):
        CameraMode.CameraMode.enableInput(self)
        self._startKeyboardUpdateTask()

    def disableInput(self):
        CameraMode.CameraMode.disableInput(self)
        self._stopKeyboardUpdateTask()