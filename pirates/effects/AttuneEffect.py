from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class AttuneEffect(PooledEffect, EffectController):

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if parent is not None:
            self.reparentTo(parent)
        if not self.particleDummy:
            self.particleDummy = render.attachNewNode(ModelNode('AttuneParticleDummy'))
            self.particleDummy.setDepthWrite(0)
            self.particleDummy.setLightOff()
        self.f = ParticleEffect.ParticleEffect('AttuneEffect')
        self.f.reparentTo(self)
        self.effectGeom = loader.loadModel('models/effects/voodooRing')
        self.effectColor = Vec4(1, 1, 1, 1)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('PointParticleFactory')
        self.p0.setRenderer('GeomParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.03)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(1.75)
        self.p0.factory.setLifespanSpread(0.0)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setGeomNode(self.effectGeom.node())
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setZScaleFlag(1)
        self.p0.renderer.setInitialXScale(1.0)
        self.p0.renderer.setFinalXScale(4.0)
        self.p0.renderer.setInitialYScale(1.0)
        self.p0.renderer.setFinalYScale(4.0)
        self.p0.renderer.setInitialZScale(1.0)
        self.p0.renderer.setFinalZScale(4.0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.2)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, -0.5))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.75)
        return

    def createTrack(self):
        posIval = LerpPosInterval(self, 0.75, Point3(0, 0, 0.5))
        self.startEffect = Sequence(Func(self.p0.clearToInitial), Func(self.p0.setBirthRate, 0.01), Func(self.p0.factory.setLifespanBase, 0.75), Func(self.particleDummy.reparentTo, render), Func(self.f.start, self, self.particleDummy), posIval, Func(self.p0.setBirthRate, 0.03), Func(self.p0.factory.setLifespanBase, 1.75), Wait(1.0), Func(self.particleDummy.wrtReparentTo, self))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(3.0), Func(self.p0.setBirthRate, 0.0), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)

    def setEffectColor(self, color):
        self.effectColor = color
        self.p0.renderer.getColorInterpolationManager().clearToInitial()
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 0.2, Vec4(0, 0, 0, 0.5), Vec4(0, 0, 0, 1), 1)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.2, 1.0, Vec4(0, 0, 0, 0.75), self.effectColor, 1)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)