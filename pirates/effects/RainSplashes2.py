from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from EffectController import EffectController
import random

class RainSplashes2(EffectController, NodePath):
    cardScale = 64.0

    def __init__(self, reference=None):
        NodePath.__init__(self, 'RainSplashes2')
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleCards')
        self.card = model.find('**/particleSplash3')
        if not RainSplashes2.particleDummy:
            RainSplashes2.particleDummy = render.attachNewNode(ModelNode('RainSplashes2ParticleDummy'))
            RainSplashes2.particleDummy.setDepthWrite(0)
            RainSplashes2.particleDummy.setColorScale(1.0, 1.0, 1.0, 1)
            RainSplashes2.particleDummy.setLightOff()
            RainSplashes2.particleDummy.setBin('water', 10)
            mask = 16777215
            stencil = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, mask, mask)
            RainSplashes2.particleDummy.setAttrib(stencil)
            if not base.useStencils:
                RainSplashes2.particleDummy.hide()
        self.reference = reference
        self.f = ParticleEffect.ParticleEffect('RainSplashes2')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('TangentRingEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(128)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(16)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.2)
        self.p0.factory.setLifespanSpread(0.05)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.2)
        self.p0.renderer.setColor(Vec4(0.8, 0.8, 1.0, 1.0))
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setInitialXScale(0.08 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.1 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.08 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.1 * self.cardScale)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETEXPLICIT)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 1.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(400.0)
        self.p0.emitter.setRadiusSpread(200.0)

    def createTrack(self):
        posUpdate = LerpFunctionInterval(self.updatePos, 1.0)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(posUpdate.loop))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(1.0), Func(posUpdate.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)

    def updatePos(self, t):
        if self.reference:
            pos = self.reference.getPos(self.getParent())
            self.setPos(pos[0], pos[1], 2.0)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)

    def destroy(self):
        EffectController.destroy(self)