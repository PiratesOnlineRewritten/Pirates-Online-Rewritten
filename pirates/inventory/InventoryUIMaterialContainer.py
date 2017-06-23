from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIStackContainer, InventoryGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import WeaponGlobals
from pirates.economy.EconomyGlobals import ItemId
from pirates.inventory import InventoryUIMaterialBagItem
orderedPouchTypes = [
 36, 33, 34, 35, 41]

class InventoryUIMaterialContainer(InventoryUIStackContainer.InventoryUIStackContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=4, countZ=4, minCountZ=4, maxCountX=5, itemList=None):
        InventoryUIStackContainer.InventoryUIStackContainer.__init__(self, manager, sizeX, sizeZ, minCountZ=minCountZ, maxCountX=maxCountX, itemList=itemList)
        self.initialiseoptions(InventoryUIMaterialContainer)
        self.textOffset = None
        gui = loader.loadModel('models/gui/gui_main')
        scale = 0.335
        self.background = self.attachNewNode('background')
        self.background.setScale(scale)
        self.background.setPos(0.5, 0, 0.47)
        gui.find('**/gui_inv_ammo').copyTo(self.background)
        self.background.flattenStrong()
        return

    def setTitleInfo(self):
        MaterialIcons = loader.loadModel('models/textureCards/shipMaterialIcons')
        self.titleImageOpen = MaterialIcons.find('**/pir_t_gui_sc_container')
        self.titleImageClosed = MaterialIcons.find('**/pir_t_gui_sc_container')
        self.titleName = PLocalizer.InventoryPageMaterial
        if not self.titleImageOpen.isEmpty():
            self.titleImageOpen.setScale(0.12)
        if not self.titleImageClosed.isEmpty():
            self.titleImageClosed.setScale(0.12)

    def figureOutStackTypes(self):
        self.listOfItemLists = [
         [
          ItemId.MATERIAL_BASIC, InventoryType.PineInPocket, InventoryType.OakInPocket, InventoryType.IronInPocket, InventoryType.SteelInPocket, InventoryType.CanvasInPocket, InventoryType.SilkInPocket], [ItemId.MATERIAL_UNCOMMON, InventoryType.GrogInPocket]]

    def setupCells(self):
        self.gridBackground = self.attachNewNode('grid-background')
        WeaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        gui = loader.loadModel('models/gui/toplevel_gui')
        chestButtonClosed = gui.find('**/treasure_chest_closed_over')
        self.figureOutStackTypes()
        self.computeCellSize()
        for Z in range(len(self.listOfItemLists)):
            print 'setting up material type %s' % Z
            if self.seperatorOn:
                self.seperatorCount += 1
            else:
                self.seperatorOn = 1
                self.gapOn = 1
            cellPos = self.findGridPos(0, Z)
            bagCell = self.makeCell(self.cellImage)
            bagCell.setPos(cellPos)
            bagItem = self.makeMaterialBagItem(Z)
            self.putIntoCell(bagItem, bagCell)
            bagCell['image'] = None
            for X in range(1, len(self.listOfItemLists[Z])):
                materialId = self.listOfItemLists[Z][X]
                print 'setting up material id %s' % materialId
                cellPos = self.findGridPos(X, Z, self.gapOn)
                materialCell = self.getCell()
                materialCell.setPos(cellPos)
                newItem = self.getItem(materialId)
                if self.textOffset != None:
                    newItem.textOffset = self.textOffset
                self.putIntoCell(newItem, materialCell)
                materialCell['image_color'] = (1.0, 1.0, 1.0, 1.0)
                self.makeCellBacking(cellPos)

        for i in self.cellList:
            n = NodePath(i.node().getStateDef(0)).getChild(0)
            if i.getNumChildren() > 1:
                n2 = NodePath(i.getChild(1).node().getStateDef(0)).getChild(0)
                newGeomC = n2.copyTo(self.gridBackground)
                newGeomC.setPos(i.getPos())
                n2.hide()
            NodePath(i.node().getStateDef(2)).hide()
            n.hide()

        self.gridBackground.flattenStrong()
        return

    def findGridPos(self, x, z, wantGap=0):
        zPos = self.sizeZ - (float(z) + 0.5) * self.cellSizeZ * 0.91 + 0.153
        if self.seperatorOn:
            zPos -= float(self.seperatorCount) * self.seperatorHeight * self.cellSizeZ
        xPos = (float(x) + 0.5) * self.cellSizeX
        if wantGap:
            xPos += self.bagStackGap
        return Point3(xPos, 0.0, zPos)

    def makeMaterialBagItem(self, materialType):
        itemTuple = [
         0, materialType, 0, 0]
        return InventoryUIMaterialBagItem.InventoryUIMaterialBagItem(self.manager, materialType, itemTuple, imageScaleFactor=1.25)

    def getItem(self, materialId):
        if materialId:
            itemTuple = [
             0, materialId, 0, localAvatar.getInventory().getStackQuantity(materialId)]
            return self.manager.makeMaterialItem(materialId, itemTuple, update=True, showMax=False)
        else:
            return None
        return None

    def cellClicked(self, cell, mouseAction=None, task=None):
        pass

    def cellUsed(self, cell):
        pass