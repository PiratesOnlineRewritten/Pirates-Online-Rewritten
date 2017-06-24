from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class AreaTeleportActorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('AreaTeleportActorAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)