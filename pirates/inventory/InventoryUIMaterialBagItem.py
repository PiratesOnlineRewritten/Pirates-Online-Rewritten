from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
from pirates.economy import EconomyGlobals
from pirates.inventory import InventoryUIItem

class InventoryUIMaterialBagItem(InventoryUIItem.InventoryUIItem):

    def __init__(self, manager, materialType, itemTuple, imageScaleFactor=1.0):
        InventoryUIItem.InventoryUIItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor)
        self.initialiseoptions(InventoryUIMaterialBagItem)
        materialIcons = loader.loadModel('models/gui/gui_icons_weapon')
        self['image'] = materialIcons.find('**/%s' % EconomyGlobals.getItemIcons(materialType))
        self.materialType = materialType