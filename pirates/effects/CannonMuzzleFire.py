from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
import random
from PooledEffect import PooledEffect
from EffectController import EffectController

class CannonMuzzleFire(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.splash = Actor.Actor()
        self.splash.loadModel('models/effects/cannonMuzzleFlash-zero')
        animDict = {}
        animDict['splashdown'] = 'models/effects/cannonMuzzleFlash-anim'
        self.splash.loadAnims(animDict)
        self.splash.reparentTo(self)
        self.splash.setTransparency(1)
        self.splash.setDepthWrite(0)
        self.splash.setColorScaleOff()
        self.splash.setLightOff()
        self.splash.setFogOff()

    def createTrack(self, rate=1):
        self.splash.setPlayRate(rate, 'splashdown')
        animDuration = self.splash.getDuration('splashdown') * 0.3
        fadeOut = self.splash.colorInterval(0.6, Vec4(1, 1, 1, 0), startColor=Vec4(1, 1, 1, 1))
        self.track = Sequence(Func(self.splash.setColor, 1, 1, 1, 1), Func(self.splash.play, 'splashdown'), Wait(animDuration), fadeOut, Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        self.detachNode()
        self.checkInEffect(self)

    def destroy(self):
        self.stop()
        self.splash.cleanup()
        del self.splash
        EffectController.destroy(self)
        PooledEffect.destroy(self)