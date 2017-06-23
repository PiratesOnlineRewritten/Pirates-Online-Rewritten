from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
from otp.otpbase import OTPRender
import random

class VoodooAttuneShield(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_chr_voodooShield')
        self.pulseIval = None
        self.effectModel.setBillboardAxis(0)
        self.effectModel.setDepthWrite(0)
        self.effectModel.setColorScaleOff()
        self.effectModel.setLightOff()
        self.effectModel.setTransparency(1)
        self.effectModel.reparentTo(self)
        self.effectModel.setScale(0.4, 0.4, 0.6)
        self.effectModel.setTwoSided(1)
        self.effectModel.setBin('fixed', 0)
        return

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        uvScroll = LerpFunctionInterval(self.setNewUVs, 1.25, toData=-1.0, fromData=0.0, extraArgs=[self.effectModel, textureStage])
        self.startEffect = Parallel(Func(uvScroll.loop))
        self.endEffect = Sequence(Func(uvScroll.pause), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.0), self.endEffect)

    def pulseEffect(self):
        if not self.pulseIval:
            scaleUp = LerpScaleInterval(self.effectModel, 0.2, Vec3(0.4, 0.4, 1.75), startScale=Vec3(0.4, 0.4, 0.6))
            scaleDown = LerpScaleInterval(self.effectModel, 0.4, Vec3(0.4, 0.4, 0.6), startScale=Vec3(0.4, 0.4, 1.75))
            self.pulseIval = Sequence(scaleUp, scaleDown)
        self.pulseIval.start()

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

    def setEffectColor(self, color):
        self.effectModel.setColorScale(color)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)