from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPVPBattleAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPVPBattleAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)