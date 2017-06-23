from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController

class FireSplats(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self, effectParent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if effectParent:
            self.reparentTo(effectParent)
        model = loader.loadModel('models/effects/particleCards')
        self.card = model.find('**/particleSplat')
        if not FireSplats.particleDummy:
            FireSplats.particleDummy = base.effectsRoot.attachNewNode(ModelNode('FireSplatsParticleDummy'))
            FireSplats.particleDummy.setDepthWrite(0)
            FireSplats.particleDummy.setLightOff()
            FireSplats.particleDummy.setColorScaleOff()
            FireSplats.particleDummy.setBin('fixed', 55)
        self.duration = 10.0
        self.effectScale = 1.0
        self.f = ParticleEffect.ParticleEffect('FireSplats')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(4)
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(96)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(4)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-1.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(360.0)
        self.p0.factory.setLifespanBase(1.0)
        self.p0.factory.setLifespanSpread(0.3)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAUSER)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(1.0, 0.4, 0.2, 1.0), Vec4(0.35, 0.0, 0.0, 0.0), 1)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-1.0)
        self.p0.emitter.setAmplitudeSpread(0.75)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 18.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.setScale(VBase3(self.effectScale, 1, 1))

    def enable(self):
        self.f.start(self, self.particleDummy)

    def disable(self):
        self.f.disable()

    def createTrack(self, lod=None):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)

    def setScale(self, scale=VBase3(1, 1, 1)):
        self.effectScale = scale[0]
        self.p0.renderer.setInitialXScale(0.04 * self.cardScale * self.effectScale)
        self.p0.renderer.setInitialYScale(0.04 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalXScale(0.03 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalYScale(0.06 * self.cardScale * self.effectScale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 18.0 * self.effectScale))
        self.p0.emitter.setRadius(5.0 * self.effectScale)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)