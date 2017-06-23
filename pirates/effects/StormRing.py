from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from EffectController import EffectController

class StormRing(EffectController, NodePath):
    cardScale = 64.0

    def __init__(self):
        NodePath.__init__(self, 'StormRing')
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleWhiteSmoke')
        if not StormRing.particleDummy:
            StormRing.particleDummy = render.attachNewNode(ModelNode('StormRingDummy'))
            StormRing.particleDummy.setDepthWrite(0)
            StormRing.particleDummy.setColorScale(1.0, 1.0, 1.0, 1.0)
            StormRing.particleDummy.setLightOff()
            StormRing.particleDummy.setBin('background', 116)
        self.duration = 10
        self.f = ParticleEffect.ParticleEffect('StormRing')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('TangentRingEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(256)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(1)
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
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(0)
        self.p0.renderer.setYScaleFlag(0)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setInitialXScale(1.0 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.5 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.5 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.45 * self.cardScale)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETEXPLICIT)
        self.p0.emitter.setAmplitude(3.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 1.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(160.0)
        self.p0.emitter.setRadiusSpread(5)

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)