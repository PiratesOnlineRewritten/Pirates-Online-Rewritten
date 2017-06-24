from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBattleNPCAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleNPCAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)