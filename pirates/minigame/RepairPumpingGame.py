import random
from pandac.PandaModules import TextNode, CardMaker
from direct.gui.DirectGui import DirectLabel
from direct.task import Task
from direct.interval.LerpInterval import LerpFunc
from RepairMincroGame import RepairMincroGame
from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import RepairGlobals
from pirates.piratesbase import PiratesGlobals
ROTATION_MAX = -45
ROTATION_MIN = 45
UP = 1
DOWN = -1
TOP = 1
BOTTOM = 0
WATER_LEVEL_START = 1.05
WATER_LEVEL_DONE = 0.12

class RepairPumpingGame(RepairMincroGame):
    pumpDownSounds = None
    pumpUpSounds = None
    pumpGoodSounds = None
    pumpBadSounds = None

    def __init__(self, repairGame):
        self.config = RepairGlobals.Pumping
        RepairMincroGame.__init__(self, repairGame, 'pumping', PLocalizer.Minigame_Repair_Pumping_Start)

    def _initVars(self):
        RepairMincroGame._initVars(self)
        self.pumpRate = 0.0
        self.remainingWater = 1.0
        self.chainCount = 0
        self.barDirection = UP
        self.goalIndex = TOP
        self.currentBarRate = self.config.barStartRange[0]
        self.hitRange = self.config.hitRange[0]
        self.barPercent = 0.0
        self.failedPercentAndDirection = (-1.0, UP)

    def _initAudio(self):
        RepairMincroGame._initAudio(self)
        if not self.pumpDownSounds:
            RepairPumpingGame.pumpDownSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_DOWN01), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_DOWN02), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_DOWN03))
            RepairPumpingGame.pumpUpSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_UP01), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_UP02), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_UP03))
            RepairPumpingGame.pumpGoodSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_GOOD01), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_GOOD02), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_GOOD03), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_GOOD04), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_GOOD05), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_GOOD06))
            RepairPumpingGame.pumpBadSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PUMP_BAD),)

    def _initVisuals(self):
        RepairMincroGame._initVisuals(self)
        self.model = loader.loadModel('models/gui/pir_m_gui_srp_pumping_main')
        self.visual = self.attachNewNode('visual')
        self.visual.setPos(-0.25, 0.0, 0.075)
        goalTopLoc = self.model.find('**/locator_top')
        goalTopLoc.reparentTo(self.visual)
        goalBottomLoc = self.model.find('**/locator_bottom')
        goalBottomLoc.reparentTo(self.visual)
        self.goalPositions = (goalBottomLoc.getPos(self), goalTopLoc.getPos(self))
        self.greatLabel = DirectLabel(text=PLocalizer.Minigame_Repair_Pumping_Great, text_fg=(0.2,
                                                                                              0.8,
                                                                                              0.3,
                                                                                              1.0), text_pos=(0.0,
                                                                                                              0.6), text_align=TextNode.ACenter, text_font=PiratesGlobals.getPirateFont(), relief=None, text_shadow=(0.0,
                                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                                     1.0), scale=(0.08,
                                                                                                                                                                                                                                  0.08,
                                                                                                                                                                                                                                  0.08), pos=(-0.465, 0.0, 0.0), parent=self)
        self.failLabel = DirectLabel(text=PLocalizer.Minigame_Repair_Pumping_Fail, text_fg=(0.8,
                                                                                            0.2,
                                                                                            0.3,
                                                                                            1.0), text_pos=(0.0,
                                                                                                            0.6), text_align=TextNode.ARight, text_font=PiratesGlobals.getPirateFont(), text_shadow=(0.0,
                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                     1.0), relief=None, scale=(0.08,
                                                                                                                                                                                                                               0.08,
                                                                                                                                                                                                                               0.08), pos=(-0.625, 0.0, 0.0), parent=self)
        self.shipBackground = self.model.find('**/static_ship_background')
        self.shipBackground.reparentTo(self.visual)
        self.waterMeter = self.model.find('**/sprite_waterBottom')
        self.waterMeter.reparentTo(self.visual)
        self.waterTop = self.model.find('**/sprite_waterTop')
        self.waterTop.reparentTo(self.visual)
        self.waterMeterTopLoc = self.waterMeter.find('**/locator_topOfShipWater')
        self.pumpBackground = self.model.find('**/pumpBackground')
        self.pumpBackground.reparentTo(self.visual)
        self.pumpWaterTop = self.model.find('**/sprite_pumpWaterTop')
        self.pumpWaterTop.reparentTo(self.visual)
        self.pumpWaterBottom = self.model.find('**/sprite_pumpWaterBottom')
        self.pumpWaterBottom.reparentTo(self.visual)
        self.pumpWaterTopLoc = self.pumpWaterBottom.find('**/locator_topOfPumpWater')
        self.pumpHandle = self.model.find('**/sprite_handle')
        self.pumpHandle.reparentTo(self.visual)
        self.pumpBar = self.model.find('**/static_pump')
        self.pumpBar.reparentTo(self.visual)
        self.goalBox = self.model.find('**/sprite_clickField')
        self.goalBox.reparentTo(self.visual)
        self.goalBox.setTransparency(1)
        self.enableGoalBox()
        self.pumpLine = self.model.find('**/sprite_bar')
        self.pumpLine.reparentTo(self.visual)
        self.ghostLine = self.visual.attachNewNode('ghostLine')
        self.pumpLine.getChild(0).copyTo(self.ghostLine)
        self.ghostLine.setScale(self.pumpLine.getScale())
        self.ghostLine.setColor(1.0, 0.2, 0.2, 1.0)
        self.shipForground = self.model.find('**/static_ship_foreground')
        self.shipForground.reparentTo(self.visual)
        cm = CardMaker('cardMaker')
        cm.setFrame(-0.33, 0.33, 0.0, 1.0)
        self.goalBox.setZ(self.goalPositions[TOP].getZ())
        self.goalBoxStartScale = self.goalBox.getSz()
        self.enableGoalBox()
        self.pumpWaterUpLerp = LerpFunc(self.setPumpWater, fromData=-0.1, toData=1.0, duration=0.5)
        self.pumpWaterDownLerp = LerpFunc(self.setPumpWater, fromData=1.0, toData=-0.1, duration=0.5)
        self.model.removeNode()
        del self.model
        return

    def destroy(self):
        del self.goalPositions
        self.pumpBar.removeNode()
        self.pumpLine.removeNode()
        self.goalBox.removeNode()
        self.pumpHandle.removeNode()
        self.waterMeter.removeNode()
        self.waterTop.removeNode()
        self.ghostLine.removeNode()
        self.shipBackground.removeNode()
        self.shipForground.removeNode()

    def reset(self):
        RepairMincroGame.reset(self)
        self.remainingWater = WATER_LEVEL_START
        self.chainCount = 0
        self.barDirection = UP
        self.goalIndex = TOP
        self.barPercent = 0.0
        self.failedPercentAndDirection = (-1.0, UP)
        actualZ = self.goalPositions[BOTTOM].getZ()
        actualZ -= self.visual.getZ()
        self.pumpLine.setZ(actualZ)
        self.setGoalIndex(TOP)
        self.pumpHandle.setR(ROTATION_MIN)
        self.waterMeter.setSz(WATER_LEVEL_START)
        self.waterTop.setZ(self.waterMeterTopLoc.getZ(self.visual))
        self.ghostLine.stash()
        self.setPumpWater(1.0)
        self.failLabel.stash()
        self.greatLabel.stash()
        self.repairGame.gui.setTutorial(self.name)
        self.repairGame.gui.setTitle(self.name)

    def setDifficulty(self, difficulty):
        RepairMincroGame.setDifficulty(self, difficulty)
        percent = difficulty / self.repairGame.difficultyMax
        dif = self.config.pumpPowerRange[0] - self.config.pumpPowerRange[1]
        self.pumpRate = self.config.pumpPowerRange[0] - dif * percent
        dif = self.config.barStartRange[0] - self.config.barStartRange[1]
        self.currentBarRate = self.config.barStartRange[0] - dif * percent
        dif = self.config.hitRange[0] - self.config.hitRange[1]
        self.hitRange = self.config.hitRange[0] - dif * percent
        self.goalBox.setSz(self.hitRange / 0.18 * self.goalBoxStartScale)

    def setGoalIndex(self, goalIndex):
        self.goalIndex = goalIndex
        self.goalBox.setZ(self, self.goalPositions[goalIndex].getZ())
        self.goalBox.setR(180 * (goalIndex - 1))

    def resetFail(self):
        self.failedPercentAndDirection = (
         -1.0, UP)
        self.enableGoalBox()
        self.hideMarkers()

    def updateTask(self, task):
        dt = globalClock.getDt()
        percentTimeThisStep = dt / (self.currentBarRate + self.config.barSpeedMax)
        self.barPercent = self.barPercent + percentTimeThisStep * self.barDirection
        if self.failedPercentAndDirection[0] >= 0.0:
            if self.failedPercentAndDirection[1] != self.barDirection:
                if self.failedPercentAndDirection[0] * self.barDirection < self.barPercent * self.barDirection:
                    self.resetFail()
        if self.barPercent >= 1.0:
            self.barPercent = 1.0
            self.barDirection = DOWN
            if not self.isLineInBox():
                self.chainCount = 0
            if self.failedPercentAndDirection[0] < 0.5:
                self.resetFail()
        elif self.barPercent <= 0.0:
            self.barPercent = 0.0
            self.barDirection = UP
            if not self.isLineInBox():
                self.chainCount = 0
            if self.failedPercentAndDirection[0] > 0.5:
                self.resetFail()
        actualZ = self.goalPositions[0].getZ() + (self.goalPositions[1].getZ() - self.goalPositions[0].getZ()) * self.barPercent
        actualZ -= self.visual.getZ()
        self.pumpLine.setZ(actualZ)
        return Task.cont

    def enableGoalBox(self):
        self.goalBox.setColor(0.2, 1.0, 0.2, 0.6)
        self.goalBoxEnabled = 1

    def disableGoalBox(self):
        self.goalBox.setColor(1.0, 0.2, 0.2, 0.3)
        self.goalBoxEnabled = 0

    def isLineInBox(self):
        if self.goalIndex == TOP:
            return self.barPercent >= 1.0 - self.hitRange
        else:
            return self.barPercent <= self.hitRange

    def onMouseClick(self):
        if self.isLineInBox() and self.goalBoxEnabled == 1:
            actualPumpAmount = self.pumpRate + self.config.chainMultiplier * self.chainCount * self.pumpRate
            actualPumpAmount *= WATER_LEVEL_START - WATER_LEVEL_DONE
            self.remainingWater -= actualPumpAmount
            self.remainingWater = max(0.0, self.remainingWater)
            self.waterMeter.setSz(self.remainingWater)
            self.waterTop.setZ(self.waterMeterTopLoc.getZ(self.visual) - 0.001)
            if self.barPercent > 0.5:
                self.pumpWaterDownLerp.duration = self.currentBarRate
                self.pumpWaterDownLerp.start()
                self.barDirection = DOWN
                self.pumpHandle.setR(ROTATION_MAX)
                random.choice(self.pumpDownSounds).play()
            else:
                self.pumpWaterUpLerp.duration = self.currentBarRate
                self.pumpWaterUpLerp.start()
                self.barDirection = UP
                self.pumpHandle.setR(ROTATION_MIN)
                random.choice(self.pumpUpSounds).play()
            if self.barPercent > 0.5:
                self.setGoalIndex(BOTTOM)
            else:
                self.setGoalIndex(TOP)
            self.currentBarRate /= self.config.barSpeedIncrease
            self.chainCount += 1
            self.setSuccessMarker()
            if self.remainingWater <= WATER_LEVEL_DONE and self.barDirection == DOWN:
                self.remainingWater = 0.0
                self.request('Outro')
                return
            totalRange = WATER_LEVEL_START - WATER_LEVEL_DONE
            current = WATER_LEVEL_START - self.remainingWater
            percent = min(100, int(current / totalRange * 100))
            self.repairGame.d_reportMincroGameProgress(percent, max(0, min(5, self.chainCount) - 1))
        else:
            self.disableGoalBox()
            self.currentBarRate /= self.config.barSpeedDecrease
            self.currentBarRate += (1 - self.config.barSpeedDecrease) * self.config.barSpeedMin
            self.currentBarRate = min(self.currentBarRate, self.config.barSpeedMin)
            self.setFailMarker()
            self.chainCount = 0
            self.failedPercentAndDirection = (self.barPercent, self.barDirection)

    def setPumpWater(self, value):
        self.pumpWaterBottom.setSz(value)
        self.pumpWaterTop.setZ(self.pumpWaterTopLoc.getZ(self.visual))

    def setSuccessMarker(self):
        self.greatLabel.setZ(self.pumpLine.getZ())
        self.greatLabel.unstash()
        pumpSoundIndex = min(len(self.pumpGoodSounds) - 1, self.chainCount / 2)
        self.pumpGoodSounds[pumpSoundIndex].play()

    def setFailMarker(self):
        self.hideMarkers()
        self.ghostLine.setPos(self.pumpLine.getPos())
        self.ghostLine.unstash()
        self.failLabel.setZ(self.pumpLine.getZ())
        self.failLabel.unstash()
        random.choice(self.pumpBadSounds).play()

    def hideMarkers(self):
        self.ghostLine.stash()
        self.greatLabel.stash()
        self.failLabel.stash()

    def enterGame(self):
        RepairMincroGame.enterGame(self)
        taskMgr.add(self.updateTask, 'RepairPumpingGame.updateTask')
        self.accept('mouse1', self.onMouseClick)
        self.enableGoalBox()

    def exitGame(self):
        RepairMincroGame.exitGame(self)
        taskMgr.remove('RepairPumpingGame.updateTask')
        self.ignore('mouse1')

    def enterOutro(self):
        RepairMincroGame.enterOutro(self)
        self.repairGame.d_reportMincroGameScore(150)