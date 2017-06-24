from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PVPGameShipBattleAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameShipBattleAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)