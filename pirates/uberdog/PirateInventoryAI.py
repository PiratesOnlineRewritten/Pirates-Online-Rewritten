from pirates.uberdog.DistributedInventoryAI import DistributedInventoryAI
from direct.directnotify import DirectNotifyGlobal

class PirateInventoryAI(DistributedInventoryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateInventoryAI')

    def setGoldInPocket(self, quantity):
        self.b_setStack(InventoryType.ItemTypeMoney, quantity)

    def getGoldInPocket(self):
        item = self.getStack(InventoryType.ItemTypeMoney)

        if not item:
            return 0

        return item[1]

    def setOverallRep(self, quantity):
        self.b_setAccumulator(InventoryType.OverallRep, quantity)

    def getOverallRep(self):
        item = self.getAccumulator(InventoryType.OverallRep)

        if not item:
            return 0

        return item[1]

    def setPotionsRep(self, quantity):
        self.b_setAccumulator(InventoryType.PotionsRep, quantity)

    def getPotionsRep(self):
        item = self.getAccumulator(InventoryType.PotionsRep)

        if not item:
            return 0

        return item[1]

    def setFishingRep(self, quantity):
        self.b_setAccumulator(InventoryType.FishingRep, quantity)

    def getFishingRep(self):
        item = self.getAccumulator(InventoryType.FishingRep)

        if not item:
            return 0

        return item[1]
