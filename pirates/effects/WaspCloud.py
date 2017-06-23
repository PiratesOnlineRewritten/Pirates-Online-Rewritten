from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class WaspCloud(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.speed = 20.0
        if not WaspCloud.particleDummy:
            WaspCloud.particleDummy = render.attachNewNode(ModelNode('WaspCloudParticleDummy'))
            WaspCloud.particleDummy.setDepthWrite(0)
        self.f = ParticleEffect.ParticleEffect('WaspCloud')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereSurfaceEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('Noise')
        force0 = LinearJitterForce(25.0, 0)
        force0.setVectorMasks(1, 1, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)
        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.05)
        self.p0.setLitterSize(10)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.5)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(40.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(30.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAUSER)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setAnimateFramesEnable(True)
        self.p0.renderer.setAnimateFramesRate(18.0)
        self.p0.renderer.addTextureFromNode('models/effects/particleWasp_tflip', '**/*')
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(2.0)
        self.p0.renderer.setFinalXScale(1.5)
        self.p0.renderer.setInitialYScale(2.0)
        self.p0.renderer.setFinalYScale(1.5)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.20000000298023224, 0.800000011920929, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(0.7843137383460999, 0.5882353186607361, 0.5882353186607361, 1.0), 1)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.800000011920929, 1.0, Vec4(0.7843137383460999, 0.5882353186607361, 0.5882353186607361, 1.0), Vec4(0.7843137383460999, 0.5882353186607361, 0.5882353186607361, 0.0), 1)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 0.20000000298023224, Vec4(1.0, 1.0, 1.0, 0.0), Vec4(1.0, 1.0, 1.0, 1.0), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(3.0)

    def createTrack(self):
        fadeIn = self.particleDummy.colorInterval(1.0, Vec4(1, 1, 1, 1), startColor=Vec4(0.0, 0.0, 0.0, 1))
        fadeOut = self.particleDummy.colorInterval(0.5, Vec4(0, 0, 0, 1), startColor=Vec4(1, 1, 1, 1))
        self.setScale(0.5, 1, 1)
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.05), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), fadeIn)
        self.endEffect = Sequence(Func(self.wrtReparentTo, render), Parallel(fadeOut, Func(self.p0.setBirthRate, 100)), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)