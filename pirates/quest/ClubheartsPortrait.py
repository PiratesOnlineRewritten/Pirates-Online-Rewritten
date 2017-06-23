from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer, PiratesGlobals
from pirates.piratesgui import GuiButton
from pirates.piratesgui.CheckButton import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals, InventoryGlobals
from pirates.makeapirate import ClothingGlobals
from pirates.piratesgui.CheckButton import *
from pirates.inventory.InventoryGlobals import Locations
from pirates.quest.QuestConstants import NPCIds

class ClubheartsPortrait(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, parent=base.a2dTopLeft, relief=None, pos=(1.0, 0, -0.35))
        self.initialiseoptions(ClubheartsPortrait)
        portraitGui = loader.loadModel('models/props/portrait_clubhearts')
        detailGui = loader.loadModel('models/gui/gui_card_detail')
        maleItems = [
         ItemGlobals.STRAW_EXPLORER_HAT, ItemGlobals.FLAP_LONG_SLEEVE, ItemGlobals.F44_DUBLOON_BREECHES]
        femaleItems = [
         ItemGlobals.WOODLAND_TOP, ItemGlobals.CANDYBOX_SKIRT, ItemGlobals.FOREST_KNEE_BOOTS]
        if localAvatar.getStyle().getGender() == 'm':
            titleName = PLocalizer.NPCNames[NPCIds.BEN_CLUBHEART]
            self.items = maleItems
        else:
            titleName = PLocalizer.NPCNames[NPCIds.SANDIE_CLUBHEART]
            self.items = femaleItems
        panels = self.attachNewNode('panels')
        topPanel = panels.attachNewNode('topPanel')
        detailGui.find('**/top_panel').copyTo(topPanel)
        topPanel.setScale(0.06)
        topPanel.reparentTo(self)
        topPanel.setZ(0.08)
        middlePanel = panels.attachNewNode('middlePanel')
        detailGui.find('**/middle_panel').copyTo(middlePanel)
        middlePanel.setScale(0.06)
        middlePanel.reparentTo(self)
        middlePanel.setZ(0.08)
        for i in range(1, 6):
            middlePanel = panels.attachNewNode('middlePanel%s' % i)
            detailGui.find('**/middle_panel').copyTo(middlePanel)
            middlePanel.setScale(0.06)
            middlePanel.reparentTo(self)
            middlePanel.setZ(0.08 - i * 0.125)

        panels.flattenStrong()
        bottomPanel = panels.attachNewNode('bottomPanel')
        detailGui.find('**/bottom_panel').copyTo(bottomPanel)
        bottomPanel.reparentTo(self)
        bottomPanel.setScale(0.06)
        bottomPanel.setZ(-0.5)
        self.bg = DirectFrame(parent=self, relief=None, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_fg=PiratesGuiGlobals.TextFG26, text_align=TextNode.ACenter, text=titleName, text_pos=(0.0,
                                                                                                                                                                                                     0.25), text_shadow=PiratesGuiGlobals.TextShadow, image=portraitGui.find('**/picture'), image_scale=0.125, image_pos=(0.0, 0.0, -0.08))
        portraitGui.removeNode()
        detailGui.removeNode()
        i = 0
        self.checkBoxes = []
        for item in self.items:
            self.checkBoxes.append(self.makeItem(item, i))
            i += 1

        self.accept(InventoryGlobals.getCategoryChangeMsg(localAvatar.getInventoryId(), InventoryType.ItemTypeClothing), self.updateItems)
        return

    def destroy(self):
        self.ignoreAll()
        for checkBox in self.checkBoxes:
            checkBox[0].destroy()
            checkBox[1].destroy()

        self.checkBoxes = []
        self.items = []
        DirectFrame.destroy(self)

    def makeItem(self, itemId, index):
        checkBox = CheckButton(parent=self, relief=None, scale=0.35, value=self.isItemEquipped(itemId), pos=(-0.17, 0, -0.42 - index * 0.075), state=DGG.DISABLED)
        typeText = ClothingGlobals.getClothingTypeName(ItemGlobals.getType(itemId))
        label = DirectLabel(parent=self, relief=None, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG0, text_align=TextNode.ALeft, text=typeText, pos=(-0.12, 0, -0.43 - index * 0.075))
        return (
         checkBox, label)

    def isItemEquipped(self, itemId):
        inv = localAvatar.getInventory()
        if not inv:
            return False
        locationRange = Locations.RANGE_EQUIP_CLOTHES
        for location in range(locationRange[0], locationRange[1] + 1):
            locatable = inv.getLocatables().get(location)
            if locatable and locatable[1] == itemId:
                return True

        return False

    def updateItems(self, event=None):
        for i in range(0, len(self.items)):
            self.checkBoxes[i][0]['value'] = self.isItemEquipped(self.items[i])