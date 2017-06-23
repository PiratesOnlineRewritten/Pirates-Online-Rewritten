from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.battle import DistributedBattleNPC
from pirates.npc import Skeleton
import random
import NPCSkeletonGameFSM

class DistributedNPCSkeleton(DistributedBattleNPC.DistributedBattleNPC, Skeleton.Skeleton):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCSkeleton')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        Skeleton.Skeleton.__init__(self)

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        self.setInteractOptions(isTarget=False, allowInteract=False)

    def disable(self):
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        Skeleton.Skeleton.disable(self)

    def delete(self):
        DistributedBattleNPC.DistributedBattleNPC.delete(self)
        Skeleton.Skeleton.delete(self)

    def getNameText(self):
        return Skeleton.Skeleton.getNameText(self)

    def setAvatarType(self, avatarType):
        Skeleton.Skeleton.setAvatarType(self, avatarType)
        DistributedBattleNPC.DistributedBattleNPC.setAvatarType(self, avatarType)

    def createGameFSM(self):
        self.gameFSM = NPCSkeletonGameFSM.NPCSkeletonGameFSM(self)

    def initializeDropShadow(self):
        Skeleton.Skeleton.initializeDropShadow(self)

    def setSpeed(self, forwardSpeed, rotateSpeed):
        if self.gameFSM.state == 'Jump':
            return
        Skeleton.Skeleton.setSpeed(self, forwardSpeed, rotateSpeed)

    def setHp(self, hitPoints, quietly=0):
        DistributedBattleNPC.DistributedBattleNPC.setHp(self, hitPoints, quietly)
        if self.glow:
            self.glow.adjustHeartColor(float(self.hp) / float(self.maxHp))

    def play(self, *args, **kwArgs):
        Skeleton.Skeleton.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        Skeleton.Skeleton.loop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        Skeleton.Skeleton.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        Skeleton.Skeleton.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        Skeleton.Skeleton.stop(self, *args, **kwArgs)

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
            self.loop(turnAnim, blendDelay=0.15)

    def getTurnAnim(self, noticeDif):
        if self.avatarType.getTrack() in [0]:
            return 'crazy_idle'
        else:
            return DistributedBattleNPC.DistributedBattleNPC.getTurnAnim(self, noticeDif)

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
            reaction = random.choice(['emote_flex', 'emote_clap'])
        elif self.getLevel() + 4 >= localAvatar.getLevel():
            reaction = random.choice(['emote_laugh', 'cutlass_taunt'])
        else:
            reaction = random.choice(['emote_fear', 'emote_anger'])
        return reaction