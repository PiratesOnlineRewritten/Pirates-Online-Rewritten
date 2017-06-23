from pandac.PandaModules import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from pirates.effects import PolyTrail
from PooledEffect import PooledEffect
from EffectController import EffectController
from otp.otpbase import OTPRender
import random

class JollySoulDrain(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self, type=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleEvilSmoke')
        if not self.particleDummy:
            self.particleDummy = self.attachNewNode(ModelNode('JollySoulDrainParticleDummy'))
            self.particleDummy.setDepthWrite(0)
            self.particleDummy.setLightOff()
            self.particleDummy.setColorScaleOff()
            self.particleDummy.setFogOff()
            self.particleDummy.hide(OTPRender.ShadowCameraBitmask)
            self.particleDummy.setBin('fixed', 160)
        self.f = ParticleEffect.ParticleEffect('JollySoulDrain')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)

    def createTrack(self):
        self.p0.setPoolSize(128)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.8)
        self.p0.factory.setLifespanSpread(0.3)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(360.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.5)
        self.p0.factory.setAngularVelocitySpread(0.3)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setAnimateFramesEnable(True)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.01 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.0005 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.005 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.0005 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(1)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOneMinusConstantColor, ColorBlendAttrib.OOneMinusIncomingAlpha)
        self.p0.renderer.getColorInterpolationManager().addConstant(0.0, 1.0, Vec4(0.7843137383460999, 1.0, 1.0, 1.0), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.7, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.1)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 2.0), Wait(1.5), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(3.0), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)