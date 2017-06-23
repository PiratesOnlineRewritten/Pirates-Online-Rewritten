from direct.directnotify.DirectNotifyGlobal import directNotify

class QuestAvatarBase():
    notify = directNotify.newCategory('QuestAvatarBase')

    def __init__(self):
        self.questNPCInterest = {}

    def getQuests(self):
        inventory = self.getInventory()
        if inventory is None:
            err = 'could not get inventory'
            if hasattr(self, 'doId'):
                err += ' for %s' % self.doId
            return []
        else:
            return inventory.getQuestList()
        return

    def getQuestById(self, questId):
        quests = self.getQuests()
        for currQuest in quests:
            if currQuest.questId == questId:
                return currQuest

        return None

    def addQuestNPCInterest(self, npcId, questId):
        self.questNPCInterest[npcId] = questId
        messenger.send('questInterestChange-%s' % npcId, [])

    def removeQuestNPCInterest(self, npcId):
        self.questNPCInterest.pop(npcId, None)
        messenger.send('questInterestChange-%s' % npcId, [])
        return

    def hasQuestNPCInterest(self, npcId):
        return self.questNPCInterest.get(npcId)