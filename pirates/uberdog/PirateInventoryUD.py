from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class PirateInventoryUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PirateInventoryUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)