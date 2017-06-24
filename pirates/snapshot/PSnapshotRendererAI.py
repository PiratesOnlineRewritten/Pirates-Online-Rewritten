from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PSnapshotRendererAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PSnapshotRendererAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)