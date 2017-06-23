from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from pirates.piratesbase import PiratesGlobals
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class PistolFlame(PooledEffect, EffectController):
    cardScale = 64.0

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.setColorScaleOff()
        self.startCol = Vec4(0.5, 0.5, 0.5, 1)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleDot')
        if not PistolFlame.particleDummy:
            PistolFlame.particleDummy = render.attachNewNode(ModelNode('FireParticleDummy'))
            PistolFlame.particleDummy.setDepthWrite(0)
            PistolFlame.particleDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            PistolFlame.particleDummy.setFogOff()
        self.flash = loader.loadModel('models/effects/lanternGlow')
        self.flash.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.flash.setDepthWrite(0)
        self.flash.setFogOff()
        self.flash.setColorScale(self.startCol)
        self.flash.setBillboardPointEye(0.2)
        self.flash.setBin('fixed', 120)
        self.flash.setScale(25)
        self.flash.reparentTo(self)
        self.flash.hide()
        self.f = ParticleEffect.ParticleEffect('PistolFlame')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('SphereVolumeEmitter')
        self.f.addParticles(self.p0)
        f0 = ForceGroup.ForceGroup('frict')
        force0 = LinearFrictionForce(1.0, 10.0, 1.0)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)

    def createTrack(self):
        self.p0.setPoolSize(32)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(8)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.1)
        self.p0.factory.setLifespanSpread(0.02)
        self.p0.factory.setMassBase(0.7)
        self.p0.factory.setMassSpread(0.6)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(180.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setAngularVelocity(40.0)
        self.p0.factory.setAngularVelocitySpread(20.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.04 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.02 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.04 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.02 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPNOBLEND)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(0.0)
        self.p0.emitter.setAmplitudeSpread(0.3)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 30.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.1)
        fadeBlast = self.flash.colorScaleInterval(0.15, Vec4(0, 0, 0, 0), startColorScale=self.startCol, blendType='easeOut')
        scaleBlast = self.flash.scaleInterval(0.2, 10, blendType='easeIn')
        self.playFlash = Sequence(Func(self.flash.show), Parallel(fadeBlast, scaleBlast), Func(self.flash.hide), Func(self.flash.setColorScale, Vec4(1, 1, 1, 1)))
        self.playParticles = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy), Func(self.f.reparentTo, self), Wait(0.15), Func(self.p0.setBirthRate, 100), Wait(1.5), Func(self.cleanUpEffect))
        self.track = Parallel(self.playParticles, self.playFlash)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)