from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PVPGameBattleAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameBattleAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)