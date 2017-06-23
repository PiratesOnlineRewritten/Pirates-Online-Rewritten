from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryListItem
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import WeaponGlobals

class InventoryList(DirectScrolledFrame):

    def __init__(self, inventory, height, trade=0, buy=0, sell=0, use=0, weapon=0, listItemClass=InventoryListItem.InventoryListItem, listItemWidth=0, listItemHeight=0):
        self.ListItem = listItemClass
        self.listItemWidth = listItemWidth
        self.listItemHeight = listItemHeight
        self.width = self.listItemWidth + PiratesGuiGlobals.ScrollbarSize
        self.height = height
        charGui = loader.loadModel('models/gui/char_gui')
        DirectScrolledFrame.__init__(self, relief=None, state=DGG.NORMAL, manageScrollBars=0, autoHideScrollBars=1, frameSize=(0, self.width, 0, self.height), canvasSize=(0, self.width - 0.05, 0.025, self.height - 0.025), verticalScroll_relief=None, verticalScroll_image=charGui.find('**/chargui_slider_small'), verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, 0, self.height), verticalScroll_image_scale=(self.height + 0.05, 1, 0.75), verticalScroll_image_hpr=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           90), verticalScroll_image_pos=(self.width - PiratesGuiGlobals.ScrollbarSize * 0.5 - 0.004, 0, self.height * 0.5), verticalScroll_image_color=(0.61,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         0.6,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         1), verticalScroll_thumb_image=(charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), verticalScroll_thumb_relief=None, verticalScroll_thumb_image_scale=0.25, verticalScroll_resizeThumb=0, horizontalScroll_relief=None, sortOrder=5)
        self.initialiseoptions(InventoryList)
        self.verticalScroll.incButton.destroy()
        self.verticalScroll.decButton.destroy()
        self.horizontalScroll.incButton.destroy()
        self.horizontalScroll.decButton.destroy()
        self.horizontalScroll.hide()
        self.accept('press-wheel_up-%s' % self.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % self.guiId, self.mouseWheelDown)
        self.trade = trade
        self.buy = buy
        self.sell = sell
        self.use = use
        self.weapon = weapon
        self.inventory = inventory
        self.panels = []
        self.loadInventoryPanels()
        charGui.removeNode()
        return

    def mouseWheelUp(self, task=None):
        if self.verticalScroll.isHidden():
            return
        amountScroll = 0.075
        if self.verticalScroll['value'] > 0:
            self.verticalScroll['value'] -= amountScroll

    def mouseWheelDown(self, task=None):
        if self.verticalScroll.isHidden():
            return
        amountScroll = 0.075
        if self.verticalScroll['value'] < 1.0:
            self.verticalScroll['value'] += amountScroll

    def loadInventoryPanels(self):
        for item in self.inventory:
            data = [
             item, 1]
            self.addPanel(data, repack=0)

        self.repackPanels()

    def destroy(self):
        self.ignoreAll()
        for panel in self.panels:
            panel.destroy()

        del self.panels
        DirectScrolledFrame.destroy(self)

    def sortPanels(self):
        self.panels.sort(cmp=lambda a, b: cmp(a.name, b.name))
        self.repackPanels()

    def repackPanels(self):
        z = self.listItemHeight
        i = 0
        for i in range(len(self.panels)):
            self.panels[i].setPos(0.01, 0, -z * (i + 1))
            self.panels[i].origionalPos = self.panels[i].getPos(render2d)

        self['canvasSize'] = (
         0, self.listItemWidth - 0.09, -z * (i + 1), 0)

    def addPanel(self, data, repack=1):
        itemId = data[0]
        if itemId == InventoryType.MeleeWeaponL1:
            return
        isDisabled = 0
        panel = self.ListItem(data, trade=self.trade, buy=self.buy, sell=self.sell, use=self.use, weapon=self.weapon, isDisabled=isDisabled)
        panel.reparentTo(self.getCanvas())
        self.panels.append(panel)
        if repack:
            self.repackPanels()
        self.accept('press-wheel_up-%s' % panel.guiId, self.mouseWheelUp)
        self.accept('press-wheel_down-%s' % panel.guiId, self.mouseWheelDown)

    def removePanel(self, data, repack=1):
        for panel in self.panels:
            if panel.data == data:
                self.inventory.remove(panel.data)
                self.panels.remove(panel)
                panel.destroy()
                if repack:
                    self.repackPanels()
                return

    def getPanel(self, data):
        for panel in self.panels:
            if panel.data[0] == data[0]:
                return panel

    def removeAllPanels(self):
        for panel in self.panels:
            panel.destroy()

        self.panels = []
        self.inventory = []

    def show(self):
        DirectScrolledFrame.show(self)

    def hide(self):
        DirectScrolledFrame.hide(self)

    def getItemQuantity(self, itemId):
        counter = 0
        for panel in self.panels:
            if panel.data[0] == itemId:
                counter += panel.data[1]

        return counter