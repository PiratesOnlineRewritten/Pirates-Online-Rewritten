from direct.showbase.DirectObject import *
from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from direct.task.Task import Task
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.GridChild import SmoothGridChild
import random
from otp.movement import Mover
from pirates.demo import DemoGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.distributed.DistributedTargetableObject import DistributedTargetableObject
from pirates.battle import EnemyGlobals

class DistributedMovingObject(DistributedSmoothNode, DistributedTargetableObject, SmoothGridChild):
    notify = directNotify.newCategory('DistributedMovingObject')

    def __init__(self, cr):
        DistributedSmoothNode.__init__(self, cr)
        DistributedTargetableObject.__init__(self, cr)
        SmoothGridChild.__init__(self)
        self.maxAISpeed = 0
        self.canMove = True
        self.aggroMode = EnemyGlobals.AGGRO_MODE_FORCED
        self.debugName = None
        self.debugNameNP = None
        self.spawnPosIndex = ''
        return

    def setSpawnPosIndex(self, index):
        self.spawnPosIndex = index

    def getSpawnPosIndex(self):
        return self.spawnPosIndex

    def requestGameState(self, state):
        pass

    def generate(self):
        DistributedSmoothNode.generate(self)
        DistributedTargetableObject.generate(self)
        if base.config.GetBool('create-client-coll-spheres', 0) is 1:
            self.setupDebugCollisions()

    def announceGenerate(self):
        DistributedSmoothNode.announceGenerate(self)
        DistributedTargetableObject.announceGenerate(self)

    def disable(self):
        self.stopSmooth()
        DistributedSmoothNode.disable(self)
        DistributedTargetableObject.disable(self)
        if base.config.GetBool('create-client-coll-spheres', 0) is 1:
            self.cleanupDebugcollisions()
        base.cr.handleObjDelete(self)

    def delete(self):
        DistributedSmoothNode.delete(self)
        DistributedTargetableObject.delete(self)
        SmoothGridChild.delete(self)

    def setLocation(self, parentId, zoneId):
        DistributedSmoothNode.setLocation(self, parentId, zoneId)

    def wrtReparentTo(self, parent):
        DistributedSmoothNode.wrtReparentTo(self, parent)

    def transformTelemetry(self, x, y, z, h, p, r, e):
        return SmoothGridChild.transformTelemetry(self, x, y, z, h, p, r, e)

    def updateCurrentZone(self):
        return SmoothGridChild.updateCurrentZone(self)

    def setupDebugCollisions(self):
        pass

    def cleanupDebugcollisions(self):
        pass

    def setMaxSpeed(self, speed):
        self.maxAISpeed = speed

    def getMaxSpeed(self):
        return self.maxAISpeed

    def wantsSmoothing(self):
        return 1

    def setMyPosHpr(self, x, y, z, h, p, r):
        self.setPosHpr(x, y, z, h, p, r)

    def showDebugName(self):
        if __debug__ and base.config.GetBool('move-obj-nametags', 0) is 1:
            if self.debugNameNP:
                self.debugNameNP.removeNode()
            else:
                self.debugName = TextNode('NPCName')
                self.debugName.setAlign(TextNode.ACenter)
                self.debugName.setTextColor(0, 0, 0, 1)
            debugNameText = str(self.getDoId()) + ' (Team:' + str(self.getTeam()) + ')'
            if hasattr(self, 'level'):
                debugNameText += ' (Lvl: ' + str(self.level) + ')'
            self.debugName.setText(debugNameText)
            self.debugNameNP = self.attachNewNode(self.debugName.generate())
            posAndScale = self.getDebugNamePosScale()
            self.debugNameNP.setPos(*posAndScale[0])
            self.debugNameNP.setScale(posAndScale[1])
            self.debugNameNP.setBillboardPointEye(2)
            CullBinManager.getGlobalPtr().addBin('gui-popup', CullBinManager.BTUnsorted, 60)
            self.debugNameNP.setBin('gui-popup', 0)
            self.debugNameNP.setDepthTest(0)

    def getDebugNamePosScale(self):
        return [
         (0, 0, 10), 2.0]

    def setStartState(self, startState):
        self.startState = startState

    def setAggroRadius(self, val):
        self.aggroRadius = val

    def getAggroRadius(self):
        return self.aggroRadius

    def setAggroMode(self, val):
        self.aggroMode = val

    def getAggroMode(self):
        return self.aggroMode

    def getEffectiveAggroRadius(self):
        if self.aggroRadius == EnemyGlobals.USE_DEFAULT_AGGRO:
            return base.cr.gameStatManager.getInstantAggroRadius()
        else:
            return self.aggroRadius

    def getSkillRankBonus(self, skillId):
        return 0

    def getSkillRank(self, skillId):
        return 0