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
from pirates.pirate import Human
import random
from pirates.inventory import ItemGlobals
from pirates.pirate import AvatarTypes
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.effects.Drown import Drown
from pirates.battle import EnemyGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class DistributedBountyHunter(DistributedBattleNPC.DistributedBattleNPC, Human.Human):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBountyHunter')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        Human.Human.__init__(self)
        self.inNotice = 0
        self.antiEffect = None
        self.antiIval = None
        self.sfxList = []
        return

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
        if not self.loaded:
            if self.uniqueId:
                self.setDNAId(self.uniqueId)
            if self.style:
                Human.Human.generateHuman(self, self.style.gender, base.cr.human)
            self.checkState()
        self.getMinimapObject()

    def setTeam(self, team):
        DistributedBattleNPC.DistributedBattleNPC.setTeam(self, team)

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        self.setInteractOptions(isTarget=False, allowInteract=False)

    def disable(self):
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        self.stopBlink()
        if self.antiIval:
            self.antiIval.finish()
            self.antiIval = None
        return

    def delete(self):
        self.sfxList = []
        DistributedBattleNPC.DistributedBattleNPC.delete(self)
        Human.Human.delete(self)

    def getNameText(self):
        return Human.Human.getNameText(self)

    def isBattleable(self):
        return 1

    def setUniqueId(self, uniqueId):
        if uniqueId:
            self.setDNAId(uniqueId)
            self.loaded = 0

    def setDNAId(self, dnaId):
        if dnaId and NPCList.NPC_LIST.has_key(dnaId):
            dnaDict = NPCList.NPC_LIST[dnaId]
            customDNA = HumanDNA.HumanDNA()
            customDNA.loadFromNPCDict(dnaDict)
            self.setDNAString(customDNA)
            self.checkState()
        else:
            self.setDNAString(None)
            self.setDefaultDNA()
            gender = random.choice(['m', 'm', 'f'])
            self.style.makeNPCBountyHunter(seed=None, gender=gender)
            self.checkState()
        return

    def play(self, *args, **kwArgs):
        Human.Human.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        Human.Human.loop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        Human.Human.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        Human.Human.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        Human.Human.stop(self, *args, **kwArgs)

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
        pass

    def getDeathTrack(self):
        if self.hp > 0:
            self.nametag3d.hide()
            return Sequence(Wait(3.0))
        return DistributedBattleNPC.DistributedBattleNPC.getDeathTrack(self)

    def doAntiEffect(self):
        if self.antiIval and self.antiIval.isPlaying():
            return
        antiEffect = Drown.getEffect()
        if antiEffect:
            effectScale = EnemyGlobals.getEffectScale(self)
            antiEffect.reparentTo(self)
            antiEffect.setScale(effectScale)
            antiEffect.play()

    def getMinimapObject(self):
        mmObj = DistributedBattleNPC.DistributedBattleNPC.getMinimapObject(self)
        if mmObj:
            if self.getTeam() == PiratesGlobals.PLAYER_TEAM:
                color = VBase4(0.1, 1.0, 0.1, 0.7)
                mmObj.setIconColor(color=color)
            else:
                mmObj.setIconColor()
        return mmObj