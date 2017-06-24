from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedGoldReceiptUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGoldReceiptUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)