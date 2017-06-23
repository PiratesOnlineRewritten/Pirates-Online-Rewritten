from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import GuiTray, QuestPage
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.GuiButton import GuiButton
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class ChestTray(GuiTray.GuiTray):
    WantClothingPage = base.config.GetBool('want-clothing-page', 0)
    WantTitlesPage = base.config.GetBool('want-land-infamy', 0) or base.config.GetBool('want-sea-infamy', 0)

    def __init__(self, parent, parentMgr, **kw):
        GuiTray.GuiTray.__init__(self, parent, 0.6, 0.12, **kw)
        self.initialiseoptions(ChestTray)
        self.setBin('gui-fixed', 0)
        self.state = 0
        self.buttonsParent = self.attachNewNode(ModelNode('ChestTray.buttonsParent'), sort=1)
        self.stickyButtonsParent = self.attachNewNode(ModelNode('ChestTray.stickyButtonsParent'), sort=1)
        self.stickyButtonsParent.setPos(0, 0, 0.02)
        self.buttons = {}
        self.buildShowHideButtonsIvals()
        self.openSfx = loadSfx(SoundGlobals.SFX_GUI_OPEN_SEACHEST)
        self.openSfx.setVolume(0.4)
        self.closeSfx = loadSfx(SoundGlobals.SFX_GUI_CLOSE_SEACHEST)
        self.closeSfx.setVolume(0.4)
        gui = loader.loadModel('models/gui/toplevel_gui')
        gui_main = loader.loadModel('models/gui/gui_main')
        helpPos = (
         -0.26, 0, 0.06)
        helpDelay = 0
        self.buttonImage = gui.find('**/topgui_icon_box')
        self.buttonImageIn = gui.find('**/topgui_icon_box_in')
        self.buttonColors = (
         VBase4(0.7, 0.7, 0.7, 1), VBase4(0.8, 0.8, 0.8, 1), VBase4(1.0, 1.0, 1.0, 1), VBase4(0.6, 0.6, 0.6, 1))
        self.currentButtonIn = None
        self.highlightButtons = ['guiMgrToggleMap', 'guiMgrToggleWeapons', 'guiMgrToggleQuest', 'guiMgrToggleLevels', 'guiMgrToggleShips', 'guiMgrToggleTreasures', 'guiMgrToggleLookout', 'guiMgrToggleInventory', 'guiMgrToggleTitles']
        buttonOptions = {'image': self.buttonImage,'geom': None,'relief': None,'frameSize': (0, 0.12, 0, 0.12),'image_scale': 0.47,'image_pos': (0.06, 0, 0.06),'image0_color': self.buttonColors[0],'image1_color': self.buttonColors[1],'image2_color': self.buttonColors[2],'image3_color': self.buttonColors[3],'geom_scale': 0.12,'geom_pos': (0.06, 0, 0.06),'command': self.togglePanel}
        extraHeight = 0
        if self.WantTitlesPage:
            extraHeight = 0.12
        buttonOptions['geom'] = gui.find('**/friend_button_over')
        buttonOptions['geom_scale'] = 0.12
        self.socialButton = GuiButton(parent=self.buttonsParent, hotkeys=['f', 'shift-f'], hotkeyLabel='F', helpText=PLocalizer.SocialButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleSocial'], pos=(0.01, 0, 1.16 + extraHeight), **buttonOptions)
        self.buttons['guiMgrToggleSocial'] = self.socialButton
        buttonOptions['geom'] = gui.find('**/compass_small_button_open_over')
        buttonOptions['geom_scale'] = 0.09
        self.radarButton = GuiButton(parent=self.buttonsParent, hotkeys=['c', 'shift-c'], hotkeyLabel='C', helpText=PLocalizer.RadarButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleRadar'], pos=(0.01, 0, 1.04 + extraHeight), **buttonOptions)
        self.buttons['guiMgrToggleRadar'] = self.radarButton
        buttonPosZ = 0.88
        buttonHeight = 0.12
        if self.WantTitlesPage:
            buttonPosZ += buttonHeight
        buttonOptions['geom'] = gui_main.find('**/world_map_icon')
        buttonOptions['geom_scale'] = 0.095
        self.mapButton = GuiButton(parent=self.buttonsParent, hotkeys=['m', 'shift-m'], hotkeyLabel='M', helpText=PLocalizer.MapButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleMap'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons['guiMgrToggleMap'] = self.mapButton
        buttonPosZ -= buttonHeight
        self.highlightButton('guiMgrToggleMap')
        buttonOptions['geom'] = (
         gui.find('**/treasure_chest_closed_over'),)
        buttonOptions['geom_scale'] = 0.12
        self.bagButton = GuiButton(parent=self.buttonsParent, hotkeys=['i', 'shift-i'], hotkeyLabel='I', helpText=PLocalizer.SocialButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleInventory'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons['guiMgrToggleInventory'] = self.bagButton
        buttonPosZ -= buttonHeight
        buttonOptions['geom'] = gui.find('**/topgui_icon_weapons')
        buttonOptions['geom_scale'] = 0.18
        self.weaponButton = GuiButton(parent=self.buttonsParent, hotkeys=['y', 'shift-y'], hotkeyLabel='Y', helpText=PLocalizer.WeaponButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleWeapons'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons['guiMgrToggleWeapons'] = self.weaponButton
        buttonPosZ -= buttonHeight
        buttonOptions['geom'] = gui.find('**/topgui_icon_skills')
        buttonOptions['geom_scale'] = 0.18
        self.levelButton = GuiButton(parent=self.buttonsParent, hotkeys=['k', 'shift-k'], hotkeyLabel='K', helpText=PLocalizer.SkillButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleLevels'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons['guiMgrToggleLevels'] = self.levelButton
        buttonPosZ -= buttonHeight
        if self.WantClothingPage:
            buttonOptions['geom'] = gui.find('**/topgui_icon_clothing')
            buttonOptions['geom_scale'] = 0.17
            self.clothingButton = GuiButton(parent=self.buttonsParent, helpText=PLocalizer.ClothingButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleClothing'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
            self.buttons['guiMgrToggleClothing'] = self.clothingButton
            buttonPosZ -= buttonHeight
        if self.WantTitlesPage:
            buttonOptions['geom'] = gui.find('**/topgui_infamy_frame')
            buttonOptions['geom_scale'] = 0.2
            self.titlesButton = GuiButton(parent=self.buttonsParent, hotkeys=['b', 'shift-b'], hotkeyLabel='B', helpText=PLocalizer.TitlesButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleTitles'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
            self.buttons['guiMgrToggleTitles'] = self.titlesButton
            buttonPosZ -= buttonHeight
        buttonOptions['geom'] = gui.find('**/topgui_icon_ship')
        buttonOptions['geom_scale'] = 0.2
        self.shipsButton = GuiButton(parent=self.buttonsParent, hotkeys=['h', 'shift-h'], hotkeyLabel='H', helpText=PLocalizer.ShipsButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleShips'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons['guiMgrToggleShips'] = self.shipsButton
        buttonPosZ -= buttonHeight
        buttonOptions['geom'] = gui.find('**/topgui_icon_journal')
        buttonOptions['geom_scale'] = 0.18
        self.questButton = GuiButton(parent=self.buttonsParent, hotkeys=['j', 'shift-j'], hotkeyLabel='J', helpText=PLocalizer.QuestButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleQuest'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons['guiMgrToggleQuest'] = self.questButton
        buttonPosZ -= buttonHeight
        self.lookoutButtonNormal = gui.find('**/telescope_button')
        self.lookoutButtonLight = gui.find('**/telescope_button_over')
        self.lookoutButtonSearch3o = gui.find('**/lookout_icon_over_03')
        buttonOptions['geom'] = None
        self.lookoutButton = GuiButton(parent=self.buttonsParent, hotkeys=['l', 'shift-l'], hotkeyLabel='L', helpText=PLocalizer.LookoutButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleLookout'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons['guiMgrToggleLookout'] = self.lookoutButton
        buttonPosZ -= buttonHeight
        self.lookoutButtonImage = OnscreenImage(parent=self.stickyButtonsParent, image=self.lookoutButtonLight, scale=0.3, pos=(0.065,
                                                                                                                                0.0,
                                                                                                                                0.215))
        self.lookoutButtonImage.sourceImage = self.lookoutButtonLight
        buttonOptions['geom'] = gui.find('**/topgui_icon_main_menu')
        buttonOptions['geom_scale'] = 0.18
        self.mainMenuButton = GuiButton(parent=self.buttonsParent, hotkeys=[PiratesGlobals.OptionsHotkey, 'escape'], hotkeyLabel='F7', helpText=PLocalizer.QuestButtonHelp, helpPos=helpPos, helpDelay=helpDelay, extraArgs=['guiMgrToggleMainMenu'], pos=(0.01, 0, buttonPosZ), **buttonOptions)
        self.buttons['guiMgrToggleMainMenu'] = self.mainMenuButton
        buttonPosZ -= buttonHeight
        self.chestButtonClosed = (
         gui.find('**/treasure_chest_closed'), gui.find('**/treasure_chest_closed'), gui.find('**/treasure_chest_closed_over'))
        self.chestButtonOpen = gui.find('**/treasure_chest_open_over')
        self.chestButton = GuiButton(command=self.toggle, parent=self, relief=None, image=self.chestButtonClosed, image_scale=0.15, image_pos=(0.05,
                                                                                                                                               0,
                                                                                                                                               0.06), scale=1.2)
        self.chestHotkeyText = DirectLabel(parent=self.chestButton, relief=None, text='Tab', text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(0.11,
                                                                                                                                                                                0.0), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), textMayChange=1)
        self.buttonsParent.hide()
        self.buttonsParent.setPos(0.2, 0, 0.14)
        self.stickyButtonsParent.hide()
        self.stickyButtonsParent.setPos(0.2, 0, 0.14)
        gui.removeNode()
        return

    def destroy(self):
        self.showButtonsIval.pause()
        del self.showButtonsIval
        self.hideButtonsIval.pause()
        del self.hideButtonsIval
        self.buttonsParent.removeNode()
        del self.buttonsParent
        self.stickyButtonsParent.removeNode()
        del self.stickyButtonsParent
        for button in self.buttons:
            self.buttons[button].destroy()
            self.buttons[button] = None

        del self.buttons
        self.bagButton = None
        self.radarButton = None
        self.lookoutButton = None
        self.mapButton = None
        self.shipsButton = None
        self.titlesButton = None
        self.mainMenuButton = None
        self.socialButton = None
        self.levelButton = None
        self.chestButton = None
        self.questButton = None
        self.weaponButton = None
        loader.unloadSfx(self.openSfx)
        loader.unloadSfx(self.closeSfx)
        del self.openSfx
        del self.closeSfx
        GuiTray.GuiTray.destroy(self)
        return

    def highlightButton(self, button):

        def changeButtonImage(button, image):
            button['image'] = image
            button['image0_color'] = self.buttonColors[0]
            button['image1_color'] = self.buttonColors[1]
            button['image2_color'] = self.buttonColors[2]
            button['image3_color'] = self.buttonColors[3]

        if self.currentButtonIn:
            changeButtonImage(self.buttons[self.currentButtonIn], self.buttonImage)
        self.currentButtonIn = button
        changeButtonImage(self.buttons[self.currentButtonIn], self.buttonImageIn)

    def togglePanel(self, message, args=None):
        if localAvatar.getInventory() == None:
            return
        if message in self.highlightButtons:
            self.highlightButton(message)
        messenger.send(message, [args])
        return

    def toggle(self):
        if not self.isHidden():
            messenger.send(PiratesGlobals.SeaChestHotkey)
            if localAvatar.guiMgr.questPage:
                chestPanel = localAvatar.guiMgr.chestPanel
                if chestPanel.currPageIndex:
                    currPage = chestPanel.pages[chestPanel.currPageIndex]

    def isOpen(self):
        return self.state

    def showButtons(self):
        if self.hideButtonsIval.isPlaying():
            self.hideButtonsIval.finish()
        self.showButtonsIval.start()

    def hideButtons(self):
        if self.showButtonsIval.isPlaying():
            self.showButtonsIval.finish()
        for button in self.buttons:
            self.buttons[button].hideDetails()

        self.hideButtonsIval.start()

    def slideOpen(self):
        if not self.state:
            self.openSfx.play()
        self.state = 1
        self.chestButton['image'] = self.chestButtonOpen
        self.showButtons()
        if localAvatar.guiMgr.questPage:
            chestPanel = localAvatar.guiMgr.chestPanel
            if chestPanel.currPageIndex:
                currPage = chestPanel.pages[chestPanel.currPageIndex]

    def slideClose(self):
        if self.state:
            self.closeSfx.play()
        self.state = 0
        self.chestButton['image'] = self.chestButtonClosed
        self.hideButtons()

    def buildShowHideButtonsIvals(self, includeSticky=True):
        showSequence = Sequence(Func(self.buttonsParent.show))
        showParallel = Parallel(LerpPosInterval(self.buttonsParent, 0.2, pos=Point3(0, 0, 0.14), startPos=self.buttonsParent.getPos, blendType='easeOut'))
        if includeSticky:
            showSequence.append(Func(self.stickyButtonsParent.show))
            showParallel.append(LerpPosInterval(self.stickyButtonsParent, 0.2, pos=Point3(0, 0, 0.14), startPos=self.stickyButtonsParent.getPos, blendType='easeOut'))
        showSequence.append(showParallel)
        self.showButtonsIval = showSequence
        hideParallel = Parallel(LerpPosInterval(self.buttonsParent, 0.2, pos=Point3(0.2, 0, 0.14), startPos=self.buttonsParent.getPos, blendType='easeIn'))
        hideSequence = Sequence(hideParallel, Func(self.buttonsParent.hide))
        if includeSticky:
            hideSequence.append(Func(self.stickyButtonsParent.hide))
            hideParallel.append(LerpPosInterval(self.stickyButtonsParent, 0.2, pos=Point3(0.2, 0, 0.14), startPos=self.stickyButtonsParent.getPos, blendType='easeIn'))
        hideSequence.append(hideParallel)
        self.hideButtonsIval = hideSequence

    def hideChestButton(self):
        self.chestButton.hide()

    def showChestButton(self):
        self.chestButton.show()