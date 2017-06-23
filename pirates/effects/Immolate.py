from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class Immolate(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleFlameSmoke')
        self.speed = 1.0
        if not Immolate.particleDummy:
            Immolate.particleDummy = render.attachNewNode(ModelNode('ImmolateParticleDummy'))
            Immolate.particleDummy.setDepthWrite(0)
            Immolate.particleDummy.setLightOff()
            Immolate.particleDummy.setColorScaleOff()
        self.f = ParticleEffect.ParticleEffect('Immolate')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(24)
        self.p0.setBirthRate(0.1)
        self.p0.setLitterSize(3)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(4.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.25)
        self.p0.factory.setLifespanSpread(0.5)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(20.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAIN)
        self.p0.renderer.setUserAlpha(1)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1, 1, 1, 1))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.03 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.075 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.03 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.06 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOne)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(0.8, 0.65, 0.65, 0.5), Vec4(0.0, 0.0, 0.0, 0.0), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(3.0)
        self.p0.emitter.setAmplitudeSpread(1.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, -0.6))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(2.0)

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100), Wait(3.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(0.5), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)