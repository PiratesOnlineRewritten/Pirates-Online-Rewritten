from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController
from otp.otpbase import OTPRender
import random

class BurpEffect(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleGroundFog')
        if not BurpEffect.particleDummy:
            BurpEffect.particleDummy = render.attachNewNode(ModelNode('BurpEffectParticleDummy'))
            BurpEffect.particleDummy.setDepthWrite(0)
            BurpEffect.particleDummy.setFogOff()
            BurpEffect.particleDummy.setLightOff()
            BurpEffect.particleDummy.setColorScaleOff()
            BurpEffect.particleDummy.setTwoSided(1)
        self.icon = loader.loadModel('models/effects/skull')
        self.icon.setBillboardAxis(0.0)
        self.icon.setDepthWrite(0)
        self.icon.setFogOff()
        self.icon.setLightOff()
        self.icon.setColorScaleOff()
        self.icon.reparentTo(self)
        self.icon.setPos(self, 0, 0, -0.3)
        self.icon.setBin('fixed', 65)
        self.icon.hide(OTPRender.ShadowCameraBitmask)
        self.f = ParticleEffect.ParticleEffect('BurpEffect')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereSurfaceEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, 0.5), 1.0, 0)
        force0.setVectorMasks(1, 1, 1)
        force0.setActive(1)
        f0.addForce(force0)
        force1 = LinearJitterForce(1.0, 0)
        force1.setVectorMasks(1, 1, 1)
        force1.setActive(1)
        f0.addForce(force1)
        self.f.addForceGroup(f0)
        self.p0.setPoolSize(128)
        self.p0.setBirthRate(0.1)
        self.p0.setLitterSize(9)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(0)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(6.0)
        self.p0.factory.setLifespanSpread(0.1)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(0.2)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 0.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.001 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.001 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.02 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.02 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, -1.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.25)

    def createTrack(self):
        self.icon.unstash()
        self.icon.setColorScale(0.0, 0.0, 0.0, 0.0)
        self.icon.setScale(1.0)
        self.icon.reparentTo(render)
        temp = self.attachNewNode('temp')
        temp.setPos(0.5, 0.0, -1.25)
        self.icon.setPos(temp.getPos(render))
        temp.detachNode()
        skullFadeIn = self.icon.colorScaleInterval(2.0, Vec4(0.1, 0.1, 0, 0.35), startColorScale=Vec4(0, 0, 0, 0))
        skullFadeOut = self.icon.colorScaleInterval(1.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(0.1, 0.1, 0, 0.35))
        skullScaleUp = self.icon.scaleInterval(4.0, 3.0, startScale=0.1, blendType='easeOut')
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.02), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(skullFadeIn.start), Func(skullScaleUp.start))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Sequence(skullFadeOut, Func(skullScaleUp.finish), Func(self.icon.stash)), Wait(6.5), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.5), self.endEffect)

    def cleanUpEffect(self):
        self.icon.stash()
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        self.icon.detachNode()
        self.icon = None
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return