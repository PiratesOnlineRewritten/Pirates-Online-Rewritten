from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class ExteriorDoorTeleportActorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('ExteriorDoorTeleportActorAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)