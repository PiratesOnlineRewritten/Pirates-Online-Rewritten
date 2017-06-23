from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
import random
from pirates.piratesbase import PiratesGlobals
from PooledEffect import PooledEffect
from EffectController import EffectController
from otp.otpbase import OTPRender

class MusketShot(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.flame = model.find('**/particleGlow')
        self.flame.setBillboardAxis(0)
        self.flame.setPos(0, 0, 0.5)
        self.flame.reparentTo(self)
        self.flash = model.find('**/particleSpark')
        self.flash.setBillboardPointWorld(0.2)
        self.flash.reparentTo(self)
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.hide(OTPRender.ShadowCameraBitmask)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()

    def createTrack(self):
        scaleFlame = self.flame.scaleInterval(0.06, Vec3(1, 1, 4), startScale=Vec3(5, 5, 8))
        scaleFlash = self.flash.scaleInterval(0.04, 1.5, startScale=3)
        fadeFlash = LerpColorScaleInterval(self, 0.2, Vec4(0.4, 0.1, 0.1, 1), startColorScale=Vec4(1, 1, 1, 1))
        self.track = Sequence(Func(self.flame.show), Func(self.flash.show), Parallel(scaleFlame, scaleFlash, fadeFlash), Func(self.flame.hide), Func(self.flash.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)