from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DoorTeleportActorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DoorTeleportActorAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)