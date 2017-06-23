from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PLocalizer, PiratesGlobals
from direct.interval.IntervalGlobal import *
from pirates.battle import CannonGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import DialogButton
import string

class NewTutorialPanel(GuiPanel.GuiPanel):
    STAGE_TO_EVENTS = {'exitCannon': 'cannonExited','drawSword': 'weaponEquipped','attackSword': 'properHit','comboSword': 'didSlash','cutlassLvl': 'seachestOpened','cutlassSkillOpen': 'skillPanelOpened','cutlassSkillUnlock': 'skillImprovementAttempted','cutlassDoneLvl': 'closePointSpendPanel','compassActiveQuest': 'closeCompassActiveQuest','compassIconsBearing': 'closeCompassIconsBearing','compassIconsPeople': 'closeCompassIconsPeople','specialMenu': 'usedSpecialAttack','specialUse': 'usedSpecialAttack','sheatheSword': 'weaponSheathed','questPageOpen': 'questPageOpened','questPageClose': 'seachestClosed','seachestOpen': 'seachestOpened','pistolAim': 'pistolMoved','pistolTarget': 'pistolAimedTarget','pistolHit': 'pistolHitTarget','pistolPractice': 'weaponSheathed','lookoutChestOpen': 'seachestOpened','lookoutOpen': 'lookoutOpened','lookoutClose': 'lookoutClosed'}
    DIMENSION_TO_EVENTS = {'seachestOpen': (1.25, 0.25, 0.2, 0, 0.2),'questPageOpen': (1.25, 0.25, 0.2, 0, 0.2),'questPageClose': (1.25, 0.25, 0.2, 0, 0.2),'boardShip': (1.25, 0.25, 0.2, 0, 0.2),'useCannon': (1.25, 0.25, 0.2, 0, 1.4),'moveCannon': (1.25, 0.25, 0.2, 0, 1.4),'fireCannon': (1.25, 0.25, 0.2, 0, 1.4),'exitCannon': (1.25, 0.25, 0.2, 0, 1.4),'leaveJail': (1.25, 0.25, 0.2, 0, 0.2),'showBlacksmith': (1.27, 0.25, 0.2, 0, 0.2),'doCutlassTutorial': (1.25, 0.25, 0.2, 0, 1.2),'drawSword': (1.25, 0.25, 0.2, 0, 1.2),'attackSword': (1.25, 0.25, 0.2, 0, 1.2),'comboSword': (1.25, 0.25, 0.2, 0, 1.2),'bonusSword': (1.25, 0.25, 0.2, 0, 1.2),'cutlassLvl': (1.25, 0.25, 0.2, 0, 0.25),'cutlassSkillOpen': (1.25, 0.25, 0.2, 0, 0.25),'cutlassSkillUnlock': (1.25, 0.25, 0.2, 0, 0.25),'cutlassDoneLvl': (1.25, 0.25, 0.2, 0, 0.25),'specialMenu': (1.25, 0.25, 0.2, 0, 1.2),'skillLearning': (1.27, 0.25, 0.2, 0, 1.2),'sheatheSword': (1.25, 0.25, 0.2, 0, 1.2),'showSkeleton': (1.27, 0.25, 0.2, 0, 0.2),'showJungleTia': (1.25, 0.25, 0.2, 0, 0.2),'receiveCompass': (1.25, 0.25, 0.2, 0, 0.2),'compassActiveQuest': (1.25, 0.25, 0.2, 0, 1.2),'compassIconsBearing': (1.25, 0.25, 0.2, 0, 1.2),'compassIconsPeople': (1.25, 0.25, 0.2, 0, 1.2),'showNavy': (1.25, 0.25, 0.2, 0, 0.2),'showGovMansion': (1.25, 0.25, 0.2, 0, 0.2),'showDarby': (1.25, 0.25, 0.2, 0, 0.2),'showDinghy': (1.25, 0.25, 0.2, 0, 0.2),'showBarbossa': (1.25, 0.25, 0.2, 0, 0.2),'pistolAim': (1.25, 0.25, 0.2, 0, 0.25),'pistolTarget': (1.25, 0.25, 0.2, 0, 0.25),'pistolHit': (1.25, 0.25, 0.2, 0, 0.25),'pistolPractice': (1.25, 0.25, 0.2, 0, 0.25),'learnLookout': (1.25, 0.25, 0.2, 0, 0.2),'lookoutChestOpen': (1.25, 0.25, 0.2, 0, 0.2),'lookoutOpen': (1.25, 0.25, 0.2, 0, 0.2),'lookoutClose': (1.25, 0.25, 0.2, 0, 0.2),'showTortugaJack': (1.25, 0.25, 0.2, 0, 0.2),'teleport_tut1': (1.25, 0.25, 0.2, 0, 0.2),'teleport_tut2': (1.25, 0.25, 0.2, 0, 0.2),'teleport_tut3': (1.25, 0.25, 0.2, 0, 0.2),'chat_tut1': (1.25, 0.25, 0.2, 0, 1.2),'chat_tut2': (1.25, 0.25, 0.2, 0, 1.2),'chat_tut3': (1.27, 0.25, 0.2, 0, 1.2),'chat_tut4': (1.27, 0.25, 0.2, 0, 0.2),'chat_tut5': (1.27, 0.25, 0.2, 0, 0.2),'chat_tut6': (1.25, 0.25, 0.2, 0, 1.2),'chat_tut7': (1.25, 0.25, 0.2, 0, 1.2),'chat_tut8': (1.25, 0.25, 0.2, 0, 1.2),'chat_tut_alt1': (1.25, 0.25, 0.2, 0, 1.2),'chat_tut_alt2': (1.25, 0.25, 0.2, 0, 1.2),'chat_tut_alt3': (1.25, 0.25, 0.2, 0, 1.2),'chat_tut_alt4': (1.27, 0.25, 0.2, 0, 1.2),'chat_tut_alt5': (1.27, 0.25, 0.2, 0, 0.2),'chat_tut_alt6': (1.27, 0.25, 0.2, 0, 0.2),'chat_tut_alt7': (1.25, 0.25, 0.2, 0, 1.2),'chat_tut_alt8': (1.25, 0.25, 0.2, 0, 1.2)}
    ARROW_TO_EVENTS = {'seachestOpen': (base.a2dBottomRight, -0.25, 0, 0.25, 135),'questPageOpen': (base.a2dBottomRight, -0.225, 0, 0.43, 135),'questPageClose': (base.a2dBottomRight, -0.25, 0, 0.25, 135),'drawSword': (base.a2dBottomRight, -0.675, 0, 0.25, 135),'cutlassLvl': (base.a2dBottomRight, -0.25, 0, 0.25, 135),'cutlassSkillOpen': (base.a2dBottomRight, -0.25, 0, 1.0, 135),'cutlassSkillUnlock': (base.a2dBottomRight, -1.0, 0, 1.05, 135),'cutlassDoneLvl': (base.a2dBottomRight, -0.25, 0, 0.25, 135),'specialMenu': (base.a2dBottomCenter, -0.425, 0, 0.325, 135),'chat_tut1': (base.a2dBottomLeft, 0.4, 0, 0.2, 225),'chat_tut2': (base.a2dBottomLeft, 0.5, 0, 0.2, 225),'chat_tut5': (base.a2dBottomLeft, 1.45, 0, 1.55, 225),'chat_tut_alt2': (base.a2dBottomLeft, 0.3, 0, 0.2, 225),'chat_tut_alt6': (base.a2dBottomLeft, 1.45, 0, 1.55, 225),'lookoutChestOpen': (base.a2dBottomRight, -0.225, 0, 0.25, 135),'lookoutOpen': (base.a2dBottomRight, -0.225, 0, 0.545, 135),'lookoutClose': (base.a2dBottomRight, -0.25, 0, 0.25, 135)}
    ICON_TO_EVENTS = {'seachestOpen': ('models/gui/toplevel_gui', 'treasure_chest_closed', 0.17),'questPageOpen': ('models/gui/toplevel_gui', 'topgui_icon_journal', 0.286),'questPageClose': ('models/gui/toplevel_gui', 'treasure_chest_open', 0.17),'moveCannon': ('models/gui/toplevel_gui', 'icon_mouse_right', 0.17),'fireCannon': ('models/gui/toplevel_gui', 'icon_mouse_left', 0.17),'showBlacksmith': ('models/gui/toplevel_gui', 'icon_warehouse', 0.225),'doCutlassTutorial': ('models/gui/gui_icons_weapon', 'pir_t_ico_swd_cutlass_a', 0.17),'drawSword': ('models/gui/gui_icons_weapon', 'pir_t_ico_swd_cutlass_a', 0.17),'attackSword': ('models/gui/toplevel_gui', 'icon_mouse_left', 0.17),'comboSword': ('models/gui/toplevel_gui', 'icon_mouse_double_left', 0.285),'bonusSword': ('models/gui/toplevel_gui', 'icon_mouse_double_left', 0.285),'cutlassLvl': ('models/gui/toplevel_gui', 'treasure_chest_closed', 0.17),'cutlassSkillOpen': ('models/gui/toplevel_gui', 'topgui_icon_skills', 0.17),'cutlassSkillUnlock': ('models/textureCards/skillIcons', 'tutorial_sweep', 0.1),'cutlassDoneLvl': ('models/gui/toplevel_gui', 'treasure_chest_open', 0.17),'specialMenu': ('models/textureCards/skillIcons', 'tutorial_sweep', 0.1),'skillLearning': ('models/gui/toplevel_gui', 'topgui_icon_skills', 0.17),'showSkeleton': ('models/gui/toplevel_gui', 'icon_grave_yard', 0.225),'showJungleTia': ('models/gui/toplevel_gui', 'icon_jungle_entrance', 0.225),'receiveCompass': ('models/gui/toplevel_gui', 'compass_small_button_open', 0.25),'compassActiveQuest': ('models/gui/toplevel_gui', 'compass_small_button_open', 0.25),'compassIconsBearing': ('models/gui/toplevel_gui', 'compass_small_button_open', 0.25),'compassIconsPeople': ('models/gui/toplevel_gui', 'compass_small_button_open', 0.25),'showNavy': ('models/gui/toplevel_gui', 'icon_navy', 0.225),'showGovMansion': ('models/gui/toplevel_gui', 'icon_gov_mansion', 0.225),'showDarby': ('models/gui/toplevel_gui', 'icon_darby', 0.225),'showDinghy': ('models/gui/toplevel_gui', 'icon_dinghy', 0.225),'showBarbossa': ('models/gui/toplevel_gui', 'icon_cave_entrance', 0.225),'chat_tut1': ('models/gui/triangle', 'triangle_over', 0.085),'chat_tut2': ('models/gui/triangle', 'triangle_over', 0.085),'chat_tut3': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'chat_tut4': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'chat_tut5': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'chat_tut6': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'chat_tut7': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'chat_tut8': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'chat_tut_alt2': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'chat_tut_alt4': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'chat_tut_alt5': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'chat_tut_alt6': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'chat_tut_alt7': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'chat_tut_alt8': ('models/gui/chat_frame_skull', 'chat_frame_skull_over', 0.3),'pistolAim': ('models/gui/toplevel_gui', 'icon_mouse_right', 0.17),'pistolHit': ('models/gui/toplevel_gui', 'icon_mouse_left', 0.17),'learnLookout': ('models/gui/toplevel_gui', 'telescope_button', 0.225),'lookoutChestOpen': ('models/gui/toplevel_gui', 'treasure_chest_closed', 0.17),'lookoutOpen': ('models/gui/toplevel_gui', 'telescope_button', 0.225),'lookoutClose': ('models/gui/toplevel_gui', 'treasure_chest_open', 0.17),'showTortugaJack': ('models/gui/toplevel_gui', 'icon_faithful_bride', 0.225)}
    IVALS_TO_EVENTS = {'compassActiveQuest': True,'compassIconsBearing': True,'compassIconsPeople': True}

    def __init__(self, tutorialList, ignoreEscape=True, title=None):
        mode = tutorialList[0]
        aspectRatio = 1.32
        showClose = False
        self.closeMessage = self.STAGE_TO_EVENTS.get(mode, 'closeTutorialWindow')
        self.closeMessageCatchall = 'closeTutorialWindowAll'
        self.mode = mode
        width, height, x, y, z = self.DIMENSION_TO_EVENTS.get(mode, (PiratesGuiGlobals.TutorialPanelWidth, PiratesGuiGlobals.TutorialPanelHeight, 0.03, 0, 1.0))
        GuiPanel.GuiPanel.__init__(self, '', width * aspectRatio, height * aspectRatio, showClose, modelName='general_frame_e', borderScale=0.4, bgBuffer=0.15)
        self.initialiseoptions(NewTutorialPanel)
        self.reparentTo(base.a2dBottomLeft)
        self.setPos(x, y, z)
        self.setBin('gui-popup', 0)
        iconFile, iconName, iconScale = self.ICON_TO_EVENTS.get(self.mode, ('models/gui/toplevel_gui',
                                                                            'not_defined',
                                                                            0.17))
        guiFile = loader.loadModel(iconFile)
        flip = 0
        if iconName == 'icon_mouse_right':
            iconName = 'icon_mouse_left'
            flip = 1
        if iconName == 'icon_mouse_left':
            iconScale = 0.75
        self.icon = guiFile.find('**/' + iconName)
        if self.icon.isEmpty():
            self.icon = None
        if self.icon:
            self.icon.reparentTo(self)
            self.icon.setPos(0.17, 0, 0.12 * aspectRatio)
            self.icon.setScale(iconScale * aspectRatio)
            if flip:
                self.icon.setHpr(180, 0, 0)
            textXOffset = 0.3
        else:
            textXOffset = 0.1
        arrowParent, ax, ay, az, ar = self.ARROW_TO_EVENTS.get(self.mode, (None, 0,
                                                                           0, 0,
                                                                           135))
        if arrowParent:
            self.arrow = loader.loadModel('models/gui/arrow_with_halo')
            if self.arrow.isEmpty():
                self.arrow = loader.loadModel('models/gui/compass_arrow')
            self.arrow.setBin('gui-popup', 0)
            arrowScale = 0.75
            self.arrow.reparentTo(arrowParent)
            self.arrow.setPos(ax, ay, az)
            self.arrow.setScale(arrowScale)
            self.arrow.setR(ar)
            self.arrow.hide()
        else:
            self.arrow = None
        self.openSfx = None
        self.showPanelIval = None
        self.createShowPanelIval()
        undefText = 'undefined text'
        if base.config.GetBool('want-easy-combos', 1) and PLocalizer.TutorialPanelDialogEasyCombo.get(mode):
            text = PLocalizer.TutorialPanelDialogEasyCombo.get(mode)
        else:
            text = PLocalizer.TutorialPanelDialog.get(mode, undefText)
        loc = string.find(text, '[')
        start = 0
        title = None
        if loc >= 0:
            loc2 = string.find(text, ']')
            start = loc2 + 1
            title = text[loc + 1:loc2]
        listLen = len(tutorialList)
        self.yesTutorial = self.noTutorial = None
        buttonPos = (
         0.6 + textXOffset, 0, 0.11)
        yesButtonText = PLocalizer.lOk
        if listLen > 3:
            self.wreckHitButton = []
            for addText in tutorialList[1:3]:
                localText = PLocalizer.TutorialPanelDialog.get(addText, undefText)
                if localText != undefText:
                    text += localText
                else:
                    text += addText

            self.modifyText = text
        else:
            if listLen >= 3:
                buttonPos = (
                 0.7 + textXOffset, 0, 0.11)
                self.noTutorial = DialogButton.DialogButton(self, text=PLocalizer.lNo, buttonStyle=DialogButton.DialogButton.NO, pos=buttonPos)
                buttonPos = (
                 0.4 + textXOffset, 0, 0.11)
                yesButtonText = PLocalizer.lYes
            if listLen >= 2:
                self.yesTutorial = DialogButton.DialogButton(self, text=yesButtonText, buttonStyle=DialogButton.DialogButton.YES, pos=buttonPos)
        self.createTextIcons()
        yOffsetFudge = 0.0
        ratio = width / height
        if ratio >= 5:
            wordWrap = 25
        else:
            if ratio >= 2:
                wordWrap = 12
            else:
                wordWrap = 8
                yOffsetFudge = 0.05
            lenText = len(text)
            possibleNumLines = int(lenText / wordWrap)
            if title:
                textYOffset = (height + yOffsetFudge) / 1.5 * aspectRatio
                self.titleText = DirectLabel(parent=self, relief=None, text=title, text_scale=PiratesGuiGlobals.TextScaleLarge * aspectRatio, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(textXOffset, 0, textYOffset))
            else:
                self.titleText = None
                textYOffset = (height + yOffsetFudge) / 1.5 * aspectRatio
            self.helpText = DirectLabel(parent=self, relief=None, text=text[start:len(text)], text_scale=PiratesGuiGlobals.TextScaleLarge * aspectRatio, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG8, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=wordWrap, pos=(textXOffset, 0, textYOffset))
            if ignoreEscape:
                self.ignore('escape')
        self.hide()
        base.ntp = self
        return

    def createTextIcons(self):
        tpMgr = TextPropertiesManager.getGlobalPtr()
        if not tpMgr.hasGraphic('cutlassEquip'):
            topGui = loader.loadModel('models/gui/toplevel_gui')
            triangleGui = loader.loadModel('models/gui/triangle')
            skullGui = loader.loadModel('models/gui/chat_frame_skull')
            kbButton = topGui.find('**/keyboard_button')
            nomButton = topGui.find('**/icon_mouse')
            lmButton = topGui.find('**/icon_mouse_left')
            lmButton.setScale(4)
            csButton = skullGui.find('**/*skull')
            caButton = triangleGui.find('**/triangle')
            rmButton = topGui.find('**/icon_mouse_left')
            rmButton.setScale(4)
            rmButton.setHpr(180, 0, 0)
            jnButton = topGui.find('**/topgui_icon_journal')
            skButton = topGui.find('**/topgui_icon_skills')
            chestClosedButton = topGui.find('**/treasure_chest_closed')
            chestOpenButton = topGui.find('**/treasure_chest_open')
            cm = CardMaker('cm')
            tabCardRoot = NodePath('tabCardRoot')
            tabCard = kbButton.copyTo(kbButton)
            tabCard.setScale(2.0, 1, 1)
            tabCard.reparentTo(tabCardRoot)
            ctrlCardRoot = NodePath('ctrlCardRoot')
            ctrlCard = kbButton.copyTo(kbButton)
            ctrlCard.setScale(2.0, 1, 1)
            ctrlCard.reparentTo(ctrlCardRoot)
            shiftCardRoot = NodePath('shiftCardRoot')
            shiftCard = kbButton.copyTo(kbButton)
            shiftCard.setScale(2.2, 1, 1)
            shiftCard.reparentTo(shiftCardRoot)
            escapeCardRoot = NodePath('escapeCardRoot')
            escapeCard = kbButton.copyTo(kbButton)
            escapeCard.setScale(2.0, 1, 1)
            escapeCard.reparentTo(escapeCardRoot)
            oneCardRoot = NodePath('oneCardRoot')
            oneCard = kbButton.copyTo(kbButton)
            oneCard.reparentTo(oneCardRoot)
            questPageCard = kbButton.copyTo(kbButton)
            questPageCard.setScale(1.2)
            skillPageCardRoot = NodePath('skillCardRoot')
            skillPageCard = skButton.copyTo(skButton)
            skillPageCard.setScale(3.0)
            skillPageCard.setPos(0, 0, -0.1)
            skillPageCard.reparentTo(skillPageCardRoot)
            weapon1Card = kbButton.copyTo(kbButton)
            weapon2Card = kbButton.copyTo(kbButton)
            lookoutCard = kbButton.copyTo(kbButton)
            mouseCard = nomButton.copyTo(nomButton)
            mouseCard.setScale(2)
            leftClickCard = lmButton.copyTo(lmButton)
            leftClickCard.setScale(2)
            chatSkullCard = csButton.copyTo(csButton)
            chatSkullCard.setScale(5)
            chatArrowCard = caButton.copyTo(caButton)
            rightClickCard = rmButton.copyTo(rmButton)
            rightClickCard.setScale(2)
            moveCard = kbButton.copyTo(kbButton)
            skillCardRoot = NodePath('skillCardRoot')
            skillGui = loader.loadModel('models/textureCards/skillIcons.bam')
            sweep = skillGui.findTexture('tutorial_sweep')
            skillCard = NodePath(cm.generate())
            skillCard.setTexture(sweep)
            skillCard.setTransparency(TransparencyAttrib.MAlpha)
            skillCard.setScale(1.5)
            skillCard.setPos(0.0, 0, -2)
            skillCard.reparentTo(skillCardRoot)
            chestClosedCard = chestClosedButton.copyTo(chestClosedButton)
            chestClosedCard.setScale(5)
            chestOpenCard = chestOpenButton.copyTo(chestOpenButton)
            chestOpenCard.setScale(5)
            journalCardRoot = NodePath('journalCardRoot')
            journalCard = jnButton.copyTo(jnButton)
            journalCard.setScale(4)
            journalCard.reparentTo(journalCardRoot)
            tabText = DirectLabel(parent=tabCardRoot, relief=None, text=PLocalizer.TabKey, text_scale=1.0, text_align=TextNode.ACenter, text_fg=(0,
                                                                                                                                                 0,
                                                                                                                                                 0,
                                                                                                                                                 1), text_wordwrap=12, pos=(0.0, 0.0, -0.15))
            ctrlText = DirectLabel(parent=ctrlCardRoot, relief=None, text=PLocalizer.CtrlKey, text_scale=1.0, text_align=TextNode.ACenter, text_fg=(0,
                                                                                                                                                    0,
                                                                                                                                                    0,
                                                                                                                                                    1), text_wordwrap=12, pos=(0.0, 0.0, -0.15))
            shiftText = DirectLabel(parent=shiftCardRoot, relief=None, text=PLocalizer.ShiftKey, text_scale=1.0, text_align=TextNode.ACenter, text_fg=(0,
                                                                                                                                                       0,
                                                                                                                                                       0,
                                                                                                                                                       1), text_wordwrap=12, pos=(0.0, 0.0, -0.15))
            escapeText = DirectLabel(parent=escapeCardRoot, relief=None, text=PLocalizer.EscapeKey, text_scale=1.0, text_align=TextNode.ACenter, text_fg=(0,
                                                                                                                                                          0,
                                                                                                                                                          0,
                                                                                                                                                          1), text_wordwrap=12, pos=(0.0, 0.0, -0.15))
            oneText = DirectLabel(parent=oneCardRoot, relief=None, text=PLocalizer.OneKey, text_scale=1.0, text_align=TextNode.ACenter, text_fg=(0,
                                                                                                                                                 0,
                                                                                                                                                 0,
                                                                                                                                                 1), text_wordwrap=12, pos=(0.0, 0.0, -0.15))
            questPageText = DirectLabel(parent=questPageCard, relief=None, text=PLocalizer.QuestPageKey, text_scale=0.9, text_align=TextNode.ACenter, text_font=PiratesGlobals.getPirateFont(), text_fg=(0,
                                                                                                                                                                                                         0,
                                                                                                                                                                                                         0,
                                                                                                                                                                                                         1), text_wordwrap=12, pos=(0.0, 0, -0.05))
            weapon1Text = DirectLabel(parent=weapon1Card, relief=None, text=PLocalizer.WeaponSlot1, text_scale=0.9, text_align=TextNode.ACenter, text_fg=(0,
                                                                                                                                                          0,
                                                                                                                                                          0,
                                                                                                                                                          1), text_wordwrap=12, pos=(0.0, 0, -0.15))
            weapon2Text = DirectLabel(parent=weapon2Card, relief=None, text=PLocalizer.WeaponSlot2, text_scale=0.9, text_align=TextNode.ACenter, text_fg=(0,
                                                                                                                                                          0,
                                                                                                                                                          0,
                                                                                                                                                          1), text_wordwrap=12, pos=(0.0, 0, -0.15))
            lookoutText = DirectLabel(parent=lookoutCard, relief=None, text=PLocalizer.LookoutPageKey, text_scale=0.9, text_align=TextNode.ACenter, text_fg=(0,
                                                                                                                                                             0,
                                                                                                                                                             0,
                                                                                                                                                             1), text_wordwrap=12, pos=(0.0, 0, -0.15))
            moveText = DirectLabel(parent=moveCard, relief=None, text=PLocalizer.ForwardMoveKey, text_scale=0.9, text_align=TextNode.ACenter, text_fg=(0,
                                                                                                                                                       0,
                                                                                                                                                       0,
                                                                                                                                                       1), text_wordwrap=12, pos=(0.0, 0, -0.15))
            tpMgr.setGraphic('tabButton', tabCardRoot)
            tpMgr.setGraphic('ctrlButton', ctrlCardRoot)
            tpMgr.setGraphic('shiftButton', shiftCardRoot)
            tpMgr.setGraphic('escapeButton', escapeCardRoot)
            tpMgr.setGraphic('oneButton', oneCardRoot)
            tpMgr.setGraphic('chestClosedButton', chestClosedCard)
            tpMgr.setGraphic('chestOpenButton', chestOpenCard)
            tpMgr.setGraphic('questPageButton', questPageCard)
            tpMgr.setGraphic('skillPageButton', skillPageCardRoot)
            tpMgr.setGraphic('journalButton', journalCardRoot)
            tpMgr.setGraphic('cutlassEquip', weapon1Card)
            tpMgr.setGraphic('pistolEquip', weapon2Card)
            tpMgr.setGraphic('mouseIcon', mouseCard)
            tpMgr.setGraphic('leftClick', leftClickCard)
            tpMgr.setGraphic('rightClick', rightClickCard)
            tpMgr.setGraphic('moveKeys', moveCard)
            tpMgr.setGraphic('skillKey', skillCardRoot)
            tpMgr.setGraphic('lookoutKey', lookoutCard)
            tpMgr.setGraphic('chatSkull', chatSkullCard)
            tpMgr.setGraphic('chatArrow', chatArrowCard)
        return

    def activate(self):
        if self.isEmpty():
            return
        base.tPanel = self
        self.showPanel()
        if self.closeMessage:
            self.accept(self.closeMessage, self.destroy)
        if self.closeMessageCatchall:
            self.accept(self.closeMessageCatchall, self.destroy)
        if self.mode == 'compassIconsPeople':
            localAvatar.guiMgr.radarGui.getRadarAvatarObject().setColorScale(0, 0, 1, 1)
        self.accept('clientLogout', self.destroy)

    def createShowPanelIval(self):
        self.openSfx = loadSfx(SoundGlobals.SFX_GUI_SHOW_PANEL)
        if self.arrow:
            arrowFunc = Func(self.arrow.show)
            self.arrowIval = Sequence(LerpColorScaleInterval(self.arrow, 1.0, VBase4(1, 1, 1, 0.6), startColorScale=VBase4(1, 1, 1, 1), blendType='easeIn'))
        else:
            arrowFunc = Func(self.show)
        self.showPanelIval = Sequence(Func(self.show), Func(base.playSfx, self.openSfx), arrowFunc, LerpPosInterval(self, 0.5, Point3(self.getX(), self.getY(), self.getZ()), startPos=Point3(-1.0, self.getY(), self.getZ()), blendType='easeOut'))

    def showPanel(self):
        if self.showPanelIval.isPlaying():
            self.showPanelIval.finish()
            if self.arrow:
                self.arrowIval.finish()
        self.showPanelIval.start()
        if self.arrow:
            self.arrowIval.loop()

    def setYesCommand(self, command, extraArgs=[]):
        self.yesTutorial['command'] = command
        self.yesTutorial['extraArgs'] = extraArgs

    def setNoCommand(self, command, extraArgs=[]):
        self.noTutorial['command'] = command
        self.noTutorial['extraArgs'] = extraArgs

    def setWreckButtonText(self, hitCount):
        if hitCount < 1 or hitCount > 3:
            return
        modText = '%s/3' % hitCount
        self.helpText['text'] = self.modifyText + modText

    def destroy(self):
        try:
            self.NewTutorialPanel_destroyed
        except:
            self.NewTutorialPanel_destroyed = 1
            self.ignore('tooFar')
            self.ignore('clientLogout')
            ivalClear = self.IVALS_TO_EVENTS.get(self.mode, False)
            if ivalClear:
                localAvatar.guiMgr.clearIvals()
            if self.showPanelIval:
                self.showPanelIval.pause()
                del self.showPanelIval
                if self.arrow:
                    self.arrowIval.pause()
                    del self.arrowIval
            if self.arrow:
                self.arrow.hide()
                del self.arrow
            if self.closeMessage:
                self.ignore(self.closeMessage)
            if self.closeMessageCatchall:
                self.ignore(self.closeMessageCatchall)
            del self.helpText
            if self.titleText:
                del self.titleText
            if self.openSfx:
                del self.openSfx
            DirectFrame.destroy(self)