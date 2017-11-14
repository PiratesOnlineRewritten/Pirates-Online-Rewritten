import random
import math
from pandac.PandaModules import Point2, Point3, Vec2
from pandac.PandaModules import NodePath, CardMaker
from pandac.PandaModules import MouseButton
from direct.task import Task
from direct.gui.DirectGui import *
from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from RepairMincroGame import RepairMincroGame
from RepairBarnacle import RepairBarnacle
from pirates.piratesbase import PiratesGlobals
import RepairGlobals

class RepairCareeningGame(RepairMincroGame):
    scrubSounds = None
    powerFullSound = None
    powerEmptySound = None

    def __init__(self, repairGame):
        self.config = RepairGlobals.Careening
        RepairMincroGame.__init__(self, repairGame, 'careening', PLocalizer.Minigame_Repair_Careening_Start)

    def _initVars(self):
        RepairMincroGame._initVars(self)
        self.lastMousePos = Point2(0.0, 0.0)
        self.isMouseDown = False
        self.barnacleCount = 0
        self.currentBarnacles = []

    def _initAudio(self):
        RepairMincroGame._initAudio(self)
        if not self.scrubSounds:
            RepairCareeningGame.scrubSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_SCRUB01), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_SCRUB02), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_SCRUB03), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_SCRUB04), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_SCRUB05), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_SCRUB06), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_SCRUB07), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_SCRUB08))
            for sound in RepairCareeningGame.scrubSounds:
                sound.setVolume(0.75)

            RepairCareeningGame.powerFullSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_CHRGCOMP)
            RepairCareeningGame.powerFullSound.setVolume(0.75)
            RepairCareeningGame.powerEmptySound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_CAREEN_CHRGEMPTY)
            RepairCareeningGame.powerEmptySound.setVolume(0.75)

    def _initVisuals(self):
        RepairMincroGame._initVisuals(self)
        self.model = loader.loadModel('models/gui/pir_m_gui_srp_careening_main')
        self.board = self.model.find('**/hull')
        self.board.reparentTo(self)
        self.board.setScale(1.0)
        self.board.setPos(-0.12, 0.0, 0.19)
        self.brush = self.model.find('**/brushCursor')
        self.brush.reparentTo(aspect2d)
        self.brush.stash()
        barnacleGeom = [
         self.model.find('**/barnacles/barnacle0'), self.model.find('**/barnacles/barnacle1'), self.model.find('**/barnacles/barnacle2')]
        self.barnacles = []
        for i in range(self.config.barnacleCountRange[1]):
            bGeom = barnacleGeom[random.randint(0, 1)].copyTo(NodePath('barnacle%i' % i))
            bGeom.setBin('fixed', 36)
            if random.random() < self.config.mossPercentage:
                mGeom = barnacleGeom[2].copyTo(NodePath('moss'))
                mGeom.reparentTo(bGeom)
                mGeom.setPos(random.uniform(0, self.config.mossPosVariance), 0.0, random.uniform(0, self.config.mossPosVariance))
                mGeom.setBin('fixed', 35)
            b = RepairBarnacle('barnacle%i' % i, bGeom)
            b.reparentTo(self)
            self.barnacles.append(b)
            b.stash()

        self.scrubPowerMeter = self.model.find('**/scrubMeter')
        self.scrubMeterBackground = self.model.find('**/scrubMeterBackground')
        self.scrubMeterBackground.setBin('fixed', 32)
        self.scrubMeterBar = self.model.find('**/scrubMeterBar')
        self.scrubMeterBar.setBin('fixed', 33)
        self.scrubMeterFrame = self.model.find('**/scrubMeterFrame')
        self.scrubMeterFrame.setBin('fixed', 34)
        self.scrubPowerMeter.reparentTo(self)
        self.scrubPowerMeter.setPos(0.68, 0.0, 0.2)
        self.scrubPowerMeter.setSz(1.25)
        self.pushLabel = DirectLabel(text=PLocalizer.Minigame_Repair_Careening_Power, pos=(0.68, 0.0, -0.27), text_fg=(1.0,
                                                                                                                       1.0,
                                                                                                                       1.0,
                                                                                                                       1.0), text_shadow=(0.0,
                                                                                                                                          0.0,
                                                                                                                                          0.0,
                                                                                                                                          1.0), text_font=PiratesGlobals.getPirateFont(), scale=(0.08,
                                                                                                                                                                                                 0.08,
                                                                                                                                                                                                 0.08), parent=self, relief=None)
        return

    def reset(self):
        RepairMincroGame.reset(self)
        self.lastMousePos = Point2(0.0, 0.0)
        self.isMouseDown = False
        self.randomizeBoard()
        self.repairGame.gui.setTutorial(self.name)
        self.brush.stash()
        self.repairGame.gui.setTitle(self.name)

    def destroy(self):
        RepairMincroGame.destroy(self)
        self.scrubPowerMeter.detachNode()
        self.scrubPowerMeter = None
        self.scrubMeterBackground.detachNode()
        self.scrubMeterBackground = None
        self.scrubMeterBar.detachNode()
        self.scrubMeterBar = None
        self.scrubMeterFrame.detachNode()
        self.scrubMeterFrame = None
        del self.lastMousePos
        del self.currentBarnacles
        self.board.removeNode()
        del self.board
        self.brush.removeNode()
        del self.barnacles
        return

    def setDifficulty(self, difficulty):
        RepairMincroGame.setDifficulty(self, difficulty)
        percent = difficulty / self.repairGame.difficultyMax
        dif = self.config.barnacleCountRange[1] - self.config.barnacleCountRange[0]
        self.barnacleCount = int(math.floor(self.config.barnacleCountRange[0] + dif * percent))
        dif = self.config.barnacleHPScaleRange[1] - self.config.barnacleHPScaleRange[0]
        self.barnacleHPScale = self.config.barnacleHPScaleRange[0] + dif * percent

    def onMouseDown(self):
        self.isMouseDown = True

    def onMouseUp(self):
        self.isMouseDown = False

    def randomizeBoard(self):
        self.currentBarnacles = []
        i = 0
        for b in self.barnacles:
            if i < self.barnacleCount:
                x = random.uniform(self.config.xRange[0], self.config.xRange[1])
                y = random.uniform(self.config.yRange[0], self.config.yRange[1])
                moss = b.find('**/barnacle2')
                closeToEdge = False
                if x - self.config.mossEdgeRestrictionAmount <= self.config.xRange[0] or x + self.config.mossEdgeRestrictionAmount >= self.config.xRange[1]:
                    closeToEdge = True
                elif y - self.config.mossEdgeRestrictionAmount <= self.config.yRange[0] or y + self.config.mossEdgeRestrictionAmount >= self.config.yRange[1]:
                    closeToEdge = True
                if not moss.isEmpty() and closeToEdge:
                    moss.stash()
                elif not moss.isEmpty():
                    moss.unstash()
                hp = random.uniform(self.config.barnacleHPRange[0], self.config.barnacleHPRange[1])
                b.setMaxHP(hp * self.barnacleHPScale, self.config.barnacleHPRange[1] * self.barnacleHPScale)
                b.setPos(x, 0.0, y)
                b.request('Idle')
                self.currentBarnacles.append(b)
            else:
                b.request('Clean')
            i += 1

    def getMousePosition(self):
        if base.mouseWatcherNode.hasMouse():
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()
            self.lastMousePos = Point2(x, y)
        return self.lastMousePos

    def playScrubBarnacleSound(self, powerScrubOn):
        sound = random.choice(self.scrubSounds)
        if sound.status() == 1:
            if powerScrubOn:
                sound.setPlayRate(0.75)
            else:
                sound.setPlayRate(2.0)
            sound.play()

    def updateTask(self, task):
        dt = globalClock.getDt()
        lastPos = self.lastMousePos
        mousePosition = self.getMousePosition()
        mouseChange = lastPos - mousePosition
        powerScale = 1.0
        if self.isMouseDown:
            if self.scrubMeterBar.getSz() > 0:
                powerScale = self.config.superScrubMultiplier
                self.scrubMeterBar.setSz(self.scrubMeterBar.getSz() - self.config.superScrubDecreaseRate * dt)
            elif self.scrubMeterBar.getSz() != 0.0:
                self.scrubMeterBar.setSz(0.0)
                self.powerEmptySound.play()
        else:
            if self.scrubMeterBar.getSz() < 1:
                self.scrubMeterBar.setSz(self.scrubMeterBar.getSz() + self.config.superScrubIncreaseRate * dt)
            elif self.scrubMeterBar.getSz() != 1.0:
                self.scrubMeterBar.setSz(1.0)
                self.powerFullSound.play()

        completeCount = 0
        barnacleHitThisRound = False
        for b in self.currentBarnacles:
            b.heat = max(0.0, b.heat - dt * 1.0)
            b.barnacleGeom.setColor(1.0, 1 - b.heat, 1 - b.heat, 1.0)
            if b.checkCollision(mousePosition):
                if mouseChange.length() > 0.0:
                    barnacleHitThisRound = True
                b.reduceHP(mouseChange, powerScale)
            if b.getCurrentOrNextState() in ['Clean', 'Falling']:
                completeCount += 1

        if barnacleHitThisRound:
            powerScrubOn = self.scrubMeterBar.getSz() > 0 and self.isMouseDown
            self.playScrubBarnacleSound(powerScrubOn)
        if self.lastCompleteCount != completeCount:
            percent = int((completeCount + 0.0) / self.barnacleCount * 100)
            self.repairGame.d_reportMincroGameProgress(percent)
            self.lastCompleteCount = completeCount
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            mpos = Point3(mpos.getX(), mpos.getY(), 0.0)
            mpos = aspect2d.getRelativePoint(render2d, mpos)
            if self.brush.isStashed():
                self.brush.unstash()
            if self.isMouseDown and self.scrubMeterBar.getSz() > 0:
                randomR = random.random() * 40.0 - 20.0
                randomScale = random.random() * 0.3
                self.brush.setScale(1.2 + randomScale)
                self.brush.setHpr(0, 0, randomR)
                self.brush.setPos(mpos.getX(), 0.0, mpos.getY())
            else:
                self.brush.setScale(1.0)
                self.brush.setHpr(0, 0, 0)
                self.brush.setPos(mpos.getX(), 0.0, mpos.getY())

        if completeCount == self.barnacleCount:
            self.request('Outro')

        return task.cont

    def enterGame(self):
        RepairMincroGame.enterGame(self)
        self.lastCompleteCount = 0
        taskMgr.add(self.updateTask, 'RepairCareeningGame.updateTask-%d' % id(self))
        self.accept('mouse1', self.onMouseDown)
        self.accept('mouse1-up', self.onMouseUp)
        if base.mouseWatcherNode.hasMouse() and base.mouseWatcherNode.isButtonDown(MouseButton.one()):
            self.onMouseDown()

    def exitGame(self):
        RepairMincroGame.exitGame(self)
        taskMgr.remove('RepairCareeningGame.updateTask-%d' % id(self))
        self.ignore('mouse1')
        self.ignore('mouse1-up')
        self.brush.stash()

    def enterOutro(self):
        RepairMincroGame.enterOutro(self)
        self.repairGame.d_reportMincroGameScore(150)
