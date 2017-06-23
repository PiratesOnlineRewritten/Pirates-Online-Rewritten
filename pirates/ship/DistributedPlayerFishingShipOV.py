from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObjectOV

class DistributedPlayerFishingShipOV(DistributedObjectOV.DistributedObjectOV):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerFishingShipOV')

    def __init__(self, cr):
        DistributedObjectOV.DistributedObjectOV.__init__(self, cr)