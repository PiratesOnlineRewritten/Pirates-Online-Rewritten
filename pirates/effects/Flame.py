from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class Flame(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleFire2')
        self.setDepthWrite(0)
        self.setFogOff()
        self.setLightOff()
        self.setColorScaleOff()
        self.effectScale = 1.0
        self.duration = 0.0
        self.f = ParticleEffect.ParticleEffect('Flame')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(128)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(6)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-1.0)
        self.p0.factory.setLifespanBase(0.75)
        self.p0.factory.setLifespanSpread(0.25)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(0.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(350.0)
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
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(1.0, 0.6, 0.2, 1.0), Vec4(0.6, 0.2, 0.2, 0.5), 1)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-0.75)
        self.p0.emitter.setAmplitudeSpread(0.25)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(5.0)

    def createTrack(self):
        self.resetEffect()
        shrinkSize = LerpFunctionInterval(self.setNewSize, 2.5, toData=0.001, fromData=1.0)
        moveUp = LerpPosInterval(self, 3.5, Vec3(0, 0, 0))
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(1.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def setCursedColor(self):
        self.p0.renderer.getColorInterpolationManager().clearToInitial()
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(0.75, 0.85, 0.3, 1.0), Vec4(0.4, 0.85, 0.3, 0.5), 1)

    def setDefaultColor(self):
        self.p0.renderer.getColorInterpolationManager().clearToInitial()
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(1.0, 0.6, 0.2, 1.0), Vec4(0.5, 0.2, 0.2, 0.5), 1)

    def resetEffect(self):
        if self.p0:
            self.p0.renderer.setUserAlpha(1.0)
            self.p0.renderer.setInitialXScale(0.045 * self.cardScale * self.effectScale)
            self.p0.renderer.setInitialYScale(0.04 * self.cardScale * self.effectScale)
            self.p0.renderer.setFinalXScale(0.02 * self.cardScale * self.effectScale)
            self.p0.renderer.setFinalYScale(0.035 * self.cardScale * self.effectScale)
            self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0 * self.effectScale))
            self.p0.emitter.setRadius(5.0 * self.effectScale)

    def setNewSize(self, time):
        if self.p0:
            self.p0.renderer.setFinalXScale(0.02 * self.cardScale * self.effectScale * time)
            self.p0.renderer.setFinalYScale(0.035 * self.cardScale * self.effectScale * time)
            self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0 * self.effectScale * time))
            self.p0.renderer.setUserAlpha(2.0 * time)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)