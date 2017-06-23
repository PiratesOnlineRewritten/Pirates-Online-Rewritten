from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUISlotContainer
from pirates.inventory.InventoryUIGlobals import *
from pirates.makeapirate import TattooGlobals
from pirates.inventory import InventoryRemoveConfirm
from pirates.inventory.InventoryGlobals import Locations
from pirates.inventory import InventoryGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory.InventoryGlobals import Locations
from pirates.inventory import ItemGlobals
from pirates.inventory import ItemConstants

class InventoryUITattooDressingContainer(InventoryUISlotContainer.InventoryUISlotContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, slotList=None, background=None):
        self.background = background
        countX = 2
        countZ = len(TattooGlobals.ZONE_LIST) / 2
        InventoryUISlotContainer.InventoryUISlotContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ, slotList)
        self.containerType = CONTAINER_TATTOO
        self.initialiseoptions(InventoryUITattooDressingContainer)
        self.heldItemOldCell = None
        self.rightClickAction = {InventoryType.ItemTypeTattoo: (Locations.RANGE_JEWELERY_AND_TATTOO, None, 0)}
        self.accept('newItemHeld', self.handleNewHeldItem)
        return

    def manageCells(self, slotList):
        InventoryUISlotContainer.InventoryUISlotContainer.manageCells(self, slotList)
        tattooGui = loader.loadModel('models/textureCards/tattooIcons')
        for cell in self.cellList:
            flip = 0
            if cell.slotId != None:
                if cell.slotId in Locations.RANGE_EQUIP_L_ARM_TATTOO:
                    tattooIcon = tattooGui.find('**/icon_shop_tailor_arm')
                    scale = self.imageScale * self.cellSizeX * 0.6
                    flip = 1
                elif cell.slotId in Locations.RANGE_EQUIP_R_ARM_TATTOO:
                    tattooIcon = tattooGui.find('**/icon_shop_tailor_arm')
                    scale = self.imageScale * self.cellSizeX * 0.6
                elif cell.slotId in Locations.RANGE_EQUIP_CHEST_TATTOO:
                    tattooIcon = tattooGui.find('**/icon_shop_tailor_chest_male')
                    scale = self.imageScale * self.cellSizeX * 0.6
                elif cell.slotId in Locations.RANGE_EQUIP_FACE_TATTOO:
                    tattooIcon = tattooGui.find('**/icon_shop_tailor_face_male')
                    scale = self.imageScale * self.cellSizeX * 0.6
                if not tattooIcon.isEmpty():
                    gui = loader.loadModel('models/gui/gui_icons_weapon')
                    cell['image'] = gui.find('**/pir_t_gui_frm_inventoryBox')
                    cell['image_color'] = (0.5, 0.5, 0.5, 1.0)
                    cell['geom'] = tattooIcon
                    if flip:
                        cell['geom_scale'] = (
                         -scale, 0, scale)
                    else:
                        cell['geom_scale'] = (
                         scale, 0, scale)
                    cell['geom_pos'] = self.imagePos
                    cell['geom_color'] = (0.4, 0.4, 0.4, 1.0)
            cell.container.markCell(cell, MASK_EMPTYEQUIP)

        return

    def destroy(self):
        self.ignoreAll()
        InventoryUISlotContainer.InventoryUISlotContainer.destroy(self)

    def canDrag(self):
        return 1

    def wearTattoo(self, cell, type, remove=None, mouseAction=MOUSE_CLICK, task=None):
        itemToWear = cell.inventoryItem
        self.manager.wearTattoo(itemToWear, type, remove)
        if remove:
            gui = loader.loadModel('models/gui/gui_icons_weapon')

    def releaseItem(self):
        dressCell = self.cellList[0]
        if not dressCell.inventoryItem:
            return
        item = dressCell.inventoryItem
        item.cell = self.heldItemOldCell
        self.heldItemOldCell.inventoryItem = item
        dressCell.inventoryItem = None
        self.manager.putIntoHeld(item, self.heldItemOldCell)
        self.heldItemOldCell = None
        self.manager.releaseHeld()
        return

    def handleNewHeldItem(self, itemTuple, canUse):
        if itemTuple != None:
            itemCat = itemTuple[0]
            itemId = itemTuple[1]
            itemRanges = InventoryGlobals.getEquipRanges(itemCat, itemId)
            if not itemRanges:
                return
            itemUseSlots = InventoryGlobals.expandRanges(itemRanges)
            for cell in self.cellList:
                if cell.slotId:
                    if cell.slotId in itemUseSlots:
                        cell.container.markCell(cell, MASK_ISDEST)
                        cell.container.unmarkCell(cell, MASK_NOTDEST)
                        canUse or cell.container.markCell(cell, MASK_NOTMEETREQUIREMENTS)
                else:
                    cell.container.markCell(cell, MASK_NOTDEST)
                    cell.container.unmarkCell(cell, MASK_ISDEST)

        else:
            for cell in self.cellList:
                cell.container.unmarkCell(cell, MASK_NOTDEST)
                cell.container.unmarkCell(cell, MASK_ISDEST)
                cell.container.unmarkCell(cell, MASK_NOTMEETREQUIREMENTS)
                self.checkReqsForCell(cell)

        return

    def colorizeCell(self, cell, color):
        cell['image_color'] = color
        if cell.inventoryItem:
            cell['geom_color'] = (0.0, 0.0, 0.0, 0.0)
        else:
            cell['geom_color'] = color

    def postUpdate(self, cell):
        if cell and cell.slotId:
            location = InventoryGlobals.getTattooLocationBySlot(cell.slotId)
            gui = loader.loadModel('models/gui/gui_icons_weapon')
            if not cell.inventoryItem:
                self.wearTattoo(cell, location, remove=1)
                cell.container.markCell(cell, MASK_EMPTYEQUIP)
                cell.container.unmarkCell(cell, MASK_FULLEQUIP)
            else:
                cell.inventoryItem.refreshImageColor()
                self.wearTattoo(cell, location)
                cell.container.markCell(cell, MASK_FULLEQUIP)
                cell.container.unmarkCell(cell, MASK_EMPTYEQUIP)
        avInv = localAvatar.getInventory()
        if avInv and avInv.findAvailableLocation(InventoryType.ItemTypeTattoo) in [Locations.INVALID_LOCATION, Locations.NON_LOCATION]:
            localAvatar.sendRequestContext(InventoryType.InventoryFull)

    def testCellReqs(self, cell):
        if MASK_NOTMEETREQUIREMENTS in cell.statusMask:
            return 0
        else:
            return 1

    def canGive(self, myCell):
        if localAvatar.gameFSM.state in ('Fishing', 'ParlorGame'):
            return 0
        return InventoryUISlotContainer.InventoryUISlotContainer.canGive(self, myCell)

    def canReceive(self, myCell, fromSwap=0, itemInQuestion=None):
        if localAvatar.gameFSM.state in ('Fishing', 'ParlorGame'):
            return 0
        return InventoryUISlotContainer.InventoryUISlotContainer.canReceive(self, myCell, fromSwap, itemInQuestion)