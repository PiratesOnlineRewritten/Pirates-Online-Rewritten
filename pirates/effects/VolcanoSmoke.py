from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController

class VolcanoSmoke(NodePath, EffectController):
    cardScale = 64.0

    def __init__(self):
        NodePath.__init__(self, 'VolcanoSmoke')
        EffectController.__init__(self)
        self.particleDummy = self.attachNewNode(ModelNode('VolcanoSmokeParticleDummy'))
        self.particleDummy.setDepthWrite(0)
        self.particleDummy.setColorScaleOff()
        self.particleDummy.setLightOff()
        self.particleDummy.clearFog()
        self.particleDummy.setBin('fixed', 10)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleWhiteSmoke')
        self.f = ParticleEffect.ParticleEffect('VolcanoSmoke')
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.duration = 10.0
        self.f0 = ForceGroup.ForceGroup('volcano')
        self.force0 = LinearJitterForce(12.0, 0)
        self.force0.setVectorMasks(1, 1, 0)
        self.force0.setActive(1)
        self.f0.addForce(self.force0)
        self.f.addForceGroup(self.f0)
        self.p0.setPoolSize(32)
        self.p0.setBirthRate(3.0)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(60.0)
        self.p0.factory.setLifespanSpread(30.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(180.0)
        self.p0.factory.setFinalAngle(0.0)
        self.p0.factory.setFinalAngleSpread(360.0)
        self.p0.factory.enableAngularVelocity(0)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAUSER)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 0.05, Vec4(1, 0, 0, 0), Vec4(1, 0.6, 0.25, 1.0))
        self.p0.renderer.getColorInterpolationManager().addLinear(0.05, 0.1, Vec4(1, 0.6, 0.25, 1), Vec4(0.25, 0.25, 0.25, 1.0))
        self.p0.renderer.getColorInterpolationManager().addConstant(0.1, 0.8, Vec4(0.25, 0.25, 0.25, 1))
        self.p0.renderer.getColorInterpolationManager().addLinear(0.8, 1.0, Vec4(0.25, 0.25, 0.25, 1.0), Vec4(0.5, 0.5, 0.5, 0.0))
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETEXPLICIT)
        self.p0.emitter.setAmplitude(0.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(2.0)
        self.f.addParticles(self.p0)

    def setEffectScale(self, effectScale):
        self.p0.renderer.setInitialXScale(2.5 * self.cardScale * effectScale)
        self.p0.renderer.setFinalXScale(9.0 * self.cardScale * effectScale)
        self.p0.renderer.setInitialYScale(2.5 * self.cardScale * effectScale)
        self.p0.renderer.setFinalYScale(8.0 * self.cardScale * effectScale)
        self.p0.emitter.setAmplitude(0.0 * effectScale)
        self.p0.emitter.setAmplitudeSpread(10.0 * effectScale)
        self.p0.emitter.setOffsetForce(Vec3(0.0, -5.0, 15.0) * effectScale)
        self.p0.accelerate(45, 1, 0.05 * self.p0.getBirthRate())

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 3.0), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100), Wait(90.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.f0.cleanup()

    def destroy(self):
        EffectController.destroy()
        self.f0.destroy()