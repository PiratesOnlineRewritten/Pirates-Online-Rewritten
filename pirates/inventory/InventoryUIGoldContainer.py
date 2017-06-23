from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIStackContainer
from pirates.inventory.InventoryUIGlobals import *
from pirates.uberdog.UberDogGlobals import InventoryType

class InventoryUIGoldContainer(InventoryUIStackContainer.InventoryUIStackContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0):
        InventoryUIStackContainer.InventoryUIStackContainer.__init__(self, manager, sizeX, sizeZ, minCountZ=1, itemList=[InventoryType.ItemTypeMoney])
        self.containerType = CONTAINER_GOLD
        self.initialiseoptions(InventoryUIGoldContainer)
        self.accept('openingContainer', self.checkSetup)

    def checkSetup(self, caller=None):
        if not self.isReady:
            self.doSetup()
            self.isReady = 1

    def getCell(self):
        SkillIcons = loader.loadModel('models/textureCards/skillIcons')
        cellImageGold = (SkillIcons.find('**/base'), SkillIcons.find('**/base_down'), SkillIcons.find('**/base_over'))
        goldCell = self.makeCell(cellImageGold, 1.0)
        return goldCell

    def canDrag(self):
        return 0

    def setupCells(self):
        self.figureOutStackTypes()
        self.computeCellSize()
        for Z in range(self.gridZ):
            for X in range(len(self.listOfItemLists[Z])):
                itemId = self.listOfItemLists[Z][X]
                ammoCell = self.getCell()
                ammoCell.setPos(self.findGridPos(X, Z))
                newItem = self.getItem(itemId)
                self.putIntoCell(newItem, ammoCell)

    def isSkillValid(self, skillId):
        return 1

    def getItem(self, itemId):
        itemTuple = [
         0, itemId, 0, localAvatar.getMoney()]
        return self.manager.makeGoldItem(itemTuple, update=True)