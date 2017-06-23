from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.inventory.InventoryUIGlobals import *
from pirates.economy import EconomyGlobals
from pirates.makeapirate import ClothingGlobals
from pirates.inventory import InventoryUISellContainer
from pirates.inventory import ItemGlobals
from pirates.piratesgui import GuiButton
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import InventoryStackSeller
from pirates.inventory import InventoryGlobals
from pirates.inventory.ItemGlobals import DYE_COLORS, COLOR_VALUES

class InventorySellConfirm(BorderFrame):

    def __init__(self, manager, callback, **kw):
        self.sizeX = 0.8
        self.sizeZ = 0.8
        textScale = PiratesGuiGlobals.TextScaleTitleSmall
        optiondefs = (('state', DGG.DISABLED, None), ('frameSize', (-0.0 * self.sizeX, 1.0 * self.sizeX, -0.0 * self.sizeZ, 1.0 * self.sizeZ), None), ('modelName', 'pir_m_gui_frm_main_blue', None), ('nameTag', PLocalizer.InventorySellTitle, None))
        self.defineoptions(kw, optiondefs)
        BorderFrame.__init__(self)
        self.initialiseoptions(InventorySellConfirm)
        self.accept('UpdateSellContainer', self.update)
        self.manager = manager
        self.callback = callback
        self.confirmDialog = None
        self.totalGoldValue = 0
        self.setup()
        return

    def destroy(self):
        self.ignore('UpdateSellContainer')
        base.localAvatar.guiMgr.setIgnoreMainMenuHotKey(True)
        base.localAvatar.guiMgr.setIgnoreAllKeys(False)
        base.localAvatar.guiMgr.hideSeaChest()
        base.localAvatar.guiMgr.setIgnoreMainMenuHotKey(False)
        self.manager.releaseFromSale()
        if self.inventoryPanelSell:
            self.inventoryPanelSell.clearSale()
        if self.stackSeller:
            self.stackSeller.destroy()
            self.stackSeller = None
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        self.ignoreAll()
        localAvatar.enableLootUI()
        BorderFrame.destroy(self)
        return

    def setup(self):
        self.setBin('gui-fixed', 0)
        self.buttonSize = self.manager.standardButtonSize
        self.inventoryPanelSell = InventoryUISellContainer.InventoryUISellContainer(self.manager, self.sellItem, sizeX=self.buttonSize * 3, sizeZ=self.buttonSize * 2, countX=3, countZ=2)
        self.inventoryPanelSell.setup()
        self.inventoryPanelSell.setPos(self.sizeX / 4.0 - 0.01, 0.0, self.sizeZ / 4.0 + 0.09)
        self.inventoryPanelSell.reparentTo(self)
        self.messageLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.InventorySellMessage, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=16, text_shadow=PiratesGuiGlobals.TextShadow, pos=(self.sizeX * 0.5, 0.0, self.sizeZ * 0.85))
        self.goldCostLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.InventorySellGoldCost % 0, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(self.sizeX * 0.5, 0.0, self.sizeZ * 0.25))
        Gui = loader.loadModel('models/gui/toplevel_gui')
        buttonImage = (Gui.find('**/generic_button'), Gui.find('**/generic_button_down'), Gui.find('**/generic_button_over'), Gui.find('**/generic_button_disabled'))
        self.confirmButton = GuiButton.GuiButton(parent=self, text=PLocalizer.InventorySell, text_fg=PiratesGuiGlobals.TextFG2, text_pos=(0.0, -0.014), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, image=GuiButton.GuiButton.blueGenericButton, image_scale=(0.6,
                                                                                                                                                                                                                                                                                                                                      0.6,
                                                                                                                                                                                                                                                                                                                                      0.6), pos=(self.sizeX * 0.5, 0, 0.12), relief=None, command=self.confirmSale)
        self.confirmButton['state'] = DGG.DISABLED
        self.stackSeller = None
        main_gui = loader.loadModel('models/gui/gui_main')
        generic_x = main_gui.find('**/x2')
        generic_box = main_gui.find('**/exit_button')
        generic_box_over = main_gui.find('**/exit_button_over')
        main_gui.removeNode()
        closeButton = GuiButton.GuiButton(parent=self, relief=None, pos=(1.0, 0, -0.01), image=(generic_box, generic_box, generic_box_over, generic_box), image_scale=0.4, command=self.callback)
        xButton = OnscreenImage(parent=closeButton, image=generic_x, scale=0.2, pos=(-0.256, 0, 0.766))
        localAvatar.disableLootUI()
        return

    def update(self):
        self.totalGoldValue = self.inventoryPanelSell.calculateTotalGoldValue()
        self.goldCostLabel['text'] = PLocalizer.InventorySellGoldCost % int(self.totalGoldValue * ItemGlobals.GOLD_SALE_MULTIPLIER)
        if self.inventoryPanelSell.hasItemsToSell():
            self.confirmButton['state'] = DGG.NORMAL
        else:
            self.confirmButton['state'] = DGG.DISABLED

    def sellItem(self, cell):
        if cell.inventoryItem.getCategory() == InventoryType.ItemTypeConsumable:
            if not self.stackSeller:
                self.stackSeller = InventoryStackSeller.InventoryStackSeller(cell, self)
                self.stackSeller.reparentTo(self)
                self.stackSeller.setPos(0.08, 0, 0.08)

    def setStackAmount(self, cell, amount):
        for sellCell in self.inventoryPanelSell.gridDict.values():
            if sellCell.inventoryItem and sellCell.inventoryItem.inventoryCell == cell:
                sellCell.inventoryItem.amount = amount
                sellCell.inventoryItem.updateAmountText()

    def cancelItem(self):
        cell = self.stackSeller.fromCell
        for sellCell in self.inventoryPanelSell.gridDict.values():
            if sellCell.inventoryItem and sellCell.inventoryItem.inventoryCell == cell:
                sellCell.inventoryItem.inventoryCell['state'] = DGG.NORMAL
                sellCell.inventoryItem.inventoryCell.clearColorScale()
                sellCell.inventoryItem.destroy()

    def cancelSale(self):
        self.inventoryPanelSell.clearSale()
        self.update()
        self.manager.releaseFromSale()

    def confirmSale(self):
        if localAvatar.getInventory().getGoldInPocket() + self.totalGoldValue * ItemGlobals.GOLD_SALE_MULTIPLIER > InventoryGlobals.GOLD_CAP:
            r = Functor(self.reconfirmSale)
            if self.confirmDialog:
                self.confirmDialog.destroy()
                self.confirmDialog = None
            self.confirmDialog = PDialog.PDialog(text=PLocalizer.ExcessGoldLost, style=OTPDialog.YesNo, command=r)
        else:
            self.reconfirmSale()
        return

    def reconfirmSale(self, doSale=True):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if doSale:
            for cell in self.inventoryPanelSell.gridDict.values():
                if cell.inventoryItem:
                    self.manager.markSlotPending(cell.inventoryItem.inventoryCell.slotId)
                    itemToSell = localAvatar.getInventory().getLocatables().get(cell.inventoryItem.inventoryCell.slotId)
                    messenger.send('sellItem', [itemToSell, cell.inventoryItem.amount])

            self.inventoryPanelSell.clearSale()
            self.update()
        return