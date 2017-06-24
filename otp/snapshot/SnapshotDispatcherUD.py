from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class SnapshotDispatcherUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('SnapshotDispatcherUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)