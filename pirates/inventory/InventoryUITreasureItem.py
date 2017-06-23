from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
from pirates.piratesbase import CollectionMap
from pirates.inventory import InventoryUINoTradeItem

class InventoryUITreasureItem(InventoryUINoTradeItem.InventoryUINoTradeItem):

    def __init__(self, manager, itemTuple, imageScaleFactor=1.0, showMax=1):
        InventoryUINoTradeItem.InventoryUINoTradeItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor, showMax=showMax)
        self.initialiseoptions(InventoryUITreasureItem)
        treasureGui = loader.loadModel('models/gui/treasure_gui')
        self['image'] = treasureGui.find('**/%s' % CollectionMap.Assets.get(itemTuple[1]))
        self['image_scale'] = 0.1 * imageScaleFactor
        self.imageScale = 3.0
        self.textScale = 1.1

    def destroy(self):
        InventoryUINoTradeItem.InventoryUINoTradeItem.destroy(self)

    def getName(self):
        return PLocalizer.Collections.get(self.itemTuple[1])