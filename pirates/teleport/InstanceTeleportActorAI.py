from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class InstanceTeleportActorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('InstanceTeleportActorAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)