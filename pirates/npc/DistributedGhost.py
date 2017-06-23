from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from pandac.PandaModules import *
from pirates.effects.GhostAura import GhostAura
from pirates.pirate import DistributedPirateBase
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.battle import DistributedBattleNPC
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.leveleditor import NPCList
from pirates.pirate import HumanDNA
from pirates.pirate import AvatarTypes
import Ghost
import random

class DistributedGhost(DistributedBattleNPC.DistributedBattleNPC, Ghost.Ghost):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGhost')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        Ghost.Ghost.__init__(self)
        self.ghostEffect = None
        self.inNotice = 0
        self.selectedGhostColor = 0
        self.enemyColor = 2
        self.attackGhostMode = 2
        self.peaceGhostMode = 1
        return

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
        if self.getTeam() != 0:
            self.selectedGhostColor = self.enemyColor
        if not self.loaded:
            if self.style:
                Ghost.Ghost.generateHuman(self, self.style.gender, base.cr.human)
            self.setGhostColor(self.selectedGhostColor)
            self.checkState()
        self.getMinimapObject()
        yieldThread('ghost done')

    def setTeam(self, team):
        DistributedBattleNPC.DistributedBattleNPC.setTeam(self, team)
        if team == 0:
            self.selectedGhostColor = 0
        else:
            self.selectedGhostColor = self.enemyColor
        if self.isGenerated():
            if self.isGhost:
                ghostHold = self.isGhost
                self.setIsGhost(0)
                self.setGhostColor(self.selectedGhostColor)
                self.setIsGhost(ghostHold)

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        self.setInteractOptions(isTarget=False, allowInteract=False)

    def disable(self):
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        self.stopBlink()

    def delete(self):
        DistributedBattleNPC.DistributedBattleNPC.delete(self)
        Ghost.Ghost.delete(self)

    def getNameText(self):
        return Ghost.Ghost.getNameText(self)

    def isBattleable(self):
        return 1

    def setDNAId(self, dnaId):
        if dnaId and NPCList.NPC_LIST.has_key(dnaId):
            dnaDict = NPCList.NPC_LIST[dnaId]
            customDNA = HumanDNA.HumanDNA()
            customDNA.loadFromNPCDict(dnaDict)
            self.setDNAString(customDNA)
            self.setGhostColor(self.selectedGhostColor)
            self.checkState()
        else:
            self.setDNAString(None)
            self.setDefaultDNA()
            gender = random.choice(['m', 'f'])
            self.style.makeNPCGhost(seed=None, gender=gender)
            self.setGhostColor(self.selectedGhostColor)
            self.checkState()
        return

    def play(self, *args, **kwArgs):
        Ghost.Ghost.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        Ghost.Ghost.loop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        Ghost.Ghost.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        Ghost.Ghost.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        Ghost.Ghost.stop(self, *args, **kwArgs)

    def shouldNotice(self):
        if self.animSet == 'default':
            return 1
        else:
            return 0

    def startNoticeLoop(self):
        pass

    def endNoticeLoop(self):
        pass

    def startShuffle(self, turnAnim):
        if self.playNoticeAnims():
            self.loop(turnAnim, partName='legs', blendDelay=0.15)

    def midShuffle(self):
        if self.playNoticeAnims():
            self.loop('idle', blendDelay=0.3)

    def playNoticeAnim(self):
        if not self.doneThreat:
            self.doneThreat = 1
            if self.preselectedReaction:
                reaction = self.preselectedReaction
                self.preselectedReaction = None
            else:
                reaction = self.getNoticeAnimation()
            if reaction:
                self.play(reaction, blendInT=0.3, blendOutT=0.3)
        return

    def presetNoticeAnimation(self):
        self.preselectedReaction = self.getNoticeAnimation()
        return self.getDuration(self.preselectedReaction)

    def getNoticeAnimation(self):
        reaction = None
        if self.getLevel() - 10 >= localAvatar.getLevel():
            reaction = random.choice(['emote_laugh', 'emote_anger'])
        elif self.getLevel() + 4 >= localAvatar.getLevel():
            reaction = random.choice(['emote_laugh', 'emote_anger'])
        else:
            reaction = random.choice(['emote_laugh', 'emote_anger'])
        return reaction

    def doNoticeFX(self):
        if self.isGhost == 1:
            self.setIsGhost(self.attackGhostMode)
            self.inNotice = 1

    def battleFX(self, entering):
        if entering:
            self.setIsGhost(self.attackGhostMode)
        else:
            self.setIsGhost(self.peaceGhostMode)

    def abortNotice(self):
        DistributedBattleNPC.DistributedBattleNPC.abortNotice(self)
        if self.inNotice:
            self.checkState()
            self.inNotice = 0

    def endNotice(self):
        DistributedBattleNPC.DistributedBattleNPC.endNotice(self)
        if self.inNotice:
            self.checkState()
            self.inNotice = 0

    def checkState(self):
        if self.getGameState() == 'Battle':
            self.setIsGhost(self.attackGhostMode)
        else:
            self.setIsGhost(self.peaceGhostMode)

    def getDeathTrack(self):
        if self.hp > 0:
            self.nametag3d.hide()
            self.setIsGhost(4)
            return Sequence(Wait(3.0))
        return DistributedBattleNPC.DistributedBattleNPC.getDeathTrack(self)

    def getMinimapObject(self):
        mmObj = DistributedBattleNPC.DistributedBattleNPC.getMinimapObject(self)
        if mmObj:
            if self.getTeam() == PiratesGlobals.PLAYER_TEAM:
                color = VBase4(0.1, 1.0, 0.1, 0.7)
                mmObj.setIconColor(color=color)
            else:
                mmObj.setIconColor()
        return mmObj