from direct.distributed.DistributedObjectUD import DistributedObjectUD
from direct.directnotify import DirectNotifyGlobal

class DistributedInventoryUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryUD')

    def __init__(self, air):
        DistributedObjectUD.__init__(self, air)
