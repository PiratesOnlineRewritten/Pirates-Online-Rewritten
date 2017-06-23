from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task import Task
from pirates.minigame import DiceGlobals
from pirates.minigame import PlayingCard
from pirates.piratesgui import GuiTray
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
import random
import math

class DiceGameGUI(DirectFrame):
    HandPos = (
     Vec3(-4.0, 3.5, DiceGlobals.PIT_HEIGHT), Vec3(-8.0, 0, DiceGlobals.PIT_HEIGHT), Vec3(-4.0, -4.5, DiceGlobals.PIT_HEIGHT), Vec3(0, -4.5, DiceGlobals.PIT_HEIGHT), Vec3(4.0, -4.5, DiceGlobals.PIT_HEIGHT), Vec3(8.0, 0, DiceGlobals.PIT_HEIGHT), Vec3(4.0, 3.5, DiceGlobals.PIT_HEIGHT))
    ArrowPosHpr = (
     (
      Vec3(-0.4, 0, 0.66), Vec3(0, 0, 90)), (Vec3(-0.82, 0, 0.33), Vec3(0, 0, 90)), (Vec3(-0.5, 0, -0.08), Vec3(0, 0, 90)), (Vec3(0, 0, -0.08), Vec3(0, 0, 90)), (Vec3(0.5, 0, -0.08), Vec3(0, 0, 90)), (Vec3(0.82, 0, 0.33), Vec3(0, 0, 90)), (Vec3(0.4, 0, 0.66), Vec3(0, 0, 90)))

    def __init__(self, table, numDice=12, public_roll=1, name='Dice Game'):
        DirectFrame.__init__(self, relief=None)
        self.numDice = numDice
        self.initialiseoptions(DiceGameGUI)
        self.hasRolled = False
        self.public = public_roll
        self.table = table
        self.arrow = loader.loadModel('models/gui/arrow')
        self.arrow.reparentTo(self)
        self.arrow.setScale(0.15)
        self.arrow.hide()
        self.menu = GuiTray.GuiTray(0.75, 0.2)
        self.menu.setPos(-0.4, 0, -1)
        self.dice = {}
        self.diceval = []
        self.finalPos = []
        self.lerpList = []
        self.gameLabel = DirectLabel(parent=self, relief=None, text=name, text_align=TextNode.ACenter, text_scale=0.15, pos=(-0.8, 0, 0.7), text_fg=(1,
                                                                                                                                                     1.0,
                                                                                                                                                     1.0,
                                                                                                                                                     1), text_shadow=(0,
                                                                                                                                                                      0,
                                                                                                                                                                      1.0,
                                                                                                                                                                      1))
        self.gameLabel.show()
        self.turnStatus = DirectLabel(parent=self, relief=None, text=PLocalizer.DiceText_Wait, text_align=TextNode.ALeft, text_scale=0.06, pos=(0.28,
                                                                                                                                                0,
                                                                                                                                                0.77), text_fg=(1,
                                                                                                                                                                0.9,
                                                                                                                                                                0.6,
                                                                                                                                                                1), text_shadow=(1.0,
                                                                                                                                                                                 0,
                                                                                                                                                                                 1.0,
                                                                                                                                                                                 1))
        self.turnStatus.show()
        self.gameStatus = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=0.06, pos=(0.28,
                                                                                                                          0,
                                                                                                                          0.69), text_fg=(1,
                                                                                                                                          0.9,
                                                                                                                                          0.6,
                                                                                                                                          1), text_shadow=(1.0,
                                                                                                                                                           0,
                                                                                                                                                           1.0,
                                                                                                                                                           1))
        self.gameStatus.show()
        self.mainButton = DirectButton(parent=self.menu, relief=DGG.RAISED, state=DGG.NORMAL, text='%s %d' % (PLocalizer.DiceText_Ante, self.table.ante), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, frameColor=(0.0,
                                                                                                                                                                                                                                                                                   0.8,
                                                                                                                                                                                                                                                                                   0.1,
                                                                                                                                                                                                                                                                                   1), frameSize=(0,
                                                                                                                                                                                                                                                                                                  0.3,
                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                  0.12), borderWidth=PiratesGuiGlobals.BorderWidth, text_pos=(0.1,
                                                                                                                                                                                                                                                                                                                                                              0.03), textMayChange=1, pos=(0.18,
                                                                                                                                                                                                                                                                                                                                                                                           0,
                                                                                                                                                                                                                                                                                                                                                                                           0.05), command=self.table.playerIsReady, extraArgs=[])
        self.exitButton = DirectButton(parent=self.menu, relief=DGG.RAISED, text='X', text_align=TextNode.ACenter, text_scale=0.04, text_pos=(0.02,
                                                                                                                                              0.01), text_fg=(0.75,
                                                                                                                                                              0.75,
                                                                                                                                                              0.75,
                                                                                                                                                              1), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, frameColor=PiratesGuiGlobals.ButtonColor1, borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameSize=(0,
                                                                                                                                                                                                                                                                                                                                   0.04,
                                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                                   0.04), pos=(0.75 - 0.01 - 0.04, 0, 0.01), command=self.table.guiCallback, extraArgs=[-1])
        return

    def showArrow(self, seatIndex):
        pos, hpr = self.ArrowPosHpr[seatIndex]
        self.arrow.setPosHpr(pos, hpr)
        self.arrow.show()

    def hideArrow(self):
        self.arrow.hide()

    def enableAction(self):
        self.mainButton['state'] = DGG.NORMAL

    def disableAction(self):
        self.mainButton['state'] = DGG.DISABLED

    def timeToRoll(self):
        self.mainButton['state'] = DGG.NORMAL
        self.mainButton['command'] = self.rollDice
        self.mainButton['extraArgs'] = []
        self.mainButton['text'] = 'ROLL DICE'
        self.mainButton['frameColor'] = (0, 0.6, 0.8, 1)

    def rollDice(self):
        self.table.sendChat(DiceGlobals.CHAT_ROLL)
        self.mainButton['state'] = DGG.DISABLED
        self.mainButton.hide()
        self.accept('mouse1', self.startRoll, extraArgs=[])
        self.mousePath = {}

    def startRoll(self):
        self.ignore('mouse1')
        self.accept('mouse1-up', self.doTheRoll, extraArgs=[])
        if base.mouseWatcherNode.hasMouse():
            mouseData = base.win.getPointer(0)
            self.MouseInitialPosX = mouseData.getX()
            self.MouseInitialPosY = mouseData.getY()
        else:
            self.MouseInitialPosX = 0
            self.MouseInitialPosY = 0
        self.MouseStartTime = time.time()

    def loadDie(self, dienum):
        self.dice[dienum] = loader.loadModel('models/props/dice')
        self.dice[dienum].setScale(0.3)
        self.dice[dienum].reparentTo(self.table)
        startX = 0.0 + -0.2 * dienum + random.random() * dienum * 0.4
        startY = 0.0 + -0.2 * dienum + random.random() * dienum * 0.4
        pos1 = Vec3(startX, startY, DiceGlobals.PIT_HEIGHT)
        self.dice[dienum].setPos(pos1)
        self.dice[dienum].setHpr(self.randomFace())
        print 'DiceGameGUI:loadDie - loaded die %d with value %d' % (dienum, self.diceval[dienum])

    def doTheRoll(self):
        if self.table.gameState != DiceGlobals.DSTATE_DOROLL:
            return
        self.ignore('mouse1-up')
        taskMgr.remove(self.taskName('turnStatusStep'))
        if base.mouseWatcherNode.hasMouse():
            mouseData = base.win.getPointer(0)
            self.MouseFinalPosX = mouseData.getX()
            self.MouseFinalPosY = mouseData.getY()
        else:
            self.MouseFinalPosX = 0
            self.MouseFinalPosY = 0
        self.MouseEndTime = time.time()
        self.MouseTimeDiff = self.MouseEndTime - self.MouseStartTime
        print 'DiceGameGUI: rolling times %f and %f' % (self.MouseStartTime, self.MouseEndTime)
        print 'DiceGameGUI: difference of %f' % self.MouseTimeDiff
        self.table.gameState = DiceGlobals.DSTATE_WAIT
        del self.diceval
        self.diceval = []
        for i in range(self.numDice):
            self.diceval.append(random.randint(1, 6))
            self.finalPos.append([0, 0])
            self.loadDie(i)

        val1 = 0.0 + self.MouseFinalPosX
        val1 -= self.MouseInitialPosX
        val1 /= DiceGlobals.MOUSE_SCALE
        val2 = 0.0 + self.MouseInitialPosY
        val2 -= self.MouseFinalPosY
        val2 /= DiceGlobals.MOUSE_SCALE
        speed = self.MouseTimeDiff * 10
        if speed < 0.6:
            speed = 0.6
        if speed > 2.5:
            speed = 2.5
        for i in range(self.numDice):
            self.lerpList.append([])

        for i in range(self.numDice):
            tmpvec = self.finalRest(i, val1, val2, 0, False)
            self.diceVectorCalc(i, speed, self.finalPos[i][0], self.finalPos[i][1], self.dice[i].getPos())

        self.diceSeqs = []
        for i in range(self.numDice):
            seq = Sequence(self.lerpList[i][0])
            for h in range(1, len(self.lerpList[i])):
                seq.append(self.lerpList[i][h])

            if i == 0:
                func = Func(self.sendRoll)
                seq.append(func)
            seq.start()

        self.hasRolled = True

    def sendRoll(self):
        self.table.sendUpdate('playerHasRolled', [self.table.mySeat, self.diceval])

    def randomFace(self):
        tmp1 = random.randint(-179, 180)
        tmp2 = random.randint(-179, 180)
        tmp3 = random.randint(-179, 180)
        return Vec3(tmp1, tmp2, tmp3)

    def dieFace(self, val):
        if val == 1:
            return DiceGlobals.DICE_FACE_1
        elif val == 2:
            return DiceGlobals.DICE_FACE_2
        elif val == 3:
            return DiceGlobals.DICE_FACE_3
        elif val == 4:
            return DiceGlobals.DICE_FACE_4
        elif val == 5:
            return DiceGlobals.DICE_FACE_5
        elif val == 6:
            return DiceGlobals.DICE_FACE_6

    def resetGui(self):
        if self.hasRolled:
            for diei in range(self.numDice):
                self.dice[diei].removeNode()
                del self.dice[diei]

        self.dice = {}
        self.hasRolled = False

    def destroy(self):
        del self.table
        self.arrow.removeNode()
        del self.arrow
        if self.hasRolled:
            for diei in range(self.numDice):
                self.dice[diei].removeNode()
                del self.dice[diei]

            del self.lerpList
            self.lerpList = []
        self.dice = {}
        self.mainButton.destroy()
        self.exitButton.destroy()
        self.menu.destroy()
        self.gameLabel.destroy()
        self.gameStatus.destroy()
        self.turnStatus.destroy()
        DirectFrame.destroy(self)

    def diceVectorCalc(self, dienum, timeSlice, xforce, yforce, startPos):
        if xforce > -0.01 and xforce < 0.01:
            xforce = 0.01
        if yforce > -0.01 and yforce < 0.01:
            yforce = 0.01
        distance = math.sqrt((xforce - startPos[0]) * (xforce - startPos[0]) + (yforce - startPos[1]) * (yforce - startPos[1]))
        Yslope = 0.0 + (yforce - startPos[1]) / (xforce - startPos[0])
        Xslope = 0.0 + (xforce - startPos[0]) / (yforce - startPos[1])
        CY = yforce - Yslope * xforce
        CX = xforce - Xslope * yforce
        wallDist = 99999.0
        newX = 0.0
        newY = 0.0
        oldX = 0.0
        oldY = 0.0
        oldTime = 0.0
        newTime = 0.0
        if xforce > DiceGlobals.PIT_X_MAX:
            print 'DiceGameGUI: Die %d Hit Right Wall' % dienum
            oldX = DiceGlobals.PIT_X_MAX
            oldY = 0.0 + Yslope * oldX + CY
            wallDist = math.sqrt((oldX - startPos[0]) * (oldX - startPos[0]) + (oldY - startPos[1]) * (oldY - startPos[1]))
            oldTime = timeSlice
            oldTime *= wallDist
            oldTime /= distance
            newTime = timeSlice - oldTime
            newX = DiceGlobals.PIT_X_MAX - (xforce - DiceGlobals.PIT_X_MAX)
            newY = yforce
        elif xforce < DiceGlobals.PIT_X_MIN:
            print 'DiceGameGUI: Die %d Hit Left wall' % dienum
            oldX = DiceGlobals.PIT_X_MIN
            oldY = 0.0 + Yslope * oldX + CY
            wallDist = math.sqrt((oldX - startPos[0]) * (oldX - startPos[0]) + (oldY - startPos[1]) * (oldY - startPos[1]))
            oldTime = timeSlice
            oldTime *= wallDist
            oldTime /= distance
            newTime = timeSlice - oldTime
            newX = DiceGlobals.PIT_X_MIN + (DiceGlobals.PIT_X_MIN - xforce)
            newY = yforce
        if yforce > DiceGlobals.PIT_Y_MAX:
            possY = DiceGlobals.PIT_Y_MAX
            possX = 0.0 + Xslope * possY + CX
            possDist = math.sqrt((possX - startPos[0]) * (possX - startPos[0]) + (possY - startPos[1]) * (possY - startPos[1]))
            if possDist < wallDist:
                print 'DiceGameGUI: Die %d Hit Top Wall' % dienum
                oldX = possX
                oldY = possY
                wallDist = possDist
                oldTime = timeSlice
                oldTime *= wallDist
                oldTime /= distance
                newTime = timeSlice - oldTime
                newX = xforce
                newY = DiceGlobals.PIT_Y_MAX - (yforce - DiceGlobals.PIT_Y_MAX)
        elif yforce < DiceGlobals.PIT_Y_MIN:
            possY = DiceGlobals.PIT_Y_MIN
            possX = 0.0 + Xslope * possY + CX
            possDist = math.sqrt((possX - startPos[0]) * (possX - startPos[0]) + (possY - startPos[1]) * (possY - startPos[1]))
            if possDist < wallDist:
                print 'DiceGameGUI: Die %d Hit Bottom Wall' % dienum
                oldX = possX
                oldY = possY
                wallDist = possDist
                oldTime = timeSlice
                oldTime *= wallDist
                oldTime /= distance
                newTime = timeSlice - oldTime
                newX = xforce
                newY = DiceGlobals.PIT_Y_MIN - yforce + DiceGlobals.PIT_Y_MIN
        if wallDist != 99999.0:
            pos2 = Vec3(oldX, oldY, DiceGlobals.PIT_HEIGHT)
            hpr = self.randomFace()
            lerp = LerpPosHprInterval(self.dice[dienum], oldTime, pos2, hpr, blendType='noBlend')
            self.lerpList[dienum].append(lerp)
            newTime += random.random() * (newTime / 6.0)
            newTime += newTime / 4.0
            self.diceVectorCalc(dienum, newTime, newX, newY, pos2)
        else:
            pos2 = self.finalRest(dienum, xforce, yforce, DiceGlobals.PIT_HEIGHT)
            hpr = self.dieFace(self.diceval[dienum])
            lerp = LerpPosHprInterval(self.dice[dienum], timeSlice, pos2, hpr, blendType='easeOut')
            self.lerpList[dienum].append(lerp)
            self.lerpList[dienum].append(Wait(2.0))
            leftPt = 0.0 - (self.numDice - 1) / 2
            dieX = dienum + leftPt
            guiPos = Vec3(dieX, 0, DiceGlobals.PIT_HEIGHT + 1)
            lerp = LerpPosInterval(self.dice[dienum], 1.5, guiPos, blendType='easeOut')
            self.lerpList[dienum].append(lerp)

    def bounceDie(self):
        for i in range(self.numDice):
            if random.randint(0, 99) < 50:
                self.bounceOne(i)

    def bounceOne(self, dieN):
        hpr = self.dice[dieN].getHpr()
        hp0 = hpr[0] - 45
        hp0 += random.random() * 90
        hp1 = hpr[1] - 45
        hp1 += random.random() * 90
        hp2 = hpr[2] - 45
        hp2 += random.random() * 90
        hpr = Vec3(hp0, hp1, hp2)
        wait = random.random() * 0.2
        lerp = LerpHprInterval(self.dice[dieN], 0.2, hpr)
        hpr = self.dieFace(self.diceval[dieN])
        lerp2 = LerpHprInterval(self.dice[dieN], 0.3, hpr)
        seq = Sequence(Wait(wait), lerp, lerp2)
        seq.start()

    def nudgeDie(self, dieN, dieV):
        for i in range(self.numDice):
            if i != dieN and random.randint(0, 99) < 70:
                self.bounceOne(i)

        self.diceval[dieN] = dieV
        self.table.sendUpdate('changeDice', [self.table.mySeat, self.diceval])
        hpr = self.dieFace(dieV)
        lerp = LerpHprInterval(self.dice[dieN], 0.5, hpr)
        lerp.start()

    def finalRest(self, dieN, xpos, ypos, zpos, edge=True):
        loop = True
        while loop:
            loop = False
            if edge:
                if xpos > DiceGlobals.PIT_X_MAX:
                    xpos -= random.random() * 1.0
                    loop = True
                if xpos < DiceGlobals.PIT_X_MIN:
                    xpos += random.random() * 1.0
                    loop = True
                if ypos > DiceGlobals.PIT_Y_MAX:
                    ypos -= random.random() * 1.0
                    loop = True
                if ypos < DiceGlobals.PIT_Y_MIN:
                    ypos += random.random() * 1.0
                    loop = True
            for i in range(self.numDice):
                if i != dieN:
                    if xpos - self.finalPos[i][0] < DiceGlobals.SPACE and xpos - self.finalPos[i][0] > -DiceGlobals.SPACE and ypos - self.finalPos[i][1] < DiceGlobals.SPACE and ypos - self.finalPos[i][1] > -DiceGlobals.SPACE:
                        xpos -= 1.0
                        xpos += random.random() * 2.0
                        ypos -= 1.0
                        ypos += random.random() * 2.0
                        loop = True

        self.finalPos[dieN][0] = xpos
        self.finalPos[dieN][1] = ypos
        return Vec3(xpos, ypos, zpos)

    def turnStatusStep(self, task=None):
        if self.taskStep < 10:
            self.turnStatus['text_scale'] = 0.06 + 0.002 * self.taskStep
            self.turnStatus['text_fg'] = (1, 0.9, 0.6 - self.taskStep * 0.05, 1)
            self.turnStatus.setPos(0.28 - 0.01 * self.taskStep, 0, 0.77)
        elif self.taskStep < 20:
            self.turnStatus['text_scale'] = 0.06 + 0.002 * (19 - self.taskStep)
            self.turnStatus['text_fg'] = (1, 0.9, 0.6 - (19 - self.taskStep) * 0.05, 1)
            self.turnStatus.setPos(0.28 - 0.01 * (19 - self.taskStep), 0, 0.77)
        else:
            return Task.done
        self.taskStep += 1
        return Task.cont

    def updateTurnStatus(self, text):
        self.taskStep = 0
        taskMgr.add(self.turnStatusStep, self.taskName('turnStatusStep'), priority=40)
        self.turnStatus['text'] = text