from direct.directnotify import DirectNotifyGlobal
from pirates.npc.BossBase import BossBase
from pirates.npc.BossNPCList import BOSS_NPC_LIST

class BossAI(BossBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('BossAI')

    def __init__(self, air):
        BossBase.__init__(self, air)
        self.air = air

    def getBossName(self):
        return self.bossData['Name']

    def getBossLevel(self):
        return self.bossData['Level']