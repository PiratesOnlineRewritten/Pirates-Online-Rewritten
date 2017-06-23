from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from EffectController import EffectController
from PooledEffect import PooledEffect

class PowderKegWaterSplash(PooledEffect, EffectController):

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.setDepthWrite(0)
        self.setBin('fixed', 18)
        self.effectScale = 1.0
        self.f = ParticleEffect.ParticleEffect('PowderKegWaterSplash')
        self.f.reparentTo(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSplash')
        self.cardScale = 64.0
        self.p1 = Particles.Particles('particles-1')
        self.p1.setFactory('PointParticleFactory')
        self.p1.setRenderer('SpriteParticleRenderer')
        self.p1.setEmitter('DiscEmitter')
        self.f.addParticles(self.p1)
        self.p1.setPoolSize(128)
        self.p1.setBirthRate(0.01)
        self.p1.setLitterSize(3)
        self.p1.setLitterSpread(1)
        self.p1.setSystemLifespan(0.0)
        self.p1.setLocalVelocityFlag(1)
        self.p1.setSystemGrowsOlderFlag(0)
        self.p1.factory.setLifespanBase(0.5)
        self.p1.factory.setLifespanSpread(0.15)
        self.p1.factory.setMassBase(1.0)
        self.p1.factory.setMassSpread(0.0)
        self.p1.factory.setTerminalVelocityBase(400.0)
        self.p1.factory.setTerminalVelocitySpread(0.0)
        self.p1.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p1.renderer.setUserAlpha(0.75)
        self.p1.renderer.setFromNode(self.card)
        self.p1.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p1.renderer.setXScaleFlag(1)
        self.p1.renderer.setYScaleFlag(1)
        self.p1.renderer.setAnimAngleFlag(0)
        self.p1.renderer.setNonanimatedTheta(0.0)
        self.p1.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p1.renderer.setAlphaDisable(0)
        self.p1.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p1.emitter.setAmplitude(-1.0)
        self.p1.emitter.setAmplitudeSpread(0.5)
        self.p1.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p1.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))

    def createTrack(self):
        self.setEffectScale(self.effectScale)
        self.startEffect = Sequence(Func(self.p1.setBirthRate, 0.01), Func(self.p1.clearToInitial), Func(self.f.start, self, self))
        self.endEffect = Sequence(Func(self.p1.setBirthRate, 100.0), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(0.25), self.endEffect)

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p1.renderer.setInitialXScale(0.025 * self.cardScale * scale)
        self.p1.renderer.setFinalXScale(0.15 * self.cardScale * scale)
        self.p1.renderer.setInitialYScale(0.05 * self.cardScale * scale)
        self.p1.renderer.setFinalYScale(0.1 * self.cardScale * scale)
        self.p1.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0 * scale))
        self.p1.emitter.setRadius(20.0 * scale)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)