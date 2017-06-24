from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedTeleportZoneUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportZoneUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)