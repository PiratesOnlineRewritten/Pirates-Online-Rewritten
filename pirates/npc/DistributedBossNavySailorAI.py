from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from pirates.npc.BossAI import BossAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBossNavySailorAI(DistributedBattleNPCAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossNavySailorAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
        BossAI.__init__(self, air)
        self.dnaId = ''

    def setDNAId(self, dnaId):
        self.dnaId = dnaId

    def d_setDNAId(self, dnaId):
        self.sendUpdate('setDNAId', [dnaId])

    def b_setDNAId(self, dnaId):
        self.setDNAId(dnaId)
        self.d_setDNAId(dnaId)

    def getDNAId(self):
        return self.dnaId