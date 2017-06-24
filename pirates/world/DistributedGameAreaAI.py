from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedGameAreaAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameAreaAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)