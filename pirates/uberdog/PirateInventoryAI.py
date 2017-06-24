from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PirateInventoryAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateInventoryAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)