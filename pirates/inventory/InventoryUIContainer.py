from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory.InventoryGlobals import Locations
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.uberdog import InventoryRequestBase
from pirates.inventory import ItemGlobals
from sets import Set

class InventoryUIContainer(DirectFrame, InventoryRequestBase.InventoryRequestBase):
    testItemCount = 0
    cellCount = 0
    detailsDelay = 0.3
    detailsPos = None
    detailsHeight = None
    notify = directNotify.newCategory('InventoryUIContainer')

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=None, countZ=None, cellInfo=None):
        if not manager.hasContainerBeenAdded(self):
            optiondefs = (
             (
              'state', DGG.NORMAL, self.setState),)
            self.defineoptions({}, optiondefs)
            DirectFrame.__init__(self, parent=NodePath())
            InventoryRequestBase.InventoryRequestBase.__init__(self)
            self.manager = manager
            self.manager.addContainer(self)
            self.sizeX = sizeX
            self.sizeZ = sizeZ
            self.cellSizeX = sizeX
            self.cellSizeZ = sizeZ
            self.screenSizeMult = 0.5
            self.screenSizeX = (base.a2dRight - base.a2dLeft) * self.screenSizeMult
            self.screenSizeZ = (base.a2dTop - base.a2dBottom) * self.screenSizeMult
            self.cellList = []
            self.containerType = CONTAINER_NORMAL
            self.cellClickedCommand = self.cellClick
            self.rightClickAction = {}
            self.rolloverSound = None
            self.setupBackground()
            self.setupCellImage()
            self.titleImageOpen = None
            self.titleImageClosed = None
            self.titleName = None
            self.setTitleInfo()
            if countX and countZ:
                self.setupGrid(countX, countZ)
            self.manageCells(cellInfo)
            self.accept('localLevelUp', self.checkReqs)
        return

    def manageCells(self, cellInfo):
        pass

    def getItemPriceMult(self):
        return ItemGlobals.GOLD_SALE_MULTIPLIER

    def setTitleInfo(self):
        gui = loader.loadModel('models/gui/toplevel_gui')
        chestButtonOpen = gui.find('**/treasure_chest_open')
        chestButtonClosed = gui.find('**/treasure_chest_closed')
        self.titleImageOpen = chestButtonOpen
        self.titleImageClosed = chestButtonClosed
        self.titleName = 'Generic'
        self.titleImageOpen.setScale(0.17)
        self.titleImageClosed.setScale(0.17)

    def destroy(self):
        self.clearOut()
        self.ignoreAll()
        self.cellClickedCommand = None
        self.manager = None
        DirectFrame.destroy(self)
        return

    def clearOut(self):
        for cell in self.cellList:
            cell.inventoryItem = None
            cell.container = None
            cell.number = None
            cell.hotlink = None
            cell.unbind(DGG.ENTER)
            cell.unbind(DGG.EXIT)
            cell.unbind(DGG.WITHIN)
            cell.unbind(DGG.WITHOUT)
            if cell.boundEvent:
                cell.ignore(cell.boundEvent)
            cell.destroy()

        self.cellList = []
        return

    def canDrag(self):
        return 1

    def testWithIn(self):
        return 1

    def makeCell(self, cellImage=None, imageScale=None, imagePos=None, frameScale=(1.0, 1.0), offset=(0.0, 0.0)):
        textScale = 0.25 * self.cellSizeX
        if not imageScale:
            imageScale = self.imageScale
        if not imagePos:
            imagePos = self.imagePos
        if not cellImage:
            cell = DirectButton(parent=self, relief=None, rolloverSound=self.rolloverSound, frameSize=(offset[0] + self.cellSizeX * -0.5 * frameScale[0], offset[0] + self.cellSizeX * 0.5 * frameScale[0], offset[1] + self.cellSizeZ * -0.5 * frameScale[1], offset[1] + self.cellSizeZ * 0.5 * frameScale[1]), textMayChange=1, text='', text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_scale=textScale, text_pos=(0.0, self.cellSizeZ * -0.27), pos=(self.cellSizeX * 0.5, 0.0, self.cellSizeZ * 0.5), command=self.cellClick, extraArgs=[None])
        else:
            imageScale = imageScale * self.cellSizeX
            cell = DirectButton(parent=self, relief=None, rolloverSound=self.rolloverSound, textMayChange=1, image=cellImage, image_scale=imageScale, image_pos=imagePos, frameSize=(imagePos[0] - imageScale / 2.0, imagePos[0] + imageScale / 2.0, imagePos[2] - imageScale / 2.0, imagePos[2] + imageScale / 2.0), text='', text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_scale=textScale, text_pos=(0.0, self.cellSizeZ * -0.27), pos=(self.cellSizeX * 0.5, 0.0, self.cellSizeZ * 0.5), command=self.cellClick, extraArgs=[None])
        cell.cellSizeX = self.cellSizeX
        cell.cellSizeZ = self.cellSizeZ
        cell['extraArgs'] = [cell]
        cellLabel = DirectLabel(parent=cell, textMayChange=1, text='', text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=PiratesGuiGlobals.TextFG2, text_scale=textScale, text_align=TextNode.ARight, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.45 * self.cellSizeX - 0, -0.65 * self.cellSizeZ + textScale))
        cellLabel.hide()
        cell.labelText = ''
        cell.boundEvent = None
        cell.labelEvent = None
        cell.label = cellLabel
        cell.inventoryItem = None
        cell.hotlink = None
        cell.container = self
        cell.number = InventoryUIContainer.cellCount
        cell.showLabel = 0
        cell.statusMask = Set([])
        InventoryUIContainer.cellCount += 1
        if self.testWithIn():
            cell.bind(DGG.ENTER, self.manager.startCellItemDetails, extraArgs=[cell, self.detailsPos, self.detailsHeight, self.detailsDelay])
            cell.bind(DGG.EXIT, self.manager.cancelCellItemDetails)
            cell.bind(DGG.WITHIN, self.manager.setWithin, extraArgs=[cell, 0])
            cell.bind(DGG.WITHOUT, self.manager.setWithin, extraArgs=[cell, 1])
        else:
            cell.bind(DGG.ENTER, self.enterCell, extraArgs=[cell])
            cell.bind(DGG.EXIT, self.exitCell, extraArgs=[cell])
        cell.bind(DGG.B1PRESS, self.manager.withinDrag)
        cell.bind(DGG.B3PRESS, self.manager.rightPress)
        self.cellList.append(cell)
        cell.slotId = None
        return cell

    def makeCellLabel(self, cell):
        if cell.label.isEmpty():
            cellLabel = DirectLabel(parent=cell, textMayChange=1, text='', text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=PiratesGuiGlobals.TextFG2, text_scale=textScale, text_align=TextNode.ARight, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.45 * self.cellSizeX - 0, 0.45 * self.cellSizeZ - textScale))
            cell.label = cellLabel
            cell.label['text'] = cell.labelText

    def handleWithIn(self, cell, clear):
        pass

    def enterCell(self, cell, pos=None):
        self.manager.startCellItemDetails(cell, self.detailsPos, self.detailsHeight, self.detailsDelay)
        self.manager.setWithin(cell, 0)

    def exitCell(self, cell, pos=None):
        self.manager.cancelCellItemDetails()
        self.manager.setWithin(cell, 1)

    def countItems(self):
        itemCount = 0
        for cell in self.cellList:
            if cell.inventoryItem:
                itemCount += 1

        return itemCount

    def getTotalHeight(self):
        return self.sizeZ

    def resizeItem(self, item):
        sizeProp = 0.46
        textScale = 0.25 * self.cellSizeX
        item.setScale(1, 1, 1)
        item['frameSize'] = (self.cellSizeX * -sizeProp, self.cellSizeX * sizeProp, self.cellSizeZ * -sizeProp, self.cellSizeZ * sizeProp)
        item['borderWidth'] = (self.cellSizeX * 0.05, self.cellSizeX * 0.05)
        item['text_scale'] = textScale * item.textScale
        item['text_pos'] = (0.0, self.cellSizeZ * item.textOffset + textScale * 0.35)
        item['image_scale'] = 0.9 * self.cellSizeX * item.imageScale

    def markCell(self, cell, maskBit):
        cell.statusMask.add(maskBit)
        self.colorStatus(cell)

    def unmarkCell(self, cell, maskBit):
        cell.statusMask.discard(maskBit)
        self.colorStatus(cell)

    def colorizeCell(self, cell, color):
        cell['image_color'] = color
        if cell.inventoryItem:
            cell.inventoryItem['image_color'] = (
             cell.inventoryItem.iconColor[0], cell.inventoryItem.iconColor[1], cell.inventoryItem.iconColor[2], cell.inventoryItem.iconColor[3])

    def colorStatus(self, cell):
        if not cell.statusMask:
            cell['image'] = self.cellImage
            self.colorizeCell(cell, CELL_COLOR_NORMAL)
        elif MASK_TRASH in cell.statusMask:
            cell['image'] = self.focusCellImage
            self.colorizeCell(cell, CELL_COLOR_TRASH)
        elif MASK_HELD in cell.statusMask:
            cell['image'] = self.focusCellImage
            self.colorizeCell(cell, CELL_COLOR_HELD)
        elif MASK_NOTMEETREQUIREMENTS in cell.statusMask:
            cell['image'] = self.workingCellImage
            self.colorizeCell(cell, CELL_COLOR_NOTMEETREQUIREMENTS)
        elif MASK_ISDEST in cell.statusMask:
            cell['image'] = self.workingCellImage
            self.colorizeCell(cell, CELL_COLOR_ISDEST)
        elif MASK_NOTDEST in cell.statusMask:
            cell['image'] = self.workingCellImage
            self.colorizeCell(cell, CELL_COLOR_NOTDEST)
        elif MASK_EMPTYEQUIP in cell.statusMask:
            cell['image'] = self.workingCellImage
            self.colorizeCell(cell, CELL_COLOR_EMPTYEQUIP)
        elif MASK_FULLEQUIP in cell.statusMask:
            cell['image'] = self.focusCellImage
            self.colorizeCell(cell, CELL_COLOR_FULLEQUIP)
        elif MASK_PENDING in cell.statusMask:
            cell['image'] = self.workingCellImage
            self.colorizeCell(cell, CELL_COLOR_PENDING)

    def putIntoCell(self, item, cell):
        if cell and item and not cell.inventoryItem:
            if item.cell:
                self.unHotlinkItem(item)
                item.cell.label.reparentTo(item.cell)
                item.cell.inventoryItem = None
                item.cell = None
            self.resizeItem(item)
            cell.inventoryItem = item
            item.reparentTo(cell)
            item.cell = cell
            item.onPutInCell()
            if cell['image']:
                cell.inventoryItem['image_color'] = (cell.inventoryItem.iconColor[0], cell.inventoryItem.iconColor[1], cell.inventoryItem.iconColor[2], cell.inventoryItem.iconColor[3])
            if cell.showLabel:
                cell.label.reparentTo(item)
            if cell.slotId:
                messenger.send('inventory_slot_assigned %s' % cell.slotId, [cell.slotId])
        return

    def assignSlot(self, cell, slotId):
        cell.slotId = slotId
        messenger.send('inventory_slot_assigned %s' % cell.slotId, [cell.slotId])

    def grabCellItem(self, cell):
        item = cell.inventoryItem
        self.unHotlinkCell(cell)
        if item:
            cell.inventoryItem.reparentTo(hidden)
            item.hideDetails()
        cell.label.reparentTo(cell)
        return item

    def unHotlinkCell(self, cell):
        if cell.hotlink:
            unlink = cell.hotlink
            cell.hotlink = None
            if unlink.hotlink:
                self.unHotlinkItem(unlink)
        if cell.container.containerType == CONTAINER_HOTLINK:
            cell['geom'] = None
            cell['text'] = ''
        elif cell.container.containerType == CONTAINER_SLOTDISPLAY:
            cell['geom'] = None
            cell['text'] = ''
        return

    def unHotlinkItem(self, item):
        if item.hotlink:
            unlink = item.hotlink
            item.hotlink = None
            if unlink.hotlink:
                self.unHotlinkCell(unlink)
        return

    def tryPutIntoFirstOpenCell(self, item):
        for cell in self.cellList:
            if not cell.inventoryItem:
                self.putIntoCell(item, cell)
                return 1

        return 0

    def takeOut(self):
        messenger.send('openingContainer', [self])

    def putAway(self):
        if self.manager.heldFromCell in self.cellList:
            self.manager.releaseHeld()

    def onRelease(self, cell):
        pass

    def postClick(self, cell):
        pass

    def postPickupLockout(self):
        pass

    def postUpdate(self, cell):
        if cell in self.cellList:
            self.checkReqsForCell(cell)

    def canSwap(self, myCell, otherCell):
        if not (myCell.inventoryItem and otherCell.inventoryItem):
            return 0
        elif self.canGive(myCell) and otherCell.container and otherCell.container.canGive(otherCell) and self.canReceive(myCell, fromSwap=1, itemInQuestion=otherCell.inventoryItem) and otherCell.container.canReceive(otherCell, fromSwap=1, itemInQuestion=myCell.inventoryItem):
            return 1
        else:
            return 0

    def canGive(self, myCell):
        if myCell.inventoryItem and not self.manager.isSlotPending(myCell.slotId):
            return 1
        return 0

    def canReceive(self, myCell, fromSwap=0, itemInQuestion=None):
        if myCell.inventoryItem and not fromSwap or self.manager.isSlotPending(myCell.slotId) or MASK_NOTDEST in myCell.statusMask:
            if myCell.inventoryItem:
                print ' ->Item%s' % myCell.inventoryItem.getName()
            return 0
        return 1

    def putHeldInCell(self, cell):
        heldItem = self.manager.removeFromHeld()
        self.putIntoCell(heldItem, cell)

    def checkEmpty(self):
        pass

    def cellUsed(self, cell):
        if self.manager.heldItem:
            if cell.inventoryItem and cell.inventoryItem == self.manager.heldItem:
                self.manager.releaseHeld()
            elif self.canSwap(cell, self.manager.heldFromCell) and self.manager.heldFromCell.container.canSwap(self.manager.heldFromCell, cell):
                self.manager.swapHeldWithCell(cell)
            elif self.canReceive(cell, itemInQuestion=self.manager.heldItem):
                self.manager.placeHeldIntoCell(cell)
            else:
                self.manager.displayReasonNoUse(popUp=1)
                if cell.inventoryItem:
                    self.manager.testFullSlot()
                self.manager.releaseHeld()
        elif self.canGive(cell):
            self.manager.putIntoHeld(self.grabCellItem(cell), cell)

    def cellClick(self, cell, mouseAction=MOUSE_CLICK, task=None):
        if self.manager.locked:
            return
        if not self.manager.heldItem:
            self.manager.itemPickup = PICKUP_EMPTY
        if mouseAction == MOUSE_CLICK and self.manager.itemPickup == PICKUP_DRAG and not self.manager.pickupTimedOut and cell == self.manager.heldFromCell:
            self.manager.itemPickup = PICKUP_CLICK
        elif mouseAction == MOUSE_CLICK and self.manager.itemPickup == PICKUP_EMPTY and not self.canDrag():
            self.manager.itemPickup = PICKUP_CLICK
            self.cellUsed(cell)
        elif mouseAction == MOUSE_CLICK and self.manager.itemPickup == PICKUP_CLICK:
            self.cellUsed(cell)
        elif mouseAction == MOUSE_PRESS and self.manager.itemPickup == PICKUP_EMPTY and self.canDrag():
            self.manager.itemPickup = PICKUP_DRAG
            self.manager.startPickupWithTimer()
            self.cellUsed(cell)
        elif mouseAction == MOUSE_RELEASE and self.manager.itemPickup == PICKUP_DRAG:
            self.cellUsed(cell)
            self.manager.releaseHeld()

    def setupGrid(self, gridX=4, gridZ=4):
        self.gridDict = {}
        self.gridX = gridX
        self.gridZ = gridZ
        self.cellSizeX = self.sizeX / float(gridX)
        self.cellSizeZ = self.sizeZ / float(gridZ)
        self.gridBackground = self.attachNewNode('grid-background')
        for Z in range(gridZ - 1, -1, -1):
            for X in range(gridX):
                gridCell = self.makeCell(self.cellImage)
                cellPos = self.findGridPos(X, Z)
                gridCell.setPos(cellPos)
                self.gridDict[X, Z] = gridCell
                self.makeCellBacking(cellPos)

        self.gridBackground.flattenStrong()

    def makeCellBacking(self, cellPos):
        backing = self.gridBacking.copyTo(self.gridBackground)
        backing.setPos(cellPos)
        backing.setScale(self.imageScale * self.cellSizeX)

    def findGridPos(self, x, z):
        return Point3((float(x) + 0.5) * self.cellSizeX, 0, (float(z) + 0.5) * self.cellSizeZ)

    def putIntoGrid(self, item, gridX, gridZ):
        gridCell = self.gridDict.get((gridX, gridZ))
        self.putIntoCell(item, gridCell)
        return item.cell == gridCell

    def setupBackground(self):
        pass

    def setupCellImage(self):
        gui = loader.loadModel('models/gui/gui_icons_weapon')
        self.gridBacking = gui.find('**/pir_t_gui_frm_inventoryBox')
        self.cellImage = (NodePath('empty'), gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox'))
        self.workingCellImage = (
         gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox'))
        self.focusCellImage = (
         gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'))
        self.imageScale = 1.0
        self.imagePos = (0.0, 0.0, 0.0)
        self.relief = DGG.FLAT

    def cellRightClick(self, cell, mouseAction=MOUSE_CLICK, task=None):
        if mouseAction == MOUSE_PRESS:
            if cell.inventoryItem and self.manager.heldItem == None and (localAvatar.guiMgr.combatTray.isUsingSkill or localAvatar.guiMgr.combatTray.isCharging):
                localAvatar.guiMgr.createWarning(PLocalizer.NoSwitchingItemsWarning, PiratesGuiGlobals.TextFG6)
                return
            rangeData = self.rightClickAction.get(cell.inventoryItem.getCategory())
            if rangeData == None:
                return
            flatRange = rangeData[0]
            rangeTypeDict = rangeData[1]
            canRightClickReplace = rangeData[2]
            destCell = None
            if flatRange:
                if len(flatRange) > 1:
                    slotRange = range(flatRange[0], flatRange[1] + 1)
                else:
                    slotRange = (
                     flatRange[0],)
                for slotId in slotRange:
                    destSlot = slotId
                    testCell = self.manager.slotToCellMap.get(destSlot)
                    itemInfo = cell.inventoryItem.itemTuple
                    itemType = ItemGlobals.getType(itemInfo[1])
                    if self.manager.isSlotPending(destSlot):
                        pass
                    elif testCell.inventoryItem and ItemGlobals.getType(testCell.inventoryItem.itemTuple[1]) == itemType:
                        destCell = testCell
                    elif testCell.inventoryItem == None:
                        destCell = testCell
                        break

            elif rangeTypeDict:
                itemInfo = cell.inventoryItem.itemTuple
                itemType = ItemGlobals.getType(itemInfo[1])
                subtypeRange = rangeTypeDict.get(itemType)
                if len(subtypeRange) > 1:
                    slotRange = range(subtypeRange[0], subtypeRange[1] + 1)
                else:
                    slotRange = (
                     subtypeRange[0],)
                if slotRange:
                    for slotId in slotRange:
                        destSlot = slotId
                        destCell = self.manager.slotToCellMap.get(destSlot)
                        if destCell.inventoryItem == None:
                            break

            if destCell and cell.inventoryItem and not self.manager.isSlotPending(destCell.slotId):
                if self.manager.testCanUse(cell.inventoryItem.itemTuple):
                    self.manager.putIntoHeld(cell.inventoryItem, cell)
                    if destCell.inventoryItem:
                        if canRightClickReplace:
                            self.manager.swapHeldWithCell(destCell)
                        else:
                            self.manager.displaySlotFullReason()
                    else:
                        self.manager.placeHeldIntoCell(destCell)
                else:
                    self.manager.displayReasonNoUse(popUp=0)
                self.manager.releaseHeld()
        return

    def testCellReqs(self, cell):
        return 1
        if MASK_NOTMEETREQUIREMENTS in cell.statusMask:
            return 0
        else:
            return 1

    def checkReqsForCell(self, cell):
        if cell.inventoryItem:
            canUse, Reason = self.manager.canLocalUseItem(cell.inventoryItem.itemTuple)
            if not canUse and cell != self.manager.heldFromCell:
                cell.container.markCell(cell, MASK_NOTMEETREQUIREMENTS)
                return
        cell.container.unmarkCell(cell, MASK_NOTMEETREQUIREMENTS)

    def checkReqs(self, thing=None, thing2=None):
        for cell in self.cellList:
            self.checkReqsForCell(cell)