from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class SwordFreeze(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self, effectParent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if effectParent:
            self.reparentTo(effectParent)
        self.duration = 10.0
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleWhiteSmoke')
        self.setDepthWrite(0)
        self.setFogOff()
        self.setLightOff()
        self.setColorScaleOff()
        self.setBin('fixed', 60)
        self.f = ParticleEffect.ParticleEffect('SwordFreeze')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('LineEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(24)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-1.0)
        self.p0.factory.setLifespanBase(0.6)
        self.p0.factory.setLifespanSpread(0.2)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 0.8))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(0.25, 0.3, 1, 1), Vec4(0.7, 0.8, 1, 1), 1)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-0.75)
        self.p0.emitter.setAmplitudeSpread(0.25)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 10.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setEndpoint1(Point3(-1.25, 0.0, 0.0))
        self.p0.emitter.setEndpoint2(Point3(1.25, 0.0, 0.0))
        self.setEffectScale(1.0)

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.012), Func(self.p0.clearToInitial), Func(self.f.start, self, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def setScale(self, scale=VBase3(1, 1, 1)):
        self.setEffectScale(scale[0])

    def setEffectScale(self, scale):
        self.p0.renderer.setInitialXScale(0.004 * self.cardScale * scale)
        self.p0.renderer.setInitialYScale(0.006 * self.cardScale * scale)
        self.p0.renderer.setFinalXScale(0.002 * self.cardScale * scale)
        self.p0.renderer.setFinalYScale(0.002 * self.cardScale * scale)
        self.p0.emitter.setAmplitude(-0.2 * scale)
        self.p0.emitter.setAmplitudeSpread(0.25 * scale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 1.25) * scale)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)