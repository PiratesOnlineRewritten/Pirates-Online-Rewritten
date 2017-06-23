from pandac.PandaModules import Vec4
from direct.directnotify import DirectNotifyGlobal
from pirates.npc.DistributedGhost import DistributedGhost
from pirates.pirate import AvatarTypes
from pirates.npc.Boss import Boss
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class DistributedBossGhost(DistributedGhost, Boss):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossGhost')

    def __init__(self, cr):
        DistributedGhost.__init__(self, cr)
        Boss.__init__(self, cr)
        self.enemyColor = 13
        self.attackGhostMode = 2
        self.peaceGhostMode = 2
        self.runawaySound = None
        self.killSound = None
        self.damageSound = None
        self.recentlyPlayedDamage = False
        return

    def announceGenerate(self):
        DistributedGhost.announceGenerate(self)
        self.addBossEffect(AvatarTypes.Navy)
        self.runawaySound = loadSfx(SoundGlobals.SFX_MONSTER_EP_RUNAWAY)
        self.killSound = loadSfx(SoundGlobals.SFX_MONSTER_EP_LAUGHTER)
        self.damageSound = loadSfx(SoundGlobals.SFX_MONSTER_EP_SHORT_LAUGH)

    def disable(self):
        self.removeBossEffect()
        taskMgr.remove(self.uniqueName('restoreDamageSounds'))
        if self.runawaySound:
            self.runawaySound.stop()
            loader.unloadSfx(self.runawaySound)
            self.runawaySound = None
        if self.killSound:
            self.killSound.stop()
            loader.unloadSfx(self.killSound)
            self.killSound = None
        if self.damageSound:
            self.damageSound.stop()
            loader.unloadSfx(self.damageSound)
            self.damageSound = None
        DistributedGhost.disable(self)
        return

    def setAvatarType(self, avatarType):
        DistributedGhost.setAvatarType(self, avatarType)
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

    def sendGhostKillTaunt(self):
        if self.killSound:
            base.playSfx(self.killSound, node=self)

    def sendGhostRunawayTaunt(self):
        if self.runawaySound:
            base.playSfx(self.runawaySound, node=self)

    def playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, itemEffects=[], multihit=0, targetBonus=0, skillResult=0):
        if self.damageSound and not self.recentlyPlayedDamage:
            self.recentlyPlayedDamage = True
            base.playSfx(self.damageSound, node=self, cutoff=60)
            taskMgr.doMethodLater(15.0, self.restoreDamageSounds, self.uniqueName('restoreDamageSounds'))
        DistributedGhost.playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, itemEffects=itemEffects, multihit=multihit, targetBonus=targetBonus)

    def restoreDamageSounds(self, task):
        self.recentlyPlayedDamage = False