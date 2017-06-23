from AITrade import AITrade
from pirates.uberdog.UberDogGlobals import GiftOrigin, InventoryCategory, InventoryType, InventoryId
from direct.directnotify.DirectNotifyGlobal import directNotify

class AIMagicWordTrade(AITrade):
    notify = directNotify.newCategory('AIMagicWordTrade')

    def __init__(self, distObj, fromId, avatarId=None, inventoryId=None, timeout=4.0):
        AITrade.__init__(self, distObj, avatarId, inventoryId, timeout)
        self.giftOrigin = GiftOrigin.MAGIC_WORD
        self.fromId = fromId

    def _checkRules(self, givingLimitChanges, givingStacks, givingAccumulators, givingDoIds, givingLocatable, takingLimitChanges, takingStacks, takingAccumulators, takingDoIds, takingLocatable):
        pass

    def setAccumulator(self, accumulatorType, quantity):
        setAccumulator = InventoryId.getLimitChange(accumulatorType)
        self.giving.append((setAccumulator, quantity))

    def setReputation(self, category, amount):
        self.setAccumulator(category, amount)

    def getOrigin(self):
        return self.giftOrigin