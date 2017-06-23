from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from direct.particles import ParticleEffect
from direct.particles import Particles
from PooledEffect import PooledEffect

class StunEffect(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.dummy = self.attachNewNode(ModelNode('dummyNode'))
        self.dummy2 = self.dummy.attachNewNode(ModelNode('dummyNode2'))
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSpark')
        self.setDepthWrite(0)
        self.setColorScaleOff()
        self.setLightOff()
        self.duration = 1.5
        self.direction = 1
        self.effectScale = 1.0
        self.f = ParticleEffect.ParticleEffect('StunEffect')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('RingEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(10)
        self.p0.setBirthRate(0.2)
        self.p0.setLitterSize(2)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(0)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.5)
        self.p0.factory.setLifespanSpread(0.25)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAIN)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(0.75, 0.75, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(1)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOne, ColorBlendAttrib.OOneMinusIncomingAlpha)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.75, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(0, 0, 0, 0), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.1)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.75)
        self.p0.emitter.setRadiusSpread(0.0)

    def createTrack(self):
        self.p0.renderer.setInitialXScale(0.001 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalXScale(0.006 * self.cardScale * self.effectScale)
        self.p0.renderer.setInitialYScale(0.001 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalYScale(0.0075 * self.cardScale * self.effectScale)
        rotateOne = LerpHprInterval(self.dummy, self.duration, Vec3(0, 10, -10), startHpr=Vec3(0, -10, 10))
        rotateTwo = LerpHprInterval(self.dummy, self.duration, Vec3(0, -10, 10), startHpr=Vec3(0, 10, -10))
        rotate = Sequence(rotateOne, rotateTwo)
        rotateH = LerpHprInterval(self.dummy2, self.duration, Vec3(0, 0, 0), startHpr=Vec3(self.direction * 360, 0, 0))
        self.startEffect = Sequence(Func(self.p0.clearToInitial), Func(self.p0.setBirthRate, 0.2), Func(self.f.start, self, self.dummy2), Func(rotate.loop), Func(rotateH.loop))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(1.25), Func(rotate.finish), Func(rotateH.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(2.0 * self.duration), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)