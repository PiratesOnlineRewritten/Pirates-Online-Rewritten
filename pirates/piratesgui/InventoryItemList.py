from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemGui
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import WeaponGlobals
from pirates.piratesgui.InventoryList import InventoryList
from pirates.piratesbase import PLocalizer

class InventoryItemList(InventoryList):

    def __init__(self, inventory, height, trade=0, buy=0, sell=0, use=0, weapon=0, listItemClass=InventoryItemGui.InventoryItemGui, listItemWidth=PiratesGuiGlobals.InventoryItemGuiWidth):
        InventoryList.__init__(self, inventory=inventory, height=height, trade=trade, buy=buy, sell=sell, use=use, weapon=weapon, listItemClass=listItemClass, listItemWidth=listItemWidth, listItemHeight=PiratesGuiGlobals.InventoryItemGuiHeight)
        self.initialiseoptions(InventoryItemList)
        self.all_panels = []

    def getPanel(self, data):
        for panel in self.all_panels:
            if panel.data == data:
                return panel

    def filterByItemGroup(self, itemGroup):
        if len(self.all_panels) == 0:
            self.all_panels = self.panels
        self.panels = []
        for panel in self.all_panels:
            if getItemGroup(panel.data[0]) == itemGroup:
                self.panels.append(panel)
                panel.show()
            else:
                panel.hide()

        self.repackPanels()

    def sortByTypeAndLevel(self):

        def sortData(a, b):
            aId = a.getData()[0]
            bId = b.getData()[0]
            aType = EconomyGlobals.getItemType(aId)
            bType = EconomyGlobals.getItemType(bId)
            if aType == bType:
                if aType <= ItemType.WAND or aType == ItemType.POTION:
                    aSubtype = ItemGlobals.getSubtype(aId)
                    bSubtype = ItemGlobals.getSubtype(bId)
                    if aSubtype == bSubtype:
                        if aType <= ItemType.WAND:
                            aLevel = ItemGlobals.getWeaponRequirement(aId)
                            bLevel = ItemGlobals.getWeaponRequirement(bId)
                            if aLevel == bLevel:
                                if a.price == b.price:
                                    if aId > bId:
                                        return 1
                                    else:
                                        return -1
                                elif a.price > b.price:
                                    return 1
                                else:
                                    return -1
                            elif aLevel > bLevel:
                                return 1
                            else:
                                return -1
                        else:
                            aLevel = ItemGlobals.getNotorietyRequirement(aId)
                            bLevel = ItemGlobals.getNotorietyRequirement(bId)
                            if aLevel == bLevel:
                                if a.price == b.price:
                                    if aId > bId:
                                        return 1
                                    else:
                                        return -1
                                elif a.price > b.price:
                                    return 1
                                else:
                                    return -1
                            elif aLevel > bLevel:
                                return 1
                            else:
                                return -1
                    elif aSubtype > bSubtype:
                        return 1
                    else:
                        return -1
                elif aId > bId:
                    return 1
                else:
                    return -1
            elif aType > bType:
                return 1
            else:
                return -1

        self.panels.sort(sortData)
        self.repackPanels()