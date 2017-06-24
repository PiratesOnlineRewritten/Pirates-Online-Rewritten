from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBattleAvatarAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleAvatarAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)