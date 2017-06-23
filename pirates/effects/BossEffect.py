from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from EffectController import EffectController
from PooledEffect import PooledEffect

class BossEffect(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.setLightOff()
        self.setColorScaleOff()
        self.setDepthWrite(0)
        self.setBin('fixed', 100)
        self.effectScale = 1.0
        self.effectColor = Vec4(1, 1, 1, 1)
        model = loader.loadModel('models/effects/particleCards')
        self.card = model.find('**/particleSparkles')
        self.cardScale = 64.0
        self.f = ParticleEffect.ParticleEffect('BossEffect')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(16)
        self.p0.setBirthRate(0.0)
        self.p0.setLitterSize(4)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.0)
        self.p0.factory.setLifespanSpread(0.25)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1, 1, 1, 1))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.setEffectScale(self.effectScale)
        self.setEffectColor(self.effectColor)

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.5), Func(self.p0.clearToInitial), Func(self.f.start, self, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(3.0), self.endEffect)

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p0.renderer.setInitialXScale(0.04 * self.effectScale * self.cardScale)
        self.p0.renderer.setFinalXScale(0.08 * self.effectScale * self.cardScale)
        self.p0.renderer.setInitialYScale(0.04 * self.effectScale * self.cardScale)
        self.p0.renderer.setFinalYScale(0.08 * self.effectScale * self.cardScale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.2 * self.effectScale))
        self.p0.emitter.setRadius(self.effectScale)
        self.setScale(1, 1, 2)

    def setEffectColor(self, color):
        self.effectColor = color
        self.p0.renderer.setColor(self.effectColor)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)