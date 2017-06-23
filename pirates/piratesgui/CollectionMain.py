from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryPage
from pirates.piratesgui import InventoryItemGui
from pirates.piratesgui import InventoryItemList
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import CollectionMap

class CollectionMain(InventoryPage.InventoryPage):

    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(CollectionMain)
        gui = loader.loadModel('models/gui/toplevel_gui')
        ornament = loader.loadModel('models/gui/gui_treasure_window_a')
        ornament.setPos(0.53, 0, 0.72)
        ornament.setScale(0.315)
        ornament.reparentTo(self)
        ornament.flattenStrong()
        self.treasureList = DirectScrolledFrame(parent=self, relief=None, state=DGG.NORMAL, frameColor=PiratesGuiGlobals.FrameColor, borderWidth=PiratesGuiGlobals.BorderWidth, frameSize=(0, PiratesGuiGlobals.InventoryPanelWidth - 0.1, 0, PiratesGuiGlobals.InventoryPanelHeight - 0.1 - PiratesGuiGlobals.ScrollbarSize), canvasSize=(0, PiratesGuiGlobals.InventoryPanelWidth - 1.1, 0, PiratesGuiGlobals.InventoryPanelHeight - 0.1 - PiratesGuiGlobals.ScrollbarSize), verticalScroll_frameColor=PiratesGuiGlobals.ScrollbarColor, verticalScroll_borderWidth=(0.005,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       0.005), verticalScroll_frameSize=(0, PiratesGuiGlobals.ScrollbarSize, 0, PiratesGuiGlobals.InventoryPageHeight - 0.4), verticalScroll_thumb_frameColor=PiratesGuiGlobals.ButtonColor2, verticalScroll_incButton_frameColor=PiratesGuiGlobals.ButtonColor2, verticalScroll_decButton_frameColor=PiratesGuiGlobals.ButtonColor2, horizontalScroll_frameColor=PiratesGuiGlobals.ScrollbarColor, horizontalScroll_borderWidth=(0.005,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0.005), horizontalScroll_frameSize=(0, PiratesGuiGlobals.InventoryItemGuiWidth + PiratesGuiGlobals.ScrollbarSize, 0, PiratesGuiGlobals.ScrollbarSize), horizontalScroll_thumb_frameColor=PiratesGuiGlobals.ButtonColor2, horizontalScroll_incButton_frameColor=PiratesGuiGlobals.ButtonColor2, horizontalScroll_decButton_frameColor=PiratesGuiGlobals.ButtonColor2, sortOrder=5)
        self.treasureList.setPos(0.02, 0, -0.02)
        localHeight = PiratesGuiGlobals.InventoryPanelHeight - 0.2
        self.card = loader.loadModel('models/gui/treasure_gui')
        tex = gui.find('**/treasure_w_coin*')
        self.goldPic = DirectFrame(parent=self.treasureList.getCanvas(), relief=None, image=tex, image_scale=0.4, image_pos=(-0.05, 0, 0), pos=(0.35, 0, localHeight - 0.36), text=PLocalizer.MoneyName, text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ALeft, text_scale=0.03, text_pos=(-0.2, 0.02, 0))
        self.numGold = DirectLabel(parent=self.goldPic, relief=None, text='0', text_align=TextNode.ALeft, text_scale=0.04, text_fg=PiratesGuiGlobals.TextFG2, textMayChange=1, pos=(0.04, 0, -0.03), text_font=PiratesGlobals.getInterfaceOutlineFont())
        if base.cr.config.GetBool('buried-treasure', 0):
            self.buryButton = DirectButton(parent=self, relief=None, image=tex, image_scale=0.4, image_pos=(0,
                                                                                                            0,
                                                                                                            0), pos=(0.5, 0, localHeight - 0.12), command=self.buryTreasure, text='BURY TREASURE', text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ACenter, text_scale=0.025, text_pos=(0, -0.085, 0))
        tex = gui.find('**/treasure_w_card*')
        self.cardPic = DirectFrame(parent=self.treasureList.getCanvas(), relief=None, image=tex, image_scale=0.4, image_pos=(-0.05, 0, 0), pos=(0.76, 0, localHeight - 0.36), text=PLocalizer.CheatCardName, text_fg=PiratesGuiGlobals.TextFG2, text_align=TextNode.ALeft, text_scale=0.03, text_pos=(-0.23, 0.02, 0))
        self.cardPic.setTransparency(1)
        self.numCards = DirectLabel(parent=self.cardPic, relief=None, text='0', text_align=TextNode.ALeft, text_scale=0.04, text_fg=PiratesGuiGlobals.TextFG2, textMayChange=1, pos=(0.042, 0, -0.03), text_font=PiratesGlobals.getInterfaceOutlineFont())
        self.treLabel = DirectLabel(parent=self.treasureList.getCanvas(), relief=None, text=PLocalizer.Treasure, text_align=TextNode.ALeft, text_scale=0.03, text_fg=PiratesGuiGlobals.TextFG2, textMayChange=1, pos=(0.144, 0, localHeight - 0.48))
        spotPic = gui.find('**/treasure_w_a_slot')
        blipParent = NodePath('blipParent')
        for colSpot in range(4):
            for rowSpot in range(4):
                if colSpot > 0:
                    blip = spotPic.copyTo(blipParent)
                    blip.setScale(0.45)
                    blip.setPos(0.24 + 0.18 * rowSpot, 0, localHeight - 0.4 - 0.18 * colSpot)

        blipParent.flattenStrong()
        blipFrame = DirectFrame(parent=self.treasureList.getCanvas(), relief=None, geom=blipParent)
        gui.removeNode()
        self.setPics = {}
        return

    def show(self):
        self.refreshList()
        InventoryPage.InventoryPage.show(self)

    def hide(self, hideSub=True):
        InventoryPage.InventoryPage.hide(self)
        if hideSub:
            if hasattr(base, 'localAvatar'):
                base.localAvatar.guiMgr.collectionPage.hide()

    def addPanel(self, data, repack=1):
        pass

    def removePanel(self, index, repack=1):
        pass

    def clearList(self):
        for item in self.setPics:
            self.setPics[item].destroy()

        self.setPics = {}

    def goToCollection(self, setKey):
        base.localAvatar.guiMgr.showSubCollection(setKey=setKey)

    def refreshList(self, newWeaponId=None):
        inv = localAvatar.getInventory()
        if not inv:
            return
        cardCount = 0
        for i in range(52):
            cardCount += inv.getStackQuantity(InventoryType.begin_Cards + i)

        self.numCards['text'] = '%d' % cardCount
        self.numGold['text'] = '%d' % base.localAvatar.getMoney()
        setCount = 0
        activeSets = []
        heightOffset = 0
        for loopItr in range(len(InventoryType.Collection_Sets)):
            setKey = InventoryType.Collection_Sets[loopItr]
            if inv.getStackQuantity(setKey) > 0:
                activeSets.append([setKey, loopItr])

        setCount = len(activeSets)
        for loopItr in range(setCount):
            setKey = activeSets[loopItr][0]
            spot = activeSets[loopItr][1]
            if setKey in self.setPics:
                pass
            else:
                rowSpot = spot % 4
                colSpot = 1 + spot / 4
                localHeight = PiratesGuiGlobals.InventoryPanelHeight - 0.2
                pic_name = CollectionMap.Assets[setKey]
                tex = self.card.find('**/%s*' % pic_name)
                self.setPics[setKey] = DirectButton(parent=self.treasureList.getCanvas(), relief=None, image=tex, image_scale=0.34, image2_scale=0.36, image_pos=(0,
                                                                                                                                                                  0,
                                                                                                                                                                  0), pos=(0.24 + 0.18 * rowSpot, 0, localHeight - 0.4 - 0.18 * colSpot), command=self.goToCollection, extraArgs=[setKey], text=PLocalizer.Collections[setKey], text0_fg=PiratesGuiGlobals.TextFG1, text1_fg=PiratesGuiGlobals.TextFG1, text2_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=5, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleTiny, text_pos=(0, -0.085, 0))
                self.setPics[setKey].setTransparency(1)
            if inv.getStackQuantity(setKey) > 1:
                pass

        return

    def buryTreasure(self):
        print 'DPARIS DEBUG - Attempting to bury treasure here'

    def destroy(self):
        self.clearList()
        self.treasureList.destroy()
        del self.treasureList
        DirectFrame.destroy(self)