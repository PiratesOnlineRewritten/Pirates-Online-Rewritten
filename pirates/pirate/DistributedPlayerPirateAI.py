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

        self.inventoryId = 0
        self.founder = False
        self.defaultShard = 0
        self.defaultZone = 0

    def setInventoryId(self, inventoryId):
        self.inventoryId = inventoryId

    def d_setInventoryId(self, inventoryId):
        self.sendUpdate('setInventoryId', [inventoryId])

    def b_setInventoryId(self, inventoryId):
        self.setInventoryId(inventoryId)
        self.d_setInventoryId(inventoryId)

    def getInventoryId(self):
        return self.inventoryId

    def getInventory(self):
        return self.air.doId2do.get(self.inventoryId)

    def d_relayTeleportLoc(self, shardId, zoneId, teleportMgrDoId):
        self.sendUpdateToAvatarId(self.doId, 'relayTeleportLoc', [shardId, zoneId, teleportMgrDoId])

    def setFounder(self, founder):
        self.founder = founder

    def d_setFounder(self, founder):
        self.sendUpdate('setFounder', [founder])

    def b_setFounder(self, founder):
        self.setFounder(founder)
        self.d_setFounder(founder)

    def getFounder(self):
        return self.founder

    def setDefaultShard(self, defaultShard):
        self.defaultShard = defaultShard

    def d_setDefaultShard(self, defaultShard):
        self.sendUpdate('setDefaultShard', [defaultShard])

    def b_setDefaultShard(self, defaultShard):
        self.setDefaultShard(defaultShard)
        self.d_setDefaultShard(defaultShard)

    def getDefaultShard(self):
        return self.defaultShard

    def setDefaultZone(self, defaultZone):
        self.defaultZone = defaultZone

    def d_setDefaultZone(self, defaultZone):
        self.sendUpdate('setDefaultZone', [defaultZone])

    def b_setDefaultZone(self, defaultZone):
        self.setDefaultZone(defaultZone)
        self.d_setDefaultZone(defaultZone)

    def getDefaultZone(self):
        return self.defaultZone

    def d_forceTeleportStart(self, instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone):
        self.sendUpdateToAvatarId(self.doId, 'forceTeleportStart', [instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone])

    def destroy(self):
        self.d_setGameState('TeleportOut')

        DistributedPlayerAI.destroy(self)
        DistributedBattleAvatarAI.destroy(self)
