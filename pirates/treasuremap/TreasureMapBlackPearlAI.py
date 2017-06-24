from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class TreasureMapBlackPearlAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TreasureMapBlackPearlAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)