from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedShipLoaderUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipLoaderUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)