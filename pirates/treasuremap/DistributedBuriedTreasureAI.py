from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBuriedTreasureAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuriedTreasureAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)