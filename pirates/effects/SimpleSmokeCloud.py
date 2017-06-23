from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class SimpleSmokeCloud(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSmoke')
        if not SimpleSmokeCloud.particleDummy:
            SimpleSmokeCloud.particleDummy = render.attachNewNode(ModelNode('SimpleSmokeCloudParticleDummy'))
            SimpleSmokeCloud.particleDummy.setColorScaleOff()
            SimpleSmokeCloud.particleDummy.setDepthWrite(0)
            SimpleSmokeCloud.particleDummy.setLightOff()
        self.f = ParticleEffect.ParticleEffect('SimpleSmokeCloud')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(3)
        self.p0.setBirthRate(0.1)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.5)
        self.p0.factory.setLifespanSpread(0.25)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(2000.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(180.0)
        self.p0.factory.enableAngularVelocity(0)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 1.0))
        self.setEffectScale(1.0)

    def createTrack(self):
        self.track = Sequence(Wait(0.1), Func(self.p0.setBirthRate, 0.1), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Wait(1.0), Func(self.p0.setBirthRate, 100), Wait(3.0), Func(self.cleanUpEffect))

    def setEffectScale(self, scale):
        self.p0.renderer.setInitialXScale(0.05 * self.cardScale * scale)
        self.p0.renderer.setFinalXScale(0.25 * self.cardScale * scale)
        self.p0.renderer.setInitialYScale(0.05 * self.cardScale * scale)
        self.p0.renderer.setFinalYScale(0.3 * self.cardScale * scale)
        self.p0.emitter.setAmplitude(6.0 * scale)
        self.p0.emitter.setAmplitudeSpread(2.0 * scale)
        self.p0.emitter.setOffsetForce(Vec3(2.5, 2.5, 5.0) * scale)
        self.p0.emitter.setRadius(6.0 * scale)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)