from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTreasureMapInstanceAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTreasureMapInstanceAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)