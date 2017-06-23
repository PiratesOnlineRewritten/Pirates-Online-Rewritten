from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUISlotContainer
from pirates.inventory.InventoryUIGlobals import *
from pirates.makeapirate import ClothingGlobals
from pirates.inventory import InventoryRemoveConfirm
from pirates.inventory.InventoryGlobals import Locations
from pirates.inventory import InventoryGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory.InventoryGlobals import Locations
from pirates.inventory import ItemGlobals
from pirates.inventory import ItemConstants

class InventoryUIDressingContainer(InventoryUISlotContainer.InventoryUISlotContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, slotList=None):
        countX = 1
        countZ = len(ClothingGlobals.CLOTHING_STRING)
        InventoryUISlotContainer.InventoryUISlotContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ, slotList)
        self.containerType = CONTAINER_DRESSING
        self.initialiseoptions(InventoryUIDressingContainer)
        self.heldItemOldCell = None
        self.rightClickAction = {InventoryType.ItemTypeClothing: (Locations.RANGE_CLOTHES, None, 0)}
        self.accept('newItemHeld', self.handleNewHeldItem)
        return

    def manageCells(self, slotList):
        InventoryUISlotContainer.InventoryUISlotContainer.manageCells(self, slotList)
        tailorGui = loader.loadModel('models/textureCards/tailorIcons')
        for cell in self.cellList:
            if cell.slotId != None:
                if cell.slotId in Locations.RANGE_EQUIP_HAT_CLOTHES:
                    clothingIcon = tailorGui.find('**/icon_shop_tailor_hat')
                    scale = self.imageScale * self.cellSizeX * 0.7
                elif cell.slotId in Locations.RANGE_EQUIP_COAT_CLOTHES:
                    clothingIcon = tailorGui.find('**/icon_shop_tailor_coat')
                    scale = self.imageScale * self.cellSizeX * 0.7
                elif cell.slotId in Locations.RANGE_EQUIP_VEST_CLOTHES:
                    clothingIcon = tailorGui.find('**/icon_shop_tailor_vest')
                    scale = self.imageScale * self.cellSizeX * 0.6
                elif cell.slotId in Locations.RANGE_EQUIP_SHIRT_CLOTHES:
                    clothingIcon = loader.loadModel('models/gui/char_gui').find('**/chargui_cloth')
                    scale = self.imageScale * self.cellSizeX * 1.4
                elif cell.slotId in Locations.RANGE_EQUIP_BELT_CLOTHES:
                    clothingIcon = tailorGui.find('**/icon_shop_tailor_belt')
                    scale = self.imageScale * self.cellSizeX * 0.7
                elif cell.slotId in Locations.RANGE_EQUIP_PANTS_CLOTHES:
                    clothingIcon = tailorGui.find('**/icon_shop_tailor_pants')
                    scale = self.imageScale * self.cellSizeX * 0.7
                elif cell.slotId in Locations.RANGE_EQUIP_BOOTS_CLOTHES:
                    clothingIcon = tailorGui.find('**/icon_shop_tailor_booths')
                    scale = self.imageScale * self.cellSizeX * 0.7
                if not clothingIcon.isEmpty():
                    gui = loader.loadModel('models/gui/gui_icons_weapon')
                    cell['image'] = gui.find('**/pir_t_gui_frm_inventoryBox')
                    cell['image_color'] = (0.5, 0.5, 0.5, 1.0)
                    cell['geom'] = clothingIcon
                    cell['geom_scale'] = scale
                    cell['geom_pos'] = self.imagePos
                    cell['geom_color'] = (0.4, 0.4, 0.4, 1.0)
            cell.container.markCell(cell, MASK_EMPTYEQUIP)

        return

    def destroy(self):
        self.ignoreAll()
        InventoryUISlotContainer.InventoryUISlotContainer.destroy(self)

    def canDrag(self):
        return 1

    def canGive(self, myCell):
        if localAvatar.gameFSM.state in ('Fishing', 'ParlorGame'):
            return 0
        return InventoryUISlotContainer.InventoryUISlotContainer.canGive(self, myCell)

    def canReceive(self, myCell, fromSwap=0, itemInQuestion=None):
        if localAvatar.gameFSM.state in ('Fishing', 'ParlorGame'):
            return 0
        return InventoryUISlotContainer.InventoryUISlotContainer.canReceive(self, myCell, fromSwap, itemInQuestion)

    def wearItem(self, cell, location, remove=None, mouseAction=MOUSE_CLICK, task=None):
        itemToWear = cell.inventoryItem
        self.manager.wearItem(itemToWear, location, remove)

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
            equipLocation = InventoryGlobals.getClothingTypeBySlot(cell.slotId)
            gui = loader.loadModel('models/gui/gui_icons_weapon')
            if not cell.inventoryItem:
                self.wearItem(cell, equipLocation, remove=1)
                cell.container.markCell(cell, MASK_EMPTYEQUIP)
                cell.container.unmarkCell(cell, MASK_FULLEQUIP)
            else:
                cell.inventoryItem.refreshImageColor()
                self.wearItem(cell, equipLocation)
                cell.container.markCell(cell, MASK_FULLEQUIP)
                cell.container.unmarkCell(cell, MASK_EMPTYEQUIP)

    def testCellReqs(self, cell):
        if MASK_NOTMEETREQUIREMENTS in cell.statusMask:
            return 0
        else:
            return 1

    def canReceive(self, myCell, fromSwap=0, itemInQuestion=None):
        if itemInQuestion:
            pass
        if itemInQuestion and not self.manager.canLocalUseItem(itemInQuestion.itemTuple)[0]:
            return 0
        else:
            return InventoryUISlotContainer.InventoryUISlotContainer.canReceive(self, myCell, fromSwap)