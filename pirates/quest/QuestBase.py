from pirates.quest import QuestReward
from pirates.quest import QuestDB, QuestLadderDB

class QuestBase():

    def __init__(self):
        self.owningAvId = None
        return

    def announceGenerate(self):
        if self.questDNA and self.owningAvId:
            questModInfo = self.questDNA.getQuestMod()
            owningAv = getBase().getRepository().getDo(self.owningAvId)
            if questModInfo and owningAv:
                owningAv.addQuestNPCInterest(questModInfo[0], self.doId)

    def delete(self):
        if self.questDNA:
            questModInfo = self.questDNA.getQuestMod()
            owningAv = getBase().getRepository().getDo(self.owningAvId)
            if questModInfo and owningAv:
                owningAv.removeQuestNPCInterest(questModInfo[0])
            messenger.send(self.getDeletedEventString(), [self.getDeletedEventString()])

    def setOwningAv(self, avId):
        self.owningAvId = avId

    def getOwningAv(self):
        return self.owningAvId

    def getCompleteEventString(self):
        return 'quest-complete-%d' % self.doId

    def getDroppedEventString(self):
        return 'quest-dropped-%d' % self.doId

    def getDeletedEventString(self):
        return 'quest-deleted-%d' % self.doId


def questObjMod(quests, object, av, repository):
    for currQuestInt in quests:
        currId = QuestDB.getQuestIdFromQuestInt(currQuestInt)
        if currId:
            containerDNA = QuestDB.QuestDict.get(currId)
        else:
            containerDNA = QuestLadderDB.getContainerFromQuestInt(currQuestInt)
        questModInfo = containerDNA.getQuestMod()
        questObjId = None
        if questModInfo:
            questObjId = questModInfo[0]
        if questObjId in [object.getUniqueId(), object.getSpawnPosIndex()]:
            questInterestId = av.hasQuestNPCInterest(object.getUniqueId())
            if QuestLadderDB.questIntInHistory(currQuestInt, av.getQuestLadderHistory()):
                return questModInfo[3]
            elif questInterestId:
                questObj = repository.doId2do.get(questInterestId)
                if questObj and questObj.isComplete():
                    return questModInfo[3]
                return questModInfo[2]
            else:
                return questModInfo[1]

    return