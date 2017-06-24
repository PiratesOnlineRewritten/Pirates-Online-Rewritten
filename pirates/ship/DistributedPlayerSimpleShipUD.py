from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedPlayerSimpleShipUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerSimpleShipUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)