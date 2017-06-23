from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiPanel, RedeemCodeGUI
from pirates.piratesgui import GuiButton, DialogButton
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.pirate import DynamicHuman
from pirates.piratesgui.TabBar import LeftTab, TabBar
from direct.interval.IntervalGlobal import *
from pirates.makeapirate import JewelryGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.uberdog.UberDogGlobals import InventoryType
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from direct.task import Task
import random
from pirates.piratesbase import Freebooter
from pirates.inventory import ItemGlobals, DropGlobals
from pirates.inventory.InventoryGlobals import *
from pirates.uberdog.TradableInventoryBase import InvItem
RBROW_CAMERA = 0
LBROW_CAMERA = 1
LEAR_CAMERA = 2
REAR_CAMERA = 3
NOSE_CAMERA = 4
MOUTH_CAMERA = 5
LHAND_CAMERA = 6
RHAND_CAMERA = 7
BUYING = 0
SELLING = 1

class JewelryStoreTab(LeftTab):

    def __init__(self, tabBar, name, **kw):
        optiondefs = (
         ('modelName', 'general_frame_d', None), ('borderScale', 0.38, None), ('bgBuffer', 0.15, None))
        self.defineoptions(kw, optiondefs)
        LeftTab.__init__(self, tabBar, name, **kw)
        self.initialiseoptions(JewelryStoreTab)
        return None


class JewelryStoreTabBar(TabBar):

    def refreshTabs(self):
        for x, name in enumerate(self.tabOrder):
            tab = self.tabs[name]
            tab.reparentTo(self.bParent)
            tab.setPos(-0.07, 0, 1.1 - 0.1 * (x + self.offset))
            (tab.setScale(0.2, 1, 0.2),)

        self.activeIndex = max(0, min(self.activeIndex, len(self.tabOrder) - 1))
        if len(self.tabOrder):
            name = self.tabOrder[self.activeIndex]
            tab = self.tabs[name]
            tab.reparentTo(self.fParent)
            tab.setX(-0.08)
            tab.setScale(0.2, 1, 0.22)

    def makeTab(self, name, **kw):
        return JewelryStoreTab(self, name, **kw)


class JewelryStoreCartList(DirectScrolledFrame):

    def __init__(self, parent, width, height, itemWidth, itemHeight):
        self.width = width + PiratesGuiGlobals.ScrollbarSize
        self.listItemHeight = itemHeight
        self.listItemWidth = itemWidth
        self.height = height
        self.parent = parent
        charGui = loader.loadModel('models/gui/char_gui')
        DirectScrolledFrame.__init__(self, relief=None, state=DGG.NORMAL, manageScrollBars=0, autoHideScrollBars=1, frameSize=(0, self.width, 0, self.height), canvasSize=(0, self.width - 0.05, 0.025, self.height - 0.025), verticalScroll_relief=None, verticalScroll_image=charGui.find('**/chargui_slider_small'), verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, 0, self.height), verticalScroll_image_scale=(self.height + 0.05, 1, 0.75), verticalScroll_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           90), verticalScroll_image_pos=(self.width - PiratesGuiGlobals.ScrollbarSize * 0.5 - 0.004, 0, self.height * 0.5), verticalScroll_image_color=(0.61,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         1), verticalScroll_thumb_image=(charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), verticalScroll_thumb_relief=None, verticalScroll_thumb_image_scale=0.25, verticalScroll_resizeThumb=0, horizontalScroll_relief=None, sortOrder=5)
        self.initialiseoptions(JewelryStoreCartList)
        self.verticalScroll.incButton.destroy()
        self.verticalScroll.decButton.destroy()
        self.horizontalScroll.incButton.destroy()
        self.horizontalScroll.decButton.destroy()
        self.horizontalScroll.hide()
        self.panels = []
        self.purchases = []
        self.itemColor = Vec4(0.2, 0.2, 0.2, 1.0)
        charGui.removeNode()
        return

    def destroy(self):
        self.ignoreAll()
        for panel in self.panels:
            panel.destroy()

        del self.panels
        del self.purchases
        DirectScrolledFrame.destroy(self)

    def setItemColor(self, color):
        self.itemColor = color

    def repackPanels(self):
        z = self.listItemHeight
        i = 0
        for i in range(len(self.panels)):
            self.panels[i].setPos(0.01, 0, -z * (i + 1))
            self.panels[i].origionalPos = self.panels[i].getPos(render2d)

        self['canvasSize'] = (
         0, self.listItemWidth - 0.09, -z * (i + 1), 0)

    def addPanel(self, data, repack=1):
        uid = data[1]
        itemCost = ItemGlobals.getGoldCost(uid)
        itemText = PLocalizer.getItemName(uid)
        if self.parent.mode == 1:
            itemCost = int(itemCost * ItemGlobals.GOLD_SALE_MULTIPLIER)
        maxLength = 25 - len(str(itemCost))
        isDisabled = 0
        panel = DirectButton(parent=self, relief=None, text=itemText[:maxLength], text_fg=self.itemColor, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleMed, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.06,
                                                                                                                                                                                                                                    0.0), command=self.removePanel, extraArgs=[data])
        panel.costLabel = DirectLabel(parent=panel, relief=None, text=str(itemCost), text_fg=self.itemColor, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleMed, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.45,
                                                                                                                                                                                                                                        0.0), image=self.parent.CoinImage, image_scale=0.15, image_pos=(0.48,
                                                                                                                                                                                                                                                                                                        0.0,
                                                                                                                                                                                                                                                                                                        0.014))
        panel.bind(DGG.ENTER, self.highlightStart, extraArgs=[panel])
        panel.bind(DGG.EXIT, self.highlightStop, extraArgs=[panel])
        panel.data = data
        panel.price = itemCost
        panel.reparentTo(self.getCanvas())
        self.panels.append(panel)
        self.purchases.append(data)
        if repack:
            self.repackPanels()
        return

    def highlightStart(self, item, event=None):
        item['text_fg'] = PiratesGuiGlobals.TextFG6
        item.costLabel['text_fg'] = PiratesGuiGlobals.TextFG6

    def highlightStop(self, item, event=None):
        item['text_fg'] = self.itemColor
        item.costLabel['text_fg'] = self.itemColor

    def removePanel(self, data, repack=1):
        for panel in self.panels:
            if panel.data == data:
                self.parent.updateButton(data, 1)
                self.panels.remove(panel)
                self.purchases.remove(data)
                panel.destroy()
                if repack:
                    self.repackPanels()
                self.parent.updateBalance()
                return

    def hasPanel(self, data):
        for panel in self.panels:
            if panel.data == data:
                return True

        return False

    def removeAllPanels(self):
        for panel in self.panels:
            panel.destroy()

        self.panels = []
        self.purchases = []
        self.repackPanels()

    def show(self):
        DirectScrolledFrame.show(self)

    def hide(self):
        DirectScrolledFrame.hide(self)

    def getItemQuantity(self, itemId):
        counter = 0
        for panel in self.panels:
            if panel.data[0] == itemId:
                counter += panel.data[1]

        return counter


class JewelryStoreGUI(DirectFrame):
    notify = directNotify.newCategory('JewelryStoreGUI')
    width = (PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.06) * 2
    height = 1.5
    columnWidth = PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.05
    holidayIdList = []

    def __init__(self, npc, shopId, **kw):
        optiondefs = (
         ('relief', None, None), ('framSize', (0, self.width, 0, self.height), None), ('sortOrder', 20, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, None, **kw)
        self.initialiseoptions(JewelryStoreGUI)
        self.pirate = None
        self.camIval = None
        self.buttons = []
        self.buttonIndex = 0
        self.jewelryAmount = 0
        self.currentPage = None
        self.buttonsPerPage = 4
        self.displayRegionStates = {}
        self.prevIdx = 0
        self.mode = BUYING
        self.redeemCodeGUI = None
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.CoinImage = gui.find('**/treasure_w_coin*')
        self.ParchmentIcon = gui.find('**/main_gui_quest_scroll')
        self.jewelerIconsA = loader.loadModel('models/gui/char_gui')
        self.jewelerIconsB = loader.loadModel('models/textureCards/shopIcons')
        self.ShirtIcon = loader.loadModel('models/gui/char_gui').find('**/chargui_cloth')
        self.LockIcon = gui.find('**/pir_t_gui_gen_key_subscriber')
        self.backTabParent = self.attachNewNode('backTabs', sort=0)
        self.panel = GuiPanel.GuiPanel(None, self.width, self.height, parent=self, showClose=False)
        self.setPos(0.0, 0, -0.75)
        self.balance = 0
        self.npc = npc
        self.rootTitle = PLocalizer.JewelryStore
        self.model = loader.loadModel('models/gui/gui_shop_tailor')
        self.model.reparentTo(self.panel)
        self.model.setPos(0.625, 0.0, 1.05)
        self.model.setScale(0.337, 0.0, 0.327)
        self.paid = Freebooter.getPaidStatus(localAvatar.getDoId())
        self.shopId = shopId
        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()
        self.initialCamPos = camera.getPos()
        self.initialCamHpr = camera.getHpr()
        self.initialPirateH = 0
        self.cartWidth = self.columnWidth - 0.1
        self.cartHeight = self.height - 0.25
        self.cartFrame = DirectFrame(parent=self.panel, relief=None, frameSize=(0, self.cartWidth, 0, self.cartHeight))
        self.cartFrame.setPos(self.columnWidth + 0.025, 0, 0.08)
        self.categoryText = [
         [
          PLocalizer.Hat, PLocalizer.Hats], [PLocalizer.Shirt, PLocalizer.Shirts], [PLocalizer.Vest, PLocalizer.Vests], [PLocalizer.Coat, PLocalizer.Coats], [PLocalizer.Pants, PLocalizer.Pants], [PLocalizer.Belt, PLocalizer.Belts], [None, None], [PLocalizer.Shoe, PLocalizer.Shoes]]
        self.buyParchment = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.TailorPurchase, text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                                                   0.2), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, image=self.ParchmentIcon, image_scale=(0.24,
                                                                                                                                                                                                                                                                                                                                           0.0,
                                                                                                                                                                                                                                                                                                                                           0.3), image_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                            0.0,
                                                                                                                                                                                                                                                                                                                                                            0.0), pos=(0.3,
                                                                                                                                                                                                                                                                                                                                                                       0.0,
                                                                                                                                                                                                                                                                                                                                                                       0.92))
        self.sellParchment = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.TailorSelling, text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                                                   0.2), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, image=self.ParchmentIcon, image_scale=(0.24,
                                                                                                                                                                                                                                                                                                                                           0.0,
                                                                                                                                                                                                                                                                                                                                           0.3), image_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                            0.0,
                                                                                                                                                                                                                                                                                                                                                            0.0), pos=(0.3,
                                                                                                                                                                                                                                                                                                                                                                       0.0,
                                                                                                                                                                                                                                                                                                                                                                       0.48))
        self.purchaseInventory = JewelryStoreCartList(self, self.cartWidth, self.cartHeight - 0.95, self.cartWidth, self.cartHeight / 20.0)
        self.purchaseInventory.reparentTo(self.cartFrame)
        self.purchaseInventory.setPos(0.0, 0.0, 0.76)
        self.sellInventory = JewelryStoreCartList(self, self.cartWidth, self.cartHeight - 0.95, self.cartWidth, self.cartHeight / 20.0)
        self.sellInventory.reparentTo(self.cartFrame)
        self.sellInventory.setPos(0.0, 0.0, 0.31)
        self.frontTabParent = self.panel.attachNewNode('frontTab', sort=2)
        self.currentWardrobe = []
        self.balanceTitle = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.Total, text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                                        0.0), text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.09,
                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                             0.225))
        self.balanceValue = DirectFrame(parent=self.cartFrame, relief=None, text=str(self.balance), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(-0.055, 0.0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, image=self.CoinImage, image_scale=0.15, image_pos=(-0.025,
                                                                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                                                                      0.015), pos=(self.cartWidth, 0, 0.225))
        self.myGoldTitle = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.YourMoney, text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                                           0.0), text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.09,
                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                0.155))
        self.myGold = DirectFrame(parent=self.cartFrame, relief=None, text=str(localAvatar.getMoney()), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(-0.055, 0.0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, image=self.CoinImage, image_scale=0.15, image_pos=(-0.025,
                                                                                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                                                                                          0.015), pos=(self.cartWidth, 0, 0.155))
        self.commitButton = DialogButton.DialogButton(command=self.handleCommitPurchase, parent=self.cartFrame, text=PLocalizer.PurchaseCommit, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.02, -PiratesGuiGlobals.TextScaleLarge * 0.25), text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, buttonStyle=DialogButton.DialogButton.YES)
        self.commitButton.setPos(self.cartWidth / 2, 0, 0.005)
        self.closeButton = DialogButton.DialogButton(command=self.closePanel, parent=self.cartFrame, text=PLocalizer.lClose, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.02, -PiratesGuiGlobals.TextScaleLarge * 0.25), text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, buttonStyle=DialogButton.DialogButton.NO)
        self.closeButton.setPos(self.cartWidth / 2 - 0.55, 0, 0.005)
        self.redeemCodeButton = DialogButton.DialogButton(command=self.showRedeemCodeGUI, parent=self.cartFrame, text=PLocalizer.ShopRedeem, text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow)
        self.redeemCodeButton.setPos(-0.015, 0, 0.005)
        self.storeButton = DialogButton.DialogButton(command=self.changeMode, state=DGG.DISABLED, parent=self.cartFrame, text=PLocalizer.InteractStore, text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, image_color=Vec4(0.7, 0.95, 0.7, 1.0), scale=0.9, extraArgs=[0])
        self.storeButton.setPos(-0.4, 0.0, 1.15)
        self.wardrobeButton = DialogButton.DialogButton(command=self.changeMode, state=DGG.NORMAL, parent=self.cartFrame, text=PLocalizer.TailorWardrobe, text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, text_shadow=PiratesGuiGlobals.TextShadow, image_color=Vec4(0.95, 0.7, 0.7, 1.0), scale=0.9, extraArgs=[1])
        self.wardrobeButton.setPos(-0.18, 0.0, 1.15)
        tGui = loader.loadModel('models/gui/triangle')
        triangle = (tGui.find('**/triangle'), tGui.find('**/triangle_down'), tGui.find('**/triangle_over'))
        self.nextPageButton = DirectButton(parent=self.panel, relief=None, state=DGG.DISABLED, image=triangle, image_scale=0.065, pos=(0.54,
                                                                                                                                       0.0,
                                                                                                                                       0.175), rolloverSound=None, command=self.nextPage)
        self.prevPageButton = DirectButton(parent=self.panel, relief=None, state=DGG.DISABLED, image=triangle, image_scale=-0.065, pos=(0.16,
                                                                                                                                        0.0,
                                                                                                                                        0.175), rolloverSound=None, command=self.previousPage)
        self.pageNumber = DirectFrame(parent=self.panel, relief=None, text='', text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0,
                                                                                                                                                                                                      0.0), text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.35,
                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                           0.1625))
        self.titleLabel = DirectLabel(parent=self, relief=None, text='', text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge * 1.3, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.62,
                                                                                                                                                                                                                                           0.0,
                                                                                                                                                                                                                                           1.33))
        self.titleLabel.setBin('gui-fixed', 1)
        self.createPirate()
        charGui = loader.loadModel('models/gui/char_gui')
        self.rotateSlider = DirectSlider(parent=base.a2dBottomLeft, relief=None, command=self.rotatePirate, image=charGui.find('**/chargui_slider_small'), image_scale=(2.15,
                                                                                                                                                                        2.15,
                                                                                                                                                                        1.5), thumb_relief=None, thumb_image=(charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), pos=(0.8,
                                                                                                                                                                                                                                                                                                                                                      0.0,
                                                                                                                                                                                                                                                                                                                                                      0.09), text_align=TextNode.ACenter, text_scale=(0.1,
                                                                                                                                                                                                                                                                                                                                                                                                      0.1), text_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                      0.1), text_fg=PiratesGuiGlobals.TextFG1, scale=0.43, text=PLocalizer.RotateSlider, value=0.5, sortOrder=-1)
        self.rotateSlider['extraArgs'] = [
         self.rotateSlider]
        self.rotateSliderOrigin = 0.5
        self.accept('mouse1', self._startMouseReadTask)
        self.accept('mouse1-up', self._stopMouseReadTask)
        self.clothWindows = []
        self.clothRenders = []
        self.clothHumans = []
        self.clothCameraNPs = []
        self.clothCameras = []
        self.createDisplayRegions()
        self.alertDialog = None
        self.accept('aspectRatioChanged', self.aspectRatioChange)
        self.accept('NonPayerPanelShown', self.hideDisplayRegions)
        self.accept('NonPayerPanelHidden', self.showDisplayRegions)
        self.accept('MainMenuShown', self.hideDisplayRegions)
        self.accept('MainMenuHidden', self.showDisplayRegions)
        self.accept('GUIShown', self.showDisplayRegions)
        self.accept('GUIHidden', self.hideDisplayRegions)
        localAvatar.guiMgr.chatPanel.show()
        localAvatar.guiMgr.chatPanel.startFadeTextIval()
        self.accept(localAvatar.uniqueName('jewelryUpdate'), self.reloadPirateDNA, extraArgs=[self.pirate])
        self.showQuestLabel = False
        if not localAvatar.guiMgr.trackedQuestLabel.isHidden():
            localAvatar.guiMgr.hideTrackedQuestInfo()
            self.showQuestLabel = True
        self.equipRequests = {JewelryGlobals.RBROW: None,JewelryGlobals.LBROW: None,JewelryGlobals.LEAR: None,JewelryGlobals.REAR: None,JewelryGlobals.NOSE: None,JewelryGlobals.MOUTH: None,JewelryGlobals.LHAND: None,JewelryGlobals.RHAND: None}
        self.initTabs()
        self.updateBalance()
        return

    def showRedeemCodeGUI(self):
        if self.redeemCodeGUI:
            self.redeemCodeGUI.showCode()
        else:
            self.redeemCodeGUI = RedeemCodeGUI.RedeemCodeGUI(self)

    def hideDisplayRegions(self):
        for id in range(len(self.clothRenders)):
            if self.clothRenders[id].isHidden():
                self.displayRegionStates[id] = False
            else:
                self.displayRegionStates[id] = True
            self.clothRenders[id].hide()

    def showDisplayRegions(self):
        for id in range(len(self.clothRenders)):
            if self.displayRegionStates[id]:
                self.clothRenders[id].show()

    def aspectRatioChange(self):
        properties = base.win.getProperties()
        x = properties.getXSize()
        y = properties.getYSize()
        ar = float(x) / float(y)
        width = 0.1 * aspect2d.getScale()[0]
        height = 0.075 * aspect2d.getScale()[2]
        offsetX = 0.13 * aspect2d.getScale()[0]
        offsetY = -0.015 * aspect2d.getScale()[2]
        for id in range(len(self.buttons)):
            button = self.buttons[id]
            displayRegion = self.clothWindows[id]
            p = button.getPos(render2d) - Point3(width + offsetX, 0, height + offsetY)
            pv = Point3((p[0] + 1) / 2.0, 0.0, (p[2] + 1) / 2.0)
            displayRegion.setDimensions(pv[0], pv[0] + width, pv[2], pv[2] + height)

    def rotatePirate(self, slider):
        if self.pirate and slider:
            value = slider.getValue()
            if value != self.rotateSliderOrigin:
                diff = value - self.rotateSliderOrigin
                h = diff * 360.0 + self.pirate.getH()
                self.pirate.setH(h)
                self.rotateSliderOrigin = value

    def destroy(self):
        DirectFrame.destroy(self)
        self._stopMouseReadTask()
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
            camera.setHpr(0, 0, 0)
        self.rotateSlider.destroy()
        self.cleanupRegions()
        self.unloadPirate()
        if self.model:
            self.model.removeNode()
            self.model = None
        if self.CoinImage:
            self.CoinImage.removeNode()
            self.CoinImage = None
        if self.ParchmentIcon:
            self.ParchmentIcon.removeNode()
            self.ParchmentIcon = None
        if self.ShirtIcon:
            self.ShirtIcon.removeNode()
            self.ShirtIcon = None
        if self.jewelerIconsA:
            self.jewelerIconsA.removeNode()
            self.jewelerIconsA = None
        if self.jewelerIconsB:
            self.jewelerIconsB.removeNode()
            self.jewelerIconsB = None
        if self.alertDialog:
            self.alertDialog.destroy()
        if self.redeemCodeGUI:
            self.redeemCodeGUI.destroy()
        if len(localAvatar.guiMgr.trackedQuestLabel['text']):
            if self.showQuestLabel:
                localAvatar.guiMgr.showTrackedQuestInfo()
        localAvatar.guiMgr.chatPanel.hide()
        return

    def createPirate(self):
        if self.pirate is None:
            self.pirate = DynamicHuman.DynamicHuman()
            self.pirate.setDNAString(localAvatar.style)
            self.pirate.generateHuman(localAvatar.style.gender)
            self.pirate.model.setupSelectionChoices('DEFAULT')
            self.pirate.mixingEnabled = False
            self.pirate.enableBlend()
            self.pirate.loop('idle_centered')
            self.pirate.loop('idle')
            self.pirate.setControlEffect('idle_centered', 0)
            self.pirate.setControlEffect('idle', 1)
            self.pirate.useLOD(2000)
            dummy = self.npc.attachNewNode('dummy')
            dummy.setPos(self.npc.getPos() - Vec3(0, 7, 0))
            parent = self.npc.getParent()
            self.pirate.reparentTo(parent)
            pos = dummy.getPos()
            hpr = dummy.getHpr()
            self.pirate.setPos(pos)
            self.pirate.setHpr(hpr)
            self.pirate.lookAt(self.npc)
            dummy.detachNode()
            self.initialPirateH = self.pirate.getH()
        self.pirate.show()
        localAvatar.stash()
        return

    def focusCamera(self, cameraId=RBROW_CAMERA):
        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
        if self.pirate is None:
            self.createPirate()
        self.pirate.setH(self.initialPirateH)
        self.rotateSlider['value'] = self.rotateSliderOrigin = 0.5
        dummy = self.pirate.attachNewNode('dummy')
        if cameraId == RBROW_CAMERA:
            dummy.setPos(dummy, 1, 2, self.pirate.headNode.getZ(self.pirate) + 0.5)
        else:
            if cameraId == LBROW_CAMERA:
                dummy.setPos(dummy, -1, 2, self.pirate.headNode.getZ(self.pirate) + 0.5)
            else:
                if cameraId == LEAR_CAMERA:
                    dummy.setPos(dummy, -2, 2, self.pirate.headNode.getZ(self.pirate) + 0.25)
                elif cameraId == REAR_CAMERA:
                    dummy.setPos(dummy, 2, 2, self.pirate.headNode.getZ(self.pirate) + 0.25)
                elif cameraId == NOSE_CAMERA:
                    dummy.setPos(dummy, 0, 2, self.pirate.headNode.getZ(self.pirate) + 0.25)
                elif cameraId == MOUTH_CAMERA:
                    dummy.setPos(dummy, 0, 2, self.pirate.headNode.getZ(self.pirate))
                elif cameraId == LHAND_CAMERA:
                    dummy.setPos(dummy, -2, 2.5, self.pirate.leftHandNode.getZ(self.pirate))
                else:
                    if cameraId == RHAND_CAMERA:
                        dummy.setPos(dummy, 2, 2.5, self.pirate.rightHandNode.getZ(self.pirate))
                    else:
                        dummy.setPos(dummy, 0, 0, 0)
                    dummy.wrtReparentTo(render)
                    if cameraId == RBROW_CAMERA:
                        dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
                    elif cameraId == LBROW_CAMERA:
                        dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
                    elif cameraId == LEAR_CAMERA:
                        dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
                    else:
                        if cameraId == REAR_CAMERA:
                            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
                        if cameraId == NOSE_CAMERA:
                            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.1)
                        if cameraId == MOUTH_CAMERA:
                            dummy.lookAt(self.pirate, self.pirate.headNode.getX(self.pirate), self.pirate.headNode.getY(self.pirate), self.pirate.headNode.getZ(self.pirate) * 1.075)
                        if cameraId == LHAND_CAMERA:
                            dummy.lookAt(self.pirate, self.pirate.leftHandNode.getX(self.pirate), self.pirate.leftHandNode.getY(self.pirate), self.pirate.leftHandNode.getZ(self.pirate) * 1.2)
                        if cameraId == RHAND_CAMERA:
                            dummy.lookAt(self.pirate, self.pirate.rightHandNode.getX(self.pirate), self.pirate.rightHandNode.getY(self.pirate), self.pirate.rightHandNode.getZ(self.pirate) * 1.2)
                        dummy.lookAt(0, 0, 0, 0)
                dummy.setH(dummy, -17)
                dummy.setP(dummy, -12)
                camPos = dummy.getPos()
                camHpr = Point3(dummy.getH(), dummy.getP(), 0)
                dummy.detachNode()
                camera.wrtReparentTo(render)
                camH = camera.getH() % 360
                h = camHpr[0] % 360
                if camH > h:
                    h += 360
            if h - camH > 180:
                h -= 360
        camHpr.setX(h)
        camera.setH(camH)
        t = 1.5
        self.camIval = camera.posHprInterval(t, pos=camPos, hpr=camHpr, blendType='easeOut')
        localAvatar.cameraFSM.request('Control')
        self.camIval.start()
        return

    def unloadPirate(self):
        if self.pirate:
            self.pirate.detachNode()
            self.pirate.cleanupHuman()
            self.pirate.delete()
            self.pirate = None
        localAvatar.unstash()
        return

    def closePanel(self):
        messenger.send('exitStore')
        self.ignoreAll()
        camera.setPos(self.initialCamPos)
        camera.setHpr(self.initialCamHpr)
        equips = []
        for type in self.equipRequests.keys():
            equip = self.equipRequests.get(type)
            id = 0
            primary = 0
            secondary = 0
            if equip is not None:
                uid = equip[0]
                item = JewelryGlobals.jewelry_id.get(uid)
                if item is not None:
                    equips.append([type, uid])
                    id = item[0]
                    primary = item[4]
                    secondary = item[5]
                else:
                    equips.append([type, -1])
                    id = -1
                    primary = 0
                    secondary = 0
                if type == JewelryGlobals.RBROW:
                    localAvatar.style.setJewelryZone4(id, primary, secondary)
                elif type == JewelryGlobals.LBROW:
                    localAvatar.style.setJewelryZone3(id, primary, secondary)
                elif type == JewelryGlobals.LEAR:
                    localAvatar.style.setJewelryZone1(id, primary, secondary)
                elif type == JewelryGlobals.REAR:
                    localAvatar.style.setJewelryZone2(id, primary, secondary)
                elif type == JewelryGlobals.NOSE:
                    localAvatar.style.setJewelryZone5(id, primary, secondary)
                elif type == JewelryGlobals.MOUTH:
                    localAvatar.style.setJewelryZone6(id, primary, secondary)
                elif type == JewelryGlobals.LHAND:
                    localAvatar.style.setJewelryZone7(id, primary, secondary)
                elif type == JewelryGlobals.RHAND:
                    localAvatar.style.setJewelryZone8(id, primary, secondary)

        if len(equips) > 0:
            self.npc.sendRequestJewelryEquip(equips)
            gender = localAvatar.style.getGender()
            localAvatar.generateHuman(gender, base.cr.humanHigh)
            localAvatar.motionFSM.off()
            localAvatar.motionFSM.on()
        self.unloadPirate()
        return

    def handleCommitPurchase(self):
        if self.purchaseInventory == []:
            base.localAvatar.guiMgr.createWarning(PLocalizer.EmptyPurchaseWarning, PiratesGuiGlobals.TextFG6)
            return
        inventory = base.localAvatar.getInventory()
        if inventory:
            if inventory.getGoldInPocket() < self.balance:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughMoneyWarning, PiratesGuiGlobals.TextFG6)
                return
            if self.balance < 0 and inventory.getGoldInPocket() + self.balance > GOLD_CAP:
                base.localAvatar.guiMgr.createWarning(PLocalizer.CannotHoldGoldWarning, PiratesGuiGlobals.TextFG6)
                return
        purchaseArgList = []
        sellArgList = []
        for item in self.purchaseInventory.purchases:
            uid = item[1]
            id = ItemGlobals.getMaleModelId(uid)
            type = item[0]
            primary = ItemGlobals.getPrimaryColor(uid)
            secondary = ItemGlobals.getSecondaryColor(uid)
            itemCost = ItemGlobals.getGoldCost(uid)
            location = item[2]
            purchaseArgList.append([uid, location])

        for item in self.sellInventory.purchases:
            uid = item[1]
            id = ItemGlobals.getMaleModelId(uid)
            type = item[0]
            primary = ItemGlobals.getPrimaryColor(uid)
            secondary = ItemGlobals.getSecondaryColor(uid)
            itemCost = ItemGlobals.getGoldCost(uid)
            location = item[2]
            sellArgList.append([uid, location])
            if self.equipRequests[type] == [uid, id, primary, secondary]:
                self.equipRequests[type] = None

        self.purchaseInventory.removeAllPanels()
        self.sellInventory.removeAllPanels()
        self.npc.sendRequestJewelry(purchaseArgList, sellArgList)
        self.changeMode(1, refresh=True)
        return

    def updateBalance(self, extraArgs=None):
        self.myGold['text'] = str(localAvatar.getMoney())
        self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG2
        self.balance = 0
        for item in self.purchaseInventory.panels:
            self.balance += max(item.price, 1)

        for item in self.sellInventory.panels:
            self.balance -= max(item.price, 1)

        transactions = len(self.purchaseInventory.purchases) + len(self.sellInventory.purchases)
        if self.balance > 0:
            self.balanceTitle['text'] = PLocalizer.Total
            self.balanceValue['text'] = str(abs(self.balance))
            self.commitButton['text'] = PLocalizer.PurchaseCommit
        else:
            if self.balance < 0:
                self.balanceTitle['text'] = PLocalizer.Gain
                self.balanceValue['text'] = str(abs(self.balance))
                self.commitButton['text'] = PLocalizer.TailorSell
            else:
                self.balanceTitle['text'] = PLocalizer.Total
                self.balanceValue['text'] = str(abs(self.balance))
                self.commitButton['text'] = PLocalizer.GenericConfirmDone
            if self.balance > localAvatar.getMoney() or transactions == 0:
                if self.balance > localAvatar.getMoney():
                    self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG6
                self.commitButton['state'] = DGG.DISABLED
            elif self.balance < 0:
                self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG4
                self.commitButton['state'] = DGG.NORMAL
            else:
                self.balanceValue['text_fg'] = PiratesGuiGlobals.TextFG2
                self.commitButton['state'] = DGG.NORMAL
            inventory = base.localAvatar.getInventory()
            if inventory:
                if inventory.getGoldInPocket() < self.balance or self.purchaseInventory.panels == []:
                    self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor3
                else:
                    self.commitButton['frameColor'] = PiratesGuiGlobals.ButtonColor4

    def checkPanel(self, panel, inventory, itemId):
        purchaseQty = self.purchaseInventory.getItemQuantity(itemId)
        panel.checkPlayerInventory(itemId, purchaseQty)

    def initTabs(self):
        self.tabBar = JewelryStoreTabBar(parent=self, backParent=self.backTabParent, frontParent=self.frontTabParent, offset=0)
        self.pageNames = []
        self.createTabs()
        if len(self.pageNames) > 0:
            self.setPage(self.pageNames[0])

    def createTabs(self):
        for item in JewelryGlobals.JewelryTypes:
            if not self.isPageAdded(item):
                self.addTab(item)

    def addTab(self, id):
        newTab = self.tabBar.addTab(id, command=self.setPage, extraArgs=[id])
        if id == JewelryGlobals.RBROW:
            tabIcon = self.jewelerIconsB.find('**/icon_shop_tailor_brow')
            tabScale = (-0.5, 0.5, 0.5)
        elif id == JewelryGlobals.LBROW:
            tabIcon = self.jewelerIconsB.find('**/icon_shop_tailor_brow')
            tabScale = (0.5, 0.5, 0.5)
        elif id == JewelryGlobals.LEAR:
            tabIcon = self.jewelerIconsA.find('**/chargui_ears')
            tabScale = (1.7, 1.7, 1.7)
        elif id == JewelryGlobals.REAR:
            tabIcon = self.jewelerIconsA.find('**/chargui_ears')
            tabScale = (-1.7, 1.7, 1.7)
        elif id == JewelryGlobals.NOSE:
            tabIcon = self.jewelerIconsA.find('**/chargui_nose')
            tabScale = 1.7
        elif id == JewelryGlobals.MOUTH:
            tabIcon = self.jewelerIconsA.find('**/chargui_mouth')
            tabScale = 1.7
        elif id == JewelryGlobals.LHAND:
            tabIcon = self.jewelerIconsB.find('**/icon_shop_tailor_hand')
            tabScale = (0.5, 0.5, 0.5)
        elif id == JewelryGlobals.RHAND:
            tabIcon = self.jewelerIconsB.find('**/icon_shop_tailor_hand')
            tabScale = (-0.5, 0.5, 0.5)
        else:
            tabIcon = None
            tabScale = 0.0
        tabText = PLocalizer.JewelryNames.get(id)
        newTab.nameTag = DirectLabel(parent=newTab, relief=None, state=DGG.DISABLED, pos=(0.06, 0, -0.035), text_fg=PiratesGuiGlobals.TextFG1, text_scale=0.2, image=tabIcon, image_scale=tabScale)
        self.pageNames.append(id)
        return

    def isPageAdded(self, pageName):
        return self.pageNames.count(pageName) > 0

    def nextPage(self):
        if self.jewelryAmount - (self.buttonIndex + self.buttonsPerPage) > 0:
            startIndex = self.buttonIndex + self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)
        else:
            self.setPage(self.currentPage, 0, False)

    def previousPage(self):
        if self.buttonIndex > 0:
            startIndex = self.buttonIndex - self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)
        else:
            remainder = self.jewelryAmount % self.buttonsPerPage
            if remainder:
                startIndex = self.jewelryAmount - remainder
            else:
                startIndex = self.jewelryAmount - self.buttonsPerPage
            self.setPage(self.currentPage, startIndex, False)

    def setJewelry(self, pirate, type, uid):
        idx = ItemGlobals.getMaleModelId(uid)
        primaryColor = ItemGlobals.getPrimaryColor(uid)
        secondaryColor = ItemGlobals.getSecondaryColor(uid)
        if type == JewelryGlobals.LBROW:
            pirate.setJewelryZone3(idx, primaryColor, secondaryColor)
        elif type == JewelryGlobals.RBROW:
            pirate.setJewelryZone4(idx, primaryColor, secondaryColor)
        elif type == JewelryGlobals.LEAR:
            pirate.setJewelryZone1(idx, primaryColor, secondaryColor)
        elif type == JewelryGlobals.REAR:
            pirate.setJewelryZone2(idx, primaryColor, secondaryColor)
        elif type == JewelryGlobals.NOSE:
            pirate.setJewelryZone5(idx, primaryColor, secondaryColor)
        elif type == JewelryGlobals.MOUTH:
            pirate.setJewelryZone6(idx, primaryColor, secondaryColor)
        elif type == JewelryGlobals.LHAND:
            pirate.setJewelryZone7(idx, primaryColor, secondaryColor)
        elif type == JewelryGlobals.RHAND:
            pirate.setJewelryZone8(idx, primaryColor, secondaryColor)
        else:
            print 'Unknown type'
        pirate.model.handleJewelryHiding()

    def addToCart(self, button, type, uid, location=0):
        data = [
         type, uid, location]
        inventory = base.localAvatar.getInventory()
        if not inventory:
            return
        if self.mode == BUYING:
            if button.addToCart.buyState:
                limit = PiratesGlobals.WARDROBE_LIMIT_JEWELER
                current = 0
                locatables = []
                for item in self.purchaseInventory.panels:
                    dataId = item.data[1]
                    locatables.append(InvItem([InventoryType.ItemTypeJewelry, dataId, 0]))

                locatables.append(InvItem([InventoryType.ItemTypeJewelry, uid, 0]))
                locationIds = inventory.canAddLocatables(locatables)
                for locationId in locationIds:
                    if locationId in (Locations.INVALID_LOCATION, Locations.NON_LOCATION):
                        base.localAvatar.guiMgr.createWarning(PLocalizer.InventoryFullWarning, PiratesGuiGlobals.TextFG6)
                        return

                self.purchaseInventory.addPanel(data)
                button.addToCart['text'] = PLocalizer.TailorRemove
                button.addToCart.buyState = 0
            else:
                button.addToCart['text'] = PLocalizer.TailorAddToCart
                button.addToCart.buyState = 1
                self.purchaseInventory.removePanel(data)
        elif self.mode == SELLING:
            if button.addToCart.buyState:
                itemCount = 1
                itemId = data[1]
                for item in self.sellInventory.panels:
                    dataId = item.data[1]
                    if itemId == dataId:
                        itemCount += 1

                if inventory.getItemQuantity(InventoryType.ItemTypeJewelry, itemId) < itemCount:
                    base.localAvatar.guiMgr.createWarning(PLocalizer.DoNotOwnEnoughWarning, PiratesGuiGlobals.TextFG6)
                    return
                self.sellInventory.addPanel(data)
                button.addToCart['text'] = PLocalizer.TailorRemove
                button.addToCart.buyState = 0
            else:
                button.addToCart['text'] = PLocalizer.TailorSell
                button.addToCart.buyState = 1
                self.sellInventory.removePanel(data)
        self.updateBalance()

    def updateButton(self, data, buyState):
        for item in self.buttons:
            if item.jewelryUID == data[1] and item.jewelryLocation == data[2]:
                if self.mode == BUYING and item.jewelryUID not in self.currentWardrobe:
                    item.addToCart['text'] = PLocalizer.TailorAddToCart
                elif self.mode == SELLING:
                    item.addToCart['text'] = PLocalizer.TailorSell
                item.addToCart.buyState = 1
                return

    def changeMode(self, mode, refresh=False):
        if self.mode == mode and not refresh:
            return
        elif self.mode == mode and refresh:
            self.setPage(self.currentPage, 0, refreshWardrobe=refresh)
            return
        if self.mode == BUYING:
            self.prevIdx = self.buttonIndex
            idx = 0
        else:
            idx = self.prevIdx
        self.mode = mode
        self.setPage(self.currentPage, idx, refreshWardrobe=refresh)

    def setWardrobe(self, jewelry):
        if self.currentWardrobe:
            self.currentWardrobe = []
        self.currentWardrobe = jewelry
        self.setPage(self.currentPage, refreshWardrobe=False)

    def reloadPirateDNA(self, pirate):
        if self.equipRequests[JewelryGlobals.RBROW] is None:
            jewelryZone4 = list(localAvatar.style.getJewelryZone4())
        else:
            jewelryZone4 = list(self.equipRequests[JewelryGlobals.RBROW][1:])
        if self.equipRequests[JewelryGlobals.LBROW] is None:
            jewelryZone3 = list(localAvatar.style.getJewelryZone3())
        else:
            jewelryZone3 = list(self.equipRequests[JewelryGlobals.LBROW][1:])
        if self.equipRequests[JewelryGlobals.LEAR] is None:
            jewelryZone1 = list(localAvatar.style.getJewelryZone1())
        else:
            jewelryZone1 = list(self.equipRequests[JewelryGlobals.LEAR][1:])
        if self.equipRequests[JewelryGlobals.REAR] is None:
            jewelryZone2 = list(localAvatar.style.getJewelryZone2())
        else:
            jewelryZone2 = list(self.equipRequests[JewelryGlobals.REAR][1:])
        if self.equipRequests[JewelryGlobals.NOSE] is None:
            jewelryZone5 = list(localAvatar.style.getJewelryZone5())
        else:
            jewelryZone5 = list(self.equipRequests[JewelryGlobals.NOSE][1:])
        if self.equipRequests[JewelryGlobals.MOUTH] is None:
            jewelryZone6 = list(localAvatar.style.getJewelryZone6())
        else:
            jewelryZone6 = list(self.equipRequests[JewelryGlobals.MOUTH][1:])
        if self.equipRequests[JewelryGlobals.LHAND] is None:
            jewelryZone7 = list(localAvatar.style.getJewelryZone7())
        else:
            jewelryZone7 = list(self.equipRequests[JewelryGlobals.LHAND][1:])
        if self.equipRequests[JewelryGlobals.RHAND] is None:
            jewelryZone8 = list(localAvatar.style.getJewelryZone8())
        else:
            jewelryZone8 = list(self.equipRequests[JewelryGlobals.RHAND][1:])
        if not hasattr(pirate, 'style'):
            return
        pirate.style.setJewelryZone1(jewelryZone1[0], jewelryZone1[1], jewelryZone1[2])
        pirate.style.setJewelryZone2(jewelryZone2[0], jewelryZone2[1], jewelryZone2[2])
        pirate.style.setJewelryZone3(jewelryZone3[0], jewelryZone3[1], jewelryZone3[2])
        pirate.style.setJewelryZone4(jewelryZone4[0], jewelryZone4[1], jewelryZone4[2])
        pirate.style.setJewelryZone5(jewelryZone5[0], jewelryZone5[1], jewelryZone5[2])
        pirate.style.setJewelryZone6(jewelryZone6[0], jewelryZone6[1], jewelryZone6[2])
        pirate.style.setJewelryZone7(jewelryZone7[0], jewelryZone7[1], jewelryZone7[2])
        pirate.style.setJewelryZone8(jewelryZone8[0], jewelryZone8[1], jewelryZone8[2])
        pirate.model.handleJewelryHiding()
        return

    def equipJewelry(self, jewelry):
        type = jewelry[1]
        uid = jewelry[2]
        item = JewelryGlobals.jewelry_id.get(uid)
        itemButton = jewelry[0]
        if item:
            id = item[0]
            primary = item[4]
            secondary = item[5]
            self.equipRequests[type] = [
             uid, id, primary, secondary]
        else:
            self.equipRequests[type] = [
             -1, 0, 0, 0]
        self.reloadPirateDNA(self.pirate)
        for button in self.buttons:
            if button != itemButton:
                button.itemText['text'] = ''
                if button.questDrop is True:
                    button.itemText['text'] = PLocalizer.ShopQuestItem

        itemButton.itemText['text'] = PLocalizer.TattooShopOwned

    def sortItems(self, item1, item2):
        if item1[1] == True:
            return -1
        elif item2[1] == True:
            return 1
        elif self.mode == BUYING:
            if item1[6] is not None:
                return -1
            elif item2[6] is not None:
                return 1
            elif item1[3] > item2[3]:
                return 1
            elif item1[3] < item2[3]:
                return -1
            elif item1[4] > item2[4]:
                return 1
            elif item1[4] < item2[4]:
                return -1
            elif item1[5] > item2[5]:
                return 1
            elif item1[5] < item2[5]:
                return -1
            else:
                return 0
        elif self.mode == SELLING:
            if item1[2] < item2[2]:
                return 1
            elif item1[2] > item2[2]:
                return -1
            else:
                return 0
        return

    def setPage(self, pageName, startIndex=0, refreshWardrobe=True):
        self.tabBar.unstash()
        self.titleLabel['text'] = '\x01smallCaps\x01' + self.rootTitle + ' - ' + PLocalizer.JewelryNames.get(pageName) + '\x02'
        previousPage = self.currentPage
        if self.currentPage != pageName:
            self.prevIdx = 0
        self.currentPage = pageName
        jewelryType = pageName
        gender = localAvatar.style.getGender()
        if self.currentPage != previousPage:
            self.focusCamera(self.currentPage)
        if localAvatar.style.getGender() == 'm':
            GENDER = 'MALE'
        else:
            GENDER = 'FEMALE'
        if refreshWardrobe:
            self.npc.sendRequestJewelryList()
        if self.equipRequests[JewelryGlobals.RBROW] is None:
            currentRBROW = localAvatar.style.getJewelryZone4()
        else:
            currentRBROW = self.equipRequests[JewelryGlobals.RBROW][1:]
        if self.equipRequests[JewelryGlobals.LBROW] is None:
            currentLBROW = localAvatar.style.getJewelryZone3()
        else:
            currentLBROW = self.equipRequests[JewelryGlobals.LBROW][1:]
        if self.equipRequests[JewelryGlobals.LEAR] is None:
            currentLEAR = localAvatar.style.getJewelryZone1()
        else:
            currentLEAR = self.equipRequests[JewelryGlobals.LEAR][1:]
        if self.equipRequests[JewelryGlobals.REAR] is None:
            currentREAR = localAvatar.style.getJewelryZone2()
        else:
            currentREAR = self.equipRequests[JewelryGlobals.REAR][1:]
        if self.equipRequests[JewelryGlobals.NOSE] is None:
            currentNOSE = localAvatar.style.getJewelryZone5()
        else:
            currentNOSE = self.equipRequests[JewelryGlobals.NOSE][1:]
        if self.equipRequests[JewelryGlobals.MOUTH] is None:
            currentMOUTH = localAvatar.style.getJewelryZone6()
        else:
            currentMOUTH = self.equipRequests[JewelryGlobals.MOUTH][1:]
        if self.equipRequests[JewelryGlobals.LHAND] is None:
            currentLHAND = localAvatar.style.getJewelryZone7()
        else:
            currentLHAND = self.equipRequests[JewelryGlobals.LHAND][1:]
        if self.equipRequests[JewelryGlobals.RHAND] is None:
            currentRHAND = localAvatar.style.getJewelryZone8()
        else:
            currentRHAND = self.equipRequests[JewelryGlobals.RHAND][1:]
        jewelry = []
        if self.mode == BUYING:
            jewelryIds = DropGlobals.getStoreItems(self.npc.uniqueId)
            for jewelryId in jewelryIds:
                if ItemGlobals.getType(jewelryId) == self.getItemGlobalsType(jewelryType) and ItemGlobals.getClass(jewelryId) == InventoryType.ItemTypeJewelry:
                    id = ItemGlobals.getMaleModelId(jewelryId)
                    primary = ItemGlobals.getPrimaryColor(jewelryId)
                    secondary = ItemGlobals.getSecondaryColor(jewelryId)
                    cost = ItemGlobals.getGoldCost(jewelryId)
                    holiday = ItemGlobals.getHoliday(jewelryId)
                    location = 0
                    if not holiday or holiday in JewelryStoreGUI.holidayIdList:
                        jewelry.append([jewelryId, False, cost, id, primary, secondary, holiday, location])

        if self.mode == SELLING:
            if self.currentWardrobe:
                for itemInfo in self.currentWardrobe:
                    id = itemInfo[0]
                    location = itemInfo[1]
                    type = self.getJewelryGlobalsType(id)
                    if type == jewelryType:
                        cost = ItemGlobals.getGoldCost(id)
                        equipped = False
                        jewelryId = ItemGlobals.getMaleModelId(id)
                        primaryColor = ItemGlobals.getPrimaryColor(jewelryId)
                        secondaryColor = ItemGlobals.getSecondaryColor(jewelryId)
                        holiday = ItemGlobals.getHoliday(id)
                        if location in range(Locations.RANGE_EQUIP_JEWELRY[0], Locations.RANGE_EQUIP_JEWELRY[1]):
                            equipped = True
                        jewelry.append([id, equipped, cost, jewelryId, primaryColor, secondaryColor, holiday, location])

        jewelry.sort(self.sortItems)
        jewelryAmount = 0
        startPos = Vec3(0.35, 0.0, 1.05)
        buttonScale = Vec3(0.6, 0.6, 0.6)
        for item in self.buttons:
            item.destroy()

        self.buttons = []
        self.jewelryAmount = 0
        self.buttonIndex = startIndex
        if self.mode == BUYING:
            self.storeButton['state'] = DGG.DISABLED
            self.wardrobeButton['state'] = DGG.NORMAL
            buttonColorA = Vec4(0.7, 0.95, 0.7, 1.0)
            buttonColorB = Vec4(0.4, 0.65, 0.4, 1.0)
            self.purchaseInventory.setItemColor(Vec4(0.3, 0.95, 0.3, 1.0))
        elif self.mode == SELLING:
            self.storeButton['state'] = DGG.NORMAL
            self.wardrobeButton['state'] = DGG.DISABLED
            buttonColorA = Vec4(0.95, 0.7, 0.7, 1.0)
            buttonColorB = Vec4(0.65, 0.4, 0.4, 1.0)
            self.sellInventory.setItemColor(Vec4(0.95, 0.3, 0.3, 1.0))
        self.reloadPirateDNA(self.pirate)
        regionData = []
        for jewel in jewelry:
            if self.jewelryAmount - startIndex < self.buttonsPerPage and self.jewelryAmount >= startIndex:
                uid = jewel[0]
                type = jewelryType
                combo = ItemGlobals.getMaleModelId(uid)
                desc = PLocalizer.getItemFlavorText(uid)
                cost = ItemGlobals.getGoldCost(uid)
                primaryColor = ItemGlobals.getPrimaryColor(uid)
                secondaryColor = ItemGlobals.getSecondaryColor(uid)
                owned = False
                equipped = jewel[1]
                questDrop = False
                location = jewel[7]
                if uid in JewelryGlobals.quest_items:
                    questDrop = True
                if self.mode == SELLING:
                    cost = int(cost * ItemGlobals.GOLD_SALE_MULTIPLIER)
                for item in self.currentWardrobe:
                    if uid == item:
                        owned = True

                if self.mode == SELLING:
                    buttonState = DGG.DISABLED
                else:
                    buttonState = DGG.NORMAL
                helpText = desc
                jewelryButton = GuiButton.GuiButton(command=self.setJewelry, parent=self.panel, state=buttonState, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(-0.02, -0.05), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, pos=startPos, image_scale=buttonScale, image_color=buttonColorA, helpText=helpText, helpDelay=0, helpPos=(0.0, 0.0, -0.11), helpLeftAlign=True, extraArgs=[self.pirate, type, uid])
                jewelryButton.helpWatcher.setPos(jewelryButton.getPos())
                jewelryButton.itemText = DirectFrame(parent=jewelryButton, relief=None, text='', text_fg=PiratesGuiGlobals.TextFG1, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleSmall, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=True, pos=(-0.13, 0, -0.085))
                if self.mode == BUYING and not owned:
                    jewelryButton.itemText['text'] = PLocalizer.TailorPreview
                elif self.mode == SELLING and equipped:
                    jewelryButton.itemText['text'] = PLocalizer.TattooShopOwned
                else:
                    if questDrop is True and self.mode == SELLING and not equipped:
                        jewelryButton.itemText['text'] = PLocalizer.ShopQuestItem
                    else:
                        jewelryButton.itemText['text'] = ''
                    jewelryButton.addToCart = GuiButton.GuiButton(command=self.addToCart, parent=jewelryButton, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image_color=buttonColorB, pos=(0.16,
                                                                                                                                                                                                                                                                                                                             0.0,
                                                                                                                                                                                                                                                                                                                             0.055))
                    jewelryButton.addToCart['extraArgs'] = [
                     jewelryButton, type, uid, location]
                    jewelryButton.bind(DGG.ENTER, self.highlightJewelryStart, extraArgs=[self.jewelryAmount])
                    jewelryButton.bind(DGG.EXIT, self.highlightJewelryStop, extraArgs=[self.jewelryAmount])
                    if self.mode == BUYING and not owned:
                        jewelryButton.cost = DirectFrame(parent=jewelryButton, relief=None, text=str(cost), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(-0.055, 0.0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, image=self.CoinImage, image_scale=0.15, image_pos=(-0.025,
                                                                                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                                                                                              0.015), pos=(0.25, 0, -0.05))
                    if not self.paid:
                        jewelryButton.addToCart['geom'] = self.LockIcon
                        jewelryButton.addToCart['geom_scale'] = 0.2
                        jewelryButton.addToCart['geom_pos'] = Vec3(-0.1, 0.0, 0.0)
                        jewelryButton.addToCart['command'] = localAvatar.guiMgr.showNonPayer
                        jewelryButton.addToCart['extraArgs'] = ['JEWELRY_CANNOT_BUY-SELL', 10]
                    data = [
                     type, uid, location]
                    if self.mode == BUYING and owned:
                        jewelryButton.addToCart.buyState = 0
                        jewelryButton.addToCart['state'] = DGG.DISABLED
                        jewelryButton['state'] = DGG.DISABLED
                        jewelryButton.addToCart['text'] = PLocalizer.TailorPurchased
                    elif self.mode == BUYING and self.purchaseInventory.hasPanel(data):
                        jewelryButton.addToCart.buyState = 0
                        jewelryButton.addToCart['state'] = DGG.NORMAL
                        jewelryButton.addToCart['text'] = PLocalizer.TailorRemove
                    elif self.mode == SELLING and self.sellInventory.hasPanel(data):
                        jewelryButton.addToCart.buyState = 0
                        jewelryButton.addToCart['state'] = DGG.NORMAL
                        jewelryButton.addToCart['text'] = PLocalizer.TailorRemove
                    else:
                        jewelryButton.addToCart.buyState = 1
                        jewelryButton.addToCart['state'] = DGG.NORMAL
                        if self.mode == BUYING:
                            jewelryButton.addToCart['text'] = PLocalizer.TailorAddToCart
                        if self.mode == SELLING:
                            jewelryButton.addToCart['text'] = PLocalizer.TailorSell
                startPos -= Vec3(0.0, 0.0, jewelryButton.getHeight() - 0.02)
                jewelryButton.jewelryType = jewelryType
                jewelryButton.jewelryCombo = combo
                jewelryButton.jewelryUID = uid
                jewelryButton.equipped = equipped
                jewelryButton.questDrop = questDrop
                jewelryButton.jewelryLocation = location
                regionData.append([jewelryType, uid])
                self.buttons.append(jewelryButton)
            self.jewelryAmount += 1

        if not len(jewelry):
            jewelryButton = GuiButton.GuiButton(parent=self.panel, state=DGG.DISABLED, text=PLocalizer.TailorEmptyWardrobe, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0,
                                                                                                                                                                         0.0), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, pos=startPos, image_scale=buttonScale, image_color=buttonColorA)
            jewelryButton.jewelryType = -1
            jewelryButton.jewelryCombo = -1
            jewelryButton.jewelryUID = -1
            self.buttons.append(jewelryButton)
        if len(jewelry):
            self.setupDisplayRegions(regionData, pageName)
        else:
            for item in self.clothRenders:
                item.hide()

            if self.jewelryAmount <= self.buttonsPerPage:
                self.nextPageButton['state'] = DGG.DISABLED
                self.prevPageButton['state'] = DGG.DISABLED
            if startIndex:
                self.prevPageButton['state'] = DGG.NORMAL
            if startIndex + self.buttonsPerPage < self.jewelryAmount:
                self.nextPageButton['state'] = DGG.NORMAL
                self.prevPageButton['state'] = DGG.NORMAL
            if self.jewelryAmount > self.buttonsPerPage:
                numPages = float(self.jewelryAmount) / float(self.buttonsPerPage)
                remainder = numPages - int(numPages)
                if remainder > 0:
                    numPages += 1.0 - remainder
                page = startIndex / self.buttonsPerPage + 1
            numPages = 1
            page = 1
        self.pageNumber['text'] = '%s %s / %s' % (PLocalizer.TailorPage, page, int(numPages))
        return

    def _stopMouseReadTask(self):
        taskMgr.remove('JewelryStore-MouseRead')

    def _startMouseReadTask(self):
        self._stopMouseReadTask()
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        taskMgr.add(self._mouseReadTask, 'JewelryStore-MouseRead')

    def _mouseReadTask(self, task):
        if not base.mouseWatcherNode.hasMouse():
            pass
        else:
            winSize = (
             base.win.getXSize(), base.win.getYSize())
            mouseData = base.win.getPointer(0)
            if mouseData.getX() > winSize[0] or mouseData.getY() > winSize[1]:
                pass
            else:
                dx = mouseData.getX() - self.lastMousePos[0]
                mouseData = base.win.getPointer(0)
                self.lastMousePos = (mouseData.getX(), mouseData.getY())
                value = self.rotateSlider['value']
                value = max(-1, min(1, value + dx * 0.004))
                self.rotateSlider['value'] = value
        return Task.cont

    def highlightJewelryStart(self, item, event=None):
        pass

    def highlightJewelryStop(self, item, event=None):
        pass

    def cleanupRegions(self):
        for item in self.clothWindows:
            base.win.removeDisplayRegion(item)
            item = None

        self.clothWindows = []
        for item in self.clothCameras:
            del item

        self.clothCameras = []
        for item in self.clothRenders:
            item.remove()
            item.removeNode()

        self.clothRenders = []
        for item in self.clothHumans:
            item.delete()
            item.remove()
            item.removeNode()

        self.clothHumans = []
        for item in self.clothCameraNPs:
            item.remove()
            item.removeNode()

        self.clothCameraNPs = []
        return

    def createDisplayRegions(self):
        startRegion = Vec4(0.526, 0.596, 0.62, 0.69)
        for x in range(self.buttonsPerPage):
            clothWindow = base.win.makeDisplayRegion(startRegion[0], startRegion[1], startRegion[2], startRegion[3])
            clothWindow.setSort(10)
            clothCamera = Camera('clothCamera' + str(x))
            clothRender = NodePath('clothRender' + str(x))
            clothHuman = DynamicHuman.DynamicHuman()
            clothHuman.setDNAString(localAvatar.style)
            clothHuman.generateHuman(localAvatar.style.gender)
            clothCameraNP = NodePath(clothCamera)
            clothCameraNP.reparentTo(clothRender)
            clothHuman.reparentTo(clothRender)
            clothWindow.setCamera(clothCameraNP)
            clothHuman.pose('idle', 1)
            clothHuman.dropShadow.hide()
            clothCamera.getLens().setAspectRatio(base.camLens.getAspectRatio())
            clothCamera.getLens().setNear(0.1)
            self.clothCameras.append(clothCamera)
            self.clothHumans.append(clothHuman)
            self.clothWindows.append(clothWindow)
            self.clothCameraNPs.append(clothCameraNP)
            self.clothRenders.append(clothRender)
            startRegion -= Vec4(0.0, 0.0, 0.12, 0.12)
            self.displayRegionStates[x] = True

    def setupDisplayRegions(self, regionData, pageName):
        bodyShape = localAvatar.style.getBodyShape()
        bodyOffset = 0.5
        if bodyShape == 0:
            bodyOffset = 0.5
        else:
            if bodyShape == 1:
                bodyOffset = 0.5
            else:
                if bodyShape == 2:
                    bodyOffset = 0.5
                elif bodyShape == 3:
                    bodyOffset = 0.5
                elif bodyShape == 4:
                    bodyOffset = 0.5
                x = 0
                m = Mat4(Mat4.identMat())
                rightEyeHeight = None
                leftEarHeight = None
                noseHeight = None
                mouthHeight = None
                leftIndexHeight = None
                rightIndexHeight = None
                gender = localAvatar.style.getGender()
                source = localAvatar
                source.pose('idle', 1)
                source.update()
                for x in range(len(regionData)):
                    if pageName == JewelryGlobals.RBROW:
                        if rightEyeHeight is None:
                            source.getLOD('2000').getChild(0).node().findJoint('trs_right_eyebrow').getNetTransform(m)
                            rightEyeHeight = TransformState.makeMat(m).getPos().getZ()
                        if gender == 'f':
                            offsetX = -0.3
                            offsetZ = -rightEyeHeight
                            offsetY = 0.4 + bodyOffset
                        else:
                            offsetX = -0.2
                            offsetZ = -rightEyeHeight * 0.99
                            offsetY = 0.3 + bodyOffset
                        offsetH = 230
                    elif pageName == JewelryGlobals.LBROW:
                        if rightEyeHeight is None:
                            source.getLOD('2000').getChild(0).node().findJoint('trs_right_eyebrow').getNetTransform(m)
                            rightEyeHeight = TransformState.makeMat(m).getPos().getZ()
                        if gender == 'f':
                            offsetX = 0.4
                            offsetZ = -rightEyeHeight
                            offsetY = 0.25 + bodyOffset
                        else:
                            offsetX = 0.3
                            offsetZ = -rightEyeHeight * 0.99
                            offsetY = 0.15 + bodyOffset
                        offsetH = -240
                    elif pageName == JewelryGlobals.REAR:
                        if leftEarHeight is None:
                            source.getLOD('2000').getChild(0).node().findJoint('def_trs_left_ear').getNetTransform(m)
                            leftEarHeight = TransformState.makeMat(m).getPos().getZ()
                        if gender == 'f':
                            offsetZ = -leftEarHeight
                            offsetY = 0.6 + bodyOffset
                            offsetX = -0.15
                        else:
                            offsetZ = -leftEarHeight * 0.99
                            offsetY = 0.5 + bodyOffset
                            offsetX = -0.04
                        offsetH = 250
                    elif pageName == JewelryGlobals.LEAR:
                        if leftEarHeight is None:
                            source.getLOD('2000').getChild(0).node().findJoint('def_trs_left_ear').getNetTransform(m)
                            leftEarHeight = TransformState.makeMat(m).getPos().getZ()
                        if gender == 'f':
                            offsetZ = -leftEarHeight
                            offsetY = 0.4 + bodyOffset
                            offsetX = 0.15
                        else:
                            offsetZ = -leftEarHeight * 0.99
                            offsetY = 0.3 + bodyOffset
                            offsetX = 0.04
                        offsetH = -250
                    elif pageName == JewelryGlobals.NOSE:
                        if noseHeight is None:
                            source.getLOD('2000').getChild(0).node().findJoint('def_trs_mid_nose_bot').getNetTransform(m)
                            noseHeight = TransformState.makeMat(m).getPos().getZ()
                        if gender == 'f':
                            offsetZ = -noseHeight - 0.01
                            offsetY = 0.45 + bodyOffset
                        else:
                            offsetZ = -noseHeight
                            offsetY = 0.4 + bodyOffset
                        offsetX = 0.06
                        offsetH = 180
                    elif pageName == JewelryGlobals.MOUTH:
                        if mouthHeight is None:
                            source.getLOD('2000').getChild(0).node().findJoint('trs_lips_top').getNetTransform(m)
                            mouthHeight = TransformState.makeMat(m).getPos().getZ()
                        offsetZ = -mouthHeight + 0.02
                        offsetY = 0.6 + bodyOffset
                        offsetX = 0.08
                        offsetH = 180
                    elif pageName == JewelryGlobals.LHAND:
                        if leftIndexHeight is None:
                            source.getLOD('2000').getChild(0).node().findJoint('def_left_index01').getNetTransform(m)
                            leftIndexHeight = TransformState.makeMat(m).getPos().getZ()
                        if gender == 'f':
                            offsetZ = -leftIndexHeight + 0.05
                            offsetX = -0.7
                            offsetY = 1.25 + bodyOffset
                        else:
                            offsetZ = -leftIndexHeight
                            if bodyShape == 4:
                                offsetX = -1.0
                                offsetY = 1.75 + bodyOffset
                            elif bodyShape == 3:
                                offsetX = -0.7
                                offsetY = 1.25 + bodyOffset
                            elif bodyShape == 1:
                                offsetX = -0.7
                                offsetY = 1.25 + bodyOffset
                            elif bodyShape == 0:
                                offsetX = -0.7
                                offsetY = 1.25 + bodyOffset
                            else:
                                offsetX = -0.8
                                offsetY = 1.25 + bodyOffset
                        offsetH = 160
                    elif pageName == JewelryGlobals.RHAND:
                        if rightIndexHeight is None:
                            source.getLOD('2000').getChild(0).node().findJoint('def_right_index01').getNetTransform(m)
                            rightIndexHeight = TransformState.makeMat(m).getPos().getZ()
                        if gender == 'f':
                            offsetZ = -rightIndexHeight + 0.05
                            offsetX = 0.8
                            offsetY = 1.25 + bodyOffset
                        else:
                            offsetZ = -rightIndexHeight
                            if bodyShape == 4:
                                offsetX = 1.0
                                offsetY = 1.75 + bodyOffset
                            elif bodyShape == 3:
                                offsetX = 0.7
                                offsetY = 1.25 + bodyOffset
                            elif bodyShape == 1:
                                offsetX = 0.7
                                offsetY = 1.25 + bodyOffset
                            elif bodyShape == 0:
                                offsetX = 0.7
                                offsetY = 1.25 + bodyOffset
                            else:
                                offsetX = 0.8
                                offsetY = 1.25 + bodyOffset
                        offsetH = 210
                    else:
                        offsetZ = 0.0
                        offsetY = 0.0
                        offsetX = 0.0
                        offsetH = 0
                    self.clothHumans[x].setX(offsetX)
                    self.clothHumans[x].setY(offsetY)
                    self.clothHumans[x].setZ(offsetZ)
                    self.clothHumans[x].setH(offsetH)
                    self.reloadPirateDNA(self.clothHumans[x])
                    type = regionData[x][0]
                    uid = regionData[x][1]
                    combo = ItemGlobals.getMaleModelId(uid)
                    self.setJewelry(self.clothHumans[x], type, uid)
                    self.clothHumans[x].style.setClothesHat(0, 0)
                    self.clothHumans[x].model.handleHeadHiding()
                    self.clothRenders[x].show()

            x = len(regionData)
            if x < self.buttonsPerPage:
                for y in range(self.buttonsPerPage - x):
                    self.clothRenders[self.buttonsPerPage - 1 - y].hide()

        self.aspectRatioChange()
        return

    def showWardrobeLimitAlert(self, type):
        self.removeAlertDialog()
        limit = str(PiratesGlobals.WARDROBE_LIMIT_JEWELER)
        text = PLocalizer.ShopLimitJewelry % limit
        self.alertDialog = PDialog.PDialog(text=text, text_align=TextNode.ACenter, style=OTPDialog.Acknowledge, pos=(-0.65, 0.0, 0.0), command=self.removeAlertDialog)
        self.alertDialog.setBin('gui-fixed', 3, 3)

    def removeAlertDialog(self, value=None):
        if self.alertDialog:
            self.alertDialog.destroy()
            self.alertDialog = None
        return

    def getJewelryGlobalsType(self, id):
        itemType = ItemGlobals.getType(id)
        if itemType == ItemGlobals.BROW:
            return JewelryGlobals.LBROW
        elif itemType == ItemGlobals.EAR:
            return JewelryGlobals.LEAR
        elif itemType == ItemGlobals.NOSE:
            return JewelryGlobals.NOSE
        elif itemType == ItemGlobals.MOUTH:
            return JewelryGlobals.MOUTH
        elif itemType == ItemGlobals.HAND:
            return JewelryGlobals.LHAND

    def getItemGlobalsType(self, type):
        if type in (JewelryGlobals.LBROW, JewelryGlobals.RBROW):
            return ItemGlobals.BROW
        elif type in (JewelryGlobals.LEAR, JewelryGlobals.REAR):
            return ItemGlobals.EAR
        elif type == JewelryGlobals.NOSE:
            return ItemGlobals.NOSE
        elif type == JewelryGlobals.MOUTH:
            return ItemGlobals.MOUTH
        elif type in (JewelryGlobals.LHAND, JewelryGlobals.RHAND):
            return ItemGlobals.HAND