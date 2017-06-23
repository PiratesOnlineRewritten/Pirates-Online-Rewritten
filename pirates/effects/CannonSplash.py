from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController
import random
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class CannonSplash(PooledEffect, EffectController):
    cardScale = 64.0
    splashSfx = []
    particleDummy = None
    splashSfxNames = (SoundGlobals.SFX_FX_WATER_SPLASH_01, SoundGlobals.SFX_FX_WATER_SPLASH_02, SoundGlobals.SFX_FX_WATER_SPLASH_03, SoundGlobals.SFX_FX_WATER_SPLASH_04, SoundGlobals.SFX_FX_WATER_SPLASH_05, SoundGlobals.SFX_FX_WATER_SPLASH_06, SoundGlobals.SFX_FX_WATER_SPLASH_07, SoundGlobals.SFX_FX_WATER_SPLASH_08)

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleSplash')
        if not CannonSplash.particleDummy:
            CannonSplash.particleDummy = render.attachNewNode(ModelNode('CannonSplashParticleDummy'))
            CannonSplash.particleDummy.setDepthWrite(0)
        if not self.splashSfx:
            for audio in self.splashSfxNames:
                self.splashSfx.append(loadSfx(audio))

        self.f = ParticleEffect.ParticleEffect('CannonSplash')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -40.0), 1.0, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)
        self.p0.setPoolSize(32)
        self.p0.setLitterSize(5)
        self.p0.setLitterSpread(2)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-8.0)
        self.p0.factory.setLifespanBase(3.0)
        self.p0.factory.setLifespanSpread(1.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.9)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.2)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.1 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.7 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.1 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.7 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETCUSTOM)
        self.p0.emitter.setAmplitude(2.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 40.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 1.0))
        self.p0.emitter.setRadius(1.0)
        self.p0.emitter.setOuterAngle(90.0)
        self.p0.emitter.setInnerAngle(0.0)
        self.p0.emitter.setOuterMagnitude(20.0)
        self.p0.emitter.setInnerMagnitude(0.0)
        self.p0.emitter.setCubicLerping(0)

    def createTrack(self):

        def playSplashSfx():
            if self.splashSfx:
                sfx = random.choice(self.splashSfx)
                base.playSfx(sfx, node=self, volume=1.0, cutoff=1500)

        self.track = Sequence(Func(playSplashSfx), Func(self.p0.setBirthRate, 0.05), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Wait(0.3), Func(self.p0.setBirthRate, 100), Wait(4.0), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)