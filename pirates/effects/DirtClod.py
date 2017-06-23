from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class DirtClod(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleDirtClod')
        if not DirtClod.particleDummy:
            DirtClod.particleDummy = render.attachNewNode(ModelNode('DirtClodParticleDummy'))
            DirtClod.particleDummy.setDepthWrite(0)
        self.f = ParticleEffect.ParticleEffect('DirtClod')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -20.0), 1.0, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)

    def createTrack(self):
        self.p0.setPoolSize(32)
        self.p0.setBirthRate(0.5)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-5.0)
        self.p0.factory.setLifespanBase(3.0)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(0.3)
        self.p0.factory.setMassSpread(0.05)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAUSER)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.04 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.07 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.04 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.07 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETCUSTOM)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 40.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 1.0))
        self.p0.emitter.setRadius(0.6)
        self.p0.emitter.setOuterAngle(45.0)
        self.p0.emitter.setInnerAngle(0.0)
        self.p0.emitter.setOuterMagnitude(1.0)
        self.p0.emitter.setInnerMagnitude(0.0)
        self.p0.emitter.setCubicLerping(0)
        self.track = Sequence(Func(self.p0.setBirthRate, 0.03), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Wait(0.1), Func(self.p0.setBirthRate, 100), Wait(3.0), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)