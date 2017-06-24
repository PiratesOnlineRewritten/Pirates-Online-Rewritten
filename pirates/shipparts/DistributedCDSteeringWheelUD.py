from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedCDSteeringWheelUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCDSteeringWheelUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)