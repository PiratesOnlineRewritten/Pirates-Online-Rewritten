from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from pirates.pirate import DistributedPirateBase
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.battle import DistributedBattleNPC
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.leveleditor import NPCList
from pirates.pirate import HumanDNA
from pirates.pirate import AvatarTypes
import NavySailor
import random

class DistributedNPCNavySailor(DistributedBattleNPC.DistributedBattleNPC, NavySailor.NavySailor):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCNavySailor')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        NavySailor.NavySailor.__init__(self)

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
        if not self.loaded:
            if self.style:
                NavySailor.NavySailor.generateHuman(self, self.style.gender, base.cr.human)
        yieldThread('navy done')

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        self.setInteractOptions(isTarget=False, allowInteract=False)

    def disable(self):
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        self.stopBlink()

    def delete(self):
        DistributedBattleNPC.DistributedBattleNPC.delete(self)
        NavySailor.NavySailor.delete(self)

    def getNameText(self):
        return NavySailor.NavySailor.getNameText(self)

    def isBattleable(self):
        return 1

    def setDNAId(self, dnaId):
        if dnaId and NPCList.NPC_LIST.has_key(dnaId):
            dnaDict = NPCList.NPC_LIST[dnaId]
            customDNA = HumanDNA.HumanDNA()
            customDNA.loadFromNPCDict(dnaDict)
            self.setDNAString(customDNA)
        else:
            self.setDNAString(None)
            self.setDefaultDNA()
            if self.avatarType.isA(AvatarTypes.TradingCo):
                self.style.makeNPCIndiaNavySailor()
            else:
                self.style.makeNPCNavySailor()
        return

    def play(self, *args, **kwArgs):
        NavySailor.NavySailor.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        NavySailor.NavySailor.loop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        NavySailor.NavySailor.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        NavySailor.NavySailor.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        NavySailor.NavySailor.stop(self, *args, **kwArgs)

    def shouldNotice(self):
        if self.animSet in ['default', 'attention']:
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
            if self.currentWeapon and self.currentWeapon.getName() == 'bayonet':
                self.loop('idle', partName='legs', blendDelay=0.3)
            else:
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
        if self.preselectedReaction:
            return self.getDuration(self.preselectedReaction)
        else:
            return self.noticeSpeed

    def getNoticeAnimation(self):
        reaction = None
        if self.currentWeapon and self.currentWeapon.getName() == 'bayonet':
            if self.getLevel() - 10 >= localAvatar.getLevel():
                reaction = 'bayonet_idle_to_fight_idle'
            elif self.getLevel() + 4 >= localAvatar.getLevel():
                reaction = 'bayonet_idle_to_fight_idle'
            else:
                reaction = 'bayonet_idle_to_fight_idle'
        elif self.getLevel() - 10 >= localAvatar.getLevel():
            reaction = random.choice(['emote_flex', 'emote_laugh'])
        elif self.getLevel() + 4 >= localAvatar.getLevel():
            reaction = random.choice(['emote_anger', 'cutlass_taunt'])
        else:
            reaction = random.choice(['emote_fear', 'emote_no'])
        return reaction