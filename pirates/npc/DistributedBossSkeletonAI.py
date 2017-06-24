from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBossSkeletonAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossSkeletonAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)