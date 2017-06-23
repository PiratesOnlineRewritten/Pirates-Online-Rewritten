from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIContainer
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory import ItemGlobals

class InventoryUISellContainer(InventoryUIContainer.InventoryUIContainer):

    def __init__(self, manager, callback, sizeX=1.0, sizeZ=1.0, countX=None, countZ=None, hotkeyList=[]):
        InventoryUIContainer.InventoryUIContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ)
        self.containerType = CONTAINER_SELL
        self.initialiseoptions(InventoryUISellContainer)
        self.callback = callback

    def setup(self):
        pass

    def destroy(self):
        self.ignoreAll()
        InventoryUIContainer.InventoryUIContainer.destroy(self)

    def canDrag(self):
        return 1

    def cellUsed(self, cell):
        if self.manager.heldFromCell:
            itemId = self.manager.heldFromCell.inventoryItem.getId()
            itemInfo = (ItemGlobals.getClass(itemId), itemId, 0, 0)
            item = self.manager.makeLocatableItem(itemInfo)
            if item:
                item.inventoryCell = self.manager.heldFromCell
                item.amount = 1
                self.manager.heldFromCell['state'] = DGG.DISABLED
                self.manager.heldFromCell.setColorScale(0.5, 0.5, 0.5, 1)
                self.putIntoCell(item, cell)
                self.callback(self.manager.heldFromCell)

    def cellClick(self, cell, mouseAction=MOUSE_CLICK, task=None):
        if cell.inventoryItem and not mouseAction == MOUSE_CLICK:
            cell.inventoryItem.inventoryCell['state'] = DGG.NORMAL
            cell.inventoryItem.inventoryCell.clearColorScale()
            cell.inventoryItem.destroy()
        if self.manager.heldFromCell:
            self.cellUsed(cell)
            self.manager.releaseHeld()
        messenger.send('UpdateSellContainer')

    def hasItemsToSell(self):
        for cell in self.gridDict.values():
            if cell.inventoryItem:
                return True

        return False

    def calculateTotalGoldValue(self):
        totalCost = 0
        for cell in self.gridDict.values():
            if cell.inventoryItem:
                totalCost += ItemGlobals.getGoldCost(cell.inventoryItem.getId()) * cell.inventoryItem.amount

        return totalCost

    def clearSale(self):
        for cell in self.gridDict.values():
            if cell.inventoryItem:
                cell.inventoryItem.inventoryCell['state'] = DGG.NORMAL
                cell.inventoryItem.inventoryCell.clearColorScale()
                cell.inventoryItem.destroy()

    def setupCellImage(self):
        gui = loader.loadModel('models/gui/gui_icons_weapon')
        self.gridBacking = gui.find('**/pir_t_gui_frm_inventoryBox')
        self.cellImage = (gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox'))
        self.workingCellImage = (
         gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox'))
        self.focusCellImage = (
         gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'))
        self.imageScale = 1.0
        self.imagePos = (0.0, 0.0, 0.0)
        self.relief = DGG.FLAT