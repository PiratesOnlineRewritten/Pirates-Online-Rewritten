from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedNPCSimpleShipAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCSimpleShipAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)