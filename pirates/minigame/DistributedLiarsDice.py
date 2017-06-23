import random
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.minigame import DistributedDiceGame
from pirates.minigame import DiceGlobals
from pirates.piratesgui import GuiTray
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer

class DistributedLiarsDice(DistributedDiceGame.DistributedDiceGame):

    def __init__(self, cr):
        DistributedDiceGame.DistributedDiceGame.__init__(self, cr, numdice=5, public=0, name="Liar's Dice")
        self.animPlaying = 0

    def rollResults(self, seat, dice):
        print 'DistributedLiarsDice:rollResults - seat %d' % seat
        self.dicevals[seat] = dice
        if seat == self.mySeat:
            if self.gameState == DiceGlobals.DSTATE_WAIT:
                self.gameState = DiceGlobals.DSTATE_PLAY

    def extraGuiSetup(self):
        self.betDice = 1
        self.betValue = 1
        self.oldDice = 1
        self.oldValue = 1
        self.challDice = []
        self.challSeq = {}
        self.cheatDetect = 0
        self.mojoDetect = 0
        self.checkButton = DirectButton(parent=self.gui, relief=DGG.RAISED, state=DGG.DISABLED, text='CALL BLUFF', text_align=TextNode.ACenter, text_scale=0.08, text_fg=(0.5,
                                                                                                                                                                          0.5,
                                                                                                                                                                          0.4,
                                                                                                                                                                          1), frameColor=(1,
                                                                                                                                                                                          0.9,
                                                                                                                                                                                          0.6,
                                                                                                                                                                                          1), frameSize=(0,
                                                                                                                                                                                                         0.47,
                                                                                                                                                                                                         0,
                                                                                                                                                                                                         0.12), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.23,
                                                                                                                                                                                                                                                                     0.033), textMayChange=1, pos=(-0.23, 0, -0.31), command=self.guiCallback, extraArgs=['call bluff'])
        self.checkButton.hide()
        self.claimButton = DirectButton(parent=self.gui, relief=DGG.RAISED, state=DGG.DISABLED, text='MAKE CLAIM', text_align=TextNode.ACenter, text_scale=0.08, text_fg=PiratesGuiGlobals.TextFG2, frameColor=(0.2,
                                                                                                                                                                                                                0.6,
                                                                                                                                                                                                                0.1,
                                                                                                                                                                                                                1), frameSize=(0,
                                                                                                                                                                                                                               0.47,
                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                               0.12), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.23,
                                                                                                                                                                                                                                                                                           0.033), textMayChange=1, pos=(-0.23, 0, -0.02), command=self.guiCallback, extraArgs=['make claim'])
        self.claimButton.hide()
        self.mojoButton = DirectButton(parent=self.gui, relief=DGG.RAISED, state=DGG.DISABLED, text='USE MOJO', text_align=TextNode.ACenter, text_scale=0.08, text_fg=(0.2,
                                                                                                                                                                       0.35,
                                                                                                                                                                       0.6,
                                                                                                                                                                       1), frameColor=(0.4,
                                                                                                                                                                                       0.6,
                                                                                                                                                                                       1.0,
                                                                                                                                                                                       1), frameSize=(0,
                                                                                                                                                                                                      0.45,
                                                                                                                                                                                                      0,
                                                                                                                                                                                                      0.12), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.23,
                                                                                                                                                                                                                                                                  0.033), textMayChange=1, pos=(0.7, 0, -0.4), command=self.guiCallback, extraArgs=['mojo'])
        self.mojoButton.hide()
        self.catchCheat = DirectButton(parent=self.gui, relief=DGG.RAISED, state=DGG.DISABLED, text='CATCH CHEATER', text_align=TextNode.ACenter, text_scale=0.04, text_fg=(0.8,
                                                                                                                                                                            0.4,
                                                                                                                                                                            0.4,
                                                                                                                                                                            1), frameColor=(0.6,
                                                                                                                                                                                            0.3,
                                                                                                                                                                                            0.3,
                                                                                                                                                                                            1), frameSize=(0,
                                                                                                                                                                                                           0.45,
                                                                                                                                                                                                           0,
                                                                                                                                                                                                           0.12), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.23,
                                                                                                                                                                                                                                                                       0.033), textMayChange=1, pos=(0.84,
                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                     0.84), command=self.guiCallback, extraArgs=['catch cheat'])
        self.catchCheat.hide()
        self.cheatButton = DirectButton(parent=self.gui, relief=DGG.RAISED, state=DGG.DISABLED, text='CHEAT', text_align=TextNode.ACenter, text_scale=0.08, text_fg=(0.7,
                                                                                                                                                                     0.4,
                                                                                                                                                                     0.3,
                                                                                                                                                                     1), frameColor=(1,
                                                                                                                                                                                     0.7,
                                                                                                                                                                                     0.5,
                                                                                                                                                                                     1), frameSize=(0,
                                                                                                                                                                                                    0.45,
                                                                                                                                                                                                    0,
                                                                                                                                                                                                    0.12), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.23,
                                                                                                                                                                                                                                                                0.033), textMayChange=1, pos=(-1.1, 0, -0.4), command=self.guiCallback, extraArgs=['cheat'])
        self.cheatButton.hide()
        self.diceNumText = DirectLabel(parent=self.gui, relief=None, text='Num Dice', text_align=TextNode.ALeft, text_scale=0.1, pos=(-0.4, 0, -0.5), text_fg=(1,
                                                                                                                                                               0.9,
                                                                                                                                                               0.6,
                                                                                                                                                               1), text_shadow=(0,
                                                                                                                                                                                0,
                                                                                                                                                                                0,
                                                                                                                                                                                1))
        self.diceNumText.hide()
        self.diceNumLabel = DirectLabel(parent=self.gui, relief=None, text='1', text_align=TextNode.ALeft, text_scale=0.2, pos=(-0.28, 0, -0.7), text_fg=(1,
                                                                                                                                                          0.9,
                                                                                                                                                          0.6,
                                                                                                                                                          1), text_shadow=(0,
                                                                                                                                                                           0,
                                                                                                                                                                           0,
                                                                                                                                                                           1))
        self.diceNumLabel.hide()
        self.diceValText = DirectLabel(parent=self.gui, relief=None, text='Value', text_align=TextNode.ALeft, text_scale=0.1, pos=(0.27, 0, -0.5), text_fg=(1,
                                                                                                                                                            0.9,
                                                                                                                                                            0.6,
                                                                                                                                                            1), text_shadow=(0,
                                                                                                                                                                             0,
                                                                                                                                                                             0,
                                                                                                                                                                             1))
        self.diceValText.hide()
        self.diceValLabel = DirectLabel(parent=self.gui, relief=None, text='1', text_align=TextNode.ALeft, text_scale=0.2, pos=(0.33, 0, -0.7), text_fg=(1,
                                                                                                                                                         0.9,
                                                                                                                                                         0.6,
                                                                                                                                                         1), text_shadow=(0,
                                                                                                                                                                          0,
                                                                                                                                                                          0,
                                                                                                                                                                          1))
        self.diceValLabel.hide()
        self.diceUpButton = DirectButton(parent=self.gui, relief=DGG.RAISED, text='>', text_align=TextNode.ACenter, text_scale=0.05, text_pos=(0.02,
                                                                                                                                               0.01), text_fg=(0,
                                                                                                                                                               0,
                                                                                                                                                               0,
                                                                                                                                                               1), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, frameColor=PiratesGuiGlobals.ButtonColor2, borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameSize=(0,
                                                                                                                                                                                                                                                                                                                                    0.05,
                                                                                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                                                                                    0.05), pos=(-0.1, 0, -0.69), command=self.guiCallback, extraArgs=['dice up'])
        self.diceUpButton.hide()
        self.diceDownButton = DirectButton(parent=self.gui, relief=DGG.RAISED, text='<', text_align=TextNode.ACenter, text_scale=0.05, text_pos=(0.02,
                                                                                                                                                 0.01), text_fg=(0,
                                                                                                                                                                 0,
                                                                                                                                                                 0,
                                                                                                                                                                 1), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, frameColor=PiratesGuiGlobals.ButtonColor2, borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameSize=(0,
                                                                                                                                                                                                                                                                                                                                      0.05,
                                                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                                                      0.05), pos=(-0.38, 0, -0.69), command=self.guiCallback, extraArgs=['dice down'])
        self.diceDownButton.hide()
        self.valueUpButton = DirectButton(parent=self.gui, relief=DGG.RAISED, text='>', text_align=TextNode.ACenter, text_scale=0.05, text_pos=(0.02,
                                                                                                                                                0.01), text_fg=(0,
                                                                                                                                                                0,
                                                                                                                                                                0,
                                                                                                                                                                1), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, frameColor=PiratesGuiGlobals.ButtonColor2, borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameSize=(0,
                                                                                                                                                                                                                                                                                                                                     0.05,
                                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                                     0.05), pos=(0.51, 0, -0.69), command=self.guiCallback, extraArgs=['value up'])
        self.valueUpButton.hide()
        self.valueDownButton = DirectButton(parent=self.gui, relief=DGG.RAISED, text='<', text_align=TextNode.ACenter, text_scale=0.05, text_pos=(0.02,
                                                                                                                                                  0.01), text_fg=(0,
                                                                                                                                                                  0,
                                                                                                                                                                  0,
                                                                                                                                                                  1), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, frameColor=PiratesGuiGlobals.ButtonColor2, borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameSize=(0,
                                                                                                                                                                                                                                                                                                                                       0.05,
                                                                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                                                                       0.05), pos=(0.26, 0, -0.69), command=self.guiCallback, extraArgs=['value down'])
        self.valueDownButton.hide()
        return

    def extraGuiDestroy(self):
        self.valueUpButton.destroy()
        self.valueDownButton.destroy()
        self.diceUpButton.destroy()
        self.diceDownButton.destroy()
        self.checkButton.destroy()
        self.claimButton.destroy()
        self.mojoButton.destroy()
        self.cheatButton.destroy()
        self.diceNumText.destroy()
        self.diceValText.destroy()
        self.catchCheat.destroy()
        taskMgr.remove('doneCheat')
        i = len(self.challDice) - 1
        while i > -1:
            self.challDice[i].removeNode()
            del self.challDice[i]
            i -= 1

        self.challDice = []
        self.challSeq.clear()

    def extraGuiCallback(self, action):
        if action == 'value up':
            if self.betValue < 6:
                self.sendChat(DiceGlobals.CHAT_DICEUP)
                self.betValue += 1
                self.diceValLabel['text'] = '%d' % self.betValue
            return 1
        elif action == 'value down':
            if self.betValue > 1 and (self.betValue > self.oldValue or self.betDice > self.oldDice):
                self.sendChat(DiceGlobals.CHAT_DICEDOWN)
                self.betValue -= 1
                self.diceValLabel['text'] = '%d' % self.betValue
            return 1
        elif action == 'dice up':
            if self.betDice < self.numDice * self.NumSeats:
                self.sendChat(DiceGlobals.CHAT_DICEUP)
                self.betDice += 1
                if self.betDice == 10:
                    self.diceNumLabel.setPos(-0.34, 0, -0.7)
                self.diceNumLabel['text'] = '%d' % self.betDice
            return 1
        elif action == 'dice down':
            if self.betDice > 1 and self.betDice > self.oldDice:
                self.sendChat(DiceGlobals.CHAT_DICEDOWN)
                self.betDice -= 1
                if self.betDice == 9:
                    self.diceNumLabel.setPos(-0.28, 0, -0.7)
                self.diceNumLabel['text'] = '%d' % self.betDice
                if self.betDice == self.oldDice and self.betValue < self.oldValue:
                    self.betValue = self.oldValue
                    self.diceValLabel['text'] = '%d' % self.betValue
            return 1
        elif action == 'make claim':
            self.makeClaim()
            return 1
        elif action == 'call bluff':
            self.callBluff()
            return 1
        elif action == 'cheat':
            self.tryToCheat()
            return 1
        elif action == 'mojo':
            self.useMojo()
            return 1
        elif action == 'catch cheat':
            self.caughtYou()
            return 1
        else:
            return 0

    def extraYourTurn(self):
        self.cheatDetect -= 20
        if self.cheatDetect < 0:
            self.cheatDetect = 0
        self.mojoDetect -= 20
        if self.mojoDetect < 0:
            self.mojoDetect = 0
        self.catchCheat['state'] = DGG.DISABLED
        self.catchCheat.hide()
        taskMgr.remove('doneCheat')
        if self.gameState == DiceGlobals.DSTATE_PLAY:
            print 'DistributedDiceGame:yourTurn - powering up buttons'
            self.diceNumText.show()
            self.diceValText.show()
            self.diceNumLabel.show()
            self.diceValLabel.show()
            self.diceUpButton.show()
            self.diceUpButton['state'] = DGG.NORMAL
            self.diceDownButton.show()
            self.diceDownButton['state'] = DGG.NORMAL
            self.valueDownButton.show()
            self.valueDownButton['state'] = DGG.NORMAL
            self.valueUpButton.show()
            self.valueUpButton['state'] = DGG.NORMAL
            self.checkButton.show()
            self.checkButton['frameColor'] = (1, 0.9, 0.6, 1)
            self.checkButton['state'] = DGG.NORMAL
            self.claimButton.show()
            self.claimButton['frameColor'] = (0.2, 0.6, 0.1, 1)
            self.claimButton['state'] = DGG.NORMAL
            self.mojoButton.show()
            self.mojoButton['state'] = DGG.NORMAL
            self.mojoButton['frameColor'] = (0.4, 0.6, 1.0, 1)
            self.cheatButton.show()
            self.cheatButton['state'] = DGG.NORMAL
            self.cheatButton['frameColor'] = (1, 0.7, 0.5, 1)
            self.gui.mainButton['state'] = DGG.DISABLED

    def extraGuiReset(self):
        self.diceUpButton.hide()
        self.diceUpButton['state'] = DGG.DISABLED
        self.diceDownButton.hide()
        self.diceDownButton['state'] = DGG.DISABLED
        self.valueDownButton.hide()
        self.valueDownButton['state'] = DGG.DISABLED
        self.valueUpButton.hide()
        self.valueUpButton['state'] = DGG.DISABLED
        self.checkButton.hide()
        self.checkButton['state'] = DGG.DISABLED
        self.claimButton.hide()
        self.claimButton['state'] = DGG.DISABLED
        self.mojoButton.hide()
        self.mojoButton['state'] = DGG.DISABLED
        self.cheatButton.hide()
        self.cheatButton['state'] = DGG.DISABLED
        self.betDice = 1
        self.betValue = 1
        self.oldDice = 1
        self.oldValue = 1
        self.cheatDetect = 0
        self.mojoDetect = 0
        if self.animPlaying == 0:
            self.diceNumText.hide()
            self.diceValText.hide()
            self.diceNumLabel.hide()
            self.diceValLabel.hide()
            self.diceValLabel.setPos(0.33, 0, -0.7)
            self.diceValText.setPos(0.27, 0, -0.5)
            self.diceNumText.setPos(-0.4, 0, -0.5)
            self.diceNumLabel.setPos(-0.28, 0, -0.7)
            self.diceNumLabel['text'] = '%d' % self.betDice
            self.diceValLabel['text'] = '%d' % self.betValue

    def notYourTurn(self):
        self.diceUpButton['state'] = DGG.DISABLED
        self.diceDownButton['state'] = DGG.DISABLED
        self.valueDownButton['state'] = DGG.DISABLED
        self.valueUpButton['state'] = DGG.DISABLED
        self.checkButton['frameColor'] = (1, 0.9, 0.6, 0.5)
        self.checkButton['state'] = DGG.DISABLED
        self.claimButton['frameColor'] = (0.2, 0.6, 0.1, 0.5)
        self.claimButton['state'] = DGG.DISABLED
        self.mojoButton['frameColor'] = (0.4, 0.6, 1.0, 0.5)
        self.mojoButton['state'] = DGG.DISABLED
        self.cheatButton['state'] = DGG.DISABLED
        self.cheatButton['frameColor'] = (1, 0.7, 0.5, 0.5)

    def useMojo(self):
        attempt = random.randint(0, 100) + self.mojoDetect
        if attempt < 60:
            base.localAvatar.setChatAbsolute('Mojo flows smoothly.', CFThought | CFTimeout)
            self.gui.bounceDie()
            self.mojoDetect += random.randint(0, 40)
            self.sendUpdate('cheatResult', [self.mySeat, self.betValue, 0])
        elif attempt < 80:
            base.localAvatar.setChatAbsolute('Your mojo twists.', CFThought | CFTimeout)
            self.mojoDetect += random.randint(0, 20)
            self.gui.bounceDie()
            self.sendUpdate('cheatResult', [self.mySeat, 0, 0])
        elif attempt < 120:
            base.localAvatar.setChatAbsolute('The Mojo works roughly.', CFThought | CFTimeout)
            self.mojoDetect += random.randint(0, 60)
            self.gui.bounceDie()
            self.sendUpdate('cheatResult', [self.mySeat, self.betValue, 2])
        else:
            base.localAvatar.setChatAbsolute('You botch the Mojo.', CFThought | CFTimeout)
            self.gui.bounceDie()
            self.mojoDetect = 150
            self.sendUpdate('cheatResult', [self.mySeat, 0, 4])

    def incomingCheat(self, seat, catchTime, dieV):
        if seat != self.mySeat:
            return
        if catchTime > 0:
            self.catchCheat['state'] = DGG.NORMAL
            rndr = random.randint(1, 4)
            if rndr == 1:
                self.catchCheat.setPos(0.84, 0, 0.84)
            elif rndr == 2:
                self.catchCheat.setPos(-0.84, 0, 0.84)
            elif rndr == 3:
                self.catchCheat.setPos(0.84, 0, -0.84)
            else:
                self.catchCheat.setPos(-0.84, 0, -0.84)
            self.catchCheat.show()
            taskMgr.doMethodLater(catchTime, self.doneCheating, 'doneCheat')
        if dieV > 0:
            self.gui.nudgeDie(random.randint(0, self.numDice - 1), dieV)
        else:
            self.gui.bounceDie()

    def doneCheating(self, task):
        self.catchCheat['state'] = DGG.DISABLED
        self.catchCheat.hide()

    def tryToCheat(self):
        attempt = random.randint(0, 100) + self.cheatDetect
        if attempt < 60:
            base.localAvatar.setChatAbsolute('You jostle the table.', CFThought | CFTimeout)
            self.cheatDetect += random.randint(0, 40)
            self.gui.nudgeDie(random.randint(0, self.numDice - 1), self.betValue)
            self.sendUpdate('cheatResult', [self.mySeat, 0, 0])
        elif attempt < 80:
            base.localAvatar.setChatAbsolute('You jostle the table.', CFThought | CFTimeout)
            self.cheatDetect += random.randint(0, 20)
            self.gui.bounceDie()
            self.sendUpdate('cheatResult', [self.mySeat, 0, 0])
        elif attempt < 120:
            base.localAvatar.setChatAbsolute('You roughly thump the table.', CFThought | CFTimeout)
            self.gui.nudgeDie(random.randint(0, self.numDice - 1), self.betValue)
            self.cheatDetect += random.randint(0, 60)
            self.sendUpdate('cheatResult', [self.mySeat, 0, 2])
        else:
            base.localAvatar.setChatAbsolute('You roughly thump the table.', CFThought | CFTimeout)
            self.gui.bounceDie()
            self.cheatDetect = 150
            self.sendUpdate('cheatResult', [self.mySeat, 0, 4])

    def makeClaim(self):
        if self.betDice > self.oldDice or self.betValue > self.oldValue:
            self.sendUpdate('betUpdate', [self.mySeat, self.betDice, self.betValue])
            self.notYourTurn()
        else:
            self.gui.gameStatus['text'] = PLocalizer.DiceText_LowBet

    def tableStatus(self, betDice, betValue):
        self.betDice = betDice
        self.oldDice = betDice
        self.betValue = betValue
        self.oldValue = betValue
        self.diceNumLabel['text'] = '%d' % self.betDice
        self.diceValLabel['text'] = '%d' % self.betValue
        if self.betDice > 9:
            self.diceNumLabel.setPos(-0.34, 0, -0.7)
        else:
            self.diceNumLabel.setPos(-0.28, 0, -0.7)

    def gotCaught(self, seat, name):
        if seat == self.mySeat:
            self.notYourTurn()
        self.gui.gameStatus['text'] = PLocalizer.DiceText_Caught % name

    def caughtYou(self):
        print 'DistributedLiarsDice:caughtYou'
        self.sendUpdate('catchCheater', [self.mySeat])

    def callBluff(self):
        if self.oldDice == 1 and self.oldValue == 1:
            self.gui.gameStatus['text'] = PLocalizer.DiceText_FirstClaim
        else:
            self.sendUpdate('callBluff', [self.mySeat, self.oldDice, self.oldValue])

    def displayChallenge(self, dieN, dieV, player1, player2, elimName):
        print 'Entering displayChallenge with %d dice' % len(self.challDice)
        self.animPlaying = 1
        self.extraGuiReset()
        self.diceNumText.setPos(0.6, 0, 0.4)
        self.diceNumLabel.setPos(0.7, 0, 0.2)
        self.diceValText.setPos(0.61, 0, 0.0)
        self.diceValLabel.setPos(0.7, 0, -0.2)
        self.diceValLabel.show()
        self.diceValText.show()
        self.diceNumLabel.show()
        self.diceNumText.show()
        self.diceNumLabel['text'] = '%d' % dieN
        self.diceValLabel['text'] = '%d' % dieV
        self.gui.gameStatus['text'] = '%s %s' % (elimName, PLocalizer.DiceText_Call)
        diceCount = 0
        curCount = 0
        for who, dlist in self.dicevals.iteritems():
            diceCount += dlist.count(dieV)
            counter = 0
            for i in range(len(dlist)):
                counter += 1
                die = loader.loadModel('models/props/dice')
                die.setScale(0.3)
                die.reparentTo(self)
                die.setHpr(self.gui.dieFace(dlist[i]))
                die.setPos(self.gui.HandPos[who])
                self.challDice.append(die)
                self.challDice[len(self.challDice) - 1].show()
                pos = Vec3(-5.0 + 1.2 * counter, -6.4 + 0.9 * who, DiceGlobals.PIT_HEIGHT + 5)
                lerp = LerpPosInterval(self.challDice[len(self.challDice) - 1], 3.0, pos, blendType='easeOut')
                if curCount == 0:
                    self.challSeq[curCount] = Sequence(lerp)
                    if dlist[i] == dieV:
                        func = Func(self.hiliteDice, curCount)
                        self.challSeq[curCount].append(func)
                    self.challSeq[curCount].append(Wait(6.0))
                    self.challSeq[curCount].append(Func(self.endChallenge))
                else:
                    self.challSeq[curCount] = Sequence(lerp)
                    if dlist[i] == dieV:
                        func = Func(self.hiliteDice, curCount)
                        self.challSeq[curCount].append(func)
                curCount += 1

        for i in range(0, curCount):
            self.challSeq[i].start()

        self.gui.gameStatus['text'] = '%s is Eliminated' % elimName

    def hiliteDice(self, dieN):
        retic = loader.loadModel('models/misc/sphere')
        retic.setColorScale(0.1, 0.7, 1.0, 1)
        retic.setScale(0.5, 0.5, 0.25)
        pos = self.challDice[dieN].getPos()
        pos2 = Vec3(pos[0], pos[1], pos[2] - 0.2)
        retic.reparentTo(self)
        retic.setPos(pos2)
        retic.show()
        self.challDice.append(retic)

    def endChallenge(self):
        i = len(self.challDice) - 1
        while i > -1:
            self.challDice[i].removeNode()
            del self.challDice[i]
            i -= 1

        self.challDice = []
        self.challSeq = {}
        if self.animPlaying == 2:
            if self.gui:
                self.gui.mainButton['state'] = DGG.NORMAL
                self.gui.mainButton['frameColor'] = (0.0, 0.8, 0.1, 1)
        self.animPlaying = 0
        self.diceValLabel.hide()
        self.diceValText.hide()
        self.diceNumLabel.hide()
        self.diceNumText.hide()
        self.diceValLabel.setPos(0.33, 0, -0.7)
        self.diceValText.setPos(0.27, 0, -0.5)
        self.diceNumText.setPos(-0.4, 0, -0.5)
        self.diceNumLabel.setPos(-0.28, 0, -0.7)
        self.diceNumLabel['text'] = '%d' % 1
        self.diceValLabel['text'] = '%d' % 1

    def youWin(self, winId, name):
        DistributedDiceGame.DistributedDiceGame.youWin(self, winId, name)
        if self.animPlaying:
            self.animPlaying = 2
            self.gui.mainButton['state'] = DGG.DISABLED
            self.gui.mainButton['frameColor'] = (0.0, 0.4, 0.05, 1)
        else:
            self.gui.mainButton['state'] = DGG.NORMAL
            self.gui.mainButton['frameColor'] = (0.0, 0.8, 0.1, 1)