from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.ai import HolidayGlobals
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import ItemType
from pirates.holiday import CatalogHoliday
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import GuiPanel, RedeemCodeGUI
from pirates.piratesgui import GuiButton, DialogButton
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiButton
from pirates.pirate import DynamicHuman
from pirates.pirate import Human
from pirates.pirate import HumanDNA
from pirates.piratesgui.TabBar import LeftTab, TabBar
from direct.interval.IntervalGlobal import *
from pirates.makeapirate import ClothingGlobals
from pirates.makeapirate import TattooGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from direct.task import Task
from pirates.piratesbase import Freebooter
from pirates.piratesgui.InventoryItemGui import InventoryItemGui
from pirates.inventory.InventoryGlobals import *
from pirates.uberdog.TradableInventoryBase import InvItem
from pirates.inventory import ItemGlobals, DropGlobals
from pirates.inventory import ItemConstants
from pirates.inventory import InventoryUIStoreContainer
from pirates.pirate import AvatarTypes
from pirates.economy.SimpleStoreItem import *
import random
from math import sin
from math import cos
from math import pi
import time

class SimpleStoreTab(LeftTab):

    def __init__(self, tabBar, name, **kw):
        optiondefs = (
         ('modelName', 'general_frame_d', None), ('borderScale', 0.38, None), ('bgBuffer', 0.15, None))
        self.defineoptions(kw, optiondefs)
        LeftTab.__init__(self, tabBar, name, **kw)
        self.initialiseoptions(SimpleStoreTab)
        return None


class SimpleStoreTabBar(TabBar):

    def hasTabs(self):
        return len(self.getOrder()) > 0

    def refreshTabs(self):
        for x, name in enumerate(self.tabOrder):
            tab = self.tabs[name]
            tab.reparentTo(self.bParent)
            tab.setPos(-0.07, 0, 1.08 - 0.15 * (x + self.offset))
            (tab.setScale(0.22, 1, 0.235),)

        self.activeIndex = max(0, min(self.activeIndex, len(self.tabOrder) - 1))
        if len(self.tabOrder):
            name = self.tabOrder[self.activeIndex]
            tab = self.tabs[name]
            tab.reparentTo(self.fParent)
            tab.setX(-0.08)
            tab.setScale(0.23, 1, 0.27)

    def makeTab(self, name, **kw):
        return SimpleStoreTab(self, name, **kw)


class SimpleStoreColorPicker(BorderFrame):
    sizeX = 0.65
    sizeZ = 0.25

    def __init__(self, store, parentFrame, item, **kw):
        optiondefs = (
         (
          'state', DGG.DISABLED, None), ('frameSize', (-0.5 * self.sizeX, 0.5 * self.sizeX, -0.5 * self.sizeZ, 0.5 * self.sizeZ), None), ('modelName', 'pir_m_gui_frm_subframe', None), ('imageColorScale', VBase4(0.75, 0.75, 0.9, 0.75), None))
        self.defineoptions(kw, optiondefs)
        BorderFrame.__init__(self, parent=parentFrame)
        self.store = store
        self.item = item
        self.colorButtons = []
        self.selectedColor = None
        self._parent = parentFrame
        self.setup()
        return

    def setup(self):
        self.setBin('gui-fixed', 1)
        offsetx = -0.5 * self.sizeX + 0.12
        offsety = 0.5 * self.sizeZ - 0.055
        colorSet = colorsNotOwned = range(0, 21)
        numcolors = len(colorsNotOwned)
        colorsOwned = []
        charGui = loader.loadModel('models/gui/char_gui')
        for idx in range(0, numcolors):
            color = colorSet[idx]
            colorButton = GuiButton.GuiButton(parent=self, pos=(offsetx, 0.0, offsety), image=(charGui.find('**/chargui_frame04'), charGui.find('**/chargui_frame04_down'), charGui.find('**/chargui_frame04_over')), image_scale=(0.115, 0.0, 0.088), helpText=PLocalizer.TailorColorStrings.get(color), helpDelay=0, command=self.selectColor)
            colorFrame = DirectFrame(parent=colorButton, frameSize=(-0.025, 0.025, -0.025, 0.025))
            colorButton['extraArgs'] = [
             color]
            colorFrame['frameColor'] = ItemConstants.DYE_COLORS[color]
            offsetx += 0.07
            if idx != 0 and (idx + 1) % 7 == 0:
                offsetx = -0.5 * self.sizeX + 0.12
                offsety -= 0.07
            self.colorButtons.append(colorButton)
            if idx in colorsOwned:
                colorButton['state'] = DGG.DISABLED
                colorButton['image_color'] = Vec4(0.5, 0.5, 0.5, 0.5)
                colorFrame.setColorScale(0.5, 0.5, 0.5, 0.5)

    def destroy(self):
        self._parent = None
        for button in self.colorButtons:
            button.destroy()

        self.colorButtons = []
        BorderFrame.destroy(self)
        return

    def selectColor(self, colorId):
        if self.selectedColor:
            self.selectedColor.setScale(1.0)
            self.selectedColor['image_color'] = VBase4(1, 1, 1, 1)
            self.selectedColor['state'] = DGG.NORMAL
        self.selectedColor = self.colorButtons[colorId]
        self.selectedColor.setScale(1.2)
        self.selectedColor['image_color'] = VBase4(1, 1, 0, 1)
        self.selectedColor['state'] = DGG.DISABLED
        if self.store.previewPirate:
            self.item.unapply(self.store.previewPirate, localAvatar.style)
            self.item.colorId = colorId
            self.item.apply(self.store.previewPirate)
        self.store.invContainer.getItem(self.item.uid).setColorId(colorId)
        self.store.showClicked()


class SimpleStoreBuyPanelGUI(BorderFrame):
    sizeX = 0.65
    sizeZ = 0.25

    def __init__(self, store, parentFrame, item, purchasable=False, **kw):
        optiondefs = (('state', DGG.DISABLED, None), ('frameSize', (-0.5 * self.sizeX, 0.5 * self.sizeX, -0.65 * self.sizeZ, 0.5 * self.sizeZ), None), ('modelName', 'pir_m_gui_frm_subframe', None), ('imageColorScale', VBase4(0.75, 0.75, 0.9, 0.75), None))
        self.defineoptions(kw, optiondefs)
        BorderFrame.__init__(self, parent=parentFrame)
        self.store = store
        self.item = item
        self.purchasable = purchasable
        self.ownedLabel = None
        self.qtyLabel = None
        self.qtyText = None
        self.minusButton = None
        self.plusButton = None
        self.costLabel = None
        self.costText = None
        self.buyButton = None
        self.setPending(0)
        self.setupGui()
        return

    def setPending(self, pending):
        self.pending = pending
        taskMgr.remove('simpleStoreBuyPanelPurchasePending')
        if pending:
            taskMgr.doMethodLater(10.0, self.handlePurchaseTimeout, 'simpleStoreBuyPanelPurchasePending')

    def handlePurchaseTimeout(self, task=None):
        self.setPending(0)
        localAvatar.guiMgr.createWarning(PLocalizer.PurchaseTimeout, PiratesGuiGlobals.TextFG6)
        self.updateGui()

    def destroy(self):
        taskMgr.remove('simpleStoreBuyPanelPurchasePending')
        self.store = None
        self.item = None
        self.purchasable = None
        if self.qtyLabel:
            self.qtyLabel.destroy()
            self.qtyLabel = None
        if self.qtyText:
            self.qtyText.destroy()
            self.qtyText = None
        if self.minusButton:
            self.minusButton.destroy()
            self.minusButton = None
        if self.plusButton:
            self.plusButton.destroy()
            self.plusButton = None
        if self.costLabel:
            self.costLabel.destroy()
            self.costLabel = None
        if self.costText:
            self.costText.destroy()
            self.costText = None
        if self.buyButton:
            self.buyButton.destroy()
            self.buyButton = None
        BorderFrame.destroy(self)
        return

    def setupGui(self):
        inventory = base.localAvatar.getInventory()
        qtyLimit = ItemGlobals.getStackLimit(self.item.uid)
        if not qtyLimit:
            qtyLimit = inventory.getStackLimit(self.item.uid)
        freeSpace = qtyLimit - self.item.getQuantityInInventory()
        stackable = self.item.checkStackable()
        if stackable:
            qtyMult = max(1, EconomyGlobals.getItemQuantity(self.item.uid))
            qtyLimit = ItemGlobals.getStackLimit(self.item.uid)
            if not qtyLimit:
                qtyLimit = inventory.getStackLimit(self.item.uid)
            self.item.quantity = freeSpace
        else:
            qtyMult = 1
            qtyLimit = 10

        def plusQuantity():
            inventory = base.localAvatar.getInventory()
            self.item.quantity += qtyMult
            self.updateGui()

        def minusQuantity():
            inventory = base.localAvatar.getInventory()
            self.item.quantity -= qtyMult
            self.updateGui()

        self.qtyLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=PLocalizer.SimpleStoreQty, text_font=PiratesGlobals.getInterfaceFont(), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, text_pos=(0, 0, 0), pos=(-0.2, 0, 0.015))
        self.minusButton = GuiButton.GuiButton(parent=self, text='-', text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.014), text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image=GuiButton.GuiButton.blueGenericButton, image_scale=(0.125, 0.36, 0.36), pos=(0.04, 0.0, 0.028), command=minusQuantity)
        if self.item.quantity == qtyMult:
            self.minusButton['state'] = DGG.DISABLED
        self.plusButton = GuiButton.GuiButton(parent=self, text='+', text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.014), text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image=GuiButton.GuiButton.blueGenericButton, image_scale=(0.125, 0.36, 0.36), pos=(0.18, 0.0, 0.038), command=plusQuantity)
        if self.item.quantity == qtyLimit:
            self.plusButton['state'] = DGG.DISABLED
        self.qtyText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=str(self.item.quantity), text_font=PiratesGlobals.getInterfaceFont(), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ARight, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, text_pos=(0, 0, 0), pos=(0.14, 0, 0.015), textMayChange=1)
        self.qtyFullText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=PLocalizer.SimpleStoreFull, text_font=PiratesGlobals.getInterfaceFont(), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, text_pos=(0, 0, 0), pos=(0.17, 0, 0.015), textMayChange=1)
        self.qtyFullText.hide()
        quantity = self.item.getQuantityInInventory()
        if stackable:
            freeSpace = qtyLimit - self.item.getQuantityInInventory()
        else:
            freeSpace = len(localAvatar.getInventory().getFreeLocations(self.item.itemClass, self.item.itemType))
        if self.item.quantity > freeSpace:
            self.qtyText['text_fg'] = VBase4(1, 0, 0, 1)
        self.ownedLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=PLocalizer.SimpleStoreOwned + ' %s' % quantity, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, text_pos=(0, 0, 0.0), pos=(-0.2, 0, 0.08), text_font=PiratesGlobals.getInterfaceFont(), textMayChange=1)
        totalCost = int(self.item.cost * qtyMult) * self.item.quantity / qtyMult
        costText = PLocalizer.ShopFree if self.item.cost == 0 else str(totalCost)
        self.costLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, image=self.store.CoinImage, image_scale=0.15, image_pos=Vec3(0.38, 0, 0.012), text=PLocalizer.SimpleStoreCost, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, text_pos=(0, 0, 0.0), pos=(-0.2, 0, -0.05), text_font=PiratesGlobals.getInterfaceFont(), textMayChange=1)
        self.costText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=str(costText), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ARight, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, text_pos=(0, 0, 0.0), pos=(0.14, 0, -0.05), text_font=PiratesGlobals.getInterfaceFont())
        totalMoney = localAvatar.getInventory().getGoldInPocket()
        if totalCost > totalMoney:
            self.costText['text_fg'] = VBase4(1, 0, 0, 1)
        self.buyButton = GuiButton.GuiButton(parent=self, text=PLocalizer.PurchaseCommit, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.014), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image=GuiButton.GuiButton.blueGenericButton, image_scale=(0.6, 0.6, 0.6), pos=(0.0, 0.0, -0.115), command=self.store.handleBuyItem)
        if not self.purchasable:
            self.buyButton.hide()
        self.updateGui()
        self.store.npc.resumeShopping()
        return

    def updateGui(self):
        if self.item == None:
            return
        if self.item.quantity < 0:
            self.item.quantity = 0
        inventory = base.localAvatar.getInventory()
        quantity = self.item.getQuantityInInventory()
        inventory = base.localAvatar.getInventory()
        qtyLimit = ItemGlobals.getStackLimit(self.item.uid)
        if not qtyLimit:
            qtyLimit = inventory.getStackLimit(self.item.uid)
        freeSpace = None
        stackable = self.item.checkStackable()
        if stackable:
            freeSpace = qtyLimit - self.item.getQuantityInInventory()
        else:
            freeSpace = len(localAvatar.getInventory().getFreeLocations(self.item.itemClass, self.item.itemType))
        if self.item.quantity > freeSpace:
            self.item.quantity = freeSpace
        if stackable:
            qtyMult = max(1, EconomyGlobals.getItemQuantity(self.item.uid))
            qtyLimit = ItemGlobals.getStackLimit(self.item.uid)
            if not qtyLimit:
                qtyLimit = inventory.getStackLimit(self.item.uid)
            self.ownedLabel['text'] = PLocalizer.SimpleStoreOwned + '  %s / %s' % (quantity, qtyLimit)
            self.qtyFullText['text'] = PLocalizer.SimpleStoreFull
        else:
            qtyMult = 1
            qtyLimit = 10
            self.ownedLabel['text'] = PLocalizer.SimpleStoreOwned + '  %s' % quantity
            self.qtyFullText['text'] = PLocalizer.SimpleStoreFullNonStack
        full = 0
        self.plusButton['state'] = DGG.NORMAL
        self.plusButton.show()
        self.buyButton['state'] = DGG.NORMAL
        if self.item.quantity >= freeSpace:
            full = 1
            self.plusButton['state'] = DGG.DISABLED
            self.plusButton.hide()
        self.minusButton['state'] = DGG.NORMAL
        self.minusButton.show()
        if self.item.quantity <= 0:
            self.minusButton['state'] = DGG.DISABLED
            self.minusButton.hide()
        if self.item.quantity > freeSpace:
            self.qtyText['text_fg'] = VBase4(1, 0, 0, 1)
        else:
            self.qtyText['text_fg'] = VBase4(1, 1, 1, 1)
        if full:
            self.qtyFullText.show()
        else:
            self.qtyFullText.hide()
        self.qtyText['text'] = '%s' % self.item.quantity
        if self.item.cost:
            totalCost = int(self.item.cost * qtyMult) * self.item.quantity / qtyMult
            self.costText['text'] = str(totalCost)
            totalMoney = localAvatar.getInventory().getGoldInPocket()
            if totalCost > totalMoney:
                self.costText['text_fg'] = VBase4(1, 0, 0, 1)
            else:
                self.costText['text_fg'] = VBase4(1, 1, 1, 1)
        if self.pending:
            self.buyButton['state'] = DGG.DISABLED
            self.buyButton['text'] = PLocalizer.PurchasePending
        elif self.item.quantity == 0:
            self.buyButton['state'] = DGG.DISABLED
            self.buyButton['text'] = PLocalizer.PurchaseCommit
        else:
            self.buyButton['state'] = DGG.NORMAL
            self.buyButton['text'] = PLocalizer.PurchaseCommit
        return


class SimpleStoreGUI(DirectFrame):
    notify = directNotify.newCategory('SimpleStoreGUI')
    guiPos = (0.625, 0.0, -0.05)
    guiWidth = 1.25
    guiHeight = 1.35
    buyPanelXFactor = -0.182
    buyPanelZFactor = -0.375
    storeIconName = None
    holidayIdList = []
    itemGlobalsClasses = {InventoryType.ItemTypeClothing: SimpleClothingItem,InventoryType.ItemTypeJewelry: SimpleJewelryItem,InventoryType.ItemTypeTattoo: SimpleTattooItem,InventoryType.ItemTypeWeapon: SimpleWeaponItem,InventoryType.ItemTypeConsumable: SimpleConsumableItem,ItemType.DAGGERAMMO: SimpleAmmoItem,ItemType.PISTOLAMMO: SimpleAmmoItem,ItemType.CANNONAMMO: SimpleAmmoItem,ItemType.GRENADEAMMO: SimpleAmmoItem,ItemType.PISTOL_POUCH: SimplePouchItem,ItemType.DAGGER_POUCH: SimplePouchItem,ItemType.GRENADE_POUCH: SimplePouchItem,ItemType.CANNON_POUCH: SimplePouchItem,ItemType.FISHING_POUCH: SimplePouchItem,ItemType.FISHING_LURE: SimpleFishingLureItem}

    def __init__(self, storeName, npc=None, shopId=None, **kw):
        optiondefs = (
         ('relief', None, None), ('frameSize', (-self.guiWidth / 2, self.guiWidth / 2, -self.guiHeight / 2, self.guiHeight / 2), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, None, **kw)
        self.confirmDialog = None
        self.rollInItem = None
        self.rollInItemTask = None
        self.clickedItem = None
        self.previewItem = None
        self.buyPanelItem = None
        self.camIval = None
        self.initialiseoptions(SimpleStoreGUI)
        self.npc = npc
        self.storeName = storeName
        self.shopId = shopId
        self.pvpMode = 0
        if shopId == PiratesGlobals.PRIVATEER_HATS:
            self.pvpMode = 1
        self.paid = Freebooter.getPaidStatus(localAvatar.getDoId())
        self.previewPirate = None
        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()
        self.initialCamPos = camera.getPos()
        self.initialCamHpr = camera.getHpr()
        self.initialPirateH = 0
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.CoinImage = gui.find('**/treasure_w_coin*')
        skullModel = loader.loadModel('models/gui/avatar_chooser_rope')
        self.RenownImage = skullModel.find('**/avatar_c_B_delete')
        self.ParchmentIcon = None
        self.TailorIcons = loader.loadModel('models/textureCards/tailorIcons')
        self.ShirtIcon = loader.loadModel('models/gui/char_gui').find('**/chargui_cloth')
        self.LockIcon = gui.find('**/pir_t_gui_gen_key_subscriber')
        self.ColorPickerIcon = gui.find('**/pir_t_gui_gen_colorPicker')
        self.redeemCodeGUI = None
        self.invContainer = None
        self.itemCardPlaceholder = None
        self.storeIcon = None
        self.instructionText = None
        self.setPos(*self.guiPos)
        self.backTabParent = self.attachNewNode('backTabs', sort=0)
        self.backTabParent.setPos(-0.5 * self.guiWidth, 0.0, -0.4 * self.guiHeight)
        textScale = PiratesGuiGlobals.TextScaleTitleSmall
        self.cartFrame = BorderFrame(parent=self, state=DGG.DISABLED, frameSize=(-self.guiWidth / 2, self.guiWidth / 2, -self.guiHeight / 2, self.guiHeight / 2), text=PLocalizer.InventorySellTitle, text_align=TextNode.ACenter, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=(1, 1, 1, 1), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, text_scale=textScale, text_pos=(self.guiWidth * 0.5, self.guiHeight * 0.95 - textScale), modelName='pir_m_gui_frm_main_blue', showHeadBoard=True, nameTag='---')
        self.cartFrame.setPos(0.0, 0.0, 0.0)
        self.frontTabParent = self.attachNewNode('frontTab', sort=2)
        self.frontTabParent.setPos(-0.5 * self.guiWidth, 0.0, -0.4 * self.guiHeight)
        currencyIcon = self.RenownImage if self.pvpMode else self.CoinImage
        self.myGold = DirectFrame(parent=self.cartFrame, relief=None, text='000000', text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0, 0), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, image=currencyIcon, image_scale=0.15, image_pos=(0.2, 0, 0.014), pos=(0.25 * self.guiWidth, 0, -0.35 * self.guiHeight))
        self.sellButton = GuiButton.GuiButton(parent=self.cartFrame, text=PLocalizer.SimpleStoreSell, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.014), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image=GuiButton.GuiButton.blueGenericButton, image_scale=(0.6, 0.6, 0.6), command=self.showSellGUI)
        self.sellButton.setPos(0.28 * self.guiWidth, 0, -0.4 * self.guiHeight)
        charGui = loader.loadModel('models/gui/char_gui')
        self.rotateSlider = DirectSlider(parent=base.a2dBottomLeft, relief=None, command=self.rotatePreviewPirate, image=charGui.find('**/chargui_slider_small'), image_scale=(2.15, 2.15, 1.5), thumb_relief=None, thumb_image=(charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), pos=(0.8, 0.0, 0.09), text_align=TextNode.ACenter, text_scale=(0.1, 0.1), text_pos=(0.0, 0.1), text_fg=PiratesGuiGlobals.TextFG1, scale=0.43, text=PLocalizer.RotateSlider, value=0.5, sortOrder=-1)
        self.rotateSlider['extraArgs'] = [self.rotateSlider]
        self.rotateSliderOrigin = 0.5
        self.alertDialog = None
        self.accept('mouse1', self._startMouseReadTask)
        self.accept('mouse1-up', self._stopMouseReadTask)
        localAvatar.guiMgr.chatPanel.show()
        localAvatar.guiMgr.chatPanel.startFadeTextIval()
        self.accept(localAvatar.uniqueName('accessoriesUpdate'), self.reloadPirateDNA)
        merchIds = self.getMerchandiseIds()
        self.stock = self.getStockItems(merchIds)
        self.stock = self.removeHolidayItems(self.stock)
        self.stock = self.filterStockItems(self.stock, localAvatar)
        self.createItemCardPlaceholder()
        self.createPreviewPirate()
        self.focusCamera()
        self.setupPanel()
        self.initTabs()
        self.updateBalance()
        self.lastRun = 0
        self.showQuestLabel = False
        if localAvatar.guiMgr.questPage:
            if not localAvatar.guiMgr.trackedQuestLabel.isHidden():
                localAvatar.guiMgr.hideTrackedQuestInfo()
                self.showQuestLabel = True
        main_gui = loader.loadModel('models/gui/gui_main')
        generic_x = main_gui.find('**/x2')
        generic_box = main_gui.find('**/exit_button')
        generic_box_over = main_gui.find('**/exit_button_over')
        main_gui.removeNode()
        self.closeButton = GuiButton.GuiButton(parent=self, relief=None, pos=(0.83, 0, -0.14), image=(generic_box, generic_box, generic_box_over, generic_box), image_scale=0.4, command=self.closePanel)
        self.xButton = OnscreenImage(parent=self.closeButton, image=generic_x, scale=0.2, pos=(-0.256, 0, 0.766))
        self.accept('TownfolkEndingInteract', self.closePanel)
        return

    def setupPanel(self):
        self.buyPanel = None
        self.colorPanel = None
        return

    def setupGrid(self, gridX=3, gridZ=7):
        if self.invContainer:
            self.invContainer.destroy()
            self.invContainer = None
        imageScale = 0.135
        self.gridX = gridX
        self.gridZ = gridZ
        self.invContainer = InventoryUIStoreContainer.InventoryUIStoreContainer(self, localAvatar.guiMgr.inventoryUIManager, sizeX=imageScale * self.gridX, sizeZ=imageScale * self.gridZ, countX=self.gridX, countZ=self.gridZ)
        self.invContainer.setPos(0.118 * self.guiWidth, 0, -0.275 * self.guiHeight)
        self.invContainer.reparentTo(self.cartFrame)
        return

    def changeMode(self, mode, refresh=True):
        pass

    def showSellGUI(self):
        self.hide()
        self.npc.startSellItems(push=True)

    def purchaseConfirmation(self):
        pass

    def showBuyGUI(self):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        self.confirmDialog = PDialog.PDialog(pos=(-1, 0, 0), text=PLocalizer.InventoryBuyMessage, style=OTPDialog.YesNo, command=self.handleBuyItem)
        return

    def rotatePreviewPirate(self, slider):
        if self.previewPirate and slider:
            value = slider.getValue()
            if value != self.rotateSliderOrigin:
                diff = value - self.rotateSliderOrigin
                h = diff * 360.0 + self.previewPirate.getH()
                self.previewPirate.setH(h)
                self.rotateSliderOrigin = value

    def destroy(self):
        localAvatar.guiMgr.inventoryUIManager.cancelCellItemDetails()
        self.ignoreAll()
        DirectFrame.destroy(self)
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        self._stopMouseReadTask()
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
            camera.setHpr(0, 0, 0)
        self.rotateSlider.destroy()
        self.unloadPirate()
        if self.CoinImage:
            self.CoinImage.removeNode()
            self.CoinImage = None
        if self.ParchmentIcon:
            self.ParchmentIcon.removeNode()
            self.ParchmentIcon = None
        if self.TailorIcons:
            self.TailorIcons.removeNode()
            self.TailorIcons = None
        if self.ShirtIcon:
            self.ShirtIcon.removeNode()
            self.ShirtIcon = None
        if self.LockIcon:
            self.LockIcon.removeNode()
            self.LockIcon = None
        if self.alertDialog:
            self.alertDialog.destroy()
        if self.redeemCodeGUI:
            self.redeemCodeGUI.destroy()
        if len(localAvatar.guiMgr.trackedQuestLabel['text']):
            if self.showQuestLabel:
                localAvatar.guiMgr.showTrackedQuestInfo()
        localAvatar.guiMgr.chatPanel.hide()
        if self.closeButton:
            self.closeButton.destroy()
            self.closeButton = None
        if self.xButton:
            self.xButton.destroy()
            self.xButton = None
        if self.invContainer:
            self.invContainer.destroy()
            self.invContainer = None
        return

    def createItemCardPlaceholder(self):
        if not self.itemCardPlaceholder:
            sizeX = 0.65
            sizeZ = 0.88
            self.itemCardPlaceholder = BorderFrame(parent=self.cartFrame, state=DGG.DISABLED, frameSize=(-0.5 * sizeX, 0.5 * sizeX, -0.5 * sizeZ, 0.5 * sizeZ), imageColorScale=(0.75, 0.75, 0.9, 0.75), modelName='pir_m_gui_frm_subframe')
            self.itemCardPlaceholder.setPos(self.buyPanelXFactor * self.guiWidth, 0.0, 0.125)
        if self.storeIconName and not self.storeIcon:
            storeIcon = loader.loadModel(self.storeIconName)
            self.storeIcon = storeIcon.copyTo(self.itemCardPlaceholder)
            self.storeIcon.getChildren()[0].setH(90)
            self.storeIcon.getChildren()[0].setPos(1.933 * 2, 0, 1.55 * 2)
            self.storeIcon.setScale(0.1)
            storeIcon.removeNode()
        self.titleText = DirectLabel(parent=self.itemCardPlaceholder, relief=None, state=DGG.DISABLED, text='', text_font=PiratesGlobals.getInterfaceFont(), text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=14, text_pos=(0, 0, 0), pos=(0.0, 0.0, -0.505))
        self.instructionText = DirectLabel(parent=self.itemCardPlaceholder, relief=None, state=DGG.DISABLED, text=PLocalizer.SimpleStoreClickPreview, text_font=PiratesGlobals.getInterfaceFont(), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=14, text_pos=(0, 0, 0), pos=(0.0, 0.0, -0.55))
        return

    def createPreviewPirate(self):
        self.previewPirate = DynamicHuman.DynamicHuman()
        self.previewPirate.isPaid = localAvatar.isPaid
        self.previewPirate.setDNAString(localAvatar.style)
        self.previewPirate.generateHuman(localAvatar.style.gender)
        self.previewPirate.model.setupSelectionChoices('DEFAULT')
        self.previewPirate.mixingEnabled = True
        self.previewPirate.enableBlend()
        self.previewPirate.loop('idle')
        self.previewPirate.useLOD(2000)
        dummy = self.npc.attachNewNode('dummy')
        dummy.setPos(self.npc.getPos() - Vec3(0, 7, 0))
        parent = self.npc.getParent()
        self.previewPirate.reparentTo(parent)
        pos = dummy.getPos()
        hpr = dummy.getHpr()
        self.previewPirate.setPos(pos)
        self.previewPirate.setHpr(hpr)
        self.previewPirate.lookAt(self.npc)
        dummy.detachNode()
        self.initialPirateH = self.previewPirate.getH()
        self.previewPirate.show()
        localAvatar.stash()

    def unloadPirate(self):
        if self.previewPirate:
            self.previewPirate.detachNode()
            self.previewPirate.cleanupHuman()
            self.previewPirate.delete()
            self.previewPirate = None
        localAvatar.unstash()
        return

    def setPreviewItem(self, itemId):
        if self.buyPanel:
            self.buyPanel.updateGui()
        if self.previewItem and self.previewItem.uid == itemId:
            return
        if self.previewItem:
            self.previewItem.unapply(self.previewPirate, localAvatar.style)
        item = self.stock.get(itemId)
        self.previewItem = item
        if not self.previewItem:
            return
        self.previewItem.apply(self.previewPirate)
        gender = localAvatar.style.getGender()
        if self.previewItem.itemClass == InventoryType.ItemTypeClothing:
            if self.previewItem.itemType == ClothingGlobals.SHIRT and gender == 'f':
                vestIdx = localAvatar.style.getClothesVest()[0]
                if vestIdx in [3, 4]:
                    self.showCutOffVestAlert()
        currTime = globalClock.getFrameTime()
        if currTime - self.lastRun > 10:
            flavorAnim = self.previewItem.getFlavorAnim()
            self.previewPirate.play(flavorAnim)
            self.lastRun = currTime
        self.focusCamera()

    def reloadPirateDNA(self):
        if self.previewPirate is None:
            self.createPreviewPirate()
        self.setPreviewItem(None)
        return

    def focusCamera(self):
        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
        self.previewPirate.setH(self.initialPirateH)
        self.rotateSlider['value'] = self.rotateSliderOrigin = 0.5
        dummy = self.previewPirate.attachNewNode('dummy')
        if self.previewItem:
            dummy.setPos(dummy, self.previewItem.getCameraPos(self.previewPirate))
            dummy.wrtReparentTo(render)
            dummy.lookAt(self.previewPirate, self.previewItem.getCameraLookAtPos(self.previewPirate))
        else:
            dummy.setPos(dummy, 0, 10, self.previewPirate.headNode.getZ(self.previewPirate))
            dummy.wrtReparentTo(render)
            dummy.lookAt(self.previewPirate, self.previewPirate.headNode.getX(self.previewPirate), self.previewPirate.headNode.getY(self.previewPirate), self.previewPirate.headNode.getZ(self.previewPirate) * 0.9)
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
        if self.camIval and self.camIval.endPos == camPos and self.camIval.endHpr == camHpr:
            return
        t = 1.5
        self.camIval = camera.posHprInterval(t, pos=camPos, hpr=camHpr, blendType='easeOut')
        localAvatar.cameraFSM.request('Control')
        self.camIval.start()
        return

    def _stopMouseReadTask(self):
        taskMgr.remove('SimpleStore-MouseRead')

    def _startMouseReadTask(self):
        self._stopMouseReadTask()
        mouseData = base.win.getPointer(0)
        self.lastMousePos = (mouseData.getX(), mouseData.getY())
        taskMgr.add(self._mouseReadTask, 'SimpleStore-MouseRead')

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

    def showWardrobeLimitAlert(self, type):
        self.reloadPirateDNA()
        self.removeAlertDialog()
        limit = str(PiratesGlobals.WARDROBE_LIMIT_TAILOR)
        text = PLocalizer.ShopLimitTailor % limit
        self.alertDialog = PDialog.PDialog(text=text, text_align=TextNode.ACenter, style=OTPDialog.Acknowledge, pos=(-0.65, 0.0, 0.0), command=self.removeAlertDialog)
        self.alertDialog.setBin('gui-fixed', 3, 3)

    def removeAlertDialog(self, value=None):
        if self.alertDialog:
            self.alertDialog.destroy()
            self.alertDialog = None
        return

    def getMoney(self):
        inventory = base.localAvatar.getInventory()
        if not inventory:
            return 0
        if self.pvpMode:
            return inventory.getStackQuantity(InventoryType.PVPCurrentInfamy)
        return inventory.getGoldInPocket()

    def getMaxMoney(self, inventory):
        if not inventory:
            return 0
        if self.pvpMode:
            return inventory.getStackLimit(InventoryType.PVPCurrentInfamy)
        return GOLD_CAP

    def closePanel(self):
        messenger.send('exitStore')
        self.ignoreAll()
        camera.setPos(self.initialCamPos)
        camera.setHpr(self.initialCamHpr)
        self.unloadPirate()
        if not hasattr(base, 'localAvatar'):
            return

    def handleBuyItem(self, value=DGG.DIALOG_YES):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if value != DGG.DIALOG_YES:
            return
        if not self.buyPanelItem:
            base.localAvatar.guiMgr.createWarning(PLocalizer.EmptyPurchaseWarning, PiratesGuiGlobals.TextFG6)
            return
        stackable = self.buyPanelItem.checkStackable()
        inventory = base.localAvatar.getInventory()
        myMoney = inventory.getGoldInPocket()
        if self.pvpMode:
            myMoney = self.getMoney()
        if inventory:
            if stackable:
                qtyMult = max(1, EconomyGlobals.getItemQuantity(self.buyPanelItem.uid))
                qtyLimit = ItemGlobals.getStackLimit(self.buyPanelItem.uid)
                if not qtyLimit:
                    qtyLimit = inventory.getStackLimit(self.buyPanelItem.uid)
                freeSpace = qtyLimit - self.buyPanelItem.getQuantityInInventory()
            else:
                qtyMult = 1
                freeSpace = len(inventory.getFreeLocations(self.buyPanelItem.itemClass, self.buyPanelItem.itemType))
            totalCost = int(self.buyPanelItem.cost * qtyMult) * self.buyPanelItem.quantity / qtyMult
            if myMoney < totalCost:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughMoneyWarning, PiratesGuiGlobals.TextFG6)
                return
            if self.buyPanelItem.cost < 0 and myMoney + totalCost > self.getMaxMoney(inventory):
                base.localAvatar.guiMgr.createWarning(PLocalizer.CannotHoldGoldWarning, PiratesGuiGlobals.TextFG6)
                return
            if self.buyPanelItem.quantity > freeSpace:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NoInventorySpaceWarning, PiratesGuiGlobals.TextFG6)
                return
        if self.buyPanelItem.quantity > 0:
            if not stackable:
                for i in range(self.buyPanelItem.quantity):
                    self.buyPanelItem.purchase(self.npc)

            else:
                self.buyPanelItem.purchase(self.npc)
            self.buyPanel.setPending(1)
            self.buyPanel.updateGui()
        return

    def purchaseConfirmation(self):
        if self.buyPanelItem and self.buyPanel.pending:
            itemName = self.invContainer.getItem(self.buyPanelItem.uid).getName()
            text = PLocalizer.PurchaseConfirmation % (str(self.buyPanelItem.quantity), itemName)
            localAvatar.guiMgr.createWarning(text, PiratesGuiGlobals.TextFG6)
            itemId = self.buyPanelItem.uid
            self.itemClicked(None)
            self.itemClicked(itemId)
            self.buyPanel.updateGui()
        return

    def updateBalance(self):
        yourMoney = PLocalizer.YourPVPMoney if self.pvpMode else PLocalizer.YourMoney
        self.myGold['text'] = yourMoney + ' ' + str(self.getMoney())

    def initTabs(self):
        self.tabBar = SimpleStoreTabBar(parent=self, backParent=self.backTabParent, frontParent=self.frontTabParent, offset=0)
        self.createTabs()
        if self.tabBar.hasTabs():
            firstTabName = self.tabBar.getOrder()[0]
            self.tabBar.selectTab(firstTabName)
            self.setTab(firstTabName)

    def addTab(self, tabId, displayName='', text='', image=None, image_scale=None):
        newTab = self.tabBar.addTab(tabId, command=self.setTab, extraArgs=[tabId])
        newTab.displayName = displayName
        if image:
            textPosition = (-0.07, -0.2, 0.0)
        else:
            textPosition = (-0.07, -0.0, 0.0)
        newTab.nameTag = DirectLabel(parent=newTab, relief=None, state=DGG.DISABLED, pos=(0.06, 0, -0.035) if image else (0.0, 0, 0.0), text=text, text_pos=textPosition, text_scale=PiratesGuiGlobals.TextScaleLarge * 4.0, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceFont(), text_wordwrap=6, image=image, image_pos=(-0.1, 0.0, 0.07), image_scale=image_scale)
        return

    def setTab(self, tabId):
        self.tabBar.unstash()
        self.reloadPirateDNA()
        self.rollInItem = None
        self.clickedItem = None
        self.setPreviewItem(None)
        self.setBuyPanelItem(None)
        if self.rollInItemTask:
            taskMgr.remove(self.rollInItemTask)
            self.rollInItemTask = None
        self.setupGrid()
        titleText = ''
        titleText += '\x01smallCaps\x01'
        titleText += self.storeName
        titleText += '\x02'
        self.cartFrame.nameTagLabel['text'] = titleText
        self.cartFrame.resetDecorations()
        itemIds = self.getTabItemIds(tabId)
        self.makeTabButtons(tabId, itemIds)
        self.itemCardPlaceholder.show()
        return

    def makeTabButtons(self, tabId, itemIds):
        self.invContainer.setupItems(itemIds)
        self.invContainer.disableUnusedCells()

    def canChangeSelection(self):
        return self.confirmDialog is None

    def setBuyPanelItem(self, itemId):
        if self.buyPanelItem:
            if self.buyPanelItem.uid == itemId:
                return

            if self.buyPanelItem:
                self.buyPanel.destroy()
                self.buyPanel = None

            if itemId is None and self.colorPanel:
                self.colorPanel.hide()

        item = self.stock.get(itemId)
        self.buyPanelItem = item
        if not self.buyPanelItem:
            return

        self.buyPanel = SimpleStoreBuyPanelGUI(self, self.cartFrame, self.buyPanelItem, purchasable=True)
        self.buyPanel.setPos(self.buyPanelXFactor * self.guiWidth, 0.0, -0.475)

        if not self.colorPanel:
            self.colorPanel = self.colorPanel or SimpleStoreColorPicker(self, self.cartFrame, self.buyPanelItem)
            self.colorPanel.setPos(self.buyPanelXFactor * self.guiWidth, 0.0, -0.19)
        else:
            self.colorPanel.item = self.buyPanelItem
        if isinstance(self.buyPanelItem, SimpleClothingItem) and ItemGlobals.canDyeItem(itemId):
            self.colorPanel.selectColor(self.buyPanelItem.colorId)
            self.colorPanel.show()
        else:
            self.colorPanel.hide()

    def itemRollIn(self, itemId, task=None):
        if self.rollInItem:
            self.itemRollOut(self.rollInItem.uid)

        item = self.stock.get(itemId)
        self.rollInItem = item
        if self.rollInItem or self.clickedItem:
            self.itemCardPlaceholder.hide()
        if self.clickedItem and itemId == self.clickedItem.uid:
            self.setBuyPanelItem(itemId)
        elif self.clickedItem and not self.rollInItem:
            self.setBuyPanelItem(itemId)
        else:
            self.setBuyPanelItem(None)
            if self.rollInItemTask:
                taskMgr.remove(self.rollInItemTask)
                self.rollInItemTask = None

        if getBase().config.GetBool('want-simple-preview', 0):
            self.setPreviewItem(itemId)

    def itemRollOut(self, itemId, task=None):
        if not self.rollInItem or self.rollInItem.uid != itemId:
            return
        self.rollInItem = None
        if getBase().config.GetBool('want-simple-preview', 0):
            if self.previewItem and itemId == self.previewItem.uid:
                self.setPreviewItem(None)
        if not self.clickedItem:
            self.itemCardPlaceholder.show()
        if self.rollInItemTask:
            taskMgr.remove(self.rollInItemTask)
            self.rollInItemTask = None
        return

    def itemClicked(self, itemId, task=None):
        if self.clickedItem and itemId == self.clickedItem.uid:
            return
        self.clickedItem = self.stock.get(itemId)
        if isinstance(self.clickedItem, SimpleClothingItem) and ItemGlobals.canDyeItem(itemId):
            InventoryUIStoreContainer.InventoryUIStoreContainer.detailsHeight = 0.22
        else:
            InventoryUIStoreContainer.InventoryUIStoreContainer.detailsHeight = 0.56
        self.showClicked()
        if not self.clickedItem:
            self.itemCardPlaceholder.show()
        self.setPreviewItem(itemId)
        if getBase().config.GetBool('want-simple-buy', 0):
            self.showBuyGUI()
        else:
            self.setBuyPanelItem(itemId)

    def showClicked(self):
        if not self.clickedItem:
            return
        self.invContainer.showItemDetails(self.clickedItem.uid)
        self.itemRollIn(self.clickedItem.uid)

    def getMerchandiseIds(self):
        merchIds = DropGlobals.getStoreItems(self.npc.uniqueId)[:]
        return merchIds

    def getStockItems(self, merchIds):
        stock = {}
        for id in merchIds:
            item = self.itemFromItemId(id)
            stock[id] = item

        return stock

    def removeHolidayItems(self, stock):
        newStock = {}
        activeHolidayIds = base.cr.newsManager.getActiveHolidayList()
        for itemKey in stock:
            item = stock[itemKey]
            if not item.holidayId or item.holidayId in activeHolidayIds:
                newStock[itemKey] = item

        return newStock

    def filterStockItems(self, stock, pirate):
        newStock = {}
        for id in stock.keys():
            item = stock[id]
            if not item or not item.canBeUsed(pirate):
                pass
            else:
                newStock[id] = item

        return newStock

    def getStockIds(self, stock):
        return stock.keys()

    def createTabs(self):
        pass

    def itemFromItemId(self, itemId):
        item = itemType = None
        itemGlobalsClass = ItemGlobals.getClass(itemId)
        if itemGlobalsClass in self.itemGlobalsClasses:
            item = self.itemGlobalsClasses[itemGlobalsClass](itemId)
        if not item:
            itemType = EconomyGlobals.getItemType(itemId)
            if itemType in self.itemGlobalsClasses:
                item = self.itemGlobalsClasses[itemType](itemId)
        if not item:
            self.notify.warning('Unhandled item: %s' % (itemId,))
            return
        return item

    def tabIdFromItemId(self, uid):
        return ItemGlobals.getType(uid)

    def getTabItemIds(self, tabId):
        allIds = self.getStockIds(self.stock)
        tabIds = [ aId for aId in allIds if self.tabIdFromItemId(aId) == tabId ]
        return tabIds

    def getTabItems(self, tabId):
        items = {}
        itemIds = self.getTabItemIds(tabId)
        for itemId in itemIds:
            if self.stock.get(itemId):
                items[itemId] = self.stock[itemId]

        return items


class CatalogStoreGUI(SimpleStoreGUI):
    storeIconName = 'models/buildings/sign1_eng_a_icon_tailor'

    def __init__(self, npc, shopId, **kw):
        self.npc = npc
        self.previewSceneGraph = NodePath('PreviewSceneGraph')
        self.createPreviewBuffer()
        self.createPreviewMale()
        self.createPreviewFemale()
        self.cm = None
        self.previewCards = {}
        merchIds = self.getMerchandiseIds()
        self.maleStock = self.getStockItems(merchIds)
        self.maleStock = self.removeHolidayItems(self.maleStock)
        self.maleStock = self.filterStockItems(self.maleStock, self.previewMale)
        self.currTabMaleStock = {}
        merchIds = self.getMerchandiseIds()
        self.femaleStock = self.getStockItems(merchIds)
        self.femaleStock = self.removeHolidayItems(self.femaleStock)
        self.femaleStock = self.filterStockItems(self.femaleStock, self.previewFemale)
        self.currTabFemaleStock = {}
        SimpleStoreGUI.__init__(self, PLocalizer.CatalogStore, npc, shopId, **kw)
        self.rotateSlider.hide()
        return

    def destroy(self):
        SimpleStoreGUI.destroy(self)
        if self.previewMale:
            self.previewMale.detachNode()
            self.previewMale = None
        if self.previewFemale:
            self.previewFemale.detachNode()
            self.previewFemale = None
        self.destroyPreviewBuffer()
        for id in self.previewCards.keys():
            self.previewCards[id].detachNode()
            self.previewCards.pop(id)

        return

    def createTabs(self):
        stockHolidayIds = set([ item.holidayId for item in self.stock.itervalues() if item.holidayId ])
        if not stockHolidayIds:
            return
        firstTab = max(stockHolidayIds)
        while stockHolidayIds:
            holidayId = max(stockHolidayIds)
            stockHolidayIds.remove(holidayId)
            displayName = CatalogHoliday.getCatalogDisplayNameForHoliday(holidayId)
            tabName = CatalogHoliday.getCatalogTabNameForHoliday(holidayId)
            self.addTab(holidayId, displayName, tabName)

        self.setTab(firstTab)

    def tabIdFromItemId(self, uid):
        return ItemGlobals.getHoliday(uid)

    def setTab(self, tabId):
        SimpleStoreGUI.setTab(self, tabId)
        self.updateCatalogRender(tabId)
        self.itemCardPlaceholder.show()
        holidayName = PLocalizer.CATALOG_HOLIDAY_ID_2_NAME.get(tabId)
        if holidayName:
            self.titleText['text'] = holidayName
        else:
            self.titleText['text'] = ''

    def updateCatalogRender(self, tabId):
        self.unapplyStockFromPirate(self.currTabMaleStock, self.previewMale, self.maleDNA)
        self.currTabMaleStock = {}
        for uid in self.maleStock.iterkeys():
            if self.tabIdFromItemId(uid) == tabId:
                self.currTabMaleStock[uid] = self.maleStock[uid]

        self.applyStockToPirate(self.currTabMaleStock, self.previewMale)
        self.unapplyStockFromPirate(self.currTabFemaleStock, self.previewFemale, self.femaleDNA)
        self.currTabFemaleStock = {}
        for uid in self.femaleStock.iterkeys():
            if self.tabIdFromItemId(uid) == tabId:
                self.currTabFemaleStock[uid] = self.femaleStock[uid]

        self.applyStockToPirate(self.currTabFemaleStock, self.previewFemale)
        for card in self.previewCards.itervalues():
            card.detachNode()

        if not self.previewCards.get(tabId):
            self.previewCards[tabId] = self.createPreviewCard()
        self.previewCards[tabId].reparentTo(self.itemCardPlaceholder)

    def createPreviewBuffer(self):
        self.previewBg = loader.loadModel('models/gui/pir_m_gui_frm_catalog_bg')
        self.previewBg.setScale(1.08, 1.11, 1.11)
        self.previewBg.setPos(0, 17, -2.27)
        self.previewBuffer = base.win.makeTextureBuffer('par', 256, 512)
        self.previewLens = PerspectiveLens()
        self.previewLens.setNear(0.5)
        self.previewLens.setAspectRatio(0.64 / 0.865)
        self.previewCam = base.makeCamera(win=self.previewBuffer, scene=self.previewSceneGraph, clearColor=Vec4(1), lens=self.previewLens)
        self.previewCam.node().getDisplayRegion(0).setIncompleteRender(False)
        self.previewCam.reparentTo(self.previewSceneGraph)
        self.previewBg.reparentTo(self.previewCam)

    def destroyPreviewBuffer(self):
        if self.previewBuffer:
            base.graphicsEngine.removeWindow(self.previewBuffer)
            self.previewBuffer = None
            self.previewBg.detachNode()
            self.previewCam.detachNode()
            self.previewCam = None
        return

    def createPreviewPirate(self):
        pass

    def createPreviewMale(self):
        self.previewMale = DynamicHuman.DynamicHuman()
        self.previewMale.ignoreAll()
        self.previewMale.mixingEnabled = False
        self.maleDNA = HumanDNA.HumanDNA('m')
        self.previewMale.setDNAString(self.maleDNA)
        self.previewMale.generateHuman('m')
        self.previewMale.stopBlink()
        self.previewMale.pose('idle', 1)
        lodNode = self.previewMale.find('**/+LODNode').node()
        lodNode.forceSwitch(lodNode.getHighestSwitch())
        self.previewMale.reparentTo(self.previewSceneGraph)
        self.previewMale.setH(190)
        self.previewMale.setPos(1, 9.5, -3)
        if localAvatar.style.getGender() == 'f':
            self.previewMale.setY(10)

    def createPreviewFemale(self):
        self.previewFemale = DynamicHuman.DynamicHuman()
        self.previewFemale.ignoreAll()
        self.previewFemale.mixingEnabled = False
        self.femaleDNA = HumanDNA.HumanDNA('f')
        self.previewFemale.setDNAString(self.femaleDNA)
        self.previewFemale.generateHuman('f')
        self.previewFemale.stopBlink()
        self.previewFemale.pose('idle', 1)
        lodNode = self.previewFemale.find('**/+LODNode').node()
        lodNode.forceSwitch(lodNode.getHighestSwitch())
        self.previewFemale.reparentTo(self.previewSceneGraph)
        self.previewFemale.setH(170)
        self.previewFemale.setPos(-1, 9.5, -3)
        if localAvatar.style.getGender() == 'm':
            self.previewFemale.setY(10)

    def unapplyStockFromPirate(self, stock, pirate, originalStyle):
        for stockItem in stock.itervalues():
            stockItem.unapply(pirate, originalStyle)

    def applyStockToPirate(self, stock, pirate):
        for stockItem in stock.itervalues():
            stockItem.apply(pirate)

    def createPreviewCard(self):
        if not self.cm:
            self.cm = CardMaker('previewCard')
            self.cm.setFrame(-0.32, 0.32, -0.4325, 0.4325)
        tex = self.previewBuffer.getTexture()
        previewCard = NodePath(self.cm.generate())
        previewCard.setTexture(tex, 1)
        return previewCard

    def setPreviewItem(self, itemId):
        item = self.stock.get(itemId)
        self.previewItem = item
        if not self.previewItem:
            return

    def focusCamera(self):
        if self.previewItem:
            SimpleStoreGUI.focusCamera(self)
            return
        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
        dummy = self.npc.attachNewNode('dummy')
        dummy.setPos(dummy, 0, 3, self.npc.headNode.getZ(self.npc) + 0.25)
        dummy.wrtReparentTo(render)
        dummy.lookAt(self.npc, self.npc.headNode.getX(self.npc), self.npc.headNode.getY(self.npc), self.npc.headNode.getZ(self.npc) + 0.25)
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
        if self.camIval and self.camIval.endPos == camPos and self.camIval.endHpr == camHpr:
            return
        t = 1.5
        self.camIval = camera.posHprInterval(t, pos=camPos, hpr=camHpr, blendType='easeOut')
        localAvatar.cameraFSM.request('Control')
        self.camIval.start()
        return


class AccessoriesStoreGUI(SimpleStoreGUI):
    storeIconName = 'models/buildings/sign1_eng_a_icon_tailor'
    tabInfos = [
     [
      ClothingGlobals.HAT, '**/icon_shop_tailor_hat', 0.55], [ClothingGlobals.BELT, '**/icon_shop_tailor_belt', 0.55], [ClothingGlobals.SHOE, '**/icon_shop_tailor_booths', 0.4], [ClothingGlobals.COAT, '**/icon_shop_tailor_coat', 0.4], [ClothingGlobals.PANT, '**/icon_shop_tailor_pants', 0.4], [ClothingGlobals.VEST, '**/icon_shop_tailor_vest', 0.5]]

    def __init__(self, npc, shopId, **kw):
        self.TailorIcons = loader.loadModel('models/textureCards/tailorIcons')
        self.ShirtIcon = loader.loadModel('models/gui/char_gui').find('**/chargui_cloth')
        SimpleStoreGUI.__init__(self, PLocalizer.TailorStore, npc, shopId, **kw)

    def createTabs(self):
        for item in self.tabInfos:
            self.addTab(item[0], ClothingGlobals.getClothingTypeName(item[0]), image=self.TailorIcons.find(item[1]), image_scale=item[2])

        self.addTab(ClothingGlobals.SHIRT, PLocalizer.CatalogStore, image=self.ShirtIcon, image_scale=1.2)

    def showCutOffVestAlert(self):
        self.removeAlertDialog()
        text = PLocalizer.ShopFemaleVestConflict
        self.alertDialog = PDialog.PDialog(text=text, text_align=TextNode.ACenter, style=OTPDialog.Acknowledge, pos=(-0.65, 0.0, 0.0), command=self.removeAlertDialog)
        self.alertDialog.setBin('gui-fixed', 3, 3)


class JewelryStoreGUI(SimpleStoreGUI):
    storeIconName = 'models/buildings/sign1_eng_a_icon_jeweler'
    iconsA = loader.loadModel('models/gui/char_gui')
    iconsB = loader.loadModel('models/textureCards/shopIcons')
    tabInfos = {JewelryGlobals.RBROW: [iconsB.find('**/icon_shop_tailor_brow'), (-0.5, 0.5, 0.5)],JewelryGlobals.LBROW: [iconsB.find('**/icon_shop_tailor_brow'), (0.5, 0.5, 0.5)],JewelryGlobals.LEAR: [iconsA.find('**/chargui_ears'), (1.7, 1.7, 1.7)],JewelryGlobals.REAR: [iconsA.find('**/chargui_ears'), (-1.7, 1.7, 1.7)],JewelryGlobals.NOSE: [iconsA.find('**/chargui_nose'), 1.7],JewelryGlobals.MOUTH: [iconsA.find('**/chargui_mouth'), 1.7],JewelryGlobals.LHAND: [iconsB.find('**/icon_shop_tailor_hand'), (0.5, 0.5, 0.5)],JewelryGlobals.RHAND: [iconsB.find('**/icon_shop_tailor_hand'), (-0.5, 0.5, 0.5)]}

    def __init__(self, npc, shopId, **kw):
        SimpleStoreGUI.__init__(self, PLocalizer.ShopJewelry, npc, shopId, **kw)

    def getTabItemIds(self, tabId):
        allIds = self.getMerchandiseIds()
        tabType = SimpleJewelryItem.itemTypeFromJewelryType(tabId)
        tabIds = [ aId for aId in allIds if self.tabIdFromItemId(aId) == tabType ]
        return tabIds

    def setTab(self, tabId):
        SimpleStoreGUI.setTab(self, tabId)
        items = SimpleStoreGUI.getTabItems(self, tabId)
        for item in items.itervalues():
            item.jewelryType = tabId

    def createTabs(self):
        for key, value in self.tabInfos.iteritems():
            self.addTab(key, PLocalizer.JewelryNames.get(key), image=value[0], image_scale=value[1])


class TattooStoreGUI(SimpleStoreGUI):
    storeIconName = 'models/buildings/sign1_eng_a_icon_tattoo'
    tabInfos = [
     [
      TattooGlobals.ZONE1, PLocalizer.TattooChest, '**/icon_shop_tailor_chest_male', 0.4], [TattooGlobals.ZONE2, PLocalizer.TattooLeftArm, '**/icon_shop_tailor_arm', 0.4], [TattooGlobals.ZONE3, PLocalizer.TattooRightArm, '**/icon_shop_tailor_arm', (-0.4, 0.4, 0.4)], [TattooGlobals.ZONE4, PLocalizer.TattooFace, '**/icon_shop_tailor_face_male', 0.4]]

    def __init__(self, npc, shopId, **kw):
        SimpleStoreGUI.__init__(self, PLocalizer.TattooShop, npc, shopId, **kw)

    def getTabItemIds(self, tabId):
        allIds = self.stock.keys()
        tabType = SimpleTattooItem.itemTypeFromTattooType(tabId)
        tabIds = [ aId for aId in allIds if self.tabIdFromItemId(aId) == tabType ]
        return tabIds

    def setTab(self, tabId):
        SimpleStoreGUI.setTab(self, tabId)
        items = SimpleStoreGUI.getTabItems(self, tabId)
        for item in items.itervalues():
            item.zone = tabId

    def createTabs(self):
        for item in self.tabInfos:
            self.addTab(item[0], item[1], image=SimpleTattooItem.Icons.find(item[2]), image_scale=item[3])


class MerchantStoreGUI(SimpleStoreGUI):
    TabIdFromItemType = {ItemConstants.SWORD: 'SWORD',ItemConstants.GUN: 'GUN',ItemConstants.DOLL: 'DOLL',ItemConstants.DAGGER: 'DAGGER',ItemConstants.GRENADE: 'GRENADE',ItemConstants.STAFF: 'STAFF',ItemConstants.CANNON: 'CANNON',ItemConstants.SAILING: 'CHARMS',ItemConstants.AXE: 'AXE',ItemConstants.FENCING: 'FENCING',ItemConstants.POTION: 'POTION',ItemConstants.ODDS_AND_ENDS: 'ODDS_AND_ENDS',ItemConstants.MONSTER: 'MONSTER',ItemConstants.FISHING: 'FISHING',ItemConstants.QUEST_PROP: 'QUEST_PROP'}
    TabIdFromItemTypeGroup = {EconomyGlobals.ItemTypeGroup.CUTLASS: 'SWORD',EconomyGlobals.ItemTypeGroup.PISTOL: 'GUN',EconomyGlobals.ItemTypeGroup.DOLL: 'DOLL',EconomyGlobals.ItemTypeGroup.DAGGER: 'DAGGER',EconomyGlobals.ItemTypeGroup.GRENADE: 'GRENADE',EconomyGlobals.ItemTypeGroup.WAND: 'STAFF',EconomyGlobals.ItemTypeGroup.CANNON: 'CANNON',EconomyGlobals.ItemTypeGroup.POTION: 'POTION',EconomyGlobals.ItemTypeGroup.FISHING_GEAR: 'FISHING'}
    TabOrder = [
     'DAGGER', 'SWORD', 'AXE', 'FENCING', 'GUN', 'GRENADE', 'DOLL', 'STAFF', 'POTION', 'CHARMS', 'CANNON', 'FISHING', 'MONSTER', 'QUEST_PROP', 'ODDS_AND_ENDS', 'UNKNOWN']
    TabDisplayNames = {'AXE': 'AXE','CHARMS': 'CHARMS','DAGGER': 'DAGGER','DOLL': 'DOLL','FENCING': 'FENCING','FISHING': 'FISHING','GRENADE': 'GRENADE','GUN': 'GUN','MONSTER': 'MONSTER','ODDS_AND_ENDS': 'ODDS_AND_ENDS','POTION': 'POTION','QUEST_PROP': 'QUEST_PROP','STAFF': 'STAFF','SWORD': 'SWORD','CANNON': 'CANNON','UNKNOWN': 'UNKNOWN'}
    TabDisplayIcons = {'AXE': ('**/pir_t_ico_swd_rapier_a', 'weapon'),'CHARMS': ('**/pir_t_ico_swd_rapier_a', 'weapon'),'DAGGER': ('**/pir_t_ico_knf_dagger_a', 'weapon'),'DOLL': ('**/pir_t_ico_dol_spirit_b', 'weapon'),'FENCING': ('**/pir_t_ico_swd_rapier_a', 'weapon'),'FISHING': ('**/pir_t_gui_fsh_mdRodIcon', 'fishing'),'GRENADE': ('**/pir_t_ico_bom_grenade', 'weapon'),'GUN': ('**/pir_t_ico_gun_pistol_a', 'weapon'),'MONSTER': ('**/pir_t_ico_swd_rapier_a', 'weapon'),'ODDS_AND_ENDS': ('**/pir_t_ico_swd_rapier_a', 'weapon'),'POTION': ('**/pir_t_ico_pot_elixir', 'skill'),'QUEST_PROP': ('**/pir_t_ico_swd_rapier_a', 'weapon'),'STAFF': ('**/pir_t_ico_stf_ward_a', 'weapon'),'SWORD': ('**/pir_t_ico_swd_cutlass_a', 'weapon'),'CANNON': ('**/cannon', 'skill'),'UNKNOWN': ('**/pir_t_ico_swd_rapier_a', 'weapon')}

    def __init__(self, inventory, name, npc, **kw):
        self.inventory = inventory
        self.tabInventory = {}
        for itemId in self.inventory:
            tabId = None
            itemType = ItemGlobals.getType(itemId)
            if itemType:
                tabId = self.TabIdFromItemType.get(itemType, 'UNKNOWN')
            else:
                itemTypeGroup = EconomyGlobals.getItemGroup(itemId)
                tabId = self.TabIdFromItemTypeGroup.get(itemTypeGroup, 'UNKNOWN')
            if tabId:
                self.tabInventory.setdefault(tabId, [])
                self.tabInventory[tabId].append(itemId)

        SimpleStoreGUI.__init__(self, name, npc, **kw)
        self.rotateSlider.hide()
        return

    def getTabItemIds(self, tabId):
        return self.tabInventory[tabId]

    def createTabs(self):
        for tabId in self.TabOrder:
            tabName = self.TabDisplayNames[tabId]
            if tabId in self.tabInventory:
                displayInfo = self.TabDisplayIcons[tabId]
                if displayInfo[1] == 'weapon':
                    icons = loader.loadModel('models/gui/gui_icons_weapon')
                elif displayInfo[1] == 'skill':
                    icons = loader.loadModel('models/textureCards/skillIcons')
                elif displayInfo[1] == 'fishing':
                    icons = loader.loadModel('models/textureCards/fishing_icons')
                image = icons.find(displayInfo[0])
                self.addTab(tabId, tabName, tabName, image=image, image_scale=0.55)

    def startCellItemDetails(self, cell, detailsPos, detailsHeight, detailsDelay, event=None):
        item = None
        if cell:
            item = cell.inventoryItem or cell.hotlink
        if item:
            oldTasks = taskMgr.getTasksNamed('inventoryUIHideDetailsTask')
            oldTasks = [ tsk for tsk in oldTasks if tsk.cell == cell if tsk.item == item ]
            for tsk in oldTasks:
                taskMgr.remove(tsk)

            tsk = taskMgr.doMethodLater(detailsDelay, self.showDetails, 'inventoryUIShowDetailsTask', extraArgs=[item, cell, detailsPos, detailsHeight])
            tsk.cell = cell
            tsk.item = item
        else:
            oldTasks = taskMgr.getTasksNamed('inventoryUIShowDetailsTask')
            oldTasks = [ tsk for tsk in oldTasks if tsk.cell == cell ]
            for tsk in oldTasks:
                taskMgr.remove(tsk)

        return

    def cancelCellItemDetails(self, cell, detailsDelay=0, event=None):
        item = None
        if cell:
            item = cell.inventoryItem or cell.hotlink
        if item:
            oldTasks = taskMgr.getTasksNamed('inventoryUIShowDetailsTask')
            oldTasks = [ tsk for tsk in oldTasks if tsk.cell == cell if tsk.item == item ]
            for tsk in oldTasks:
                taskMgr.remove(tsk)

            if not detailsDelay:
                self.hideDetails(item)
            else:
                tsk = taskMgr.doMethodLater(detailsDelay, self.hideDetails, 'inventoryUIHideDetailsTask', extraArgs=[item])
                tsk.cell = cell
                tsk.item = item
        return

    def hideDetails(self, item, task=None):
        item.hideDetails()

    def showDetails(self, item, cell, detailsPos, detailsHeight, task=None):
        item.showDetails(cell, detailsPos, detailsHeight)

    def focusCamera(self):
        if localAvatar.gameFSM.camIval is not None:
            if localAvatar.gameFSM.camIval.isPlaying():
                localAvatar.gameFSM.camIval.finish()
        if self.camIval:
            self.camIval.finish()
            self.camIval = None
        dummy = self.npc.attachNewNode('dummy')
        dummy.setPos(dummy, 0, 3, self.npc.headNode.getZ(self.npc) + 0.25)
        dummy.wrtReparentTo(render)
        dummy.lookAt(self.npc, self.npc.headNode.getX(self.npc), self.npc.headNode.getY(self.npc), self.npc.headNode.getZ(self.npc) + 0.25)
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
        if self.camIval and self.camIval.endPos == camPos and self.camIval.endHpr == camHpr:
            return
        t = 1.5
        self.camIval = camera.posHprInterval(t, pos=camPos, hpr=camHpr, blendType='easeOut')
        localAvatar.cameraFSM.request('Control')
        self.camIval.start()
        return

    def getMerchandiseIds(self):
        return self.inventory