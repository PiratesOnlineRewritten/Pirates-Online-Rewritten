from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM
from direct.task import Task
from direct.showbase.InputStateGlobal import inputState
from pirates.pirate import ShipCamera
from pirates.pirate import FPSCamera
from pirates.pirate import CannonCamera
from pirates.pirate import CannonDefenseCamera

class CameraFSM(FSM):

    def __init__(self, av):
        FSM.__init__(self, 'CameraFSM')
        self.av = av
        self.orbitCamera = ShipCamera.ShipCamera(self.av)
        self.orbitCamera.setLookAtOffset(Vec3(0, 0, self.av.getHeight()))
        self.fpsCamera = FPSCamera.FPSCamera(self.av)
        self.cannonCamera = CannonCamera.CannonCamera()
        self.cannonDefenseCamera = CannonDefenseCamera.CannonDefenseCamera()
        self.currentCamera = None
        self.cameras = (
         self.orbitCamera, self.fpsCamera, self.cannonCamera, self.cannonDefenseCamera)
        self._rmbToken = inputState.watchWithModifiers('RMB', 'mouse3')
        return

    def cleanup(self):
        FSM.cleanup(self)
        if hasattr(self, 'cameras'):
            self._rmbToken.release()
            del self._rmbToken
            self.ignoreAll()
            del self.cameras
            del self.currentCamera
            self.orbitCamera.destroy()
            del self.orbitCamera
            self.fpsCamera.destroy()
            del self.fpsCamera
            self.cannonCamera.destroy()
            del self.cannonCamera
            self.cannonDefenseCamera.destroy()
            del self.cannonDefenseCamera

    def __str__(self):
        outStr = FSM.__str__(self)
        outStr += '(currentCamera: %s)' % self.currentCamera
        return outStr

    def getCurrentCamera(self):
        return self.currentCamera

    def getOrbitCamera(self):
        return self.orbitCamera

    def getFPSCamera(self):
        return self.fpsCamera

    def getCannonCamera(self):
        return self.cannonCamera

    def getCameras(self):
        return self.cameras

    def enableMouseControl(self):
        for camera in self.cameras:
            camera.enableMouseControl()

    def disableMouseControl(self):
        for camera in self.cameras:
            camera.disableMouseControl()

    def defaultFilter(self, request, args):
        if request != self.getCurrentOrNextState():
            return FSM.defaultFilter(self, request, args)
        return None

    def enterOff(self):
        self.currentCamera = None
        return

    def exitOff(self):
        pass

    def enterOrbit(self, subject=None):
        if subject:
            self.orbitCamera.setSubject(subject)
        self.orbitCamera.start()
        self.currentCamera = self.orbitCamera

    def exitOrbit(self):
        self.orbitCamera.setSubject(None)
        self.orbitCamera.stop()
        return

    def enterFPS(self):
        self.fpsCamera.start()
        self.currentCamera = self.fpsCamera

    def exitFPS(self):
        self.fpsCamera.stop()

    def enterCannon(self, cannonProp):
        self.cannonCamera.start(cannonProp)
        self.currentCamera = self.cannonCamera
        localAvatar.hide()
        localAvatar.nametag3d.hide()

    def exitCannon(self):
        self.cannonCamera.stop()
        localAvatar.show()
        localAvatar.nametag3d.show()

    def enterCannonDefense(self, cannonProp):
        self.cannonDefenseCamera.start(cannonProp)
        self.currentCamera = self.cannonDefenseCamera
        localAvatar.nametag3d.hide()

    def exitCannonDefense(self):
        self.cannonDefenseCamera.stop()
        localAvatar.nametag3d.show()

    def enterControl(self):
        self.currentCamera = None
        return

    def exitControl(self):
        pass