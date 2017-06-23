from pandac.PandaModules import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from pirates.effects import PolyTrail
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class VoodooProjectile(PooledEffect, EffectController):
    cardScale = 128.0

    def __init__(self, type=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleMaps')
        self.card = model.find('**/particleDarkSmoke')
        if not VoodooProjectile.particleDummy:
            VoodooProjectile.particleDummy = render.attachNewNode(ModelNode('VoodooProjectileParticleDummy'))
            VoodooProjectile.particleDummy.setDepthWrite(0)
            VoodooProjectile.particleDummy.setLightOff()
            VoodooProjectile.particleDummy.setColorScaleOff()
            VoodooProjectile.particleDummy.setFogOff()
        self.effectColor = Vec4(0.5, 0.2, 1, 1)
        self.f = ParticleEffect.ParticleEffect('VoodooProjectile')
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory('ZSpinParticleFactory')
        self.p0.setRenderer('SpriteParticleRenderer')
        self.p0.setEmitter('DiscEmitter')
        self.f.addParticles(self.p0)
        self.motion_color = [
         Vec4(0.5, 0.2, 1.0, 1.0), Vec4(0.5, 0.2, 1.0, 1.0), Vec4(0.5, 0.2, 1.0, 1.0), Vec4(0.5, 0.2, 1.0, 1.0), Vec4(0.5, 0.2, 1.0, 1.0)]
        r = 0.2
        vertex_list = [Vec4(r, 0.0, r, 1.0), Vec4(r, 0.0, -r, 1.0), Vec4(-r, 0.0, -r, 1.0), Vec4(-r, 0.0, r, 1.0), Vec4(r, 0.0, r, 1.0)]
        self.motion_trail = PolyTrail.PolyTrail(None, vertex_list, self.motion_color)
        self.motion_trail.reparentTo(self)
        self.motion_trail.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.p0.setPoolSize(256)
        self.p0.setBirthRate(0.01)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        self.p0.factory.setLifespanBase(0.5)
        self.p0.factory.setLifespanSpread(0.15)
        self.p0.factory.setMassBase(1.0)
        self.p0.factory.setMassSpread(0.0)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        self.p0.factory.setInitialAngle(0.0)
        self.p0.factory.setInitialAngleSpread(90.0)
        self.p0.factory.enableAngularVelocity(1)
        self.p0.factory.setFinalAngle(1080.0)
        self.p0.factory.setFinalAngleSpread(0.0)
        self.p0.factory.setAngularVelocity(500.0)
        self.p0.factory.setAngularVelocitySpread(100.0)
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAINOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setInitialXScale(0.01 * self.cardScale)
        self.p0.renderer.setInitialYScale(0.01 * self.cardScale)
        self.p0.renderer.setFinalXScale(0.025 * self.cardScale)
        self.p0.renderer.setFinalYScale(0.025 * self.cardScale)
        self.p0.renderer.setNonanimatedTheta(0.0)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), Vec4(0.5, 0.2, 1.0, 0.25), 1)
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitude(-0.25)
        self.p0.emitter.setAmplitudeSpread(0.25)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, -2.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.p0.emitter.setRadius(0.1)
        return

    def createTrack(self, targetPos, speed, target, motion_color):
        self.startEffect = Sequence(Func(self.p0.setBirthRate, 0.01), Func(self.p0.clearToInitial), Func(self.f.start, self, self.particleDummy))
        self.endEffect = Sequence(Func(self.p0.setBirthRate, 100.0), Wait(1.5), Func(self.cleanUpEffect))
        try:
            if target:
                throwTrack = ProjectileInterval(self, startPos=self.getPos(), endPos=targetPos, duration=speed, gravityMult=1.0)
            else:
                endZ = 0
                if targetPos[2] < endZ:
                    endZ = targetPos[2]
                throwTrack = ProjectileInterval(self, endZ=endZ, startPos=self.getPos(), wayPoint=targetPos, timeToWayPoint=1.0, gravityMult=1.0)
        except StandardError, e:
            throwTrack = None

        if throwTrack:
            if not motion_color:
                motion_color = self.motion_color
                self.motion_trail.setVertexColors(motion_color)
            movement = Sequence(Func(self.motion_trail.beginTrail), throwTrack, Func(self.motion_trail.endTrail))
            self.track = Sequence(self.startEffect, movement, self.endEffect)
        else:
            self.track = Wait(2)
        return

    def play(self, targetPos, time, target):
        motion_color = [Vec4(1.0, 1.0, 1.0, 1.0), self.effectColor, Vec4(1.0, 1.0, 1.0, 1.0), self.effectColor, Vec4(1.0, 1.0, 1.0, 1.0)]
        self.createTrack(targetPos, time, target, motion_color)
        self.track.start()

    def setEffectColor(self, color):
        self.effectColor = Vec4(1, 1, 1, 1) - (Vec4(1, 1, 1, 1) - color) / 1.5
        self.p0.renderer.getColorInterpolationManager().clearToInitial()
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0, 1.0, Vec4(1.0, 1.0, 1.0, 1.0), self.effectColor, 1)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        self.motion_trail.destroy()
        EffectController.destroy(self)
        PooledEffect.destroy(self)