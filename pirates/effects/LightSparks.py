from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController

class LightSparks(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self, effectParent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectScale = 1.0
        model = loader.loadModel('models/effects/particleCards')
        self.card = model.find('**/particleSparkle')
        if not LightSparks.particleDummy:
            LightSparks.particleDummy = base.effectsRoot.attachNewNode(ModelNode('LightSparksParticleDummy'))
            LightSparks.particleDummy.setColorScaleOff()
            LightSparks.particleDummy.setDepthWrite(0)
            LightSparks.particleDummy.setLightOff()
            LightSparks.particleDummy.setBin('fixed', 70)
        self.f = ParticleEffect.ParticleEffect('FireSparks')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-sparks')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(10)
        self.p0.setBirthRate(0.1)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.0)
        self.p0.factory.setLifespanSpread(0.25)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.2)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 0.25, 0.1, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETCUSTOM)
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 1.0))
        self.setEffectScale(1.0)

    def createTrack(self, lod=None):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.2), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)

    def setEffectScale(self, scale):
        self.p0.renderer.setInitialXScale(0.005 * self.cardScale * scale)
        self.p0.renderer.setInitialYScale(0.005 * self.cardScale * scale)
        self.p0.renderer.setFinalXScale(0.006 * self.cardScale * scale)
        self.p0.renderer.setFinalYScale(0.006 * self.cardScale * scale)
        self.p0.emitter.setAmplitude(0.5 * scale)
        self.p0.emitter.setAmplitudeSpread(0.5 * scale)
        self.p0.emitter.setOffsetForce(Vec3(0.5, 0.5, 5.0) * scale)
        self.p0.emitter.setRadius(1.0 * scale)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)