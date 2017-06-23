from pandac.PandaModules import Vec4
from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedNPCSkeleton import DistributedNPCSkeleton
from pirates.pirate import AvatarTypes
from pirates.npc.Boss import Boss

class DistributedBossSkeleton(DistributedNPCSkeleton, Boss):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossSkeleton')

    def __init__(self, cr):
        DistributedNPCSkeleton.__init__(self, cr)
        Boss.__init__(self, cr)

    def generate(self):
        DistributedNPCSkeleton.generate(self)

    def announceGenerate(self):
        DistributedNPCSkeleton.announceGenerate(self)
        if not self.isInInvasion():
            self.addBossEffect(AvatarTypes.Undead)

    def disable(self):
        self.removeBossEffect()
        DistributedNPCSkeleton.disable(self)

    def setAvatarType(self, avatarType):
        DistributedNPCSkeleton.setAvatarType(self, avatarType)
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