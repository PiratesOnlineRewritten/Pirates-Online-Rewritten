from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class EvilRingEffect(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if parent is not None:
            self.reparentTo(parent)
        if not EvilRingEffect.particleDummy:
            EvilRingEffect.particleDummy = render.attachNewNode(ModelNode('EvilRingEffectParticleDummy'))
            EvilRingEffect.particleDummy.setColorScaleOff()
            EvilRingEffect.particleDummy.setLightOff()
            EvilRingEffect.particleDummy.setFogOff()
            EvilRingEffect.particleDummy.setDepthWrite(0)
            EvilRingEffect.particleDummy.setDepthTest(0)
            EvilRingEffect.particleDummy.setBin('shadow', 0)
            EvilRingEffect.particleDummy.setTransparency(TransparencyAttrib.MAlpha)
        self.effectScale = 1.0
        self.effectColor = Vec4(1, 1, 1, 1)
        self.duration = 4.0
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleDarkSmoke')
        self.f = ParticleEffect.ParticleEffect('EvilRingEffect')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('RingEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(256)
        self.p0.setBirthRate(0.0)
        self.p0.setLitterSize(8)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.35)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(10.0)
        self.p0.factory.enableAngularVelocity(0)
        self.p0.factory.setFinalAngle(90.0)
        self.p0.factory.setFinalAngleSpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.005 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.03 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.005 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.025 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOneMinusFbufferAlpha, ColorBlendAttrib.OOneMinusIncomingAlpha)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(0.6, 0.8, 0.7, 0.4), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.0)
        self.p0.emitter.setRadiusSpread(0.0)
        return

    def createTrack(self):
        expand = LerpFunctionInterval(self.reSize, 0.5, toData=1.0, fromData=0.0)
        shrink = LerpFunctionInterval(self.reSize, 0.75, toData=0.0, fromData=1.0)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), expand)
        self.endEffect = Sequence(shrink, Func(self.p0.setBirthRate, 100), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def reSize(self, t):
        self.p0.emitter.setRadius(self.effectScale * t)

    def setEffectColor(self, color):
        self.effectColor = Vec4(1, 1, 1, 0) - (Vec4(1, 1, 1, 1) - color) / 2.0
        self.p0.renderer.getColorInterpolationManager().clearToInitial()
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, self.effectColor, Vec4(0.6, 0.8, 0.7, 0.4), 1)

    def changeEffectColor(self, color):
        self.effectColor = color
        self.p0.renderer.getColorInterpolationManager().clearToInitial()
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, color, color, 1)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)