from pirates.uberdog.DistributedInventoryAI import DistributedInventoryAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType

class PirateInventoryAI(DistributedInventoryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateInventoryAI')

    def setGoldInPocket(self, quantity):
        self.b_setStack(InventoryType.ItemTypeMoney, quantity)

    def getGoldInPocket(self):
        return self.getItem(self.getStack, InventoryType.ItemTypeMoney)

    def setOverallRep(self, quantity):
        self.b_setAccumulator(InventoryType.OverallRep, quantity)

    def getOverallRep(self):
        return self.getItem(self.getAccumulator, InventoryType.OverallRep)

    def setPotionsRep(self, quantity):
        self.b_setAccumulator(InventoryType.PotionsRep, quantity)

    def getPotionsRep(self):
        return self.getItem(self.getAccumulator, InventoryType.PotionsRep)

    def setFishingRep(self, quantity):
        self.b_setAccumulator(InventoryType.FishingRep, quantity)

    def getFishingRep(self):
        return self.getItem(self.getAccumulator, InventoryType.FishingRep)
