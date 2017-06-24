from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedShipCannonUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipCannonUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)