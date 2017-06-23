from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from otp.otpbase import OTPRender
import random
from PooledEffect import PooledEffect
from EffectController import EffectController

class VoodooPestilence(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleEvilSmoke')
        self.effectScale = 1.0
        if not self.particleDummy:
            self.particleDummy = render.attachNewNode(ModelNode('selfParticleDummy'))
            self.particleDummy.setDepthWrite(0)
            self.particleDummy.setColorScaleOff()
            self.particleDummy.setLightOff()
            self.particleDummy.setFogOff()
            self.particleDummy.hide(OTPRender.ShadowCameraBitmask)
        self.f = ParticleEffect.ParticleEffect('VoodooPestilence')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        self.f.setP(90.0)
        self.p0.setPoolSize(256)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(3)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(0)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.2)
        self.p0.factory.setLifespanSpread(0.2)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(360.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(300.0)
        self.p0.factory.setAngularVelocitySpread(25.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOneMinusFbufferAlpha, ColorBlendAttrib.OOneMinusIncomingAlpha)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(0.1, 0.2, 0.1, 0.5), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.3)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, -0.45))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.01)

    def createTrack(self):
        self.p0.renderer.setInitialXScale(0.003 * self.effectScale * self.cardScale)
        self.p0.renderer.setFinalXScale(0.0001 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.0015 * self.effectScale * self.cardScale)
        self.p0.renderer.setFinalYScale(0.0001 * self.cardScale)
        if self.effectScale > 1.0:
            self.p0.emitter.setAmplitude(0.15)
            self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, -0.1))
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(2.5), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.25), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)