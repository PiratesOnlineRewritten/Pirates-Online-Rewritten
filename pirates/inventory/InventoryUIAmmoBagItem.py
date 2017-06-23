from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
from pirates.economy import EconomyGlobals
from pirates.inventory import InventoryUIItem

class InventoryUIAmmoBagItem(InventoryUIItem.InventoryUIItem):

    def __init__(self, manager, skillId, itemTuple, imageScaleFactor=1.0):
        InventoryUIItem.InventoryUIItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor)
        self.initialiseoptions(InventoryUIAmmoBagItem)
        weaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        fishingIcons = loader.loadModel('models/textureCards/fishing_icons')
        if self.itemTuple[1]:
            self['image'] = weaponIcons.find('**/%s' % EconomyGlobals.getItemIcons(self.itemTuple[1]))
        elif skillId == EconomyGlobals.ItemType.FISHING_POUCH:
            self['image'] = fishingIcons.find('**/%s' % EconomyGlobals.getItemTypeIcon(skillId))
        else:
            self['image'] = weaponIcons.find('**/%s' % EconomyGlobals.getItemTypeIcon(skillId))
        self.skillId = skillId