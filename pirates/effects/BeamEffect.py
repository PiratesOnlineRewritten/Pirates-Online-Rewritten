from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class BeamEffect(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.setLightOff()
        self.setDepthWrite(0)
        self.setColorScaleOff()
        self.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.hide()
        self.beams = []
        self.numBeams = 6
        self.numPoses = 20.0
        self.duration = 1.0
        self.target = None
        self.targetPos = None
        self.isTaperingBeam = 1
        self.beamDummy = self.attachNewNode('beamDummy')
        for i in range(self.numBeams):
            beam = loader.loadModel('models/effects/lightning_beam')
            beam.reparentTo(self)
            self.beams.append(beam)

        self.targetDummy = self.attachNewNode('targetDummy')
        return

    def __calculateBeam(self):
        if not self.target and not self.targetPos:
            return
        if not self.target:
            self.targetDummy.setPos(self.targetPos)
            self.target = self.targetDummy
        distance = self.getDistance(self.target)
        self.lookAt(self.target)
        avgBeamLength = distance / self.numBeams
        prevTarget = self.beamDummy
        prevY = 0
        if self.isTaperingBeam:
            self.beamDummy.setScale(6.0)
        for i in range(self.numBeams):
            if i == self.numBeams - 1:
                newX = self.target.getX()
                newY = self.target.getY()
                newZ = self.target.getZ()
            else:
                randomSpread = random.uniform(-avgBeamLength / 2, avgBeamLength / 2)
                newX = random.uniform(-2.0, 2.0)
                newY = avgBeamLength + randomSpread + prevY
                newZ = random.uniform(-2.0, 2.0)
            self.beams[i].setPos(self, newX, newY, newZ)
            self.beams[i].lookAt(prevTarget)
            dist = self.beams[i].getDistance(prevTarget) + 0.4
            if self.isTaperingBeam:
                self.beams[i].setSx(4.0)
                self.beams[i].setSy(prevTarget, dist / 10)
                self.beams[i].setSz(4.0)
            else:
                self.beams[i].setScale(prevTarget, 0.9, dist / 10, 0.9)
            prevTarget = self.beams[i]
            prevY = newY

    def createTrack(self, duration=1.0):
        anim = Sequence()
        anim.append(Func(self.__calculateBeam))
        for i in range(self.numPoses):
            anim.append(Wait(self.duration / self.numPoses))
            anim.append(Func(self.__calculateBeam))

        scroller = LerpFunctionInterval(self.setNewUVs, fromData=0.0, toData=20.0 * self.duration, duration=self.duration)
        self.track = Sequence(Func(self.showAll), Parallel(anim, scroller), Func(self.hideAll), Func(self.cleanUpEffect))

    def setNewUVs(self, time):
        for beam in self.beams:
            texStage = beam.findAllTextureStages()[0]
            beam.setTexOffset(texStage, 0, time)

    def showAll(self):
        self.show()
        for beam in self.beams:
            beam.show()

    def hideAll(self):
        self.hide()
        for beam in self.beams:
            beam.hide()

    def cleanUpEffect(self):
        self.target = None
        self.targetPos = None
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)
        return

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)