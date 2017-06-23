from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class SmokePillar(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSmoke')
        self.speed = 20.0
        self.radius = 7.0
        self.spriteScale = 1.0
        if not SmokePillar.particleDummy:
            SmokePillar.particleDummy = render.attachNewNode(ModelNode('SmokePillarParticleDummy'))
            SmokePillar.particleDummy.setDepthWrite(0)
            SmokePillar.particleDummy.setLightOff()
        self.f = ParticleEffect.ParticleEffect('SmokePillar')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -40.0), 1.0, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)

    def createTrack(self):
        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.3)
        self.p0.setLitterSize(10)
        self.p0.setLitterSpread(4)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-10.0)
        self.p0.factory.setLifespanBase(1.0)
        self.p0.factory.setLifespanSpread(0.5)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.95)
        self.p0.factory.setTerminalVelocityBase(2000.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(30.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(5.0)
        self.p0.factory.setAngularVelocitySpread(1.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.6)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.12 * self.spriteScale * self.cardScale)
        self.p0.renderer.setFinalXScale(0.35 * self.spriteScale * self.cardScale)
        self.p0.renderer.setInitialYScale(0.12 * self.spriteScale * self.cardScale)
        self.p0.renderer.setFinalYScale(0.35 * self.spriteScale * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(5.0)
        self.p0.emitter.setAmplitudeSpread(2.0)
        self.p0.emitter.setOffsetForce(Vec3(5.0, 5.0, 60.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 1.0))
        self.p0.emitter.setRadius(self.radius)
        self.track = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Wait(0.3), Func(self.p0.setBirthRate, 100), Wait(7.0), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)