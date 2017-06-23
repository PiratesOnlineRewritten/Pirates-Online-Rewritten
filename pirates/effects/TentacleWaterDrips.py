from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from PooledEffect import PooledEffect
from EffectController import EffectController

class TentacleWaterDrips(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleRockShower')
        self.cardScale = 64.0
        self.effectScale = 1.0
        self.particleDummy = base.effectsRoot.attachNewNode(ModelNode('WaterDripsParticleDummy'))
        self.particleDummy.setDepthWrite(0)
        self.particleDummy.setFogOff()
        self.particleDummy.setLightOff()
        self.particleDummy.setBin('fixed', 60)
        self.f = ParticleEffect.ParticleEffect('TentacleWaterDrips')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('RectangleEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(36)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(0.0)
        self.p0.factory.setLifespanBase(1.5)
        self.p0.factory.setLifespanSpread(0.2)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.75)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.25)
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setOffsetForce(Vec3(0.0, 1.0, -32))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.setEffectScale(self.effectScale)
        self.setEffectLength(self.effectScale)

    def createTrack(self):
        self.decreaseIntensity = LerpFunctionInterval(self.setIntensity, 4.0 * self.effectScale, toData=0, fromData=0.5)
        self.startEffect = Sequence(Func(self.p0.clearToInitial), Func(self.p0.setBirthRate, 0.02), Func(self.p0.renderer.setUserAlpha, 0.9), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(self.decreaseIntensity, Func(self.p0.setBirthRate, 10.0), Wait(3.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.0), self.endEffect)

    def setEffectLength(self, length):
        self.p0.emitter.setMinBound(Point2(0, -5 * self.effectScale))
        self.p0.emitter.setMaxBound(Point2(length, 5 * self.effectScale))

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p0.renderer.setInitialXScale(0.025 * self.cardScale * scale)
        self.p0.renderer.setInitialYScale(0.01 * self.cardScale * scale)
        self.p0.renderer.setFinalXScale(0.07 * self.cardScale * scale)
        self.p0.renderer.setFinalYScale(0.3 * self.cardScale * scale)

    def setIntensity(self, intensity):
        self.p0.setBirthRate(0.2 + (0.5 - intensity))
        self.p0.renderer.setUserAlpha(intensity + 0.4)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)