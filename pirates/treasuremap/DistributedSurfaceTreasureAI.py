from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedSurfaceTreasureAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSurfaceTreasureAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)