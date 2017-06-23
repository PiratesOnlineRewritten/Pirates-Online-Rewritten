from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.battle import WeaponGlobals
from pirates.minigame import PotionGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.DialMeter import DialMeter
from pirates.piratesgui.BorderFrame import BorderFrame
buffTable = {WeaponGlobals.C_CORRUPTION: ('buff_curse', PLocalizer.BuffCorruption),WeaponGlobals.C_POISON: ('buff_poison', PLocalizer.BuffPoison),WeaponGlobals.C_ACID: ('buff_acid', PLocalizer.BuffAcid),WeaponGlobals.C_HOLD: ('buff_hold', PLocalizer.BuffHold),WeaponGlobals.C_WOUND: ('buff_wound', PLocalizer.BuffWound),WeaponGlobals.C_ON_FIRE: ('buff_burn', PLocalizer.BuffOnFire),WeaponGlobals.C_FLAMING: ('buff_burn', PLocalizer.BuffOnFire),WeaponGlobals.C_STUN: ('buff_stun', PLocalizer.BuffStun),WeaponGlobals.C_UNSTUN: ('buff_stun', PLocalizer.BuffUnstun),WeaponGlobals.C_SLOW: ('buff_stun', PLocalizer.BuffSlow),WeaponGlobals.C_PAIN: ('buff_stun', PLocalizer.BuffSlow),WeaponGlobals.C_DIRT: ('buff_blind', PLocalizer.BuffBlind),WeaponGlobals.C_BLIND: ('buff_blind', PLocalizer.BuffBlind),WeaponGlobals.C_CURSE: ('buff_curse', PLocalizer.BuffCurse),WeaponGlobals.C_HASTEN: ('buff_hasten', PLocalizer.BuffHasten % int(WeaponGlobals.HASTEN_BONUS * 100)),WeaponGlobals.C_TAUNT: ('buff_taunt', PLocalizer.BuffTaunt),WeaponGlobals.C_WEAKEN: ('buff_weaken', PLocalizer.BuffWeaken),WeaponGlobals.C_REGEN: ('buff_stun', PLocalizer.BuffRegen),WeaponGlobals.C_SPAWN: ('buff_blind', PLocalizer.BuffSpawn),WeaponGlobals.C_VOODOO_STUN_LOCK: ('buff_stun', PLocalizer.BuffVoodooStunLock),WeaponGlobals.C_UNKNOWN_EFFECT: ('buff_weaken', PLocalizer.BuffUnknownEffect),WeaponGlobals.C_REP_BONUS_LVL1: ('buff_repBoost', PLocalizer.BuffReputation % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_REP_BONUS_LVL1) * 100)),WeaponGlobals.C_REP_BONUS_LVL2: ('buff_repBoost', PLocalizer.BuffReputation % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_REP_BONUS_LVL2) * 100)),WeaponGlobals.C_REP_BONUS_LVL3: ('buff_repBoost', PLocalizer.BuffReputation % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_REP_BONUS_LVL3) * 100)),WeaponGlobals.C_GOLD_BONUS_LVL1: ('buff_goldBoost', PLocalizer.BuffGold % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_GOLD_BONUS_LVL1) * 100)),WeaponGlobals.C_GOLD_BONUS_LVL2: ('buff_goldBoost', PLocalizer.BuffGold % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_GOLD_BONUS_LVL2) * 100)),WeaponGlobals.C_CANNON_DAMAGE_LVL1: ('buff_cannonDmgUp', PLocalizer.BuffCannonDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_CANNON_DAMAGE_LVL1) * 100)),WeaponGlobals.C_CANNON_DAMAGE_LVL2: ('buff_cannonDmgUp', PLocalizer.BuffCannonDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_CANNON_DAMAGE_LVL2) * 100)),WeaponGlobals.C_CANNON_DAMAGE_LVL3: ('buff_cannonDmgUp', PLocalizer.BuffCannonDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_CANNON_DAMAGE_LVL3) * 100)),WeaponGlobals.C_PISTOL_DAMAGE_LVL1: ('buff_gunDmgUp', PLocalizer.BuffPistolDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_PISTOL_DAMAGE_LVL1) * 100)),WeaponGlobals.C_PISTOL_DAMAGE_LVL2: ('buff_gunDmgUp', PLocalizer.BuffPistolDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_PISTOL_DAMAGE_LVL2) * 100)),WeaponGlobals.C_PISTOL_DAMAGE_LVL3: ('buff_gunDmgUp', PLocalizer.BuffPistolDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_PISTOL_DAMAGE_LVL3) * 100)),WeaponGlobals.C_CUTLASS_DAMAGE_LVL1: ('buff_swordDmgUp', PLocalizer.BuffCutlassDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_CUTLASS_DAMAGE_LVL1) * 100)),WeaponGlobals.C_CUTLASS_DAMAGE_LVL2: ('buff_swordDmgUp', PLocalizer.BuffCutlassDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_CUTLASS_DAMAGE_LVL2) * 100)),WeaponGlobals.C_CUTLASS_DAMAGE_LVL3: ('buff_swordDmgUp', PLocalizer.BuffCutlassDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_CUTLASS_DAMAGE_LVL3) * 100)),WeaponGlobals.C_DOLL_DAMAGE_LVL1: ('buff_voodooDmgUp', PLocalizer.BuffDollDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_DOLL_DAMAGE_LVL1) * 100)),WeaponGlobals.C_DOLL_DAMAGE_LVL2: ('buff_voodooDmgUp', PLocalizer.BuffDollDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_DOLL_DAMAGE_LVL2) * 100)),WeaponGlobals.C_DOLL_DAMAGE_LVL3: ('buff_voodooDmgUp', PLocalizer.BuffDollDamage % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_DOLL_DAMAGE_LVL3) * 100)),WeaponGlobals.C_BURP: ('buff_burp', PLocalizer.BuffBurp),WeaponGlobals.C_FART: ('buff_fart', PLocalizer.BuffFart),WeaponGlobals.C_FART_LVL2: ('buff_fart', PLocalizer.BuffFartLvl2),WeaponGlobals.C_VOMIT: ('buff_puke', PLocalizer.BuffVomit),WeaponGlobals.C_HASTEN_LVL1: ('buff_hasten', PLocalizer.BuffHasten % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_HASTEN_LVL1) * 100)),WeaponGlobals.C_HASTEN_LVL2: ('buff_hasten', PLocalizer.BuffHasten % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_HASTEN_LVL2) * 100)),WeaponGlobals.C_HASTEN_LVL3: ('buff_hasten', PLocalizer.BuffHasten % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_HASTEN_LVL3) * 100)),WeaponGlobals.C_ACCURACY_BONUS_LVL1: ('buff_accuracy', PLocalizer.BuffAccuracy % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_ACCURACY_BONUS_LVL1) * 100)),WeaponGlobals.C_ACCURACY_BONUS_LVL2: ('buff_accuracy', PLocalizer.BuffAccuracy % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_ACCURACY_BONUS_LVL2) * 100)),WeaponGlobals.C_ACCURACY_BONUS_LVL3: ('buff_accuracy', PLocalizer.BuffAccuracy % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_ACCURACY_BONUS_LVL3) * 100)),WeaponGlobals.C_REGEN_LVL1: ('buff_healthRegeneration', PLocalizer.BuffPotionRegen % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_REGEN_LVL1) * 100)),WeaponGlobals.C_REGEN_LVL2: ('buff_healthRegeneration', PLocalizer.BuffPotionRegen % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_REGEN_LVL2) * 100)),WeaponGlobals.C_REGEN_LVL3: ('buff_healthRegeneration', PLocalizer.BuffPotionRegen % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_REGEN_LVL3) * 100)),WeaponGlobals.C_REGEN_LVL4: ('buff_healthRegeneration', PLocalizer.BuffPotionRegen % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_REGEN_LVL4) * 100)),WeaponGlobals.C_HEAD_GROW: ('buff_headIncrease', PLocalizer.BuffHeadGrow),WeaponGlobals.C_CRAZY_SKIN_COLOR: ('buff_crazyColor', PLocalizer.BuffCrazySkinColor),WeaponGlobals.C_SIZE_REDUCE: ('buff_avatarDecrease', PLocalizer.BuffSizeReduce),WeaponGlobals.C_SIZE_INCREASE: ('buff_avatarIncrease', PLocalizer.BuffSizeIncrease),WeaponGlobals.C_SCORPION_TRANSFORM: ('buff_scorpionTransform', PLocalizer.BuffScorpionTransform),WeaponGlobals.C_ALLIGATOR_TRANSFORM: ('buff_alligatorTransform', PLocalizer.BuffAlligatorTransform),WeaponGlobals.C_CRAB_TRANSFORM: ('buff_crabTransform', PLocalizer.BuffCrabTransform),WeaponGlobals.C_HEAD_FIRE: ('buff_headOnFire', PLocalizer.BuffHeadFire),WeaponGlobals.C_INVISIBILITY_LVL1: ('buff_invisibility', PLocalizer.BuffInvisibility),WeaponGlobals.C_INVISIBILITY_LVL2: ('buff_invisibility', PLocalizer.BuffInvisibility),WeaponGlobals.C_ATTUNE: ('buff_attune', PLocalizer.BuffAttune),WeaponGlobals.C_KNOCKDOWN: ('buff_stun', PLocalizer.BuffKnockdown),WeaponGlobals.C_DARK_CURSE: ('buff_curse', PLocalizer.BuffDarkCurse),WeaponGlobals.C_GHOST_FORM: ('buff_blind', PLocalizer.BuffGhostForm),WeaponGlobals.C_MASTERS_RIPOSTE: ('buff_hasten', PLocalizer.BuffMastersRiposte),WeaponGlobals.C_NOT_IN_FACE: ('buff_taunt', PLocalizer.BuffNotInFace),WeaponGlobals.C_MONKEY_PANIC: ('buff_taunt', PLocalizer.BuffMonkeyPanic),WeaponGlobals.C_QUICKLOAD: ('buff_burn', PLocalizer.BuffQuickload),WeaponGlobals.C_TOXIN: ('buff_poison', PLocalizer.BuffToxin),WeaponGlobals.C_ON_CURSED_FIRE: ('buff_burn', PLocalizer.BuffOnFire),WeaponGlobals.C_VOODOO_REFLECT: ('buff_attune', PLocalizer.BuffVoodooReflect),WeaponGlobals.C_FURY: ('buff_attune', PLocalizer.BuffFury),WeaponGlobals.C_MELEE_SHIELD: ('buff_attune', PLocalizer.BuffMeleeShield),WeaponGlobals.C_MISSILE_SHIELD: ('buff_attune', PLocalizer.BuffMissileShield),WeaponGlobals.C_MAGIC_SHIELD: ('buff_attune', PLocalizer.BuffMagicShield),WeaponGlobals.C_WARDING: ('buff_invisibility', PLocalizer.BuffWarding),WeaponGlobals.C_NATURE: ('buff_healthRengeration', PLocalizer.BuffNature),WeaponGlobals.C_DARK: ('buff_swordDmgUp', PLocalizer.BuffDark),WeaponGlobals.C_FULLSAIL: ('sail_full_sail', PLocalizer.BuffFullSail),WeaponGlobals.C_COMEABOUT: ('sail_come_about', PLocalizer.BuffComeAbout),WeaponGlobals.C_OPENFIRE: ('buff_openfire', PLocalizer.BuffOpenFire),WeaponGlobals.C_RAM: ('sail_ramming_speed', PLocalizer.BuffRam),WeaponGlobals.C_TAKECOVER: ('sail_take_cover', PLocalizer.BuffTakeCover),WeaponGlobals.C_RECHARGE: ('sail_recharge', PLocalizer.BuffPowerRecharge),WeaponGlobals.C_WRECKHULL: ('buff_openfire', PLocalizer.BuffWreckHull),WeaponGlobals.C_WRECKMASTS: ('buff_openfire', PLocalizer.BuffWreckMasts),WeaponGlobals.C_SINKHER: ('buff_openfire', PLocalizer.BuffSinkHer),WeaponGlobals.C_INCOMING: ('buff_openfire', PLocalizer.BuffIncoming),WeaponGlobals.C_FIX_IT_NOW: ('sail_come_about', PLocalizer.BuffFixItNow),WeaponGlobals.C_SUMMON_CHICKEN: ('buff_burp', PLocalizer.BuffSummonChicken),WeaponGlobals.C_SUMMON_MONKEY: ('buff_burp', PLocalizer.BuffSummonMonkey),WeaponGlobals.C_SUMMON_WASP: ('buff_burp', PLocalizer.BuffSummonWasp),WeaponGlobals.C_SUMMON_DOG: ('buff_burp', PLocalizer.BuffSummonDog),WeaponGlobals.C_REP_BONUS_LVLCOMP: ('buff_repBoost', PLocalizer.BuffReputation % int(PotionGlobals.getPotionPotency(WeaponGlobals.C_REP_BONUS_LVLCOMP) * 100))}

class BuffIcon(DirectFrame):
    Background = None
    Card = None

    def __init__(self, parent, effectId, duration, attackerId, **kw):
        optiondefs = (('relief', None, None), )
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent, **kw)
        self.initialiseoptions(BuffIcon)
        if not self.Background:
            self.Background = loader.loadModel('models/gui/lookout_gui').find('**/lookout_submit')
            self.Background.setScale(0.33)
        if not self.Card:
            self.Card = loader.loadModel('models/textureCards/buff_icons')
        self.myIcon = None
        self.detailFrame = None
        self.dial = None
        self.iconScale = 0.07
        self.effectId = effectId
        self.maxDuration = duration
        self.timeLeft = duration
        self.lastTimestamp = None
        self.attackerId = attackerId
        self.setDepthWrite(0)
        self.setFogOff()
        self.setLightOff()
        self.setBin('gui-fixed', 0)
        return

    def makeIcons(self):
        self.Background.copyTo(self)
        self.dial = DialMeter(parent=self, meterColor=Vec4(0.3, 0.0, 0.8, 1), baseColor=Vec4(0, 0, 0, 1), scale=0.17, sortOrder=0)
        if self.effectId in buffTable:
            info = buffTable.get(self.effectId)
        else:
            info = buffTable.get(WeaponGlobals.C_UNKNOWN_EFFECT)
        self.myIcon = DirectButton(parent=self, relief=None, geom=self.Card.find('**/' + info[0]), geom_scale=self.iconScale, sortOrder=1)
        self.myIcon.bind(DGG.ENTER, self.showDetails)
        self.myIcon.bind(DGG.EXIT, self.hideDetails)
        self.updateIconInfo()
        return

    def makeDetails(self):
        if self.detailFrame:
            return
        normalScale = 0.973072
        parent = self.getParent()
        if parent:
            for i in range(0, 2):
                parent = parent.getParent()
                if not parent:
                    break

        if parent:
            parentScale = parent.getScale()[0]
        else:
            parentScale = normalScale
        durationStr = str(int(self.maxDuration))
        if self.effectId in buffTable:
            text = buffTable[self.effectId][1] + PLocalizer.BuffDuration % durationStr
        else:
            text = buffTable[WeaponGlobals.C_UNKNOWN_EFFECT][1] + PLocalizer.BuffDuration % durationStr
        self.detailBox = DirectLabel(state=DGG.DISABLED, relief=None, text=text, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleExtraLarge * normalScale / parentScale, text_fg=(1,
                                                                                                                                                                                                   1,
                                                                                                                                                                                                   1,
                                                                                                                                                                                                   1), text_wordwrap=15, text_shadow=(0,
                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                      1), textMayChange=1)
        height = -(self.detailBox.getHeight() + 0.01)
        width = max(0.25, self.detailBox.getWidth() + 0.04)
        self.detailFrame = BorderFrame(parent=self.myIcon, state=DGG.DISABLED, frameSize=(-0.04, width, height, 0.07), pos=(0.05, 0, -0.05))
        self.detailBox.reparentTo(self.detailFrame)
        self.detailFrame.setBin('gui-popup', 0)
        self.detailFrame.hide()
        return

    def showDetails(self, event):
        self.makeDetails()
        self.detailFrame.show()
        self.updateIconInfo()

    def hideDetails(self, event):
        if self.detailFrame:
            self.detailFrame.hide()

    def updateIconInfo(self):
        if self.lastTimestamp == None:
            timeOffset = 0.0
        else:
            timeOffset = globalClockDelta.localElapsedTime(self.lastTimestamp)
        duration = max(0.0, self.timeLeft - timeOffset)
        self.dial.update(duration, self.maxDuration)
        if self.detailFrame and not self.detailFrame.isHidden():
            if duration > 0:
                durationStr = PLocalizer.BuffDuration % str(int(duration) + 1)
            else:
                durationStr = ''
            if self.effectId in buffTable:
                text = buffTable[self.effectId][1] + durationStr
            else:
                text = buffTable[WeaponGlobals.C_UNKNOWN_EFFECT][1] + durationStr
            self.detailBox['text'] = text
        return

    def destroy(self):
        DirectFrame.destroy(self)