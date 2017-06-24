from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPVPShipBattleAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPVPShipBattleAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)