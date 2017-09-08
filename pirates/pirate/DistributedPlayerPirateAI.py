from direct.directnotify import DirectNotifyGlobal
from otp.avatar.DistributedPlayerAI import DistributedPlayerAI
from pirates.pirate.HumanDNA import HumanDNA
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI
from pirates.quest.DistributedQuestAvatarAI import DistributedQuestAvatarAI

class DistributedPlayerPirateAI(DistributedPlayerAI, HumanDNA, DistributedBattleAvatarAI, DistributedQuestAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPlayerPirateAI')

    def __init__(self, air):
        DistributedPlayerAI.__init__(self, air)
        HumanDNA.__init__(self)
        DistributedBattleAvatarAI.__init__(self, air)
        DistributedQuestAvatarAI.__init__(self, air)

    def d_relayTeleportLoc(self, shardId, zoneId, teleportMgrDoId):
        self.sendUpdateToAvatarId(self.doId, 'relayTeleportLoc', [shardId, zoneId, teleportMgrDoId])
