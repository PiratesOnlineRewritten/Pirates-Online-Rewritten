from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class WaterRipple(PooledEffect, EffectController):

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if parent is not None:
            self.reparentTo(parent)
        if not WaterRipple.particleDummy:
            WaterRipple.particleDummy = render.attachNewNode(ModelNode('DarkAuraParticleDummy'))
            WaterRipple.particleDummy.setDepthWrite(0)
            WaterRipple.particleDummy.setFogOff()
            WaterRipple.particleDummy.setBin('water', 50)
        self.effectScale = 1.0
        self.f = ParticleEffect.ParticleEffect('WaterRipple')
        self.f.reparentTo(self)
        self.effectGeom = loader.loadModel('models/effects/ripple')
        if not self.effectGeom:
            self.effectGeom = loader.loadModel('models/misc/smiley')
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('GeomParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.p0.emitter.setRadius(0.25)
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(8)
        self.p0.setBirthRate(0.75)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(4.0)
        self.p0.factory.setLifespanSpread(1.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(1.0)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, -0.01))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.renderer.setGeomNode(self.effectGeom.node())
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setZScaleFlag(1)
        self.setEffectScale(self.effectScale)
        self.disturb = None
        return

    def createTrack(self):
        self.disturb = Sequence(Func(self.p0.setEmitter, 'DiscEmitter'), Func(self.p0.setBirthRate, 0.3), Func(self.p0.factory.setLifespanBase, 2.5), Wait(1.0), Func(self.p0.setEmitter, 'PointEmitter'), Func(self.p0.setBirthRate, 1.0), Func(self.p0.factory.setLifespanBase, 4.0))
        self.startEffect = Sequence(Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), self.disturb)
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(3.0), Func(self.p0.setBirthRate, 0.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p0.renderer.setInitialXScale(0.2 * scale)
        self.p0.renderer.setFinalXScale(6.0 * scale)
        self.p0.renderer.setInitialYScale(0.2 * scale)
        self.p0.renderer.setFinalYScale(6.0 * scale)
        self.p0.renderer.setInitialZScale(0.2 * scale)
        self.p0.renderer.setFinalZScale(6.0 * scale)

    def disturbRipple(self):
        if self.disturb:
            self.disturb.start()

    def cleanUpEffect(self):
        if self.disturb:
            self.disturb.pause()
            self.disturb = None
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)
        return

    def destroy(self):
        if self.disturb:
            self.disturb.pause()
            self.disturb = None
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return