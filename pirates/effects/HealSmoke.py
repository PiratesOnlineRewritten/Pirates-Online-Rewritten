from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
import random
from PooledEffect import PooledEffect
from EffectController import EffectController

class HealSmoke(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setColorScaleOff()
        self.setFogOff()
        model = loader.loadModel('models/effects/candleHalo')
        self.card = model.find('**/effectCandleHalo')
        self.effectColor = Vec4(1, 1, 1, 1)
        self.f = ParticleEffect.ParticleEffect('HealSmoke')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(128)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(16)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(0)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.6)
        self.p0.factory.setLifespanSpread(0.5)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(0)
        self.p0.renderer.setInitialXScale(0.02 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.01 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.01 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.06 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 4.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(1.5)

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.04), Func(self.p0.clearToInitial), Func(self.f.start, self, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100), Wait(3.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(3.0), self.endEffect)

    def setEffectColor(self, color, wantBlending=True):
        self.effectColor = color
        self.p0.renderer.getColorInterpolationManager().clearToInitial()
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 0.25, Vec4(0, 0, 0, 0), Vec4(1, 1, 1, 1), 1)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.25, 1.0, Vec4(1, 1, 1, 1), self.effectColor, 1)
        if wantBlending:
            self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        else:
            self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MNone)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)