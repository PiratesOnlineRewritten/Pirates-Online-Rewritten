from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from pirates.effects import PolyTrail
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class VenomSpitProjectile(PooledEffect, EffectController):

    def __init__(self, type=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.motion_color = [
         Vec4(0.5, 0.6, 0.8, 1.0), Vec4(0.5, 0.6, 0.8, 1.0), Vec4(0.5, 0.6, 0.8, 1.0), Vec4(0.5, 0.6, 0.8, 1.0), Vec4(0.5, 0.6, 0.8, 1.0)]
        r = 0.2
        vertex_list = [Vec4(r, 0.0, r, 1.0), Vec4(r, 0.0, -r, 1.0), Vec4(-r, 0.0, -r, 1.0), Vec4(-r, 0.0, r, 1.0), Vec4(r, 0.0, r, 1.0)]
        self.motion_trail = PolyTrail.PolyTrail(None, vertex_list, self.motion_color)
        self.motion_trail.reparentTo(self)
        self.motion_trail.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        return

    def createTrack(self, targetPos, speed, target, motion_color):
        if target:
            throwTrack = ProjectileInterval(self, startPos=self.getPos(), endPos=targetPos, duration=speed, gravityMult=1.0)
        else:
            throwTrack = ProjectileInterval(self, endZ=-10, startPos=self.getPos(), wayPoint=targetPos, timeToWayPoint=1.0, gravityMult=1.0)
        if not motion_color:
            motion_color = self.motion_color
        self.motion_trail.setVertexColors(motion_color)
        movement = Sequence(Func(self.motion_trail.beginTrail), throwTrack, Func(self.motion_trail.endTrail))
        self.track = Sequence(movement, Func(self.cleanUpEffect))

    def play(self, targetPos, speed, target):
        motion_color = [
         Vec4(0.1, 1.0, 0.4, 1.0), Vec4(0.5, 1.0, 0.4, 1.0), Vec4(0.1, 1.0, 0.4, 1.0), Vec4(0.5, 1.0, 0.4, 1.0), Vec4(0.1, 1.0, 0.4, 1.0)]
        self.createTrack(targetPos, speed, target, motion_color)
        self.track.start()

    def cleanUpEffect(self):
        self.detachNode()
        self.checkInEffect(self)

    def destroy(self):
        self.stop()
        self.motion_trail.destroy()
        EffectController.destroy(self)
        PooledEffect.destroy(self)