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

class InventoryUIWeaponContainer(InventoryUISlotContainer.InventoryUISlotContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=4, countZ=4, slotList=None):
        InventoryUISlotContainer.InventoryUISlotContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ, slotList)
        self.initialiseoptions(InventoryUIWeaponContainer)
        self.rightClickAction = {InventoryType.ItemTypeWeapon: (Locations.RANGE_EQUIP_WEAPONS, None, 0),InventoryType.ItemTypeCharm: (Locations.RANGE_EQUIP_ITEMS, None, 1)}
        return

    def setupBackground(self):
        gui = loader.loadModel('models/gui/gui_main')
        scale = 0.335
        self.background = self.attachNewNode('background')
        self.background.setScale(scale)
        self.background.setPos(0.42, 0, 0.52)
        gui.find('**/gui_inv_weapon').copyTo(self.background)
        self.background.flattenStrong()

    def setTitleInfo(self):
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.titleImageOpen = gui.find('**/topgui_icon_weapons')
        self.titleImageClosed = gui.find('**/topgui_icon_weapons')
        self.titleName = PLocalizer.InventoryPageWeapons
        self.titleImageOpen.setScale(0.22)
        self.titleImageClosed.setScale(0.22)

    def postUpdate(self, cell):
        InventoryUISlotContainer.InventoryUISlotContainer.postUpdate(self, cell)
        avInv = localAvatar.getInventory()
        if avInv and avInv.findAvailableLocation(InventoryType.ItemTypeWeapon) in [Locations.INVALID_LOCATION, Locations.NON_LOCATION]:
            localAvatar.sendRequestContext(InventoryType.InventoryFull)
        messenger.send('checkForWeapons')