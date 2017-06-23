from pirates.quest.QuestPath import QuestStep
from pirates.quest.QuestIndicatorNodeNPC import QuestIndicatorNodeNPC
from pirates.quest.QuestIndicatorNodeNPCOffset import QuestIndicatorNodeNPCOffset
from pirates.quest.QuestIndicatorNodeItem import QuestIndicatorNodeItem
from pirates.quest.QuestIndicatorNodeArea import QuestIndicatorNodeArea
from pirates.quest.QuestIndicatorNodeTunnel import QuestIndicatorNodeTunnel
from pirates.quest.QuestIndicatorNodeExtDoor import QuestIndicatorNodeExtDoor
from pirates.quest.QuestIndicatorNodeIntDoor import QuestIndicatorNodeIntDoor
from pirates.quest.QuestIndicatorNodeQuestNode import QuestIndicatorNodeQuestNode
from pirates.quest.QuestIndicatorNodeDinghy import QuestIndicatorNodeDinghy
from pirates.quest.QuestIndicatorNodeShip import QuestIndicatorNodeShip
from pirates.quest.QuestIndicatorNodeNPCArea import QuestIndicatorNodeNPCArea
from pirates.quest.QuestIndicatorNodeQuestProp import QuestIndicatorNodeQuestProp

class QuestStepIndicator():
    TypeMap = {QuestStep.STNPC: QuestIndicatorNodeNPCOffset,QuestStep.STNPCEnemy: QuestIndicatorNodeNPC,QuestStep.STItem: QuestIndicatorNodeItem,QuestStep.STArea: QuestIndicatorNodeArea,QuestStep.STTunnel: QuestIndicatorNodeTunnel,QuestStep.STExteriorDoor: QuestIndicatorNodeExtDoor,QuestStep.STInteriorDoor: QuestIndicatorNodeIntDoor,QuestStep.STQuestNode: QuestIndicatorNodeQuestNode,QuestStep.STDinghy: QuestIndicatorNodeDinghy,QuestStep.STShip: QuestIndicatorNodeShip,QuestStep.STNPCArea: QuestIndicatorNodeNPCArea,QuestStep.STQuestProp: QuestIndicatorNodeQuestProp}

    def __init__(self):
        self.questStep = None
        self.indicatorNode = None
        self.muted = False
        return

    def delete(self):
        self.hideQuestStep()
        self.indicatorNone = None
        self.questStep = None
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def showQuestStep(self, questStep):
        if self.questStep is not questStep:
            self.hideQuestStep()
            self.questStep = questStep
            if self.questStep:
                questType = questStep.getStepType()
                IndicatorClass = QuestStepIndicator.TypeMap.get(questType)
                if IndicatorClass:
                    self.indicatorNode = IndicatorClass(questStep)
                    if self.muted:
                        self.hideEffect()

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def hideQuestStep(self):
        if self.indicatorNode:
            self.indicatorNode.delete()
            self.indicatorNode = None
        self.questStep = None
        return

    def showEffect(self):
        self.muted = False
        if self.indicatorNode:
            self.indicatorNode.showEffect()

    def hideEffect(self):
        self.muted = True
        if self.indicatorNode:
            self.indicatorNode.hideEffect()