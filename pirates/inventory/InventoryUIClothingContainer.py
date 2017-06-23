from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory.InventoryUIGlobals import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory.InventoryGlobals import Locations
from pirates.inventory import ItemGlobals
from pirates.inventory import InventoryUISlotContainer

class InventoryUIClothingContainer(InventoryUISlotContainer.InventoryUISlotContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=4, countZ=4, slotList=None):
        InventoryUISlotContainer.InventoryUISlotContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ, slotList)
        self.initialiseoptions(InventoryUIClothingContainer)
        self.rightClickAction = {InventoryType.ItemTypeClothing: (None, Locations.CLOTHING_TYPE_TO_RANGE, 1)}
        self.overflowInfo = DirectLabel(parent=self, relief=None, textMayChange=0, text=PLocalizer.OverflowHint, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=PiratesGuiGlobals.TextFG2, text_scale=0.04, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0,
                                                                                                                                                                                                                                                                                                           0))
        self.overflowInfo.setPos(0.25, 0, 1.07)
        self.overflowInfo.hide()
        base.clothPage = self
        self.accept('overflowChanged', self.handleOverflow)
        return

    def setupBackground(self):
        gui = loader.loadModel('models/gui/gui_main')
        scale = 0.335
        self.background = self.attachNewNode('background')
        self.background.setScale(scale)
        self.background.setPos(0.23, 0, 0.52)
        gui.find('**/gui_inv_clothing').copyTo(self.background)
        PiratesGlobals.flattenOrdered(self.background)

    def setTitleInfo(self):
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.titleImageOpen = gui.find('**/topgui_icon_clothing')
        self.titleImageClosed = gui.find('**/topgui_icon_clothing')
        self.titleName = PLocalizer.InventoryPageClothing
        self.titleImageOpen.setScale(0.22)
        self.titleImageClosed.setScale(0.22)

    def handleOverflow(self, info=None):
        self.overflowInfo.hide()
        overflowItems = localAvatar.getInventory().getOverflowItems()
        for item in overflowItems:
            if item[0] in (InventoryType.ItemTypeClothing,):
                self.overflowInfo.show()
                return

    def postUpdate(self, cell):
        if cell in self.cellList:
            self.checkReqsForCell(cell)
        avInv = localAvatar.getInventory()
        if avInv and avInv.findAvailableLocation(InventoryType.ItemTypeClothing) in [Locations.INVALID_LOCATION, Locations.NON_LOCATION]:
            localAvatar.sendRequestContext(InventoryType.InventoryFull)