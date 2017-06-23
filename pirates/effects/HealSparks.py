from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from PooledEffect import PooledEffect
from EffectController import EffectController
import os

class HealSparks(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSpark')
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()
        self.setColorScaleOff()
        self.effectColor = Vec4(1, 1, 1, 1)
        self.f = ParticleEffect.ParticleEffect('HealSparks')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.05)
        self.p0.setLitterSize(4)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.5)
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
        self.p0.renderer.setInitialXScale(0.001 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.004 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.001 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.005 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(1.0)

    def createTrack(self, delay=0.0):
        self.p0.renderer.setInitialXScale(0.001 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.004 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.001 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.005 * self.cardScale)
        self.startEffect = Sequence(Wait(delay), Func(self.p0.clearToInitial), Func(self.p0.softStart), Func(self.f.start, self, self))
        self.endEffect = Sequence(Func(self.p0.softStop), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(3.0), self.endEffect)

    def setEffectColor(self, color):
        self.effectColor = color
        self.p0.renderer.getColorInterpolationManager().clearToInitial()
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, self.effectColor * 2.0, self.effectColor, 1)

    def play(self, delay=0.0):
        self.createTrack(delay)
        self.track.start()

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        self.adjustIval = None
        return