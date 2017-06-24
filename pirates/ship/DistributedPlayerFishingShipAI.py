from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPlayerFishingShipAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerFishingShipAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)