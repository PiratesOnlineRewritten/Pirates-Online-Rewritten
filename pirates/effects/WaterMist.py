from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import Particles
from direct.particles import ParticleEffect
from EffectController import EffectController
from PooledEffect import PooledEffect

class WaterMist(PooledEffect, EffectController):

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.sinkTimeScale = 1.0
        self.setDepthWrite(0)
        self.setLightOff()
        self.setBin('fixed', 20)
        self.effectScale = 1.0
        self.f = ParticleEffect.ParticleEffect('WaterMist')
        self.f.reparentTo(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleWhiteSteam')
        self.cardScale = 64.0
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(8)
        self.p0.setBirthRate(0.25)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(2.5)
        self.p0.factory.setLifespanSpread(0.5)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(0.4)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.0)
        self.p0.emitter.setAmplitudeSpread(0.5)
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))

    def createTrack(self):
        self.setEffectScale(self.effectScale)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.25), Func(self.p0.clearToInitial), Func(self.f.start, self, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(3.0 * self.sinkTimeScale), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(12.0 * self.sinkTimeScale), self.endEffect)

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p0.renderer.setInitialXScale(0.2 * self.cardScale * scale)
        self.p0.renderer.setFinalXScale(0.3 * self.cardScale * scale)
        self.p0.renderer.setInitialYScale(0.2 * self.cardScale * scale)
        self.p0.renderer.setFinalYScale(0.3 * self.cardScale * scale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 6.0 * scale))
        self.p0.emitter.setRadius(20.0 * scale)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)