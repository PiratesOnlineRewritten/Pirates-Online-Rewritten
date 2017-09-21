from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from direct.directnotify import DirectNotifyGlobal

class DistributedNPCSkeletonAI(DistributedBattleNPCAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCSkeletonAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
