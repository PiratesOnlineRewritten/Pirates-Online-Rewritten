from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from otp.otpbase import OTPRender
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class FlamingSkull(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleFire')
        if not FlamingSkull.particleDummy:
            FlamingSkull.particleDummy = render.attachNewNode(ModelNode('FlamingSkullParticleDummy'))
            FlamingSkull.particleDummy.setDepthWrite(0)
            FlamingSkull.particleDummy.setFogOff()
            FlamingSkull.particleDummy.setLightOff()
            FlamingSkull.particleDummy.setColorScaleOff()
            FlamingSkull.particleDummy.setTwoSided(1)
            FlamingSkull.particleDummy.setBin('fixed', 60)
            FlamingSkull.particleDummy.hide(OTPRender.ShadowCameraBitmask)
        self.icon = loader.loadModel('models/effects/skull')
        self.icon.setBillboardAxis(0.0)
        self.icon.setDepthWrite(0)
        self.icon.setFogOff()
        self.icon.setLightOff()
        self.icon.setColorScaleOff()
        self.icon.reparentTo(self)
        self.icon.setPos(self, 0, 0, -0.3)
        self.icon.setBin('fixed', 65)
        self.icon.hide(OTPRender.ShadowCameraBitmask)
        self.f = ParticleEffect.ParticleEffect('FlamingSkull')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereSurfaceEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(128)
        self.p0.setBirthRate(0.2)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.2)
        self.p0.factory.setLifespanSpread(0.5)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.2)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(20.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.0018 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.0018 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.0001 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.0001 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOneMinusFbufferAlpha, ColorBlendAttrib.OOneMinusIncomingAlpha)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(0, 0, 0, 1.0), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-0.75)
        self.p0.emitter.setAmplitudeSpread(0.5)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 4.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.5)

    def createTrack(self):
        self.p0.renderer.setInitialXScale(0.01 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.01 * self.cardScale)
        self.icon.show()
        self.icon.setColorScale(0, 0, 0, 0)
        self.icon.setScale(1.0)
        skullFadeIn = self.icon.colorScaleInterval(3.0, Vec4(0.1, 0.1, 0, 0.25), startColorScale=Vec4(0, 0, 0, 0))
        skullFadeOut = self.icon.colorScaleInterval(1.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(0.1, 0.1, 0, 0.25))
        skullPulseUp = self.icon.scaleInterval(0.05, 1.25, startScale=1.0)
        skullPulseDown = self.icon.scaleInterval(0.05, 1.0, startScale=1.25)
        skullPulse = Sequence(skullPulseUp, skullPulseDown)
        skullColorPulseUp = self.icon.colorScaleInterval(0.1, Vec4(0.1, 0.1, 0, 0.5), startColorScale=Vec4(0, 0, 0, 0.25))
        skullColorPulseDown = self.icon.colorScaleInterval(0.1, Vec4(0, 0, 0, 0.25), startColorScale=Vec4(0.1, 0.1, 0, 0.5))
        skullColorPulse = Sequence(skullColorPulseUp, skullColorPulseDown)
        growSize = LerpFunctionInterval(self.setNewSize, 3.0, toData=1.0, fromData=0.001)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Func(skullFadeIn.start), Func(skullPulse.loop), growSize, Func(skullColorPulse.loop))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Sequence(skullFadeOut, Func(skullPulse.finish), Func(skullColorPulse.finish), Func(self.icon.hide)), Wait(1.0), Func(self.cleanUpEffect))
        self.track = Parallel(self.startEffect, Wait(5.0), self.endEffect)

    def setNewSize(self, time):
        if self.p0:
            self.p0.emitter.setAmplitude(-2.0 * time)
            self.p0.renderer.setFinalXScale(0.001 * time * self.cardScale)
            self.p0.renderer.setFinalYScale(0.001 * time * self.cardScale)
            self.p0.renderer.setUserAlpha(min(0.5 * time * 3, 0.5))

    def playLaunch(self, time, targetPos):
        if self.p0:
            throwTrack = LerpPosInterval(self, time, targetPos)
            self.fireTrack = Sequence(throwTrack, Func(self.stopLoop))
            self.fireTrack.start()

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)