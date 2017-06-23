import re
import random
import types
from pandac.PandaModules import *
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals
from direct.interval.IntervalGlobal import *

class DistributedNPCToy(DistributedInteractive.DistributedInteractive):
    notify = directNotify.newCategory('DistributedNPCToy')

    def __init__(self, cr):
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        NodePath.__init__(self, 'DistributedNPCToy')
        self.__geomLoaded = 0
        self.uniqueId = ''
        self.parentObjId = None
        self.pendingPlacement = None
        self.name = 'NPC Toy Name'
        self.interactSeq = None
        return

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        self.loadGeom()
        self.cr.uidMgr.addUid(self.uniqueId, self.getDoId())

    def disable(self):
        DistributedInteractive.DistributedInteractive.disable(self)

    def delete(self):
        if self.interactSeq:
            self.interactSeq.pause()
            self.interactSeq = None
        DistributedInteractive.DistributedInteractive.delete(self)
        self.removeNode()
        taskMgr.remove(self.uniqueName('playReact'))
        return

    def setUniqueId(self, uid):
        if self.uniqueId != '':
            self.cr.uidMgr.removeUid(self.uniqueId)
        self.uniqueId = uid

    def getUniqueId(self):
        return self.uniqueId

    def setModelPath(self, modelPath):
        self.notify.debug('setModelPath %s' % modelPath)
        self.modelPath = modelPath

    def loadGeom(self):
        if self.__geomLoaded:
            return
        self.geom = loader.loadModel(self.modelPath)
        self.geom.reparentTo(self)
        self.__geomLoaded = 1

    def unloadGeom(self):
        pass

    def setParentObjId(self, parentObjId):
        self.parentObjId = parentObjId

        def putObjOnParent(parentObj, self=self):
            print 'putObj %s on parent %s' % (self.doId, parentObj)
            self.parentObj = parentObj
            self.reparentTo(parentObj)
            self.setColorScale(1, 1, 1, 1, 1)
            self.pendingPlacement = None
            return

        if parentObjId > 0:
            self.pendingPlacement = base.cr.relatedObjectMgr.requestObjects([self.parentObjId], eachCallback=putObjOnParent)

    def setLocation(self, parentId, zoneId):
        pass

    def moveSelf(self, xyz):
        randX = random.random() * 0.3 - 0.15
        randY = random.random() * 0.3 - 0.15
        randZ = random.random() * 0.3 - 0.15
        self.setPos(xyz[0] + randX, xyz[1] + randY, xyz[2] + randZ)
        self.setH(self.getH() - random.random() * 6)
        self.setP(random.random() * 7)
        self.setR(random.random() * 7)

    def finishInteraction(self, xyzhpr):
        self.setPos(xyzhpr[0])
        self.setP(xyzhpr[1][1])
        self.setR(xyzhpr[1][2])

    def playInteraction(self, task=None):
        currPos = self.getPos()
        currHpr = self.getHpr()
        currPosX = currPos[0]
        currPosY = currPos[1]
        currPosZ = currPos[2]
        currH = currHpr[0]
        currP = currHpr[1]
        currR = currHpr[2]
        self.interactSeq = Sequence(Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.finishInteraction, (VBase3(currPosX, currPosY, currPosZ), (currH, currP, currR))))
        self.interactSeq.start()

    def setMovie(self, avId):
        av = self.cr.doId2do.get(avId)
        if av:
            availAnims = [
             'boxing_kick', 'boxing_punch']
            anim = random.choice(availAnims)
            av.play(anim)
            if anim == 'boxing_kick':
                reactDelay = 0.43
            else:
                reactDelay = 0.4
            taskMgr.doMethodLater(reactDelay, self.playInteraction, self.uniqueName('playReact'))