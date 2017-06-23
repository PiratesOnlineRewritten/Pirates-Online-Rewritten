from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory import InventoryUIItem

class InventoryUINoTradeItem(InventoryUIItem.InventoryUIItem):

    def __init__(self, manager, itemTuple, imageScaleFactor=1.0, showMax=1):
        InventoryUIItem.InventoryUIItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor)
        self.initialiseoptions(InventoryUINoTradeItem)
        self['relief'] = None
        self.textScale = 0.9
        self.itemType = ITEM_NOTRADE
        return