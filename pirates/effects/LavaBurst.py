from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class LavaBurst(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if parent is not None:
            self.reparentTo(parent)
        self.loopEffect = None
        self.effectScale = 1.0
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/pir_t_efx_msc_lavaSplash')
        if not LavaBurst.particleDummy:
            LavaBurst.particleDummy = base.effectsRoot.attachNewNode(ModelNode('LavaBurstParticleDummy'))
            LavaBurst.particleDummy.setDepthWrite(0)
            LavaBurst.particleDummy.setColorScaleOff()
            LavaBurst.particleDummy.setLightOff()
            LavaBurst.particleDummy.setBin('fixed', 50)
        self.f = ParticleEffect.ParticleEffect('LavaEruption')
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f0 = ForceGroup.ForceGroup('gravity')
        self.force0 = LinearVectorForce(Vec3(0.0, 0.0, -8.0), 1.0, 0)
        self.force0.setVectorMasks(0, 0, 1)
        self.force0.setActive(1)
        self.f0.addForce(self.force0)
        self.f.addForceGroup(self.f0)
        self.p0.setPoolSize(12)
        self.p0.setBirthRate(100)
        self.p0.setLitterSize(4)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(2.0)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(15.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(30.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 0.8, 0.8, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 20.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.5)
        self.f.addParticles(self.p0)
        return

    def createTrack(self, lod=None):
        self.loopEffect = Sequence(Func(self.randomizeEffect), Func(self.p0.setBirthRate, 0.025), Func(self.p0.clearToInitial), Wait(1.0), Func(self.p0.setBirthRate, 100.0), Wait(2.0 + 4.0 * random.random()))
        self.startEffect = Sequence(Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Func(self.loopEffect.loop))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)

    def enableEffect(self):
        EffectController.enableEffect(self)
        EffectController.startLoop(self)

    def disableEffect(self):
        EffectController.disableEffect(self)
        EffectController.stopLoop(self)

    def setEffectScale(self, effectScale):
        self.effectScale = effectScale
        self.scaleEffectProperties(effectScale)

    def scaleEffectProperties(self, effectScale):
        self.p0.renderer.setInitialXScale(0.01 * self.cardScale * effectScale)
        self.p0.renderer.setFinalXScale(0.025 * self.cardScale * effectScale)
        self.p0.renderer.setInitialYScale(0.03 * self.cardScale * effectScale)
        self.p0.renderer.setFinalYScale(0.004 * self.cardScale * effectScale)
        self.p0.emitter.setAmplitude(1.0 * effectScale)
        self.p0.emitter.setAmplitudeSpread(0.5 * effectScale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 5.0) * effectScale)
        self.p0.emitter.setRadius(1.0 * effectScale)

    def randomizeEffect(self):
        randomX = -10.0 + 20.0 * random.random()
        randomY = -10.0 + 20.0 * random.random()
        self.f.setPos(randomX, randomY, 0.0)
        randomScale = self.effectScale + random.randint(-25, 25) * self.effectScale / 100.0
        self.scaleEffectProperties(randomScale)

    def cleanUpEffect(self):
        if self.loopEffect:
            self.loopEffect.finish()
            self.loopEffect = None
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)
        return

    def destroy(self):
        if self.loopEffect:
            self.loopEffect.finish()
            self.loopEffect = None
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return