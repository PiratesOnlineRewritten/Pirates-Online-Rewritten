from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
import random
from PooledEffect import PooledEffect
from EffectController import EffectController

class GraveShackles(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.splash = Actor.Actor()
        self.splash.loadModel('models/props/voodoo_chains_zero')
        animDict = {}
        animDict['idle'] = 'models/props/voodoo_chains_idle'
        animDict['grab'] = 'models/props/voodoo_chains_grab'
        self.splash.loadAnims(animDict)
        self.splash.reparentTo(self)
        self.splash.setDepthWrite(0)
        self.splash.setBin('fixed', 10)

    def createTrack(self, rate=1):
        fadeOut = self.splash.colorScaleInterval(1.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(1, 1, 1, 1))
        self.startEffect = Sequence(Func(self.splash.setColorScale, 1, 1, 1, 1), self.splash.actorInterval('grab', playRate=1.0), Func(self.splash.loop, 'idle'))
        self.endEffect = Sequence(self.splash.actorInterval('grab', playRate=-1.0), fadeOut, Func(self.splash.stop), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)

    def cleanUpEffect(self):
        self.detachNode()
        self.checkInEffect(self)

    def destroy(self):
        self.stop()
        self.splash.cleanup()
        del self.splash
        EffectController.destroy(self)
        PooledEffect.destroy(self)