from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.inventory.LootableAI import LootableAI
from direct.directnotify import DirectNotifyGlobal

class DistributedFishingSpotAI(DistributedInteractiveAI, LootableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFishingSpotAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        LootableAI.__init__(self, air)
        self.index = 0
        self.oceanOffset = 0
        self.onBoat = False

    def setIndex(self, index):
        self.index = index

    def d_setIndex(self, index):
        self.sendUpdate('setIndex', [index])

    def b_setIndex(self, index):
        self.setIndex(index)
        self.d_setIndex(index)

    def getIndex(self):
        return self.index

    def setOceanOffset(self, offset):
        self.oceanOffset = offset

    def d_setOceanOffset(self, offset):
        self.sendUpdate('setOceanOffset', [offset])

    def b_setOceanOffset(self, offset):
        self.setOceanOffset(offset)
        self.d_setOceanOffset(offset)

    def getOceanOffset(self):
        return self.oceanOffset

    def setOnABoat(self, onBoat):
        self.onBoat = onBoat

    def d_setOnABoat(self, onBoat):
        self.sendUpdate('setOnABoat', [onBoat])

    def b_setOnABoat(self, onBoat):
        self.setOnABoat(onBoat)
        self.d_setOnABoat(onBoat)

    def getOnABoat(self):
        return self.onBoat

    def caughtFish(self, fishId, weight):
        pass

    def lostLure(self, lureId):
        pass

    def d_firstTimeFisher(self, avatarId):
        self.sendUpdateToAvaarId(avatarId, 'firstTimeFisher', [])

    def d_spotFilledByAvId(self, avId):
        self.sendUpdate('spotFilledByAvId', [avId])

    def d_setXpBonus(self, xpBonusAmount):
        self.sendUpdate('setXpBonus', [xpBonusAmount])

    def d_setGoldBonus(self, goldBonusAmount):
        self.sendUpdate('setGoldBonus', [goldBonusAmount])




