from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from PooledEffect import PooledEffect
from EffectController import EffectController

class SwordThunders(PooledEffect, EffectController):

    def __init__(self, effectParent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.duration = 10.0
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_chr_swordThunders')
        self.effectModel.reparentTo(self)
        self.effectModel2 = loader.loadModel('models/effects/pir_m_efx_chr_swordThunders')
        self.effectModel2.reparentTo(self)
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setTwoSided(1)
        self.setDepthWrite(0)
        self.setColorScaleOff()
        self.setLightOff()
        self.setFogOff()

    def createTrack(self):
        flipIval = Sequence(Func(self.effectModel.setR, 0), Wait(0.1), Func(self.effectModel.setR, 90), Wait(0.1), Func(self.effectModel.setR, 180), Wait(0.1), Func(self.effectModel.setR, 270), Wait(0.1))
        flipIval2 = Sequence(Func(self.effectModel2.setR, 90), Wait(0.12), Func(self.effectModel2.setR, 180), Wait(0.12), Func(self.effectModel2.setR, 270), Wait(0.12), Func(self.effectModel2.setR, 0), Wait(0.12))
        self.startEffect = Sequence(Func(flipIval.loop), Func(flipIval2.loop))
        self.endEffect = Sequence(Func(flipIval.pause), Func(flipIval2.pause), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)