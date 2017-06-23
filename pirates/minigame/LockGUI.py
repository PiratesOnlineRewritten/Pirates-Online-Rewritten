import random
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.minigame import PlayingCardGlobals
from pirates.minigame import PlayingCard
from pirates.piratesgui import GuiTray
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import PiratesTimer
from pirates.reputation import DistributedReputationAvatar
from pirates.minigame import LockGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class LockGUI(DirectFrame):

    def __init__(self, table, avId, difficulty=10):
        DirectFrame.__init__(self, relief=None)
        self.initialiseoptions(LockGUI)
        self.table = table
        self.difficulty = difficulty
        self.numLayers = difficulty / 10
        if self.numLayers < 1:
            self.numLayers = 1
        if self.numLayers > 6:
            self.numLayers = 6
        self.currentLayer = 1
        self.mechVal = 0
        self.lockMech = 0
        self.mechZPos = LockGlobals.StartZPos
        self.mechXPos = LockGlobals.StartXPos
        self.lockZPos = LockGlobals.LockZPos
        self.lockXPos = LockGlobals.LockXPos
        self.layerZPos = LockGlobals.LockZPos
        self.layerXPos = LockGlobals.LockXPos
        self.mechDir = 1
        self.lockSpeed = LockGlobals.StartSpeed
        self.lockSpeed += self.difficulty / 50
        self.toolState = LockGlobals.LSTATE_ACTIVE
        self.unlockSound = loadSfx(SoundGlobals.SFX_LOCKPICK_SUCCESS)
        self.missSound = loadSfx(SoundGlobals.SFX_LOCKPICK_FAIL)
        self.trySound = loadSfx(SoundGlobals.SFX_LOCKPICK_TRY)
        self.layerModel = loader.loadModel('models/props/Keys')
        print 'Found ', self.layerModel
        self.layerImage = self.layerModel.find('**/Lock_L')
        print 'Found ', self.layerImage
        self.layerImage.reparentTo(self)
        self.layerImage.setPos(0, 50, 0)
        self.layerImage.setScale(1.0)
        self.layerImage.show()
        self.mechLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.LockMechanism, text_align=TextNode.ALeft, text_scale=0.09, pos=(-0.4, 0, -0.7), text_fg=(1,
                                                                                                                                                                        0.9,
                                                                                                                                                                        0.6,
                                                                                                                                                                        1), text_shadow=(0,
                                                                                                                                                                                         0,
                                                                                                                                                                                         0,
                                                                                                                                                                                         1))
        self.mechNode = self.attachNewNode('mechNode')
        self.mechNode.setScale(0.5)
        self.mechNode.setPos(0, 0, 0.2)
        self.mechImage = PlayingCard.PlayingCardNodePath('standard', 13)
        self.mechImage.reparentTo(self.mechNode)
        self.mechImage.setPos(0.6, 0, -1.72)
        self.mechImage.show()
        self.mechTool = PlayingCard.PlayingCardNodePath('standard', 13)
        self.mechTool.reparentTo(self.mechNode)
        self.mechTool.setPos(self.mechXPos, 0, self.mechZPos)
        self.mechTool.show()
        self.lockImage = {}
        self.lockImage[self.currentLayer] = PlayingCard.PlayingCardNodePath('standard', 13)
        self.lockImage[self.currentLayer].reparentTo(self.mechNode)
        self.lockImage[self.currentLayer].setPos(LockGlobals.LockXPos, 0, LockGlobals.LockZPos)
        self.setLockMech(random.randint(0, LockGlobals.MaxTool))
        self.lockImage[self.currentLayer].show()
        self.mechLeftButton = DirectButton(parent=self, relief=DGG.RAISED, text='<', text_align=TextNode.ACenter, text_scale=0.05, text_pos=(0.02,
                                                                                                                                             0.01), text_fg=(0,
                                                                                                                                                             0,
                                                                                                                                                             0,
                                                                                                                                                             1), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, frameColor=PiratesGuiGlobals.ButtonColor2, borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameSize=(0,
                                                                                                                                                                                                                                                                                                                                  0.05,
                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                  0.05), pos=(0.13, 0, -0.7), command=self.table.guiCallback, extraArgs=[LockGlobals.LGUI_MECHLEFT])
        self.mechRightButton = DirectButton(parent=self, relief=DGG.RAISED, text='>', text_align=TextNode.ACenter, text_scale=0.05, text_pos=(0.02,
                                                                                                                                              0.01), text_fg=(0,
                                                                                                                                                              0,
                                                                                                                                                              0,
                                                                                                                                                              1), text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, frameColor=PiratesGuiGlobals.ButtonColor2, borderWidth=PiratesGuiGlobals.BorderWidthSmall, frameSize=(0,
                                                                                                                                                                                                                                                                                                                                   0.05,
                                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                                   0.05), pos=(0.42, 0, -0.7), command=self.table.guiCallback, extraArgs=[LockGlobals.LGUI_MECHRIGHT])
        self.timer = PiratesTimer.PiratesTimer()
        self.timer.posInTopRightCorner()
        self.timer.show()
        self.timer.countdown(60, self.gameTimerExpired)
        return

    def setLockMech(self, newLockMech):
        self.lockMech = newLockMech
        self.lockImage[self.currentLayer].setValue(13 + self.lockMech)
        self.lockImage[self.currentLayer].setImage()

    def adjustMechanism(self, mechChange):
        if self.toolState == LockGlobals.LSTATE_ACTIVE or self.toolState == LockGlobals.LSTATE_RESET:
            self.mechVal = self.mechVal + mechChange
            if self.mechVal < 0:
                self.mechVal = LockGlobals.MaxTool
            elif self.mechVal > LockGlobals.MaxTool:
                self.mechVal = 0
            self.mechImage.setValue(13 + self.mechVal)
            self.mechImage.setImage()
            self.mechTool.setValue(13 + self.mechVal)
            self.mechTool.setImage()

    def gameTimerExpired(self):
        print 'LockGUI:gameTimerExpired'
        if self.toolState != LockGlobals.LSTATE_OPEN:
            self.toolState = LockGlobals.LSTATE_DONE
            self.solveLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.LockpickFailed, text_align=TextNode.ACenter, text_scale=0.2, pos=(0,
                                                                                                                                                      0,
                                                                                                                                                      0), text_fg=(1,
                                                                                                                                                                   1,
                                                                                                                                                                   1,
                                                                                                                                                                   1), text_shadow=(0,
                                                                                                                                                                                    0,
                                                                                                                                                                                    0,
                                                                                                                                                                                    1))
            self.solveLabel.show()
        return

    def tryLock(self):
        print 'LockGUI:tryLock'
        if self.toolState == LockGlobals.LSTATE_ACTIVE:
            self.toolState = LockGlobals.LSTATE_TRY
            base.playSfx(self.trySound)

    def mechMove(self):
        self.mechXPos += 0.01 * self.mechDir * self.lockSpeed
        if self.mechXPos > 1.99:
            self.mechDir *= -1
        elif self.mechXPos < -1.99:
            self.mechDir *= -1

    def lockHeartbeat(self):
        if self.toolState == LockGlobals.LSTATE_ACTIVE:
            self.mechMove()
        elif self.toolState == LockGlobals.LSTATE_TRY:
            if self.mechZPos < LockGlobals.LockZPos - 0.3:
                self.mechZPos += 0.01
            elif self.lockMech != self.mechVal or self.mechXPos > 0.05 or self.mechXPos < -0.05:
                self.toolState = LockGlobals.LSTATE_FAIL
                base.playSfx(self.missSound)
            elif self.mechZPos < LockGlobals.LockXPos - 0.1:
                self.mechZPos += 0.01
            else:
                self.layerOpen()
                self.lockSpeed += 0.1 * random.randint(0, 8)
        elif self.toolState == LockGlobals.LSTATE_FAIL:
            if self.mechZPos > LockGlobals.StartZPos:
                self.mechZPos -= 0.01
            else:
                self.toolState = LockGlobals.LSTATE_ACTIVE
        elif self.toolState == LockGlobals.LSTATE_RESET:
            if self.mechZPos > LockGlobals.StartZPos:
                self.mechZPos -= 0.01
            if self.layerZPos < LockGlobals.LayerZPos:
                self.layerZPos += 0.015
            elif self.layerXPos > LockGlobals.LayerXPos + self.currentLayer * 0.25:
                self.layerXPos -= 0.015
            if self.lockXPos > LockGlobals.LockXPos:
                self.lockXPos -= 0.015
            else:
                if self.lockZPos > LockGlobals.LockZPos:
                    self.lockZPos -= 0.015
                else:
                    self.toolState = LockGlobals.LSTATE_ACTIVE
                if self.mechZPos > LockGlobals.StartZPos:
                    self.mechZPos -= 0.01
                self.mechMove()
            self.lockImage[self.currentLayer].setPos(self.lockXPos, 0, self.lockZPos)
            self.lockImage[self.currentLayer - 1].setPos(self.layerXPos, 0, self.layerZPos)
        self.mechTool.setPos(self.mechXPos, 0, self.mechZPos)

    def lockOpen(self, name):
        print 'LockGUI:lockOpen'
        self.timer.stop()
        self.solveLabel = DirectLabel(parent=self, relief=None, text=PLocalizer.UnlockedBy, text_align=TextNode.ACenter, text_scale=0.2, pos=(0,
                                                                                                                                              0,
                                                                                                                                              0), text_fg=(1,
                                                                                                                                                           1,
                                                                                                                                                           1,
                                                                                                                                                           1), text_shadow=(0,
                                                                                                                                                                            0,
                                                                                                                                                                            0,
                                                                                                                                                                            1))
        self.solveLabel.show()
        self.solveLabel2 = DirectLabel(parent=self, relief=None, text=name, text_align=TextNode.ACenter, text_scale=0.2, pos=(0, 0, -0.3), text_fg=(1,
                                                                                                                                                    1,
                                                                                                                                                    1,
                                                                                                                                                    1), text_shadow=(0,
                                                                                                                                                                     0,
                                                                                                                                                                     0,
                                                                                                                                                                     1))
        self.solveLabel2.show()
        self.toolState = LockGlobals.LSTATE_OPEN
        return

    def layerOpen(self):
        if self.currentLayer == self.numLayers:
            self.toolState = LockGlobals.LSTATE_OPEN
            self.timer.stop()
            base.playSfx(self.unlockSound)
            avId = base.localAvatar.getDoId()
            self.table.sendUpdate('d_openLock', [base.localAvatar.name, avId])
        else:
            self.toolState = LockGlobals.LSTATE_RESET
            base.playSfx(self.unlockSound)
            self.lockXPos = LockGlobals.NewXPos
            self.lockZPos = LockGlobals.NewZPos
            self.layerXPos = LockGlobals.LockXPos
            self.layerZPos = LockGlobals.LockZPos
            self.currentLayer += 1
            self.lockImage[self.currentLayer] = PlayingCard.PlayingCardNodePath('standard', 13 + self.lockMech)
            self.lockImage[self.currentLayer].reparentTo(self.mechNode)
            self.lockImage[self.currentLayer].setPos(LockGlobals.NewXPos, 0, LockGlobals.NewZPos)
            self.setLockMech(random.randint(0, LockGlobals.MaxTool))
            self.lockImage[self.currentLayer].show()

    def destroy(self):
        del self.table
        self.timer.destroy()
        del self.timer
        del self.unlockSound
        del self.missSound
        del self.trySound
        DirectFrame.destroy(self)