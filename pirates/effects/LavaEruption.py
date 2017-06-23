from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class LavaEruption(NodePath, EffectController):
    cardScale = 128.0
    eruptionSfx = None

    def __init__(self):
        NodePath.__init__(self, 'LavaEruption')
        EffectController.__init__(self)
        if not self.eruptionSfx:
            self.eruptionSfx = loadSfx(SoundGlobals.SFX_FX_VOLCANO_ERUPT_LOOP)
        self.eruptionSfxIval = None
        self.startEffect = None
        self.endEffect = None
        self.track = None
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/pir_t_efx_msc_lavaSplash')
        self.duration = 10.0
        self.particleDummy = self.attachNewNode(ModelNode('LavaEruptionParticleDummy'))
        self.particleDummy.setDepthWrite(0)
        self.particleDummy.setColorScaleOff()
        self.particleDummy.setLightOff()
        self.particleDummy.setFogOff()
        self.particleDummy.setBin('fixed', 20)
        self.f = ParticleEffect.ParticleEffect('LavaEruption')
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereSurfaceEmitter')
        self.f0 = ForceGroup.ForceGroup('gravity')
        self.force0 = LinearVectorForce(Vec3(0.0, 0.0, -18.0), 2.0, 0)
        self.force0.setVectorMasks(0, 0, 1)
        self.force0.setActive(1)
        self.f0.addForce(self.force0)
        self.f.addForceGroup(self.f0)
        self.p0.setPoolSize(64)
        self.p0.setBirthRate(100)
        self.p0.setLitterSize(3)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(4.0)
        self.p0.factory.setLifespanSpread(0.5)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(180.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(36.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 0.8, 0.8, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 30.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(10.0)
        self.f.addParticles(self.p0)
        return

    def setEffectScale(self, effectScale):
        if self.p0:
            self.p0.renderer.setInitialXScale(0.12 * self.cardScale * effectScale)
            self.p0.renderer.setFinalXScale(0.5 * self.cardScale * effectScale)
            self.p0.renderer.setInitialYScale(0.12 * self.cardScale * effectScale)
            self.p0.renderer.setFinalYScale(0.5 * self.cardScale * effectScale)
            self.p0.emitter.setAmplitude(0.0 * effectScale)
            self.p0.emitter.setAmplitudeSpread(25.0 * effectScale)
            self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 65.0) * effectScale)
            self.p0.emitter.setRadius(30.0 * effectScale)

    def createTrack(self):

        def playEruptionSfx():
            if self.eruptionSfx and not self.eruptionSfxIval:
                self.eruptionSfxIval = SoundInterval(self.eruptionSfx, node=self, cutOff=5000, seamlessLoop=False)
                self.eruptionSfxIval.loop()

        def stopEruptionSfx():
            if self.eruptionSfxIval:
                self.eruptionSfxIval.finish()
                self.eruptionSfxIval = None
            return

        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.2), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(playEruptionSfx))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100), Func(stopEruptionSfx), Wait(4.5), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def destroy(self):
        if self.eruptionSfxIval:
            self.eruptionSfxIval.pause()
            self.eruptionSfxIval = None
        if self.track:
            self.track.pause()
            self.track = None
        if self.startEffect:
            self.startEffect.pause()
            self.startEffect = None
        if self.endEffect:
            self.endEffect.pause()
            self.endEffect = None
        EffectController.destroy(self)
        return