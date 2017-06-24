from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPopulationTrackerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPopulationTrackerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)