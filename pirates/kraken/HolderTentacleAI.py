from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class HolderTentacleAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('HolderTentacleAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)