from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from pirates.piratesbase import PiratesGlobals
from EffectController import EffectController
import random

class DarkWaterFog(EffectController, NodePath):
    cardScale = 64.0

    def __init__(self, radius=700, radiusSpread=300, lifespan=4.0):
        NodePath.__init__(self, 'DarkWaterFog')
        EffectController.__init__(self)
        self.radius = 700
        self.radiusSpread = 300
        self.lifespan = 4.0
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleGunSmoke')
        if not DarkWaterFog.particleDummy:
            DarkWaterFog.particleDummy = render.attachNewNode(ModelNode('DarkWaterFogParticleDummy'))
            DarkWaterFog.particleDummy.setDepthWrite(0)
            DarkWaterFog.particleDummy.setColorScaleOff()
            DarkWaterFog.particleDummy.setLightOff()
            DarkWaterFog.particleDummy.setBin('water', 100)
        self.f = ParticleEffect.ParticleEffect('DarkWaterFog')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('TangentRingEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(512)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(10)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(self.lifespan)
        self.p0.factory.setLifespanSpread(2.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(0.65)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(2.56 * self.cardScale)
        self.p0.renderer.setFinalXScale(1.92 * self.cardScale)
        self.p0.renderer.setInitialYScale(1.28 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.64 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.getColorInterpolationManager().addConstant(0.0, 1.0, Vec4(0.2, 0.3, 0.5, 0.3), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-20.0)
        self.p0.emitter.setAmplitudeSpread(10.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 12.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, -10.0))
        self.p0.emitter.setRadius(self.radius)
        self.p0.emitter.setRadiusSpread(self.radiusSpread)

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.setPoolSize, 512.0), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 4.0), Wait(3.8), Func(self.p0.setPoolSize, 0.0), Wait(1.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)

    def tuneFog(self, alpha):
        self.p0.renderer.setUserAlpha(alpha)