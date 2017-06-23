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

class FuseSparks(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.flash = model.find('**/particleSpark')
        self.flash.reparentTo(self)
        self.sparks = loader.loadModel('models/effects/particleSpark_tflip')
        self.sparks.setScale(0.5)
        self.sparks.reparentTo(self)
        self.sparks2 = loader.loadModel('models/effects/particleSpark_tflip')
        self.sparks2.setHpr(0, 0, 45)
        self.sparks2.setScale(0.6)
        self.sparks2.getChild(0).getChild(0).node().pose(3)
        self.sparks2.getChild(0).getChild(0).node().loop(1)
        self.sparks2.reparentTo(self)
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setBillboardPointWorld()
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()

    def createTrack(self):
        scaleFlashUp = LerpScaleInterval(self.flash, 0.1, 1.1, startScale=0.8)
        scaleFlashDown = LerpScaleInterval(self.flash, 0.15, 0.8, startScale=1.3)
        scaleFlashIval = Sequence(scaleFlashUp, scaleFlashDown)
        rotateSparkIval = LerpHprInterval(self.sparks2, 1.0, Vec3(0, 0, 360), startHpr=Vec3(0, 0, 0))
        self.startEffect = Sequence(Func(scaleFlashIval.loop), Func(rotateSparkIval.loop))
        self.endEffect = Sequence(Func(scaleFlashIval.finish), Func(rotateSparkIval.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)