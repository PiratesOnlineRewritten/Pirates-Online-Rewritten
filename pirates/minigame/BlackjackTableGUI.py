from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pirates.minigame.TableGUI import TableGUI
from pirates.minigame import PlayingCardGlobals
from pirates.minigame import PlayingCard
from pirates.piratesgui import GuiTray
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import InventoryGlobals
from pirates.piratesgui.GuiButton import GuiButton
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class SplitBase():

    def deleteSplitDisplay(self, node):
        if node:
            for card in node.cardArray:
                card.detachNode()

            for label in node.labelArray:
                label.detachNode()
                label.destroy()

            node.cardArray = []
            node.labelArray = []


class BlackjackStatusPanel(DirectFrame, SplitBase):

    def __init__(self, maxHandCards):
        DirectFrame.__init__(self, parent=base.a2dBackground, relief=DGG.FLAT)
        self.initialiseoptions(BlackjackStatusPanel)
        self.arrow = loader.loadModel('models/gui/compass_arrow')
        self.arrow.reparentTo(self)
        self.arrow.setScale(0.25)
        self.arrow.setPosHpr(0, 0, 0.26, 0, 0, 180)
        self.arrow.hide()
        self.hand = []
        self.cardScaler = self.attachNewNode('cardScaler')
        self.cardScaler.setScale(0.5)
        for i in range(maxHandCards):
            left = 0.06 * maxHandCards * 0.5
            card = PlayingCard.PlayingCardNodePath('standard', PlayingCardGlobals.Unknown)
            card.reparentTo(self.cardScaler)
            card.setPos(i * 0.06 - left, 0, 0)
            card.hide()
            self.hand.append(card)

        self.actionLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ACenter, text_scale=0.04, pos=(0,
                                                                                                                             0,
                                                                                                                             0.15), text_fg=(1,
                                                                                                                                             1,
                                                                                                                                             1,
                                                                                                                                             1), text_shadow=(0,
                                                                                                                                                              0,
                                                                                                                                                              0,
                                                                                                                                                              1))
        self.handNameLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ACenter, text_scale=0.04, pos=(0, 0, -0.13), text_fg=(1,
                                                                                                                                                      1,
                                                                                                                                                      1,
                                                                                                                                                      1), text_shadow=(0,
                                                                                                                                                                       0,
                                                                                                                                                                       0,
                                                                                                                                                                       1))
        self.splitLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ACenter, text_scale=0.04, pos=(0, 0, -0.17), text_fg=(1,
                                                                                                                                                   1,
                                                                                                                                                   1,
                                                                                                                                                   1), text_shadow=(0,
                                                                                                                                                                    0,
                                                                                                                                                                    0,
                                                                                                                                                                    1))
        self.handsLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ACenter, text_scale=0.04, pos=(0, 0, -0.21), text_fg=(1,
                                                                                                                                                   1,
                                                                                                                                                   1,
                                                                                                                                                   1), text_shadow=(0,
                                                                                                                                                                    0,
                                                                                                                                                                    0,
                                                                                                                                                                    1))
        self.handsLabel.cardArray = []
        self.handsLabel.labelArray = []
        self.actionLabel.setTransparency(1)
        self.fadeActionLabel = Sequence(Func(self.actionLabel.show), LerpColorScaleInterval(self.actionLabel, 0.1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0)), Wait(3.0), LerpColorScaleInterval(self.actionLabel, 0.5, Vec4(1, 1, 1, 0), Vec4(1, 1, 1, 1)), Func(self.actionLabel.hide))
        return

    def destroy(self):
        self.deleteSplitDisplay(self.handsLabel)
        self.fadeActionLabel.pause()
        del self.fadeActionLabel
        DirectFrame.destroy(self)

    def displayAction(self, text, table, seat):
        name = ''
        actor = None
        if seat >= 0 and seat < len(table.actors):
            actor = table.actors[seat]
        else:
            actor = table.dealer
        if actor:
            name = actor.getName()
        if text == '':
            self.actionLabel['text'] = text
        else:
            self.actionLabel['text'] = name + '\n' + text
        self.fadeActionLabel.finish()
        self.fadeActionLabel.start()
        return


class BlackjackTableGUI(DirectFrame, TableGUI, SplitBase):
    HandPos = (
     Vec3(0, 0, 0.4), Vec3(0.38, 0, 0.33), Vec3(0.65, 0, 0.1), Vec3(0.45, 0, -0.26), Vec3(0, 0, -0.3), Vec3(-0.45, 0, -0.26), Vec3(-0.65, 0, 0.1), Vec3(-0.38, 0, 0.33))
    LocalAvatarGuiIndex = 4

    def sliderValueToBid(self, value):
        bid = int(value * self.table.betMultiplier * 50)
        bid = bid / 5
        bid = bid * 5
        if bid < 2:
            bid = 2
        return bid

    def x_to_gui_coordinate(self, x):
        return x * self.width

    def y_to_gui_coordinate(self, y):
        return self.height - y * self.height

    def create_slider(self, update_function, default_value, x, y, resolution, label, parent):
        slider_x = self.x_to_gui_coordinate(x)
        slider_y = self.y_to_gui_coordinate(y)

        def update_slider(slider, update_function):
            string = slider.label + '  (%d)' % self.sliderValueToBid(slider['value'])
            slider['text'] = string
            update_function(slider['value'])

        charGui = loader.loadModel('models/gui/char_gui')
        slider = DirectSlider(parent=parent, relief=None, command=update_slider, image=charGui.find('**/chargui_slider_small'), image_scale=(2.15,
                                                                                                                                             2.15,
                                                                                                                                             1.5), thumb_relief=None, thumb_image=(charGui.find('**/chargui_slider_node'), charGui.find('**/chargui_slider_node_down'), charGui.find('**/chargui_slider_node_over')), pos=(slider_x, 0.0, slider_y), text_align=TextNode.ACenter, text_scale=(0.1,
                                                                                                                                                                                                                                                                                                                                                                                              0.1), text_pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                                                                              0.1), text_fg=PiratesGuiGlobals.TextFG1, scale=0.43, pageSize=resolution, text='default', value=default_value)
        charGui.removeNode()
        slider.label = label
        slider['extraArgs'] = [slider, update_function]
        return slider

    def __init__(self, table):
        DirectFrame.__init__(self, relief=None)
        self.initialiseoptions(BlackjackTableGUI)
        self.table = table
        self.destroyed = False
        self.maxHandCards = 14
        self.playerStatusPanels = []
        for i in range(self.table.NumSeats + 1):
            statusPanel = BlackjackStatusPanel(self.maxHandCards)
            statusPanel.setName('playerHand-%s' % i)
            pos = self.HandPos[i]
            statusPanel.setPos(pos)
            self.playerStatusPanels.append(statusPanel)

        self.localStatusPanel = self.playerStatusPanels[self.LocalAvatarGuiIndex]
        width = 1.0
        height = 0.25
        self.menu = BorderFrame(parent=base.a2dBottomCenter, frameSize=(-width / 2.0, width / 2.0, 0, height), pos=(0,
                                                                                                                    0,
                                                                                                                    0))
        self.width = width
        self.height = height
        self.initializeTableInterface()
        x = -0.36
        y = 0.1775
        x_increment = 0.24
        helpText = PLocalizer.TableCardsHelp
        helpPos = (0.0, 0.0, 0.24)
        text = PLocalizer.BlackjackCardSwap
        button = GuiButton(parent=self.menu, command=self.playerAction, helpText=helpText, helpPos=helpPos, pos=(x, 0, y), canReposition=True)
        self.setButtonSettings2Lines(button, (x, 0, y), text, [PlayingCardGlobals.CardSwap])
        button.show()
        self.cardSwapButton = button
        self.buttonArray = self.buttonArray + [button]
        x += x_increment
        text = PLocalizer.BlackjackDoubleDown
        button = GuiButton(parent=self.menu, command=self.playerAction, canReposition=True)
        self.setButtonSettings2Lines(button, (x, 0, y), text, [PlayingCardGlobals.DoubleDown])
        button.show()
        self.doubleDownButton = button
        self.buttonArray = self.buttonArray + [button]
        x += x_increment
        text = PLocalizer.BlackjackStay
        button = GuiButton(parent=self.menu, command=self.playerAction, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [PlayingCardGlobals.Stay])
        button.show()
        self.stayButton = button
        self.buttonArray = self.buttonArray + [button]
        x += x_increment
        text = PLocalizer.BlackjackHit
        button = GuiButton(parent=self.menu, command=self.playerAction, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [PlayingCardGlobals.Hit])
        button.show()
        self.hitButton = button
        self.buttonArray = self.buttonArray + [button]
        x += x_increment
        x = -0.36
        y = 0.07
        x_increment = 0.24
        x += x_increment
        x += x_increment
        text = PLocalizer.BlackjackSplit
        button = GuiButton(parent=self.menu, command=self.playerAction, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [PlayingCardGlobals.Split])
        button.show()
        self.splitButton = button
        self.buttonArray = self.buttonArray + [button]
        x += x_increment
        bid = self.table.getTableBidAmount()
        text = PLocalizer.BlackjackBid + ' ' + bid.__repr__()
        button = GuiButton(parent=self.menu, command=self.playerAction, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [PlayingCardGlobals.Bid])
        button.show()
        self.bidButton = button
        self.buttonArray = self.buttonArray + [button]
        x += x_increment

        def bid_update_function(value):
            bid = self.sliderValueToBid(value)
            text = PLocalizer.BlackjackBid + ' ' + bid.__repr__()
            self.bidButton['text'] = text
            self.bidAmount = bid

        self.bidAmount = 2
        default_value = 0.0
        x = 0.0
        y = -0.25
        label = PLocalizer.BlackjackBid
        resolution = 1.0
        self.bidSlider = self.create_slider(bid_update_function, default_value, x, y, resolution, label, self.menu)
        x = -0.36
        y = 0.1775
        x_increment = 0.24
        text = PLocalizer.PokerCheat1
        button = GuiButton(parent=self.menu, command=self.cardSwapButtonSelection, canReposition=True)
        self.setButtonSettings2Lines(button, (x, 0, y), text, [PlayingCardGlobals.Cheat1])
        self.cheat1Button = button
        self.buttonArray = self.buttonArray + [button]
        x = x + x_increment
        text = PLocalizer.PokerCheat2
        button = GuiButton(parent=self.menu, command=self.cardSwapButtonSelection, canReposition=True)
        self.setButtonSettings2Lines(button, (x, 0, y), text, [PlayingCardGlobals.Cheat2])
        self.cheat2Button = button
        self.buttonArray = self.buttonArray + [button]
        x = x + x_increment
        self.hideCheatButtons()
        self.disableAllPlayButtons()
        gui = loader.loadModel('models/gui/toplevel_gui')
        goldCoin = gui.find('**/treasure_w_coin*')
        scale = 0.32
        currentMoney = localAvatar.getInventory().getGoldInPocket()
        self.moneyDisplay = DirectLabel(parent=self.menu, relief=None, pos=(-0.3 + x_increment / 2.0, 0, 0.075), geom=goldCoin, geom_scale=(scale, scale, scale), geom_pos=(0,
                                                                                                                                                                            0,
                                                                                                                                                                            0), text='%s' % currentMoney, text_align=TextNode.ALeft, text_scale=0.035, text_pos=(0.045, -0.01), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, scale=1.1)
        self.accept(InventoryGlobals.getCategoryQuantChangeMsg(localAvatar.getInventoryId(), InventoryType.ItemTypeMoney), self.setMoney)
        this = self
        identifier = 0
        this.sfxArray = []
        this.hitIdentifier = identifier
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_HIT)]
        identifier = identifier + 1
        self.hands = []
        self.splitCardsArray = []
        self.canSplit = False
        self.canDoubleDown = False
        self.bid = False
        return

    def cardSwapButtonSelection(self, card):
        self.cheat1Button.hide()
        self.cheat2Button.hide()
        self.cardIndexSelection(card)

    def startCardIndexSelection(self):
        self.cheat1Button.show()
        self.cheat2Button.show()
        self.cancelButton.show()
        self.hideActionButtons()

    def playerAction(self, action):
        base.localAvatar.delayAFK()
        if action == PlayingCardGlobals.CardSwap:
            self.startCardIndexSelection()
        else:
            self.table.guiCallback(action)
            self.endTimer()
            self.disableAllPlayButtons()
            if action == PlayingCardGlobals.Split:
                length = len(self.hands)
                if length > 0 and self.table.localAvatarSeat > 0 and self.table.localAvatarSeat < length:
                    hand = self.hands[self.table.localAvatarSeat]
                    if hand and len(hand) == 2:
                        self.splitCardsArray.append(hand[1])

    def setMoney(self, money):
        self.moneyDisplay['text'] = '%s' % money
        self.table.displayStacks(self.table.localAvatarSeat, money)

    def showArrow(self, seatIndex):
        self.hideArrow()
        guiIndex = self.getGuiIndex(seatIndex)
        self.playerStatusPanels[guiIndex].arrow.show()
        self.playerStatusPanels[guiIndex].actionLabel.hide()

    def hideArrow(self):
        map(lambda panel: panel.arrow.hide(), self.playerStatusPanels)

    def getGuiIndex(self, seatIndex):
        return (self.LocalAvatarGuiIndex - self.table.localAvatarSeat + seatIndex) % (self.table.NumSeats + 1)

    def setTableState(self, hands, allHands):
        for panel in self.playerStatusPanels:
            for card in panel.hand:
                card.hide()

            panel.handNameLabel.hide()
            panel.splitLabel.hide()
            panel.handsLabel.hide()

        self.hands = hands
        for i in range(len(hands)):
            newHand = hands[i]
            guiIndex = self.getGuiIndex(i)
            panel = self.playerStatusPanels[guiIndex]
            hand = panel.hand
            handNameLabel = panel.handNameLabel
            splitLabel = panel.splitLabel
            handsLabel = panel.handsLabel
            for card, newValue in zip(hand, newHand):
                card.show()
                card.setValue(newValue)
                if newValue == PlayingCardGlobals.Unknown:
                    card.turnDown()
                else:
                    card.turnUp()

            self.centerCards(panel, newHand)
            if newHand and PlayingCardGlobals.Unknown not in newHand:
                handValue = PlayingCardGlobals.getBlackjackHandValue(newHand)
                if handValue == 21 and len(newHand) == 2:
                    handArray = allHands[i]
                    total_hands = len(handArray)
                    if total_hands <= 1:
                        handNameLabel['text'] = PLocalizer.BlackjackHand
                    else:
                        handNameLabel['text'] = str(handValue)
                elif handValue > 21:
                    handNameLabel['text'] = PLocalizer.BlackjackBusted % handValue
                else:
                    handNameLabel['text'] = str(handValue)
                handNameLabel.show()
                if i == self.table.localAvatarSeat:
                    handArray = allHands[i]
                    total_hands = len(handArray)
                    if total_hands > 1:
                        current_hand_index = self.table.getCurrentHandIndex(i, allHands)
                        splitLabel['text'] = PLocalizer.BlackjackHandofHand % (current_hand_index + 1, total_hands)
                        splitLabel.show()
                        hands_text = ''
                        for h in range(current_hand_index):
                            hands_text = hands_text + str(PlayingCardGlobals.getBlackjackHandValue(handArray[h])) + '   '

                        handsLabel.show()
                        self.createSplitDisplay(i, allHands, handsLabel)
                    self.canSplit = False
                    self.canDoubleDown = False
                    if newHand[0] in self.splitCardsArray:
                        self.splitCardsArray.remove(newHand[0])
                    if handValue >= 21:
                        self.disableAllPlayButtons()
                    else:
                        self.updateSplitAndDoubleDown(newHand)

    def updateSplitAndDoubleDown(self, hand):
        self.canSplit = False
        self.canDoubleDown = False
        length = len(hand)
        if length == 2:
            if self.table.getPlayerChips() >= self.bidAmount:
                self.canDoubleDown = True
                if self.splitableHand(hand[0], hand[1]):
                    self.canSplit = True

    def updatePlayButtions(self):
        self.disableAllPlayButtons()
        if self.canDoubleDown:
            self.normalButton(self.doubleDownButton)
        self.normalButton(self.stayButton)
        self.normalButton(self.hitButton)
        if self.canSplit:
            self.normalButton(self.splitButton)
        have_cheat_card = False
        if self.swapCard == False:
            for card_id in range(52):
                if self.table.getPlayerInventoryCardCount(card_id) > 0:
                    have_cheat_card = True
                    break

        if have_cheat_card:
            self.normalButton(self.cardSwapButton)
        else:
            self.disableButton(self.cardSwapButton)

    def setEvent(self, seatIndex, action):
        guiIndex = self.getGuiIndex(seatIndex)
        panel = self.playerStatusPanels[guiIndex]
        actionText = PlayingCardGlobals.getBlackjackActionText(action)
        if len(action) >= 2:
            if action[0] == PlayingCardGlobals.Bid and action[1] == 0:
                actionText = ' '
            if seatIndex == self.table.localAvatarSeat:
                if action[0] == PlayingCardGlobals.Bid:
                    if action[1] == 0:
                        self.bid = False
                    else:
                        self.bid = True
        panel.displayAction(actionText, self.table, seatIndex)
        if seatIndex == self.table.localAvatarSeat:
            time = 0.0
            if action[0] == PlayingCardGlobals.AskForBid:
                time = PlayingCardGlobals.BidTimeout
                self.disableAllPlayButtons()
                self.normalButton(self.bidButton)
                self.bidSlider.show()
                self.splitCardsArray = []
                self.swapCard = False
                self.bid = False
            if action[0] == PlayingCardGlobals.AskCard:
                time = PlayingCardGlobals.AskCardTimeout
                self.updatePlayButtions()
            if action[0] == PlayingCardGlobals.Stay:
                self.disableAllPlayButtons()
            if action[0] == PlayingCardGlobals.DoubleDown:
                self.disableAllPlayButtons()
            if action[0] == PlayingCardGlobals.Split:
                time = PlayingCardGlobals.AskCardTimeout
                self.disableAllPlayButtons()
            if time > 0.0:
                self.startTimer(time)

    def disableAllPlayButtons(self):
        self.disableButton(self.splitButton)
        self.disableButton(self.doubleDownButton)
        self.disableButton(self.stayButton)
        self.disableButton(self.hitButton)
        self.disableButton(self.bidButton)
        self.bidSlider.hide()
        self.disableButton(self.cardSwapButton)

    def destroy(self):
        self.endTimer()
        self.deleteTableGUI()
        del self.bidSlider
        self.menu.destroy()
        del self.menu
        for panel in self.playerStatusPanels:
            panel.destroy()

        del self.playerStatusPanels
        del self.localStatusPanel
        self.destroyed = True
        del self.table
        DirectFrame.destroy(self)
        this = self
        if this.sfxArray:
            length = len(this.sfxArray)
            for i in range(length):
                sfx = this.sfxArray[i]
                this.sfxArray[i] = None
                if sfx:
                    loader.unloadSfx(sfx)

        return

    def leaveAction(self, action):
        self.deleteLeaveDialog()
        self.leaveDialog = PDialog.PDialog(text=PLocalizer.PokerLeaveConfirmMessage, style=OTPDialog.YesNo, giveMouse=False, command=self.leaveCallback)
        self.table.setDialogBin(self.leaveDialog)

    def timerExpiredCallback(self):
        self.disableAllPlayButtons()
        self.showActionButtons()
        self.hideCheatButtons()
        self.leaveButton.show()
        self.cheat1Button.hide()
        self.cheat2Button.hide()
        self.endTimer()
        self.deleteSwapDialog()

    def splitableHand(self, card1, card2):
        state = False
        rank1 = card1 % 13
        rank2 = card2 % 13
        if rank1 == rank2:
            state = True
        elif rank1 >= 8 and rank1 <= 11 and rank2 >= 8 and rank2 <= 11:
            state = True
        return state

    def showActionButtons(self):
        self.splitButton.show()
        self.doubleDownButton.show()
        self.stayButton.show()
        self.hitButton.show()
        self.bidButton.show()
        if self.cardSwapButton:
            self.cardSwapButton.show()
        self.leaveButton.show()
        self.moneyDisplay.show()

    def hideActionButtons(self):
        self.splitButton.hide()
        self.doubleDownButton.hide()
        self.stayButton.hide()
        self.hitButton.hide()
        self.bidButton.hide()
        self.bidSlider.hide()
        if self.cardSwapButton:
            self.cardSwapButton.hide()
        self.leaveButton.hide()
        self.moneyDisplay.show()

    def cancelSelection(self, value=None):
        self.hideButtonArray(self.suitButtonArray)
        self.hideButtonArray(self.rankButtonArray)
        self.cancelButton.hide()
        self.showActionButtons()
        self.cheat1Button.hide()
        self.cheat2Button.hide()

    def createSplitDisplay(self, seat, allHands, parent):
        self.deleteSplitDisplay(parent)
        handArray = allHands[seat]
        total_hands = len(handArray)
        if total_hands > 1:
            current_hand_index = self.table.getCurrentHandIndex(seat, allHands)
            x_increment = 0.24
            x_size = (total_hands - 1) * x_increment
            x = -x_size * 0.5
            y = -0.16
            card_y = -0.05
            for h in range(total_hands):
                hand = handArray[h]
                value = PlayingCardGlobals.getBlackjackHandValue(hand)
                scale = 0.375
                length = len(hand)
                card_x_increment = 0.06
                left = card_x_increment * scale * length * -0.5
                for i in range(length):
                    card = PlayingCard.PlayingCardNodePath('standard', PlayingCardGlobals.Unknown)
                    card.reparentTo(parent)
                    card.setPos(x + left + i * (card_x_increment * scale), 0, card_y)
                    card.setScale(scale)
                    card.setValue(hand[i])
                    card.turnUp()
                    card.show()
                    parent.cardArray.append(card)
                    if h == current_hand_index:
                        color = 1.0
                        card.setColor(color, color, color, 1.0)
                    else:
                        color = 0.6
                        card.setColor(color, color, color, 1.0)

                label = DirectLabel(parent=parent, relief=None, text='', text_align=TextNode.ACenter, text_scale=0.04, pos=(x, 0.0, y), text_fg=(1,
                                                                                                                                                 1,
                                                                                                                                                 1,
                                                                                                                                                 1), text_shadow=(0,
                                                                                                                                                                  0,
                                                                                                                                                                  0,
                                                                                                                                                                  1))
                label['text'] = str(value)
                label.show()
                parent.labelArray.append(label)
                x += x_increment

        return

    def centerCards(self, panel, hand):
        x_increment = 0.06
        length = len(hand)
        left = x_increment * length * -0.5
        for i in range(length):
            card = panel.hand[i]
            card.setPos(left + i * x_increment, 0, 0)