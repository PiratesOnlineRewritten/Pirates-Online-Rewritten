from pirates.quest.QuestIndicatorNodeNPC import QuestIndicatorNodeNPC

class QuestIndicatorNodeNPCOffset(QuestIndicatorNodeNPC):

    def __init__(self, questStep):
        QuestIndicatorNodeNPC.__init__(self, questStep)
        self.wantBottomEffect = False

    def startNearEffect(self):
        QuestIndicatorNodeNPC.startNearEffect(self)
        if self.nearEffect and self.stepObj:
            if hasattr(self.stepObj, 'getQuestIndicatorOffset'):
                self.nearEffect.setPos(self.stepObj.getQuestIndicatorOffset())
            else:
                self.nearEffect.setPos(0, 0, 0)

    def startFarEffect(self):
        QuestIndicatorNodeNPC.startFarEffect(self)
        if self.farEffect and self.stepObj:
            if hasattr(self.stepObj, 'getQuestIndicatorOffset'):
                self.farEffect.setPos(self.stepObj.getQuestIndicatorOffset())
            else:
                self.farEffect.setPos(0, 0, 0)