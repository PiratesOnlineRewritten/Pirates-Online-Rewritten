from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBossNavySailorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossNavySailorAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)