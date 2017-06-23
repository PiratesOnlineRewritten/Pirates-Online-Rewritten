from pirates.quest.QuestIndicatorNode import QuestIndicatorNode
from direct.showbase.PythonUtil import report, StackTrace

class QuestIndicatorNodeDinghy(QuestIndicatorNode):

    def __init__(self, questStep):
        self.nearEffect = None
        QuestIndicatorNode.__init__(self, 'DinghyIndicator', [
         50], questStep)
        return

    def placeInWorld(self):
        originObj = base.cr.doId2do.get(self.questStep.getOriginDoId())
        if originObj:
            posH = self.questStep.getPosH()
            pos, h = posH[:3], posH[3]
            self.reparentTo(originObj)
            self.setPos(*pos)
            self.setHpr(h, 0, 0)

    def loadZoneLevel(self, level):
        QuestIndicatorNode.loadZoneLevel(self, level)
        if level == 0:
            self.stopTargetRefresh()
        elif level == 1:
            self.request('Far')
            self.requestTargetRefresh()

    def unloadZoneLevel(self, level):
        QuestIndicatorNode.unloadZoneLevel(self, level)
        if level == 0:
            self.requestTargetRefresh()
        elif level == 1:
            self.stopTargetRefresh()
            self.request('Off')