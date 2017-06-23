from pandac.PandaModules import Vec4
from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedVoodooZombie import DistributedVoodooZombie
from pirates.pirate import AvatarTypes
from pirates.npc.Boss import Boss

class DistributedBossVoodooZombie(DistributedVoodooZombie, Boss):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedVoodooZombie')

    def __init__(self, cr):
        DistributedVoodooZombie.__init__(self, cr)
        Boss.__init__(self, cr)

    def generate(self):
        DistributedVoodooZombie.generate(self)

    def announceGenerate(self):
        DistributedVoodooZombie.announceGenerate(self)
        if not self.isInInvasion():
            self.addBossEffect(AvatarTypes.Undead)

    def disable(self):
        self.removeBossEffect()
        DistributedVoodooZombie.disable(self)

    def setAvatarType(self, avatarType):
        DistributedVoodooZombie.setAvatarType(self, avatarType)
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