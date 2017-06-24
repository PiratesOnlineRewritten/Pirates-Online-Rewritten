from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedNPCSkeletonAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCSkeletonAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)