from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from pirates.uberdog.UberDogGlobals import *

class DistributedInventoryManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('InventoryManager')

    def sendRequestInventory(self):
        self.sendUpdate('requestInventory')