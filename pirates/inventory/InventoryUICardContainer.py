from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIStackContainer
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import WeaponGlobals
from pirates.minigame import PlayingCardGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.inventory import InventoryUIContainer
from pirates.inventory.InventoryUIGlobals import *

class InventoryUICardContainer(InventoryUIStackContainer.InventoryUIStackContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=4, countZ=4, minCountZ=4, maxCountX=5, itemList=None):
        self.isReady = 0
        InventoryUIStackContainer.InventoryUIStackContainer.__init__(self, manager, sizeX, sizeZ, minCountZ=minCountZ, maxCountX=maxCountX, itemList=itemList)
        self.initialiseoptions(InventoryUICardContainer)
        self.seperatorOn = 1
        gui = loader.loadModel('models/gui/gui_main')
        scale = 0.335
        self.background = self.attachNewNode('background')
        self.background.setScale(scale)
        self.background.setPos(0.35, 0, 0.46)
        gui.find('**/gui_inv_cards').copyTo(self.background)
        self.background.flattenStrong()
        suitGui = loader.loadModel('models/gui/suit_icons')
        cardImage = suitGui.find('**/pir_t_gui_frm_goldCircle')
        if cardImage.isEmpty():
            cardImage = None
        i = 0
        for suit in ['h', 'd', 'c', 's']:
            if suit in ['h', 'd']:
                suitColor = (0.7, 0.7, 0.7, 1.0)
            else:
                suitColor = (1.0, 1.0, 1.0, 1.0)
            suitFrame = DirectFrame(parent=self.background, relief=None, geom=suitGui.find('**/suit_icon_%s' % suit), geom_scale=0.1, geom_color=suitColor, image=cardImage, image_scale=0.15, pos=(i * 0.234, 0, 0.9))
            i += 1
            n = NodePath(suitFrame.node().getStateDef(0))
            PiratesGlobals.flattenOrdered(n)
            ng = n.getChild(0).copyTo(self.background)
            ng.setPos(suitFrame.getPos())
            n.getChild(0).hide()
        else:
            PiratesGlobals.flattenOrdered(self.background)
            self.cardDict = {}
            self.updateList = []
            self.cardGroup = self.attachNewNode('cardGroup')
            self.cellSizeX = self.cellSizeX * 2.0
            return

    def setTitleInfo(self):
        gui = loader.loadModel('models/gui/toplevel_gui')
        chestButtonOpen = gui.find('**/treasure_w_card')
        chestButtonClosed = gui.find('**/treasure_w_card')
        self.titleImageOpen = chestButtonOpen
        self.titleImageClosed = chestButtonClosed
        self.titleName = PLocalizer.InventoryPageCards
        self.titleImageOpen.setScale(0.4)
        self.titleImageClosed.setScale(0.4)

    def resizeItem(self, item):
        InventoryUIStackContainer.InventoryUIStackContainer.resizeItem(self, item)
        item.updateAmountText()
        item.setPos(0, 0, 0)
        item['text_pos'] = (0.05, 0.043)
        item['geom_pos'] = (0.05, 0, 0.05)
        if item.getAmount() == 0:
            scale = 2.0 * self.cellSizeX * item.imageScale
            item['image_scale'] = [scale, scale, scale * 0.96 / 0.71]
        elif item.cell != None and item.cell == self.manager.withInCell:
            scale = 9.0 * self.cellSizeX * item.imageScale
            item['image_scale'] = [scale, scale, scale * 0.9]
            item.setPos(0.025, 0, 0)
            item['text_pos'] = (0.08, 0.043)
            item['geom_pos'] = (0.08, 0, 0.05)
        elif item.getAmount() == 1:
            scale = 7.0 * self.cellSizeX * item.imageScale
            item['image_scale'] = [scale, scale, scale * 0.9]
        else:
            scale = 7.0 * self.cellSizeX * item.imageScale
            item['image_scale'] = [scale, scale, scale * 0.9]
        return

    def handleWithIn(self, cell, clear):
        if cell and cell.inventoryItem:
            self.resizeItem(cell.inventoryItem)

    def takeOut(self):
        InventoryUIContainer.InventoryUIContainer.takeOut(self)
        if not self.isReady:
            self.doSetup()
            self.isReady = 1
            for itemId in self.itemList:
                self.accept('inventoryQuantity-%s-%s' % (localAvatar.getInventory().doId, itemId), self.handleUpdateCardItem, extraArgs=[itemId])

        for itemId in self.updateList:
            self.placeCardItem(itemId)

        self.updateBufferedCards()

    def updateBufferedCards(self):

        def invArrived(inv):
            if self.isReady:
                for itemId in self.updateList:
                    self.placeCardItem(itemId)

                self.updateList = []

        inventoryId = localAvatar.getInventoryId()
        self.getInventory(inventoryId, invArrived)

    def show(self):
        InventoryUIStackContainer.InventoryUIStackContainer.show(self)
        if self.isReady:
            self.updateBufferedCards()

    def handleUpdateCardItem(self, itemId, amount=None):
        if self.isHidden():
            if itemId not in self.updateList:
                self.updateList.append(itemId)
        else:
            self.placeCardItem(itemId)

    def clearOut(self):
        self.cardDict = {}
        self.updateList = []
        InventoryUIContainer.InventoryUIContainer.clearOut(self)
        self.cardGroup.removeChildren()
        self.ignore('seachestOpened')

    def refresh(self):
        self.clearOut()
        self.isReady = 0
        if not self.isHidden():
            self.doSetup()
            self.isReady = 1

    def figureOutStackTypes(self):
        suitDict = {}
        for cardId in self.itemList:
            suit = PlayingCardGlobals.getSuit(cardId, fromOffset=1)
            if not suitDict.has_key(suit):
                suitDict[suit] = []
            suitDict[suit].append(cardId)

        self.listOfItemLists = []
        for key in suitDict:
            itemList = suitDict[key]
            while len(itemList) > self.maxCountX:
                frontList = itemList[:self.maxCountX]
                backList = itemList[self.maxCountX:]
                self.listOfItemLists.append(frontList)
                itemList = backList

            self.listOfItemLists.append(itemList)

    def computeCellSize(self):
        self.gridZ = len(self.listOfItemLists)
        listLengths = []
        for skillList in self.listOfItemLists:
            listLengths.append(len(skillList))

        self.gridX = max(listLengths)

    def setupCells(self):
        self.figureOutStackTypes()
        self.computeCellSize()
        suitsAdded = []
        for Z in range(self.gridZ):
            for X in range(len(self.listOfItemLists[Z])):
                cardId = self.listOfItemLists[Z][X]
                cardValue = cardId - InventoryType.begin_Cards
                cardName = PlayingCardGlobals.getCardName(cardValue)
                suit = PlayingCardGlobals.getSuit(cardValue, fromOffset=0)
                rank = PlayingCardGlobals.getRank(cardValue, fromOffset=0)
                if suit not in suitsAdded:
                    suitsAdded.append(suit)
                    if self.seperatorOn:
                        self.seperatorCount += 1
                bottomCard = 0
                if rank == 0:
                    bottomCard = 1
                cardCell = self.getCell(bottomCard=bottomCard)
                cardCell.setPos(self.findGridPos(suit, rank))
                self.cardDict[cardId] = cardCell
                self.placeCardItem(cardId)

        self.accept('seachestOpened', self.updateBufferedCards)

    def placeCardItem(self, cardId):
        cardCell = self.cardDict[cardId]
        cardValue = cardId - InventoryType.begin_Cards
        if cardCell.inventoryItem:
            cardCell.inventoryItem.removeNode()
            cardCell.inventoryItem = None
        newItem = self.getItem(cardId, cardValue)
        newItem.container = self
        self.putIntoCell(newItem, cardCell)
        return

    def findGridPos(self, x, z, wantGap=0):
        offX = 0.0
        offZ = -0.05
        return Point3(offX + float(x) * self.cellSizeX * 0.21, 0, offZ + float(z) * self.cellSizeZ * 0.035)

    def getCell(self, bottomCard=0):
        if bottomCard:
            ammoCell = self.makeCell(frameScale=(0.11, 0.09), offset=(0.0, 0.0))
        else:
            ammoCell = self.makeCell(frameScale=(0.11, 0.035), offset=(0.0, 0.05))
        return ammoCell

    def getItem(self, cardId, cardValue):
        stackQuantity = 0
        inventory = localAvatar.getInventory()
        if inventory:
            stackQuantity = localAvatar.getInventory().getStackQuantity(cardId)
        itemTuple = [
         0, cardValue, 0, stackQuantity]
        cardItem = self.manager.makeCardItem(cardId, itemTuple)
        return cardItem

    def cellClick(self, cell, mouseAction=MOUSE_CLICK, task=None):
        if mouseAction == MOUSE_PRESS and cell.inventoryItem:
            cardValue = cell.inventoryItem.itemTuple[1]
            suit = PlayingCardGlobals.getSuit(cardValue, fromOffset=0)
            rank = PlayingCardGlobals.getRank(cardValue, fromOffset=0)
            messenger.send('cardPicked', [suit, rank])