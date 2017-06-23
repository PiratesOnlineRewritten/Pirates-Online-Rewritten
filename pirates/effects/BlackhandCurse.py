from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from otp.otpbase import OTPRender
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class BlackhandCurse(PooledEffect, EffectController):
    cardScale = 128.0
    cardScale2 = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.modelParent = self.attachNewNode('ModelParent')
        model = loader.loadModel('models/effects/particleCards')
        self.effectModel = model.find('**/particleWhiteGlow')
        self.effectModel.reparentTo(self.modelParent)
        model = loader.loadModel('models/effects/particleCards')
        self.effectModel2 = model.find('**/particleWhiteGlow')
        self.effectModel2.reparentTo(self.modelParent)
        self.modelParent.setBillboardAxis(0)
        self.modelParent.setBillboardPointWorld()
        self.modelParent.setBin
        self.modelParent.setScale(1.0)
        self.modelParent.setColorScale(0, 0, 0, 1.0)
        self.modelParent.setBin('fixed', 0)
        self.setDepthWrite(0)
        self.setFogOff()
        self.setLightOff()
        self.setColorScaleOff()
        self.hide(OTPRender.ShadowCameraBitmask)

    def createTrack(self):
        scalePulse = Sequence(self.effectModel.scaleInterval(0.15, Vec3(1.2, 1.2, 1.2), startScale=Vec3(0.6, 0.6, 0.6), blendType='easeIn'), self.effectModel.scaleInterval(0.15, Vec3(0.6, 0.6, 0.6), startScale=Vec3(1.2, 1.2, 1.2), blendType='easeOut'))
        self.modelParent.setColorScale(0, 0, 0, 1.0)
        fadeOut = self.modelParent.colorScaleInterval(1.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(0, 0, 0, 1.0), blendType='easeIn')
        self.startEffect = Sequence(Func(scalePulse.loop))
        self.endEffect = Sequence(fadeOut, Func(scalePulse.pause), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(3.0), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)