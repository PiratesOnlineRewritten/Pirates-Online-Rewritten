from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import *
from pirates.piratesbase import PiratesGlobals
from pirates.effects import PolyTrail
from PooledEffect import PooledEffect
from EffectController import EffectController
from direct.showbase import PythonUtil
from direct.task import Task
import random

class HomingMissile(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.target = None
        self.initialVelocity = Vec3(1, 1, 1)
        self.targetOffset = Vec3(0, 0, 0)
        self.duration = 3.0
        self.wantTrail = 1
        self.particleEffect = None
        self.motion_color = [Vec4(0.5, 0.6, 0.8, 1.0), Vec4(0.5, 0.6, 0.8, 1.0)]
        vertex_list = [
         Vec4(0.0, 1.0, 0.0, 1.0), Vec4(0.0, -1.0, 0.0, 1.0)]
        self.motion_trail = PolyTrail.PolyTrail(None, vertex_list, self.motion_color, 1.5)
        self.motion_trail.reparentTo(self)
        vertex_list = [
         Vec4(1.0, 0.0, 0.0, 1.0), Vec4(-1.0, 0.0, 0.0, 1.0)]
        self.motion_trail2 = PolyTrail.PolyTrail(None, vertex_list, self.motion_color, 1.5)
        self.motion_trail2.reparentTo(self)
        self.motion_trail.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOneMinusIncomingAlpha))
        self.motion_trail2.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOneMinusIncomingAlpha))
        return

    def createTrack(self):
        self.timeLeft = self.duration
        self.startEffect = Sequence()
        self.endEffect = Sequence()
        if self.wantTrail:
            self.startEffect.append(Func(self.motion_trail.beginTrail))
            self.startEffect.append(Func(self.motion_trail2.beginTrail))
            self.endEffect.append(Func(self.motion_trail.endTrail))
            self.endEffect.append(Func(self.motion_trail2.endTrail))
            self.motion_trail.setVertexColors(self.motion_color)
            self.motion_trail2.setVertexColors(self.motion_color)
        if self.particleEffect:
            self.particleEffect.reparentTo(self)
            self.startEffect.append(Func(self.particleEffect.startLoop))
            self.endEffect.append(Func(self.particleEffect.stopLoop))
        self.startEffect.append(Func(taskMgr.add, self.__moveMissile, PythonUtil.uniqueName('homingMissileTask')))
        self.endEffect.append(Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration * 0.99), self.endEffect)

    def __moveMissile(self, task):
        currDistance = self.getDistance(self.target)
        timeChange = self.timeLeft
        self.timeLeft = self.duration - task.time
        timeChange -= self.timeLeft
        if self.timeLeft <= 0.0:
            return Task.done
        self.initialVelocity *= self.timeLeft / self.duration
        dist = currDistance * timeChange / self.timeLeft
        self.lookAt(self.target.getPos(render) + self.targetOffset)
        self.setPos(self, self.initialVelocity)
        self.setY(self, dist)
        return Task.cont

    def cleanUpEffect(self):
        if self.wantTrail:
            self.motion_trail.endTrail()
            self.motion_trail2.endTrail()
        taskMgr.remove(PythonUtil.uniqueName('homingMissileTask'))
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        self.motion_trail.destroy()
        self.motion_trail2.destroy()
        taskMgr.remove(PythonUtil.uniqueName('homingMissileTask'))
        EffectController.destroy(self)
        PooledEffect.destroy(self)