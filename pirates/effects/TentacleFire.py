from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from PooledEffect import PooledEffect
from EffectController import EffectController

class TentacleFire(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self, effectParent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if effectParent:
            self.reparentTo(effectParent)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleFire2')
        self.effectScale = 1.0
        if not TentacleFire.particleDummy:
            TentacleFire.particleDummy = base.effectsRoot.attachNewNode(ModelNode('FireParticleDummy'))
            TentacleFire.particleDummy.setDepthWrite(0)
            TentacleFire.particleDummy.setFogOff()
            TentacleFire.particleDummy.setLightOff()
            TentacleFire.particleDummy.setColorScaleOff()
            TentacleFire.particleDummy.setBin('fixed', 120)
            TentacleFire.particleDummy.setTwoSided(1)
            TentacleFire.particleDummy.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CRed | ColorWriteAttrib.CGreen | ColorWriteAttrib.CBlue))
        self.f = ParticleEffect.ParticleEffect('TentacleFire')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('RectangleEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(3)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.setFloorZ(-1.0)
        self.p0.factory.setLifespanBase(0.6)
        self.p0.factory.setLifespanSpread(0.2)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(360.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(0.0)
        self.p0.factory.setAngularVelocitySpread(350.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(1.0, 0.6, 0.2, 1.0), Vec4(0.5, 0.2, 0.2, 0.5), 1)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-1.0)
        self.p0.emitter.setAmplitudeSpread(0.25)
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setOffsetForce(Vec3(0.0, 1.0, 15.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.setEffectScale(self.effectScale)

    def createTrack(self):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 4.0), Wait(2.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(3.0), self.endEffect)

    def setEffectLength(self, length):
        self.p0.emitter.setMinBound(Point2(0, -5 * self.effectScale))
        self.p0.emitter.setMaxBound(Point2(length, 5 * self.effectScale))

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p0.renderer.setInitialXScale(0.06 * self.cardScale * scale)
        self.p0.renderer.setInitialYScale(0.06 * self.cardScale * scale)
        self.p0.renderer.setFinalXScale(0.04 * self.cardScale * scale)
        self.p0.renderer.setFinalYScale(0.055 * self.cardScale * scale)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)