from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
import random
from PooledEffect import PooledEffect
from EffectController import EffectController

class CannonBlastSmoke(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleWhiteSmoke')
        self.particleDummy = render.attachNewNode(ModelNode('CannonSmokeParticleDummy'))
        self.particleDummy.setDepthWrite(0)
        self.particleDummy.setLightOff()
        self.f = ParticleEffect.ParticleEffect('CannonBlastSmoke')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('LineEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(8)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(6)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.25)
        self.p0.factory.setLifespanSpread(0.25)
        self.p0.factory.setMassBase(1.8)
        self.p0.factory.setMassSpread(1.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(180.0)
        self.p0.factory.enableAngularVelocity(0)
        self.p0.factory.setAngularVelocity(10.0)
        self.p0.factory.setAngularVelocitySpread(20.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.01 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.1 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.01 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.09 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.5)
        self.p0.emitter.setAmplitudeSpread(1.5)
        self.p0.emitter.setOffsetForce(Vec3(0, 4.0, 1.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setEndpoint1(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setEndpoint2(Point3(0.0, 6.0, 0.0))

    def createTrack(self, duration=0.2):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.025), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100), Wait(2.5), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(duration), self.endEffect)

    def setEffectScale(self, effectScale):
        self.p0.renderer.setInitialXScale(0.01 * self.cardScale * effectScale)
        self.p0.renderer.setFinalXScale(0.1 * self.cardScale * effectScale)
        self.p0.renderer.setInitialYScale(0.01 * self.cardScale * effectScale)
        self.p0.renderer.setFinalYScale(0.09 * self.cardScale * effectScale)
        self.p0.emitter.setOffsetForce(Vec3(0, 4.0 * effectScale, 1.0 * effectScale))
        self.p0.emitter.setAmplitude(0.5 * effectScale)
        self.p0.emitter.setAmplitudeSpread(1.5 * effectScale)
        self.p0.emitter.setEndpoint1(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setEndpoint2(Point3(0.0, 6.0 * effectScale, 0.0))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)