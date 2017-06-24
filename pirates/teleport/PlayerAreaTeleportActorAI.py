from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PlayerAreaTeleportActorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayerAreaTeleportActorAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)