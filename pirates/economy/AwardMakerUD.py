from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class AwardMakerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('AwardMakerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)