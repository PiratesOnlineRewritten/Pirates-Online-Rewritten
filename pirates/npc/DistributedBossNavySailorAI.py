from pirates.npc.BossAI import BossAI
from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedNPCNavySailorAI import DistributedNPCNavySailorAI

class DistributedBossNavySailorAI(DistributedNPCNavySailorAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossNavySailorAI')

    def __init__(self, air):
        DistributedNPCNavySailorAI.__init__(self, air)
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