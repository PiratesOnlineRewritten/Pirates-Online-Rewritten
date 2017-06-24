from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PCGuildManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PCGuildManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)