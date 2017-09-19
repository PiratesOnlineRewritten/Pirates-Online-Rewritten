import math
from panda3d.core import TextNode
from panda3d.core import NodePath
from pandac.PandaModules import Vec4
from otp.otpgui import OTPDialog
from direct.gui.DirectGui import *
from direct.gui.DirectGui import DirectWaitBar, DGG
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui.PDialog import PDialog
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence, Parallel, Wait, Func
import FishingGlobals
from FishingResults import FishingResults
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiPanel
from pirates.piratesgui.TextPrinter import TextPrinter

class FishingGameGUI():

    def __init__(self, gameObject=None):
        base.loadingScreen.beginStep('GameGUI', 3, 20)
        self.gameObject = gameObject
        gui = loader.loadModel('models/gui/toplevel_gui')
        guiIcons = loader.loadModel('models/textureCards/icons')
        weaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        fishingIcons = loader.loadModel('models/textureCards/fishing_icons')
        self.tackleBoxButton = DirectButton(parent=base.a2dBottomRight, relief=None, pos=(-0.53, 0.0, 0.1), scale=0.5, text=PLocalizer.FishingGui['Lures'], text_pos=(0, -0.15), text_scale=0.065, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), image_pos=(0, 0, 0), image_scale=0.18, geom=(fishingIcons.find('**/pir_t_gui_fsh_tackleBasket'), fishingIcons.find('**/pir_t_gui_fsh_tackleBasket'), fishingIcons.find('**/pir_t_gui_fsh_tackleBasket_over')), geom_pos=(0, 0, 0), geom_scale=0.25, geom_color=(1.0, 1.0, 1.0, 1), sortOrder=2, command=self.toggleLureSelectionDialog)
        self.tackleBoxInterval = Sequence(self.tackleBoxButton.colorScaleInterval(0.5, Vec4(1.0, 0.6, 0.6, 1.0)), self.tackleBoxButton.colorScaleInterval(0.5, Vec4(1.0, 1.0, 1.0, 1.0)))
        self.exitButton = DirectButton(parent=base.a2dBottomRight, relief=None, pos=(-0.3, 0.0, 0.1), scale=0.5, text=PLocalizer.FishingGui['ExitButton'], text_pos=(0, -0.15), text_scale=0.065, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), image_pos=(0, 0, 0), image_scale=0.18, geom=(fishingIcons.find('**/pir_t_gui_fsh_esc'), fishingIcons.find('**/pir_t_gui_fsh_esc'), fishingIcons.find('**/pir_t_gui_fsh_esc_over')), geom_pos=(0, 0, 0), geom_scale=0.25, geom_color=(1.0, 1.0, 1.0, 1), sortOrder=2, command=self.handleExitGame)
        self.OkDialog = None
        base.loadingScreen.tick()
        dialogText = PLocalizer.FishingGui['ChooseYourLure']
        self.lureSelectionPanel = GuiPanel.GuiPanel(dialogText, 0.75, 0.5, True, 1)
        self.lureSelectionPanel.reparentTo(base.a2dBottomRight)
        self.lureSelectionPanel.setPos(-0.9, 0.0, 0.22)
        self.lureSelectionPanel.regularLureButton = DirectButton(parent=self.lureSelectionPanel, relief=None, pos=(0.2, 0, 0.25), scale=0.5, text='', text_pos=(0, 0), text_scale=PiratesGuiGlobals.TextScaleSmall, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), image=fishingIcons.find('**/pir_t_gui_fsh_lureReg'), image_pos=(0, 0, 0), image_scale=0.18, geom=(gui.find('**/pir_t_gui_but_circle'), gui.find('**/pir_t_gui_but_circle'), gui.find('**/pir_t_gui_but_circle_over')), geom_pos=(0, 0, 0), geom_scale=1, geom_hpr=(0, 0, 90), geom_color=(1.0, 1.0, 1.0, 1), sortOrder=2, command=self.chooseRegularLure)
        self.lureSelectionPanel.regularLureButtonText = DirectLabel(parent=self.lureSelectionPanel, relief=None, text=PLocalizer.FishingGui['RegularLures'], text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(0.28, 0.15), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), textMayChange=1)
        base.loadingScreen.tick()
        inv = localAvatar.getInventory()
        regQty = inv.getStackQuantity(InventoryType.RegularLure)
        self.lureSelectionPanel.regularLureQty = DirectLabel(parent=self.lureSelectionPanel, relief=None, text='x' + str(regQty), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(0.3, 0.2), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), textMayChange=1)
        self.lureSelectionPanel.legendaryLureButton = DirectButton(parent=self.lureSelectionPanel, relief=None, pos=(0.55, 0.0, 0.25), scale=0.5, text='', text_pos=(0, 0), text_scale=PiratesGuiGlobals.TextScaleSmall, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), image=fishingIcons.find('**/pir_t_gui_fsh_lureLegend'), image_pos=(0, 0, 0), image_scale=0.18, geom=(gui.find('**/pir_t_gui_but_circle'), gui.find('**/pir_t_gui_but_circle'), gui.find('**/pir_t_gui_but_circle_over')), geom_pos=(0, 0, 0), geom_scale=1, geom_hpr=(0, 0, 90), geom_color=(1.0, 1.0, 1.0, 1), sortOrder=2, command=self.chooseLegendaryLure)
        self.lureSelectionPanel.legendaryLureButtonText = DirectLabel(parent=self.lureSelectionPanel, relief=None, text=PLocalizer.FishingGui['LegendaryLures'], text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(0.65, 0.15), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), textMayChange=1)
        inv = localAvatar.getInventory()
        legQty = inv.getStackQuantity(InventoryType.LegendaryLure)
        self.lureSelectionPanel.legendaryLureQty = DirectLabel(parent=self.lureSelectionPanel, relief=None, text='x' + str(legQty), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleSmall, text_pos=(0.66, 0.2), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), textMayChange=1)
        self.lureSelectionPanel.hide()
        self.lureSelectionPanelShowing = False
        self.resultsScreen = FishingResults(self.gameObject)
        self.resultsScreen.hide()
        bestRod = 1 #self.gameObject.getAvatarsBestRod()
        if bestRod == -1:
            base.notify.error('Somehow the avatar got into the fishing game without a rod in their inventory!')
        if bestRod == ItemGlobals.FISHING_ROD_3:
            self.castPowerMeterModel = loader.loadModel('models/gui/pir_m_gui_fsh_fishingBarExpert')
        elif bestRod == ItemGlobals.FISHING_ROD_2:
            self.castPowerMeterModel = loader.loadModel('models/gui/pir_m_gui_fsh_fishingBarNovice')
        else:
            self.castPowerMeterModel = loader.loadModel('models/gui/pir_m_gui_fsh_fishingBarBeginner')
        base.loadingScreen.tick()
        self.castPowerMeter = NodePath('castPowerMeter')
        self.castPowerMeter.reparentTo(base.a2dLeftCenter)
        self.castMeterBackground = self.castPowerMeterModel.find('**/background')
        self.castMeterBackground.setBin('fixed', 32)
        self.castMeterBackground.reparentTo(self.castPowerMeter)
        self.castMeterBar = self.castPowerMeterModel.find('**/meter')
        self.castMeterBar.setBin('fixed', 33)
        self.castMeterBar.reparentTo(self.castPowerMeter)
        self.castMeterBar.setColorScale(0.5, 0.5, 1.0, 1.0)
        self.castMeterFrame = self.castPowerMeterModel.find('**/bar')
        self.castMeterFrame.setBin('fixed', 34)
        self.castMeterFrame.reparentTo(self.castPowerMeter)
        self.castPowerMeter.setPos(0.137, 0, 0.228)
        self.castPowerMeter.setScale(1)
        self.lineHealthMeter = NodePath('lineHealthMeter')
        self.lineHealthMeter.reparentTo(base.a2dLeftCenter)
        self.lineHealthMeterModel = loader.loadModel('models/gui/pir_m_gui_fsh_fishingBarHealth')
        self.lineHealthMeterBackground = self.lineHealthMeterModel.find('**/background')
        self.lineHealthMeterBackground.setBin('fixed', 32)
        self.lineHealthMeterBackground.reparentTo(self.lineHealthMeter)
        self.lineHealthMeterBar = self.lineHealthMeterModel.find('**/meter')
        self.lineHealthMeterBar.setBin('fixed', 33)
        self.lineHealthMeterBar.reparentTo(self.lineHealthMeter)
        self.lineHealthMeterFrame = self.lineHealthMeterModel.find('**/bar')
        self.lineHealthMeterFrame.setBin('fixed', 34)
        self.lineHealthMeterFrame.reparentTo(self.lineHealthMeter)
        self.lineHealthMeter.setPos(0.137, 0, 0.25)
        self.lineHealthMeter.setScale(1)
        self.lineLengthLabel = TextPrinter()
        self.lineLengthLabel.text.setScale(1.2)
        self.lineLengthLabel.text.setHpr(0.0, 0.0, 0.0)
        self.lineLengthLabel.text['sortOrder'] = 200
        self.lineLengthLabel.text.setBin('gui-fixed', 10)
        self.lineLengthLabel.text.setDepthTest(0)
        self.lineLengthLabel.text.setDepthWrite(0)
        self.lineLengthLabel.showText('0', (1, 1, 1, 1))
        base.loadingScreen.endStep('GameGUI')
        return

    def updateLureQuantities(self, caller=None):
        inv = localAvatar.getInventory()
        regQty = inv.getStackQuantity(InventoryType.RegularLure)
        legQty = inv.getStackQuantity(InventoryType.LegendaryLure)
        self.lureSelectionPanel.regularLureQty['text'] = 'x' + str(regQty)
        self.lureSelectionPanel.legendaryLureQty['text'] = 'x' + str(legQty)

    def handleExitGame(self):
        messenger.send('escape')

    def chooseRegularLure(self):
        inv = localAvatar.getInventory()
        qty = inv.getStackQuantity(InventoryType.RegularLure)
        if qty > 0:
            self.gameObject.chooseLure(InventoryType.RegularLure)
            self.lureSelectionPanel.hide()
            self.lureSelectionPanelShowing = False
            self.gameObject.sfx['lureEquip'].play()
        else:
            localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughFishingLures, PiratesGuiGlobals.TextFG6)
            self.gameObject.tutorialManager.showTutorial(InventoryType.FishingNoMoreLures)

    def chooseLegendaryLure(self):
        inv = localAvatar.getInventory()
        qty = inv.getStackQuantity(InventoryType.LegendaryLure)
        if qty > 0:
            self.gameObject.chooseLure(InventoryType.LegendaryLure)
            self.lureSelectionPanel.hide()
            self.lureSelectionPanelShowing = False
            self.gameObject.sfx['lureEquip'].play()
        else:
            localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughFishingLures, PiratesGuiGlobals.TextFG6)

    def hideGui(self):
        self.tackleBoxInterval.finish()
        self.castPowerMeter.reparentTo(hidden)
        self.lineHealthMeter.reparentTo(hidden)
        self.tackleBoxButton.reparentTo(hidden)
        self.exitButton.hide()
        self.resultsScreen.cleanUp()
        self.lureSelectionPanelShowing = False
        self.lureSelectionPanel.hide()
        self.lineLengthLabel.text.hide()
        if self.OkDialog is not None:
            self.OkDialog.cleanup()
            self.OkDialog = None
        return

    def showGui(self):
        self.toggleGuiElements()

    def hideExitButton(self):
        self.exitButton.hide()

    def toggleGuiElements(self):
        if self.gameObject.fsm.getCurrentOrNextState() == 'LegendaryFish':
            self.hideGui()
            return
        if self.gameObject.fsm.getCurrentOrNextState() in ['Offscreen', 'ChargeCast', 'Cast', 'PlayerIdle']:
            self.lineHealthMeter.reparentTo(hidden)
            self.castPowerMeter.reparentTo(base.a2dLeftCenter)
            self.lineLengthLabel.text.reparentTo(base.a2dLeftCenter)
            self.lineLengthLabel.text.setPos(0.137, 0.0, 0.528)
            self.exitButton.show()
            self.tackleBoxButton.show()
            if self.tackleBoxInterval.isPlaying():
                self.toggleLureSelectionDialog()
        if self.gameObject.fsm.getCurrentOrNextState() in ['Fishing', 'Reeling', 'QuickReel', 'FishFight']:
            self.castPowerMeter.reparentTo(hidden)
            self.lineHealthMeter.reparentTo(base.a2dLeftCenter)
            self.lineLengthLabel.text.reparentTo(base.a2dLeftCenter)
            self.lineLengthLabel.text.setPos(0.137, 0.0, 0.538)
            self.updateLineHealthMeter(self.gameObject.lineHealth)
            self.tackleBoxButton.hide()
            self.lureSelectionPanel.hide()
            self.lureSelectionPanelShowing = False
        self.tackleBoxButton.reparentTo(base.a2dBottomRight)

    def setTackleBoxPulse(self, bool):
        if bool:
            self.tackleBoxInterval.loop()
        else:
            self.tackleBoxInterval.finish()

    def setTackleBoxPulse(self, bool):
        if bool:
            self.tackleBoxInterval.loop()
        else:
            self.tackleBoxInterval.finish()

    def resetGui(self):
        self.castMeterBar.setScale(1.0, 1.0, 0.01)
        self.lineHealthMeterBar.setScale(1.0, 1.0, 1.0)
        self.toggleGuiElements()

    def destroy(self):
        self.castPowerMeter.removeNode()
        self.lineHealthMeter.removeNode()
        self.lureSelectionPanel.destroy()
        self.lureSelectionPanel.regularLureButton = None
        self.lureSelectionPanel.regularLureButtonText = None
        self.lureSelectionPanel.legendaryLureButton = None
        self.lureSelectionPanel.legendaryLureButtonText = None
        self.lureSelectionPanel = None
        self.lineLengthLabel = None
        self.tackleBoxButton.destroy()
        self.tackleBoxButton = None
        self.exitButton.destroy()
        self.exitButton = None
        return

    def startPowerMeter(self):
        self.startCastFrameTime = globalClock.getFrameTime()

    def updateCastPowerMeter(self, value):
        self.castMeterBar.setScale(1.0, 1.0, value / 100.0)

    def updateCastPowerMeterTask(self, task):
        time = globalClock.getFrameTime()
        elapsed = max(time - self.startCastFrameTime, 0.0)
        value = round(-math.cos(elapsed * 5.0) * 50.0 + 50.0)
        value = max(value, 0.0)
        self.updateCastPowerMeter(value)
        return Task.again

    def updateLineHealthMeter(self, value):
        self.lineHealthMeterBar.setScale(1.0, 1.0, value / 100.0)
        self.lineHealthMeterBar.setColorScale(self.gameObject.getLineColorBasedOnHealth())

    def showRewardDialog(self, fish):
        self.resultsScreen.showAll()
        self.exitButton.hide()

    def showExitCheckDialog(self):
        dialogText = PLocalizer.FishingGui['AreYouSure']
        self.OkDialog = PDialog(text=dialogText, style=OTPDialog.Acknowledge, giveMouse=False, command=self.closeDialogGotoPlayerIdle)
        self.OkDialog.setPos(0.8, 0.0, 0.5)

    def closeDialogGotoPlayerIdle(self, arg):
        self.OkDialog.cleanup()
        self.OkDialog = None
        self.gameObject.fsm.request('PlayerIdle')
        return

    def toggleLureSelectionDialog(self):
        if self.lureSelectionPanelShowing:
            self.lureSelectionPanel.hide()
        else:
            self.lureSelectionPanel.show()
        self.lureSelectionPanelShowing = not self.lureSelectionPanelShowing