from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class WaterRippleSplash(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if parent is not None:
            self.reparentTo(parent)
        if not self.particleDummy:
            self.particleDummy = render.attachNewNode(ModelNode('WaterRippleSplashParticleDummy'))
            self.particleDummy.setDepthWrite(0)
            self.particleDummy.setLightOff()
            self.particleDummy.setFogOff()
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()
        self.setBin('water', 50)
        self.f = ParticleEffect.ParticleEffect('WaterRippleSplash')
        self.f.reparentTo(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSplash')
        self.p1 = Particles.Particles('particles-2')
        self.p1.setFactory('PointParticleFactory')
        self.p1.setRenderer('SpriteParticleRenderer')
        self.p1.setEmitter('DiscEmitter')
        self.f.addParticles(self.p1)
        f0 = ForceGroup.ForceGroup('gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -15.0), 1.0, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)
        self.p1.setPoolSize(24)
        self.p1.setBirthRate(0.02)
        self.p1.setLitterSize(6)
        self.p1.setLitterSpread(1)
        self.p1.setSystemLifespan(0.0)
        self.p1.setLocalVelocityFlag(1)
        self.p1.setSystemGrowsOlderFlag(0)
        self.p1.factory.setLifespanBase(0.5)
        self.p1.factory.setLifespanSpread(0.1)
        self.p1.factory.setMassBase(1.0)
        self.p1.factory.setMassSpread(0.0)
        self.p1.factory.setTerminalVelocityBase(400.0)
        self.p1.factory.setTerminalVelocitySpread(0.0)
        self.p1.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p1.renderer.setUserAlpha(0.2)
        self.p1.renderer.setFromNode(self.card)
        self.p1.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p1.renderer.setXScaleFlag(1)
        self.p1.renderer.setYScaleFlag(1)
        self.p1.renderer.setAnimAngleFlag(0)
        self.p1.renderer.setInitialXScale(0.015 * self.cardScale)
        self.p1.renderer.setFinalXScale(0.005 * self.cardScale)
        self.p1.renderer.setInitialYScale(0.005 * self.cardScale)
        self.p1.renderer.setFinalYScale(0.02 * self.cardScale)
        self.p1.renderer.setNonanimatedTheta(0.0)
        self.p1.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p1.renderer.setAlphaDisable(0)
        self.p1.renderer.getColorInterpolationManager().addLinear(0.6, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(1.0, 1.0, 1.0, 0.0), 1)
        self.p1.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p1.emitter.setAmplitude(1.0)
        self.p1.emitter.setAmplitudeSpread(0.0)
        self.p1.emitter.setOffsetForce(Vec3(0.0, 0.0, 4.0))
        self.p1.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p1.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p1.emitter.setRadius(0.75)
        return

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p1.setBirthRate, 0.02), Func(self.p1.clearToInitial), Func(self.f.start, self, self))
        self.endEffect = Sequence(Func(self.p1.setBirthRate, 100.0), Func(self.cleanUpEffect))
        self.endEffect2 = Sequence(Func(self.p1.setBirthRate, 100.0))
        self.track = Sequence(self.startEffect, Wait(0.5), self.endEffect2)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)