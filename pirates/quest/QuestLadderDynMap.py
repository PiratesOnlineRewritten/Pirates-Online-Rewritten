from direct.directnotify import DirectNotifyGlobal
from pirates.quest import QuestLadder
from pirates.quest import QuestLadderDB
from pirates.quest import QuestDB

class QuestLadderDynMap():

    def __init__(self):
        self.QuestIDLadderDynMap = {}
        for ladderId, ladderDNA in QuestLadderDB.FortuneQuestLadderDict.items():
            ladderInt = ladderDNA.questInt
            for container in ladderDNA.getContainers():
                if container.isContainer():
                    self.getMappingFromContainer(container, ladderId, ladderInt)
                else:
                    self.addMapping(container.questId, ladderId, ladderInt)

        for ladderId, ladderDNA in QuestLadderDB.FameQuestLadderDict.items():
            ladderInt = ladderDNA.questInt
            for container in ladderDNA.getContainers():
                if container.isContainer():
                    self.getMappingFromContainer(container, ladderId, ladderInt)
                else:
                    self.addMapping(container.questId, ladderId, ladderInt)

    def getMappingFromContainer(self, container, ladderId, ladderInt):
        for containerChild in container.getContainers():
            if containerChild.isContainer():
                self.getMappingFromContainer(containerChild, ladderId, ladderInt)
            else:
                self.addMapping(containerChild.questId, ladderId, ladderInt)

    def addMapping(self, questId, ladderId, ladderInt):
        ladder = (
         ladderId, ladderInt)
        self.QuestIDLadderDynMap[questId] = ladder

    def findQuestLadderId(self, questId):
        if questId == 'test.1visit':
            return 'Error'
        if questId == 'test.3visit':
            return 'Error'
        ladder = self.QuestIDLadderDynMap[questId]
        return ladder[0]

    def findQuestLadderInt(self, questId):
        if questId == 'test.1visit':
            return 8888
        if questId == 'test.3visit':
            return 8888
        ladder = self.QuestIDLadderDynMap[questId]
        return ladder[1]

    def getCompleteMapping(self):
        return self.QuestIDLadderDynMap