from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task import Task
import random
import math
from pirates.minigame import DistributedGameTable
from pirates.minigame import PlayingCardGlobals
from pirates.minigame import PlayingCard
from pirates.minigame import PokerTableGUI
from pirates.minigame import PokerBase
from pirates.piratesbase import PLocalizer
from otp.otpgui import OTPDialog
from pirates.piratesgui import PDialog
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.interact.InteractiveBase import END_INTERACT_EVENT
from pirates.audio import SoundGlobals

class DistributedPokerTable(DistributedGameTable.DistributedGameTable, PokerBase.PokerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPokerTable')

    def __init__(self, cr, evaluatorGame, numRounds):
        DistributedGameTable.DistributedGameTable.__init__(self, cr)
        self.round = 0
        self.numRounds = numRounds
        self.buttonSeat = 0
        self.communityCards = []
        self.playerHands = []
        self.potSize = 0
        self.maxBet = 0
        self.playerActions = []
        self.localAvatarHand = []
        self.evaluatorGame = evaluatorGame
        self.wantMeter = 0
        self.getReady = 1
        self.hasGui = 0
        self.radarState = None
        self.currentCheatType = -1
        self.currentCheatTarget = -1
        self.excitement = 0
        self.excitementT = 0
        self.handValue = 0
        self.balanceT = 0
        self.chips = 0
        self.handId = PlayingCardGlobals.Nothing
        self.sortedCards = None
        self.handIdArray = None
        self.sortedCardsArray = None
        self.cheat = False
        self.dialog = None
        self.requestDialog = None
        self.leaveReason = PlayingCardGlobals.PlayerStateUndefined
        self.swapResultDialog = None
        self.pickupCardsIvalArray = [
         None, None, None, None, None, None, None, None, None, None]
        self.playSequenceArray = [None, None, None, None, None, None, None, None, None, None]
        self.actionSequenceArray = [None, None, None, None, None, None, None, None, None, None]
        self.totalWinningsArray = []
        self.intervalList = []
        self.endOfHand = False
        return

    def generate(self):
        DistributedGameTable.DistributedGameTable.generate(self)
        self.setName(self.uniqueName('DistributedPokerTable'))
        self.dealerAnims = Sequence()

    def getGameType(self):
        return PlayingCardGlobals.Unknown

    def getInteractText(self):
        return PLocalizer.InteractTablePoker

    def setAnteList(self, anteList):
        self.anteList = anteList

    def excitementTask(self, task):
        if task.initialStart == -1:
            return Task.done
        if task.initialStart == 1:
            task.lastTime = task.time
            task.initialStart = 0
            return Task.cont
        deltaTime = task.time - task.lastTime
        task.lastTime = task.time
        if self.isLocalAvatarSeated() and self.isLocalAvatarPlaying():
            deltaPerc = self.excitement / 20 * deltaTime
            startPerc = self.gui.getMeterPercent()
            finalPerc = deltaPerc + startPerc
            if finalPerc >= 100:
                finalPerc = 100
            self.gui.setMeterPercent(finalPerc)
            if self.gui.getMeterPercent() >= 100:
                self.gui.meter.setColor(0, 0, 1, 1)
            elif self.handValue > 500:
                self.gui.meter.setColor(0, 1, 0, 1)
            else:
                self.gui.meter.setColor(1, 0, 0, 1)
        return Task.cont

    def reduceExcitement(self, delta=20):
        if self.isLocalAvatarSeated() and self.isLocalAvatarPlaying():
            initial = self.gui.getMeterPercent()
            final = initial - delta
            if final < 0:
                final = 0
            self.gui.setMeterPercent(final)
        self.acceptOnce('j', self.reduceExcitement)

    def balanceTask(self, task):
        if task.initialStart == -1:
            return Task.done
        if task.initialStart == 1:
            task.lastTime = task.time
            task.initialStart = 0
            return Task.cont
        deltaTime = task.time - task.lastTime
        task.lastTime = task.time
        if self.isLocalAvatarSeated() and self.isLocalAvatarPlaying():
            left = self.leftMass + self.baseMass
            right = self.rightMass + self.baseMass
            gravity = self.gravity
            oldMomentum = self.balanceM
            fulcrumPos = self.fulcrumPos
            currentAngle = self.gui.getBalanceAngle()
            cos = math.cos(math.radians(currentAngle))
            spring = self.springConst
            friction = self.friction
            I = left * math.pow(0 - fulcrumPos, 2) + right * math.pow(0.5 - fulcrumPos, 2)
            Tgrav = self.gravity * (left * (0 - fulcrumPos) * cos + right * (0.5 - fulcrumPos) * cos)
            Trestore = -spring * currentAngle
            T = Tgrav + Trestore
            A = T / I
            L = (1 - friction) * (oldMomentum + A * deltaTime)
            V = L / I
            self.balanceM = L
            self.gui.setBalanceAngle(currentAngle + V * deltaTime)
        return Task.cont

    def balanceLeft(self):
        self.fulcrumPos = self.fulcrumPos - 0.005
        if self.fulcrumPos < 0:
            self.fulcrumPos = 0
        if self.isLocalAvatarSeated():
            self.gui.balanceL.setScale(self.fulcrumPos / 2.0, 1, 0.01)
            self.gui.balanceL.setX(-self.fulcrumPos / 2.0)
            self.gui.balanceR.setScale((0.5 - self.fulcrumPos) / 2.0, 1, 0.01)
            self.gui.balanceR.setX((0.5 - self.fulcrumPos) / 2.0)
            self.gui.balance.setX(self.fulcrumPos - 0.25)
            self.gui.fulcrum.setX(self.fulcrumPos - 0.25)
            self.gui.weightR.setX(0.5 - self.fulcrumPos - 0.03)
            self.gui.weightL.setX(-(self.fulcrumPos - 0.03))
        self.acceptOnce('y', self.balanceLeft)

    def balanceRight(self):
        self.fulcrumPos = self.fulcrumPos + 0.005
        if self.fulcrumPos > 0.5:
            self.fulcrumPos = 0.5
        if self.isLocalAvatarSeated():
            self.gui.balanceL.setScale(self.fulcrumPos / 2.0, 1, 0.01)
            self.gui.balanceL.setX(-self.fulcrumPos / 2.0)
            self.gui.balanceR.setScale((0.5 - self.fulcrumPos) / 2.0, 1, 0.01)
            self.gui.balanceR.setX((0.5 - self.fulcrumPos) / 2.0)
            self.gui.balance.setX(self.fulcrumPos - 0.25)
            self.gui.fulcrum.setX(self.fulcrumPos - 0.25)
            self.gui.weightR.setX(0.5 - self.fulcrumPos - 0.03)
            self.gui.weightL.setX(-(self.fulcrumPos - 0.03))
        self.acceptOnce('u', self.balanceRight)

    def addMassLeft(self):
        self.leftMass = self.leftMass + 0.1
        if self.isLocalAvatarSeated():
            oldscale = self.gui.weightL.getScale()
            self.gui.weightL.setScale(0.03, 1, 0.05 * self.leftMass)
            self.gui.weightL.setZ(0.05 * self.leftMass + 0.01)
        self.acceptOnce('h', self.addMassLeft)

    def subMassLeft(self):
        self.leftMass = self.leftMass - 0.1
        if self.leftMass <= 0:
            self.leftMass = 0.1
        if self.isLocalAvatarSeated():
            oldscale = self.gui.weightL.getScale()
            self.gui.weightL.setScale(0.03, 1, 0.05 * self.leftMass)
            self.gui.weightL.setZ(0.05 * self.leftMass + 0.01)
        self.acceptOnce('n', self.subMassLeft)

    def addMassRight(self):
        self.rightMass = self.rightMass + 0.1
        if self.isLocalAvatarSeated():
            oldscale = self.gui.weightR.getScale()
            self.gui.weightR.setScale(0.03, 1, 0.05 * self.rightMass)
            self.gui.weightR.setZ(0.05 * self.rightMass + 0.01)
        self.acceptOnce('j', self.addMassRight)

    def subMassRight(self):
        self.rightMass = self.rightMass - 0.1
        if self.rightMass <= 0:
            self.rightMass = 0.1
        if self.isLocalAvatarSeated():
            oldscale = self.gui.weightR.getScale()
            self.gui.weightR.setScale(0.03, 1, 0.05 * self.rightMass)
            self.gui.weightR.setZ(0.05 * self.rightMass + 0.01)
        self.acceptOnce('m', self.subMassRight)

    def createGui(self):
        if not self.hasGui:
            if self.getGameVariation() == PiratesGlobals.PARLORGAME_VARIATION_UNDEAD:
                base.musicMgr.request(SoundGlobals.MUSIC_TORMENTA, priority=1, volume=0.6)
            self.gui = PokerTableGUI.PokerTableGUI(self, self.maxCommunityCards, self.maxHandCards)
            self.gui.setTableState(self.round, self.buttonSeat, self.communityCards, self.playerHands, self.totalWinningsArray)
            self.radarState = localAvatar.guiMgr.radarGui.state
            localAvatar.guiMgr.radarGui.request('Off')
            if self.getGameVariation() != PiratesGlobals.PARLORGAME_VARIATION_UNDEAD:
                localAvatar.guiMgr.gameGui.hide()
            self.hasGui = 1

    def satDown(self, seatIndex):
        self.createGui()
        if self.wantMeter == 1:
            self.gui.setMeterPercent(0)
        if self.wantMeter == 1:
            self.excitementT = taskMgr.add(self.excitementTask, 'PokerExcitement')
            self.excitementT.initialStart = 1
        if self.wantMeter == 2:
            self.balanceT = taskMgr.add(self.balanceTask, 'PokerBalance')
            self.balanceT.initialStart = 1
            self.baseMass = 1
            self.leftMass = 1
            self.rightMass = 1
            self.balanceM = 0
            self.gravity = 9.8
            self.fulcrumPos = 0.25
            self.friction = 0.1
            self.springConst = 0.05
            self.isStopped = True
        self.cameraNode = NodePath('CameraNode')
        camera.reparentTo(self.cameraNode)
        self.cameraNode.setPosHpr(0, 0.75, 22, 0, -45, 0)
        camera.setHpr(0, 0, 0)
        camera.setPos(-self.sittingOffset, 4.9, -11)
        base.camLens.setMinFov(60)
        self.cameraNode.reparentTo(localAvatar)
        if self.wantMeter == 1:
            self.acceptOnce('j', self.reduceExcitement)
        self.chips = 0
        self.chips = self.getPlayerChips()
        self.endOfHand = False
        text = self.getSitDownText()
        color = Vec4(1.0, 1.0, 1.0, 1.0)
        self.gui.showSitDownText(text, color)

    def getSitDownText(self):
        return PLocalizer.SitDownPoker

    def gotUp(self, seatIndex):
        if self.hasGui:
            self.gui.destroy()
            del self.gui
            self.hasGui = 0
        if self.radarState:
            localAvatar.guiMgr.radarGui.request(self.radarState)
        if self.getGameVariation() != PiratesGlobals.PARLORGAME_VARIATION_UNDEAD:
            localAvatar.guiMgr.gameGui.show()
        else:
            base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_TORMENTA, removeFromPlaylist=True)
        self.localAvatarHand = []
        self.removeCardsFromHand(localAvatar)

    def getCallAmount(self):
        previousAction = self.playerActions[self.localAvatarSeat]
        alreadyBet = previousAction[1]
        callAmount = self.maxBet - alreadyBet
        return callAmount

    def allIn(self):
        self.gui.disableAction(PLocalizer.PokerWaitingForOtherPlayers)
        self.d_clientAction(self.round, [PlayingCardGlobals.AllIn, 0])

    def guiCallback(self, action, allin_amount=0):
        if action == PlayingCardGlobals.CheckCall or action == PlayingCardGlobals.Check:
            self.gui.disableAction(PLocalizer.PokerWaitingForOtherPlayers)
            callAmount = self.getCallAmount()
            self.d_clientAction(self.round, [action, self.maxBet])
        elif action == PlayingCardGlobals.BetRaise:
            self.gui.disableAction(PLocalizer.PokerWaitingForOtherPlayers)
            betAmount = self.maxBet + self.getMinimumBetAmount()
            self.d_clientAction(self.round, [action, betAmount])
        elif action == PlayingCardGlobals.AllIn:
            self.gui.disableAction(PLocalizer.PokerWaitingForOtherPlayers)
            self.d_clientAction(self.round, [action, allin_amount])
        elif action == PlayingCardGlobals.Fold:
            self.setLocalAvatarHand([])
            self.gui.disableAction(PLocalizer.PokerWaitingForNextGame)
            if self.wantMeter == 2:
                self.ignore('y')
                self.ignore('u')
                self.ignore('h')
                self.ignore('n')
                self.ignore('j')
                self.ignore('m')
                self.gui.balance.hide()
                self.gui.fulcrum.hide()
            self.d_clientAction(self.round, [action, 0])
        elif action == PlayingCardGlobals.Leave:
            if self.hasGui:
                self.gui.disableAction()
            self.requestExit()
        elif action == PlayingCardGlobals.Cheat1:
            self.requestingCheat(PlayingCardGlobals.ReplaceHoleCardOneCheat, self.card_id)
        elif action == PlayingCardGlobals.Cheat2:
            self.requestingCheat(PlayingCardGlobals.ReplaceHoleCardTwoCheat, self.card_id)
        else:
            self.notify.error('guiCallback: unknown action: %s' % action)

    def undoCheat(self, cheatType, cheatTarget):
        pass

    def disable(self):
        DistributedGameTable.DistributedGameTable.disable(self)
        if self.gameType == 0:
            if self.excitementT != 0:
                self.excitementT.initialStart = -1
            if self.balanceT != 0:
                self.balanceT.initialStart = -1
        self.dealerAnims.pause()
        del self.dealerAnims
        length = len(self.pickupCardsIvalArray)
        for i in range(length):
            pickupCardsIval = self.pickupCardsIvalArray[i]
            self.pickupCardsIvalArray[i] = None
            if pickupCardsIval:
                pickupCardsIval.pause()
                del pickupCardsIval

        length = len(self.actionSequenceArray)
        for i in range(length):
            self.endActionSequence(i)

        length = len(self.playSequenceArray)
        for i in range(length):
            playSequence = self.playSequenceArray[i]
            self.playSequenceArray[i] = None
            if playSequence:
                playSequence.pause()
                del playSequence

        for interval in self.intervalList:
            interval.pause()

        return

    def delete(self):
        self.deleteSwapResultDialog()
        DistributedGameTable.DistributedGameTable.delete(self)
        if self.hasGui:
            if self.getGameVariation() == PiratesGlobals.PARLORGAME_VARIATION_UNDEAD:
                base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_TORMENTA, removeFromPlaylist=True)
            self.gui.destroy()
            del self.gui
            self.hasGui = 0

    def removeInterval(self, interval):
        if interval in self.intervalList:
            self.intervalList.remove(interval)

    def setTableState(self, round, buttonSeat, communityCards, playerHands, totalWinningsArray, chipsCount):
        self.updateStacks(chipsCount)
        self.round = round
        if self.round == 0:
            self.localAvatarHand = []
            self.handId = PlayingCardGlobals.Nothing
            self.sortedCards = None
            self.cheat = False
            if self.hasGui:
                self.gui.enableCheat()
                self.gui.hideArrow()
            self.endOfHand = False
        self.buttonSeat = buttonSeat
        self.communityCards = communityCards
        self.playerHands = playerHands
        self.totalWinningsArray = totalWinningsArray
        self.savedHandTampered = 1
        numPlayers = 0
        for i in range(len(playerHands)):
            if playerHands:
                numPlayers += 1

        numPlayers = len(filter(lambda hand: hand, playerHands))
        if numPlayers == 1 or round == self.numRounds:
            self.endOfHand = True
            self.processWinners(playerHands, totalWinningsArray)
            self.updateGui()
        else:
            self.dealerAnims.pause()
            self.dealerAnims = self.dealerAnim(self.round)
            self.dealerAnims.append(Func(self.updateGui))
            self.dealerAnims.start()
        return

    def playActorAnimation(self, actor, animation):
        actor.play(animation)

    def processWinners(self, playerHands, totalWinningsArray):
        total_winners = 0
        total_active = 0
        length = len(self.actors)
        win_length = len(totalWinningsArray)
        for i in range(win_length):
            if totalWinningsArray[i] > 0:
                total_winners = total_winners + 1
            if totalWinningsArray[i] >= 0:
                total_active = total_active + 1

        for i in range(length):
            if i < win_length:
                actor = self.actors[i]
                if actor:
                    if totalWinningsArray[i] > 0:
                        if actor.isLocal():
                            audio = self.getAudio()
                            if audio:
                                sfx = audio.sfxArray[audio.collectIdentifier]
                                self.playSoundEffect(sfx)
                        self.endActionSequence(i)
                        if i == self.localAvatarSeat:
                            title = ''
                            text = PLocalizer.TableWinGold % totalWinningsArray[i]
                            color = Vec4(1.0, 1.0, 1.0, 1.0)
                            color = Vec4(0.2, 0.8, 0.4, 1.0)
                            position = Vec3(0.0, 0.0, -0.65)
                            self.gui.showWinText(text, color, position)
                        if total_active == 1:
                            self.playActorAnimation(actor, 'cards_set_down_win')
                        else:
                            self.playActorAnimation(actor, 'cards_set_down_win_show')
                    if totalWinningsArray[i] == PlayingCardGlobals.PlayerLost:
                        self.endActionSequence(i)
                        self.playActorAnimation(actor, 'cards_set_down_lose')
                        if i == self.localAvatarSeat:
                            text = PLocalizer.PokerYouLost
                            color = Vec4(0.7, 0.7, 0.7, 1.0)
                            color = Vec4(0.2, 0.4, 0.8, 1.0)
                            position = Vec3(0.0, 0.0, -0.65)
                            self.gui.showWinText(text, color, position)
                    if totalWinningsArray[i] == PlayingCardGlobals.PlayerInactive:
                        pass
                    if totalWinningsArray[i] == PlayingCardGlobals.PlayerOutOfChips:
                        self.endActionSequence(i)
                        self.playActorAnimation(actor, 'cards_set_down_lose')
                        if actor.isLocal():
                            reason = PlayingCardGlobals.PlayerOutOfChips
                            self.playerMustLeave(reason)
                    if totalWinningsArray[i] == PlayingCardGlobals.PlayerCaughtCheating:
                        self.endActionSequence(i)
                        self.playActorAnimation(actor, 'cards_set_down_lose')
                        if actor.isLocal():
                            reason = PlayingCardGlobals.PlayerCaughtCheating
                            self.playerMustLeave(reason)

        if self.isLocalAvatarSeated():
            self.gui.disableAction(PLocalizer.PokerWaitingForNextGame)

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
        if self.leaveReason == PlayingCardGlobals.PlayerCaughtCheating:
            string = PLocalizer.PokerCaughtCheatingMessage % PlayingCardGlobals.CheatingFine
            self.dialog = PDialog.PDialog(text=string, style=OTPDialog.Acknowledge, command=self.dialogCallback)
            self.setDialogBin(self.dialog)
        elif self.leaveReason == PlayingCardGlobals.PlayerOutOfChips:
            self.dialog = PDialog.PDialog(text=PLocalizer.PokerOutOfChipsMessage, style=OTPDialog.Acknowledge, command=self.dialogCallback)
            self.setDialogBin(self.dialog)
        self.guiCallback(PlayingCardGlobals.Leave)
        self.removeCardsFromHand(localAvatar)

    def playerMustLeave(self, reason):
        delay = 5.0
        self.leaveReason = reason
        taskMgr.doMethodLater(delay, self.delayedPlayerLeave, self.uniqueName('delayedPlayerLeave'))
        self.gui.menu.hide()

    def updateGui(self):
        if self.isLocalAvatarSeated():
            if self.round <= 1:
                self.gui.handId = PlayingCardGlobals.Nothing
                self.gui.sortedCards = None
            else:
                self.gui.handId = self.handId
                self.gui.sortedCards = self.sortedCards
            self.gui.setTableState(self.round, self.buttonSeat, self.communityCards, self.playerHands, self.totalWinningsArray)
            self.gui.setLocalAvatarHand(self.localAvatarHand)
        return

    def setPotSize(self, potSize):
        self.potSize = potSize
        self.displayStacks(self.getPotSeat(), potSize)
        if self.isLocalAvatarSeated():
            self.gui.setPotSize(potSize)

    def removeCardsFromHand(self, actor):
        if actor.leftHandNode.getNumChildren() > 0:
            npc = actor.leftHandNode.getChildren()
            if npc:
                npc.detach()

    def endActionSequence(self, i):
        actionSequence = self.actionSequenceArray[i]
        self.actionSequenceArray[i] = None
        if actionSequence:
            actionSequence.pause()
            del actionSequence
        return

    def __playBetSequence(self, actor, i):
        self.endActionSequence(i)
        sfx = None
        audio = self.getAudio()
        if audio:
            sfx = audio.sfxArray[audio.betIdentifier]
        actionSequence = Parallel(actor.actorInterval('cards_bet'), Sequence(Wait(1.0), Func(self.playSoundEffect, sfx)))
        actionSequence.start()
        self.actionSequenceArray[i] = actionSequence
        return

    def __playCheckSequence(self, actor, i):
        self.endActionSequence(i)
        sfx = None
        audio = self.getAudio()
        if audio:
            sfx = audio.sfxArray[audio.checkIdentifier]
        actionSequence = Parallel(actor.actorInterval('cards_check'), Sequence(Wait(1.0), Func(self.playSoundEffect, sfx)))
        actionSequence.start()
        self.actionSequenceArray[i] = actionSequence
        return

    def __playFoldSequence(self, actor, i):
        self.endActionSequence(i)
        sfx = None
        audio = self.getAudio()
        if audio:
            sfx = audio.sfxArray[audio.foldIdentifier]
        actionSequence = Sequence(actor.actorInterval('cards_set_down', endFrame=50, mixingWanted=False), Func(self.playSoundEffect, sfx), Func(self.removeCardsFromHand, actor), actor.actorInterval('cards_set_down', startFrame=50, mixingWanted=False))
        actionSequence.start()
        self.actionSequenceArray[i] = actionSequence
        return

    def setPlayerActions(self, maxBet, playerActions, chipsCount):
        self.updateStacks(chipsCount)
        self.maxBet = maxBet
        oldPlayerActions = self.playerActions
        self.playerActions = playerActions
        i = 0
        for actor, newAction, oldAction in zip(self.actors, playerActions, oldPlayerActions):
            if actor and newAction != oldAction:
                mostRecentAction, amount = newAction
                if mostRecentAction == PlayingCardGlobals.CheckCall or mostRecentAction == PlayingCardGlobals.Check:
                    if amount and mostRecentAction != PlayingCardGlobals.Check:
                        self.__playBetSequence(actor, i)
                    else:
                        self.__playCheckSequence(actor, i)
                elif mostRecentAction == PlayingCardGlobals.BetRaise:
                    self.__playBetSequence(actor, i)
                elif mostRecentAction == PlayingCardGlobals.Fold:
                    self.__playFoldSequence(actor, i)
                    self.playerHands[i] = []
                elif mostRecentAction == PlayingCardGlobals.SmallBlind or mostRecentAction == PlayingCardGlobals.BigBlind:
                    self.__playBetSequence(actor, i)
                elif mostRecentAction == PlayingCardGlobals.AllIn:
                    if amount > 0:
                        self.__playBetSequence(actor, i)
            i = i + 1

        if self.isLocalAvatarSeated():
            self.gui.setPlayerActions(maxBet, playerActions)

    def askForClientAction(self, seatIndex):
        if self.isLocalAvatarSeated():
            if self.round > 0:
                self.gui.showArrow(seatIndex)
            else:
                self.gui.hideArrow()
            if seatIndex == self.localAvatarSeat:
                self.gui.enableAction()

    def setLocalAvatarHand(self, hand):
        self.localAvatarHand = hand

    def setLocalAvatarHandValue(self, handId, sortedCards):
        self.handId = handId
        self.sortedCards = sortedCards

    def setAllHandValues(self, handIdArray, sortedCardsArray):
        self.handIdArray = handIdArray
        self.sortedCardsArray = sortedCardsArray

    def requestAIPlayerTurn(self, seatIndex):
        if self.isLocalAvatarSeated():
            if self.round > 0:
                self.gui.showArrow(seatIndex)
            else:
                self.gui.hideArrow()

    def deleteSwapResultDialog(self):
        if self.swapResultDialog:
            self.swapResultDialog.destroy()
            del self.swapResultDialog
            self.swapResultDialog = None
        return

    def swapResultCallback(self, value):
        self.deleteSwapResultDialog()

    def cheatResponse(self, cheatType, cheatTarget, success, hand):
        swap = False
        if cheatType == PlayingCardGlobals.PeekCheatLeft:
            pass
        else:
            if cheatType == PlayingCardGlobals.PeekCheatRight:
                pass
            elif cheatType == PlayingCardGlobals.ReplaceHoleCardOneCheat:
                self.setLocalAvatarHand(hand)
                swap = True
            elif cheatType == PlayingCardGlobals.ReplaceHoleCardTwoCheat:
                self.setLocalAvatarHand(hand)
                swap = True
            elif cheatType == PlayingCardGlobals.ReplaceHoleCardSevenCheat:
                self.setLocalAvatarHand(hand)
                swap = True
            elif cheatType == PlayingCardGlobals.PlayBadHandTell:
                pass
            elif cheatType == PlayingCardGlobals.PlayGoodHandTell:
                pass
            if swap:
                if success:
                    string = PLocalizer.PokerSwapSuccessMessage
                else:
                    string = PLocalizer.PokerSwapFailureMessage
                self.swapResultDialog = PDialog.PDialog(text=string, style=OTPDialog.Acknowledge, giveMouse=False, command=self.swapResultCallback)
                position = self.swapResultDialog.getPos()
                position.setZ(position[2] + 0.35)
                self.swapResultDialog.setPos(position)
                self.setDialogBin(self.swapResultDialog)
                if self.isLocalAvatarSeated() and self.isLocalAvatarPlaying():
                    actor = self.actors[self.localAvatarSeat]
                    if actor:
                        actor.play('cards_cheat')
        self.updateGui()

    def sendTell(self, tell):
        self.handValue = tell
        self.excitement = pow(math.fabs(tell - 500) / 500.0, 3) * 1000
        if self.wantMeter == 2:
            side = random.randint(0, 1)
            multiplier = math.floor(self.excitement) / 333.0 + 1
            if side == 0:
                if self.handValue < 500:
                    self.leftMass = self.leftMass / multiplier
                else:
                    self.leftMass = self.leftMass * multiplier
                if self.isLocalAvatarSeated():
                    self.gui.weightL.setScale(0.03, 1, 0.05 * self.leftMass)
                    self.gui.weightL.setZ(0.05 * self.leftMass + 0.01)
            else:
                if self.handValue < 500:
                    self.rightMass = self.rightMass / multiplier
                else:
                    self.rightMass = self.rightMass * multiplier
                if self.isLocalAvatarSeated():
                    self.gui.weightR.setScale(0.03, 1, 0.05 * self.rightMass)
                    self.gui.weightR.setZ(0.05 * self.rightMass + 0.01)

    def d_clientAction(self, round, action):
        self.sendUpdate('clientAction', [round, action])

    def requestingCheat(self, cheatType, cheatTarget):
        self.currentCheatType = cheatType
        self.currentCheatTarget = cheatTarget
        self.sendUpdate('requestCheat', [cheatType, cheatTarget])
        self.cheat = True
        self.gui.disableCheat()

    def isLocalAvatarPlaying(self):
        return self.localAvatarHand != []

    def dealerAnim(self, round):
        self.notify.error('dealerAnim should be implemented by a subclass')
        return Sequence()

    def dealCommunityCards(self, numCards):
        dealCards = Sequence()
        audio = self.getAudio()
        sfx = None
        if audio:
            sfx = audio.sfxArray[audio.startDealIdentifier + int(random.random() * audio.totalDealIdentifiers)]
        dealOutwards = self.dealer.actorInterval('deal', endFrame=11, playRate=1.5, mixingWanted=False)
        dealInwards = self.dealer.actorInterval('deal', startFrame=11, playRate=3.0, mixingWanted=False)
        for i in range(numCards):
            (
             dealCards.append(Func(self.playSoundEffect, sfx)),)
            dealCards.append(dealOutwards)
            dealCards.append(dealInwards)

        dealCards.append(Func(self.dealer.loop, 'deal_idle'))
        tell_action = 0
        enable_tells = False
        for player in range(len(self.playerHands)):
            if player <= len(self.totalWinningsArray):
                tell_action = self.totalWinningsArray[player]
                enable_tells = True
            playSequence = self.playSequenceArray[player]
            self.playSequenceArray[player] = None
            if playSequence:
                playSequence.pause()
                del playSequence
            playSequence = None
            if enable_tells and tell_action != PlayingCardGlobals.NoTell:
                actor = self.actors[player]
                if actor:
                    playSequence = Sequence()
                    playSequence.append(actor.actorInterval('cards_hide', playRate=-1.0))
                    if tell_action == PlayingCardGlobals.GoodTell:
                        playSequence.append(actor.actorInterval('cards_good_tell'))
                    else:
                        playSequence.append(actor.actorInterval('cards_bad_tell'))
                    playSequence.append(actor.actorInterval('cards_hide'))
                    playSequence.append(Func(actor.loop, 'cards_hide_idle'))
                    playSequence.start()
            self.playSequenceArray[player] = playSequence

        return dealCards

    def playSoundEffect(self, sfx):
        if sfx:
            base.playSfx(sfx)

    def dealPlayerCards(self, numCards):
        deals = Sequence()
        audio = self.getAudio()
        if self.round == 1 and self.isLocalAvatarSeated():
            if audio:
                sfx = audio.sfxArray[audio.shuffleIdentifier]
                if sfx:
                    deals.append(Func(self.playSoundEffect, sfx))
                    deals.append(Wait(sfx.length()))
        dealerSeat = self.SeatInfo[-1]
        getCards = self.dealer.actorInterval('into_deal', mixingWanted=False)
        dealOutwards = self.dealer.actorInterval('deal', endFrame=10, playRate=1.4, mixingWanted=False)
        dealInwards = self.dealer.actorInterval('deal', startFrame=10, playRate=2.0, mixingWanted=False)
        dealLeftOutwards = self.dealer.actorInterval('deal_left', endFrame=7, playRate=1.4, mixingWanted=False)
        dealLeftInwards = self.dealer.actorInterval('deal_left', startFrame=7, playRate=2.0, mixingWanted=False)
        dealRightOutwards = self.dealer.actorInterval('deal_right', endFrame=7, playRate=1.4, mixingWanted=False)
        dealRightInwards = self.dealer.actorInterval('deal_right', startFrame=7, playRate=2.0, mixingWanted=False)
        cardNum = 0
        dealtCards = []
        for player in range(len(self.playerHands)):
            dealtCards.append([])

        for i in range(numCards):
            seats = range(self.NumSeats)
            slicer = self.buttonSeat + 1 % self.NumSeats
            seats = seats[slicer:] + seats[:slicer]
            for player in seats:
                if self.playerHands[player] != [] and self.actors[player]:
                    currentH = dealerSeat.getH()
                    dealerSeat.headsUp(self.actors[player])
                    headingToPlayer = dealerSeat.getH()
                    dealerSeat.setH(currentH)
                    if headingToPlayer > 35:
                        dealOutIval = dealLeftOutwards
                        dealInIval = dealLeftInwards
                    else:
                        if headingToPlayer < -35:
                            dealOutIval = dealRightOutwards
                            dealInIval = dealRightInwards
                        else:
                            dealOutIval = dealOutwards
                            dealInIval = dealInwards
                        card = self.PocketCards[cardNum]
                        cardNum += 1
                        dealtCards[player].append(card)
                        card.hide()
                        card.reparentTo(self.dealer.rightHandNode)
                        card.setPosHpr(0, 0, 0, 0, 0, 0)
                        card.setScale(render, 1.2)
                        endCardH = -(180.0 + random.random() * 360.0)
                        distance = card.getDistance(self.PocketCardPositions[player])
                        duration = distance / 9.0
                        throwCard = LerpPosHprInterval(card, duration=duration, pos=Point3(0, 0, 0), hpr=Vec3(endCardH, 0, 0), startPos=None, startHpr=None, blendType='easeOut')
                        self.intervalList.append(throwCard)
                        sfx = None
                        if audio:
                            sfx = audio.sfxArray[audio.startDealIdentifier + int(random.random() * audio.totalDealIdentifiers)]
                    dealCard = Sequence(Func(card.show), dealOutIval, Func(self.playSoundEffect, sfx), Func(card.wrtReparentTo, self.PocketCardPositions[player]), Func(throwCard.start), dealInIval, Func(self.removeInterval, throwCard))
                    deals.append(dealCard)

        deals.append(Func(self.dealer.loop, 'deal_idle'))
        finishDeal = Parallel()
        for player in range(len(self.playerHands)):
            if self.playerHands[player] != [] and self.actors[player]:
                finishDeal.append(Func(self.pickupCards, player, dealtCards[player]))

        deals.append(finishDeal)
        return deals

    def pickupCards(self, player, cards):
        actor = self.actors[player]
        if not actor:
            return

        def __reparentCards():
            for card in cards:
                card.wrtReparentTo(actor.leftHandNode)
                card.setPosHpr(0, 0, 0, 0, 0, 0)

        pickupCardsIval = self.pickupCardsIvalArray[player]
        self.pickupCardsIvalArray[player] = None
        if pickupCardsIval:
            pickupCardsIval.pause()
            del pickupCardsIval
        pickupCardsIval = Sequence(Wait(random.random() * 1.0), actor.actorInterval('cards_pick_up', endFrame=17, mixingWanted=False), Func(__reparentCards), actor.actorInterval('cards_pick_up', startFrame=17, mixingWanted=False))
        tell_action = 0
        enable_tells = False
        if player <= len(self.totalWinningsArray):
            tell_action = self.totalWinningsArray[player]
            enable_tells = True
        if enable_tells and tell_action != PlayingCardGlobals.NoTell:
            if tell_action == PlayingCardGlobals.GoodTell:
                pickupCardsIval.append(actor.actorInterval('cards_good_tell'))
            else:
                pickupCardsIval.append(actor.actorInterval('cards_bad_tell'))
        pickupCardsIval.append(actor.actorInterval('cards_hide'))
        pickupCardsIval.append(Func(actor.loop, 'cards_hide_idle'))
        pickupCardsIval.start()
        self.pickupCardsIvalArray[player] = pickupCardsIval
        return

    def getPlayerChips(self):
        inventory = localAvatar.getInventory()
        if inventory:
            self.chips = inventory.getGoldInPocket()
        return self.chips

    def requestSeatResponse(self, answer, seatIndex):
        if answer == 4:
            self.deleteRequestDialogs()
            message = PLocalizer.PokerInsufficientChipsMessage % self.minimumChipsToSitDown()
            self.requestDialog = PDialog.PDialog(text=message, style=OTPDialog.Acknowledge, command=self.requestCommand)
            self.setDialogBin(self.requestDialog)
            localAvatar.motionFSM.on()
            self.cr.interactionMgr.start()
        else:
            DistributedGameTable.DistributedGameTable.requestSeatResponse(self, answer, seatIndex)

    def getPlayerInventoryCardCount(self, card_id):
        inventory = localAvatar.getInventory()
        if inventory:
            amount = inventory.getStackQuantity(InventoryType.begin_Cards + card_id)
        else:
            amount = 0
        return amount

    def getAudio(self):
        audio = None
        if self.hasGui:
            audio = self.gui
        return audio

    def getLocalAvatarHand(self):
        return self.localAvatarHand

    def getPlayerReputation(self, avId):
        reputation = 0
        inventory = localAvatar.getInventory()
        if inventory:
            reputation = inventory.getStackQuantity(InventoryType.PokerGame)
        return reputation

    def playerExpired(self):
        if self.getGameVariation() == PiratesGlobals.PARLORGAME_VARIATION_UNDEAD:
            text = PLocalizer.PokerYouLost
            color = Vec4(0.7, 0.7, 0.7, 1.0)
            color = Vec4(0.2, 0.4, 0.8, 1.0)
            position = Vec3(0.0, 0.0, -0.65)
            self.gui.showWinText(text, color, position)
            DelayedCall(Functor(base.transitions.fadeOut), delay=3.0)
            localAvatar.guiMgr.gameGui.hide()
            self.gui.hideActionButtons()
            self.gui.hideCheatButtons()
            if self.getEndInteract():
                self.ignore(END_INTERACT_EVENT)

    def showHealthLoss(self, amount):
        localAvatar.showHpText(amount, pos=[1.75, 0, 2], scale=0.4)