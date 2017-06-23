from pandac.PandaModules import *
from direct.gui.DirectGui import *
from otp.otpgui import OTPDialog
from pirates.piratesbase import PLocalizer
from pirates.minigame import PlayingCardGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import PDialog
from pirates.piratesgui.GuiButton import GuiButton
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui import GuiTray
from pirates.minigame import PlayingCard
from pirates.minigame import PlayingCardGlobals
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class TableGUI():
    use_hourglass = False

    def suitImage(self, suit):
        card = PlayingCard.PlayingCardNodePath('standard', PlayingCardGlobals.Unknown)
        card.setScale(0.25)
        card.setValue(suit * 13)
        card.turnUp()
        card.show()
        return card

    def initializeTableInterface(self):
        self.levelUpIval = None
        self.swapCard = False
        self.cardSwapIndex = 0
        self.swapDialog = None
        self.leaveDialog = None
        self.swapResultDialog = None
        self.timer = False
        self.timeout = False
        self.buttonArray = []
        self.suitGeomArray = []
        if not True:
            self.suitGeomArray.append(self.suitImage(0))
            self.suitGeomArray.append(self.suitImage(1))
            self.suitGeomArray.append(self.suitImage(2))
            self.suitGeomArray.append(self.suitImage(3))
        else:
            self.suitIcons = loader.loadModel('models/gui/suit_icons')
            if self.suitIcons:
                scale = 0.08
                icon = self.suitIcons.find('**/suit_icon_h')
                icon.setScale(scale)
                self.suitGeomArray.append(icon)
                icon = self.suitIcons.find('**/suit_icon_d')
                icon.setScale(scale)
                self.suitGeomArray.append(icon)
                icon = self.suitIcons.find('**/suit_icon_c')
                icon.setScale(scale)
                self.suitGeomArray.append(icon)
                icon = self.suitIcons.find('**/suit_icon_s')
                icon.setScale(scale)
                self.suitGeomArray.append(icon)
            else:
                self.suitGeomArray = [
                 None, None, None, None]
        x = -0.36
        y = 0.07
        x_increment = 0.24
        text = PLocalizer.TableLeave
        button = GuiButton(parent=self.menu, command=self.leaveAction, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [PlayingCardGlobals.Leave])
        self.leaveButton = button
        self.buttonArray = self.buttonArray + [button]
        button.show()
        text = PLocalizer.TableCancel
        button = GuiButton(parent=self.menu, command=self.cancelSelection, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [0])
        self.cancelButton = button
        self.buttonArray = self.buttonArray + [button]
        button.hide()
        x = x + x_increment
        self.suit = 0
        self.rank = 0
        self.cardSwapIndex = 0
        self.suitButtonArray = []
        self.rankButtonArray = []
        x = -0.36
        y = 0.1775
        x_increment = 0.24
        suit = 0
        text = PLocalizer.PlayingCardSuits[suit]
        button = GuiButton(parent=self.menu, command=self.cardSuitSelection, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [suit])
        self.suitButtonArray = self.suitButtonArray + [button]
        geom = self.suitGeomArray[suit]
        button['geom'] = geom
        button.setGeom()
        x = x + x_increment
        suit = suit + 1
        text = PLocalizer.PlayingCardSuits[suit]
        button = GuiButton(parent=self.menu, command=self.cardSuitSelection, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [suit])
        self.suitButtonArray = self.suitButtonArray + [button]
        geom = self.suitGeomArray[suit]
        button['geom'] = geom
        button.setGeom()
        x = x + x_increment
        suit = suit + 1
        text = PLocalizer.PlayingCardSuits[suit]
        button = GuiButton(parent=self.menu, command=self.cardSuitSelection, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [suit])
        self.suitButtonArray = self.suitButtonArray + [button]
        geom = self.suitGeomArray[suit]
        button['geom'] = geom
        button.setGeom()
        x = x + x_increment
        suit = suit + 1
        text = PLocalizer.PlayingCardSuits[suit]
        button = GuiButton(parent=self.menu, command=self.cardSuitSelection, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [suit])
        self.suitButtonArray = self.suitButtonArray + [button]
        geom = self.suitGeomArray[suit]
        button['geom'] = geom
        button.setGeom()
        x = x + x_increment
        suit = suit + 1
        x = -0.36 - 0.06
        y = 0.1775
        x_increment = 0.12
        rank = 0
        text = PLocalizer.Card2
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        text = PLocalizer.Card3
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        text = PLocalizer.Card4
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        text = PLocalizer.Card5
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        text = PLocalizer.Card6
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        text = PLocalizer.Card7
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        text = PLocalizer.Card8
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        text = PLocalizer.Card9
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        x = -0.36 - 0.06
        y = 0.07
        x_increment = 0.12
        x = x + x_increment
        x = x + x_increment
        x = x + x_increment
        text = PLocalizer.CardT
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        text = PLocalizer.CardJ
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        text = PLocalizer.CardQ
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        text = PLocalizer.CardK
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        text = PLocalizer.CardA
        button = GuiButton(parent=self.menu, command=self.cardRankSelection, canReposition=True)
        self.setButtonSettingsHalfWidth(button, (x, 0, y), text, [rank])
        self.rankButtonArray = self.rankButtonArray + [button]
        x = x + x_increment
        rank = rank + 1
        return

    def setRankButtonArrayGeoms(self, geom):
        if geom:
            for button in self.rankButtonArray:
                if button:
                    button['geom'] = None
                    button.setGeom()
                    button['geom'] = geom
                    button.setGeom()

        return

    def disableButton(self, button):
        if button:
            c = 0.5
            button['state'] = DGG.DISABLED
            button['text_fg'] = (c, c, c, 1.0)

    def normalButton(self, button):
        if button:
            c = 1.0
            button['state'] = DGG.NORMAL
            button['text_fg'] = (c, c, c, 1.0)

    def setButtonSettingsHalfWidth(self, button, position, text, extra=None):
        button.configure(text=text, text_fg=(1.0, 1.0, 1.0, 1.0), text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0, -PiratesGuiGlobals.TextScaleLarge * 0.25), text_wordwrap=0, image_scale=(0.11,
                                                                                                                                                                                                     0.22,
                                                                                                                                                                                                     0.24))
        button.setPos(position[0], position[1], position[2])
        button['extraArgs'] = extra
        button.resetFrameSize()
        button.hide()

    def setButtonSettings(self, button, position, text, extra=None):
        button.configure(text=text, text_fg=(1.0, 1.0, 1.0, 1.0), text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0, -PiratesGuiGlobals.TextScaleLarge * 0.25), text_wordwrap=0, image_scale=(0.24,
                                                                                                                                                                                                     0.24,
                                                                                                                                                                                                     0.24))
        button.setPos(position[0], position[1], position[2])
        button['extraArgs'] = extra
        button.resetFrameSize()
        button.hide()

    def setButtonSettings2Lines(self, button, position, text, extra=None):
        button.configure(text=text, text_fg=(1.0, 1.0, 1.0, 1.0), text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0, PiratesGuiGlobals.TextScaleLarge * 0.25), text_wordwrap=0, image_scale=(0.24,
                                                                                                                                                                                                    0.24,
                                                                                                                                                                                                    0.24))
        button.setPos(position[0], position[1], position[2])
        button['extraArgs'] = extra
        button.resetFrameSize()
        button.hide()

    def hideButtonArray(self, buttonArray):
        length = len(buttonArray)
        for i in range(length):
            buttonArray[i].hide()

    def showButtonArray(self, buttonArray):
        length = len(buttonArray)
        for i in range(length):
            buttonArray[i].show()

    def showInventoryGroupButtonArray(self, buttonArray, itemsPerGroup):
        length = len(buttonArray)
        for j in range(length):
            buttonArray[j].show()
            self.disableButton(buttonArray[j])
            inventory = localAvatar.getInventory()
            if inventory:
                for i in range(itemsPerGroup):
                    number = inventory.getStackQuantity(InventoryType.begin_Cards + j * itemsPerGroup + i)
                    if number > 0:
                        self.normalButton(buttonArray[j])
                        break

    def showInventoryButtonArray(self, buttonArray, cardStartIndex):
        length = len(buttonArray)
        for i in range(length):
            buttonArray[i].show()
            inventory = localAvatar.getInventory()
            if inventory:
                number = inventory.getStackQuantity(InventoryType.begin_Cards + cardStartIndex + i)
                if number > 0:
                    self.normalButton(buttonArray[i])
                else:
                    self.disableButton(buttonArray[i])
            else:
                self.disableButton(buttonArray[i])

    def cardIndexSelection(self, card):
        if card != PlayingCardGlobals.CheatHelp:
            self.cardSwapIndex = card
            self.cancelButton.show()
            self.hideButtonArray(self.rankButtonArray)
            self.hideActionButtons()
        self.accept('cardPicked', self.handleCardGuiMessage)
        messenger.send('guiMgrToggleInventory')
        localAvatar.guiMgr.inventoryBagPage.openContainer(localAvatar.guiMgr.inventoryBagPage.cardBag)
        self.accept('seachestClosed', self.cancelSelection)

    def handleCardGuiMessage(self, suit, rank):
        self.ignore('cardPicked')
        self.ignore('seachestClosed')
        self.cardSuitSelection(suit)
        self.cardRankSelection(rank)
        localAvatar.guiMgr.hideSeaChest()

    def cardSuitSelection(self, suit):
        self.suit = suit
        self.hideButtonArray(self.suitButtonArray)
        geom = self.suitGeomArray[suit]
        self.setRankButtonArrayGeoms(geom)
        self.cancelButton.show()
        self.hideActionButtons()
        self.moneyDisplay.hide()

    def cardRankSelection(self, rank):
        self.rank = rank
        card_id = self.suit * 13 + self.rank
        self.hideButtonArray(self.suitButtonArray)
        self.hideButtonArray(self.rankButtonArray)
        self.cancelButton.hide()
        self.table.card_id = card_id
        suit = card_id / 13
        rank = card_id % 13
        card = -1
        hand = self.table.getLocalAvatarHand()
        if hand:
            if self.cardSwapIndex == PlayingCardGlobals.Cheat1:
                if len(hand) >= 1:
                    card = hand[0]
            if self.cardSwapIndex == PlayingCardGlobals.Cheat2:
                if len(hand) >= 2:
                    card = hand[1]
            if self.cardSwapIndex == PlayingCardGlobals.Cheat7:
                if len(hand) >= 7:
                    card = hand[6]
        if card >= 0 and card < 52:
            original_suit = card / 13
            original_rank = card % 13
            string = PLocalizer.PokerSwapConfirmMessage % (PLocalizer.getPlayingCardName(original_suit, original_rank), PLocalizer.getPlayingCardName(suit, rank))
            self.swapDialog = PDialog.PDialog(text=string, style=OTPDialog.YesNo, giveMouse=False, command=self.swapCallback)
            self.table.setDialogBin(self.swapDialog)
            position = self.swapDialog.getPos()
            position.setZ(position[2] + 0.35)
            self.swapDialog.setPos(position)

    def swapCallback(self, value):
        if self.timeout == False:
            if self.destroyed:
                pass
            else:
                if value == 1:
                    self.table.guiCallback(self.cardSwapIndex)
                    self.swapCard = True
                self.showActionButtons()
        self.deleteSwapDialog()

    def hideCheatButtons(self):
        self.hideButtonArray(self.suitButtonArray)
        self.hideButtonArray(self.rankButtonArray)
        self.cancelButton.hide()

    def cancelSelection(self, value=None):
        self.ignore('cardPicked')
        self.ignore('seachestClosed')
        self.hideButtonArray(self.suitButtonArray)
        self.hideButtonArray(self.rankButtonArray)
        self.cancelButton.hide()
        self.showActionButtons()
        localAvatar.guiMgr.hideSeaChest()

    def leaveCallback(self, value):
        if value == 1:
            if self.destroyed:
                pass
            else:
                self.table.guiCallback(PlayingCardGlobals.Leave)
            self.deleteSwapDialog()
        self.deleteLeaveDialog()

    def deleteLeaveDialog(self):
        if self.leaveDialog:
            self.leaveDialog.destroy()
            del self.leaveDialog
            self.leaveDialog = None
        return

    def deleteSwapDialog(self):
        if self.swapDialog:
            self.swapDialog.destroy()
            del self.swapDialog
            self.swapDialog = None
        return

    def showActionButtons(self):
        pass

    def hideActionButtons(self):
        pass

    def startTimer(self, time):
        showMinutes = 0
        mode = None
        titleText = ''
        titleFg = None
        infoText = ''
        cancelText = ''
        cancelCallback = None
        timerExpiredCallback = self.timerExpiredCallback
        if self.use_hourglass:
            localAvatar.guiMgr.setHourglassTimer(time, showMinutes, mode, titleText, titleFg, infoText, cancelText, cancelCallback, timerExpiredCallback)
        else:
            localAvatar.guiMgr.setTimer(time, showMinutes, mode, titleText, titleFg, infoText, cancelText, cancelCallback, timerExpiredCallback, 1)
        self.timer = True
        self.timeout = False
        if self.use_hourglass:
            timer = localAvatar.guiMgr.timerHourglass
            timer.setPos(0.591146, 0, 0.127604)
            timer.reparentTo(base.a2dBottomCenter)
            start_time = 3.0
            end_time = 5.0
            start_position = Vec3(0.591146, 0, 0.127604 - 0.5)
            end_position = Vec3(0.591146, 0, 0.127604)
            timer.setSlide(start_time, end_time, start_position, end_position)
        else:
            timer = localAvatar.guiMgr.timer
            timer.setPos(0.591146, 0, 0.127604)
            timer.reparentTo(base.a2dBottomCenter)
            if True:
                start_time = 3.0
                end_time = 5.0
                start_position = Vec3(0.591146, 0, 0.127604 - 0.5)
                end_position = Vec3(0.591146, 0, 0.127604)
                timer.setSlide(start_time, end_time, start_position, end_position)
        return

    def endTimer(self):
        if self.timer:
            if self.use_hourglass:
                localAvatar.guiMgr.hourglassTimerExpired()
            else:
                localAvatar.guiMgr.timerExpired()
            self.timer = False

    def deleteText(self):
        if not self.levelUpIval:
            return
        if self.levelUpIval:
            self.levelUpIval.pause()
            self.levelUpIval = None
        self.levelUpLabel.destroy()
        self.levelUpCategoryLabel.destroy()
        self.levelUpText.removeNode()
        del self.levelUpSfx
        return

    def createText(self):
        if self.levelUpIval:
            return
        self.levelUpSfx = loadSfx(SoundGlobals.SFX_MINIGAME_LEVELUP)
        self.levelUpSfx.setVolume(0.5)
        self.levelUpText = NodePath('text')
        self.levelUpLabel = DirectLabel(parent=self.levelUpText, relief=None, text='', text_font=PiratesGlobals.getPirateOutlineFont(), text_fg=(0.1,
                                                                                                                                                 0.7,
                                                                                                                                                 0.1,
                                                                                                                                                 1), text_shadow=(0,
                                                                                                                                                                  0,
                                                                                                                                                                  0,
                                                                                                                                                                  1), scale=0.25)
        self.levelUpCategoryLabel = DirectLabel(parent=self.levelUpText, relief=None, text='', text_font=PiratesGlobals.getPirateOutlineFont(), text_fg=(0.1,
                                                                                                                                                         0.7,
                                                                                                                                                         0.1,
                                                                                                                                                         1), text_shadow=(0,
                                                                                                                                                                          0,
                                                                                                                                                                          0,
                                                                                                                                                                          1), scale=0.125, pos=(0, 0, -0.175))
        self.levelUpIval = Sequence(Func(self.levelUpText.reparentTo, aspect2d), Parallel(LerpPosInterval(self.levelUpText, 5, pos=Point3(0, 0, 0.3), startPos=Point3(0, 0, -0.3)), Sequence(LerpColorScaleInterval(self.levelUpText, 0.5, colorScale=VBase4(1, 1, 1, 1), startColorScale=VBase4(1, 1, 1, 0)), Wait(4), LerpColorScaleInterval(self.levelUpText, 0.5, colorScale=VBase4(1, 1, 1, 0), startColorScale=VBase4(1, 1, 1, 1)))), Func(self.levelUpText.detachNode))
        return

    def showText(self, title, text, color=None, amount=0):
        self.deleteText()
        self.createText()
        self.levelUpLabel['text'] = title
        if color == None:
            self.levelUpCategoryLabel['text_fg'] = (0.1, 0.7, 0.2, 1)
            self.levelUpLabel['text_fg'] = (0.1, 0.7, 0.1, 1)
        self.levelUpCategoryLabel['text'] = text
        self.levelUpIval.pause()
        self.levelUpIval.start()
        return

    def deleteButtonArray(self, buttonArray):
        length = len(buttonArray)
        for i in range(length):
            button = buttonArray[i]
            button.destroy()
            buttonArray[i] = None

        return

    def deleteTableGUI(self):
        self.deleteButtonArray(self.buttonArray)
        self.deleteButtonArray(self.suitButtonArray)
        self.deleteButtonArray(self.rankButtonArray)
        self.deleteLeaveDialog()
        self.deleteSwapDialog()
        self.deleteText()

    def showWinText(self, text, color=None, position=None):
        text_color = color
        if color == None:
            text_color = PiratesGuiGlobals.TextFG2
        base.localAvatar.guiMgr.createTitle(text, text_color)
        if position:
            base.localAvatar.guiMgr.titler.text.setPos(position)
        return

    def showSitDownText(self, text, color=None):
        text_color = color
        if color == None:
            text_color = PiratesGuiGlobals.TextFG2
        base.localAvatar.guiMgr.createTitle(text, text_color)
        return