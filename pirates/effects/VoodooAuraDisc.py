from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController
from otp.otpbase import OTPRender

class VoodooAuraDisc(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self, effectParent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if effectParent:
            self.reparentTo(effectParent)
        self.effectGeom = loader.loadModel('models/effects/pir_m_efx_msc_auraSplat2')
        self.effectGeom.setColorScale(0.5, 1.0, 0.5, 0.3)
        self.effectGeom.setBillboardAxis(1)
        if not VoodooAuraDisc.particleDummy:
            VoodooAuraDisc.particleDummy = base.effectsRoot.attachNewNode(ModelNode('VoodooAuraDiscParticleDummy'))
            VoodooAuraDisc.particleDummy.hide(OTPRender.MainCameraBitmask)
            VoodooAuraDisc.particleDummy.showThrough(OTPRender.EnviroCameraBitmask)
            VoodooAuraDisc.particleDummy.setDepthWrite(0)
            VoodooAuraDisc.particleDummy.setLightOff()
            VoodooAuraDisc.particleDummy.setColorScaleOff()
            VoodooAuraDisc.particleDummy.setBin('shadow', -10)
        self.duration = 10.0
        self.effectScale = 1.0
        self.f = ParticleEffect.ParticleEffect('FireSplats')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('GeomParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(12)
        self.p0.setBirthRate(0.1)
        self.p0.setLitterSize(1)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.0)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setGeomNode(self.effectGeom.node())
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setZScaleFlag(1)
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOneMinusIncomingAlpha)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.setEffectScale(1.0)

    def enable(self):
        self.f.start(self, self.particleDummy)

    def disable(self):
        self.f.disable()

    def createTrack(self, lod=None):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.1), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p0.renderer.setInitialXScale(55.0 * self.effectScale)
        self.p0.renderer.setInitialYScale(55.0 * self.effectScale)
        self.p0.renderer.setFinalXScale(65.0 * self.effectScale)
        self.p0.renderer.setFinalYScale(65.0 * self.effectScale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(10.0 * self.effectScale)

    def setEffectColor(self, color):
        if self.effectGeom:
            self.effectGeom.setColorScale(color)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)