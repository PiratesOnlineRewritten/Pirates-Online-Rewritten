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
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.GuiButton import GuiButton
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.quest.QuestTaskDNA import SkeletonPokerTaskDNA
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase

class PokerStatusPanel(DirectFrame):

    def __init__(self, maxHandCards):
        DirectFrame.__init__(self, parent=base.a2dBackground, relief=DGG.FLAT)
        self.initialiseoptions(PokerStatusPanel)
        self.arrow = loader.loadModel('models/gui/compass_arrow')
        self.arrow.reparentTo(self)
        self.arrow.setScale(0.25)
        self.arrow.setPosHpr(0, 0, 0.15, 0, 0, 180)
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
        self.dealerButton = loader.loadModel('models/gui/dealer_button')
        self.dealerButton.reparentTo(self)
        self.dealerButton.setPos(-0.12, 0, 0)
        self.dealerButton.setScale(0.08)
        self.dealerButton.hide()
        self.anteLabel = DirectLabel(parent=self.dealerButton, relief=None, text='', text_align=TextNode.ACenter, text_scale=0.8, pos=(0, 0, -0.3), text_fg=(0,
                                                                                                                                                             0,
                                                                                                                                                             0,
                                                                                                                                                             1))
        self.anteLabel.setColor(0, 0, 0, 1, 100)
        self.actionLabel.setTransparency(1)
        self.fadeActionLabel = Sequence(Func(self.actionLabel.show), LerpColorScaleInterval(self.actionLabel, 0.1, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0)), Wait(2.0), LerpColorScaleInterval(self.actionLabel, 1.0, Vec4(1, 1, 1, 0), Vec4(1, 1, 1, 1)), Func(self.actionLabel.hide))
        self.handId = PlayingCardGlobals.Nothing
        self.sortedCards = None
        return

    def destroy(self):
        self.ignoreAll()
        self.fadeActionLabel.pause()
        del self.fadeActionLabel
        DirectFrame.destroy(self)

    def displayAction(self, text, table, seat):
        name = ''
        actor = None
        if seat >= 0 and seat < len(table.actors):
            actor = table.actors[seat]
        if actor:
            name = actor.getName()
        if text == '':
            self.actionLabel['text'] = text
        else:
            self.actionLabel['text'] = name + '\n' + text
        self.fadeActionLabel.finish()
        self.fadeActionLabel.start()
        return


class PokerTellMeter(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self, relief=None)
        self.initialiseoptions(PokerTellMeter)
        return


class PokerTableGUI(DirectFrame, TableGUI):
    HandPos = (
     Vec3(0, 0, 0.4), Vec3(0.38, 0, 0.33), Vec3(0.65, 0, 0.1), Vec3(0.45, 0, -0.26), Vec3(0, 0, -0.3), Vec3(-0.45, 0, -0.26), Vec3(-0.65, 0, 0.1), Vec3(-0.38, 0, 0.33))
    LocalAvatarGuiIndex = 4

    def __init__(self, table, maxCommunityCards, maxHandCards):
        DirectFrame.__init__(self, parent=base.a2dBackground, relief=None)
        self.initialiseoptions(PokerTableGUI)
        self.maxCommunityCards = maxCommunityCards
        self.maxHandCards = maxHandCards
        self.maxBet = 0
        self.numberOfTimeouts = 0
        self.table = table
        self.destroyed = False
        self.playerActions = []
        width = 1.0
        self.menu = BorderFrame(parent=base.a2dBottomCenter, frameSize=(-width / 2.0, width / 2.0, 0, 0.25), pos=(0,
                                                                                                                  0,
                                                                                                                  0))
        self.disableReason = DirectLabel(parent=self.menu, text='', text_align=TextNode.ACenter, text_scale=0.04, pos=(0,
                                                                                                                       0,
                                                                                                                       0.175), text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1)
        self.disableReason.hide()
        self.initializeTableInterface()
        x = -0.36
        y = 0.1775
        x_increment = 0.24
        helpText = PLocalizer.TableCardsHelp
        helpPos = (0.0, 0.0, 0.24)
        text = PLocalizer.PokerCheat1
        button = GuiButton(parent=self.menu, command=self.cardIndexSelection, helpText=helpText, helpPos=helpPos, pos=(x, 0, y), canReposition=True)
        self.setButtonSettings2Lines(button, (x, 0, y), text, [PlayingCardGlobals.Cheat1])
        self.cheat1Button = button
        self.buttonArray = self.buttonArray + [button]
        x = x + x_increment
        text = PLocalizer.PokerCheat2
        button = GuiButton(parent=self.menu, command=self.cardIndexSelection, helpText=helpText, helpPos=helpPos, pos=(x, 0, y), canReposition=True)
        self.setButtonSettings2Lines(button, (x, 0, y), text, [PlayingCardGlobals.Cheat2])
        self.cheat2Button = button
        self.buttonArray = self.buttonArray + [button]
        x = x + x_increment
        text = PLocalizer.PokerCheck
        button = GuiButton(parent=self.menu, command=self.playerAction, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [PlayingCardGlobals.CheckCall])
        self.passButton = button
        self.buttonArray = self.buttonArray + [button]
        x = x + x_increment
        text = PLocalizer.PokerBet
        button = GuiButton(parent=self.menu, command=self.playerAction, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [PlayingCardGlobals.BetRaise])
        self.betButton = button
        self.buttonArray = self.buttonArray + [button]
        x = x + x_increment
        x = -0.36
        y = 0.07
        x_increment = 0.24
        x = x + x_increment
        x = x + x_increment
        x = x + x_increment
        text = PLocalizer.PokerFold
        button = GuiButton(parent=self.menu, command=self.playerAction, canReposition=True)
        self.setButtonSettings(button, (x, 0, y), text, [PlayingCardGlobals.Fold])
        self.foldButton = button
        self.buttonArray = self.buttonArray + [button]
        x = x + x_increment
        self.potSizeLabel = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ACenter, text_scale=0.05, pos=(-0.15, 0.0, 0.17), text_fg=(1,
                                                                                                                                                          0.9,
                                                                                                                                                          0.6,
                                                                                                                                                          1), text_shadow=(0,
                                                                                                                                                                           0,
                                                                                                                                                                           0,
                                                                                                                                                                           1))
        if table.wantMeter == 1:
            cardMaker = CardMaker('tellMeter')
            cardMaker.setFrame(-1, 1, -1, 1)
            self.meterMax = 0.2
            self.meterBorder = NodePath(cardMaker.generate())
            self.meterBorder.setColor(1, 1, 0, 1)
            self.meterBorder.setScale(0.2, 1, 0.02)
            self.meterBorder.reparentTo(aspect2d)
            self.meter = NodePath(cardMaker.generate())
            self.meter.setColor(1, 0, 0, 1)
            self.meter.setScale(0.2, 1, 0.05)
            self.meter.reparentTo(aspect2d)
        if table.wantMeter == 2:
            cardMaker = CardMaker('tellMeter')
            cardMaker.setFrame(-1, 1, -1, 1)
            self.balance = NodePath('Balance')
            self.balance.reparentTo(aspect2d)
            self.balanceL = NodePath(cardMaker.generate())
            self.balanceL.setColor(1, 0, 0, 1)
            self.balanceL.setScale(0.125, 1, 0.01)
            self.balanceL.setPos(-0.125, 0, 0)
            self.balanceL.reparentTo(self.balance)
            self.balanceR = NodePath(cardMaker.generate())
            self.balanceR.setColor(0, 1, 0, 1)
            self.balanceR.setScale(0.125, 1, 0.01)
            self.balanceR.setPos(0.125, 0, 0)
            self.balanceR.reparentTo(self.balance)
            self.fulcrum = loader.loadModel('models/props/winebottle_B')
            self.fulcrum.setScale(0.2)
            self.fulcrum.setZ(-0.21)
            self.fulcrum.reparentTo(aspect2d)
            self.weightR = NodePath(cardMaker.generate())
            self.weightR.setColor(0, 0, 1, 1)
            self.weightR.setScale(0.03, 1, 0.05)
            self.weightR.setPos(0.22, 0, 0.06)
            self.weightR.reparentTo(self.balance)
            self.weightL = NodePath(cardMaker.generate())
            self.weightL.setColor(0, 0, 1, 1)
            self.weightL.setScale(0.03, 1, 0.05)
            self.weightL.setPos(-0.22, 0, 0.06)
            self.weightL.reparentTo(self.balance)
            self.balance.hide()
            self.fulcrum.hide()
        self.communityCardNode = NodePath('communityCards')
        self.communityCardNode.reparentTo(self)
        self.communityCardNode.setScale(0.5)
        self.communityCardNode.setPos(0, 0, 0.04)
        self.communityCards = []
        for i in range(self.maxCommunityCards):
            card = PlayingCard.PlayingCardNodePath('standard', PlayingCardGlobals.Unknown)
            card.reparentTo(self.communityCardNode)
            card.setPos(i * 0.3 - 0.6, 0, 0)
            card.hide()
            self.communityCards.append(card)

        self.playerStatusPanels = []
        for i in range(self.table.NumSeats + 1):
            statusPanel = PokerStatusPanel(self.maxHandCards)
            statusPanel.setName('playerHand-%s' % i)
            pos = self.HandPos[i]
            statusPanel.setPos(pos)
            self.playerStatusPanels.append(statusPanel)

        self.localStatusPanel = self.playerStatusPanels[self.LocalAvatarGuiIndex]
        gui = loader.loadModel('models/gui/toplevel_gui')
        goldCoin = gui.find('**/treasure_w_coin*')
        scale = 0.32
        currentMoney = self.table.getPlayerChips()
        x_increment = 0.24
        self.moneyDisplay = DirectLabel(parent=self.menu, relief=None, pos=(-0.3 + x_increment, 0, 0.075), geom=goldCoin, geom_scale=(scale, scale, scale), geom_pos=(0,
                                                                                                                                                                      0,
                                                                                                                                                                      0), text='%s' % currentMoney, text_align=TextNode.ALeft, text_scale=0.04, text_pos=(0.05, -0.01), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, scale=1.1)
        self.accept(InventoryGlobals.getCategoryQuantChangeMsg(localAvatar.getInventoryId(), InventoryType.ItemTypeMoney), self.setMoney)
        this = self
        identifier = 0
        this.sfxArray = []
        this.shuffleIdentifier = identifier
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_SHUFFLE)]
        identifier += 1
        this.startDealIdentifier = identifier
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_DEAL_01)]
        identifier += 1
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_DEAL_02)]
        identifier += 1
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_DEAL_03)]
        identifier += 1
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_DEAL_04)]
        identifier += 1
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_DEAL_05)]
        identifier += 1
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_DEAL_06)]
        identifier += 1
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_DEAL_07)]
        identifier += 1
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_DEAL_08)]
        identifier += 1
        this.totalDealIdentifiers = identifier - this.startDealIdentifier
        this.foldIdentifier = identifier
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_FOLD)]
        identifier += 1
        this.flipIdentifier = identifier
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_FLIP)]
        identifier += 1
        this.pickupIdentifier = identifier
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_PICKUP)]
        identifier += 1
        this.checkIdentifier = identifier
        check = loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_CHECK)
        check.setVolume(0.5)
        this.sfxArray = this.sfxArray + [check]
        identifier += 1
        this.betIdentifier = identifier
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_CHIPS_BET)]
        identifier += 1
        this.collectIdentifier = identifier
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_CHIPS_COLLECT)]
        identifier += 1
        this.allInIdentifier = identifier
        this.sfxArray = this.sfxArray + [loadSfx(SoundGlobals.SFX_MINIGAME_CARDS_CHIPS_ALL)]
        identifier += 1
        return

    def showActionButtons(self):
        self.cheat1Button.show()
        self.cheat2Button.show()
        self.passButton.show()
        self.betButton.show()
        self.foldButton.show()
        self.leaveButton.show()
        self.moneyDisplay.show()
        self.disableReason.hide()

    def hideActionButtons(self):
        self.cheat1Button.hide()
        self.cheat2Button.hide()
        self.passButton.hide()
        self.betButton.hide()
        self.foldButton.hide()
        self.leaveButton.hide()

    def playerAction(self, action, allin_amount=0):
        self.numberOfTimeouts = 0
        base.localAvatar.delayAFK()
        self.table.guiCallback(action, allin_amount)

    def leaveAction(self, action, allin_amount=0):
        self.deleteLeaveDialog()

        def showLeaveDialog(displayText=None):
            self.leaveDialog = PDialog.PDialog(text=displayText or PLocalizer.PokerLeaveConfirmMessage, style=OTPDialog.YesNo, giveMouse=False, command=self.leaveCallback)
            self.table.setDialogBin(self.leaveDialog)

        if self.table.gameVariation == PiratesGlobals.PARLORGAME_VARIATION_UNDEAD:

            def gotInventory(inventory):
                text = None
                try:
                    for currQuest in inventory.getQuestList():
                        for currQuestTask, currQuestTaskState in zip(currQuest.getTasks(), currQuest.getTaskStates()):
                            if isinstance(currQuestTask, SkeletonPokerTaskDNA):
                                if currQuestTaskState.isComplete():
                                    if currQuestTaskState.isComplete(bonus=True):
                                        lostProgress = 0
                                    else:
                                        lostProgress = currQuestTaskState.getBonusProgress()
                                else:
                                    lostProgress = currQuestTaskState.getProgress()
                                loseAmt = min(PiratesGlobals.PARLORGAME_UNDEAD_EXIT_LOSS, lostProgress)
                                if loseAmt > 0:
                                    text = PLocalizer.PokerUndeadLeaveConfirmMessage % str(loseAmt)
                                    raise NameError('doneSearch')

                except NameError:
                    pass

                showLeaveDialog(text)
                return

            invReq = DistributedInventoryBase.getInventory(localAvatar.inventoryId, gotInventory)
        else:
            showLeaveDialog()
        return

    def timeoutAction(self, action):
        self.table.guiCallback(action)

    def setMoney(self, money):
        self.moneyDisplay['text'] = (
         '%s' % money,)
        self.table.displayStacks(self.table.localAvatarSeat, money)

    def showArrow(self, seatIndex):
        self.hideArrow()
        guiIndex = self.getGuiIndex(seatIndex)
        self.playerStatusPanels[guiIndex].arrow.show()
        self.playerStatusPanels[guiIndex].actionLabel.hide()

    def hideArrow(self):
        map(lambda panel: panel.arrow.hide(), self.playerStatusPanels)

    def setPlayerActions(self, maxBet, playerActions):
        oldActions = self.playerActions
        self.playerActions = playerActions
        oldMaxBet = self.maxBet
        self.maxBet = maxBet
        for i, oldAction, newAction in zip(range(len(playerActions)), oldActions, playerActions):
            if oldAction != newAction:
                action, amount = newAction
                panel = self.playerStatusPanels[self.getGuiIndex(i)]
                hand = panel.hand
                label = panel.actionLabel
                if action == PlayingCardGlobals.CheckCall:
                    if amount:
                        actionText = PLocalizer.PokerCall
                    else:
                        actionText = PLocalizer.PokerCheck
                elif action == PlayingCardGlobals.BetRaise:
                    if oldMaxBet == 0:
                        actionText = PLocalizer.PokerBetAmount % amount
                    else:
                        actionText = PLocalizer.PokerRaiseAmount % amount
                elif action == PlayingCardGlobals.Fold:
                    actionText = PLocalizer.PokerFold
                    for card in hand:
                        card.hide()

                    panel.handNameLabel.hide()
                    panel.arrow.hide()
                elif action == PlayingCardGlobals.NoAction:
                    actionText = ''
                    panel.actionLabel.hide()
                elif action == PlayingCardGlobals.SmallBlind:
                    amount = self.table.anteList[1]
                    actionText = PLocalizer.PokerSmallBlindAmount % amount
                elif action == PlayingCardGlobals.BigBlind:
                    amount = self.table.anteList[2]
                    actionText = PLocalizer.PokerBigBlindAmount % amount
                elif action == PlayingCardGlobals.Check:
                    actionText = PLocalizer.PokerCheck
                elif action == PlayingCardGlobals.AllIn:
                    actionText = PLocalizer.PokerAllIn
                else:
                    self.notify.error('Unknown action: %s' % action)
                panel.displayAction(actionText, self.table, i)

    def getGuiIndex(self, seatIndex):
        return (self.LocalAvatarGuiIndex - self.table.localAvatarSeat + seatIndex) % (self.table.NumSeats + 1)

    def clearTable(self):
        for panel in self.playerStatusPanels:
            for card in panel.hand:
                card.hide()

            panel.handNameLabel.hide()
            panel.actionLabel.hide()
            panel.dealerButton.hide()
            panel.anteLabel.hide()

        for i in range(len(self.communityCards)):
            card = self.communityCards[i]
            card.hide()

    def setTableState(self, round, buttonSeat, communityCardValues, playerHandValues, totalWinningsArray):
        self.clearTable()
        self.playerStatusPanels[self.getGuiIndex(buttonSeat)].anteLabel.show()
        self.playerStatusPanels[self.getGuiIndex(buttonSeat)].dealerButton.show()
        for i in range(len(self.communityCards)):
            card = self.communityCards[i]
            if i < len(communityCardValues):
                newValue = communityCardValues[i]
                card.show()
                card.setValue(newValue)
                if newValue != PlayingCardGlobals.Unknown:
                    card.turnUp()
            else:
                card.hide()
                card.setValue(PlayingCardGlobals.Unknown)

        for i in range(len(playerHandValues)):
            newHand = playerHandValues[i]
            guiIndex = self.getGuiIndex(i)
            panel = self.playerStatusPanels[guiIndex]
            hand = panel.hand
            handNameLabel = panel.handNameLabel
            allUnknown = 1
            for card, newValue in zip(hand, newHand):
                card.show()
                card.setValue(newValue)
                if newValue == PlayingCardGlobals.Unknown:
                    card.turnDown()
                else:
                    allUnknown = 0
                    card.turnUp()

            if allUnknown:
                panel.cardScaler.setScale(0.4)
            else:
                panel.cardScaler.setScale(0.5)
            if newHand and PlayingCardGlobals.Unknown not in newHand:
                if self.table.handIdArray:
                    seat = i
                    handId = self.table.handIdArray[seat]
                    if handId > PlayingCardGlobals.Nothing:
                        sortedHand = self.table.sortedCardsArray[seat]
                        handName = PLocalizer.getHandNameFull(self.table.handIdToHandCode(handId), sortedHand)
                        handNameLabel['text'] = handName
                        handNameLabel.show()

        end = False
        length = len(totalWinningsArray)
        for i in range(length):
            if totalWinningsArray[i] != 0:
                end = True
                break

        if end and self.table.endOfHand:
            for i in range(length):
                if totalWinningsArray[i] > 0:
                    actor = self.table.actors[i]
                    if actor:
                        name = actor.getName()
                        win = totalWinningsArray[i]
                        message = PLocalizer.PokerChatWinGoldMessage % (name, win)
                        base.talkAssistant.receiveGameMessage(message)
                if totalWinningsArray[i] == PlayingCardGlobals.PlayerCaughtCheating:
                    actor = self.table.actors[i]
                    if actor:
                        name = actor.getName()
                        message = PLocalizer.PokerChatCaughtCheatingMessage % name
                        base.talkAssistant.receiveGameMessage(message)

    def setLocalAvatarHand(self, cardValues):
        map(lambda card: card.hide(), self.localStatusPanel.hand)
        self.localStatusPanel.cardScaler.setScale(0.5)
        for card, newValue in zip(self.localStatusPanel.hand, cardValues):
            card.show()
            card.setValue(newValue)
            if newValue != PlayingCardGlobals.Unknown:
                card.turnUp()

        handNameLabel = self.localStatusPanel.handNameLabel
        communityCardValues = map(lambda card: card.getValue(), self.communityCards)
        if cardValues:
            if PlayingCardGlobals.Unknown not in cardValues and (self.handId == PlayingCardGlobals.Nothing or self.sortedCards == None):
                handNameLabel.hide()
            else:
                handName = PLocalizer.getHandNameFull(self.table.handIdToHandCode(self.handId), self.sortedCards)
                handNameLabel['text'] = handName
                handNameLabel.show()
        else:
            handNameLabel.hide()
        return

    def setPotSize(self, potSize):
        if potSize:
            self.potSizeLabel['text'] = PLocalizer.PokerPotAmount % potSize
        else:
            self.potSizeLabel['text'] = ''

    def enableActionCallback(self):
        pass

    def enableAction(self):
        chips = self.table.getPlayerChips()
        minimum = self.table.getMinimumBetAmount()
        if chips <= 0:
            self.table.allIn()
        else:
            self.cheat1Button.show()
            self.cheat2Button.show()
            self.passButton.show()
            self.betButton.show()
            self.foldButton.show()
            self.disableReason.hide()
            if self.table.checkCondition():
                self.passButton['text'] = PLocalizer.PokerCheck
                self.passButton['extraArgs'] = [PlayingCardGlobals.Check]
                if chips > minimum:
                    self.betButton['text'] = PLocalizer.PokerBetAmount % minimum
                    self.betButton['extraArgs'] = [PlayingCardGlobals.BetRaise]
                else:
                    self.betButton['text'] = PLocalizer.PokerAllInAmount % chips
                    self.betButton['extraArgs'] = [PlayingCardGlobals.AllIn, chips]
            else:
                callAmount = self.table.getCallAmount()
                raiseAmount = self.table.maxBet + minimum
                if chips > callAmount:
                    if callAmount == 0:
                        self.passButton['text'] = PLocalizer.PokerCheck
                        self.passButton['extraArgs'] = [PlayingCardGlobals.Check]
                    else:
                        self.passButton['text'] = PLocalizer.PokerCallAmount % callAmount
                        self.passButton['extraArgs'] = [PlayingCardGlobals.CheckCall]
                else:
                    self.passButton['text'] = PLocalizer.PokerAllInAmount % chips
                    self.passButton['extraArgs'] = [PlayingCardGlobals.AllIn, chips]
                    self.betButton.hide()
                if chips > callAmount + minimum:
                    self.betButton['text'] = PLocalizer.PokerRaiseAmount % raiseAmount
                    self.betButton['extraArgs'] = [PlayingCardGlobals.BetRaise]
                else:
                    self.betButton['text'] = PLocalizer.PokerAllInAmount % (callAmount + chips)
                    self.betButton['extraArgs'] = [PlayingCardGlobals.AllIn, chips]
            self.startTimer(PlayingCardGlobals.SecondsPerHand)

    def timeoutFold(self):
        self.hideActionButtons()
        self.hideCheatButtons()
        self.timeoutAction(PlayingCardGlobals.Fold)
        self.leaveButton.show()
        self.timeout = True
        self.deleteSwapDialog()

    def timeoutLeave(self):
        self.hideActionButtons()
        self.hideCheatButtons()
        self.timeoutAction(PlayingCardGlobals.Leave)
        self.timeout = True
        self.deleteSwapDialog()

    def timerExpiredCallback(self):
        self.numberOfTimeouts = self.numberOfTimeouts + 1
        if self.numberOfTimeouts >= PlayingCardGlobals.MaximumTimeouts:
            self.timeoutLeave()
        else:
            self.timeoutFold()
        self.endTimer()

    def enableCheat(self):
        have_cheat_card = False
        for card_id in range(52):
            if self.table.getPlayerInventoryCardCount(card_id) > 0:
                have_cheat_card = True
                break

        if have_cheat_card:
            self.normalButton(self.cheat1Button)
            self.normalButton(self.cheat2Button)
        else:
            self.disableCheat()

    def disableCheat(self):
        self.disableButton(self.cheat1Button)
        self.disableButton(self.cheat2Button)

    def disableAction(self, reason=None):
        self.cheat1Button.hide()
        self.cheat2Button.hide()
        self.passButton.hide()
        self.betButton.hide()
        self.foldButton.hide()
        if reason:
            self.disableReason['text'] = reason
            self.disableReason.show()
        else:
            self.disableReason.hide()
        self.endTimer()

    def destroy(self):
        self.endTimer()
        self.deleteTableGUI()
        self.potSizeLabel.destroy()
        self.menu.destroy()
        del self.menu
        self.communityCardNode.removeNode()
        del self.communityCardNode
        for card in self.communityCards:
            card.removeNode()

        del self.communityCards
        for panel in self.playerStatusPanels:
            panel.destroy()

        del self.playerStatusPanels
        del self.localStatusPanel
        if self.table.wantMeter == 1:
            self.meter.removeNode()
            del self.meter
            self.meterBorder.removeNode()
            del self.meterBorder
        if self.table.wantMeter == 2:
            self.fulcrum.removeNode()
            del self.fulcrum
            self.balance.removeNode()
            del self.balance
        this = self
        if this.sfxArray:
            length = len(this.sfxArray)
            for i in range(length):
                sfx = this.sfxArray[i]
                this.sfxArray[i] = None
                if sfx:
                    loader.unloadSfx(sfx)

        self.destroyed = True
        del self.table
        DirectFrame.destroy(self)
        return

    def getMeterPercent(self):
        return self.meter.getScale()[0] / self.meterMax * 100.0

    def setMeterPercent(self, percent):
        curScale = self.meter.getScale()
        self.meter.setScale(self.meterMax * (percent / 100.0), curScale[1], curScale[2])

    def getBalanceAngle(self):
        return self.balance.getR()

    def setBalanceAngle(self, angle):
        self.balance.setR(angle)