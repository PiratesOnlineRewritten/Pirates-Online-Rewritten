from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPVPTeamBattleAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPVPTeamBattleAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)