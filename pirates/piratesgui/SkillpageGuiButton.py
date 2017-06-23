from direct.showbase import DirectObject
from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui import RadialMenu
SkillEffectDescriptions = {WeaponGlobals.C_POISON: [PLocalizer.PoisonDesc, PLocalizer.PoisonUpgrade],WeaponGlobals.C_ACID: [PLocalizer.AcidDesc, PLocalizer.AcidUpgrade],WeaponGlobals.C_HOLD: [PLocalizer.HoldDesc, PLocalizer.HoldUpgrade],WeaponGlobals.C_WOUND: [PLocalizer.WoundDesc, PLocalizer.WoundUpgrade],WeaponGlobals.C_ON_FIRE: [PLocalizer.OnFireDesc, PLocalizer.OnFireUpgrade],WeaponGlobals.C_FLAMING: [PLocalizer.OnFireDesc, PLocalizer.OnFireUpgrade],WeaponGlobals.C_STUN: [PLocalizer.StunDesc, PLocalizer.StunUpgrade],WeaponGlobals.C_SLOW: [PLocalizer.SlowDesc, PLocalizer.SlowUpgrade],WeaponGlobals.C_BLIND: [PLocalizer.BlindDesc, PLocalizer.BlindUpgrade],WeaponGlobals.C_DIRT: [PLocalizer.BlindDesc, PLocalizer.BlindUpgrade],WeaponGlobals.C_CURSE: [PLocalizer.CurseDesc, PLocalizer.CurseUpgrade],WeaponGlobals.C_HASTEN: [PLocalizer.HastenDesc, PLocalizer.HastenUpgrade],WeaponGlobals.C_TAUNT: [PLocalizer.TauntDesc, PLocalizer.TauntUpgrade],WeaponGlobals.C_WEAKEN: [PLocalizer.WeakenDesc, PLocalizer.WeakenUpgrade],WeaponGlobals.C_SOULTAP: [PLocalizer.SoulTapDesc],WeaponGlobals.C_MANADRAIN: [PLocalizer.ManaDrainDesc],WeaponGlobals.C_LIFEDRAIN: [PLocalizer.LifeDrainDesc],WeaponGlobals.C_UNDEAD_KILLER: [PLocalizer.UndeadKillerDesc],WeaponGlobals.C_MONSTER_KILLER: [PLocalizer.MonsterKillerDesc],WeaponGlobals.C_BUFF_BREAK: [PLocalizer.BuffBreakDesc, PLocalizer.BuffBreakUpgrade],WeaponGlobals.C_REGEN: [PLocalizer.RegenDesc, PLocalizer.RegenUpgrade],WeaponGlobals.C_TOXIN: [PLocalizer.ToxinDesc, PLocalizer.ToxinUpgrade],WeaponGlobals.C_ON_CURSED_FIRE: [PLocalizer.OnFireDesc, PLocalizer.OnFireUpgrade],WeaponGlobals.C_FULLSAIL: [PLocalizer.FullSailDesc],WeaponGlobals.C_COMEABOUT: [PLocalizer.ComeAboutDesc],WeaponGlobals.C_OPENFIRE: [PLocalizer.OpenFireDesc],WeaponGlobals.C_RAM: [PLocalizer.RamDesc],WeaponGlobals.C_TAKECOVER: [PLocalizer.TakeCoverDesc],WeaponGlobals.C_RECHARGE: [PLocalizer.PowerRechargeDesc],WeaponGlobals.C_ATTUNE: [PLocalizer.AttuneDesc]}
SkillComboReq = {InventoryType.DaggerCut: None,InventoryType.DaggerSwipe: None,InventoryType.DaggerGouge: PLocalizer.ComboReqSwipe,InventoryType.DaggerEviscerate: PLocalizer.ComboReqGouge,InventoryType.CutlassHack: None,InventoryType.CutlassSlash: None,InventoryType.CutlassCleave: PLocalizer.ComboReqSlash,InventoryType.CutlassFlourish: PLocalizer.ComboReqCleave,InventoryType.CutlassStab: PLocalizer.ComboReqFlourish}

class SkillpageGuiButton(DirectButton):
    SkillIcons = None

    def __init__(self, callback, skillId, skillRank):
        if not SkillpageGuiButton.SkillIcons:
            SkillpageGuiButton.SkillIcons = loader.loadModel('models/textureCards/skillIcons')
            SkillpageGuiButton.Image = (SkillpageGuiButton.SkillIcons.find('**/base'), SkillpageGuiButton.SkillIcons.find('**/base_down'), SkillpageGuiButton.SkillIcons.find('**/base_over'))
        asset = RadialMenu.getSkillIconName(skillId, 0)
        geom = SkillpageGuiButton.SkillIcons.find('**/%s' % asset)
        DirectButton.__init__(self, relief=None, pos=(0, 0, 0), image=SkillpageGuiButton.Image, image_scale=0.12, geom=geom, geom_scale=0.12, command=callback, textMayChange=1, sortOrder=70, extraArgs=[skillId])
        self.initialiseoptions(SkillpageGuiButton)
        self.skillId = skillId
        self.skillRank = skillRank
        self.showUpgrade = 0
        self.helpBox = None
        self.quantity = None
        self.bind(DGG.ENTER, self.showDetails)
        self.bind(DGG.EXIT, self.hideDetails)
        return

    def createHelpbox(self, args=None):
        if self.helpBox:
            return
        baseRank = max(self.skillRank, 1)
        lvlDamageMod = WeaponGlobals.getLevelDamageModifier(localAvatar.getLevel())
        buff = WeaponGlobals.getSkillEffectFlag(self.skillId)
        dur = WeaponGlobals.getAttackDuration(self.skillId)
        effect = dur + dur * (baseRank - 1) / 4
        dodge = WeaponGlobals.getAttackDodge(self.skillId) * baseRank
        accuracy = 0
        damageMod = 0
        reduceDamMod = 0
        rechargeMod = 0
        shipTurningMod = 0
        shipSpeedMod = 0
        rangeMod = 0
        treasureSenseMod = 0
        manaCost = WeaponGlobals.getMojoCost(self.skillId)
        damage = 0
        loDamage = 0
        mpDamage = 0
        chargeMod = 0
        if self.skillId == InventoryType.SailBroadsideLeft or self.skillId == InventoryType.SailBroadsideRight:
            damageMod = WeaponGlobals.getAttackTargetHP(self.skillId) * (baseRank - 1) * 100
        else:
            if self.skillId == InventoryType.CannonShoot:
                rechargeMod = WeaponGlobals.CANNON_SHOOT_RATE_REDUCTION * (baseRank - 1) * 100
            else:
                if WeaponGlobals.getSkillTrack(self.skillId) == WeaponGlobals.TONIC_SKILL_INDEX:
                    damage = WeaponGlobals.getAttackSelfHP(self.skillId)
                else:
                    if WeaponGlobals.getSkillTrack(self.skillId) != WeaponGlobals.PASSIVE_SKILL_INDEX:
                        damage = int(WeaponGlobals.getAttackTargetHP(self.skillId) * (1.0 + WeaponGlobals.LEVELUP_DAMAGE_MULTIPLIER * (baseRank - 1))) * lvlDamageMod
                        loDamage = damage / 2
                        mpDamage = int(WeaponGlobals.getAttackTargetMojo(self.skillId) * (1.0 + WeaponGlobals.LEVELUP_DAMAGE_MULTIPLIER * (baseRank - 1))) * lvlDamageMod
                        mpLoDamage = mpDamage / 2
                    else:
                        accuracy = WeaponGlobals.getAttackAccuracy(self.skillId) * baseRank
                        damageMod = WeaponGlobals.getAttackTargetHP(self.skillId) * baseRank * 100
                        reduceDamMod = WeaponGlobals.getAttackSelfHP(self.skillId) * baseRank
                        if reduceDamMod < 1:
                            reduceDamMod *= 100
                        if effect < 1:
                            effect *= 100
                        rechargeMod = WeaponGlobals.getAttackRechargeTime(self.skillId) * baseRank * 100
                        shipTurningMod = WeaponGlobals.getShipTurnRate(self.skillId) * baseRank * 100
                        shipSpeedMod = WeaponGlobals.getShipMaxSpeed(self.skillId) * baseRank * 100
                        treasureSenseMod = WeaponGlobals.TREASURE_SENSE_BONUS / 2 * baseRank
                        rangeMod = WeaponGlobals.getAttackRange(self.skillId) * baseRank
                        manaCost *= baseRank
                        chargeMod = WeaponGlobals.getAttackMaxCharge(self.skillId) * baseRank * 100
                    if self.skillId == InventoryType.StaffSpiritLore:
                        import pdb
                        pdb.set_trace()
                    skillInfo = PLocalizer.SkillDescriptions.get(self.skillId)
                    skillTitle = PLocalizer.InventoryTypeNames.get(self.skillId)
                    skillType = '\x01slant\x01' + skillInfo[0] + '\x02\n\n'
                    description = skillInfo[1]
                    if damage < 0:
                        description += ' ' + PLocalizer.DealsDamage
                    elif damage > 0:
                        if loDamage:
                            description += ' ' + PLocalizer.HealsDamageRange
                        else:
                            description += ' ' + PLocalizer.HealsDamage
                    if mpDamage < 0:
                        description += ' ' + PLocalizer.DealsMpDamage
                    effectId = WeaponGlobals.getSkillEffectFlag(self.skillId)
                    if effectId:
                        description += ' ' + SkillEffectDescriptions.get(effectId)[0]
                    if self.skillId == InventoryType.SailBroadsideLeft or self.skillId == InventoryType.SailBroadsideRight:
                        if damageMod > 0:
                            description += ' ' + PLocalizer.BroadsideDesc
                        if self.skillId == InventoryType.CannonShoot and rechargeMod:
                            description += ' ' + PLocalizer.CannonShootDesc
                        if self.skillId == InventoryType.DollAttune:
                            description += ' ' + PLocalizer.MultiAttuneDesc
                        if WeaponGlobals.getSkillInterrupt(self.skillId):
                            description += ' ' + PLocalizer.InterruptDesc
                        if WeaponGlobals.getSkillUnattune(self.skillId):
                            description += ' ' + PLocalizer.UnattuneDesc
                        upgradeInfo = ''
                        if self.showUpgrade and self.skillRank < 5:
                            if self.skillRank > 0:
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
                    if self.skillId in SkillComboReq and SkillComboReq[self.skillId] and self.skillRank <= 1:
                        description += ' ' + SkillComboReq[self.skillId]
                    skillDesc = '\x01gold\x01\x01smallCaps\x01' + skillTitle + '\x02\x02\n' + skillType + description + '\n\x01green\x01' + upgradeInfo + '\x02'
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
                    if buff == WeaponGlobals.C_ATTUNE and baseRank > 1:
                        stats.append(baseRank)
                    if buff == WeaponGlobals.C_WEAKEN:
                        stats.append(WeaponGlobals.WEAKEN_PENALTY * 100)
                    if effect > 0:
                        stats.append(effect)
                    if dodge:
                        stats.append(abs(dodge))
                    if accuracy:
                        stats.append(abs(accuracy))
                    if damageMod:
                        stats.append(abs(damageMod))
                    if reduceDamMod:
                        stats.append(abs(reduceDamMod))
                    if rechargeMod:
                        stats.append(abs(rechargeMod))
                    if shipTurningMod:
                        stats.append(abs(shipTurningMod))
                    if shipSpeedMod:
                        stats.append(abs(shipSpeedMod))
                    if chargeMod:
                        stats.append(abs(chargeMod))
                    if rangeMod:
                        stats.append(abs(rangeMod))
                    if self.skillId == InventoryType.SailTreasureSense:
                        stats.append(abs(treasureSenseMod))
                stats = tuple(stats)
                if self.skillRank:
                    self.rankText = DirectFrame(parent=self, relief=None, text=('\x01gold\x01\x01smallCaps\x01' + PLocalizer.Rank + ' %d' + '\x02\x02') % self.skillRank, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleSmall, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=15, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                     1), pos=(0.45,
                                                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                                                              0), textMayChange=1, sortOrder=92, state=DGG.DISABLED)
            self.helpText = DirectFrame(parent=self, relief=None, text=skillDesc % stats, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleSmall, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=15, text_shadow=(0,
                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                    1), textMayChange=1, sortOrder=91, state=DGG.DISABLED)
            height = -(self.helpText.getHeight() + 0.01)
            self.helpBox = BorderFrame(parent=self, frameSize=(-0.04, 0.5, height, 0.05), pos=(0, 0, -0.12), sortOrder=90, state=DGG.DISABLED)
            self.helpBox.setBin('gui-popup', 0)
            self.helpText.reparentTo(self.helpBox)
            if self.skillRank:
                self.rankText.reparentTo(self.helpBox)
        return

    def destroy(self):
        if self.quantity:
            self.quantity.destroy()
            self.quantity = None
        self.ignoreAll()
        DirectButton.destroy(self)
        return

    def showDetails(self, event):
        self.createHelpbox()

    def hideDetails(self, event):
        if self.helpBox:
            self.helpBox.destroy()
            self.helpBox = None
        return

    def attachQuantity(self, quantity):
        if self.quantity:
            self.quantity['text'] = 'x%s' % quantity
        else:
            self.quantity = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text='x%s' % quantity, frameColor=(0,
                                                                                                                         0,
                                                                                                                         0,
                                                                                                                         1), frameSize=(-0.01, 0.02, -0.01, 0.025), text_scale=0.0275, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.03,
                                                                                                                                                                                                                                                                                                                        0.0,
                                                                                                                                                                                                                                                                                                                        0.03), text_font=PiratesGlobals.getPirateBoldOutlineFont())
        return