import random
import math
from pandac.PandaModules import NodePath
from pandac.PandaModules import Point3
from pandac.PandaModules import AudioSound
from direct.task import Task
from direct.interval.IntervalGlobal import *
from RepairMincroGame import RepairMincroGame
from RepairLeak import RepairLeak
from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import RepairGlobals

class RepairPitchingGame(RepairMincroGame):

    def __init__(self, repairGame):
        self.config = RepairGlobals.Pitching
        RepairMincroGame.__init__(self, repairGame, 'pitching', PLocalizer.Minigame_Repair_Pitching_Start)

    def _initVars(self):
        RepairMincroGame._initVars(self)
        self.nextSpawnTime = 0.0
        self.inactiveLeaks = set()
        self.activeLeaks = set()
        self.patchedLeaks = set()
        self.locators = []
        self.leakCount = 0
        self.maxLeaks = 0
        self.bucketPouring = False

    def _initAudio(self):
        RepairMincroGame._initAudio(self)
        self.pitchSounds = (
         loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PITCH_PLUG01), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PITCH_PLUG02), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PITCH_PLUG03))
        self.leakSounds = (
         loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PITCH_LEAK01), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PITCH_LEAK02), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PITCH_LEAK03), loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_PITCH_LEAK04))

    def _initVisuals(self):
        RepairMincroGame._initVisuals(self)
        self.model = loader.loadModel('models/gui/pir_m_gui_srp_pitching_main')
        self.board = self.model.find('**/piece_hull')
        self.board.reparentTo(self)
        self.board.setPos(0.0, 0.0, 0.19)
        self.crossHair = self.model.find('**/crosshair')
        self.crossHair.reparentTo(base.a2dBackground)
        self.crossHair.setBin('fixed', 45)
        self.crossHair.setScale(1.0)
        self.crossHair.setColorScale(0.0, 1.0, 0.0, 1.0)
        self.crossHair.stash()
        self.bucketIdle = self.model.find('**/pitchCursor/idle')
        self.bucketIdle.reparentTo(base.a2dBackground)
        self.bucketIdle.setBin('fixed', 45)
        self.bucketIdle.setScale(1.35)
        self.bucketIdle.stash()
        self.bucket = self.bucketIdle.copyTo(NodePath())
        self.bucket.reparentTo(base.a2dBackground)
        self.bucket.setHpr(0, 0, 90)
        self.bucket.setBin('fixed', 45)
        self.bucket.setScale(1.35)
        self.bucket.stash()
        self.missPatch = NodePath('dummy')
        self.missPatchAsset = self.model.find('**/miss')
        self.missPatchAsset.reparentTo(self.missPatch)
        self.missPatch.reparentTo(self)
        self.missPatch.setScale(1.1)
        self.missPatch.stash()
        self.missSeq = None
        index = 1
        while True:
            locator = self.model.find('**/locator_%i' % index)
            if locator.isEmpty():
                break
            self.locators.append(locator)
            index += 1

        return

    def onMouseUp(self):
        self.bucketPouring = False

    def onMouseDown(self):
        self.bucketPouring = True
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            mpos = Point3(mpos.getX(), mpos.getY(), 0.0)
            mpos = aspect2d.getRelativePoint(render2d, mpos)
            if self.missSeq is not None:
                self.missSeq.finish()
            self.missPatch.unstash()
            self.missPatch.setPos(mpos.getX(), 0.0, mpos.getY() + 0.2)
            self.missPatchAsset.setPos(0.0, 0.0, 0.0)
            self.missSeq = Sequence(Parallel(LerpPosInterval(self.missPatch, duration=1.5, blendType='easeIn', pos=(mpos.getX(), 0.0, mpos.getY() - 0.15)), LerpPosInterval(self.missPatchAsset, duration=1.5, blendType='easeOut', pos=(0.2,
                                                                                                                                                                                                                                         0.0,
                                                                                                                                                                                                                                         0.0)), LerpColorScaleInterval(self.missPatch, duration=1.5, blendType='easeIn', startColorScale=(1.0,
                                                                                                                                                                                                                                                                                                                                          1.0,
                                                                                                                                                                                                                                                                                                                                          1.0,
                                                                                                                                                                                                                                                                                                                                          1.0), colorScale=(1.0,
                                                                                                                                                                                                                                                                                                                                                            1.0,
                                                                                                                                                                                                                                                                                                                                                            1.0,
                                                                                                                                                                                                                                                                                                                                                            0.0))), Func(self.missPatch.stash))
            self.missSeq.start()
        return

    def reset(self):
        if self.missSeq is not None:
            self.missSeq.finish()
        self.clearLeaks()
        for i in range(self.leakCount):
            self.createLeak('leak%i' % i)

        self.repairGame.gui.setTutorial(self.name)
        self.repairGame.gui.setTitle(self.name)
        self.bucketPouring = False
        return

    def destroy(self):
        RepairMincroGame.destroy(self)
        for leakSet in (self.activeLeaks, self.inactiveLeaks, self.patchedLeaks):
            for i in range(len(leakSet)):
                leak = leakSet.pop()

        del self.activeLeaks
        del self.inactiveLeaks
        del self.patchedLeaks
        for locator in self.locators:
            locator.removeNode()

        del self.locators
        self.board.removeNode()
        del self.board
        self.crossHair.removeNode()
        del self.crossHair
        self.bucket.removeNode()
        del self.bucket
        self.bucketIdle.removeNode()
        del self.bucketIdle
        if self.missSeq is not None:
            self.missSeq.finish()
        del self.missSeq
        self.missPatch.removeNode()
        del self.missPatch
        return

    def setDifficulty(self, difficulty):
        RepairMincroGame.setDifficulty(self, difficulty)
        percent = difficulty / self.repairGame.difficultyMax
        dif = self.config.leakCountRange[1] - self.config.leakCountRange[0]
        self.leakCount = int(math.floor(self.config.leakCountRange[0] + dif * percent))
        dif = self.config.maxLeaksRange[1] - self.config.maxLeaksRange[0]
        self.maxLeaks = int(math.floor(self.config.maxLeaksRange[0] + dif * percent))
        dif = self.config.spawnDelayRange[1] - self.config.spawnDelayRange[0]
        self.minSpawnTime = self.config.spawnDelayRange[0] + dif * percent
        dif = self.config.spawnDelayRange[3] - self.config.spawnDelayRange[2]
        self.maxSpawnTime = self.config.spawnDelayRange[2] + dif * percent

    def clearLeaks(self):
        for leakSet in (self.activeLeaks, self.inactiveLeaks, self.patchedLeaks):
            for i in range(len(leakSet)):
                leak = leakSet.pop()
                leak.destroy()

    _MIN_DIST = 0.2
    _MAX_TRIES = 10

    def placeLeak(self, leak):
        tooClose = True
        attempts = 0
        while tooClose and attempts < self._MAX_TRIES:
            attempts += 1
            locator = self.locators[random.randint(0, len(self.locators) - 1)]
            relative = self.getRelativePoint(self.board, Point3(locator.getX(), 0, locator.getZ()))
            x = relative.getX()
            z = relative.getZ()
            tooClose = False
            for otherLeak in self.activeLeaks:
                dist = math.hypot(otherLeak.getX() - x, otherLeak.getZ() - z)
                if dist < self._MIN_DIST:
                    tooClose = True

            for otherLeak in self.patchedLeaks:
                dist = math.hypot(otherLeak.getX() - x, otherLeak.getZ() - z)
                if dist < self._MIN_DIST:
                    tooClose = True

        leak.repositionTo(x, z)

    def createLeak(self, name):
        scale = random.uniform(self.config.leakScaleRange[0], self.config.leakScaleRange[1])
        leak = RepairLeak(name=name, parent=self, leakscale=scale, command=self.onLeakPressed)
        leak['extraArgs'] = [
         leak]
        leak.onCleanup = self.cleanupLeak
        self.inactiveLeaks.add(leak)
        leak.request('Idle')

    def cleanupLeak(self, leak):
        if leak in self.patchedLeaks:
            self.patchedLeaks.remove(leak)

    def onLeakPressed(self, leak):
        self.bucketPouring = True
        if leak in self.activeLeaks:
            self.activeLeaks.remove(leak)
            self.patchedLeaks.add(leak)
            leak.request('Patched')
            numLeaks = len(self.activeLeaks)
            remainingLeaks = len(self.inactiveLeaks) + numLeaks
            percent = 100 - int((remainingLeaks + 0.0) / self.leakCount * 100)
            random.choice(self.pitchSounds).play()
            self.repairGame.d_reportMincroGameProgress(percent, max(0, min(4, 4 + self.config.ratingGive - numLeaks)))
            self.checkWin()

    def springLeak(self):
        leakSound = random.choice(self.leakSounds)
        if not leakSound.status() == AudioSound.PLAYING:
            leakSound.play()
        newLeak = self.inactiveLeaks.pop()
        self.placeLeak(newLeak)
        self.activeLeaks.add(newLeak)
        newLeak.request('Active')

    def checkWin(self):
        if len(self.inactiveLeaks) == 0:
            if len(self.activeLeaks) == 0:
                self.request('Outro')

    def updateTask(self, task):
        elapsedTime = self.repairGame.repairClock.getTime()
        if len(self.activeLeaks) == 0:
            if len(self.inactiveLeaks) > 0:
                self.springLeak()
        if elapsedTime >= self.nextSpawnTime and len(self.inactiveLeaks) > 0:
            self.nextSpawnTime = elapsedTime + random.uniform(self.minSpawnTime, self.maxSpawnTime)
            if len(self.activeLeaks) < self.maxLeaks:
                self.springLeak()
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()
            mpos = Point3(mpos.getX(), mpos.getY(), 0.0)
            mpos = aspect2d.getRelativePoint(render2d, mpos)
            if self.config.useReticle:
                activeXOffset = -0.14
                activeYOffset = 0.02
                idleXOffset = -0.17
                idleYOffset = -0.08
                self.crossHair.unstash()
                self.crossHair.setPos(mpos.getX(), 0.0, mpos.getY())
            else:
                activeXOffset = -0.06
                activeYOffset = 0.07
                idleXOffset = -0.08
                idleYOffset = -0.03
                self.crossHair.stash()
            if self.bucketPouring:
                self.bucketIdle.stash()
                self.bucket.unstash()
                self.bucket.setPos(mpos.getX() + activeXOffset, 0.0, mpos.getY() + activeYOffset)
            else:
                self.bucketIdle.unstash()
                self.bucket.stash()
                self.bucketIdle.setPos(mpos.getX() + idleXOffset, 0.0, mpos.getY() + idleYOffset)
        return Task.cont

    def enterGame(self):
        RepairMincroGame.enterGame(self)
        taskMgr.add(self.updateTask, 'RepairPitchingGame.updateTask')
        self.bucketPouring = False
        self.accept('mouse1', self.onMouseDown)
        self.accept('mouse1-up', self.onMouseUp)
        self.nextSpawnTime = 0.0

    def exitGame(self):
        self.bucket.stash()
        self.bucketIdle.stash()
        self.crossHair.stash()
        RepairMincroGame.exitGame(self)
        self.ignore('mouse1')
        self.ignore('mouse1-up')
        taskMgr.remove('RepairPitchingGame.updateTask')
        self.clearLeaks()
        self.bucket.stash()
        self.bucketIdle.stash()

    def enterOutro(self):
        RepairMincroGame.enterOutro(self)
        self.repairGame.d_reportMincroGameScore(150)