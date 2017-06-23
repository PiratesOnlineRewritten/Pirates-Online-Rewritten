from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class JRTeleportEffect(PooledEffect, EffectController):
    card2Scale = 32.0
    cardScale = 32.0

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if parent is not None:
            self.reparentTo(parent)
        if not JRTeleportEffect.particleDummy:
            JRTeleportEffect.particleDummy = render.attachNewNode(ModelNode('JRTeleportEffectParticleDummy'))
            JRTeleportEffect.particleDummy.setColorScaleOff()
            JRTeleportEffect.particleDummy.setLightOff()
            JRTeleportEffect.particleDummy.setFogOff()
            JRTeleportEffect.particleDummy.setDepthWrite(0)
            JRTeleportEffect.particleDummy.setBin('fixed', 40)
        self.effectScale = 1.0
        self.duration = 3.0
        self.radius = 1.0
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleEvilSmoke')
        self.card2 = model.find('**/particleWhiteSmoke')
        self.f = ParticleEffect.ParticleEffect('JRTeleportEffect')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.p1 = Particles.Particles('particles-2')
        self.p1.setFactory('ZSpinParticleFactory')
        self.p1.setRenderer('SpriteParticleRenderer')
        self.p1.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        self.f.addParticles(self.p1)
        f1 = ForceGroup.ForceGroup('Noise')
        force1 = LinearNoiseForce(0.5, 0)
        force1.setVectorMasks(0, 1, 1)
        force1.setActive(1)
        f1.addForce(force1)
        self.f.addForceGroup(f1)
        self.p0.setPoolSize(256)
        self.p0.setBirthRate(0.05)
        self.p0.setLitterSize(24)
        self.p0.setLitterSpread(8)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.25)
        self.p0.factory.setLifespanSpread(0.5)
        self.p0.factory.setMassBase(4.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(90.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(500.0)
        self.p0.factory.setAngularVelocitySpread(100.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 0.6, Vec4(1.0, 1.0, 0.2, 1.0), Vec4(0.8, 0.6, 0.25, 0.75), 1)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.6, 1.0, Vec4(0.8, 0.6, 0.25, 0.75), Vec4(0.5, 0.25, 0.0, 0.0), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, -5.0))
        self.p1.setPoolSize(150)
        self.p1.setBirthRate(0.01)
        self.p1.setLitterSize(3)
        self.p1.setLitterSpread(0)
        self.p1.setSystemLifespan(0.0)
        self.p1.setLocalVelocityFlag(1)
        self.p1.setSystemGrowsOlderFlag(0)
        self.p1.factory.setLifespanBase(1.0)
        self.p1.factory.setLifespanSpread(0.0)
        self.p1.factory.setMassBase(1.0)
        self.p1.factory.setMassSpread(0.0)
        self.p1.factory.setTerminalVelocityBase(400.0)
        self.p1.factory.setTerminalVelocitySpread(0.0)
        self.p1.factory.setInitialAngle(0.0)
        self.p1.factory.setInitialAngleSpread(45.0)
        self.p1.factory.enableAngularVelocity(0)
        self.p1.factory.setFinalAngle(360.0)
        self.p1.factory.setFinalAngleSpread(0.0)
        self.p1.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p1.renderer.setUserAlpha(1.0)
        self.p1.renderer.setFromNode(self.card2)
        self.p1.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p1.renderer.setXScaleFlag(1)
        self.p1.renderer.setYScaleFlag(1)
        self.p1.renderer.setAnimAngleFlag(1)
        self.p1.renderer.setNonanimatedTheta(0.0)
        self.p1.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p1.renderer.setAlphaDisable(0)
        self.p1.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p1.renderer.getColorInterpolationManager().addLinear(0.0, 0.5, Vec4(1.0, 1.0, 0.2, 1.0), Vec4(0.8, 0.6, 0.25, 0.75), 1)
        self.p1.renderer.getColorInterpolationManager().addLinear(0.5, 1.0, Vec4(0.8, 0.6, 0.25, 0.75), Vec4(0.5, 0.25, 0.0, 0.5), 1)
        self.p1.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p1.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p1.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.setEffectScale(self.effectScale)
        return

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.1), Func(self.p0.clearToInitial), Func(self.p1.setBirthRate, 0.02), Func(self.p1.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100), Func(self.p1.setBirthRate, 100), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def reSize(self, t):
        if self.p1:
            self.p1.emitter.setRadius(self.radius * t)

    def setEffectScale(self, scale):
        self.effectScale = scale
        if self.p0:
            self.p0.renderer.setInitialXScale(0.025 * self.effectScale * self.cardScale)
            self.p0.renderer.setFinalXScale(0.015 * self.effectScale * self.cardScale)
            self.p0.renderer.setInitialYScale(0.015 * self.effectScale * self.cardScale)
            self.p0.renderer.setFinalYScale(0.05 * self.effectScale * self.cardScale)
            self.p0.emitter.setAmplitude(self.effectScale)
            self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, -1.5) * self.effectScale)
            self.p0.emitter.setRadius(self.effectScale)
        if self.p1:
            self.p1.renderer.setInitialXScale(0.015 * self.effectScale * self.cardScale)
            self.p1.renderer.setFinalXScale(0.03 * self.effectScale * self.cardScale)
            self.p1.renderer.setInitialYScale(0.015 * self.effectScale * self.cardScale)
            self.p1.renderer.setFinalYScale(0.05 * self.effectScale * self.cardScale)
            self.p1.emitter.setAmplitude(self.effectScale)
            self.p1.emitter.setOffsetForce(Vec3(0.0, 0.0, -3.0) * self.effectScale)
            self.p1.emitter.setRadius(self.effectScale * 1.25)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)