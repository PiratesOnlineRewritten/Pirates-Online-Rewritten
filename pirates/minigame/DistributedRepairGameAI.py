from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedRepairGameAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRepairGameAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)