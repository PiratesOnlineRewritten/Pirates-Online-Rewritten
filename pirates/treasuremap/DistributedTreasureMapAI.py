from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTreasureMapAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTreasureMapAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)