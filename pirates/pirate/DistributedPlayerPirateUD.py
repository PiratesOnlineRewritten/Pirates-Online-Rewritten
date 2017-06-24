from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedPlayerPirateUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerPirateUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)