from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class SparkBurst(PooledEffect, EffectController):
    darkCardScale = 128.0
    blueCardScale = 128.0
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleGlow')
        self.blueCard = model.find('**/particleGlowBlue')
        self.darkCard = model.find('**/effectDarkGlow')
        self.particleDummy = render.attachNewNode(ModelNode('SparkBurstParticleDummy'))
        self.particleDummy.setDepthWrite(0)
        self.particleDummy.setLightOff()
        self.particleDummy.setFogOff()
        self.particleDummy.setColorScaleOff()
        self.effectColor = Vec4(1, 1, 1, 1)
        self.f = ParticleEffect.ParticleEffect('SparkBurst')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('Noise')
        self.f.addForceGroup(f0)
        self.p0.setPoolSize(32)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(10)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.3)
        self.p0.factory.setLifespanSpread(0.2)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.8)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(1)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOne, ColorBlendAttrib.OOneMinusIncomingAlpha)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitudeSpread(4.0)
        self.p0.emitter.setOffsetForce(Vec3(1.0, 1.0, -0.1))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.1, 0.0, 100.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.5)

    def createTrack(self, color='Yellow'):
        if color == 'Yellow':
            self.p0.renderer.setFromNode(self.card)
        else:
            if color == 'Blue':
                self.p0.renderer.setFromNode(self.blueCard)
            else:
                self.p0.renderer.setFromNode(self.darkCard)
            if color == 'Dark':
                self.p0.renderer.setInitialXScale(0.005 * self.darkCardScale)
                self.p0.renderer.setFinalXScale(0.0001 * self.darkCardScale)
                self.p0.renderer.setInitialYScale(0.005 * self.darkCardScale)
                self.p0.renderer.setFinalYScale(0.0001 * self.darkCardScale)
                self.p0.emitter.setAmplitude(10.0)
            self.p0.renderer.setInitialXScale(0.0015 * self.darkCardScale)
            self.p0.renderer.setFinalXScale(1e-05 * self.darkCardScale)
            self.p0.renderer.setInitialYScale(0.0015 * self.darkCardScale)
            self.p0.renderer.setFinalYScale(1e-05 * self.darkCardScale)
            self.p0.emitter.setAmplitude(4.0)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.setPoolSize, 32.0), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 2.0), Wait(1.5), Func(self.p0.setPoolSize, 0.0), Wait(1.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(0.2), self.endEffect)

    def play(self, color='Yellow'):
        if self.p0:
            self.createTrack(color)
            self.track.start()

    def setEffectColor(self, color):
        self.effectColor = color - Vec4(0, 0, 1, 0)
        self.p0.renderer.getColorInterpolationManager().clearToInitial()
        self.p0.renderer.getColorInterpolationManager().addLinear(0, 1, Vec4(1.0, 1.0, 1.0, 0.0), self.effectColor, 1)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)