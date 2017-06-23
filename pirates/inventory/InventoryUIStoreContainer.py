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
from pirates.inventory import ItemGlobals
from pirates.economy import EconomyGlobals
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import *

class InventoryUIStoreContainer(InventoryUIContainer.InventoryUIContainer):
    notify = directNotify.newCategory('InventoryUIStoreContainer')
    detailsDelay = 0.0
    detailsPos = (0.398, 0.196)
    detailsHeight = 0.22

    def __init__(self, store, manager, sizeX=1.0, sizeZ=1.0, countX=None, countZ=None):
        InventoryUIContainer.InventoryUIContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ)
        self.initialiseoptions(InventoryUIStoreContainer)
        self.store = store
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
        self.clickedCell = None
        self.xCount = 0
        self.zCount = 0
        return

    def destroy(self):
        self.ignoreAll()
        self.clickedCell = None
        InventoryUIContainer.InventoryUIContainer.destroy(self)
        return

    def testWithIn(self):
        return 0

    def getItemPriceMult(self):
        return 1.0

    def enterCell(self, cell, pos=None):
        return
        if not self.store.canChangeSelection():
            return
        if cell.inventoryItem:
            self.notify.debug('enterCell: %s' % (cell.inventoryItem.itemTuple,))
            self.store.itemRollIn(cell.inventoryItem.itemTuple[1])
        InventoryUIContainer.InventoryUIContainer.enterCell(self, cell, pos)

    def exitCell(self, cell, pos=None):
        return
        if not self.store.canChangeSelection():
            return
        if cell.inventoryItem:
            self.notify.debug('exitCell: %s' % (cell.inventoryItem.itemTuple,))
            self.store.itemRollOut(cell.inventoryItem.itemTuple[1])
        InventoryUIContainer.InventoryUIContainer.exitCell(self, cell, pos)

    def cellClick(self, cell, mouseAction=MOUSE_CLICK, task=None):
        if not self.store.canChangeSelection():
            return
        if self.clickedCell:
            self.clickedCell['state'] = DGG.NORMAL
            self.clickedCell.clearColorScale()
        self.clickedCell = cell
        self.clickedCell['state'] = DGG.DISABLED
        self.clickedCell.setColorScale(0.5, 0.5, 0.5, 1)
        if cell.inventoryItem:
            self.notify.debug('cellClick: %s' % (cell.inventoryItem.itemTuple,))
            self.store.itemClicked(cell.inventoryItem.itemTuple[1])

    def showItemDetails(self, itemId):
        for cell in self.cellList:
            if cell.inventoryItem and cell.inventoryItem.itemTuple[1] == itemId:
                self.manager.startCellItemDetails(cell, self.detailsPos, self.detailsHeight, self.detailsDelay)
                return

    def getItem(self, itemId):
        for cell in self.cellList:
            if cell.inventoryItem and cell.inventoryItem.itemTuple[1] == itemId:
                return cell.inventoryItem

    def setupItems(self, itemList):
        for itemId in itemList:
            itemClass = ItemGlobals.getClass(itemId)
            itemType = EconomyGlobals.getItemType(itemId)
            itemTuple = [itemClass, itemId, 0, 0]
            item = None
            if itemClass == InventoryType.ItemTypeWeapon:
                item = self.manager.makeWeaponItem(itemTuple)
            else:
                if itemClass == InventoryType.ItemTypeCharm:
                    item = self.manager.makeCharmItem(itemTuple)
                elif itemClass == InventoryType.ItemTypeConsumable:
                    itemTuple[3] = 1
                    item = self.manager.makeConsumableItem(itemTuple, showMax=0)
                elif itemClass == InventoryType.ItemTypeClothing:
                    item = self.manager.makeClothingItem(itemTuple)
                else:
                    if itemClass == InventoryType.ItemTypeMoney:
                        item = self.manager.makeGoldItem(itemTuple)
                    elif itemClass == InventoryType.TreasureCollection:
                        item = self.manager.makeTreasureItem(itemTuple)
                    elif itemClass == InventoryType.ItemTypeJewelry:
                        item = self.manager.makeJewelryItem(itemTuple)
                    elif itemClass == InventoryType.ItemTypeTattoo:
                        item = self.manager.makeTattooItem(itemTuple)
                    elif itemClass == InventoryCategory.CARDS:
                        cardId = itemId
                        itemTuple[1] -= InventoryType.begin_Cards
                        item = self.manager.makeCardItem(cardId, itemTuple, imageScaleFactor=1.9)
                    elif itemClass == InventoryCategory.WEAPON_PISTOL_AMMO:
                        itemTuple[1] = WeaponGlobals.getSkillAmmoInventoryId(itemId)
                        item = self.manager.makeAmmoItem(itemId, itemTuple, showMax=0)
                    elif itemType in [EconomyGlobals.ItemType.DAGGERAMMO, EconomyGlobals.ItemType.PISTOLAMMO, EconomyGlobals.ItemType.GRENADEAMMO, EconomyGlobals.ItemType.CANNONAMMO]:
                        itemTuple = [0, itemId, 0, EconomyGlobals.getItemQuantity(itemId)]
                        skillId = WeaponGlobals.getSkillIdForAmmoSkillId(itemId)
                        item = self.manager.makeAmmoItem(skillId, itemTuple, showMax=0)
                    elif itemType in [EconomyGlobals.ItemType.PISTOL_POUCH, EconomyGlobals.ItemType.DAGGER_POUCH, EconomyGlobals.ItemType.GRENADE_POUCH, EconomyGlobals.ItemType.CANNON_POUCH, EconomyGlobals.ItemType.FISHING_POUCH]:
                        item = self.manager.makePouchItem(itemTuple)
                    elif itemType in (EconomyGlobals.ItemType.FISHING_LURE,):
                        itemTuple[1] = WeaponGlobals.getSkillAmmoInventoryId(itemId)
                        itemTuple[3] = EconomyGlobals.getItemQuantity(itemId)
                        item = self.manager.makeFishingItem(itemId, itemTuple, showMax=0)
                    if itemClass in (InventoryType.ItemTypeMoney, InventoryCategory.CARDS, InventoryType.TreasureCollection):
                        self.addGridCell(self.stackImage, 1.0)
                    if itemClass == InventoryCategory.WEAPON_PISTOL_AMMO:
                        self.addGridCell(self.stackImage2, 1.0)
                    if itemType in (EconomyGlobals.ItemType.FISHING_LURE,):
                        self.addGridCell(self.stackImage, 1.0)
                    self.addGridCell()
                if item:
                    self.tryPutIntoFirstOpenCell(item)
            item.showResaleValue = False
            if self.zCount == self.gridZ:
                break

        while self.zCount < self.gridZ:
            self.addGridCell()

        return

    def canSwap(self, myCell, otherCell):
        return 0

    def canReceive(self, myCell, fromSwap=0, itemInQuestion=None):
        return 0

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

    def disableUnusedCells(self):
        for cell in self.gridDict.values():
            if not cell.inventoryItem:
                cell['state'] = DGG.DISABLED