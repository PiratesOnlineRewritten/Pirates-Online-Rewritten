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

class StowawayListItem(DirectButton):
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
        if StowawayListItem.guiLoaded:
            return
        StowawayListItem.topGui = loader.loadModel('models/gui/toplevel_gui')
        StowawayListItem.coinImage = StowawayListItem.topGui.find('**/treasure_w_coin*')
        StowawayListItem.weaponIcons = loader.loadModel('models/gui/gui_icons_weapon')
        StowawayListItem.skillIcons = loader.loadModel('models/textureCards/skillIcons')
        StowawayListItem.guiLoaded = True

    def loadData(self):
        itemId = self.data[0]
        name = PLocalizer.LocationNames[itemId]
        self.price = EconomyGlobals.StowawayCost[itemId]
        self.name = PLocalizer.makeHeadingString(name, 2)
        self.minLvl = EconomyGlobals.getItemMinLevel(self.data[0])

    def destroy(self):
        del self.data
        del self.weapon
        DirectButton.destroy(self)

    def getData(self):
        return self.data

    def sendEvents(self):
        if self.buy:
            messenger.send(PiratesGuiGlobals.InventoryBuyEvent, [
             self.data, self.buy])

    def bringToFront(self):
        self.reparentTo(self.getParent())