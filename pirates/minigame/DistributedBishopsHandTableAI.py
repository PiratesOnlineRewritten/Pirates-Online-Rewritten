from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBishopsHandTableAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBishopsHandTableAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)