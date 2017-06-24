from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedPCCannonUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPCCannonUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)