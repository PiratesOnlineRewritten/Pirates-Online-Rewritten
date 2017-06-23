from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from EffectController import EffectController
from PooledEffect import PooledEffect
from otp.otpbase import OTPRender

class PulseEffect(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.duration = 10.0
        self.intensity = 1.0
        self.usesSound = True
        self.soundIval = None
        self.heartSfxIval = None
        self.hide(OTPRender.ShadowCameraBitmask)
        self.setDepthWrite(0)
        self.setLightOff()
        self.f = ParticleEffect.ParticleEffect('PulseEffect')
        self.f.reparentTo(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/pir_t_efx_msc_glowingRays')
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(1)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(360.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(0.0)
        self.p0.factory.setLifespanBase(0.75)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(0.5)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(0.5, 0, 0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.setEffectScale(1.0)
        return

    def createTrack(self):
        self.p0.setPoolSize(1)
        self.p0.factory.setLifespanBase(0.75)
        self.p0.renderer.setColor(Vec4(0.5, 0, 0, 1.0))
        self.startEffect = Sequence(Wait(0.12), Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(1.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.0), self.endEffect)

    def setScale(self, scale=VBase3(1, 1, 1)):
        self.setEffectScale(scale[0])

    def setEffectScale(self, scale):
        self.p0.renderer.setInitialXScale(0.0005 * self.cardScale * scale)
        self.p0.renderer.setFinalXScale(0.075 * self.cardScale * scale)
        self.p0.renderer.setInitialYScale(0.0005 * self.cardScale * scale)
        self.p0.renderer.setFinalYScale(0.075 * self.cardScale * scale)
        self.p0.emitter.setAmplitude(0.0 * scale)
        self.p0.emitter.setAmplitudeSpread(0.1 * scale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.5) * scale)
        self.p0.emitter.setRadius(0.25 * scale)

    def addBlending(self):
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)

    def removeBlending(self):
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MNone)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)