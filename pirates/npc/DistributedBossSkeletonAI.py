from pirates.npc.DistributedNPCSkeletonAI import DistributedNPCSkeletonAI
from pirates.npc.BossAI import BossAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBossSkeletonAI(DistributedNPCSkeletonAI, BossAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossSkeletonAI')

    def __init__(self, air):
        DistributedNPCSkeletonAI.__init__(self, air)
        BossAI.__init__(self, air)