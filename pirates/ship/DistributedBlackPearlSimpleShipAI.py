from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBlackPearlSimpleShipAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackPearlSimpleShipAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)