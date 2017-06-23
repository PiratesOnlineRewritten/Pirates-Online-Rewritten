from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory import ItemGlobals
from pirates.inventory import InventoryUIItem
from pirates.inventory import InventoryGlobals

class InventoryUIStackItem(InventoryUIItem.InventoryUIItem):

    def __init__(self, manager, itemTuple, imageScaleFactor=1.0, showMax=1, update=True):
        InventoryUIItem.InventoryUIItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor)
        self.initialiseoptions(InventoryUIStackItem)
        self['relief'] = None
        self.textScale = 0.9
        self.showMax = showMax
        self.itemType = ITEM_STACK
        self.amount = None
        self.canStack = 1
        self.localStore = 0
        if not itemTuple[2] and update:
            self.localStore = 1
            self.updateAmount()
            self.accept('inventoryQuantity-%s-%s' % (localAvatar.getInventoryId(), itemTuple[1]), self.updateAmount)
            self.accept('inventoryLimit-%s-%s' % (localAvatar.getInventoryId(), itemTuple[1]), self.updateAmount)
        else:
            self.amount = itemTuple[3]
            self.updateAmountText()
        return

    def updateAmount(self, caller=None):
        if not self.localStore:
            import pdb
            pdb.set_trace()
        amount = localAvatar.getInventory().getStackQuantity(self.getId())
        self.amount = amount
        self.updateAmountText()

    def updateAmountText(self):
        inv = localAvatar.getInventory()
        if not inv:
            return
        limit = ItemGlobals.getStackLimit(self.getId())
        if not limit:
            limit = inv.getStackLimit(self.getId())
        if self.showMax:
            self['text'] = '%s/%s' % (self.amount, limit)
        else:
            self['text'] = '%s' % self.amount

    def getAmount(self):
        return localAvatar.getInventory().getStackQuantity(self.getId())

    def getLimit(self):
        return localAvatar.getInventory().getStackLimit(self.getId())