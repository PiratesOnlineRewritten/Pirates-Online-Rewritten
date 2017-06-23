import random
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import Vec4
from pirates.battle import WeaponGlobals
from pirates.minigame import PotionGlobals
from pirates.effects.VomitEffect import VomitEffect
from pirates.effects.FartEffect import FartEffect
from pirates.effects.BurpEffect import BurpEffect
from pirates.effects.BlueFlame import BlueFlame
from pirates.effects.HealSparks import HealSparks
from pirates.effects.HealRays import HealRays
from pirates.battle.EnemySkills import EnemySkills
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from direct.showbase.DirectObject import DirectObject
from direct.distributed.ClockDelta import *

class PotionStatusEffectManager():
    notify = DirectNotifyGlobal.directNotify.newCategory('PotionStatusEffectManager')
    vomitSounds = None
    burpSounds = None
    fartSounds = None
    sparkleSound = None
    debuffSound = None

    def __init__(self, avatar):
        self.avatar = avatar
        self._vomitEffectLoop = None
        self._vomitEffectParallel = None
        self._vomitEffect = None
        self._vomitSoundInterval = None
        self._fartEffectLoop = None
        self._fartEffectParallel = None
        self._fartEffect = None
        self._fartSoundInterval = None
        self._burpEffectLoop = None
        self._burpEffectParallel = None
        self._burpEffect = None
        self._burpSoundInterval = None
        self._headFireEffect = None
        self._headFireSeq = None
        self._potionSparks = None
        self._potionRays = None
        self._genericPotionEffectSequence = None
        self._activeGenericPotionId = -1
        self._turnInvisibleSeq = None
        self._headFireSeq = None
        if not self.vomitSounds:
            PotionStatusEffectManager.vomitSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_BARF_1), loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_BARF_2), loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_BARF_3), loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_BARF_4))
            PotionStatusEffectManager.burpSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_BURP_1), loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_BURP_2), loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_BURP_3))
            PotionStatusEffectManager.fartSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_FART_1), loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_FART_2), loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_FART_3), loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_FART_4), loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_FART_5))
            PotionStatusEffectManager.sparkleSound = loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_SPARKLE)
            PotionStatusEffectManager.debuffSound = loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_DEBUFF)
        return

    def disable(self):
        if self._headFireSeq:
            self._headFireSeq.clearToInitial()
            self._headFireSeq = None
        if self._turnInvisibleSeq:
            self._turnInvisibleSeq.clearToInitial()
            self._turnInvisibleSeq = None
        return

    def addStatusEffect(self, effectId, attackerId, duration, timeLeft, timestamp, buffData):
        timeSince = globalClockDelta.localElapsedTime(timestamp) + (duration - timeLeft)
        if effectId == WeaponGlobals.C_VOMIT:
            self._addVomitEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_FART:
            self._addFartEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_FART_LVL2:
            self._addFartEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_BURP:
            self._addBurpEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_HEAD_FIRE:
            if self._headFireSeq:
                self._headFireSeq.clearToInitial()
                self._headFireSeq = None
            self._headFireSeq = self.avatar.getTransformSequence(None, self._addHeadFireEffect, [attackerId, timeLeft], timeSince)
            self._headFireSeq.start()
        elif effectId in [WeaponGlobals.C_INVISIBILITY_LVL1, WeaponGlobals.C_INVISIBILITY_LVL2]:
            if self._turnInvisibleSeq:
                self._turnInvisibleSeq.clearToInitial()
                self._turnInvisibleSeq = None
            self._turnInvisibleSeq = self.avatar.getTransformSequence(None, self.avatar.setIsInvisible, [True], timeSince)
            self._turnInvisibleSeq.start()
        elif effectId in [WeaponGlobals.C_SCORPION_TRANSFORM, WeaponGlobals.C_ALLIGATOR_TRANSFORM, WeaponGlobals.C_CRAB_TRANSFORM]:
            self.avatar.setCreatureTransformation(True, effectId, timeSince)
        elif effectId in [WeaponGlobals.C_SIZE_INCREASE, WeaponGlobals.C_SIZE_REDUCE]:
            self.avatar.playScaleChangeAnimation(buffData[1], timeSince)
        elif effectId == WeaponGlobals.C_CRAZY_SKIN_COLOR:
            self.avatar.setAvatarSkinCrazy(True, buffData[1], timeSince)
        else:
            self._addPotionEffect(effectId, attackerId, duration)
        return

    def removeStatusEffect(self, effectId, attackerId):
        if effectId == WeaponGlobals.C_VOMIT:
            self._removeVomitEffect()
            self._removePotionEffect(effectId)
        elif effectId == WeaponGlobals.C_FART:
            self._removeFartEffect()
            self._removePotionEffect(effectId)
        elif effectId == WeaponGlobals.C_FART_LVL2:
            self._removeFartEffect()
            self._removePotionEffect(effectId)
        elif effectId == WeaponGlobals.C_BURP:
            self._removeBurpEffect()
            self._removePotionEffect(effectId)
        elif effectId == WeaponGlobals.C_HEAD_FIRE:
            if self._headFireSeq:
                self._headFireSeq.clearToInitial()
                self._headFireSeq = None
            self._headFireSeq = self.avatar.getTransformSequence(None, self._removeHeadFireEffect)
            self._headFireSeq.start()
        elif effectId in [WeaponGlobals.C_INVISIBILITY_LVL1, WeaponGlobals.C_INVISIBILITY_LVL2]:
            if self._turnInvisibleSeq:
                self._turnInvisibleSeq.clearToInitial()
                self._turnInvisibleSeq = None
            self._turnInvisibleSeq = self.avatar.getTransformSequence(None, self.avatar.setIsInvisible, [False])
            self._turnInvisibleSeq.start()
        elif effectId in [WeaponGlobals.C_SCORPION_TRANSFORM, WeaponGlobals.C_ALLIGATOR_TRANSFORM, WeaponGlobals.C_CRAB_TRANSFORM]:
            self.avatar.setCreatureTransformation(False, effectId)
        elif effectId in [WeaponGlobals.C_SIZE_INCREASE, WeaponGlobals.C_SIZE_REDUCE]:
            self.avatar.playScaleChangeAnimation(1.0)
        elif effectId == WeaponGlobals.C_CRAZY_SKIN_COLOR:
            self.avatar.setAvatarSkinCrazy(False)
        else:
            self._removePotionEffect(effectId)
        return

    def _addPotionEffect(self, effectId, attackerId, duration):

        def startHealEffects():
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                self._potionSparks = HealSparks.getEffect()
                if self._potionSparks:
                    self._potionSparks.reparentTo(self.avatar)
                    self._potionSparks.setPos(0, 0, 4)
                    self._potionSparks.setHpr(0, 0, 0)
                    self._potionSparks.setScale(1.5, 1.5, 2)
                    self._potionSparks.setEffectColor(Vec4(0.3, 1, 1, 0.3))
                    self._potionSparks.startLoop()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                self._potionRays = HealRays.getEffect()
                if self._potionRays:
                    self._potionRays.reparentTo(self.avatar)
                    self._potionRays.setPos(0, 0, 4)
                    self._potionRays.setHpr(0, 0, 0)
                    self._potionRays.setScale(0.75, 0.75, 2)
                    self._potionRays.setEffectColor(Vec4(0.3, 1, 1, 1))
                    self._potionRays.startLoop()

        def stopHealEffects():
            if self._potionSparks:
                self._potionSparks.stopLoop()
                self._potionSparks = None
            if self._potionRays:
                self._potionRays.stopLoop()
                self._potionSparks = None
            return

        if self._genericPotionEffectSequence != None and self._genericPotionEffectSequence.isPlaying():
            return
        if self._genericPotionEffectSequence:
            self._genericPotionEffectSequence.clearToInitial()
        self._genericPotionEffectSequence = None
        self._activeGenericPotionId = effectId
        self._genericPotionEffectSequence = Sequence(Parallel(Func(startHealEffects), SoundInterval(self.sparkleSound, node=self.avatar, cutOff=100)), Wait(PotionGlobals.GENERIC_EFFECT_DELAY), Func(stopHealEffects))
        self._genericPotionEffectSequence.start()
        return

    def _removePotionEffect(self, effectId):
        if effectId == self._activeGenericPotionId:
            if self._genericPotionEffectSequence != None:
                self._genericPotionEffectSequence.finish()
                self._genericPotionEffectSequence = None
                self._activeGenericPotionId = -1
        SoundInterval(self.debuffSound, node=self.avatar, cutOff=100).start()
        return

    def _playIntervalIfLandRoam(self, interval):
        if self.avatar.gameFSM != None:
            if self.avatar.getGameState() in ['LandRoam', 'Battle']:
                interval.start()
        return

    def _ifInBattlePutAwayWeapon(self):
        if self.avatar.isLocal() and self.avatar.gameFSM.getCurrentOrNextState() == 'Battle':
            self.avatar.guiMgr.combatTray.toggleWeapon(self.avatar.currentWeaponId, localAvatar.currentWeaponSlotId)

    def _startVomitEffect(self):
        avatarScale = self.avatar.getEnemyScale()
        self._vomitEffect = VomitEffect.getEffect()
        if self._vomitEffect:
            self._vomitEffect.reparentTo(self.avatar.headEffects)
            self._vomitEffect.setPos(-0.05, 0.0, -0.25)
            self._vomitEffect.effectScale = avatarScale
            self._vomitEffect.play()

    def _addVomitEffect(self, attackerId, duration):
        if self._vomitEffectLoop is not None:
            return
        self._vomitEffectParallel = Sequence(Func(self._ifInBattlePutAwayWeapon), Wait(0.75), Parallel(Func(self.playVomitSfx), self.avatar.actorInterval('barf', playRate=1.0, blendInT=0.2, blendOutT=0.2), Sequence(Wait(1.0), Func(self._startVomitEffect))))
        self._vomitEffectLoop = Sequence(Func(self._playIntervalIfLandRoam, self._vomitEffectParallel), Wait(PotionGlobals.VOMIT_EFFECT_DELAY - 0.75))
        self._vomitEffectLoop.loop()
        return

    def playVomitSfx(self):
        _vomitSoundInterval = None
        sfx = random.choice(self.vomitSounds)
        _vomitSoundInterval = SoundInterval(sfx, node=self.avatar, cutOff=100)
        _vomitSoundInterval.start()
        return

    def _removeVomitEffect(self):
        if self._vomitEffectLoop is not None:
            self._vomitEffectLoop.finish()
            self._vomitEffectLoop = None
        if self._vomitEffectParallel is not None:
            self._vomitEffectParallel.finish()
            self._vomitEffectParallel = None
        if self._vomitSoundInterval is not None:
            self._vomitSoundInterval.clearToInitial()
            self._vomitSoundInterval = None
        if self._vomitEffect:
            self._vomitEffect.stop()
            self._vomitEffect = None
        return

    def _startFartEffect(self):
        avatarScale = self.avatar.getEnemyScale()
        self._fartEffect = FartEffect.getEffect()
        if self._fartEffect:
            self._fartEffect.reparentTo(self.avatar)
            self._fartEffect.setPos(0.0, -1.0, self.avatar.height / 2)
            self._fartEffect.effectScale = avatarScale
            self._fartEffect.play()

    def _addFartEffect(self, attackerId, duration):
        if self._fartEffectLoop is not None:
            return
        self._fartEffectParallel = Sequence(Func(self._ifInBattlePutAwayWeapon), Wait(0.75), Parallel(Func(self.playFartSfx), self.avatar.actorInterval('fart', playRate=1.0, blendInT=0.2, blendOutT=0.2), Sequence(Wait(0.7), Func(self._startFartEffect))))
        self._fartEffectLoop = Sequence(Func(self._playIntervalIfLandRoam, self._fartEffectParallel), Wait(PotionGlobals.FART_EFFECT_DELAY - 0.75))
        self._fartEffectLoop.loop()
        return

    def playFartSfx(self):
        _fartSoundInterval = None
        sfx = random.choice(self.fartSounds)
        _fartSoundInterval = SoundInterval(sfx, node=self.avatar, cutOff=100)
        _fartSoundInterval.start()
        return

    def _removeFartEffect(self):
        if self._fartEffectLoop is not None:
            self._fartEffectLoop.finish()
            self._fartEffectLoop = None
        if self._fartEffectParallel is not None:
            self._fartEffectParallel.finish()
            self._fartEffectParallel = None
        if self._fartSoundInterval is not None:
            self._fartSoundInterval.clearToInitial()
            self._fartSoundInterval = None
        if self._fartEffect:
            self._fartEffect.stop()
            self._fartEffect = None
        return

    def _startBurpEffect(self):
        avatarScale = self.avatar.getEnemyScale()
        self._burpEffect = BurpEffect.getEffect()
        if self._burpEffect:
            self._burpEffect.reparentTo(self.avatar.headEffects)
            self._burpEffect.setPos(-0.25, 0.0, -0.75)
            self._burpEffect.effectScale = avatarScale
            self._burpEffect.play()

    def _addBurpEffect(self, attackerId, duration):
        if self._burpEffectLoop is not None:
            return
        self._burpEffectParallel = Sequence(Func(self._ifInBattlePutAwayWeapon), Wait(0.75), Parallel(Func(self.playBurpSfx), self.avatar.actorInterval('burp', playRate=1.0, blendInT=0.2, blendOutT=0.2), Sequence(Wait(1.2), Func(self._startBurpEffect))))
        self._burpEffectLoop = Sequence(Func(self._playIntervalIfLandRoam, self._burpEffectParallel), Wait(PotionGlobals.BURP_EFFECT_DELAY - 0.75))
        self._burpEffectLoop.loop()
        return

    def playBurpSfx(self):
        _burpSoundInterval = None
        sfx = random.choice(self.burpSounds)
        _burpSoundInterval = SoundInterval(sfx, node=self.avatar, cutOff=100)
        _burpSoundInterval.start()
        return

    def _removeBurpEffect(self):
        if self._burpEffectLoop is not None:
            self._burpEffectLoop.finish()
            self._burpEffectLoop = None
        if self._burpEffectParallel is not None:
            self._burpEffectParallel.finish()
            self._burpEffectParallel = None
        if self._burpSoundInterval is not None:
            self._burpSoundInterval.clearToInitial()
            self._burpSoundInterval = None
        if self._burpEffect:
            self._burpEffect.stop()
            self._burpEffect = None
        return

    def _addHeadFireEffect(self, attackerId, duration):
        if self._headFireEffect:
            return
        avatarScale = self.avatar.getEnemyScale()
        self._headFireEffect = BlueFlame.getEffect()
        if self._headFireEffect:
            if hasattr(self.avatar, 'headEffects') and self.avatar.headEffects:
                self._headFireEffect.reparentTo(self.avatar.headEffects)
                self._headFireEffect.setPos(self.avatar.headEffects, 0.25, 0, 0.0)
                self._headFireEffect.setHpr(0, 0, 90)
            else:
                self._headFireEffect.reparentTo(self.avatar)
                self._headFireEffect.setPos(0, 0, self.avatar.height * 0.8)
            self._headFireEffect.effectScale = 0.3 * avatarScale
            self._headFireEffect.startLoop()

    def _removeHeadFireEffect(self):
        if self._headFireEffect:
            self._headFireEffect.stopLoop()
            self._headFireEffect = None
        return

    def maintainEffects(self):
        if self._headFireEffect:
            if hasattr(self.avatar, 'headEffects') and self.avatar.headEffects:
                self._headFireEffect.reparentTo(self.avatar.headEffects)
            else:
                self._headFireEffect.reparentTo(self.avatar)
        if self._potionRays:
            self._potionRays.reparentTo(self.avatar)
        if self._potionSparks:
            self._potionSparks.reparentTo(self.avatar)

    def stopTransformAnims(self):
        self._removeHeadFireEffect()
        if self._headFireSeq:
            self._headFireSeq.clearToInitial()
            self._headFireSeq = None
        if self._turnInvisibleSeq:
            self._turnInvisibleSeq.clearToInitial()
            self._turnInvisibleSeq = None
        return