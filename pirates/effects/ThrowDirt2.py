from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class ThrowDirt2(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if parent is not None:
            self.reparentTo(parent)
        if not self.particleDummy:
            self.particleDummy = render.attachNewNode(ModelNode('ThrowDirtParticleDummy'))
            self.particleDummy.setDepthWrite(0)
            self.particleDummy.setLightOff()
            self.particleDummy.setColorScaleOff()
            self.particleDummy.setFogOff()
        self.f = ParticleEffect.ParticleEffect('ThrowDirt2')
        self.f.reparentTo(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleRockShower')
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('RectangleEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('Grav')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -13.0), 1.0, 0)
        force0.setVectorMasks(1, 1, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)
        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(3)
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
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(0.3, 0.2, 0, 1))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.004 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.006 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.004 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.006 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(-3.0, 1.0, 4.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setMinBound(Point2(-0.25, -0.25))
        self.p0.emitter.setMaxBound(Point2(0.25, 0.25))
        return

    def createTrack(self):
        self.startEffect = Sequence(Wait(0.65), Func(self.p0.setBirthRate, 0.02), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.destroy))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)