from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class PiratesSpeedchatRelayUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesSpeedchatRelayUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)