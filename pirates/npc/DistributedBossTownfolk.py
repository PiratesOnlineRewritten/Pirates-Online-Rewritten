from pandac.PandaModules import Vec4
from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedNPCTownfolk import DistributedNPCTownfolk
from pirates.pirate import AvatarTypes
from pirates.npc.Boss import Boss

class DistributedBossTownfolk(DistributedNPCTownfolk, Boss):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossTownfolk')

    def __init__(self, cr):
        DistributedNPCTownfolk.__init__(self, cr)
        Boss.__init__(self, cr)

    def announceGenerate(self):
        DistributedNPCTownfolk.announceGenerate(self)
        self.addBossEffect(AvatarTypes.Navy)

    def disable(self):
        self.removeBossEffect()
        DistributedNPCTownfolk.disable(self)

    def setAvatarType(self, avatarType):
        DistributedNPCTownfolk.setAvatarType(self, avatarType)
        self.loadBossData(self.getUniqueId(), avatarType)

    def getEnemyScale(self):
        return Boss.getEnemyScale(self)

    def getBossEffect(self):
        return Boss.getBossEffect(self)

    def getBossHighlightColor(self):
        return Boss.getBossHighlightColor(self)

    def getShortName(self):
        return Boss.getShortName(self)

    def skipBossEffect(self):
        return self.isGhost