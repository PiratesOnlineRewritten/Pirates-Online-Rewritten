from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class SmokeBomb(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleWhiteSmoke')
        self.speed = 20.0
        self.radius = 8.0
        if not SmokeBomb.particleDummy:
            SmokeBomb.particleDummy = render.attachNewNode(ModelNode('SmokeBombParticleDummy'))
            SmokeBomb.particleDummy.setDepthWrite(0)
            SmokeBomb.particleDummy.setLightOff()
            SmokeBomb.particleDummy.setFogOff()
            SmokeBomb.particleDummy.setBin('fixed', 120)
        self.f = ParticleEffect.ParticleEffect('SmokeBomb')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereSurfaceEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('Gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -15.0), 1.0, 0)
        force0.setVectorMasks(1, 1, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)
        f1 = ForceGroup.ForceGroup('Noise')
        force1 = LinearNoiseForce(0.5, 0)
        force1.setVectorMasks(1, 1, 1)
        force1.setActive(1)
        f1.addForce(force1)
        self.f.addForceGroup(f1)
        self.p0.setPoolSize(128)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(5)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(2.5)
        self.p0.factory.setLifespanSpread(0.5)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(0.8, 0.8, 0.8, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.05 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.25 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.1 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.2 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOneMinusFbufferAlpha, ColorBlendAttrib.OOneMinusIncomingAlpha)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 0.8, Vec4(0.75, 0.75, 0.75, 1.0), Vec4(0.4, 0.4, 0.2, 0.5), 1)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.8, 1.0, Vec4(0.4, 0.4, 0.2, 0.5), Vec4(0.0, 0.0, 0.0, 0.0), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(10.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 4.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(8.0)

    def createTrack(self):
        self.track = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Wait(0.5), Func(self.p0.setBirthRate, 100), Wait(10.0), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)