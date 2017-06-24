from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class PCGuildManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCGuildManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)