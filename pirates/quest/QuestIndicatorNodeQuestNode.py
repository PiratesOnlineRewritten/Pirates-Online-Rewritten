from pirates.piratesgui.RadarGui import *
from pirates.quest.QuestIndicatorNode import QuestIndicatorNode
from pirates.piratesgui.RadarGui import RADAR_OBJ_TYPE_QUEST
from direct.showbase.PythonUtil import report, StackTrace

class QuestIndicatorNodeQuestNode(QuestIndicatorNode):

    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorNode.__init__(self, 'QuestNodeIndicator', questStep.nodeSizes, questStep)
        return

    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        self.ignore('tunnelSetLinks')
        QuestIndicatorNode.delete(self)
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def placeInWorld(self):
        originObj = base.cr.doId2do.get(self.questStep.getOriginDoId())
        if originObj:
            posH = self.questStep.getPosH()
            pos, h = posH[:3], posH[3]
            self.reparentTo(originObj)
            self.setPos(*pos)
            self.setHpr(h, 0, 0)
            self.setZoneLODOffset(1, Point3(*self.questStep.getNearOffset()))

    def loadZoneLevel(self, level):
        if level == 0:
            self.request('At')
        elif level == 1:
            self.request('Near')
        elif level == 2:
            self.request('Far')

    def unloadZoneLevel(self, level, cacheObs=False):
        if level == 0:
            self.request('Near')
        elif level == 1:
            self.request('Far')
        elif level == 2:
            self.request('Off')

    def enterFar(self):
        QuestIndicatorNode.enterFar(self)
        if self.farEffect:
            self.farEffect.setPos(*self.questStep.getNearVis())

    def exitFar(self):
        QuestIndicatorNode.exitFar(self)

    def enterNear(self):
        self.startFarEffect()

    def exitNear(self):
        self.stopFarEffect()

    def enterAt(self):
        pass

    def exitAt(self):
        pass

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def startFarEffect(self):
        QuestIndicatorNode.startFarEffect(self)
        if self.farEffect:
            self.farEffect.setPos(0, 0, -3.5)

    def updateGuiHints(self, questId):
        pass