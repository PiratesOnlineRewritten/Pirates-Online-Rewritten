from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory import ItemGlobals
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.uberdog import InventoryRequestBase

class InventoryUIItem(DirectFrame, InventoryRequestBase.InventoryRequestBase):
    notify = directNotify.newCategory('InventoryUIItem')

    def __init__(self, manager, itemTuple, imageScaleFactor=1.0):
        sizeX = 1.0
        sizeZ = 1.0
        textScale = 0.04
        optiondefs = (('relief', None, None), ('borderWidth', (0.01, 0.01), None), ('state', DGG.DISABLED, None), ('text', '', None), ('text_font', PiratesGlobals.getPirateBoldOutlineFont(), None), ('text_fg', (1, 1, 1, 1), None), ('text_shadow', PiratesGuiGlobals.TextShadow, None), ('textMayChange', 1, None), ('text_scale', textScale, None))
        self.defineoptions({}, optiondefs)
        DirectFrame.__init__(self, parent=NodePath())
        InventoryRequestBase.InventoryRequestBase.__init__(self)
        self.initialiseoptions(InventoryUIItem)
        self.itemTuple = itemTuple
        self.amount = 1
        self.canStack = 0
        self.cell = None
        self.hotlink = None
        self.manager = manager
        self.textScale = 1.0
        self.imageScale = 1.0 * imageScaleFactor
        self.textOffset = -0.5
        self.itemType = ITEM_NORMAL
        self.iconColor = (1, 1, 1, 1)
        self.showResaleValue = True
        return

    def destroy(self):
        self.ignoreAll()
        self.cell = None
        self.container = None
        self.itemTuple = None
        DirectFrame.destroy(self)
        return

    def showDetails(self, cell, detailsPos, detailsHeight, event=None):
        pass

    def hideDetails(self, event=None):
        pass

    def onPutInCell(self):
        pass

    def refreshImageColor(self):
        if self['image']:
            self['image_color'] = (self.iconColor[0], self.iconColor[1], self.iconColor[2], self.iconColor[3])

    def getCategory(self):
        return self.itemTuple[0]

    def getId(self):
        return self.itemTuple[1]

    def getLocation(self):
        return self.itemTuple[2]

    def getName(self):
        return ''

    def getPlunderName(self):
        return (
         self.getName(), PiratesGuiGlobals.TextFG2)