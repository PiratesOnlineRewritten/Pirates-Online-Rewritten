from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.audio import SoundGlobals
from pirates.reputation import ReputationGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryItemList
from pirates.piratesgui import GuiPanel
from pirates.piratesgui import GuiButton
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiButton
from pirates.piratesgui import PurchaseList
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.piratesgui.SongItemGui import SongItemGui

class MusicianGUI(DirectFrame):
    notify = directNotify.newCategory('MusicianGUI')
    width = (PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.06) * 2
    height = 1.35
    columnWidth = PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize + 0.05
    CoinImage = None

    def __init__(self, inventory, name, **kw):
        optiondefs = (
         ('relief', None, None), ('framSize', (0, self.width, 0, self.height), None), ('sortOrder', 20, None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, None, **kw)
        self.initialiseoptions(MusicianGUI)
        if not MusicianGUI.CoinImage:
            MusicianGUI.CoinImage = loader.loadModel('models/gui/toplevel_gui').find('**/treasure_w_coin*')
        self.panel = GuiPanel.GuiPanel(name, self.width, self.height, parent=self)
        self.panel.closeButton['command'] = self.closePanel
        self.setPos(-0.6, 0, -0.66)
        self.balance = 0
        self.inventory = inventory
        self.storeInventory = InventoryItemList.InventoryItemList(self.inventory, self.height - 0.15, buy=PiratesGuiGlobals.InventoryAdd, listItemClass=SongItemGui)
        self.storeInventory.reparentTo(self.panel)
        self.storeInventory.setPos(0.03, 0, 0.04)
        self.cartWidth = self.columnWidth - 0.1
        self.cartHeight = self.height - 0.25
        self.cartFrame = DirectFrame(parent=self.panel, relief=None, frameSize=(0, self.cartWidth, 0, self.cartHeight))
        self.cartFrame.setPos(self.columnWidth + 0.025, 0, 0.08)
        self.myGoldTitle = DirectFrame(parent=self.cartFrame, relief=None, text=PLocalizer.YourMoney, text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0, 0.0), pos=(0.01, 0, 0.155))
        self.myGold = DirectFrame(parent=self.cartFrame, relief=None, text=str(localAvatar.getMoney()), text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(-0.055, 0.0), textMayChange=1, image=MusicianGUI.CoinImage, image_scale=0.15, image_pos=(-0.025, 0, 0.025), pos=(self.cartWidth, 0, 0.155))
        self.accept(PiratesGuiGlobals.InventoryBuyEvent, self.handleBuyItem)
        self.acceptOnce('escape', self.closePanel)
        return

    def closePanel(self):
        messenger.send('exitStore')
        self.ignoreAll()

    def handleBuyItem(self, data, useCode):
        itemId = data[0]
        if not itemId:
            return
        inventory = base.localAvatar.getInventory()
        if not inventory:
            return
        if useCode == PiratesGuiGlobals.InventoryAdd:
            if base.localAvatar.getMoney() < 5:
                base.localAvatar.guiMgr.createWarning(PLocalizer.NotEnoughMoneyWarning, PiratesGuiGlobals.TextFG6)
                return
            if base.musicMgr.current.name not in [SoundGlobals.MUSIC_TAVERN_A, SoundGlobals.MUSIC_TAVERN_B, SoundGlobals.MUSIC_TAVERN_C]:
                base.localAvatar.guiMgr.createWarning(PLocalizer.WaitYourTurnWarning, PiratesGuiGlobals.TextFG6)
                return
            messenger.send('requestMusic', [itemId])
        elif useCode == PiratesGuiGlobals.InventoryRemove:
            raise

    def handleCommitPurchase(self):
        raise