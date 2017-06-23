from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIContainer
from pirates.inventory import ItemGlobals
from pirates.inventory.InventoryUIGlobals import *
from pirates.uberdog.UberDogGlobals import *
from pirates.battle import WeaponGlobals

class InventoryUIPlunderGridContainer(InventoryUIContainer.InventoryUIContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=4, countZ=4):
        InventoryUIContainer.InventoryUIContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ)
        self.xCount = 0
        self.zCount = 0
        self.containerType = CONTAINER_PLUNDER
        self.initialiseoptions(InventoryUIPlunderGridContainer)
        SkillIcons = loader.loadModel('models/textureCards/skillIcons')
        cellImageStack = (SkillIcons.find('**/base'), SkillIcons.find('**/base_down'), SkillIcons.find('**/base_over'))
        self.stackImage = cellImageStack
        gui = loader.loadModel('models/gui/gui_icons_weapon')
        cellImageStack2 = gui.find('**/pir_t_gui_frm_inventoryBox')
        extraCell = gui.find('**/pir_t_gui_frm_inventoryBox_over')
        extraCell.setScale(0.7)
        extraCell.reparentTo(cellImageStack2)
        cellImageStack2.flattenStrong()
        self.stackImage2 = cellImageStack2

    def setupPlunder(self, plunderList):
        for itemClass, itemId, stackAmount in plunderList:
            itemTuple = [itemClass, itemId, 0, stackAmount]
            if itemClass == InventoryType.ItemTypeWeapon:
                item = self.manager.makeWeaponItem(itemTuple)
            elif itemClass == InventoryType.ItemTypeCharm:
                item = self.manager.makeCharmItem(itemTuple)
            else:
                if itemClass == InventoryType.ItemTypeConsumable:
                    item = self.manager.makeConsumableItem(itemTuple, showMax=0)
                elif itemClass == InventoryType.ItemTypeClothing:
                    item = self.manager.makeClothingItem(itemTuple)
                elif itemClass == InventoryType.ItemTypeMoney:
                    item = self.manager.makeGoldItem(itemTuple)
                elif itemClass == InventoryType.TreasureCollection:
                    item = self.manager.makeTreasureItem(itemTuple)
                elif itemClass == InventoryCategory.CARDS:
                    cardId = itemId
                    itemTuple[1] -= InventoryType.begin_Cards
                    item = self.manager.makeCardItem(cardId, itemTuple, imageScaleFactor=1.9)
                elif itemClass == InventoryCategory.WEAPON_PISTOL_AMMO:
                    itemTuple[1] = WeaponGlobals.getSkillAmmoInventoryId(itemId)
                    item = self.manager.makeAmmoItem(itemId, itemTuple, showMax=0)
                elif itemClass == InventoryCategory.MONEY:
                    item = self.manager.makeMaterialItem(itemId, itemTuple, showMax=0)
                if itemClass in (InventoryType.ItemTypeMoney, InventoryCategory.CARDS, InventoryType.TreasureCollection, InventoryCategory.MONEY):
                    self.addGridCell(self.stackImage, 1.0)
                if itemClass == InventoryCategory.WEAPON_PISTOL_AMMO:
                    self.addGridCell(self.stackImage2, 1.0)
                self.addGridCell()
            self.tryPutIntoFirstOpenCell(item)

    def putIntoCell(self, item, cell):
        cell.showLabel = 1
        InventoryUIContainer.InventoryUIContainer.putIntoCell(self, item, cell)
        cell.label['text'], cell.label['text_fg'] = item.getPlunderName()
        cell.show()
        cell.label.show()

    def grabCellItem(self, cell):
        cell.showLabel = 0
        returnItem = InventoryUIContainer.InventoryUIContainer.grabCellItem(self, cell)
        cell.label.hide()
        return returnItem

    def onRelease(self, cell):
        cell.show()
        cell.label.show()

    def postClick(self, cell):
        if not cell.inventoryItem or cell.inventoryItem == self.manager.heldItem:
            cell.hide()
        else:
            cell.show()

    def postPickupLockout(self):
        if self.manager.heldItem and self.manager.heldItem.cell and self.manager.heldItem.cell in self.cellList:
            self.manager.heldItem.cell.hide()
        else:
            import pdb
            pdb.set_trace()

    def makeCell(self, cellImage=None, imageScale=None, imagePos=None):
        returnCell = InventoryUIContainer.InventoryUIContainer.makeCell(self, cellImage, imageScale, imagePos)
        textScale = 0.3 * self.cellSizeX
        returnCell.label['text_align'] = TextNode.ALeft
        returnCell.label['text_scale'] = textScale
        returnCell.label['text_font'] = PiratesGlobals.getInterfaceOutlineFont()
        returnCell.label['text_pos'] = (0.55 * self.cellSizeX - 0, 0.45 * self.cellSizeZ - textScale)
        returnCell.label['text_wordwrap'] = self.spaceSizeX / textScale
        returnCell.hide()
        return returnCell

    def canSwap(self, myCell, otherCell):
        return 0

    def canReceive(self, myCell, fromSwap=0, itemInQuestion=None):
        return 0

    def putHeldInCell(self, cell):
        fromCell = self.manager.heldFromCell
        self.manager.releaseHeld()
        self.manager.takePlunderItemFromCell(fromCell, cell)

    def checkEmpty(self):
        self.notify.debug('  itemCount %s' % self.countItems())
        if self.countItems() == 0:
            messenger.send('lootsystem-plunderContainer-Empty', [])

    def cellUsed(self, cell):
        self.notify.debug('CELL USED')
        if self.manager.heldItem:
            InventoryUIContainer.InventoryUIContainer.cellUsed(self, cell)
        elif cell.inventoryItem and (cell.inventoryItem.itemType in (ITEM_STACK, ITEM_NOTRADE) or not self.manager.localInventoryOpen):
            self.manager.itemPickup = PICKUP_EMPTY
            self.manager.takePlunderItemFromCell(cell)
        else:
            InventoryUIContainer.InventoryUIContainer.cellUsed(self, cell)
        self.checkEmpty()

    def postUpdate(self):
        InventoryUIContainer.InventoryUIContainer.postUpdate(self)
        messenger.send('lootsystem-plunderContainer-Empty', [])

    def setupCellImage(self):
        gui = loader.loadModel('models/gui/gui_icons_weapon')
        self.cellImage = (gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox'))
        self.workingCellImage = (
         gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox'))
        self.focusCellImage = (
         gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'), gui.find('**/pir_t_gui_frm_inventoryBox_over'))
        self.imageScale = 1.0
        self.imagePos = (0.0, 0.0, 0.0)
        self.relief = DGG.FLAT

    def makeCellBacking(self, cellPos):
        pass

    def setupGrid(self, gridX=4, gridZ=4):
        self.gridDict = {}
        self.gridX = gridX
        self.gridZ = gridZ
        self.cellSizeX = self.sizeX / float(gridX)
        self.cellSizeZ = self.sizeZ / float(gridZ)
        self.spaceSizeX = 0.0
        if self.cellSizeX > self.cellSizeZ:
            self.spaceSizeX = self.cellSizeX - self.cellSizeZ
            self.cellSizeX = self.cellSizeZ

    def addGridCell(self, cellImage=None, imageScale=None):
        if len(self.cellList) > self.gridX * self.gridZ:
            import pdb
            pdb.set_trace()
        if not (cellImage or imageScale):
            gridCell = self.makeCell(self.cellImage)
        else:
            gridCell = self.makeCell(cellImage, imageScale)
        gridCell.setPos(self.findGridPos(self.xCount, self.gridZ - 1 - self.zCount))
        self.gridDict[self.xCount, self.zCount] = gridCell
        if self.xCount == self.gridX - 1:
            self.xCount = 0
            self.zCount += 1
        else:
            self.xCount += 1

    def findGridPos(self, x, z):
        posZ = (float(z) + 0.5) * self.cellSizeZ
        if x == 0:
            posX = (float(x) + 0.5) * self.cellSizeX
        else:
            posX = (float(x) + 0.5) * self.cellSizeX + self.spaceSizeX * float(x)
        return Point3(posX, 0, posZ)

    def putIntoGrid(self, item, gridX, gridZ):
        gridCell = self.gridDict.get((gridX, gridZ))
        self.putIntoCell(item, gridCell)