from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from pirates.effects import PolyTrail
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class RoundshotProjectile(EffectController, NodePath):
    motion_color = [
     Vec4(0.5, 0.6, 0.8, 1.0), Vec4(0.5, 0.6, 0.8, 1.0), Vec4(0.5, 0.6, 0.8, 1.0)]
    vertex_list = [
     Vec4(0.2, 0, 0.1, 1.0), Vec4(-0.2, 0, -0.1, 1.0), Vec4(0, 0, 0.2, 1.0)]

    def __init__(self):
        NodePath.__init__(self, 'RoundshotProjectile')
        EffectController.__init__(self)
        self.shot = loader.loadModel('models/ammunition/cannonball')
        self.shot.reparentTo(self)
        self.shot.setScale(0.35)
        self.motion_trail = PolyTrail.PolyTrail(None, self.vertex_list, self.motion_color)
        self.motion_trail.setUnmodifiedVertexColors(self.motion_color)
        self.motion_trail.motion_trail.geom_node_path.setTwoSided(False)
        self.motion_trail.reparentTo(self)
        self.motion_trail.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        return

    def createTrack(self, time, targetPos, motion_color, rate=1):
        throwTrack = LerpPosInterval(self, time, targetPos)
        if not motion_color:
            motion_color = self.motion_color
        self.motion_trail.setVertexColors(motion_color)
        fader = LerpColorScaleInterval(self.shot, time, Vec4(1.0, 1.0, 1.0, 0.0))
        movement = Sequence(Func(self.motion_trail.beginTrail), throwTrack, Func(self.motion_trail.endTrail))
        self.track = Sequence(Func(self.shot.setColorScale, Vec4(1, 1, 1, 1)), Parallel(movement, fader), Func(self.cleanUpEffect), Func(self.destroy))

    def play(self, time, targetPos, motion_color=None, rate=1):
        self.createTrack(time, targetPos, motion_color)
        self.track.start()

    def cleanUpEffect(self):
        self.detachNode()

    def destroy(self):
        self.stop()
        self.motion_trail.destroy()
        EffectController.destroy(self)