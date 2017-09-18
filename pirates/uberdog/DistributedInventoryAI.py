from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInventoryAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.ownerId = 0

    def generate(self):
        self.air.inventoryManager.addInventory(self)

        DistributedObjectAI.generate(self)

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])

    def b_setOwnerId(self, ownerId):
        self.setOwnerId(ownerId)
        self.d_setOwnerId(ownerId)

    def getOwnerId(self):
        return self.ownerId

    def d_requestInventoryComplete(self):
        self.sendUpdateToAvatarId(self.ownerId, 'requestInventoryComplete', [])

    def delete(self):
        self.air.inventoryManager.removeInventory(self)

        DistributedObjectAI.delete(self)
