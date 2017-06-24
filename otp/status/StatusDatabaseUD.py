from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class StatusDatabaseUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('StatusDatabaseUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)