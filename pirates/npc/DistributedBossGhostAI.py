from pirates.npc.DistributedGhostAI import DistributedGhostAI
from pirates.npc.BossAI import BossAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBossGhostAI(DistributedGhostAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossGhostAI')

    def __init__(self, air):
        DistributedGhostAI.__init__(self, air)
        BossAI.__init__(self, air)