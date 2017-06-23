from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import CannonGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.uberdog import UberDogGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.reputation import ReputationGlobals
from pirates.inventory import ItemGlobals

class InventoryListItem(DirectButton):
    width = 0
    height = 0
    guiLoaded = False
    topGui = None
    genericButton = None
    coinImage = None
    weaponIcons = None
    skillIcons = None

    def __init__(self, data, trade=0, buy=0, sell=0, use=0, weapon=0, isDisabled=0, width=0, height=0):
        self.width = width
        self.height = height
        self.data = data
        self.trade = trade
        self.buy = buy
        self.sell = sell
        self.use = use
        self.weapon = weapon
        self.isDisabled = isDisabled
        DirectButton.__init__(self)
        self.loadGui()
        self.loadData()

    def destroyGui(self):
        pass

    def loadGui(self):
        if InventoryListItem.guiLoaded:
            return
        InventoryListItem.topGui = loader.loadModel('models/gui/toplevel_gui')
        InventoryListItem.coinImage = InventoryListItem.topGui.find('**/treasure_w_coin*')
        InventoryListItem.weaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        InventoryListItem.skillIcons = loader.loadModel('models/textureCards/skillIcons')
        InventoryListItem.fishingIcons = loader.loadModel('models/textureCards/fishing_icons')
        InventoryListItem.guiLoaded = True

    def loadData(self):
        itemId = self.data[0]
        item, quantity = self.data
        self.quantity = quantity
        itemType = EconomyGlobals.getItemType(itemId)
        if itemType <= ItemType.WAND:
            itemTypeName = PLocalizer.getItemSubtypeName(ItemGlobals.getSubtype(itemId))
        else:
            itemTypeName = PLocalizer.InventoryItemClassNames.get(itemType)
        if itemType <= ItemType.WAND or itemType == ItemType.POTION:
            name = PLocalizer.getItemName(itemId)
            self.price = ItemGlobals.getGoldCost(itemId)
        else:
            name = PLocalizer.InventoryTypeNames.get(item)
            self.price = EconomyGlobals.getItemCost(item)
        if self.sell:
            self.price /= 2
        if self.buy:
            if itemType > ItemType.WAND and itemType != ItemType.POTION:
                self.quantity = EconomyGlobals.getItemQuantity(itemId)
            self.price *= self.quantity
            self.price = int(self.price)
        self.name = PLocalizer.makeHeadingString(name, 2)
        self.itemType = itemTypeName
        if itemType != ItemType.FISHING_LURE:
            if itemType != ItemType.POTION:
                self.minLvl = ItemGlobals.getWeaponRequirement(itemId)
            else:
                self.minLvl = 0
        else:
            self.minLvl = EconomyGlobals.getItemMinLevel(self.data[0])

    def destroy(self):
        del self.data
        del self.weapon
        DirectButton.destroy(self)

    def getData(self):
        return self.data

    def sendEvents(self):
        if self.trade:
            messenger.send(PiratesGuiGlobals.InventoryTradeEvent, [
             self.data, self.trade])
        if self.buy:
            messenger.send(PiratesGuiGlobals.InventoryBuyEvent, [
             self.data, self.buy])
        if self.sell:
            messenger.send(PiratesGuiGlobals.InventorySellEvent, [
             self.data, self.sell])
        if self.use:
            messenger.send(PiratesGuiGlobals.InventoryUseEvent, [
             self.data])

    def bringToFront(self):
        self.reparentTo(self.getParent())

    def equipWeapon(self, event):
        if base.localAvatar.guiMgr.weaponPage.equipStatus > 0:
            base.localAvatar.guiMgr.weaponPage.equipWeapon(self.data[0])