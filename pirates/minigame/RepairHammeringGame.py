import math
import random
from pandac.PandaModules import Point3, NodePath
from direct.gui.DirectGui import DirectLabel
from direct.task import Task
from RepairMincroGame import RepairMincroGame
from RepairNail import RepairNail, NAIL_COLLIDE_MASK
from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import RepairGlobals
SHRINK = -1
GROW = 1

class RepairHammeringGame(RepairMincroGame):
    hammerComplete = None
    weakHammerSounds = None
    normalHammerSounds = None
    perfectHammerSound = None
    failSound = None

    def __init__(self, repairGame):
        self.config = RepairGlobals.Hammering
        RepairMincroGame.__init__(self, repairGame, 'hammering', PLocalizer.Minigame_Repair_Hammering_Start)

    def _initVars(self):
        RepairMincroGame._initVars(self)
        self.circleDirection = GROW
        self.currentMin = 0.0
        self.nailCount = 0
        self.currentNails = []
        self.aim = 1.0

    def _initAudio(self):
        RepairMincroGame._initAudio(self)
        if not self.hammerComplete:
            RepairHammeringGame.hammerComplete = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_HAMMER_COMPLETE)
            RepairHammeringGame.weakHammerSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_HAMMER_WEAKHIT01), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_HAMMER_WEAKHIT02))
            RepairHammeringGame.normalHammerSounds = (
             loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_HAMMER_HIT01), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_HAMMER_HIT02), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_HAMMER_HIT03))
            RepairHammeringGame.perfectHammerSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_HAMMER_PERFECT)
            RepairHammeringGame.failSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_FAIL)

    def _initVisuals(self):
        RepairMincroGame._initVisuals(self)
        self.model = loader.loadModel('models/gui/pir_m_gui_srp_hammering_main')
        self.board = self.model.find('**/wood')
        self.board.reparentTo(self)
        self.board.setPos(-0.02, -2.0, 0.08)
        self.board.setScale(1.3)
        self.board.setDepthTest(True)
        self.board.setDepthWrite(True)
        self.hammerSwinging = False
        self.nailParent = self.attachNewNode('nailParent')
        self.nails = []
        for i in range(self.config.nailCountRange[1]):
            nailModel = self.model.find('**/nail').copyTo(NodePath())
            nail = RepairNail(name='nail%i' % i, parent=self.nailParent, nailModel=nailModel)
            self.nails.append(nail)

        self.circle = aspect2d.attachNewNode('circle')
        self.circle.setHpr(0.0, 0.0, 0.0)
        self.circle.setZ(0.2)
        self.reticleCursorPerfect = self.model.find('**/reticleCursorPerfect')
        self.reticleCursorPerfect.reparentTo(self.circle)
        self.reticleCursor = self.model.find('**/reticleCursor')
        self.reticleCursor.reparentTo(self.circle)
        self.hammer = self.model.find('**/hammerCursor')
        self.hammer.reparentTo(aspect2d)
        self.circle.stash()
        self.hammer.stash()

    def destroy(self):
        RepairMincroGame.destroy(self)
        del self.currentNails
        self.board.removeNode()
        self.circle.removeNode()
        for n in self.nails:
            n.removeNode()

    def reset(self):
        RepairMincroGame.reset(self)
        self.aim = 1.0
        self.hammerSwinging = False
        self.circleDirection = GROW
        self.currentMin = 0.0
        self.circle.setScale(self.config.reticleScaleRange[1])
        spacing = 1.6 / (self.nailCount + 2)
        self.currentNails = []
        i = 0
        for nail in self.nails:
            if i < self.nailCount:
                nail.setPos(-0.8 + spacing * 1.5 + spacing * i, -2.0, 0.1)
                nail.request('Active')
                nail.unstash()
                self.currentNails.append(nail)
            else:
                nail.request('Idle')
            i += 1

        self.repairGame.gui.setTutorial(self.name)
        self.repairGame.gui.setTitle(self.name)

    def setDifficulty(self, difficulty):
        RepairMincroGame.setDifficulty(self, difficulty)
        percent = difficulty / self.repairGame.difficultyMax
        dif = self.config.nailCountRange[1] - self.config.nailCountRange[0]
        self.nailCount = int(math.floor(self.config.nailCountRange[0] + dif * percent))

    def onMouseUp(self):
        self.hammer.setHpr(0, 0, 0)
        self.hammerSwinging = False

    def onMouseClick(self):
        pickedObjects = self.repairGame.mousePicker.getCollisions(self.nailParent, useIntoNodePaths=True)
        self.hammerSwinging = True
        self.hammer.setHpr(0, 0, 45)
        if len(pickedObjects) > 0:
            nail = pickedObjects[0].getPythonTag('nail')
            if nail is not None:
                if nail.getCurrentOrNextState() == 'Active':
                    percent = 1.0 - self.aim
                    perfectMultiplier = 1.0
                    if percent > 1.0 - self.config.hitForgiveness:
                        percent = 1.0
                    result = nail.hitNail(percent)
                    if percent >= 1.0:
                        self.perfectHammerSound.play()
                        perfectMultiplier = 2.0
                    elif percent > 0.3:
                        random.choice(self.normalHammerSounds).play()
                    else:
                        random.choice(self.weakHammerSounds).play()
                    if result:
                        rating = 5 - nail.totalClicks
                        self.hammerComplete.play()
                        self.checkWin(rating)
            self.currentMin = self.aim
            if not taskMgr.hasTaskNamed('RepairHammerGame.updateCircleRadiusMin'):
                taskMgr.add(self.updateCircleRadiusMin, 'RepairHammerGame.updateCircleRadiusMin')
        else:
            self.failSound.play()
        return

    def updateTask(self, task):
        dt = globalClock.getDt()
        if self.config.useReticleColor:
            self.reticleCursor.setColorScale(self.currentMin, 1.0 - self.currentMin, 0.0, 1.0)
        percentTimeThisStep = dt / self.config.reticleScaleRate * 2.0
        self.aim = self.aim + percentTimeThisStep * self.circleDirection
        newScale = self.config.reticleScaleRange[0] + (self.config.reticleScaleRange[1] - self.config.reticleScaleRange[0]) * self.aim
        if self.aim >= 1.0:
            newScale = self.config.reticleScaleRange[1]
            self.circleDirection = SHRINK
            self.aim = 2.0 - self.aim
        elif self.aim <= self.currentMin:
            newScale = self.config.reticleScaleRange[0] + (self.config.reticleScaleRange[1] - self.config.reticleScaleRange[0]) * self.currentMin
            self.circleDirection = GROW
            self.aim = self.currentMin + (self.currentMin - self.aim)
        if not (self.aim >= 0.0 and self.aim <= 1.0):
            self.aim = 1.0
        percent = 1.0 - self.aim
        if percent > 1.0 - self.config.hitForgiveness:
            self.reticleCursorPerfect.setColorScale(1.0, 1.0, 1.0, 1.0)
        else:
            if self.circleDirection == SHRINK:
                self.reticleCursorPerfect.setColorScale(0.8, 0.5, 0.0, (-1.0 + percent + 6.0 * self.config.hitForgiveness) * (1.0 / (10.0 * self.config.hitForgiveness)))
            else:
                self.reticleCursorPerfect.setColorScale(0.0, 0.0, 0.0, 0.0)
            self.circle.setScale(newScale)
            if base.mouseWatcherNode.hasMouse():
                mpos = base.mouseWatcherNode.getMouse()
                mpos = Point3(mpos.getX(), mpos.getY(), 0.0)
                mpos = aspect2d.getRelativePoint(render2d, mpos)
                if self.hammer.isStashed():
                    self.hammer.unstash()
                if self.circle.isStashed():
                    self.circle.unstash()
                self.circle.setPos(mpos.getX(), 0.0, mpos.getY())
                if self.hammerSwinging:
                    self.hammer.setPos(mpos.getX() - 0.06, 0.0, mpos.getY() + 0.08)
                else:
                    self.hammer.setPos(mpos.getX() - 0.08, 0.0, mpos.getY() + 0.17)
        return Task.cont

    def updateCircleRadiusMin(self, task):
        dt = globalClock.getDt()
        newMin = self.currentMin - dt * 1.0 / self.config.recoveryTime
        if newMin <= 0.0:
            newMin = 0.0
            taskMgr.remove('RepairHammerGame.updateCircleRadiusMin')
        self.currentMin = newMin
        return Task.cont

    def checkWin(self, rating):
        nailsComplete = 0
        for n in self.currentNails:
            if n.getCurrentOrNextState() == 'Hammered':
                nailsComplete += 1

        percent = int((nailsComplete + 0.0) / self.nailCount * 100)
        self.repairGame.d_reportMincroGameProgress(percent, max(0, int(rating)))
        if nailsComplete == self.nailCount:
            self.request('Outro')

    def enterGame(self):
        RepairMincroGame.enterGame(self)
        self.accept('mouse1', self.onMouseClick)
        self.accept('mouse1-up', self.onMouseUp)
        taskMgr.add(self.updateTask, 'RepairHammerGame.updateTask')
        self.repairGame.mousePicker.setCollisionMask(NAIL_COLLIDE_MASK)
        for n in self.currentNails:
            n.request('Active')

    def exitGame(self):
        RepairMincroGame.exitGame(self)
        self.ignore('mouse1')
        taskMgr.remove('RepairHammerGame.updateTask')
        taskMgr.remove('RepairHammerGame.updateCircleRadiusMin')
        self.circle.stash()
        self.hammer.stash()
        self.repairGame.mousePicker.clearCollisionMask()

    def enterOutro(self):
        RepairMincroGame.enterOutro(self)
        self.repairGame.d_reportMincroGameScore(150)

    def exitOutro(self):
        RepairMincroGame.exitOutro(self)
        for n in self.currentNails:
            n.request('Idle')