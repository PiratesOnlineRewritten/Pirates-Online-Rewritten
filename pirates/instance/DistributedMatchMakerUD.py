from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedMatchMakerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMatchMakerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)