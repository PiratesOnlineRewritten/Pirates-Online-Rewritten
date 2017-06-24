from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedSteeringWheelUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSteeringWheelUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)