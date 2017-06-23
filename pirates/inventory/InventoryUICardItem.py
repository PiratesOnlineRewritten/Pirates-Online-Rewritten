from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.inventory.InventoryUIGlobals import *
from pirates.minigame import PlayingCardGlobals
from pirates.inventory import InventoryUIItem

class InventoryUICardItem(InventoryUIItem.InventoryUIItem):

    def __init__(self, manager, cardId, itemTuple, imageScaleFactor=1.0, showMax=0):
        amount = itemTuple[3]
        InventoryUIItem.InventoryUIItem.__init__(self, manager, itemTuple, imageScaleFactor=imageScaleFactor)
        self.initialiseoptions(InventoryUICardItem)
        self['relief'] = None
        gui = loader.loadModel('models/gui/suit_icons')
        if not amount:
            self['image'] = gui.find('**/PC_back_standard_dark')
        else:
            self['geom'] = gui.find('**/pir_t_gui_frm_goldCircle')
            self['geom_pos'] = (0.05, 0, 0.05)
            self['geom_scale'] = 0.0625
            suit = PlayingCardGlobals.getSuit(itemTuple[1], fromOffset=0)
            rank = PlayingCardGlobals.getRank(itemTuple[1], fromOffset=0)
            style = PlayingCardGlobals.Styles[0]
            self['image'] = PlayingCardGlobals.getImage(style, suit, rank)
        self.textScale = 1.5
        self.showMax = showMax
        self.itemType = ITEM_STACK
        self.amount = None
        self.localStore = 0
        self.cardId = cardId
        if amount == None:
            self.localStore = 1
            self.updateAmount()
            self.accept('inventoryQuantity-%s-%s' % (localAvatar.getInventory().doId, stackId), self.cardDirty)
        else:
            self.amount = amount
            self.updateAmountText()
        self.textOffset = 0.35
        return

    def cardDirty(self, caller=None):

        def invArrived(inv):
            amount = localAvatar.getInventory().getStackQuantity(self.itemTuple[1])
            limit = localAvatar.getInventory().getStackLimit(self.itemTuple[1])
            self.amount = amount
            self.container.refresh()

        inventoryId = localAvatar.getInventoryId()
        self.getInventory(inventoryId, invArrived)

    def updateAmount(self, caller=None):
        if not self.localStore:
            import pdb
            pdb.set_trace()

        def invArrived(inv):
            if inv:
                amount = inv.getStackQuantity(self.itemTuple[1])
                limit = inv.getStackLimit(self.itemTuple[1])
                self.amount = amount
                self.updateAmountText()

        inventoryId = localAvatar.getInventoryId()
        self.getInventory(inventoryId, invArrived)

    def updateAmountText(self):

        def invArrived(inv):
            if inv:
                limit = localAvatar.getInventory().getStackLimit(self.itemTuple[1])
                if self.amount <= 1:
                    self['text'] = ' '
                    self['geom_color'] = (0.0, 0.0, 0.0, 0.0)
                    self['image_scale'] = 1.0
                    self.setPos(0.0, 0.0, 0.0)
                elif self.showMax:
                    self['text'] = '%s/%s' % (self.amount, limit)
                else:
                    self['text'] = 'x%s' % self.amount
                    self.configure(text_fg=PiratesGuiGlobals.TextFG0, text_font=PiratesGlobals.getInterfaceFont(), text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.05,
                                                                                                                                                                          0.043))
                    self['image_scale'] = 1.5
                    self['geom_color'] = (1.0, 1.0, 1.0, 1.0)

        inventoryId = localAvatar.getInventoryId()
        self.getInventory(inventoryId, invArrived)

    def getName(self):
        return PlayingCardGlobals.getCardName(self.itemTuple[1])

    def getAmount(self):
        return localAvatar.getInventory().getStackQuantity(self.cardId)

    def getLimit(self):
        return localAvatar.getInventory().getStackLimit(self.cardId)

    def getCardId(self):
        return self.cardId