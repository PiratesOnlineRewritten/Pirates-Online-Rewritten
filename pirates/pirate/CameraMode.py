from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.showbase.PythonUtil import Enum
from direct.fsm.FSM import FSM
from otp.otpbase import OTPGlobals

class CameraMode(DirectObject.DirectObject, FSM):
    Modes = Enum('NORMAL, BATTLE')

    def __init__(self):
        FSM.__init__(self, 'CameraMode')
        self.mouseControl = False
        self.mouseDelta = (0, 0)
        self.lastMousePos = (0, 0)
        self.origMousePos = (0, 0)
        self.request('Off')
        self.__inputEnabled = False

    def destroy(self):
        pass

    def getName(self):
        pass

    def start(self):
        if not self.isActive():
            self.request('Active')

    def stop(self):
        if self.isActive():
            self.request('Off')

    def isActive(self):
        return self.state == 'Active'

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterActive(self):
        self.cTravOnFloor = CollisionTraverser('CamMode.cTravOnFloor')
        self.camFloorRayNode = self.attachNewNode('camFloorRayNode')
        self.ccRay2 = CollisionRay(0.0, 0.0, 0.0, 0.0, 0.0, -1.0)
        self.ccRay2Node = CollisionNode('ccRay2Node')
        self.ccRay2Node.addSolid(self.ccRay2)
        self.ccRay2NodePath = self.camFloorRayNode.attachNewNode(self.ccRay2Node)
        self.ccRay2BitMask = OTPGlobals.FloorBitmask
        self.ccRay2Node.setFromCollideMask(self.ccRay2BitMask)
        self.ccRay2Node.setIntoCollideMask(BitMask32.allOff())
        self.ccRay2MoveNodePath = hidden.attachNewNode('ccRay2MoveNode')
        self.camFloorCollisionBroadcaster = CollisionHandlerFloor()
        self.camFloorCollisionBroadcaster.setInPattern('on-floor')
        self.camFloorCollisionBroadcaster.setOutPattern('off-floor')
        self.camFloorCollisionBroadcaster.addCollider(self.ccRay2NodePath, self.ccRay2MoveNodePath)
        self.cTravOnFloor.addCollider(self.ccRay2NodePath, self.camFloorCollisionBroadcaster)
        self.enableInput()

    def exitActive(self):
        self.disableInput()
        del self.cTravOnFloor
        del self.ccRay2
        del self.ccRay2Node
        self.ccRay2NodePath.removeNode()
        del self.ccRay2NodePath
        self.ccRay2MoveNodePath.removeNode()
        del self.ccRay2MoveNodePath
        self.camFloorRayNode.removeNode()
        del self.camFloorRayNode

    def enableInput(self):
        self.__inputEnabled = True
        self.accept('mouse3', self.enableMouseControl)
        self.accept('mouse3-up', self.disableMouseControl)
        if base.mouseWatcherNode.isButtonDown(MouseButton.three()):
            self.enableMouseControl()

    def disableInput(self):
        self.__inputEnabled = False
        self.disableMouseControl()
        self.ignore('mouse3')
        self.ignore('mouse3-up')

    def isInputEnabled(self):
        return self.__inputEnabled

    def enableMouseControl(self):
        if hasattr(base, 'oobeMode') and base.oobeMode:
            return
        self.mouseControl = True
        mouseData = base.win.getPointer(0)
        self.origMousePos = (mouseData.getX(), mouseData.getY())
        if 'localAvatar' in __builtins__:
            localAvatar.guiMgr._hideCursor()
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)
        self.lastMousePos = (
         base.win.getXSize() / 2, base.win.getYSize() / 2)
        if self.getCurrentOrNextState() == 'Active':
            self._startMouseControlTasks()

    def disableMouseControl(self):
        if hasattr(base, 'oobeMode') and base.oobeMode:
            return
        if self.mouseControl:
            self.mouseControl = False
            self._stopMouseControlTasks()
            if 'localAvatar' in __builtins__:
                localAvatar.guiMgr._showCursor()
            base.win.movePointer(0, self.origMousePos[0], self.origMousePos[1])

    def _startMouseControlTasks(self):
        if self.mouseControl:
            properties = WindowProperties()
            properties.setMouseMode(properties.MRelative)
            base.win.requestProperties(properties)
            self._startMouseReadTask()
            self._startMouseUpdateTask()

    def _stopMouseControlTasks(self):
        properties = WindowProperties()
        properties.setMouseMode(properties.MAbsolute)
        base.win.requestProperties(properties)
        self._stopMouseReadTask()
        self._stopMouseUpdateTask()

    def _startMouseReadTask(self):
        self._stopMouseReadTask()
        taskMgr.add(self._mouseReadTask, '%s-MouseRead' % self._getTopNodeName(), priority=-29)

    def _mouseReadTask(self, task):
        if hasattr(base, 'oobeMode') and base.oobeMode:
            self.mouseDelta = (0, 0)
            return task.cont
        elif not base.mouseWatcherNode.hasMouse():
            self.mouseDelta = (0, 0)
        else:
            winSize = (
             base.win.getXSize(), base.win.getYSize())
            mouseData = base.win.getPointer(0)
            if mouseData.getX() > winSize[0] or mouseData.getY() > winSize[1]:
                self.mouseDelta = (0, 0)
            else:
                self.mouseDelta = (mouseData.getX() - self.lastMousePos[0], mouseData.getY() - self.lastMousePos[1])
                base.win.movePointer(0, winSize[0] / 2, winSize[1] / 2)
                mouseData = base.win.getPointer(0)
                self.lastMousePos = (mouseData.getX(), mouseData.getY())
        return task.cont

    def _stopMouseReadTask(self):
        taskMgr.remove('%s-MouseRead' % self._getTopNodeName())

    def _startMouseUpdateTask(self):
        self._stopMouseUpdateTask()
        taskMgr.add(self._avatarFacingTask, '%s-AvatarFacing' % self._getTopNodeName(), priority=23)
        taskMgr.add(self._mouseUpdateTask, '%s-MouseUpdate' % self._getTopNodeName(), priority=40)

    def _avatarFacingTask(self, task):
        return task.cont

    def _mouseUpdateTask(self, task):
        return task.cont

    def _stopMouseUpdateTask(self):
        taskMgr.remove('%s-MouseUpdate' % self._getTopNodeName())
        taskMgr.remove('%s-AvatarFacing' % self._getTopNodeName())

    def avFaceCamera(self):
        pass