from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class GhostAura(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSmoke')
        self.transparency = 0.25
        self.setDepthWrite(0)
        self.setFogOff()
        self.setLightOff()
        self.setColorScaleOff()
        self.effectScale = 0.6
        self.duration = 1.0
        self.f = ParticleEffect.ParticleEffect('GhostAura')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('BoxEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(48)
        self.p0.setBirthRate(0.075)
        self.p0.setLitterSize(2)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-1.0)
        self.p0.factory.setLifespanBase(1.1)
        self.p0.factory.setLifespanSpread(0.25)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(0.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(0.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(50.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-0.5)
        self.p0.emitter.setAmplitudeSpread(0.18)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 5.0))
        self.p0.emitter.setMinBound(Point3(-1.0, -1.0, -0.5))
        self.p0.emitter.setMaxBound(Point3(1.0, 1.0, 7.0))
        self.setEffectScale(1.0)

    def beThick(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            self.transparency = 0.5
            self.p0.setPoolSize(72)
            self.p0.setLitterSize(3)
            self.p0.setBirthRate(0.075)
        else:
            self.transparency = 1.0
            self.p0.setPoolSize(48)
            self.p0.setLitterSize(2)
            self.p0.setBirthRate(0.125)
        self.p0.renderer.setUserAlpha(self.transparency)

    def beWide(self):
        self.p0.emitter.setMinBound(Point3(-1.5, -1.5, -0.5))
        self.p0.emitter.setMaxBound(Point3(1.5, 1.5, 7.0))

    def beOrb(self):
        self.p0.emitter.setMinBound(Point3(-1.0, -1.0, 3.5))
        self.p0.emitter.setMaxBound(Point3(1.0, 1.0, 7.0))

    def bePositive(self):
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)

    def beNegative(self):
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MInvSubtract, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        base.gc = self

    def setBmode(self, m1, m2, m3):
        self.p0.renderer.setColorBlendMode(m1, m2, m3)

    def beNormal(self):
        self.p0.emitter.setMinBound(Point3(-1.0, -1.0, -0.5))
        self.p0.emitter.setMaxBound(Point3(1.0, 1.0, 7.0))
        self.p0.emitter.setAmplitude(-0.5)
        self.p0.emitter.setAmplitudeSpread(0.18)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.setPoolSize(48)
        self.p0.setLitterSize(2)
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            self.transparency = 0.25
            self.p0.setPoolSize(48)
            self.p0.setLitterSize(2)
            self.p0.setBirthRate(0.075)
        else:
            self.transparency = 0.5
            self.p0.setPoolSize(48)
            self.p0.setLitterSize(1)
            self.p0.setBirthRate(0.075)
        self.p0.renderer.setUserAlpha(self.transparency)

    def moveDown(self):
        self.p0.emitter.setAmplitude(-0.5)
        self.p0.emitter.setAmplitudeSpread(0.5)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, -3.5))

    def createTrack(self):
        self.p0.renderer.setUserAlpha(self.transparency)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.05), Func(self.p0.clearToInitial), Func(self.f.start, self, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p0.renderer.setInitialXScale(0.045 * self.cardScale * self.effectScale)
        self.p0.renderer.setInitialYScale(0.04 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalXScale(0.015 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalYScale(0.03 * self.cardScale * self.effectScale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0 * self.effectScale))

    def cleanUpEffect(self):
        if self.isEmpty():
            return
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)