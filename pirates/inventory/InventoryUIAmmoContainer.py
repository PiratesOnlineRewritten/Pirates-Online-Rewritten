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
from pirates.economy import EconomyGlobals
from pirates.inventory import InventoryUIAmmoBagItem
orderedPouchTypes = [
 36, 33, 34, 35, 41]

class InventoryUIAmmoContainer(InventoryUIStackContainer.InventoryUIStackContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=4, countZ=4, minCountZ=4, maxCountX=5, itemList=None):
        if not config.GetBool('want-fishing-game', False):
            orderedPouchTypes.remove(41)
        InventoryUIStackContainer.InventoryUIStackContainer.__init__(self, manager, sizeX, sizeZ, minCountZ=minCountZ, maxCountX=maxCountX, itemList=itemList)
        self.initialiseoptions(InventoryUIAmmoContainer)
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
        gui = loader.loadModel('models/gui/gui_icons_weapon')
        self.titleImageOpen = gui.find('**/pir_t_ico_can_ammoBarrel')
        self.titleImageClosed = gui.find('**/pir_t_ico_can_ammoBarrel')
        self.titleName = PLocalizer.InventoryPageAmmo
        if not self.titleImageOpen.isEmpty():
            self.titleImageOpen.setScale(0.14)
        if not self.titleImageClosed.isEmpty():
            self.titleImageClosed.setScale(0.14)

    def findMaxPouchInUse(self, listOfPouches):
        listOfPouchesOwned = []
        pouchUsed = 0
        inv = localAvatar.getInventory()
        if inv:
            for pouchId in listOfPouches:
                if inv.getStackQuantity(pouchId):
                    pouchUsed = pouchId

        return pouchUsed

    def discoverPouches(self):
        for listOfSkills in self.listOfItemLists:
            pouchType = listOfSkills[0]
            possiblePouches = EconomyGlobals.getListOfPouches(pouchType)
            actualPouchId = self.findMaxPouchInUse(possiblePouches)
            self.subBagTypeToBagId[pouchType] = actualPouchId

    def figureOutStackTypes(self):
        self.listOfItemLists = []
        for pouchType in orderedPouchTypes:
            ammoList = EconomyGlobals.getPouchAmmoList(pouchType)
            itemList = [ WeaponGlobals.getSkillIdForAmmoSkillId(ammoId) for ammoId in ammoList ]
            itemList.insert(0, pouchType)
            self.listOfItemLists.append(itemList)

        self.discoverPouches()

    def isSkillValid(self, skillId):
        return WeaponGlobals.getSkillAmmoInventoryId(skillId) in InventoryGlobals.AmmoInGUI
        SkillIcons = loader.loadModel('models/textureCards/skillIcons')
        ammoId = WeaponGlobals.getSkillAmmoInventoryId(skillId)
        ammoName = PLocalizer.InventoryTypeNames.get(ammoId)
        ammoDescription = PLocalizer.WeaponDescriptions.get(ammoId)
        ammoIconName = WeaponGlobals.getSkillIcon(skillId)
        ammoIcon = SkillIcons.find('**/%s' % ammoIconName)
        skillRepId = WeaponGlobals.getSkillReputationCategoryId(skillId)
        if ammoName and ammoDescription and ammoIcon and skillRepId:
            return 1
        else:
            return 0

    def setupCells(self):
        self.gridBackground = self.attachNewNode('grid-background')
        WeaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        gui = loader.loadModel('models/gui/toplevel_gui')
        chestButtonClosed = gui.find('**/treasure_chest_closed_over')
        self.figureOutStackTypes()
        if len(self.listOfItemLists) == 0:
            return
        self.computeCellSize()
        for Z in range(self.gridZ):
            for X in range(len(self.listOfItemLists[Z])):
                skillId = self.listOfItemLists[Z][X]
                if self.subBagTypeToBagId.has_key(skillId) and skillId not in self.subBagTypesCreated:
                    if self.seperatorOn:
                        self.seperatorCount += 1
                    else:
                        self.seperatorOn = 1
                        self.gapOn = 1
                    bagId = self.subBagTypeToBagId[skillId]
                    cellPos = self.findGridPos(X, Z)
                    bagCell = self.makeCell(self.cellImage)
                    bagCell.setPos(cellPos)
                    bagItem = self.makeAmmoBagItem(skillId, bagId)
                    self.putIntoCell(bagItem, bagCell)
                    self.subBagTypesCreated.append(skillId)
                    bagCell['image'] = None
                elif skillId in self.subBagTypesCreated:
                    pass
                else:
                    cellPos = self.findGridPos(X, Z, self.gapOn)
                    ammoCell = self.getCell()
                    ammoCell.setPos(cellPos)
                    ammoId = WeaponGlobals.getSkillAmmoInventoryId(skillId)
                    newItem = self.getItem(skillId, ammoId)
                    if newItem:
                        if self.textOffset != None:
                            newItem.textOffset = self.textOffset
                        self.putIntoCell(newItem, ammoCell)
                        ammoCell['image_color'] = (1.0, 1.0, 1.0, 1.0)
                    else:
                        ammoCell['image_color'] = (0.5, 0.5, 0.5, 1.0)
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

    def makeAmmoBagItem(self, skillId, bagId):
        itemTuple = [
         0, bagId, 0, 0]
        return InventoryUIAmmoBagItem.InventoryUIAmmoBagItem(self.manager, skillId, itemTuple, imageScaleFactor=1.25)

    def getItem(self, skillId, ammoId):
        if ammoId:
            itemTuple = [
             0, ammoId, 0, localAvatar.getInventory().getStackQuantity(ammoId)]
            return self.manager.makeAmmoItem(skillId, itemTuple, update=True)
        else:
            return None
        return None

    def cellClicked(self, cell, mouseAction=None, task=None):
        pass

    def cellUsed(self, cell):
        pass