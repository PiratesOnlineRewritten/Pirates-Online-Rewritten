from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedCrewMatchManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrewMatchManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)