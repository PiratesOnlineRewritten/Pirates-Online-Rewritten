from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from pirates.piratesbase import PiratesGlobals
from EffectController import EffectController
from pirates.piratesgui.GameOptions import Options
import random

class GroundFog(EffectController, NodePath):
    cardScale = 64.0

    def __init__(self):
        NodePath.__init__(self, 'GroundFog')
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleGroundFog')
        if not GroundFog.particleDummy:
            GroundFog.particleDummy = render.attachNewNode(ModelNode('GroundFogParticleDummy'))
            GroundFog.particleDummy.setDepthWrite(0)
            GroundFog.particleDummy.setColorScale(1.0, 1.0, 1.0, 1)
            GroundFog.particleDummy.setLightOff()
            GroundFog.particleDummy.setBin('fixed', 110)
        self.f = ParticleEffect.ParticleEffect('GroundFog')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)

    def createTrack(self, lod=Options.SpecialEffectsHigh):
        if lod >= Options.SpecialEffectsHigh:
            self.p0.setPoolSize(96)
            self.p0.setBirthRate(0.025)
            self.p0.setLitterSize(8)
        else:
            self.p0.setPoolSize(48)
            self.p0.setBirthRate(0.03)
            self.p0.setLitterSize(4)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(3.0)
        self.p0.factory.setLifespanSpread(2.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.5 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.2 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.13 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.053 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.getColorInterpolationManager().addConstant(0.0, 1.0, Vec4(0.6, 0.8, 1.0, 0.5), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETEXPLICIT)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.2, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(200.0)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.setPoolSize, 128.0), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(4.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)