from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class ShipSinkSplashes(PooledEffect, EffectController):
    card2Scale = 64.0
    cardScale = 64.0

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setBin('fixed', 50)
        self.effectScale = 1.0
        self.f = ParticleEffect.ParticleEffect('ShipSinkSplashes')
        self.f.reparentTo(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleWhiteSteam')
        self.card2 = model.find('**/particleSplash')
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.p1 = Particles.Particles('particles-2')
        self.p1.setFactory('PointParticleFactory')
        self.p1.setRenderer('SpriteParticleRenderer')
        self.p1.setEmitter('DiscEmitter')
        self.f.addParticles(self.p1)
        self.p0.setPoolSize(128)
        self.p0.setBirthRate(0.15)
        self.p0.setLitterSize(10)
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
        self.p0.renderer.setUserAlpha(0.5)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.25, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(1.0, 1.0, 1.0, 0.0), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, -2.0, 10.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p1.setPoolSize(128)
        self.p1.setBirthRate(0.01)
        self.p1.setLitterSize(3)
        self.p1.setLitterSpread(1)
        self.p1.setSystemLifespan(0.0)
        self.p1.setLocalVelocityFlag(1)
        self.p1.setSystemGrowsOlderFlag(0)
        self.p1.setFloorZ(-50)
        self.p1.factory.setLifespanBase(0.5)
        self.p1.factory.setLifespanSpread(0.15)
        self.p1.factory.setMassBase(1.0)
        self.p1.factory.setMassSpread(0.0)
        self.p1.factory.setTerminalVelocityBase(400.0)
        self.p1.factory.setTerminalVelocitySpread(0.0)
        self.p1.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p1.renderer.setUserAlpha(0.25)
        self.p1.renderer.setFromNode(self.card2)
        self.p1.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p1.renderer.setXScaleFlag(1)
        self.p1.renderer.setYScaleFlag(1)
        self.p1.renderer.setAnimAngleFlag(0)
        self.p1.renderer.setNonanimatedTheta(0.0)
        self.p1.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p1.renderer.setAlphaDisable(0)
        self.p1.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p1.emitter.setAmplitude(0.0)
        self.p1.emitter.setAmplitudeSpread(0.5)
        self.p1.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p1.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))

    def createTrack(self):
        self.setEffectScale(self.effectScale)
        shrink = LerpFunctionInterval(self.resize, 2.5, fromData=1.0, toData=0.25)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.1), Func(self.p0.clearToInitial), Func(self.p1.setBirthRate, 0.01), Func(self.p1.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(shrink, Func(self.p0.setBirthRate, 100.0), Func(self.p1.setBirthRate, 100.0), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(7.0), self.endEffect)

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p0.renderer.setInitialXScale(0.15 * self.cardScale * scale)
        self.p0.renderer.setFinalXScale(0.4 * self.cardScale * scale)
        self.p0.renderer.setInitialYScale(0.15 * self.cardScale * scale)
        self.p0.renderer.setFinalYScale(0.4 * self.cardScale * scale)
        self.p0.emitter.setRadius(20.0 * scale)
        self.p1.renderer.setInitialXScale(0.05 * self.card2Scale * scale)
        self.p1.renderer.setFinalXScale(0.2 * self.card2Scale * scale)
        self.p1.renderer.setInitialYScale(0.1 * self.card2Scale * scale)
        self.p1.renderer.setFinalYScale(0.15 * self.card2Scale * scale)
        self.p1.emitter.setOffsetForce(Vec3(0.0, 0.0, 16.0 * scale))
        self.p1.emitter.setRadius(20.0 * scale)

    def resize(self, t):
        self.setEffectScale(self.effectScale * t)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)