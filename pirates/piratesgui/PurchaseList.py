from pirates.piratesgui.InventoryList import InventoryList
from pirates.piratesgui.PurchaseListItem import PurchaseListItem
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemGui

class PurchaseList(InventoryList):

    def __init__(self, inventory, height, trade=0, buy=0, sell=0, use=0, weapon=0):
        InventoryList.__init__(self, inventory=inventory, height=height, trade=trade, buy=buy, sell=sell, use=use, weapon=weapon, listItemClass=PurchaseListItem, listItemWidth=PiratesGuiGlobals.PurchaseListItemWidth, listItemHeight=PiratesGuiGlobals.PurchaseListItemHeight)
        self.initialiseoptions(PurchaseList)
        self.loadInventoryPanels()

    def addPanel(self, data, repack=1):
        for panel in self.panels:
            if panel.data == data:
                panel.addItem()
                return

        InventoryList.addPanel(self, data, repack)
        self.sortPanels()

    def removePanel(self, data, repack=1):
        for panel in self.panels:
            if panel.data == data:
                if panel.itemCount > 1:
                    panel.removeItem()
                    self.inventory.remove(panel.data)
                else:
                    InventoryList.removePanel(self, data, repack)
                return

    def getItemQuantity(self, itemId):
        for panel in self.panels:
            if panel.data[0] == itemId:
                return panel.itemCount * panel.itemQuantity

        return 0