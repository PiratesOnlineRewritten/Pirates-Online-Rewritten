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

class InventoryUIJewelryContainer(InventoryUISlotContainer.InventoryUISlotContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=4, countZ=4, slotList=None):
        InventoryUISlotContainer.InventoryUISlotContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ, slotList)
        self.initialiseoptions(InventoryUIJewelryContainer)
        self.rightClickAction = {InventoryType.ItemTypeJewelry: (None, Locations.JEWLERY_TYPE_TO_RANGE, 1),InventoryType.ItemTypeTattoo: (None, Locations.TATTOO_TYPE_TO_RANGE, 1)}
        self.overflowInfo = DirectLabel(parent=self, relief=None, textMayChange=0, text=PLocalizer.OverflowHint, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=PiratesGuiGlobals.TextFG2, text_scale=0.04, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0,
                                                                                                                                                                                                                                                                                                           0))
        self.overflowInfo.setPos(0.1, 0, 1.06)
        self.overflowInfo.hide()
        self.accept('overflowChanged', self.handleOverflow)
        return

    def setupBackground(self):
        gui = loader.loadModel('models/gui/gui_main')
        scale = 0.335
        self.background = self.attachNewNode('background')
        self.background.setScale(scale)
        self.background.setPos(0.08, 0, 0.51)
        gui.find('**/gui_inv_jewelry').copyTo(self.background)
        self.background.flattenStrong()

    def setTitleInfo(self):
        gui = loader.loadModel('models/textureCards/shopIcons')
        self.titleImageOpen = gui.find('**/pir_t_gui_gen_trinket')
        self.titleImageClosed = gui.find('**/pir_t_gui_gen_trinket')
        self.titleName = PLocalizer.InventoryPageJewelry
        self.titleImageOpen.setScale(0.12)
        self.titleImageClosed.setScale(0.12)

    def handleOverflow(self, info=None):
        self.overflowInfo.hide()
        overflowItems = localAvatar.getInventory().getOverflowItems()
        for item in overflowItems:
            if item[0] in (InventoryType.ItemTypeJewelry, InventoryType.ItemTypeTattoo):
                self.overflowInfo.show()
                return