from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PVPGameTeamBattleAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameTeamBattleAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)