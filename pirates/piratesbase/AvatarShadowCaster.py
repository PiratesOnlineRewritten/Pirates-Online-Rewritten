from pandac.PandaModules import *
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from otp.otpbase import OTPRender
from otp.avatar import ShadowCaster
from pirates.piratesbase import TODGlobals

class AvatarShadowCaster(DirectObject):

    def __init__(self, lightSrc):
        DirectObject.__init__(self)
        self.lightSrc = lightSrc
        self.shadowCamArm = None
        self.casterState = None
        self.shadowBuffer = None
        self.shadowColor = 0.5
        self.shadowColorIndex = 0
        self.shadowsEnabled = 0
        self.clearColor = VBase4(1, 1, 1, 1)
        self.setupTask = None
        self.shadowsHidden = False
        return

    def enable(self, fMoreShadows=False):
        self.fMoreShadows = fMoreShadows
        self.disable()
        self.shadowsEnabled = 1
        ShadowCaster.setGlobalDropShadowFlag(0)
        camNode = Camera('shadowCam')
        camNode.setCameraMask(OTPRender.ShadowCameraBitmask)
        self.shadowLens = OrthographicLens()
        if fMoreShadows:
            self.shadowLens.setFilmSize(60 * 4, 60 * 4)
        else:
            self.shadowLens.setFilmSize(60, 60)
        camNode.setLens(self.shadowLens)
        self.shadowCamArm = base.camera.attachNewNode('shadowCamArm')
        self.shadowCam = self.shadowCamArm.attachNewNode(camNode)
        self.shadowCamArm.setPos(0, 40, 0)
        self.shadowCam.setPos(0, -40, 0)
        taskName = 'shadowCamCompass'
        taskMgr.remove(taskName)

        def applyCompassEffect(task, self=self):
            self.shadowCamArm.setHpr(self.lightSrc, 0, 0, 0)
            self.shadowCamArm.setScale(1)
            return Task.cont

        taskMgr.add(applyCompassEffect, taskName, priority=46)
        self.shadowTex = Texture('shadow')
        self.shadowTex.setBorderColor(self.clearColor)
        self.shadowTex.setWrapU(Texture.WMBorderColor)
        self.shadowTex.setWrapV(Texture.WMBorderColor)
        self.casterState = NodePath('temp')
        self.casterState.setColorScaleOff(10)
        self.casterState.setColor(self.shadowColor, self.shadowColor, self.shadowColor, 1, 10)
        self.casterState.setTextureOff(10)
        self.casterState.setLightOff(10)
        self.casterState.setFogOff(10)
        camNode.setInitialState(self.casterState.getState())
        render.hide(OTPRender.ShadowCameraBitmask)
        self.shadowStage = TextureStage('shadow')
        self.shadowStage.setSort(1000)
        self.turnOnShadows()

    def hideShadows(self):
        if self.shadowsHidden:
            return
        self.shadowsHidden = True
        self.turnOffShadows()

    def showShadows(self):
        if not self.shadowsHidden:
            return
        self.shadowsHidden = False
        self.turnOnShadows()

    def turnOnShadows(self):
        if self.shadowsHidden or not self.shadowsEnabled:
            return
        self.turnOffShadows()
        render.setTexProjector(self.shadowStage, NodePath(), self.shadowCam)
        self.__createBuffer()
        self.accept('close_main_window', self.__destroyBuffer)
        self.accept('open_main_window', self.__createBuffer)
        self.accept('texture_state_changed', self.__createBuffer)

    def turnOffShadows(self):
        render.clearTexProjector(self.shadowStage)
        self.__destroyBuffer()
        self.ignore('close_main_window')
        self.ignore('open_main_window')
        self.ignore('texture_state_changed')

    def disable(self):
        if not self.shadowsEnabled:
            return
        self.shadowsEnabled = 0
        taskName = 'shadowCamCompass'
        taskMgr.remove(taskName)
        self.shadowCamArm.removeNode()
        self.shadowCam.removeNode()
        if base.main_rtt:
            cam = base.main_rtt.camera_node_path.node()
            if cam:
                cam.clearTagState('caster')
        else:
            base.camNode.clearTagState('caster')
        self.turnOffShadows()
        self.shadowTex = None
        self.shadowStage = None
        ShadowCaster.setGlobalDropShadowFlag(1)
        return

    def setLightSrc(self, light):
        if not self.shadowsEnabled:
            self.lightScr = light
            return
        self.disable()
        self.lightScr = light
        self.enable()

    def updateShadows(self, h):
        while h < TODGlobals.ShadowColorTable[self.shadowColorIndex][0]:
            self.shadowColorIndex -= 1

        while h > TODGlobals.ShadowColorTable[self.shadowColorIndex + 1][0]:
            self.shadowColorIndex += 1

        prevH, prevColor = TODGlobals.ShadowColorTable[self.shadowColorIndex]
        nextH, nextColor = TODGlobals.ShadowColorTable[self.shadowColorIndex + 1]
        dt = (h - prevH) / (nextH - prevH)
        grayLevel = dt * (nextColor - prevColor) + prevColor
        if h == 0:
            self.hideShadows()
        else:
            self.showShadows()
        if self.shadowColor != grayLevel:
            self.shadowColor = grayLevel
            ShadowCaster.setGlobalDropShadowGrayLevel(1.0 - grayLevel)
            if self.shadowsEnabled:
                self.casterState.setColor(grayLevel, grayLevel, grayLevel, 1, 10)
                self.shadowCam.node().setInitialState(self.casterState.getState())

    def updateShadowAmount(self, amount):
        grayLevel = amount
        if self.shadowColor != grayLevel:
            self.shadowColor = grayLevel
            ShadowCaster.setGlobalDropShadowGrayLevel(1.0 - grayLevel)
            if self.shadowsEnabled:
                self.casterState.setColor(grayLevel, grayLevel, grayLevel, 1, 10)
                self.shadowCam.node().setInitialState(self.casterState.getState())

    def __createBuffer(self):
        if self.shadowsHidden or not self.shadowsEnabled:
            return
        self.__destroyBuffer()
        if not base.win.getGsg():
            return
        if self.fMoreShadows:
            self.shadowBuffer = base.win.makeTextureBuffer('shadow', 1024 * 4, 1024 * 4, tex=self.shadowTex)
        else:
            self.shadowBuffer = base.win.makeTextureBuffer('shadow', 1024, 1024, tex=self.shadowTex)
        self.shadowBuffer.setSort(30)
        self.shadowBuffer.setClearColor(self.clearColor)
        dr = self.shadowBuffer.makeDisplayRegion()
        dr.setCamera(self.shadowCam)
        self.setupTask = taskMgr.doMethodLater(0, self.__setupCamera, 'setupCamera')

    def __setupCamera(self, task):
        groundState = NodePath('temp')
        groundState.setTexture(self.shadowStage, self.shadowTex)
        groundState.setTexGen(self.shadowStage, TexGenAttrib.MWorldPosition)
        if base.main_rtt:
            cam = base.main_rtt.camera_node_path.node()
            if cam:
                cam.setTagStateKey('cam')
                cam.setTagState('shground', groundState.getState())
        else:
            base.camNode.setTagStateKey('cam')
            base.camNode.setTagState('shground', groundState.getState())
            if base.wantEnviroDR:
                base.enviroCam.node().setTagStateKey('cam')
                base.enviroCam.node().setTagState('shground', groundState.getState())
        self.setupTask = None
        return task.done

    def __destroyBuffer(self):
        if self.shadowBuffer:
            base.graphicsEngine.removeWindow(self.shadowBuffer)
            self.shadowBuffer = None
        if self.setupTask:
            taskMgr.remove(self.setupTask)
            self.setupTask = None
        return