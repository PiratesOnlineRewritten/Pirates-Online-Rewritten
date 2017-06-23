from pirates.piratesgui.RadarGui import *
from pirates.quest.QuestIndicatorGridNode import QuestIndicatorGridNode
from direct.showbase.PythonUtil import report, StackTrace

class QuestIndicatorNodeNPCArea(QuestIndicatorGridNode):

    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorGridNode.__init__(self, 'NPCAreaIndicator', [
         350, 400], questStep)
        self.wantBottomEffect = False
        return

    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        QuestIndicatorGridNode.delete(self)
        return

    def loadZoneLevel(self, level):
        QuestIndicatorGridNode.loadZoneLevel(self, level)

    def unloadZoneLevel(self, level):
        QuestIndicatorGridNode.unloadZoneLevel(self, level)

    def enterFar(self):
        QuestIndicatorGridNode.enterFar(self)
        self.updateGuiHints(localAvatar.activeQuestId)

    def enterNear(self):
        QuestIndicatorGridNode.enterNear(self)
        self.updateGuiHints(localAvatar.activeQuestId)

    def enterAt(self):
        QuestIndicatorGridNode.enterAt(self)

    def exitAt(self):
        pass

    def updateGuiHints(self, questId):
        if not hasattr(localAvatar, 'guiMgr') or not localAvatar.guiMgr:
            return
        hintText = ''
        quest = localAvatar.getQuestById(questId)
        if quest and not quest.isComplete():
            state = self.state
            if hasattr(self, 'newState'):
                state = self.newState
            if state in ['At', 'Near']:
                localAvatar.guiMgr.radarGui.showGlowRing()
                hintText = PLocalizer.TargetsCloseBy
            else:
                localAvatar.guiMgr.radarGui.hideGlowRing()
                hintText = PLocalizer.TargetsInHere
        else:
            localAvatar.guiMgr.radarGui.hideGlowRing()
        if self.minimapObject:
            self.minimapObject.mapGeom.stash()
        localAvatar.guiMgr.setQuestHintText(hintText)