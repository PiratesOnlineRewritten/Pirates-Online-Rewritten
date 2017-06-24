from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class PSnapshotRendererUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PSnapshotRendererUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)