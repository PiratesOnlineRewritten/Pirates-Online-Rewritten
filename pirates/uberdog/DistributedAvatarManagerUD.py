from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedAvatarManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAvatarManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)