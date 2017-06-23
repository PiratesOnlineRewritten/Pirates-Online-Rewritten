from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class WaterRippleWake(PooledEffect, EffectController):

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if parent is not None:
            self.reparentTo(parent)
        if not WaterRippleWake.particleDummy:
            WaterRippleWake.particleDummy = render.attachNewNode(ModelNode('WaterRippleWakeParticleDummy'))
            WaterRippleWake.particleDummy.setDepthWrite(0)
            WaterRippleWake.particleDummy.setFogOff()
            WaterRippleWake.particleDummy.setBin('water', 50)
        self.f = ParticleEffect.ParticleEffect('WaterRippleWake')
        self.f.reparentTo(self)
        self.effectGeom = loader.loadModel('models/effects/ripple')
        if not self.effectGeom:
            self.effectGeom = loader.loadModel('models/misc/smiley')
        self.p1 = Particles.Particles('particles-2')
        self.p1.setFactory('PointParticleFactory')
        self.p1.setRenderer('GeomParticleRenderer')
        self.p1.setEmitter('DiscEmitter')
        self.f.addParticles(self.p1)
        self.p1.setPoolSize(32)
        self.p1.setBirthRate(0.75)
        self.p1.setLitterSize(4)
        self.p1.setLitterSpread(1)
        self.p1.setSystemLifespan(0.0)
        self.p1.setLocalVelocityFlag(1)
        self.p1.setSystemGrowsOlderFlag(0)
        self.p1.factory.setLifespanBase(1.75)
        self.p1.factory.setLifespanSpread(1.0)
        self.p1.factory.setMassBase(1.0)
        self.p1.factory.setMassSpread(0.0)
        self.p1.factory.setTerminalVelocityBase(400.0)
        self.p1.factory.setTerminalVelocitySpread(0.0)
        self.p1.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p1.renderer.setUserAlpha(0.75)
        self.p1.renderer.setGeomNode(self.effectGeom.node())
        self.p1.renderer.setXScaleFlag(1)
        self.p1.renderer.setYScaleFlag(1)
        self.p1.renderer.setZScaleFlag(1)
        self.p1.renderer.setInitialXScale(0.75)
        self.p1.renderer.setFinalXScale(10.0)
        self.p1.renderer.setInitialYScale(0.75)
        self.p1.renderer.setFinalYScale(10.0)
        self.p1.renderer.setInitialZScale(0.75)
        self.p1.renderer.setFinalZScale(10.0)
        self.p1.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p1.emitter.setAmplitude(1.0)
        self.p1.emitter.setAmplitudeSpread(0.0)
        self.p1.emitter.setOffsetForce(Vec3(0.0, 0.0, -0.01))
        self.p1.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p1.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p1.emitter.setRadius(1.0)
        return

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p1.setBirthRate, 0.1), Func(self.p1.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.p1.setBirthRate, 100.0), Wait(2.0), Func(self.p1.setBirthRate, 0.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.0), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)