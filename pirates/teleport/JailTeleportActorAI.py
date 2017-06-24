from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class JailTeleportActorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('JailTeleportActorAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)