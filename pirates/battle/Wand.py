import random
import Weapon
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.effects.RayGlow import RayGlow
from pirates.inventory import ItemGlobals
from pirates.effects.VoodooGroundAura import VoodooGroundAura
from pirates.effects.VoodooAuraDiscBase import VoodooAuraDiscBase
from pirates.effects.VoodooAuraDisc import VoodooAuraDisc
from pirates.effects.VoodooAuraDisc2 import VoodooAuraDisc2
from pirates.effects.VoodooAuraHeal import VoodooAuraHeal
from pirates.effects.VoodooSmokeAura import VoodooSmokeAura
from pirates.effects.VoodooShieldAura import VoodooShieldAura
from pirates.effects.VoodooAuraBurst import VoodooAuraBurst
from pirates.effects.VoodooSmokeBlast import VoodooSmokeBlast
from pirates.effects.VoodooShieldBlast import VoodooShieldBlast
from pirates.effects.VoodooHealBlast import VoodooHealBlast
from pirates.effects.FlashEffect import FlashEffect

class Wand(Weapon.Weapon):
    modelTypes = [
     'models/handheld/pir_m_hnd_stf_dark_a', 'models/handheld/pir_m_hnd_stf_dark_b', 'models/handheld/pir_m_hnd_stf_dark_c', 'models/handheld/pir_m_hnd_stf_dark_d', 'models/handheld/pir_m_hnd_stf_nature_a', 'models/handheld/pir_m_hnd_stf_nature_b', 'models/handheld/pir_m_hnd_stf_nature_c', 'models/handheld/pir_m_hnd_stf_nature_d', 'models/handheld/pir_m_hnd_stf_ward_a', 'models/handheld/pir_m_hnd_stf_ward_b', 'models/handheld/pir_m_hnd_stf_ward_c', 'models/handheld/pir_m_hnd_stf_ward_d']
    effectTypeInfo = {ItemGlobals.GemGlowPurple: Vec4(0.5, 0.2, 1, 1),ItemGlobals.GemGlowGreen: Vec4(0, 1, 0, 1),ItemGlobals.GemGlowRed: Vec4(1, 0, 0, 1),ItemGlobals.GemGlowBlue: Vec4(0, 0, 1, 1),ItemGlobals.GemGlowMagenta: Vec4(0, 1, 1, 1),ItemGlobals.GemGlowOrange: Vec4(1, 0.6, 0, 1)}
    runAnim = 'run_with_weapon'
    neutralAnim = 'wand_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'wand_hurt'

    def getEffectColor(self, itemId=None):
        if not itemId:
            itemId = self.itemId
        effectId = ItemGlobals.getVfxType1(itemId)
        color = self.effectTypeInfo.get(effectId)
        return color

    def getOffset(self, itemId=None):
        if not itemId:
            itemId = self.itemId
        offset = ItemGlobals.getVfxOffset(itemId)
        return offset

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'wand')
        self.effect = None
        self.effect2 = None
        self.glowEffect = None
        self.effectActor = None
        self.chargeSound = None
        self.chargeLoopSound = None
        self.chargeSoundSequence = None
        self.gem = None
        self.fadePulse = None
        self.auraEffects = []
        return

    def delete(self):
        if self.chargeSoundSequence:
            self.chargeSoundSequence.finish()
            self.chargeSoundSequence = None
        if self.chargeSound:
            self.chargeSound.stop()
            self.chargeSound = None
        if self.chargeLoopSound:
            self.chargeLoopSound.stop()
            self.chargeLoopSound = None
        self.stopChargeEffect()
        self.stopAuraEffects()
        Weapon.Weapon.delete(self)
        return

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(Func(base.playSfx, self.drawSfx, node=av, cutoff=60), av.actorInterval('voodoo_draw', playRate=1.5, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        if av.curAttackAnim:
            av.curAttackAnim.pause()
            av.curAttackAnim = None
        if av.secondWeapon:
            av.secondWeapon.removeNode()
            av.secondWeapon = None
        track = Parallel(Func(base.playSfx, self.returnSfx, node=av, cutoff=60), av.actorInterval('sword_putaway', playRate=2, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.detachFrom, av)))
        if base.cr.targetMgr:
            track.append(Func(base.cr.targetMgr.setWantAimAssist, 0))
        return track

    def startChargeEffect(self):
        self.gem = self.prop.find('**/gem')
        self.gem2 = self.getModel(self.itemId).find('**/gem')
        if self.gem and not self.gem.isEmpty():
            self.gem2.reparentTo(self.gem)
            color = self.getEffectColor(self.itemId)
            offset = self.getOffset(self.itemId)
            self.gem.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOne, ColorBlendAttrib.OIncomingAlpha))
            fadeIn = LerpColorScaleInterval(self.gem, 0.5, color / 1.3, startColorScale=color)
            fadeOut = LerpColorScaleInterval(self.gem, 0.5, color, startColorScale=color / 1.3)
            self.fadePulse = Sequence(fadeIn, fadeOut)
            self.fadePulse.loop()
            self.glowEffect = RayGlow.getEffect()
            if self.glowEffect:
                self.glowEffect.reparentTo(self.gem)
                self.glowEffect.setPos(offset)
                self.glowEffect.effectScale = 0.3
                self.glowEffect.setEffectColor(Vec4(color))
                self.glowEffect.startLoop()

    def stopChargeEffect(self):
        if self.fadePulse:
            self.fadePulse.finish()
            self.fadePulse = None
        if self.glowEffect:
            self.glowEffect.stopLoop()
            self.glowEffect = None
        if self.gem and not self.gem.isEmpty():
            self.gem.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))
            self.gem.clearColorScale()
        return

    def stopAuraEffects(self):
        for effect in self.auraEffects:
            effect.stopLoop()

        self.auraEffects = []

    def getWardingAura(self, av):
        unlimited = av.isLocal()
        animSeq = Sequence(Wait(0.5))
        e1 = VoodooGroundAura.getEffect(unlimited)
        if e1:
            e1.setEffectColor(Vec4(0.4, 0.6, 1, 0.4))
            e1.reparentTo(av)
            animSeq.append(Func(e1.startLoop))
            self.auraEffects.append(e1)
        e2 = VoodooAuraDiscBase.getEffect(unlimited)
        if e2:
            e2.setEffectColor(Vec4(0, 0, 0, 0.3))
            e2.reparentTo(av)
            animSeq.append(Func(e2.startLoop))
            self.auraEffects.append(e2)
        e3 = VoodooAuraDisc.getEffect(unlimited)
        if e3:
            e3.setEffectColor(Vec4(0.4, 0.6, 1, 0.25))
            e3.reparentTo(av)
            animSeq.append(Func(e3.startLoop))
            self.auraEffects.append(e3)
        e4 = VoodooShieldAura.getEffect(unlimited)
        if e4:
            e4.reparentTo(av)
            e4.setPos(0, 0, 2)
            animSeq.append(Func(e4.startLoop))
            self.auraEffects.append(e4)
        return animSeq

    def getStartWardingAura(self, av):
        unlimited = av.isLocal()
        flashEffect = FlashEffect()
        flashEffect.reparentTo(av)
        flashEffect.setPos(0, 0, 2.0)
        flashEffect.setScale(15.0)
        flashEffect.fadeTime = 1.0
        flashEffect.setEffectColor(Vec4(0.4, 0.6, 1, 1))
        animSeq = Sequence(Wait(0.5))
        animSeq.append(Func(flashEffect.play))
        shieldBlast = VoodooShieldBlast.getEffect(unlimited)
        if shieldBlast:
            shieldBlast.reparentTo(av)
            shieldBlast.setPos(0, 0, 1.5)
            animSeq.append(Func(shieldBlast.play))
            animSeq.append(Wait(0.1))
        burstEffect = VoodooAuraBurst.getEffect(unlimited)
        if burstEffect:
            burstEffect.reparentTo(av)
            burstEffect.setPos(0, 0, 0.25)
            burstEffect.setEffectColor(Vec4(0.4, 0.6, 1, 0.6))
            animSeq.append(Func(burstEffect.play))
        return animSeq

    def getDarkAura(self, av):
        unlimited = av.isLocal()
        animSeq = Sequence(Wait(0.55))
        e1 = VoodooGroundAura.getEffect(unlimited)
        if e1:
            e1.setEffectColor(Vec4(1, 0, 0, 0.5))
            e1.reparentTo(av)
            animSeq.append(Func(e1.startLoop))
            self.auraEffects.append(e1)
        e2 = VoodooAuraDiscBase.getEffect(unlimited)
        if e2:
            e2.setEffectColor(Vec4(0, 0, 0, 0.3))
            e2.reparentTo(av)
            animSeq.append(Func(e2.startLoop))
            self.auraEffects.append(e2)
        e3 = VoodooAuraDisc2.getEffect(unlimited)
        if e3:
            e3.setEffectColor(Vec4(1, 0, 0, 0.15))
            e3.reparentTo(av)
            animSeq.append(Func(e3.startLoop))
            self.auraEffects.append(e3)
        e4 = VoodooSmokeAura.getEffect(unlimited)
        if e4:
            e4.reparentTo(av)
            e4.setPos(0, 0, 0.5)
            animSeq.append(Func(e4.startLoop))
            self.auraEffects.append(e4)
        return animSeq

    def getStartDarkAura(self, av):
        unlimited = av.isLocal()
        flashEffect = FlashEffect()
        flashEffect.reparentTo(av)
        flashEffect.setPos(0, 0, 2.0)
        flashEffect.setScale(15.0)
        flashEffect.fadeTime = 1.0
        flashEffect.setEffectColor(Vec4(1, 0, 0, 1))
        animSeq = Sequence(Wait(0.5))
        animSeq.append(Func(flashEffect.play))
        smokeBlast = VoodooSmokeBlast.getEffect(unlimited)
        if smokeBlast:
            smokeBlast.reparentTo(av)
            smokeBlast.setPos(0, 0, 1.5)
            animSeq.append(Func(smokeBlast.play))
            animSeq.append(Wait(0.1))
        burstEffect = VoodooAuraBurst.getEffect(unlimited)
        if burstEffect:
            burstEffect.reparentTo(av)
            burstEffect.setPos(0, 0, 0.25)
            burstEffect.setEffectColor(Vec4(0.5, 0, 0, 0.5))
            animSeq.append(Func(burstEffect.play))
        return animSeq

    def getNatureAura(self, av):
        unlimited = av.isLocal()
        animSeq = Sequence(Wait(0.55))
        e1 = VoodooGroundAura.getEffect(unlimited)
        if e1:
            e1.setEffectColor(Vec4(0.2, 1, 0.5, 0.35))
            e1.reparentTo(av)
            animSeq.append(Func(e1.startLoop))
            self.auraEffects.append(e1)
        e2 = VoodooAuraDiscBase.getEffect(unlimited)
        if e2:
            e2.setEffectColor(Vec4(0, 0, 0, 0.3))
            e2.reparentTo(av)
            animSeq.append(Func(e2.startLoop))
            self.auraEffects.append(e2)
        e3 = VoodooAuraDisc.getEffect(unlimited)
        if e3:
            e3.setEffectColor(Vec4(0.5, 1.0, 0.5, 0.25))
            e3.reparentTo(av)
            animSeq.append(Func(e3.startLoop))
            self.auraEffects.append(e3)
        e4 = VoodooAuraHeal.getEffect(unlimited)
        if e4:
            e4.setEffectColor(Vec4(0.3, 1, 0.6, 0.35))
            e4.reparentTo(av)
            animSeq.append(Func(e4.startLoop))
            self.auraEffects.append(e4)
        return animSeq

    def getStartNatureAura(self, av):
        unlimited = av.isLocal()
        flashEffect = FlashEffect()
        flashEffect.reparentTo(av)
        flashEffect.setPos(0, 0, 2.0)
        flashEffect.setScale(15.0)
        flashEffect.fadeTime = 1.0
        flashEffect.setEffectColor(Vec4(0.3, 1, 0.5, 1))
        animSeq = Sequence(Wait(0.5))
        animSeq.append(Func(flashEffect.play))
        healBlast = VoodooHealBlast.getEffect(unlimited)
        if healBlast:
            healBlast.reparentTo(av)
            healBlast.setPos(0, 0, 2.5)
            animSeq.append(Func(healBlast.play))
            animSeq.append(Wait(0.1))
        burstEffect = VoodooAuraBurst.getEffect(unlimited)
        if burstEffect:
            burstEffect.reparentTo(av)
            burstEffect.setPos(0, 0, 0.25)
            burstEffect.setEffectColor(Vec4(0.3, 1, 0.5, 0.5))
            animSeq.append(Func(burstEffect.play))
        return animSeq

    @classmethod
    def setupSounds(cls):
        Wand.chargeSfx = loadSfx(SoundGlobals.SFX_WEAPON_STAFF_CHARGE)
        Wand.chargeLoopSfx = loadSfx(SoundGlobals.SFX_WEAPON_STAFF_CHARGE_LOOP)
        Wand.blastFireSfx = loadSfx(SoundGlobals.SFX_SKILL_BLAST_FIRE)
        Wand.blastHitSfx = loadSfx(SoundGlobals.SFX_SKILL_BLAST_HIT)
        Wand.soulflayChargeSfx = loadSfx(SoundGlobals.SFX_SKILL_SOULFLAY_CHARGE)
        Wand.soulflayHoldSfx = loadSfx(SoundGlobals.SFX_SKILL_SOULFLAY_HOLD)
        Wand.soulflayFireSfx = loadSfx(SoundGlobals.SFX_SKILL_SOULFLAY_FIRE)
        Wand.soulflayHitSfx = loadSfx(SoundGlobals.SFX_SKILL_SOULFLAY_HIT)
        Wand.pestilenceChargeSfx = loadSfx(SoundGlobals.SFX_SKILL_PESTILENCE_CHARGE)
        Wand.pestilenceHoldSfx = loadSfx(SoundGlobals.SFX_SKILL_PESTILENCE_HOLD)
        Wand.pestilenceFireSfx = loadSfx(SoundGlobals.SFX_SKILL_PESTILENCE_FIRE)
        Wand.pestilenceHitSfx = loadSfx(SoundGlobals.SFX_SKILL_PESTILENCE_HIT)
        Wand.witherChargeSfx = loadSfx(SoundGlobals.SFX_SKILL_WITHER_CHARGE)
        Wand.witherHoldSfx = loadSfx(SoundGlobals.SFX_SKILL_WITHER_HOLD)
        Wand.witherFireSfx = loadSfx(SoundGlobals.SFX_SKILL_WITHER_FIRE)
        Wand.witherHitSfx = loadSfx(SoundGlobals.SFX_SKILL_WITHER_HIT)
        Wand.hellfireChargeSfx = loadSfx(SoundGlobals.SFX_SKILL_HELLFIRE_CHARGE)
        Wand.hellfireHoldSfx = loadSfx(SoundGlobals.SFX_SKILL_HELLFIRE_HOLD)
        Wand.hellfireFireSfx = loadSfx(SoundGlobals.SFX_SKILL_HELLFIRE_FIRE)
        Wand.hellfireHitSfx = loadSfx(SoundGlobals.SFX_SKILL_HELLFIRE_HIT)
        Wand.banishChargeSfx = loadSfx(SoundGlobals.SFX_SKILL_BANISH_CHARGE)
        Wand.banishHoldSfx = loadSfx(SoundGlobals.SFX_SKILL_BANISH_HOLD)
        Wand.banishFireSfx = loadSfx(SoundGlobals.SFX_SKILL_BANISH_FIRE)
        Wand.banishHitSfx = loadSfx(SoundGlobals.SFX_SKILL_BANISH_HIT)
        Wand.desolationChargeSfx = loadSfx(SoundGlobals.SFX_SKILL_DESOLATION_CHARGE)
        Wand.desolationHoldSfx = loadSfx(SoundGlobals.SFX_SKILL_DESOLATION_HOLD)
        Wand.desolationFireSfx = loadSfx(SoundGlobals.SFX_SKILL_DESOLATION_FIRE)
        Wand.desolationHitSfx = loadSfx(SoundGlobals.SFX_SKILL_DESOLATION_HIT)
        Wand.auraCastSfx = loadSfx(SoundGlobals.SFX_SKILL_AURA_CAST)
        Wand.auraLoopSfx = loadSfx(SoundGlobals.SFX_SKILL_AURA_LOOP)
        Wand.auraOffSfx = loadSfx(SoundGlobals.SFX_SKILL_AURA_OFF)
        Wand.drawSfx = loadSfx(SoundGlobals.SFX_WEAPON_NONBLADE_DRAW)
        Wand.returnSfx = loadSfx(SoundGlobals.SFX_WEAPON_NONBLADE_PUTAWAY)


def getSoulflayChargeSfx():
    return Wand.soulflayChargeSfx


def getPestilenceChargeSfx():
    return Wand.pestilenceChargeSfx


def getWitherChargeSfx():
    return Wand.witherChargeSfx


def getHellfireChargeSfx():
    return Wand.hellfireChargeSfx


def getBanishChargeSfx():
    return Wand.banishChargeSfx


def getDesolationChargeSfx():
    return Wand.desolationChargeSfx


def getSoulflayHoldSfx():
    return Wand.soulflayHoldSfx


def getPestilenceHoldSfx():
    return Wand.pestilenceHoldSfx


def getWitherHoldSfx():
    return Wand.witherHoldSfx


def getHellfireHoldSfx():
    return Wand.hellfireHoldSfx


def getBanishHoldSfx():
    return Wand.banishHoldSfx


def getDesolationHoldSfx():
    return Wand.desolationHoldSfx


def getBlastFireSfx():
    return Wand.blastFireSfx


def getSoulflayFireSfx():
    return Wand.soulflayFireSfx


def getPestilenceFireSfx():
    return Wand.pestilenceFireSfx


def getWitherFireSfx():
    return Wand.witherFireSfx


def getHellfireFireSfx():
    return Wand.hellfireFireSfx


def getBanishFireSfx():
    return Wand.banishFireSfx


def getDesolationFireSfx():
    return Wand.desolationFireSfx


def getBlastHitSfx():
    return Wand.blastHitSfx


def getSoulflayHitSfx():
    return Wand.soulflayHitSfx


def getPestilenceHitSfx():
    return Wand.pestilenceHitSfx


def getWitherHitSfx():
    return Wand.witherHitSfx


def getHellfireHitSfx():
    return Wand.hellfireHitSfx


def getBanishHitSfx():
    return Wand.banishHitSfx


def getDesolationHitSfx():
    return Wand.desolationHitSfx


def getChargeSfx():
    return Wand.chargeSfx


def getChargeLoopSfx():
    return Wand.chargeLoopSfx


def getAuraCastSfx():
    return Wand.auraCastSfx


def getAuraLoopSfx():
    return Wand.auraLoopSfx


def getAuraOffSfx():
    return Wand.auraOffSfx