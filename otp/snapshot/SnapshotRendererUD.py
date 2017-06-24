from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class SnapshotRendererUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('SnapshotRendererUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)