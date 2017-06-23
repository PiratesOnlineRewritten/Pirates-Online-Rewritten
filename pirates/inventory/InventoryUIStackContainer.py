from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIContainer
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.inventory.InventoryUIGlobals import *

class InventoryUIStackContainer(InventoryUIContainer.InventoryUIContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, minCountZ=4, maxCountX=5, itemList=None):
        InventoryUIContainer.InventoryUIContainer.__init__(self, manager, sizeX, sizeZ)
        self.initialiseoptions(InventoryUIStackContainer)
        self.minCountZ = minCountZ
        self.maxCountX = maxCountX
        self.itemList = itemList
        self.subBagTypeToBagId = {}
        self.subBagTypesCreated = []
        self.seperatorCount = 0
        self.seperatorOn = 0
        self.seperatorHeight = 0.5
        self.isReady = 0
        self.textScale = 0.06
        self.titleText = ''
        self.textOffset = None
        self.bagStackGap = 0.01
        self.gapOn = 0
        return

    def takeOut(self):
        InventoryUIContainer.InventoryUIContainer.takeOut(self)
        if not self.isReady:
            self.doSetup()
            self.isReady = 1

    def isSkillValid(self, skillId):
        ammoId = WeaponGlobals.getSkillAmmoInventoryId(skillId)
        ammoName = PLocalizer.InventoryTypeNames.get(ammoId)
        ammoDescription = PLocalizer.WeaponDescriptions.get(ammoId)
        ammoIconName = WeaponGlobals.getSkillIcon(skillId)
        ammoIcon = self.SkillIcons.find('**/%s' % ammoIconName)
        skillRepId = WeaponGlobals.getSkillReputationCategoryId(skillId)
        stackLimit = localAvatar.getInventory().getStackLimit(ammoId)
        if ammoName and ammoDescription and ammoIcon and stackLimit:
            return 1
        else:
            return 0

    def figureOutStackTypes(self):
        repCategoryDict = {}
        for itemId in self.itemList:
            skillRepId = WeaponGlobals.getSkillReputationCategoryId(itemId)
            if self.isSkillValid(itemId):
                if not repCategoryDict.has_key(skillRepId):
                    repCategoryDict[skillRepId] = []
                repCategoryDict[skillRepId].append(itemId)

        self.listOfItemLists = []
        for key in repCategoryDict:
            itemList = repCategoryDict[key]
            while len(itemList) > self.maxCountX:
                frontList = itemList[:self.maxCountX]
                backList = itemList[self.maxCountX:]
                self.listOfItemLists.append(frontList)
                itemList = backList

            self.listOfItemLists.append(itemList)

    def computeCellSize(self):
        self.gridZ = len(self.listOfItemLists)
        listLengths = []
        for skillList in self.listOfItemLists:
            listLengths.append(len(skillList))

        self.gridX = max(listLengths)
        self.cellSizeX = self.sizeX / max(1.0, float(self.gridX))
        self.cellSizeZ = self.sizeZ / float(max(self.gridZ, self.minCountZ))
        minSize = min(self.cellSizeX, self.cellSizeZ)
        self.cellSizeX = minSize
        self.cellSizeZ = minSize

    def setupCellImage(self):
        self.cellImage = NodePath('empty')
        self.workingCellImage = NodePath('empty')
        self.focusCellImage = NodePath('empty')
        gui = loader.loadModel('models/gui/gui_icons_weapon')
        self.gridBacking = NodePath('backing')
        baseBacking = gui.find('**/pir_t_gui_frm_inventoryBox')
        extraCell = gui.find('**/pir_t_gui_frm_inventoryBox_over')
        extraCell.setScale(0.7)
        baseBacking.reparentTo(self.gridBacking)
        extraCell.reparentTo(self.gridBacking)
        PiratesGlobals.flattenOrdered(self.gridBacking)
        self.imageScale = 1.0
        self.imagePos = (0.0, 0.0, 0.0)
        self.relief = DGG.FLAT

    def setupCells(self):
        self.gridBackground = self.attachNewNode('grid-background')
        self.figureOutStackTypes()
        if len(self.listOfItemLists) == 0:
            return
        self.computeCellSize()
        for Z in range(self.gridZ):
            for X in range(len(self.listOfItemLists[Z])):
                itemId = self.listOfItemLists[Z][X]
                cellPos = self.findGridPos(X, Z, self.gapOn)
                newCell = self.getCell()
                newCell.setPos(cellPos)
                newItem = self.getItem(itemId)
                if newItem:
                    if self.textOffset != None:
                        newItem.textOffset = self.textOffset
                    self.putIntoCell(newItem, newCell)
                self.makeGridBacking(cellPos)

        self.gridBackground.flattenStrong()
        return

    def doSetup(self):
        self.setupCells()
        self.titleLabel = DirectLabel(relief=None, parent=self, textMayChange=1, text=self.titleText, text_fg=(1,
                                                                                                               1,
                                                                                                               1,
                                                                                                               1), text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_scale=self.textScale, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.0,
                                                                                                                                                                                                                                                                                    0.0))
        self.titleLabel.setPos(self.sizeX * 0.5, 0.0, self.sizeZ + self.textScale * 0.5)
        return

    def getCell(self):
        ammoCell = self.makeCell(NodePath('stack'), 1.0)
        return ammoCell

    def getItem(self, itemId):
        itemTuple = [
         0, itemId, 0, 0]
        return self.manager.makeLocatableItem(itemTuple)

    def getTotalHeight(self):
        return self.sizeZ + self.textScale * 1.5

    def findGridPos(self, x, z, wantGap=0):
        zPos = self.sizeZ - (float(z) + 0.5) * self.cellSizeZ
        if self.seperatorOn:
            zPos -= float(self.seperatorCount) * self.seperatorHeight * self.cellSizeZ
        xPos = (float(x) + 0.5) * self.cellSizeX
        if wantGap:
            xPos += self.bagStackGap
        return Point3(xPos, 0.0, zPos)

    def cellClicked(self, cell, mouseAction=MOUSE_CLICK, task=None):
        print 'Stack Cell Clicked'
        if self.manager.heldItem:
            worked = 0
            if self.manager.heldItem.itemType == ITEM_STACK:
                if cell.inventoryItem:
                    if cell.inventoryItem.itemType == ITEM_STACK and self.manager.heldItem.ammoId == cell.inventoryItem.ammoId:
                        print 'Combine stack into cell'
                        worked = 1
                self.manager.itemPickup = worked or PICKUP_CLICK
        elif mouseAction == MOUSE_CLICK and cell.inventoryItem.itemType == ITEM_STACK:
            self.manager.selectStack(cell)

    def cellUsed(self, cell):
        if cell.inventoryItem.itemType == ITEM_STACK:
            self.manager.selectStack(cell)