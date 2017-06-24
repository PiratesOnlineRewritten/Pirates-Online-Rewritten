from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPlayerSeizeableShipAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerSeizeableShipAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)