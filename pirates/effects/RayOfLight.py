from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController

class RayOfLight(NodePath, EffectController):

    def __init__(self):
        NodePath.__init__(self, 'RayOfLight')
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_msc_rayOfLight')
        self.effectModel.setColorScale(Vec4(0, 0, 0, 0))
        self.effectModel.reparentTo(self)
        self.mainRay = self.effectModel.find('**/ray_main')
        self.mainRay.setHpr(0, 20, -10)
        self.bottomRay = self.effectModel.find('**/ray_bottom')
        self.bottomRay.stash()
        self.bottomRayEnabled = False
        self.adjustIval = None
        self.mainAnimNode = None
        self.mainAnim = None
        self.bootomAnimNode = None
        self.bottomAnim = None
        self.effectScale = 1.0
        self.av = None
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setBillboardPointWorld()
        self.setTransparency(1)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()
        return

    @report(types=['args'], dConfigParam='quest-indicator')
    def destroy(self):
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None
        if self.mainAnim:
            self.mainAnim.pause()
            self.mainAnim = None
        if self.bottomAnim:
            self.bottomAnim.pause()
            self.bottomAnim = None
        self.stopAdjustTask()
        EffectController.destroy(self)
        NodePath.detachNode(self)
        return

    def setBottomRayEnabled(self, enabled):
        self.bottomRayEnabled = enabled

    @report(types=['args'], dConfigParam='quest-indicator')
    def createTrack(self):
        if self.av and not self.av.isEmpty():
            distance = self.getDistance(self.av)
            self.effectModel.setScale(Vec3(0.25 * (1 + distance / 50.0)))
        self.mainAnimNode = NodePath('mainAnimNode')
        self.mainAnim = LerpPosInterval(self.mainAnimNode, startPos=VBase3(0, 0, 0), pos=VBase3(2.0, 1.0, 0.0), duration=10.0)
        self.mainRay.setTexProjector(TextureStage.getDefault(), self.mainAnimNode, NodePath())

        @report(types=['args'], dConfigParam='quest-indicator')
        def startBottomEffect():
            if self.bottomRayEnabled:
                self.bottomRay.unstash()
                self.bottomAnimNode = NodePath('bottomAnimNode')
                self.bottomAnim = LerpPosInterval(self.bottomAnimNode, startPos=VBase3(0, 0, 0), pos=VBase3(0.0, -1.0, 0.0), duration=3.0)
                self.bottomRay.setTexProjector(TextureStage.getDefault(), self.bottomAnimNode, NodePath())
                self.bottomAnim.loop()
            else:
                self.bottomRay.stash()

        @report(types=['args'], dConfigParam='quest-indicator')
        def stopBottomEffect():
            if self.bottomRayEnabled and self.bottomAnim:
                self.bottomAnim.finish()

        fadeInEffect = LerpColorScaleInterval(self.effectModel, 1.5, Vec4(1, 1, 1, 1), startColorScale=Vec4(0, 0, 0, 0))
        fadeOutEffect = LerpColorScaleInterval(self.effectModel, 1.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(1, 1, 1, 1))
        self.startEffect = Sequence(Func(self.mainAnim.loop), Func(startBottomEffect), Func(self.startAdjustTask), fadeInEffect, Func(self.startAdjustTask))
        self.endEffect = Sequence(fadeOutEffect, Func(self.mainAnim.finish), Func(stopBottomEffect), Func(self.reallyCleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(3.0), self.endEffect)

    @report(types=['args'], dConfigParam='quest-indicator')
    def startAdjustTask(self):
        self.stopAdjustTask()
        if localAvatar and not localAvatar.isEmpty():
            self.av = localAvatar
            task = taskMgr.doMethodLater(1, self.adjustTask, 'RayOfLightAdjustTask')
            self.adjustTask(task)

    @report(types=['args'], dConfigParam='quest-indicator')
    def stopAdjustTask(self):
        taskMgr.remove('RayOfLightAdjustTask')
        self.av = None
        if self.adjustIval:
            self.adjustIval.pause()
            self.adjustIval = None
        return

    @report(types=['args'], dConfigParam='quest-indicator')
    def adjustTask(self, task):
        if self.av and not self.av.isEmpty():
            distance = self.getDistance(self.av)
            newScale = Vec3(0.25 * (1 + distance / 50.0))
            if self.adjustIval:
                self.adjustIval.pause()
                self.adjustIval = None
            self.adjustIval = self.effectModel.scaleInterval(1, newScale)
            self.adjustIval.start()
            return task.again
        return

    @report(types=['args'], dConfigParam='quest-indicator')
    def reallyCleanUpEffect(self):
        self.stopAdjustTask()
        EffectController.reallyCleanUpEffect(self)