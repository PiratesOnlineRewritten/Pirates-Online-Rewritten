from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIContainer
from pirates.inventory.InventoryUIGlobals import *

class InventoryUISlotDisplayGrid(InventoryUIContainer.InventoryUIContainer):
    ReferenceSlots = True

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=1, countZ=1, slotList=[]):
        InventoryUIContainer.InventoryUIContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ, slotList)
        self.containerType = CONTAINER_SLOTDISPLAY
        self.initialiseoptions(InventoryUISlotDisplayGrid)

    def canDrag(self):
        return 0

    def testWithIn(self):
        return 0

    def manageCells(self, slotList):
        self.slotList = slotList
        for index in range(len(self.slotList)):
            slot = self.slotList[index]
            cell = self.cellList[index]
            cell.showLabel = 1
            cell.labelText = 'F%s' % slot
            cell.label['text'] = cell.labelText
            textScale = 0.25 * self.cellSizeX * 50.0
            cell.label.show()
            if self.manager.slotToCellMap.get(slot):
                self.setupSlotLink(cell, slot)
            self.accept('inventory_slot_assigned %s' % slot, self.setupSlotLink, extraArgs=[cell])

    def setupSlotLink(self, cell, slotId):
        fromCell = self.manager.slotToCellMap.get(slotId)
        if cell and fromCell and fromCell.inventoryItem:
            cell.hotlink = fromCell.inventoryItem
            fromCell.inventoryItem.hotlink = cell
            cell['geom'] = fromCell.inventoryItem['image']
            cell['geom_scale'] = 0.9 * self.cellSizeX * fromCell.inventoryItem.imageScale

    def cellClick(self, cell, mouseAction=MOUSE_CLICK, task=None):
        if cell.hotlink and mouseAction == MOUSE_CLICK:
            messenger.send('f%s' % cell.hotlink.cell.slotId)