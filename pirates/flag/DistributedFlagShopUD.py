from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedFlagShopUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlagShopUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)