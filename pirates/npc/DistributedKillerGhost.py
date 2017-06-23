from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from pandac.PandaModules import *
from pirates.effects.GhostAura import GhostAura
from direct.interval.IntervalGlobal import *
from pirates.pirate import DistributedPirateBase
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.battle import DistributedBattleNPC
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.leveleditor import NPCList
from pirates.pirate import HumanDNA
from pirates.pirate import AvatarTypes
from pirates.battle import EnemyGlobals
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.Immolate import Immolate
from pirates.effects.LightningStrike import LightningStrike
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import Ghost
import random

class DistributedKillerGhost(DistributedBattleNPC.DistributedBattleNPC, Ghost.Ghost):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedKillerGhost')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        Ghost.Ghost.__init__(self)
        self.ghostEffect = None
        self.soundLoopIval = None
        self.lastSound = None
        self.inNotice = 0
        self.selectedGhostColor = 4
        self.sfxList = []
        return

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
        if not self.loaded:
            if self.style:
                Ghost.Ghost.generateHuman(self, self.style.gender, base.cr.human)
            self.setGhostColor(self.selectedGhostColor)
            self.checkState()
        yieldThread('ghost done')
        ghostSoundNameList = ('audio/sfx_howl_01.mp3', 'audio/sfx_howl_02.mp3', 'audio/sfx_howl_03.mp3')
        self.ghostSounds = []
        for ghostSoundName in ghostSoundNameList:
            ghostSound = loader.loadSfx(ghostSoundName)
            self.ghostSounds.append(ghostSound)

        self.doGhostSoundLoop()

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        self.setInteractOptions(isTarget=False, allowInteract=False)

    def disable(self):
        if self.ghostEffect:
            self.ghostEffect.stopLoop()
        if self.soundLoopIval:
            self.soundLoopIval.pause()
            self.soundLoopIval = None
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        self.stopBlink()
        return

    def doGhostSoundLoop(self, task=None):
        if self.soundLoopIval:
            self.soundLoopIval.pause()
            self.soundLoopIval = None
        self.soundLoopIval = Sequence()
        sound = random.choice(self.ghostSounds)
        while sound == self.lastSound:
            sound = random.choice(self.ghostSounds)

        self.lastSound = sound
        soundIval = SoundInterval(sound, node=self, volume=1.0, seamlessLoop=False, cutOff=300.0)
        self.soundLoopIval.append(soundIval)
        self.soundLoopIval.append(Func(self.doGhostSoundLoop))
        self.soundLoopIval.start()
        if task:
            return task.done
        return

    def delete(self):
        self.sfxList = []
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

    def isInvisibleGhost(self):
        return 1

    def doNoticeFX(self):
        pass

    def battleFX(self, effect):
        if effect:
            self.setIsGhost(2)
        else:
            self.setIsGhost(3)

    def checkState(self):
        base.kg = self
        if self.getGameState == 'Battle':
            self.setIsGhost(2)
        else:
            self.setIsGhost(3)

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

    def initializeNametag3d(self):
        Ghost.Ghost.initializeNametag3d(self)
        self.nameText.hide()

    def getDeathTrack(self):
        if self.soundLoopIval:
            self.soundLoopIval.pause()
            self.soundLoopIval = None
        av = self
        animName = av.getDeathAnimName()
        duration = av.getDuration(animName)
        frames = av.getNumFrames(animName)
        delay = 0.0

        def startSFX():
            sfx = loadSfx(SoundGlobals.SFX_FX_THUNDERCLAP)
            pitchRate = 0.8 + random.random() * 0.4
            sfx.setPlayRate(pitchRate)
            si = SoundInterval(sfx, node=self, volume=1.0, seamlessLoop=False, cutOff=150.0)
            self.sfxList.append(si)
            si.start()

        def stopSmooth():
            if self.smoothStarted:
                taskName = self.taskName('smooth')
                taskMgr.remove(taskName)
            self.smoothStarted = 0

        def startVFX():
            effectScale = EnemyGlobals.getEffectScale(self)
            offset = Vec3(0.0, 0.0, -5.0)
            root = av
            deathEffect = LightningStrike.getEffect(unlimited=True)
            if deathEffect:
                deathEffect.reparentTo(render)
                deathEffect.setPos(root, offset)
                deathEffect.fadeColor = Vec4(0.5, 1, 0.5, 1)
                deathEffect.setScale(effectScale * 0.4)
                deathEffect.play()

        delay1 = random.random() * 0.5 + 0.5
        delay2 = random.random() * 0.5 + 0.5
        deathIval = Parallel(Func(stopSmooth), Func(self.setTransparency, 1), Sequence(Func(startVFX), Wait(delay1), Func(startVFX), Wait(delay2), Func(startVFX), Wait(delay1), Func(startVFX)), av.actorInterval(animName, blendOutT=0.0), Sequence(Wait(duration / 2.0), LerpColorScaleInterval(av, duration / 2.0, Vec4(1, 1, 1, 0), startColorScale=Vec4(1)), Func(self.hide, 0, PiratesGlobals.INVIS_DEATH), Func(self.clearColorScale), Func(self.clearTransparency)))
        return deathIval

    def getSpawnTrack(self):
        if self.getAnimControl('intro'):
            introIval = self.actorInterval('intro')
        else:
            fadeIn = LerpFunctionInterval(self.setAlphaScale, 2.0, fromData=0.0, toData=1.0)
            introIval = Sequence(Func(self.setTransparency, 1), fadeIn, Func(self.clearTransparency), Func(self.clearColorScale))
            introIval.append(Func(self.ambushIntroDone))
            return introIval