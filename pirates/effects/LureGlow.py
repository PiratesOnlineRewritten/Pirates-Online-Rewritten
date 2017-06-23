from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect

class LureGlow(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleCards')
        self.effectModel = model.find('**/particleSparkle')
        self.effectModel.reparentTo(self)
        self.effectColor = Vec4(1, 1, 1, 1)
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setTransparency(True)
        self.setColorScaleOff()
        self.setBillboardPointEye()
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()
        self.effectModel.hide()

    def createTrack(self):
        self.effectModel.hide()
        self.effectModel.setColorScale(self.effectColor)
        pulseIval = Sequence(LerpScaleInterval(self.effectModel, duration=0.15, scale=3.5), LerpScaleInterval(self.effectModel, duration=0.15, scale=1.0))
        self.startEffect = Sequence(Func(self.effectModel.show), Func(pulseIval.loop))
        self.endEffect = Sequence(Func(pulseIval.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.0), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)