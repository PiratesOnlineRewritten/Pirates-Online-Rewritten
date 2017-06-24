from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedCannonDefenseShipAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCannonDefenseShipAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)