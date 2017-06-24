from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class ObjectServerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('ObjectServerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)