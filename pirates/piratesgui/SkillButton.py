from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.gui.DirectGui import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui.SkillRing import SkillRing
from pirates.reputation import RepChart
from pirates.battle.EnemySkills import *
from pirates.inventory import ItemGlobals
from pirates.minigame import PotionGlobals
from pirates.minigame import PotionRecipeData
SkillEffectDescriptions = {WeaponGlobals.C_POISON: [PLocalizer.PoisonDesc, PLocalizer.PoisonUpgrade],WeaponGlobals.C_ACID: [PLocalizer.AcidDesc, PLocalizer.AcidUpgrade],WeaponGlobals.C_HOLD: [PLocalizer.HoldDesc, PLocalizer.HoldUpgrade],WeaponGlobals.C_WOUND: [PLocalizer.WoundDesc, PLocalizer.WoundUpgrade],WeaponGlobals.C_ON_FIRE: [PLocalizer.OnFireDesc, PLocalizer.OnFireUpgrade],WeaponGlobals.C_FLAMING: [PLocalizer.OnFireDesc, PLocalizer.OnFireUpgrade],WeaponGlobals.C_STUN: [PLocalizer.StunDesc, PLocalizer.StunUpgrade],WeaponGlobals.C_UNSTUN: [PLocalizer.UnstunDesc, PLocalizer.UnstunUpgrade],WeaponGlobals.C_SLOW: [PLocalizer.SlowDesc, PLocalizer.SlowUpgrade],WeaponGlobals.C_PAIN: [PLocalizer.SlowDesc, PLocalizer.SlowUpgrade],WeaponGlobals.C_BLIND: [PLocalizer.BlindDesc, PLocalizer.BlindUpgrade],WeaponGlobals.C_DIRT: [PLocalizer.BlindDesc, PLocalizer.BlindUpgrade],WeaponGlobals.C_CURSE: [PLocalizer.CurseDesc, PLocalizer.CurseUpgrade],WeaponGlobals.C_HASTEN: [PLocalizer.HastenDesc, PLocalizer.HastenUpgrade],WeaponGlobals.C_TAUNT: [PLocalizer.TauntDesc, PLocalizer.TauntUpgrade],WeaponGlobals.C_WEAKEN: [PLocalizer.WeakenDesc, PLocalizer.WeakenUpgrade],WeaponGlobals.C_SOULTAP: [PLocalizer.SoulTapDesc],WeaponGlobals.C_MANADRAIN: [PLocalizer.ManaDrainDesc],WeaponGlobals.C_LIFEDRAIN: [PLocalizer.LifeDrainDesc],WeaponGlobals.C_UNDEAD_KILLER: [PLocalizer.UndeadKillerDesc],WeaponGlobals.C_MONSTER_KILLER: [PLocalizer.MonsterKillerDesc],WeaponGlobals.C_BUFF_BREAK: [PLocalizer.BuffBreakDesc, PLocalizer.BuffBreakUpgrade],WeaponGlobals.C_REGEN: [PLocalizer.RegenDesc, PLocalizer.RegenUpgrade],WeaponGlobals.C_KNOCKDOWN: [PLocalizer.KnockdownDesc],WeaponGlobals.C_CANNON_DAMAGE_LVL1: PotionRecipeData.PotionRecipeList[10]['desc'],WeaponGlobals.C_CANNON_DAMAGE_LVL2: PotionRecipeData.PotionRecipeList[14]['desc'],WeaponGlobals.C_CANNON_DAMAGE_LVL3: PotionRecipeData.PotionRecipeList[18]['desc'],WeaponGlobals.C_PISTOL_DAMAGE_LVL1: PotionRecipeData.PotionRecipeList[11]['desc'],WeaponGlobals.C_PISTOL_DAMAGE_LVL2: PotionRecipeData.PotionRecipeList[15]['desc'],WeaponGlobals.C_PISTOL_DAMAGE_LVL3: PotionRecipeData.PotionRecipeList[19]['desc'],WeaponGlobals.C_CUTLASS_DAMAGE_LVL1: PotionRecipeData.PotionRecipeList[12]['desc'],WeaponGlobals.C_CUTLASS_DAMAGE_LVL2: PotionRecipeData.PotionRecipeList[16]['desc'],WeaponGlobals.C_CUTLASS_DAMAGE_LVL3: PotionRecipeData.PotionRecipeList[11]['desc'],WeaponGlobals.C_DOLL_DAMAGE_LVL1: PotionRecipeData.PotionRecipeList[13]['desc'],WeaponGlobals.C_DOLL_DAMAGE_LVL2: PotionRecipeData.PotionRecipeList[17]['desc'],WeaponGlobals.C_DOLL_DAMAGE_LVL3: PotionRecipeData.PotionRecipeList[20]['desc'],WeaponGlobals.C_HASTEN_LVL1: PotionRecipeData.PotionRecipeList[21]['desc'],WeaponGlobals.C_HASTEN_LVL2: PotionRecipeData.PotionRecipeList[22]['desc'],WeaponGlobals.C_HASTEN_LVL3: PotionRecipeData.PotionRecipeList[23]['desc'],WeaponGlobals.C_REP_BONUS_LVL1: PotionRecipeData.PotionRecipeList[24]['desc'],WeaponGlobals.C_REP_BONUS_LVL2: PotionRecipeData.PotionRecipeList[25]['desc'],WeaponGlobals.C_REP_BONUS_LVL3: PLocalizer.PotionDescs[InventoryType.RepBonusLvl1].safe_substitute({'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.RepBonusLvl1)) * 100),'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.RepBonusLvl1))) / 3600,'unit': 'hour'}),WeaponGlobals.C_REP_BONUS_LVLCOMP: PLocalizer.PotionDescs[InventoryType.RepBonusLvlComp].safe_substitute({'pot': int(PotionGlobals.getPotionPotency(WeaponGlobals.getSkillEffectFlag(InventoryType.RepBonusLvlComp)) * 100),'dur': int(PotionGlobals.getPotionBuffDuration(WeaponGlobals.getSkillEffectFlag(InventoryType.RepBonusLvlComp))) / 3600,'unit': 'hour'}),WeaponGlobals.C_GOLD_BONUS_LVL1: PotionRecipeData.PotionRecipeList[26]['desc'],WeaponGlobals.C_GOLD_BONUS_LVL2: PotionRecipeData.PotionRecipeList[27]['desc'],WeaponGlobals.C_INVISIBILITY_LVL1: PotionRecipeData.PotionRecipeList[28]['desc'],WeaponGlobals.C_INVISIBILITY_LVL2: PotionRecipeData.PotionRecipeList[29]['desc'],WeaponGlobals.C_REGEN_LVL1: PotionRecipeData.PotionRecipeList[35]['desc'],WeaponGlobals.C_REGEN_LVL2: PotionRecipeData.PotionRecipeList[36]['desc'],WeaponGlobals.C_REGEN_LVL3: PotionRecipeData.PotionRecipeList[37]['desc'],WeaponGlobals.C_REGEN_LVL4: PotionRecipeData.PotionRecipeList[38]['desc'],WeaponGlobals.C_BURP: PotionRecipeData.PotionRecipeList[0]['desc'],WeaponGlobals.C_FART: PotionRecipeData.PotionRecipeList[1]['desc'],WeaponGlobals.C_FART_LVL2: PLocalizer.PotionDescs[InventoryType.FartLvl2].safe_substitute({'pot': 0,'dur': 0,'unit': 0}),WeaponGlobals.C_VOMIT: PotionRecipeData.PotionRecipeList[2]['desc'],WeaponGlobals.C_HEAD_GROW: PLocalizer.PotionDescs[InventoryType.HeadGrow].safe_substitute({'pot': 0,'dur': 0,'unit': 0}),WeaponGlobals.C_CRAZY_SKIN_COLOR: PotionRecipeData.PotionRecipeList[3]['desc'],WeaponGlobals.C_SIZE_REDUCE: PotionRecipeData.PotionRecipeList[4]['desc'],WeaponGlobals.C_SIZE_INCREASE: PotionRecipeData.PotionRecipeList[5]['desc'],WeaponGlobals.C_HEAD_FIRE: PotionRecipeData.PotionRecipeList[6]['desc'],WeaponGlobals.C_SCORPION_TRANSFORM: PotionRecipeData.PotionRecipeList[7]['desc'],WeaponGlobals.C_ALLIGATOR_TRANSFORM: PotionRecipeData.PotionRecipeList[8]['desc'],WeaponGlobals.C_CRAB_TRANSFORM: PotionRecipeData.PotionRecipeList[9]['desc'],WeaponGlobals.C_ACCURACY_BONUS_LVL1: PotionRecipeData.PotionRecipeList[30]['desc'],WeaponGlobals.C_ACCURACY_BONUS_LVL2: PotionRecipeData.PotionRecipeList[31]['desc'],WeaponGlobals.C_ACCURACY_BONUS_LVL3: PotionRecipeData.PotionRecipeList[32]['desc'],WeaponGlobals.C_REMOVE_GROGGY: PotionRecipeData.PotionRecipeList[34]['desc'],WeaponGlobals.C_TOXIN: [PLocalizer.ToxinDesc, PLocalizer.ToxinUpgrade],WeaponGlobals.C_ON_CURSED_FIRE: [PLocalizer.OnFireDesc, PLocalizer.OnFireUpgrade],WeaponGlobals.C_FULLSAIL: [PLocalizer.FullSailDesc],WeaponGlobals.C_COMEABOUT: [PLocalizer.ComeAboutDesc],WeaponGlobals.C_OPENFIRE: [PLocalizer.OpenFireDesc],WeaponGlobals.C_RAM: [PLocalizer.RamDesc],WeaponGlobals.C_TAKECOVER: [PLocalizer.TakeCoverDesc],WeaponGlobals.C_RECHARGE: [PLocalizer.PowerRechargeDesc],WeaponGlobals.C_WRECKHULL: [PLocalizer.WreckHullDesc],WeaponGlobals.C_WRECKMASTS: [PLocalizer.WreckMastsDesc],WeaponGlobals.C_SINKHER: [PLocalizer.SinkHerDesc],WeaponGlobals.C_INCOMING: [PLocalizer.IncomingDesc],WeaponGlobals.C_ATTUNE: [PLocalizer.AttuneDesc]}
SkillComboReq = {InventoryType.DaggerCut: None,InventoryType.DaggerSwipe: None,InventoryType.DaggerGouge: PLocalizer.ComboReqSwipe,InventoryType.DaggerEviscerate: PLocalizer.ComboReqGouge,InventoryType.CutlassHack: None,InventoryType.CutlassSlash: None,InventoryType.CutlassCleave: PLocalizer.ComboReqSlash,InventoryType.CutlassFlourish: PLocalizer.ComboReqCleave,InventoryType.CutlassStab: PLocalizer.ComboReqFlourish}
SPECIAL_SKILL_ICONS = [
 None, 'pir_t_gui_frm_skill_special', 'pir_t_gui_frm_skill_defensive', 'pir_t_gui_frm_skill_offensive']

def getGeomScale(repId, skillId=0):
    if repId == InventoryType.PistolRep and WeaponGlobals.getSkillType(skillId) == WeaponGlobals.AMMO_SKILL:
        return 0.18
    else:
        return 0.12


class SkillButton(DirectFrame):
    notify = directNotify.newCategory('SkillButton')
    SkillIcons = None
    Image = None
    SkillRechargedSound = None
    SubLock = None

    def __init__(self, skillId, callback, quantity=0, skillRank=0, showQuantity=False, showHelp=False, showRing=False, hotkey=None, name='', showIcon=True, showLock=False, rechargeSkillId=False, isWeaponSkill=False, assocAmmo=[]):
        DirectFrame.__init__(self, parent=NodePath(), relief=None)
        self.initialiseoptions(SkillButton)
        gui = loader.loadModel('models/gui/toplevel_gui')
        if not SkillButton.SkillIcons:
            print 'not SkillButton.SkillIcons:'
            SkillButton.SkillIcons = loader.loadModel('models/textureCards/skillIcons')
            SkillButton.Image = (SkillButton.SkillIcons.find('**/base'), SkillButton.SkillIcons.find('**/base_down'), SkillButton.SkillIcons.find('**/base_over'))
            SkillButton.SkillRechargedSound = loadSfx(SoundGlobals.SFX_SKILL_RECHARGED)
            SkillButton.SubLock = gui.find('**/pir_t_gui_gen_key_subscriber')
            SkillButton.SpecialIcons = []
            for entry in SPECIAL_SKILL_ICONS:
                if not entry:
                    SkillButton.SpecialIcons.append(None)
                else:
                    specialImage = (
                     SkillButton.SkillIcons.find('**/%s' % entry),)
                    SkillButton.SpecialIcons.append(specialImage)

        model = loader.loadModel('models/effects/particleMaps')
        toggleIcon = model.find('**/particleGlow')
        toggleIcon.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.toggleFrame = DirectFrame(relief=None, state=DGG.DISABLED, parent=self, image=toggleIcon, image_scale=0.35, image_pos=(0.0, 0.0, -0.01))
        self.toggleFrame.hide()
        self.glowRing = None
        self.glowRing2 = None
        self.assocAmmo = assocAmmo
        self.skillId = skillId
        self.quantity = quantity
        self.showQuantity = showQuantity
        self.skillRank = skillRank
        self.skillRing = None
        self.callback = callback
        self.showUpgrade = False
        self.showHelp = showHelp
        self.showRing = showRing
        self.showIcon = showIcon
        self.showLock = showLock
        self.isWeaponSkill = isWeaponSkill
        self.lock = None
        self.name = name
        self.helpFrame = None
        self.quantityLabel = None
        self.skillButton = None
        self.hotkeyLabel = None
        self.hotkey = hotkey
        self.greyOut = 0
        self.tonicId = 0
        self.skillRingIval = None
        self.impulseIval = None
        self.quickImpulseIval = None
        self.isBreakAttackSkill = WeaponGlobals.getSkillTrack(self.skillId) == WeaponGlobals.BREAK_ATTACK_SKILL_INDEX
        self.isDefenseSkill = WeaponGlobals.getSkillTrack(self.skillId) == WeaponGlobals.DEFENSE_SKILL_INDEX
        self.rechargeFilled = 0
        self.defenseAuraEffect = None
        if self.isWeaponSkill:
            self.weaponBackground = DirectLabel(parent=self, state=DGG.DISABLED, image=SkillButton.SkillIcons.find('**/box_base'), image_scale=(0.22,
                                                                                                                                                0,
                                                                                                                                                0.22), image_pos=(0.0,
                                                                                                                                                                  0.0,
                                                                                                                                                                  0.0))
            self.weaponBackground.flattenLight()
            self.weaponBackground.setColor(0.2, 0.2, 0.2, 0.2)
            self.weaponBackground.setTransparency(1)
        if showRing:
            if self.isBreakAttackSkill:
                color = Vec4(1, 0, 0, 1)
            elif self.isDefenseSkill:
                color = Vec4(0, 1, 1, 1)
            else:
                color = Vec4(1, 0.8, 0.5, 1)
            self.skillRing = SkillRing(color, Vec4(0, 0, 0, 1.0))
            gs = self.skillRing.meterFaceHalf2.node().getGeomState(0)
            self.skillRing.meterFaceHalf2.node().setGeomState(0, gs.removeAttrib(ColorAttrib.getClassType()))
            self.skillRing.reparentTo(self, 0)
            self.skillRing.setPos(0, 0, 0)
        self.updateSkillId(skillId)
        if showQuantity:
            self.updateQuantity(quantity)
        if hotkey:
            self.createHotkey(hotkey)
        if showLock:
            self.createLock()
        self.skillButton.bind(DGG.ENTER, self.showDetails)
        self.skillButton.bind(DGG.EXIT, self.hideDetails)
        if self.skillId >= InventoryType.begin_Consumables and self.skillId <= InventoryType.end_Consumables and not WeaponGlobals.getSkillEffectFlag(skillId):
            self.totalRechargeTime = base.cr.battleMgr.getModifiedRechargeTime(localAvatar, InventoryType.UseItem)
            self.tonicId = InventoryType.UseItem
        else:
            self.totalRechargeTime = base.cr.battleMgr.getModifiedRechargeTime(localAvatar, self.skillId)
        if showRing:
            if not self.isBreakAttackSkill:
                self.createSkillRingIval()
            if self.tonicId:
                timeSpentRecharging = localAvatar.skillDiary.getTimeSpentRecharging(InventoryType.UseItem)
            else:
                timeSpentRecharging = localAvatar.skillDiary.getTimeSpentRecharging(self.skillId)
            if self.isBreakAttackSkill and timeSpentRecharging < self.totalRechargeTime:
                self.updateRechargeRing()
            elif not self.isBreakAttackSkill and self.totalRechargeTime and timeSpentRecharging and not timeSpentRecharging > self.totalRechargeTime:
                self.skillRingIval.start(startT=timeSpentRecharging)
            else:
                self.skillRing.meterFaceHalf1.setR(0)
                self.skillRing.meterFaceHalf2.setR(180)
                self.skillRing.meterFaceHalf1.setColor(self.skillRing.meterActiveColor, 100)
                self.skillRing.meterFaceHalf2.setColor(self.skillRing.meterActiveColor, 100)
                self.skillRing.meterFaceHalf1.show()
                self.skillRing.meterFaceHalf2.show()
        if not self.isBreakAttackSkill:
            self.checkAmount()
        if self.isDefenseSkill:
            self.startRecharge()
        if self.isWeaponSkill:
            self.weaponLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.WeaponAbility, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, pos=(0.0, 0, -0.12), sortOrder=70, state=DGG.DISABLED)
            self.weaponLabel.flattenLight()
        return

    def loadGlowRing(self):
        self.glowRing = loader.loadModel('models/effects/battleEffects').find('**/effectVoodooShockwave')
        self.glowRing.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.glowRing.reparentTo(self)
        self.glowRing.setBin('transparent', 0)
        self.glowRing.setScale(0.2)
        self.glowRing.hide()
        self.glowRing2 = loader.loadModel('models/effects/particleMaps').find('**/particleGlow')
        self.glowRing2.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OOneMinusIncomingAlpha, ColorBlendAttrib.OOne))
        self.glowRing2.reparentTo(self)
        self.glowRing2.setBin('transparent', 0)
        self.glowRing2.setScale(0.2)
        self.glowRing2.setColor(0.8, 1, 0.8, 0.2)
        self.glowRing2.reparentTo(self)
        self.glowRing2.hide()

    def checkAmount(self):
        if not self.quantity and self.showQuantity:
            if self.showRing and not self.skillRingIval.isPlaying():
                self.setGeomColor(0.5, 0.5, 0.5, 1.0)
                self.setRingColor(Vec4(0.5, 0.5, 0.5, 1.0))
        elif self.showRing and not self.skillRingIval.isPlaying():
            self.setGeomColor(1.0, 1.0, 1.0, 1.0)
            self.setRingColor(self.skillRing.meterActiveColor)

    def toggleButton(self, state):
        if state == True:
            self.toggleFrame.show()
        elif state == False:
            self.toggleFrame.hide()

    def createSkillRingIval(self):
        if self.skillRingIval:
            self.skillRingIval.pause()
            self.skillRing.meterFaceHalf1.setR(0)
            self.skillRing.meterFaceHalf2.setR(180)
            self.skillRing.setScale(1.0)
            self.skillRing.clearColorScale()
            self.setGeomColor(1.0, 1.0, 1.0, 1.0)
            self.checkAmount()
            self.skillRingIval = None
        if self.tonicId:
            timeSpentRecharging = localAvatar.skillDiary.getTimeSpentRecharging(InventoryType.UseItem)
        else:
            timeSpentRecharging = localAvatar.skillDiary.getTimeSpentRecharging(self.skillId)
        if self.isDefenseSkill:
            localAvatar.setDefenceEffect(self.skillId)
        if self.showRing:
            self.skillRingIval = Sequence(Func(localAvatar.setDefenceEffect, 0), Func(self.setGeomColor, 0.5, 0.5, 0.5, 1.0), Func(self.skillRing.meterFaceHalf1.setColor, self.skillRing.meterActiveColor, 100), Func(self.skillRing.meterFaceHalf2.setColor, self.skillRing.meterColor, 100), Func(self.skillRing.meterFaceHalf1.setR, 0), Func(self.skillRing.meterFaceHalf2.setR, 0), Func(self.skillRing.meterFaceHalf1.show), Func(self.skillRing.meterFaceHalf2.show), LerpFunc(self.skillRing.meterFaceHalf2.setR, self.totalRechargeTime / 2, 0, -180), Func(self.skillRing.meterFaceHalf2.setColor, self.skillRing.meterActiveColor, 100), Func(self.skillRing.meterFaceHalf2.setR, 0), LerpFunc(self.skillRing.meterFaceHalf1.setR, self.totalRechargeTime / 2, 0, -180), Func(self.setGeomColor, 1.0, 1.0, 1.0, 1.0), Func(base.playSfx, SkillButton.SkillRechargedSound, volume=0.5), Parallel(LerpScaleInterval(self.skillRing, 0.1, Vec3(1.2, 1.2, 1.2)), LerpColorScaleInterval(self.skillRing, 0.1, Vec4(0.0, 0.75, 0.0, 1.0), Vec4(1.0, 1.0, 1.0, 1.0), blendType='easeInOut')), Func(localAvatar.setDefenceEffect, self.skillId), LerpScaleInterval(self.skillRing, 0.2, Vec3(0.9, 0.9, 0.9)), LerpScaleInterval(self.skillRing, 0.03, Vec3(1.1, 1.1, 1.1)), Parallel(LerpScaleInterval(self.skillRing, 0.03, Vec3(1.0, 1.0, 1.0)), LerpColorScaleInterval(self.skillRing, 1, Vec4(1.0, 1.0, 1.0, 1.0), blendType='easeInOut')), Func(self.skillRing.clearColorScale), Func(self.checkAmount))
        return

    def updateSkillRingIval(self):
        if self.showRing:
            playing = self.skillRingIval.isPlaying()
            if self.tonicId:
                timeSpentRecharging = localAvatar.skillDiary.getTimeSpentRecharging(InventoryType.UseItem)
            else:
                timeSpentRecharging = localAvatar.skillDiary.getTimeSpentRecharging(self.skillId)
            if timeSpentRecharging:
                skillRechargeProgress = timeSpentRecharging / self.totalRechargeTime
            self.totalRechargeTime = base.cr.battleMgr.getModifiedRechargeTime(localAvatar, self.skillId)
            if not self.totalRechargeTime:
                self.totalRechargeTime = base.cr.battleMgr.getModifiedRechargeTime(localAvatar, InventoryType.UseItem)
            if timeSpentRecharging:
                timeSpentRecharging = skillRechargeProgress * self.totalRechargeTime
                localAvatar.skillDiary.modifyTimeSpentRecharging(self.skillId, timeSpentRecharging)
            self.createSkillRingIval()
            if playing and timeSpentRecharging:
                self.skillRingIval.start(startT=timeSpentRecharging)

    def quickGlowImpulse(self):
        if not self.glowRing2:
            self.loadGlowRing()
        self.quickImpulseIval = Sequence(Func(self.glowRing2.show), LerpScaleInterval(self.glowRing2, 0.2, Vec3(0.33, 0.33, 0.33)), LerpScaleInterval(self.glowRing2, 0.25, Vec3(0.2, 0.2, 0.2)), Func(self.glowRing2.hide))
        self.quickImpulseIval.start()

    def startPowerImpulse(self):
        if not self.glowRing:
            self.loadGlowRing()
        self.glowRing.show()
        self.impulseIval = Sequence(Parallel(LerpScaleInterval(self.glowRing, 0.1, Vec3(0.203, 0.203, 0.203)), LerpColorScaleInterval(self.glowRing, 0.1, Vec4(0.8, 0.8, 0.8, 0.8), Vec4(1.0, 1.0, 1.0, 0.8), blendType='easeInOut')), LerpScaleInterval(self.glowRing, 0.15, Vec3(0.19, 0.19, 0.19)), LerpScaleInterval(self.glowRing, 0.05, Vec3(0.202, 0.202, 0.202)), Parallel(LerpScaleInterval(self.glowRing, 0.03, Vec3(0.2, 0.2, 0.2)), LerpColorScaleInterval(self.glowRing, 0.4, Vec4(1.0, 1.0, 1.0, 1.0), blendType='easeInOut')), Func(self.glowRing.clearColorScale))
        self.impulseIval.loop()

    def stopPowerImpulse(self):
        if self.glowRing:
            self.glowRing.hide()
        if self.impulseIval:
            self.impulseIval.finish()
            self.impulseIval = None
        return

    def updateRechargeRing(self):
        timeSpentRecharging = localAvatar.skillDiary.getTimeSpentRecharging(self.skillId)
        self.totalRechargeTime = base.cr.battleMgr.getModifiedRechargeTime(localAvatar, self.skillId)
        if timeSpentRecharging >= self.totalRechargeTime and not self.rechargeFilled:
            self.rechargeFilled = 1
            if self.skillRingIval:
                self.skillRingIval.pause()
                self.skillRingIval = None
            self.skillRing.meterFaceHalf1.setR(0)
            self.skillRing.meterFaceHalf2.setR(180)
            self.skillRing.setScale(1.0)
            self.skillRing.clearColorScale()
            self.setGeomColor(1.0, 1.0, 1.0, 1.0)
            self.skillRingIval = Sequence(Func(base.playSfx, SkillButton.SkillRechargedSound, volume=0.5), Parallel(LerpScaleInterval(self.skillRing, 0.1, Vec3(1.2, 1.2, 1.2)), LerpColorScaleInterval(self.skillRing, 0.1, Vec4(0.0, 0.75, 0.0, 1.0), Vec4(1.0, 1.0, 1.0, 1.0), blendType='easeInOut')), Func(localAvatar.setDefenceEffect, self.skillId), LerpScaleInterval(self.skillRing, 0.2, Vec3(0.9, 0.9, 0.9)), LerpScaleInterval(self.skillRing, 0.03, Vec3(1.1, 1.1, 1.1)), Parallel(LerpScaleInterval(self.skillRing, 0.03, Vec3(1.0, 1.0, 1.0)), LerpColorScaleInterval(self.skillRing, 1, Vec4(1.0, 1.0, 1.0, 1.0), blendType='easeInOut')), Func(self.skillRing.clearColorScale))
            self.skillRingIval.start()
        elif timeSpentRecharging < self.totalRechargeTime:
            self.rechargeFilled = 0
            self.setGeomColor(0.5, 0.5, 0.5, 1.0)
            self.skillRing.update(timeSpentRecharging, self.totalRechargeTime)
        return

    def updateSkillId(self, skillId):
        self.skillId = skillId
        if self.skillButton:
            if self.quantityLabel:
                self.quantityLabel.detachNode()
            self.skillButton.destroy()
        if self.showQuantity and not self.quantity:
            geomColor = Vec4(0.5, 0.5, 0.5, 1.0)
        else:
            geomColor = Vec4(1.0, 1.0, 1.0, 1.0)
        if self.showIcon:
            asset = WeaponGlobals.getSkillIcon(skillId)
            if hasattr(self, '_skillIconName'):
                asset = self._skillIconName
            geom = SkillButton.SkillIcons.find('**/%s' % asset)
            if geom.isEmpty():
                geom = SkillButton.SkillIcons.find('**/base')
            repId = WeaponGlobals.getSkillReputationCategoryId(self.skillId)
            geom_scale = getGeomScale(repId, skillId)
            image_color = (1, 1, 1, 1)
        else:
            geom = (None, )
            geom_scale = 0.12
            image_color = (0.5, 0.5, 0.5, 0.5)
        specialIconId = 0
        if self.isBreakAttackSkill:
            specialIconId = 1
        else:
            if self.isDefenseSkill:
                specialIconId = 2
            elif skillId == ItemGlobals.getSpecialAttack(localAvatar.currentWeaponId):
                specialIconId = 3
            if specialIconId:
                something = SkillButton.SpecialIcons[specialIconId][0]
                if self.skillRing:
                    self.skillRing.setupFace(something)
                self['image'] = None
            elif self.skillRing:
                self.skillRing.setupFace()
            if self.showRing:
                image = None
            image = SkillButton.Image
        self.skillButton = DirectButton(parent=self, relief=None, pos=(0, 0, 0), text=('', '', self.name), text_align=TextNode.ACenter, text_shadow=Vec4(0, 0, 0, 1), text_scale=0.04, text_fg=Vec4(1, 1, 1, 1), text_pos=(0.0,
                                                                                                                                                                                                                           0.09), image=image, image_scale=0.15, image_color=image_color, geom=geom, geom_scale=geom_scale, geom_color=geomColor, command=self.callback, sortOrder=50, extraArgs=[skillId])
        self.skillButton.bind(DGG.ENTER, self.showDetails)
        self.skillButton.bind(DGG.EXIT, self.hideDetails)
        if self.quantityLabel and not self.quantityLabel.isEmpty():
            self.quantityLabel.reparentTo(self.skillButton)
        return

    def createHotkey(self, hotkey):
        self.hotkeyLabel = DirectLabel(parent=self, relief=None, text=hotkey, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, pos=(0.07, 0, -0.06), sortOrder=70, state=DGG.DISABLED)
        self.hotkeyLabel.flattenLight()
        return

    def createLock(self):
        if self.lock:
            return
        self.lock = DirectFrame(parent=self, relief=None, image=SkillButton.SubLock, image_scale=0.14, image_pos=(0.05, 0, -0.025), sortOrder=99)
        if self.showIcon:
            self.lock.setColorScale(0.9, 0.9, 0.9, 1)
            self.skillButton.setColorScale(0.4, 0.4, 0.4, 1, 1)
        else:
            self.lock.setColorScale(0.6, 0.6, 0.6, 1, 2)
            self.skillButton.clearColorScale()
        if self.showHelp:
            self.lock.hide()
        return

    def createHelpFrame(self, args=None):
        if self.helpFrame:
            return
        inv = localAvatar.getInventory()
        if not inv:
            return
        baseRank = max(self.skillRank, 1)
        lvlDamageMod = WeaponGlobals.getLevelDamageModifier(localAvatar.getLevel())
        buff = WeaponGlobals.getSkillEffectFlag(self.skillId)
        dur = WeaponGlobals.getAttackDuration(self.skillId)
        effect = dur + dur * (baseRank - 1) / 4.0
        bonus = localAvatar.getSkillRankBonus(self.skillId)
        upgradeAmt = WeaponGlobals.getAttackUpgrade(self.skillId)
        rank = localAvatar.getSkillRank(self.skillId)
        skillBoost = 0
        if self.skillId in ItemGlobals.getLinkedSkills(localAvatar.currentWeaponId):
            linkedSkillId = WeaponGlobals.getLinkedSkillId(self.skillId)
            skillBoost = ItemGlobals.getWeaponBoosts(localAvatar.currentWeaponId, linkedSkillId)
            skillBoost += ItemGlobals.getWeaponBoosts(localAvatar.getCurrentCharm(), linkedSkillId)
        else:
            skillBoost = ItemGlobals.getWeaponBoosts(localAvatar.currentWeaponId, self.skillId)
            skillBoost += ItemGlobals.getWeaponBoosts(localAvatar.getCurrentCharm(), self.skillId)
        shipBoost = 0
        if localAvatar.ship:
            shipBoost = localAvatar.ship.getSkillBoost(self.skillId)
        manaCost = 0
        if WeaponGlobals.getSkillTrack(self.skillId) != WeaponGlobals.PASSIVE_SKILL_INDEX:
            manaCost = WeaponGlobals.getMojoCost(self.skillId)
            if manaCost < 0:
                amt = localAvatar.getSkillRankBonus(InventoryType.StaffConservation)
                manaCost = min(manaCost - manaCost * amt, 1.0)
        damage = 0
        loDamage = 0
        mpDamage = 0
        mpLoDamage = 0
        if WeaponGlobals.getSkillTrack(self.skillId) == WeaponGlobals.TONIC_SKILL_INDEX:
            damage = WeaponGlobals.getAttackSelfHP(self.skillId)
        elif WeaponGlobals.getSkillTrack(self.skillId) != WeaponGlobals.PASSIVE_SKILL_INDEX:
            mod = (1.0 + bonus) * lvlDamageMod
            damage = int(WeaponGlobals.getAttackTargetHP(self.skillId) * mod)
            loDamage = damage / 2
            mpDamage = int(WeaponGlobals.getAttackTargetMojo(self.skillId) * mod)
            mpLoDamage = mpDamage / 2
        try:
            skillInfo = PLocalizer.SkillDescriptions.get(self.skillId)
            skillTitle = PLocalizer.makeHeadingString(PLocalizer.InventoryTypeNames.get(self.skillId), 2)
            skillType = PLocalizer.makeHeadingString(skillInfo[0], 1)
        except:
            self.notify.error('Error getting skill info for skillId %s' % self.skillId)

        description = skillInfo[1]
        if damage < 0:
            description += ' ' + PLocalizer.DealsDamage
        elif damage > 0:
            if loDamage:
                loDamage = 0
                description += ' ' + PLocalizer.HealsDamageRange
            else:
                description += ' ' + PLocalizer.HealsDamage
        if mpDamage < 0:
            description += ' ' + PLocalizer.DealsMpDamage
        effectId = WeaponGlobals.getSkillEffectFlag(self.skillId)
        if effectId:
            description += ' ' + SkillEffectDescriptions.get(effectId)[0]
        if bonus:
            if self.skillId == InventoryType.SailBroadsideLeft or self.skillId == InventoryType.SailBroadsideRight:
                description += ' ' + PLocalizer.BroadsideDesc
            if self.skillId == InventoryType.CannonShoot:
                description += ' ' + PLocalizer.CannonShootDesc
            if self.skillId == InventoryType.DollAttune:
                description += ' ' + PLocalizer.MultiAttuneDesc
        if WeaponGlobals.getSkillInterrupt(self.skillId):
            description += ' ' + PLocalizer.InterruptDesc
        if WeaponGlobals.getSkillUnattune(self.skillId):
            description += ' ' + PLocalizer.UnattuneDesc
        upgradeInfo = ''
        if self.showUpgrade:
            if rank < 5:
                if rank > 0:
                    upgradeInfo = skillInfo[2]
                    if upgradeInfo == '':
                        if damage < 0:
                            upgradeInfo += PLocalizer.UpgradesDamage
                        elif damage > 0:
                            upgradeInfo += PLocalizer.UpgradesHealing
                        if mpDamage < 0:
                            upgradeInfo += ' ' + PLocalizer.UpgradesMpDamage
                        if effectId:
                            entry = SkillEffectDescriptions.get(effectId)
                            if len(entry) > 1:
                                damage or upgradeInfo += PLocalizer.UpgradesDuration
                            else:
                                upgradeInfo += ' ' + PLocalizer.And
                            upgradeInfo += ' ' + entry[1]
                    upgradeInfo += '!'
            elif len(upgradeInfo) >= 4:
                upgradeInfo = skillInfo[3]
            else:
                upgradeInfo = PLocalizer.ClickToLearn
        elif not self.showIcon:
            unlockLevel = RepChart.getSkillUnlockLevel(self.skillId)
            if unlockLevel > 0:
                upgradeInfo = PLocalizer.UnlocksAtLevel % unlockLevel
        if self.skillId in SkillComboReq and SkillComboReq[self.skillId] and inv.getStackQuantity(self.skillId - 1) < 2:
            color = '\x01red\x01'
            if rank == 0:
                color = '\x01red\x01'
                upgradeInfo = ''
            description += '\n' + color + SkillComboReq[self.skillId] + '.'
        skillDesc = skillTitle + '\n' + skillType + '\n\n' + description + '\n\x01green\x01' + upgradeInfo + '\x02'
        stats = []
        if manaCost:
            stats.append(abs(manaCost))
        if damage and loDamage:
            stats.append(abs(loDamage))
            stats.append(abs(damage))
        elif damage:
            stats.append(abs(damage))
        if mpDamage:
            stats.append(abs(mpLoDamage))
            stats.append(abs(mpDamage))
        if buff == WeaponGlobals.C_CURSE:
            stats.append(WeaponGlobals.CURSED_DAM_AMP * 100)
        if buff == WeaponGlobals.C_WEAKEN:
            stats.append(WeaponGlobals.WEAKEN_PENALTY * 100)
        if effect > 0:
            stats.append(effect)
        if skillInfo[4]:
            if bonus == 0 and upgradeAmt > 0 and not (self.skillId == InventoryType.SailBroadsideLeft or self.skillId == InventoryType.SailBroadsideRight or self.skillId == InventoryType.CannonShoot):
                bonus = upgradeAmt
            if upgradeAmt < 1.0 and upgradeAmt > 0:
                bonus *= 100
            if self.skillId == InventoryType.SailTreasureSense:
                bonus /= 2.0
            elif self.skillId == InventoryType.CutlassParry:
                bonus += WeaponGlobals.getSubtypeParryBonus(localAvatar.currentWeaponId)
            if bonus:
                stats.append(abs(bonus))
        if self.skillId == InventoryType.DollAttune:
            stats.append(rank)
        if self.skillRank:
            rankText = DirectFrame(parent=self, relief=None, text=PLocalizer.makeHeadingString(PLocalizer.Rank + ' %s' % (self.skillRank + skillBoost + shipBoost), 2), text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleSmall, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=15, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                   1), pos=(0.45,
                                                                                                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                                                                                                            0), textMayChange=1, sortOrder=92, state=DGG.DISABLED)
        stats = tuple((stat + 0.01 for stat in stats))
        try:
            skillDesc % stats
        except TypeError:
            self.notify.error('Error formatting skillDesc(%s): %s' % (self.skillId, stats))

        helpText = DirectFrame(parent=self, relief=None, text=skillDesc % stats, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=17, textMayChange=1, state=DGG.DISABLED, sortOrder=91)
        height = -(helpText.getHeight() + 0.01)
        if self.lock:
            height = height - 0.04
        width = 0.55
        self.helpFrame = BorderFrame(parent=self, state=DGG.DISABLED, frameSize=(-0.04, width, height, 0.05), pos=(0, 0, -0.12), sortOrder=90)
        self.helpFrame.setBin('gui-popup', 0)
        helpText.reparentTo(self.helpFrame)
        if self.skillRank:
            rankText.reparentTo(self.helpFrame)
        if self.lock:
            self.lockedFrame = DirectFrame(parent=self.helpFrame, relief=None, pos=(0.088, 0, height + 0.03), image=SkillButton.SubLock, image_scale=0.13, image_pos=(-0.055, 0, 0.013), text=PLocalizer.VR_AuthAccess, text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG13)
            self.notify.debug('locked!')
        pos = self.helpFrame.getPos(aspect2d)
        x = min(pos[0], base.a2dRight - width)
        z = max(pos[2], base.a2dBottom - height)
        self.helpFrame.setPos(aspect2d, x, 0, z)
        return

    def showDetails(self, event):
        if self.showHelp:
            self.createHelpFrame()
        if self.showRing:
            self.skillRing.rollover(True)

    def hideDetails(self, event):
        if self.helpFrame:
            self.helpFrame.destroy()
            self.helpFrame = None
        if self.showRing:
            self.skillRing.rollover(False)
        return

    def updateQuantity(self, quantity):
        self.quantity = quantity
        if not self.showQuantity:
            return
        if quantity == WeaponGlobals.INF_QUANT:
            text = ''
        elif self.assocAmmo:
            assocQuantity = 0
            inv = localAvatar.getInventory()
            if inv:
                for ammoId in self.assocAmmo:
                    assocQuantity += inv.getItemQuantity(self.getAmmoCat(), ammoId)

            if quantity != assocQuantity:
                text = '%s' % assocQuantity
            else:
                text = 'x%s' % quantity
        else:
            text = 'x%s' % quantity
        if self.quantityLabel and not self.quantityLabel.isEmpty():
            self.quantityLabel['text'] = text
        else:
            self.quantityLabel = DirectLabel(parent=NodePath(), relief=None, state=DGG.DISABLED, text=text, frameColor=(0,
                                                                                                                        0,
                                                                                                                        0,
                                                                                                                        1), frameSize=(-0.01, 0.02, -0.01, 0.025), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.03,
                                                                                                                                                                                                                                                                                                                                                 0.0,
                                                                                                                                                                                                                                                                                                                                                 0.03), text_font=PiratesGlobals.getPirateBoldOutlineFont(), sortOrder=60)
            self.quantityLabel.flattenLight()
            self.quantityLabel.reparentTo(self)
            if self.skillButton and not self.skillButton.isEmpty():
                self.quantityLabel.reparentTo(self.skillButton)
        return

    def getAmmoCat(self):
        return None

    def startRecharge(self):
        if not self.showRing:
            return
        if self.isBreakAttackSkill:
            self.setGeomColor(0.5, 0.5, 0.5, 1.0)
            self.updateRechargeRing()
            return
        if self.skillRingIval.isPlaying():
            self.createSkillRingIval()
        self.skillRingIval.start()

    def stopRecharge(self):
        if self.showRing:
            if self.isBreakAttackSkill:
                self.setGeomColor(0.5, 0.5, 0.5, 1.0)
                self.updateRechargeRing()
                return
            if self.skillRingIval.isPlaying():
                self.skillRingIval.pause()

    def setGeomColor(self, r, g, b, a):
        self.skillButton['geom_color'] = Vec4(r, g, b, a)

    def setRingColor(self, color):
        self.skillRing.meterFaceHalf1.setColor(color[0], color[1], color[2], color[3], 100)
        self.skillRing.meterFaceHalf2.setColor(color[0], color[1], color[2], color[3], 100)

    def setShowUpgrade(self, show):
        if self.showUpgrade != show:
            self.showUpgrade = show
            if self.helpFrame:
                self.helpFrame.destroy()
                self.helpFrame = None
                self.showDetails(None)
        return

    def setShowIcon(self, show):
        if self.showIcon != show:
            self.showIcon = show
            self.updateSkillId(self.skillId)
            if self.helpFrame:
                self.helpFrame.destroy()
                self.helpFrame = None
        return

    def setShowLock(self, show):
        if self.showLock != show:
            self.showLock = show
            if show:
                self.createLock()
            elif self.lock:
                self.lock.destroy()
                self.lock = None
                self.skillButton.clearColorScale()
        return

    def destroy(self):
        self.callback = None
        if self.skillRingIval:
            self.skillRingIval.pause()
            self.skillRingIval = None
        if self.quantityLabel:
            self.quantityLabel.destroy()
            self.quantityLabel = None
        if self.impulseIval:
            self.impulseIval.pause()
            self.impulseIval = None
        if self.quickImpulseIval:
            self.quickImpulseIval.pause()
            self.quickImpulseIval = None
        self.ignoreAll()
        DirectFrame.destroy(self)
        return