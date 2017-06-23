from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from pirates.piratesgui.GameOptions import Options
from PooledEffect import PooledEffect
from EffectController import EffectController
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import random

class Fire(PooledEffect, EffectController):
    cardScale = 64.0
    burningSfx = None

    def __init__(self, effectParent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if effectParent:
            self.reparentTo(effectParent)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleFire2')
        if not self.burningSfx:
            self.burningSfx = loadSfx(SoundGlobals.SFX_FX_FIRE_LOOP)
        self.fireSfxIval = None
        if not Fire.particleDummy:
            Fire.particleDummy = base.effectsRoot.attachNewNode(ModelNode('FireParticleDummy'))
            Fire.particleDummy.setDepthWrite(0)
            Fire.particleDummy.setFogOff()
            Fire.particleDummy.setLightOff()
            Fire.particleDummy.setColorScaleOff()
            Fire.particleDummy.setBin('fixed', 60)
        self.duration = 10.0
        self.effectScale = 1.0
        self.f = ParticleEffect.ParticleEffect('Fire')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setPoolSize(96)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(4)
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(96)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(4)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-1.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(360.0)
        self.p0.factory.setLifespanBase(0.75)
        self.p0.factory.setLifespanSpread(0.25)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(1.0, 0.6, 0.2, 1.0), Vec4(0.5, 0.2, 0.2, 0.5), 1)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-0.75)
        self.p0.emitter.setAmplitudeSpread(0.25)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.setScale(VBase3(self.effectScale, 1, 1))
        return

    def enable(self):
        self.f.start(self, self.particleDummy)

    def disable(self):
        self.f.disable()

    def createTrack(self, lod=Options.SpecialEffectsHigh):
        if lod >= Options.SpecialEffectsHigh:
            self.p0.setPoolSize(96)
            self.p0.setLitterSize(4)
            self.p0.factory.enableAngularVelocity(1)
            self.p0.factory.setAngularVelocity(0.0)
            self.p0.factory.setAngularVelocitySpread(350.0)
        else:
            self.p0.setPoolSize(48)
            self.p0.setLitterSize(2)
            self.p0.factory.enableAngularVelocity(0)
        self.setNewSize(1.0)
        shrinkSize = LerpFunctionInterval(self.setNewSize, 2.5, toData=0.001, fromData=1.0)

        def playFireSfx():
            if self.burningSfx and not self.fireSfxIval:
                self.fireSfxIval = SoundInterval(self.burningSfx, node=self, cutOff=150, seamlessLoop=False)
                self.fireSfxIval.loop()

        def stopFireSfx():
            if self.fireSfxIval:
                self.fireSfxIval.finish()
                self.fireSfxIval = None
            return

        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Func(playFireSfx))
        self.endEffect = Sequence(shrinkSize, Func(stopFireSfx), Func(self.p0.setBirthRate, 100.0), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def enableEffect(self):
        self.f.start(self, self.particleDummy)
        if self.fireSfxIval:
            self.fireSfxIval.loop()

    def disableEffect(self):
        self.f.disable()
        if self.fireSfxIval:
            self.fireSfxIval.pause()

    def setNewSize(self, time):
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0 * self.effectScale * time))
        self.p0.renderer.setUserAlpha(1.0 * time)

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p0.renderer.setInitialXScale(0.05 * self.cardScale * self.effectScale)
        self.p0.renderer.setInitialYScale(0.05 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalXScale(0.03 * self.cardScale * self.effectScale)
        self.p0.renderer.setFinalYScale(0.045 * self.cardScale * self.effectScale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 15.0 * self.effectScale))
        self.p0.emitter.setRadius(6.0 * self.effectScale)

    def setScale(self, scale=VBase3(1, 1, 1)):
        self.setEffectScale(scale[0])

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        if self.fireSfxIval:
            self.fireSfxIval.pause()
            self.fireSfxIval = None
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return