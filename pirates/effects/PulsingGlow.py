from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect

class PulsingGlow(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.fadeTime = 0.15
        self.duration = 0.35
        self.effectColor = Vec4(1, 1, 1, 1)
        self.modelParent = self.attachNewNode('ModelParent')
        model = loader.loadModel('models/effects/particleCards')
        self.effectModel = model.find('**/particleWhiteGlow')
        self.effectModel.reparentTo(self.modelParent)
        model = loader.loadModel('models/effects/particleCards')
        self.effectModel2 = model.find('**/particleWhiteGlow')
        self.effectModel2.reparentTo(self.modelParent)
        self.setBillboardAxis(0)
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setBillboardPointWorld()
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()

    def createTrack(self):
        self.setColorScale(self.effectColor)
        self.modelParent.setScale(1.0)
        fadeBlast = self.colorScaleInterval(0.75, Vec4(0, 0, 0, 0), startColorScale=Vec4(self.effectColor), blendType='easeIn')
        scaleBlast = self.modelParent.scaleInterval(0.75, 15, startScale=1.25, blendType='easeOut')
        scalePulse = Sequence(self.effectModel.scaleInterval(0.1, Vec3(4.5, 2.0, 2.0), startScale=Vec3(1.8, 1.8, 1.8), blendType='easeIn'), self.effectModel.scaleInterval(0.1, Vec3(1.8, 1.8, 1.8), startScale=Vec3(4.5, 2.0, 2.0), blendType='easeOut'))
        scalePulse2 = Sequence(self.effectModel2.scaleInterval(0.12, Vec3(1.8, 1.8, 1.8), startScale=Vec3(2.0, 2.0, 4.5), blendType='easeIn'), self.effectModel2.scaleInterval(0.12, Vec3(2.0, 2.0, 4.5), startScale=Vec3(1.8, 1.8, 1.8), blendType='easeOut'))
        self.startEffect = Parallel(Func(scalePulse.loop), Func(scalePulse2.loop))
        self.endEffect = Sequence(Parallel(scaleBlast, fadeBlast), Func(scalePulse.pause), Func(scalePulse2.pause), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def setEffectColor(self, color):
        self.effectColor = color

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)