from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class SmokeCloud(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSmoke')
        self.speed = 20.0
        self.radius = 6.0
        self.spriteScale = 1.0
        if not SmokeCloud.particleDummy:
            SmokeCloud.particleDummy = render.attachNewNode(ModelNode('SmokeCloudParticleDummy'))
            SmokeCloud.particleDummy.setDepthWrite(0)
            SmokeCloud.particleDummy.setLightOff()
            SmokeCloud.particleDummy.setColorScaleOff()
        self.f = ParticleEffect.ParticleEffect('SmokeCloud')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(12)
        self.p0.setBirthRate(0.3)
        self.p0.setLitterSize(4)
        self.p0.setLitterSpread(2)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-10.0)
        self.p0.factory.setLifespanBase(1.75)
        self.p0.factory.setLifespanSpread(0.75)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(2000.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(180.0)
        self.p0.factory.enableAngularVelocity(0)
        self.p0.factory.setAngularVelocity(5.0)
        self.p0.factory.setAngularVelocitySpread(1.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.6)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.07 * self.spriteScale * self.cardScale)
        self.p0.renderer.setFinalXScale(0.22 * self.spriteScale * self.cardScale)
        self.p0.renderer.setInitialYScale(0.07 * self.spriteScale * self.cardScale)
        self.p0.renderer.setFinalYScale(0.22 * self.spriteScale * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(5.0)
        self.p0.emitter.setAmplitudeSpread(2.0)
        self.p0.emitter.setOffsetForce(Vec3(5.0, 5.0, 5.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 1.0))
        self.p0.emitter.setRadius(self.radius)

    def createTrack(self):
        self.track = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Wait(1.0), Func(self.p0.setBirthRate, 100), Wait(3.0), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)