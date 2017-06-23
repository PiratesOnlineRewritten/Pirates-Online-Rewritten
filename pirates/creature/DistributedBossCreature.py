from pandac.PandaModules import Vec4
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.DistributedCreature import DistributedCreature
from pirates.pirate import AvatarTypes
from pirates.npc.Boss import Boss
CreatureTypes = {AvatarTypes.Crab: AvatarTypes.Crab,AvatarTypes.RockCrab: AvatarTypes.Crab,AvatarTypes.StoneCrab: AvatarTypes.Crab,AvatarTypes.GiantCrab: AvatarTypes.Crab,AvatarTypes.CrusherCrab: AvatarTypes.Crab,AvatarTypes.Stump: AvatarTypes.Stump,AvatarTypes.TwistedStump: AvatarTypes.Stump,AvatarTypes.FlyTrap: AvatarTypes.FlyTrap,AvatarTypes.RancidFlyTrap: AvatarTypes.FlyTrap,AvatarTypes.AncientFlyTrap: AvatarTypes.FlyTrap,AvatarTypes.Scorpion: AvatarTypes.Scorpion,AvatarTypes.DireScorpion: AvatarTypes.Scorpion,AvatarTypes.DreadScorpion: AvatarTypes.Scorpion,AvatarTypes.Alligator: AvatarTypes.Alligator,AvatarTypes.BayouGator: AvatarTypes.Alligator,AvatarTypes.BigGator: AvatarTypes.Alligator,AvatarTypes.HugeGator: AvatarTypes.Alligator,AvatarTypes.Bat: AvatarTypes.Bat,AvatarTypes.RabidBat: AvatarTypes.Bat,AvatarTypes.VampireBat: AvatarTypes.Bat,AvatarTypes.FireBat: AvatarTypes.Bat,AvatarTypes.Wasp: AvatarTypes.Wasp,AvatarTypes.KillerWasp: AvatarTypes.Wasp,AvatarTypes.AngryWasp: AvatarTypes.Wasp,AvatarTypes.SoldierWasp: AvatarTypes.Wasp}

class DistributedBossCreature(DistributedCreature, Boss):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossCreature')

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr)
        Boss.__init__(self, cr)

    def setupCreature(self, avatarType):
        self.loadBossData(self.getUniqueId(), avatarType)
        DistributedCreature.setupCreature(self, avatarType)

    def announceGenerate(self):
        DistributedCreature.announceGenerate(self)
        if not self.isInInvasion():
            avType = CreatureTypes[self.avatarType.getNonBossType()]
            self.addBossEffect(avType)

    def disable(self):
        self.removeBossEffect()
        DistributedCreature.disable(self)

    def getEnemyScale(self):
        return Boss.getEnemyScale(self)

    def getBossEffect(self):
        return Boss.getBossEffect(self)

    def getBossHighlightColor(self):
        return Boss.getBossHighlightColor(self)

    def getShortName(self):
        return Boss.getShortName(self)