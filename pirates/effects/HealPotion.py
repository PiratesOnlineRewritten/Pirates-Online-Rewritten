from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController
import os

class HealPotion(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSpark')
        if not HealPotion.particleDummy:
            HealPotion.particleDummy = render.attachNewNode(ModelNode('HealPotionParticleDummy'))
            HealPotion.particleDummy.setDepthWrite(0)
            HealPotion.particleDummy.setLightOff()
            HealPotion.particleDummy.setFogOff()
            HealPotion.particleDummy.setColorScaleOff()
        self.effectColor = Vec4(1, 1, 1, 1)
        self.f = ParticleEffect.ParticleEffect('HealSparks')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('Gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -10.0), 1.0, 0)
        force0.setVectorMasks(1, 1, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)
        self.p0.setPoolSize(32)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(2)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.8)
        self.p0.factory.setLifespanSpread(0.1)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1, 1, 1, 1))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.002 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.003 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.002 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.004 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.0)
        self.p0.emitter.setAmplitudeSpread(0.5)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.1)

    def createTrack(self):
        self.startEffect = Sequence(Wait(2.0), Func(self.p0.clearToInitial), Func(self.p0.setBirthRate, 0.01), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(1.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(3.0), self.endEffect)

    def setEffectColor(self, color):
        self.effectColor = color
        self.p0.renderer.setColor(color)

    def play(self, delay=0.0):
        self.createTrack(delay)
        self.track.start()

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        self.adjustIval = None
        return