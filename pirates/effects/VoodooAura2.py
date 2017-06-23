from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from otp.otpbase import OTPRender
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class VoodooAura2(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/battleEffects')
        self.card = model.find('**/effectVoodooShockwave')
        if not self.particleDummy:
            self.particleDummy = self.attachNewNode(ModelNode('VoodooAura2ParticleDummy'))
            self.particleDummy.setDepthWrite(0)
            self.particleDummy.setLightOff()
            self.particleDummy.hide(OTPRender.ShadowCameraBitmask)
        self.effectColor = Vec4(1, 1, 1, 1)
        self.f = ParticleEffect.ParticleEffect('VoodooAura2')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('PointEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(0)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.0)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.5)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.005 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.012 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.005 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.012 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(0.8, 0.8, 0.8, 1), self.effectColor, 1)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.2)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))

    def createTrack(self, rate=1):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.03), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100), Wait(1.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(0.75), self.endEffect)

    def setEffectColor(self, color):
        self.effectColor = color
        self.p0.renderer.getColorInterpolationManager().clearToInitial()
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(0.8, 0.8, 0.8, 1), self.effectColor, 1)

    def cleanUpEffect(self):
        self.detachNode()
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)