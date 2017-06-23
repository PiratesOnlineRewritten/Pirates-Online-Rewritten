from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController

class FeastSmoke(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectScale = 1.0
        if parent is not None:
            self.reparentTo(parent)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleBlackSmoke')
        if not FeastSmoke.particleDummy:
            FeastSmoke.particleDummy = base.effectsRoot.attachNewNode(ModelNode('FeastSmokeParticleDummy'))
            FeastSmoke.particleDummy.setDepthWrite(0)
            FeastSmoke.particleDummy.setColorScaleOff()
            FeastSmoke.particleDummy.setLightOff()
        self.f = ParticleEffect.ParticleEffect('HeavySmoke')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(96)
        self.p0.setBirthRate(1.5)
        self.p0.setLitterSize(2)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(0.0)
        self.p0.factory.setLifespanBase(25.0)
        self.p0.factory.setLifespanSpread(5.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.2)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(30.0)
        self.p0.factory.enableAngularVelocity(0)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.8)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(1.5 * self.cardScale)
        self.p0.renderer.setInitialYScale(1.5 * self.cardScale)
        self.p0.renderer.setFinalXScale(6.0 * self.cardScale)
        self.p0.renderer.setFinalYScale(6.0 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETCUSTOM)
        self.p0.emitter.setAmplitude(6.0)
        self.p0.emitter.setAmplitudeSpread(2.0)
        self.p0.emitter.setOffsetForce(Vec3(4.0, 4.0, 75.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 1.0))
        self.p0.emitter.setRadius(10.0)
        return

    def enable(self):
        self.f.start(self, self.particleDummy)

    def disable(self):
        self.f.disable()

    def accelerate(self):
        self.p0.accelerate(25, 1, self.p0.getBirthRate())

    def createTrack(self, lod=None):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.25), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(10.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)

    def setScale(self, scale=VBase3(1, 1, 1)):
        self.effectScale = scale[0]
        self.p0.renderer.setInitialXScale(0.3 * self.cardScale * self.effectScale)
        self.p0.renderer.setInitialYScale(0.3 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalXScale(1.0 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalYScale(1.0 * self.cardScale * self.effectScale)
        self.p0.emitter.setOffsetForce(Vec3(4.0, 4.0, 50.0 * self.effectScale))
        self.p0.emitter.setRadius(10.0 * self.effectScale)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)