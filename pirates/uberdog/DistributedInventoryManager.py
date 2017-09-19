from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify import DirectNotifyGlobal

class DistributedInventoryManager(DistributedObjectGlobal):
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryManager')

    def d_sendRequestInventory(self):
        self.sendUpdate('requestInventory', [])
