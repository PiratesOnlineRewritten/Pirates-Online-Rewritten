from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.inventory.InventoryUIGlobals import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory.InventoryGlobals import Locations
from pirates.battle import WeaponGlobals
from pirates.inventory import ItemGlobals
from pirates.inventory import InventoryUISlotContainer

class InventoryUIConsumableContainerLocatable(InventoryUISlotContainer.InventoryUISlotContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=4, countZ=4, slotList=None):
        InventoryUISlotContainer.InventoryUISlotContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ, slotList)
        self.initialiseoptions(InventoryUIConsumableContainerLocatable)
        self.invReq = None
        self.overflowInfo = DirectLabel(parent=self, relief=None, textMayChange=0, text=PLocalizer.OverflowHint, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=PiratesGuiGlobals.TextFG2, text_scale=0.04, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0,
                                                                                                                                                                                                                                                                                                           0))
        self.overflowInfo.setPos(0.42, 0, 1.06)
        self.overflowInfo.hide()
        self.accept('overflowChanged', self.handleOverflow)
        return

    def destroy(self):
        if self.invReq:
            DistributedInventoryBase.cancelGetInventory(self.invReq)
            self.invReq = None
        InventoryUISlotContainer.InventoryUISlotContainer.destroy(self)
        return

    def setupBackground(self):
        gui = loader.loadModel('models/gui/gui_main')
        scale = 0.335
        self.background = self.attachNewNode('background')
        self.background.setScale(scale)
        self.background.setPos(0.42, 0, 0.52)
        gui.find('**/gui_inv_red_general1').copyTo(self.background)
        PiratesGlobals.flattenOrdered(self.background)

    def setTitleInfo(self):
        gui = loader.loadModel('models/textureCards/skillIcons')
        chestButtonOpen = gui.find('**/pir_t_ico_pot_elixir')
        chestButtonClosed = gui.find('**/pir_t_ico_pot_elixir')
        self.titleImageOpen = chestButtonOpen
        self.titleImageClosed = chestButtonClosed
        self.titleName = PLocalizer.InventoryPagePotions
        self.titleImageOpen.setScale(0.12)
        self.titleImageClosed.setScale(0.12)

    def postUpdate(self, cell):
        if cell and cell.slotId:

            def invArrived(inventory):
                itemData = inventory.getLocatable(cell.slotId)
                if itemData:
                    cell.inventoryItem.amount = itemData.getCount()
                    cell.inventoryItem.updateAmountText()
                self.invReq = None
                return

            if self.invReq:
                DistributedInventoryBase.cancelGetInventory(self.invReq)
            self.invReq = DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), invArrived)
            self.checkReqsForCell(cell)
        avInv = localAvatar.getInventory()
        if avInv and avInv.findAvailableLocation(InventoryType.ItemTypeConsumable) in [Locations.INVALID_LOCATION, Locations.NON_LOCATION]:
            localAvatar.sendRequestContext(InventoryType.InventoryFull)

    def cellRightClick(self, cell, mouseAction=MOUSE_CLICK, task=None):
        if mouseAction == MOUSE_PRESS and cell.inventoryItem:
            if self.manager.localDrinkingPotion:
                localAvatar.guiMgr.createWarning(PLocalizer.NoDoubleDrinkingItemsWarning, PiratesGuiGlobals.TextFG6)
                return
            if self.manager.testCanUse(cell.inventoryItem.itemTuple):
                itemId = cell.inventoryItem.itemTuple.getType()
                skillId = WeaponGlobals.getSkillIdForAmmoSkillId(itemId)
                if WeaponGlobals.getSkillEffectFlag(skillId):
                    cell.inventoryItem.hasDrunk = localAvatar.guiMgr.combatTray.trySkill(InventoryType.UsePotion, skillId, 0)
                else:
                    cell.inventoryItem.hasDrunk = localAvatar.guiMgr.combatTray.trySkill(InventoryType.UseItem, skillId, 0)

    def handleOverflow(self, info=None):
        self.overflowInfo.hide()
        overflowItems = localAvatar.getInventory().getOverflowItems()
        for item in overflowItems:
            if item[0] in (InventoryType.ItemTypeConsumable,):
                self.overflowInfo.show()
                return