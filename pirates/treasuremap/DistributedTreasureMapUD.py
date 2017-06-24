from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedTreasureMapUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTreasureMapUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)