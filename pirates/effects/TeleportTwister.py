from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController

class TeleportTwister(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleVolcanoSmoke')
        self.setLightOff()
        self.setColorScaleOff()
        self.setDepthWrite(0)
        self.f = ParticleEffect.ParticleEffect('TeleportDust')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('dust')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('forceGroup-1')
        force0 = LinearCylinderVortexForce(10.0, 10.0, 0.5, 2.25, 0)
        force0.setVectorMasks(1, 1, 0)
        force0.setActive(1)
        f0.addForce(force0)
        force1 = LinearSinkForce(Point3(0.0, 0.0, 0.0), LinearDistanceForce.FTONEOVERRSQUARED, 1.0, 25.0, 0)
        force1.setVectorMasks(1, 1, 0)
        force1.setActive(1)
        f0.addForce(force1)
        force2 = LinearVectorForce(Vec3(0.0, 0.0, 3.0), 1.0, 0)
        force2.setVectorMasks(0, 0, 1)
        force2.setActive(1)
        f0.addForce(force2)
        self.f.addForceGroup(f0)
        self.p0.setPoolSize(32)
        self.p0.setBirthRate(0.1)
        self.p0.setLitterSize(2)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(2.75)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(0.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(90.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(0.8)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(0.8, 0.8, 0.8, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.008 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.015 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.008 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.015 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(2.0)

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.1), Func(self.p0.clearToInitial), Func(self.f.start, self, self), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100), Wait(3.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.5), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
