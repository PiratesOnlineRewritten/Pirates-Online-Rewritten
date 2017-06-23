from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui.PDialog import PDialog
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiButton
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.reputation import ReputationGlobals
TextDict = {PiratesGuiGlobals.REWARD_PANEL_BLACK_PEARL: {'title': PLocalizer.RewardBlackPearlComplete,'summary': PLocalizer.RewardBlackPearlReward,'description': PLocalizer.RewardBlackPearlDescription,'icon': 'sail_recharge','isWeapon': False},PiratesGuiGlobals.REWARD_PANEL_DOLL: {'title': PLocalizer.RewardVoodooDollComplete,'summary': PLocalizer.RewardVoodooDollReward,'description': PLocalizer.RewardVoodooDollDescription,'icon': 'pir_t_ico_dol_spirit_a','isWeapon': True},PiratesGuiGlobals.REWARD_PANEL_DAGGER: {'title': PLocalizer.RewardDaggerComplete,'summary': PLocalizer.RewardDaggerReward,'description': PLocalizer.RewardDaggerDescription,'icon': 'pir_t_ico_knf_small','isWeapon': True},PiratesGuiGlobals.REWARD_PANEL_STAFF: {'title': PLocalizer.RewardVoodooStaffComplete,'summary': PLocalizer.RewardVoodooStaffReward,'description': PLocalizer.RewardVoodooStaffDescription,'icon': 'pir_t_ico_stf_dark_a','isWeapon': True},PiratesGuiGlobals.REWARD_PANEL_GRENADE: {'title': PLocalizer.RewardGrenadeComplete,'summary': PLocalizer.RewardGrenadeReward,'description': PLocalizer.RewardGrenadeDescription,'icon': 'pir_t_ico_bom_grenade','isWeapon': True},PiratesGuiGlobals.REWARD_PANEL_RAVENS_COVE_A: {'title': PLocalizer.RewardRavensCoveComplete,'summary': PLocalizer.RewardRavensCoveRewardA,'description': PLocalizer.RewardRavensCoveDescription,'icon': 'pir_t_ico_swd_davyJones_g','isWeapon': True},PiratesGuiGlobals.REWARD_PANEL_RAVENS_COVE_B: {'title': PLocalizer.RewardRavensCoveComplete,'summary': PLocalizer.RewardRavensCoveRewardB,'description': PLocalizer.RewardRavensCoveDescription,'icon': 'pir_t_ico_swd_davyJones_a','isWeapon': True},PiratesGuiGlobals.REWARD_PANEL_RAVENS_COVE_C: {'title': PLocalizer.RewardRavensCoveComplete,'summary': PLocalizer.RewardRavensCoveRewardC,'description': PLocalizer.RewardRavensCoveDescription,'icon': 'pir_t_ico_swd_davyJones_e','isWeapon': True}}

class RewardPanel(PDialog):

    def __init__(self, parent=None, type=PiratesGuiGlobals.REWARD_PANEL_BLACK_PEARL, doneCallback=None, **kw):
        optiondefs = (('pad', (0.55, 0.475), self.resetFrameSize), ('pos', (0.4, 0, 0), None))
        self.defineoptions(kw, optiondefs)
        PDialog.__init__(self, parent)
        self.type = type
        if doneCallback:
            self.doneCallback = doneCallback
        else:
            self.doneCallback = self.cleanup
        self.showWeaponsTrack = None
        skillIcons = loader.loadModel('models/textureCards/skillIcons')
        weaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        isWeapon = TextDict[type]['isWeapon']
        if isWeapon:
            background = skillIcons.find('**/box_base_over')
            background.setTransparency(0.5)
            icon = weaponIcons.find('**/' + TextDict[type]['icon'])
            icon.setScale(0.75)
        else:
            background = skillIcons.find('**/base_over')
            icon = skillIcons.find('**/' + TextDict[type]['icon'])
        icon.reparentTo(background)
        self.congratsText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, textMayChange=1, text=PLocalizer.RewardCongratulations, text_font=PiratesGlobals.getInterfaceOutlineFont(), text_align=TextNode.ACenter, text_scale=0.12, text_fg=PiratesGuiGlobals.TextFG1, pos=(0.0,
                                                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                                                        0.34))
        self.completeText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, textMayChange=1, text=TextDict[type]['title'], text_font=PiratesGlobals.getInterfaceOutlineFont(), text_align=TextNode.ACenter, text_scale=0.05, text_fg=PiratesGuiGlobals.TextFG2, pos=(0,
                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                               0.26))
        self.iconLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, geom=background, geom_scale=0.3, text=TextDict[type]['summary'], text_font=PiratesGlobals.getInterfaceFont(), text_align=TextNode.ACenter, text_scale=0.04, text_fg=PiratesGuiGlobals.TextFG1, text_pos=(0,
                                                                                                                                                                                                                                                                                            0.2), pos=(0,
                                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                                       -0.03))
        self.descriptionText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, textMayChange=1, text=TextDict[type]['description'], text_font=PiratesGlobals.getInterfaceFont(), text_align=TextNode.ACenter, text_scale=0.038, text_fg=PiratesGuiGlobals.TextFG1, pos=(0,
                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                  -0.26))
        self.nextButton = GuiButton.GuiButton(parent=self, state=DGG.NORMAL, text=PLocalizer.lOk, textMayChange=1, text_scale=PiratesGuiGlobals.TextScaleMed, text_pos=(0, -0.01), pos=(0,
                                                                                                                                                                                        0,
                                                                                                                                                                                        -0.5), command=self.doneCallback)
        self.borderFrame['borderScale'] = 1
        self.setupCustomReward()
        self.initialiseoptions(RewardPanel)
        self.setScale(1.25)
        return

    def destroy(self):
        if self.showWeaponsTrack:
            self.showWeaponsTrack.pause()
            self.showWeaponsTrack = None
        PDialog.destroy(self)
        return

    def showPageTwo(self):
        self.nextButton['text'] = PLocalizer.lOk
        self.nextButton['command'] = self.doneCallback
        self.nextButton.hide()
        self.iconLabel.hide()
        self.descriptionText.hide()
        self.congratsText.hide()
        self.completeText.hide()
        self.showWeaponNotoriety()

    def showWeaponNotoriety(self):
        totalReputation = 0
        inv = localAvatar.getInventory()
        level = localAvatar.getLevel()
        maxLevel = ReputationGlobals.GlobalLevelCap
        if level < maxLevel:
            textStr = PLocalizer.RewardNotorietyLessThanMax % (level, maxLevel)
            textScale = 0.05
            labelY = 0.37
            buttonY = 0.1
        else:
            textStr = PLocalizer.RewardNotorietyAtMax % maxLevel
            textScale = 0.04
            self.congratsText.show()
            labelY = 0.25
            buttonY = 0.13
        self.notorietyText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, textMayChange=1, text=textStr, text_font=PiratesGlobals.getInterfaceOutlineFont(), text_align=TextNode.ACenter, text_scale=textScale, text_fg=PiratesGuiGlobals.TextFG1, pos=(0, 0, labelY))
        self.notorietyText.hide()
        if level < maxLevel:
            self.todoText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, textMayChange=1, text=PLocalizer.RewardTodo, text_font=PiratesGlobals.getInterfaceOutlineFont(), text_align=TextNode.ACenter, text_scale=0.035, text_fg=PiratesGuiGlobals.TextFG1, pos=(0,
                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                              0.19))
            self.todoText.hide()
        else:
            self.stayTunedText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, textMayChange=1, text=PLocalizer.RewardStayTuned, text_font=PiratesGlobals.getInterfaceOutlineFont(), text_align=TextNode.ACenter, text_scale=0.035, text_fg=PiratesGuiGlobals.TextFG1, pos=(0, 0, -0.41))
            self.stayTunedText.hide()
        weapons = [
         [
          InventoryType.CutlassToken, InventoryType.CutlassRep], [InventoryType.PistolToken, InventoryType.PistolRep], [InventoryType.DaggerToken, InventoryType.DaggerRep], [InventoryType.GrenadeToken, InventoryType.GrenadeRep], [InventoryType.WandToken, InventoryType.WandRep], [InventoryType.DollToken, InventoryType.DollRep], [InventoryType.NewPlayerToken, InventoryType.CannonRep], [InventoryType.NewPlayerToken, InventoryType.SailingRep]]
        maxRep = ReputationGlobals.getTotalReputation(InventoryType.GeneralRep, ReputationGlobals.LevelCap)
        self.guiElements = []
        i = 0
        for weaponToken, weaponId in weapons:
            weaponUnlocked = False
            levelText = PLocalizer.RewardLevelLocked
            state = 0
            if inv.getStackQuantity(weaponToken):
                weaponUnlocked = True
            if weaponUnlocked:
                rep = inv.getReputation(weaponId)
                wlevel, value = ReputationGlobals.getLevelFromTotalReputation(weaponId, rep)
                levelText = PLocalizer.RewardLevelOfMax % (wlevel, ReputationGlobals.LevelCap)
                if rep >= maxRep:
                    levelText = PLocalizer.RepCapText_Skill
                    state = 1
            cb = self.makeCheckbox((0, 0, buttonY - 0.065 * i), PLocalizer.InventoryTypeNames[weaponId], None, state, [3], levelText)
            cb['indicatorValue'] = state
            cb.hide()
            self.guiElements.append(cb)
            i += 1

        self.showWeaponsTrack = Sequence()
        self.showWeaponsTrack.append(Sequence(Func(self.notorietyText.show), Wait(1)))
        if level < maxLevel:
            self.showWeaponsTrack.append(Sequence(Func(self.todoText.show), Wait(1)))
        for b in self.guiElements:
            self.showWeaponsTrack.append(Sequence(Func(b.show), Wait(0.5)))

        if level >= maxLevel:
            self.showWeaponsTrack.append(Sequence(Func(self.stayTunedText.show), Wait(1)))
        self.showWeaponsTrack.append(Func(self.nextButton.show))
        self.showWeaponsTrack.start()
        return

    def setupCustomReward(self):
        self.nextButton['text'] = PLocalizer.lNext
        self.nextButton['command'] = self.showPageTwo

    def makeCheckbox(self, pos, text, command, initialState, extraArgs, levelText):
        charGui = loader.loadModel('models/gui/toplevel_gui')
        buttonImage = (charGui.find('**/generic_button'), charGui.find('**/generic_button'), charGui.find('**/generic_button'), charGui.find('**/generic_button'))
        geomCheck = [
         charGui.find('**/generic_check'), charGui.find('**/generic_check'), charGui.find('**/generic_check'), None]
        c = DirectCheckButton(parent=self, relief=None, scale=0.064, boxBorder=0.08, boxRelief=None, boxImage=geomCheck, boxImageScale=6, boxImageColor=VBase4(0, 1, 0, 1), pos=pos, text=text, text_fg=PiratesGuiGlobals.TextFG1, text_scale=0.5, text_pos=(-2.4,
                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                             -2.8), text_align=TextNode.ALeft, text_font=PiratesGlobals.getInterfaceOutlineFont(), indicator_pos=(2.2,
                                                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                                                  0.15), command=command, indicatorValue=initialState, extraArgs=extraArgs, text0_fg=PiratesGuiGlobals.TextFG1, text1_fg=PiratesGuiGlobals.TextFG1, text2_fg=PiratesGuiGlobals.TextFG1, text3_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, image=buttonImage, image_pos=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    0.15), image_scale=(6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        1,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        2.45), state=DGG.DISABLED)
        l = DirectLabel(parent=c, text=levelText, text_font=PiratesGlobals.getInterfaceFont(), text_scale=0.5, text_align=TextNode.ALeft, frameColor=(0.8,
                                                                                                                                                      0.7,
                                                                                                                                                      0.5,
                                                                                                                                                      1), pos=(-0.3,
                                                                                                                                                               0,
                                                                                                                                                               0))
        c.setIndicatorValue()
        del charGui
        return c