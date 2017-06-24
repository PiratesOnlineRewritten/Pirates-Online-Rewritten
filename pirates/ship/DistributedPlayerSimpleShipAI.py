from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPlayerSimpleShipAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerSimpleShipAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)