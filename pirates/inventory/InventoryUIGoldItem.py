from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory.InventoryGlobals import *
from pirates.piratesbase import Freebooter
from pirates.ai import HolidayGlobals
from pirates.inventory import InventoryUIStackItem

class InventoryUIGoldItem(InventoryUIStackItem.InventoryUIStackItem):

    def __init__(self, manager, itemTuple, imageScaleFactor=1.0, update=False):
        InventoryUIStackItem.InventoryUIStackItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor, showMax=0, update=False)
        self.initialiseoptions(InventoryUIGoldItem)
        gui = loader.loadModel('models/gui/toplevel_gui')
        self['image'] = gui.find('**/treasure_w_coin*')
        self['image_scale'] = 0.1 * imageScaleFactor
        self.imageScale = 3.0
        self.textScale = 1.1
        if update:
            self.accept(getCategoryChangeMsg(localAvatar.getInventoryId(), InventoryType.ItemTypeMoney), self.updateAmount)

    def destroy(self):
        self.ignoreAll()
        InventoryUIStackItem.InventoryUIStackItem.destroy(self)

    def getName(self):
        return PLocalizer.GoldName

    def onPutInCell(self):
        self.updateAmountText()

    def updateAmount(self, caller=None):
        inventory = localAvatar.getInventory()
        if inventory:
            amount = inventory.getGoldInPocket()
            self.amount = amount
            self.updateAmountText()

    def updateAmountText(self):
        if self.cell and self.cell.container and self.cell.container.containerType == CONTAINER_PLUNDER and base.cr.newsManager and (base.cr.newsManager.getHoliday(HolidayGlobals.DOUBLEGOLDHOLIDAYPAID) and Freebooter.getPaidStatus(base.localAvatar.getDoId()) or base.cr.newsManager.getHoliday(HolidayGlobals.DOUBLEGOLDHOLIDAY)):
            self['text'] = str(self.amount / 2) + '+' + str(self.amount / 2)
        else:
            InventoryUIStackItem.InventoryUIStackItem.updateAmountText(self)