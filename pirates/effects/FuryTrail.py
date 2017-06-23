from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController

class FuryTrail(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleGlowBlue')
        self.faceCard = model.find('**/effectFury')
        self.faceCard.reparentTo(self)
        self.faceCard.setDepthWrite(0)
        self.faceCard.setLightOff()
        self.faceCard.setColorScale(0.0, 0.0, 0.0, 1.0)
        self.faceCard.setBillboardPointEye(3.0)
        self.faceCard.setScale(5.0)
        self.faceCard.setBin('fixed', 10)
        if not FuryTrail.particleDummy:
            FuryTrail.particleDummy = render.attachNewNode(ModelNode('FuryTrailParticleDummy'))
            FuryTrail.particleDummy.setDepthWrite(0)
            FuryTrail.particleDummy.setLightOff()
            FuryTrail.particleDummy.setBin('fixed', 0)
        self.f = ParticleEffect.ParticleEffect('FuryTrail')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('noise')
        force0 = LinearNoiseForce(1.5, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)
        self.p0.setPoolSize(32)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.3)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.2)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.13 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.13 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.05 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.05 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-2.0)
        self.p0.emitter.setAmplitudeSpread(0.5)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 10.0))
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(1.0)

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 2.0), Wait(1.5), Func(self.cleanUpEffect))
        self.track = Parallel(self.startEffect, Wait(6.0), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)