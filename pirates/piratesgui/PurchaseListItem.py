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
from pirates.piratesgui.InventoryListItem import InventoryListItem

class PurchaseListItem(InventoryListItem):
    itemCount = 0
    itemCost = 0
    itemQuantity = 0

    def __init__(self, data, trade=0, buy=0, sell=0, use=0, weapon=0, isDisabled=0, **kw):
        width = PiratesGuiGlobals.PurchaseListItemWidth
        height = PiratesGuiGlobals.PurchaseListItemHeight
        optiondefs = (
         ('relief', None, None), ('state', DGG.NORMAL, None), ('frameSize', (0, width, 0, height), None), ('pressEffect', 0, None), ('command', self.sendEvents, None))
        self.defineoptions(kw, optiondefs)
        InventoryListItem.__init__(self, data, trade=trade, buy=buy, sell=sell, use=use, weapon=weapon, isDisabled=isDisabled, width=PiratesGuiGlobals.PurchaseListItemWidth, height=PiratesGuiGlobals.PurchaseListItemHeight)
        self.initialiseoptions(PurchaseListItem)
        self.createGui()
        self.bind(DGG.ENTER, self.highlightStart)
        self.bind(DGG.EXIT, self.highlightStop)
        return

    def addItem(self):
        self.itemCount += 1
        self.updateItem()

    def removeItem(self):
        self.itemCount -= 1
        self.updateItem()

    def updateItem(self):
        self.quantityLabel['text'] = str(self.itemQuantity * self.itemCount)
        self.costText['text'] = str(self.itemCount * self.itemCost)
        self.price = self.itemCount * self.itemCost

    def createGui(self):
        itemId = self.data[0]
        self.itemCount += 1
        self.itemQuantity = self.quantity
        self.itemCost = self.price
        self.picture = DirectFrame(parent=self, relief=None, state=DGG.DISABLED, pos=(0.035,
                                                                                      0,
                                                                                      0.025))
        self.quantityLabel = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=str(self.quantity), text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleSmall * PLocalizer.getHeadingScale(2), text_align=TextNode.ARight, text_wordwrap=11, pos=(0.1225,
                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                   0.015))
        if len(self.name) >= 39:
            textScale = PiratesGuiGlobals.TextScaleMicro * PLocalizer.getHeadingScale(2)
        else:
            if len(self.name) >= 35:
                textScale = PiratesGuiGlobals.TextScaleTiny * PLocalizer.getHeadingScale(2)
            else:
                textScale = PiratesGuiGlobals.TextScaleSmall * PLocalizer.getHeadingScale(2)
            self.nameTag = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, text=self.name, text_fg=PiratesGuiGlobals.TextFG2, text_scale=textScale, text_align=TextNode.ALeft, pos=(0.13,
                                                                                                                                                                                              0,
                                                                                                                                                                                              0.015))
            self.costText = DirectLabel(parent=self, relief=None, state=DGG.DISABLED, image=InventoryListItem.coinImage, image_scale=0.12, image_pos=Vec3(-0.005, 0, 0.0125), text=str(self.price), text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ARight, text_wordwrap=11, text_pos=(-0.03, 0, 0), pos=(self.width - 0.035, 0, 0.015), text_font=PiratesGlobals.getInterfaceFont())
            itemClass = EconomyGlobals.getItemCategory(itemId)
            itemType = EconomyGlobals.getItemType(itemId)
            if itemType == ItemType.FISHING_ROD or itemType == ItemType.FISHING_LURE:
                asset = EconomyGlobals.getItemIcons(itemId)
                if asset:
                    self.picture['geom'] = PurchaseListItem.fishingIcons.find('**/%s*' % asset)
                    self.picture['geom_scale'] = 0.04
                    self.picture['geom_pos'] = (0, 0, 0)
            elif itemClass == ItemType.WEAPON or itemClass == ItemType.POUCH:
                asset = EconomyGlobals.getItemIcons(itemId)
                if asset:
                    self.picture['geom'] = InventoryListItem.weaponIcons.find('**/%s*' % asset)
                    self.picture['geom_scale'] = 0.04
                    self.picture['geom_pos'] = (0, 0, 0)
            elif itemClass == ItemType.CONSUMABLE:
                asset = EconomyGlobals.getItemIcons(itemId)
                if asset:
                    self.picture['geom'] = InventoryListItem.skillIcons.find('**/%s*' % asset)
                    self.picture['geom_scale'] = 0.04
                    self.picture['geom_pos'] = (0, 0, 0)
            if InventoryType.begin_WeaponCannonAmmo <= itemId and itemId <= InventoryType.end_WeaponCannonAmmo or InventoryType.begin_WeaponPistolAmmo <= itemId and itemId <= InventoryType.end_WeaponGrenadeAmmo or InventoryType.begin_WeaponDaggerAmmo <= itemId and itemId <= InventoryType.end_WeaponDaggerAmmo:
                skillId = WeaponGlobals.getSkillIdForAmmoSkillId(itemId)
                if skillId:
                    asset = WeaponGlobals.getSkillIcon(skillId)
                    if asset:
                        self.picture['geom'] = InventoryListItem.skillIcons.find('**/%s' % asset)
                        self.picture['geom_scale'] = 0.06
                        self.picture['geom_pos'] = (0, 0, 0)
            if InventoryType.SmallBottle <= itemId and itemId <= InventoryType.LargeBottle:
                self.picture['geom'] = self.topGui.find('**/main_gui_ship_bottle')
                self.picture['geom_scale'] = 0.1
                self.picture['geom_pos'] = (0, 0, 0)
        self.flattenStrong()
        return

    def destroy(self):
        del self.picture
        self.highlightStop()
        InventoryListItem.destroy(self)

    def createHighlight(self, args=None):
        self.quantityLabel['text_fg'] = self.costText['text_fg'] = self.nameTag['text_fg'] = PiratesGuiGlobals.TextFG6

    def highlightStart(self, event=None):
        taskMgr.doMethodLater(PiratesGuiGlobals.HelpPopupTime, self.createHighlight, 'itemHighlightTask')
        self.createHighlight()

    def highlightStop(self, event=None):
        taskMgr.remove('itemHighlightTask')
        self.quantityLabel['text_fg'] = self.costText['text_fg'] = self.nameTag['text_fg'] = PiratesGuiGlobals.TextFG2