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

class InventoryUIRewardsContainer(InventoryUIContainer.InventoryUIContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=None, countZ=None):
        InventoryUIContainer.InventoryUIContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ)
        self.containerType = CONTAINER_REWARDS
        self.initialiseoptions(InventoryUIRewardsContainer)

    def setup(self):
        pass

    def destroy(self):
        self.ignoreAll()
        InventoryUIContainer.InventoryUIContainer.destroy(self)

    def canDrag(self):
        return 0

    def grabCellItem(self, cell):
        pass

    def cellClick(self, cell, mouseAction=MOUSE_CLICK, task=None):
        pass

    def addRewardIntoGrid(self, itemId, x, z):
        itemInfo = (
         ItemGlobals.getClass(itemId), itemId, 0, 0)
        item = self.manager.makeLocatableItem(itemInfo)
        self.putIntoGrid(item, x, z)