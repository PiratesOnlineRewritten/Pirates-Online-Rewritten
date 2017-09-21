from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBossNavySailorAI(DistributedBattleNPCAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossNavySailorAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)