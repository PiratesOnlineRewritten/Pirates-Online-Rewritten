from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class SnapshotDispatcherAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SnapshotDispatcherAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)