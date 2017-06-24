from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedRepairBenchAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRepairBenchAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)