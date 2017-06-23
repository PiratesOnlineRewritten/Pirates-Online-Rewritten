from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from PooledEffect import PooledEffect
from EffectController import EffectController
from otp.otpbase import OTPRender
import random

class DarkPortal(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.speed = 0.75
        self.holdTime = 2.5
        self.size = 40
        self.explosionSequence = 0
        self.explosion = loader.loadModel('models/effects/darkPortal')
        self.explosion.setDepthTest(0)
        self.setDepthWrite(0)
        self.explosion.setFogOff()
        self.explosion.setLightOff()
        self.explosion.setHpr(0, -90, 0)
        self.explosion.reparentTo(self)
        self.hide()
        self.explosion.hide(OTPRender.MainCameraBitmask)
        self.explosion.showThrough(OTPRender.EnviroCameraBitmask)
        self.explosion.setBin('shadow', 0)
        self.explosion.setTransparency(TransparencyAttrib.MAlpha)
        self.explosion.setDepthWrite(0)

    def createTrack(self, rate=1):
        self.explosion.setScale(1)
        self.explosion.setColorScale(1, 1, 1, 0.75)
        scaleUp = self.explosion.scaleInterval(self.speed, self.size, startScale=0.0, blendType='easeIn', other=render)
        scaleDown = self.explosion.scaleInterval(self.speed, 0.0, startScale=self.size, blendType='easeIn', other=render)
        self.track = Sequence(Func(self.show), scaleUp, Wait(self.holdTime), scaleDown, Func(self.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)