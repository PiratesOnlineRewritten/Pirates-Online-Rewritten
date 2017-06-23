from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task import Task
import random
import math
import DistributedGameTable
import PlayingCardGlobals
import PlayingCard
import BlackjackTableGUI
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PLocalizer
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from pirates.piratesgui import PiratesGuiGlobals

class DistributedBlackjackTable(DistributedGameTable.DistributedGameTable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackjackTable')

    def __init__(self, cr):
        DistributedGameTable.DistributedGameTable.__init__(self, cr)
        self.hasGui = 0
        self.maxCommunityCards = 0
        self.maxHandCards = 2
        self.hands = []
        self.allHands = []
        self.initialPlayerBid = 0
        self.cheat = False
        self.dialog = None
        self.swapResultDialog = None
        self.chipsCount = []
        self.radarState = None
        self.betMultiplier = 1
        return

    def generate(self):
        DistributedGameTable.DistributedGameTable.generate(self)
        self.setName(self.uniqueName('DistributedBlackjackTable'))

    def getInteractText(self):
        return PLocalizer.InteractTableBlackjack

    def getSitDownText(self):
        return PLocalizer.BlackjackSitDownBlackjack

    def disable(self):
        DistributedGameTable.DistributedGameTable.disable(self)

    def delete(self):
        self.deleteSwapResultDialog()
        DistributedGameTable.DistributedGameTable.delete(self)
        if self.hasGui:
            self.gui.destroy()
            del self.gui
            self.hasGui = 0

    def allHandsToCurrentHands(self, allHandsArray):
        hands = []
        length = len(allHandsArray)
        for i in range(length):
            handArray = allHandsArray[i]
            total_hands = len(handArray)
            if total_hands <= 1:
                hands = hands + handArray
            else:
                for j in range(total_hands):
                    k = total_hands - j - 1
                    if k == 0 or len(handArray[k]) >= 2:
                        hands = hands + [handArray[k]]
                        break

        return hands

    def setTableState(self, hands, chipsCount):
        self.chipsCount = chipsCount
        self.updateStacks(chipsCount)
        self.allHands = hands
        current_hands = self.allHandsToCurrentHands(hands)
        self.hands = current_hands
        if self.isLocalAvatarSeated():
            self.gui.setTableState(current_hands, hands)

    def setBetMultiplier(self, betMultiplier):
        self.betMultiplier = betMultiplier

    def setEvent(self, seatIndex, action):
        if self.isLocalAvatarSeated():
            self.gui.setEvent(seatIndex, action)
            if action[0] == PlayingCardGlobals.Bid:
                pass
            else:
                self.gui.showArrow(seatIndex)
        if seatIndex >= 0 and seatIndex < len(self.actors):
            actor = self.actors[seatIndex]
        else:
            actor = None
        if actor:
            if action[0] == PlayingCardGlobals.Stay:
                actor.play('cards_blackjack_stay')
            if action[0] == PlayingCardGlobals.Hit:
                actor.play('cards_blackjack_hit')
                if self.isLocalAvatarSeated():
                    sfx = None
                    audio = self.getAudio()
                    if audio:
                        sfx = audio.sfxArray[audio.hitIdentifier]
                    self.playSoundEffect(sfx)
        return

    def createGui(self):
        if not self.hasGui:
            self.gui = BlackjackTableGUI.BlackjackTableGUI(self)
            self.gui.setTableState(self.hands, self.allHands)
            self.radarState = localAvatar.guiMgr.radarGui.state
            localAvatar.guiMgr.radarGui.request('Off')
            localAvatar.guiMgr.gameGui.hide()
            self.hasGui = 1

    def satDown(self, seatIndex):
        self.createGui()
        self.cameraNode = NodePath('CameraNode')
        camera.reparentTo(self.cameraNode)
        self.cameraNode.setPosHpr(0, 0.75, 22, 0, -45, 0)
        camera.setHpr(0, 0, 0)
        camera.setPos(-self.sittingOffset, 4.9, -11)
        base.camLens.setMinFov(60)
        self.cameraNode.reparentTo(localAvatar)
        self.chips = 0
        self.chips = self.getPlayerChips()
        self.initialPlayerBid = 0
        text = self.getSitDownText()
        color = Vec4(1.0, 1.0, 1.0, 1.0)
        self.gui.showSitDownText(text, color)

    def gotUp(self, seatIndex):
        self.gui.destroy()
        del self.gui
        self.hasGui = 0
        if self.radarState:
            localAvatar.guiMgr.radarGui.request(self.radarState)
        localAvatar.guiMgr.gameGui.show()

    def requestClientAction(self, action):
        if action == PlayingCardGlobals.Bid:
            if self.isLocalAvatarSeated():
                self.initialPlayerBid = 0
                self.gui.setEvent(self.localAvatarSeat, [PlayingCardGlobals.AskForBid])
                self.gui.showArrow(self.localAvatarSeat)

    def d_clientAction(self, action):
        self.sendUpdate('clientAction', [action])

    def getPlayerBidAmount(self):
        amount = 0
        if self.getPlayerChips() >= self.getTableBidAmount():
            amount = self.getTableBidAmount()
        if self.gui:
            if self.getPlayerChips() >= self.gui.bidAmount:
                amount = self.gui.bidAmount
            else:
                amount = self.getPlayerChips()
        return amount

    def guiCallback(self, guiAction):
        if guiAction == PlayingCardGlobals.Bid:
            amount = self.getPlayerBidAmount()
            self.d_clientAction([guiAction, amount])
            self.initialPlayerBid = amount
            self.cheat = False
        elif guiAction == PlayingCardGlobals.Stay:
            self.d_clientAction([guiAction, 0])
        elif guiAction == PlayingCardGlobals.Hit:
            self.d_clientAction([guiAction, 0])
        elif guiAction == PlayingCardGlobals.Split:
            if self.initialPlayerBid > 0:
                amount = self.getPlayerBidAmount()
            else:
                amount = 0
            self.d_clientAction([guiAction, amount])
        elif guiAction == PlayingCardGlobals.DoubleDown:
            if self.initialPlayerBid > 0:
                amount = self.getPlayerBidAmount()
            else:
                amount = 0
            self.d_clientAction([guiAction, amount])
        elif guiAction == PlayingCardGlobals.Cheat1:
            self.requestingCheat(PlayingCardGlobals.ReplaceHoleCardOneCheat, self.card_id)
        elif guiAction == PlayingCardGlobals.Cheat2:
            self.requestingCheat(PlayingCardGlobals.ReplaceHoleCardTwoCheat, self.card_id)
        elif guiAction == PlayingCardGlobals.AutoStay:
            self.d_clientAction([guiAction, 0])
        elif guiAction == PlayingCardGlobals.Leave:
            self.requestExit()
        else:
            self.notify.error('guiCallback: unknown action: %s' % guiAction)

    def getAudio(self):
        audio = None
        if self.hasGui:
            audio = self.gui
        return audio

    def playSoundEffect(self, sfx):
        if sfx:
            base.playSfx(sfx)

    def getTableBidAmount(self):
        return PlayingCardGlobals.BlackjackBidAmount * self.betMultiplier

    def getPlayerChips(self):
        inventory = localAvatar.getInventory()
        if inventory:
            self.chips = inventory.getGoldInPocket()
        return self.chips

    def getPlayerInventoryCardCount(self, card_id):
        inventory = localAvatar.getInventory()
        if inventory:
            amount = inventory.getStackQuantity(InventoryType.begin_Cards + card_id)
        else:
            amount = 0
        return amount

    def getLocalAvatarHand(self):
        return self.hands[self.localAvatarSeat]

    def requestingCheat(self, cheatType, cheatTarget):
        self.currentCheatType = cheatType
        self.currentCheatTarget = cheatTarget
        self.sendUpdate('requestCheat', [cheatType, cheatTarget])
        self.cheat = True

    def setLocalAvatarHand(self, hand):
        self.hands[self.localAvatarSeat] = hand
        current_hand_index = self.getCurrentHandIndex(self.localAvatarSeat, self.allHands)
        self.allHands[self.localAvatarSeat][current_hand_index] = hand

    def deleteSwapResultDialog(self):
        if self.swapResultDialog:
            self.swapResultDialog.destroy()
            del self.swapResultDialog
            self.swapResultDialog = None
        return

    def swapResultCallback(self, value):
        self.deleteSwapResultDialog()

    def deleteDialogs(self):
        if self.dialog:
            self.dialog.destroy()
            del self.dialog
            self.dialog = None
        return

    def dialogCallback(self, value):
        self.deleteDialogs()

    def delayedPlayerLeave(self, task=None):
        self.deleteDialogs()

    def cheatResponse(self, cheatType, cheatTarget, success, hand):
        swap = False
        if cheatType == PlayingCardGlobals.ReplaceHoleCardOneCheat:
            self.setLocalAvatarHand(hand)
            swap = True
        elif cheatType == PlayingCardGlobals.ReplaceHoleCardTwoCheat:
            self.setLocalAvatarHand(hand)
            swap = True
        elif cheatType == PlayingCardGlobals.CaughtCheating:
            self.guiCallback(PlayingCardGlobals.Leave)
            self.deleteDialogs()
            string = PLocalizer.PokerCaughtCheatingMessage % PlayingCardGlobals.CheatingFine
            self.dialog = PDialog.PDialog(text=string, style=OTPDialog.Acknowledge, command=self.dialogCallback)
            self.setDialogBin(self.dialog)
        if self.gui and swap:
            if success:
                string = PLocalizer.PokerSwapSuccessMessage
            else:
                string = PLocalizer.PokerSwapFailureMessage
            self.swapResultDialog = PDialog.PDialog(text=string, style=OTPDialog.Acknowledge, giveMouse=False, command=self.swapResultCallback)
            self.setDialogBin(self.swapResultDialog)
            position = self.swapResultDialog.getPos()
            position.setZ(position[2] + 0.35)
            self.swapResultDialog.setPos(position)
            self.gui.updateSplitAndDoubleDown(hand)
            self.gui.updatePlayButtions()
            self.setTableState(self.allHands, self.chipsCount)
            value = PlayingCardGlobals.getBlackjackHandValue(hand)
            if value >= 21:
                self.gui.disableAllPlayButtons()
                self.gui.endTimer()
                self.guiCallback(PlayingCardGlobals.AutoStay)
            if self.isLocalAvatarSeated() and self.isLocalAvatarPlaying():
                actor = self.actors[self.localAvatarSeat]
                if actor:
                    actor.play('cards_cheat')

    def getPlayerReputation(self, avId):
        reputation = 0
        inventory = localAvatar.getInventory()
        if inventory:
            reputation = inventory.getStackQuantity(InventoryType.BlackjackGame)
        return reputation

    def getCurrentHandIndex(self, seat, allHands):
        current_hand_index = 0
        handArray = allHands[seat]
        total_hands = len(handArray)
        if total_hands > 1:
            current_hand_index = 0
            for j in range(total_hands):
                k = total_hands - j - 1
                if k == 0 or len(handArray[k]) >= 2:
                    current_hand_index = k
                    break

        return current_hand_index

    def setHandResults(self, results):
        if self.isLocalAvatarSeated():
            length = len(results)
            for i in range(length):
                if results[i] > 0:
                    actor = self.actors[i]
                    if actor:
                        name = actor.getName()
                        win = results[i]
                        if i == self.localAvatarSeat:
                            text = PLocalizer.TableWinGold % win
                            color = Vec4(1.0, 1.0, 1.0, 1.0)
                            color = Vec4(0.2, 0.8, 0.2, 1.0)
                            self.gui.showWinText(text, color)
                else:
                    actor = self.actors[i]
                    if actor:
                        if i == self.localAvatarSeat:
                            if self.gui.bid:
                                text = PLocalizer.BlackjackDealerWins
                                color = Vec4(0.7, 0.7, 0.7, 1.0)
                                color = Vec4(0.2, 0.2, 0.8, 1.0)
                                self.gui.showWinText(text, color)
                if results[i] == PlayingCardGlobals.PlayerCaughtCheating:
                    actor = self.actors[i]
                    if actor:
                        name = actor.getName()
                        message = PLocalizer.PokerChatCaughtCheatingMessage % name
                        base.talkAssistant.receiveGameMessage(message)