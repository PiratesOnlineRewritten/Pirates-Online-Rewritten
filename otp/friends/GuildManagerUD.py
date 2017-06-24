from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class GuildManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('GuildManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)