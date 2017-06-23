from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIContainer
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory import InventoryRemoveConfirm

class InventoryUITrashContainer(InventoryUIContainer.InventoryUIContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0):
        InventoryUIContainer.InventoryUIContainer.__init__(self, manager, sizeX, sizeZ)
        self.containerType = CONTAINER_TRASH
        self.initialiseoptions(InventoryUITrashContainer)
        self.heldItemOldCell = None
        return

    def setup(self):
        gui = loader.loadModel('models/gui/toplevel_gui')
        cell = self.makeCell(self.cellImage)
        geomImage = (gui.find('**/pir_t_gui_but_trash'), gui.find('**/pir_t_gui_but_trash'), gui.find('**/pir_t_gui_but_trash_over'), gui.find('**/pir_t_gui_but_trash'))
        cell['geom'] = geomImage
        cell['geom_scale'] = 0.4

    def destroy(self):
        self.ignoreAll()
        InventoryUIContainer.InventoryUIContainer.destroy(self)

    def canDrag(self):
        return 0

    def trashItem(self, cell, mouseAction=MOUSE_CLICK, task=None):
        itemToTrash = self.manager.heldItem
        self.manager.releaseHeld()
        self.manager.deleteItem(itemToTrash)

    def releaseItem(self):
        trashCell = self.cellList[0]
        if not trashCell.inventoryItem:
            return
        item = trashCell.inventoryItem
        item.cell = self.heldItemOldCell
        self.heldItemOldCell.inventoryItem = item
        trashCell.inventoryItem = None
        self.manager.putIntoHeld(item, self.heldItemOldCell)
        self.heldItemOldCell = None
        self.manager.releaseHeld()
        return

    def discardItem(self):
        trashCell = self.cellList[0]
        item = trashCell.inventoryItem
        item.cell = self.heldItemOldCell
        self.heldItemOldCell.inventoryItem = item
        trashCell.inventoryItem = None
        self.manager.putIntoHeld(item, self.heldItemOldCell)
        self.heldItemOldCell = None
        itemToTrash = self.manager.heldItem
        self.manager.releaseHeld()
        self.manager.deleteItem(itemToTrash)
        return

    def cellUsed(self, cell):
        if self.manager.heldFromCell:
            self.heldItemOldCell = self.manager.heldFromCell
            self.manager.openRemover(self.manager.heldFromCell)

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