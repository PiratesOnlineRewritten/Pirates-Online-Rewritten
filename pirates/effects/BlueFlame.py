import random
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController
from pirates.audio.SoundGlobals import loadSfx
from pirates.audio import SoundGlobals

class BlueFlame(PooledEffect, EffectController):
    cardScale = 64.0
    burningSfx = None

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleFire2')
        if not self.burningSfx:
            self.burningSfx = loadSfx(SoundGlobals.SFX_FX_FIRE_LOOP)
        self.fireSfxIval = None
        if not BlueFlame.particleDummy:
            BlueFlame.particleDummy = render.attachNewNode(ModelNode('BurpEffectParticleDummy'))
            BlueFlame.particleDummy.setDepthWrite(0)
            BlueFlame.particleDummy.setFogOff()
            BlueFlame.particleDummy.setLightOff()
            BlueFlame.particleDummy.setColorScaleOff()
            BlueFlame.particleDummy.setTwoSided(1)
        self.f = ParticleEffect.ParticleEffect('FlamingSkull')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereSurfaceEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(128)
        self.p0.setBirthRate(0.2)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(0)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.2)
        self.p0.factory.setLifespanSpread(0.5)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.2)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(20.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.0018 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.0018 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.0001 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.0001 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(0.2, 0.6, 1.0, 1.0), Vec4(0.2, 0.2, 0.6, 0.5), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-0.75)
        self.p0.emitter.setAmplitudeSpread(0.5)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 4.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.5)
        return

    def playFireSfx(self):
        if self.burningSfx and not self.fireSfxIval:
            self.fireSfxIval = SoundInterval(self.burningSfx, node=self, cutOff=150, seamlessLoop=False)
            self.fireSfxIval.loop()

    def stopFireSfx(self):
        if self.fireSfxIval:
            self.fireSfxIval.finish()
            self.fireSfxIval = None
        return

    def createTrack(self):
        self.p0.renderer.setInitialXScale(0.01 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.01 * self.cardScale)
        growSize = LerpFunctionInterval(self.setNewSize, 3.0, toData=1.0, fromData=0.001)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.playFireSfx), Func(self.f.reparentTo, self), growSize)
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Func(self.stopFireSfx), Wait(1.0), Func(self.cleanUpEffect))
        self.track = Parallel(self.startEffect, Wait(5.0), self.endEffect)

    def setNewSize(self, time):
        if self.p0:
            self.p0.emitter.setAmplitude(-2.0 * time)
            self.p0.renderer.setFinalXScale(0.001 * time * self.cardScale)
            self.p0.renderer.setFinalYScale(0.001 * time * self.cardScale)
            self.p0.renderer.setUserAlpha(min(0.5 * time * 3, 0.5))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)