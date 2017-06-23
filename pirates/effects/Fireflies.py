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

class Fireflies(EffectController, NodePath):
    cardScale = 128.0

    def __init__(self):
        NodePath.__init__(self, 'Fireflies')
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleGlow')
        if not Fireflies.particleDummy:
            Fireflies.particleDummy = render.attachNewNode(ModelNode('FirefliesParticleDummy'))
            Fireflies.particleDummy.setDepthWrite(0)
            Fireflies.particleDummy.setFogOff()
            Fireflies.particleDummy.setColorScale(1.0, 1.0, 1.0, 1)
            Fireflies.particleDummy.setLightOff()
            Fireflies.particleDummy.setBin('fixed', 120)
        self.f = ParticleEffect.ParticleEffect('Fireflies')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('Noise')
        force0 = LinearNoiseForce(0.1, 0)
        force0.setVectorMasks(1, 1, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)

    def createTrack(self):
        self.p0.setPoolSize(256)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(10)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(5.0)
        self.p0.factory.setLifespanSpread(3.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(0)
        self.p0.renderer.setYScaleFlag(0)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.0013 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.0013 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.0013 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.0013 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOneMinusIncomingColor)
        self.p0.renderer.getColorInterpolationManager().addSinusoid(0.0, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(0.0, 0.0, 0.0, 1.0), 0.20000000298023224, 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.2)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.2, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(150.0)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.setPoolSize, 256.0), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 4.0), Wait(3.8), Func(self.p0.setPoolSize, 0.0), Wait(1.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)