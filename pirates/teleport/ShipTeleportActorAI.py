from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class ShipTeleportActorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShipTeleportActorAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)