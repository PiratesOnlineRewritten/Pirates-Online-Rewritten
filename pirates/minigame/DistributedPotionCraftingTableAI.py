from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedPotionGameAI import DistributedPotionGameAI

class DistributedPotionCraftingTableAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPotionCraftingTableAI')
    MULTIUSE = True
    
    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

        self.potionZone = 0
        self.avatar2game = {}

    def handleRequestInteraction(self, avatar, interactType, instant):
        if avatar.doId in self.avatar2game:
            return self.DENY

        self.avatar2game[avatar.doId] = DistributedPotionGameAI(self.air)
        self.avatar2game[avatar.doId].setTable(self)
        self.avatar2game[avatar.doId].setAvatar(avatar)
        self.avatar2game[avatar.doId].setColorSet(self.potionZone)
        self.avatar2game[avatar.doId].generateWithRequiredAndId(self.air.allocateChannel(), self.doId, avatar.doId)

        return self.ACCEPT

    def handleRequestExit(self, avatar):
        if avatar.doId not in self.avatar2game:
            return self.DENY

        self.avatar2game[avatar.doId].requestDelete()
        del self.avatar2game[avatar.doId]

        return self.ACCEPT

    def setPotionZone(self, potionZone):
        self.potionZone = potionZone
