from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPRender
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class EnergySpiral(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/energy_spirals')
        self.effectModel2 = loader.loadModel('models/effects/energy_spirals')
        self.effectModel2.reparentTo(self.effectModel)
        self.effectModel.setBillboardAxis(0)
        self.effectModel.setColorScaleOff()
        self.effectModel.reparentTo(self)
        self.effectColor = Vec4(1, 1, 1, 1)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setColorScaleOff()
        self.setTransparency(0, 0)
        self.hide(OTPRender.ShadowCameraBitmask)

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        self.effectModel.setTexOffset(textureStage, 0.0, 1.0)
        self.effectModel.setScale(0.4, 0.5, 0.5)
        duration = 6.0
        self.setColorScale(1.0, 1.0, 1.0, 0.0)
        fadeIn = LerpColorScaleInterval(self, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), startColorScale=Vec4(0.0, 0.0, 0.0, 0.0))
        fadeOut = LerpColorScaleInterval(self, 1.0, Vec4(0.0, 0.0, 0.0, 0.0), startColorScale=Vec4(1.0, 1.0, 1.0, 1.0))
        scaleIval = LerpScaleInterval(self.effectModel, duration, Vec3(1.0, 1.0, 4.0), startScale=Vec3(1.0, 1.0, 4.0))
        uvScroll = LerpFunctionInterval(self.setNewUVs, duration / 4.0, toData=-1.0, fromData=1.0, extraArgs=[self.effectModel, textureStage])
        self.startEffect = Sequence(Func(uvScroll.loop), fadeIn)
        self.endEffect = Sequence(fadeOut, Func(uvScroll.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(duration), self.endEffect)

    def setEffectColor(self, color):
        self.effectColor = Vec4(1, 1, 1, 1) - (Vec4(1, 1, 1, 1) - color) / 4.0 + Vec4(0.1, 0.1, 0, 1)
        self.effectModel.setColorScale(self.effectColor)

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        self.stop()
        if self.track:
            self.track = None
        self.removeNode()
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return