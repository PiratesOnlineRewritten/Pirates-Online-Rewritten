from direct.showbase.ShowBaseGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import StateData
from otp.friends import FriendSecret
from otp.otpbase import OTPGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType

class TradeOfferFrame(DirectFrame):

    def __init__(self, avName, w, h, isLocal, tradePanel):
        DirectFrame.__init__(self, parent=tradePanel, relief=DGG.RIDGE, state=DGG.NORMAL, frameColor=PiratesGuiGlobals.FrameColor, borderWidth=PiratesGuiGlobals.BorderWidth, frameSize=(0, w, 0, h), text=avName, text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.01, h - 0.04))
        self.initialiseoptions(TradeOfferFrame)
        self.isLocal = isLocal
        self.tradePanel = tradePanel
        self.itemsLabel = DirectLabel(parent=self, relief=None, text='No items', text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=11, pos=(0.02, 0, h - 0.2), textMayChange=1)
        if self.isLocal:
            self.goldButton = DirectButton(parent=self, relief=DGG.RAISED, borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameSize=(0, w - 0.04, 0, 0.04), pos=(0.02, 0, h - 0.1), text='Add 1 Gold', text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.03,
                                                                                                                                                                                                                                                                                                                                                                       0.01), frameColor=PiratesGuiGlobals.ButtonColor2, command=self.tradePanel.addGold)
        self.readyButton = DirectButton(parent=self, borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameSize=(0, w - 0.04, 0, 0.04), pos=(0.02,
                                                                                                                                            0,
                                                                                                                                            0.02), text='Ready', text_scale=PiratesGuiGlobals.TextScaleSmall, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0.03,
                                                                                                                                                                                                                                                                                                                                0.01), frameColor=PiratesGuiGlobals.ButtonColor2)
        if self.isLocal:
            self.readyButton['command'] = self.tradePanel.toggleReady
            self.readyButton['state'] = DGG.NORMAL
            self.readyButton['relief'] = DGG.RAISED
        else:
            self.readyButton['state'] = DGG.DISABLED
            self.readyButton['relief'] = DGG.FLAT
        return

    def destroy(self):
        del self.tradePanel
        DirectFrame.destroy(self)


class TradePanel(GuiPanel.GuiPanel):

    def __init__(self, trade):
        GuiPanel.GuiPanel.__init__(self, PLocalizer.TradePanelTitle, 0.8, 1)
        self.initialiseoptions(TradePanel)
        self.trade = trade
        localName = localAvatar.getName()
        self.localOffer = TradeOfferFrame(localName, 0.4 - 0.02, 0.95 - 0.02, 1, self)
        self.localOffer.setPos(0.41, 0, 0.01)
        otherName = 'Other'
        self.otherOffer = TradeOfferFrame(otherName, 0.4 - 0.02, 0.95 - 0.02, 0, self)
        self.otherOffer.setPos(0.01, 0, 0.01)
        self.accept(PiratesGlobals.TradeChangedEvent, self.updateTrade)
        self.accept(PiratesGlobals.TradeFinishedEvent, self.finishedTrade)
        self.accept(PiratesGlobals.TradeFinishedEvent, self.finishedTrade)
        self.accept(PiratesGuiGlobals.InventoryTradeEvent, self.processItem)
        self.updateTrade()
        if base.cr.avatarFriendsManager.checkIgnored(self.trade.firstAvatarId) or base.cr.avatarFriendsManager.checkIgnored(self.trade.secondAvatarId):
            self.closePanel()
            return

    def closePanel(self):
        self.trade.tradeCanceled()
        self.trade.sendRequestRemoveTrade()
        GuiPanel.GuiPanel.closePanel(self)

    def finishedTrade(self, trade):
        self.destroy()

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        del self.trade
        del self.localOffer
        del self.otherOffer
        GuiPanel.GuiPanel.destroy(self)

    def toggleReady(self):
        status = self.trade.getStatus()
        self.trade.sendRequestChangeStatus(not status)

    def addGold(self):
        giving = self.trade.getGiving()
        giving.append([InventoryType.ItemTypeMoney, 1])
        self.trade.sendRequestChangeGiving(giving)

    def getGivingText(self, giving):
        text = ''
        for item in giving:
            itemName = PLocalizer.InventoryTypeNames[item[0]]
            itemAmount = item[1]
            text += '%s %s, ' % (itemAmount, itemName)

        return text

    def updateTrade(self):
        localGiving = self.trade.getGiving()
        localStatus = self.trade.getStatus()
        self.localOffer.itemsLabel['text'] = self.getGivingText(localGiving)
        if localStatus:
            text = 'Ready'
        else:
            text = 'Not Ready'
        self.localOffer.readyButton['text'] = text
        otherGiving = self.trade.getOtherGiving()
        otherStatus = self.trade.getOtherStatus()
        self.otherOffer.itemsLabel['text'] = self.getGivingText(otherGiving)
        if otherStatus:
            text = 'Ready'
        else:
            text = 'Not Ready'
        self.otherOffer.readyButton['text'] = text

    def processItem(self, itemData, addOrRemove):
        if addOrRemove == PiratesGuiGlobals.InventoryAdd:
            giving = self.trade.getGiving()
            giving.append(itemData)
            self.trade.sendRequestChangeGiving(giving)
        elif addOrRemove == PiratesGuiGlobals.ItemRemove:
            pass

    def rejectChangeGiving(self, reason):
        pass

    def rejectChangeStatus(self, reason):
        pass

    def rejectRemoveTrade(self, reason):
        pass