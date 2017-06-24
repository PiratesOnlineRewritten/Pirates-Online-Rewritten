from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class InteriorDoorTeleportActorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('InteriorDoorTeleportActorAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)