from pandac.PandaModules import Vec3
from direct.gui.DirectGui import DirectFrame, DirectLabel
from direct.interval.IntervalGlobal import Sequence, Func, Wait, Parallel
from direct.fsm import FSM
from direct.interval.LerpInterval import LerpFunc
from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import RepairGlobals
from pirates.piratesbase import PiratesGlobals
import random

class RepairMincroGame(DirectFrame, FSM.FSM):
    readySound = None
    goSound = None
    completeSound = None

    def __init__(self, repairGame, name, startText):
        DirectFrame.__init__(self, parent=repairGame.gui, relief=None)
        FSM.FSM.__init__(self, '%sFSM' % name)
        self.defaultTransitions = {'Idle': ['Intro', 'Final'],'Intro': ['Game', 'Idle', 'Final'],'Game': ['Outro', 'Idle', 'Final'],'Outro': ['Idle', 'Final'],'Final': []}
        self.name = name
        self.repairGame = repairGame
        self.startText = startText
        self._initVars()
        self._initAudio()
        self._initVisuals()
        self._initIntervals()
        self.request('Idle')
        return

    def _initVars(self):
        self.complete = False
        self.difficulty = 0

    def _initAudio(self):
        if not self.readySound:
            RepairMincroGame.readySound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_GENERAL_READY)
            RepairMincroGame.goSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_GENERAL_GO)
            RepairMincroGame.completeSound = loadSfx(SoundGlobals.SFX_MINIGAME_REPAIR_GENERAL_GAMECOMPLETE)

    def _initVisuals(self):
        self.countDownLabel = DirectLabel(text=self.startText, text_fg=(1.0, 1.0, 1.0,
                                                                        1.0), text_shadow=(0.0,
                                                                                           0.0,
                                                                                           0.0,
                                                                                           1.0), text_font=PiratesGlobals.getPirateFont(), scale=(0.16,
                                                                                                                                                  0.16,
                                                                                                                                                  0.16), pos=(0.0,
                                                                                                                                                              0.0,
                                                                                                                                                              0.15), parent=self, relief=None, textMayChange=1)
        self.countDownLabel.setBin('fixed', 37)
        self.winLabel = DirectLabel(text=PLocalizer.Minigame_Repair_Win, text_fg=(1.0,
                                                                                  1.0,
                                                                                  1.0,
                                                                                  1.0), text_font=PiratesGlobals.getPirateFont(), text_shadow=(0.0,
                                                                                                                                               0.0,
                                                                                                                                               0.0,
                                                                                                                                               1.0), scale=(0.16,
                                                                                                                                                            0.16,
                                                                                                                                                            0.16), pos=RepairGlobals.Common.youWinPos[self.name], relief=None, parent=self)
        self.winLabel.setBin('fixed', 37)
        self.winLabel.stash()
        self.scoreLabel = DirectLabel(text=PLocalizer.Minigame_Repair_Win, text_fg=(1.0,
                                                                                    1.0,
                                                                                    1.0,
                                                                                    1.0), text_font=PiratesGlobals.getPirateFont(), text_shadow=(0.0,
                                                                                                                                                 0.0,
                                                                                                                                                 0.0,
                                                                                                                                                 1.0), scale=(0.1,
                                                                                                                                                              0.1,
                                                                                                                                                              0.1), pos=RepairGlobals.Common.scorePos[self.name], relief=None, parent=self)
        self.scoreLabel.setBin('fixed', 37)
        self.scoreLabel.stash()
        self.postWinLabel = DirectLabel(text=PLocalizer.Minigame_Repair_Pick_New_Game, text_fg=(1.0,
                                                                                                1.0,
                                                                                                1.0,
                                                                                                1.0), text_font=PiratesGlobals.getPirateFont(), text_shadow=(0.0,
                                                                                                                                                             0.0,
                                                                                                                                                             0.0,
                                                                                                                                                             1.0), scale=(0.14,
                                                                                                                                                                          0.14,
                                                                                                                                                                          0.14), pos=RepairGlobals.Common.youWinPos[self.name], relief=None, textMayChange=1, parent=self.repairGame.gui)
        self.postWinLabel.setBin('fixed', 37)
        self.postWinLabel.stash()
        return

    def _initIntervals(self):
        normalPos = Vec3(0.0, 0.0, 0.15)
        belowScreenPos = Vec3(normalPos.getX(), normalPos.getY(), normalPos.getZ() - 0.25)
        aboveScreenPos = Vec3(normalPos.getX(), normalPos.getY(), normalPos.getZ() + 0.25)
        self.introSequence = Sequence(Func(self.setCountDown, PLocalizer.Minigame_Repair_Countdown_Ready), Parallel(LerpFunc(self.countDownLabel.setPos, fromData=belowScreenPos, toData=normalPos, duration=0.25), LerpFunc(self.countDownLabel.setAlphaScale, fromData=0.0, toData=1.0, duration=0.25)), Func(self.readySound.play), Wait(0.5), Parallel(LerpFunc(self.countDownLabel.setPos, fromData=normalPos, toData=aboveScreenPos, duration=0.25), LerpFunc(self.countDownLabel.setAlphaScale, fromData=1.0, toData=0.0, duration=0.25)), Func(self.setCountDown, self.startText), Parallel(LerpFunc(self.countDownLabel.setPos, fromData=belowScreenPos, toData=normalPos, duration=0.25), LerpFunc(self.countDownLabel.setAlphaScale, fromData=0.0, toData=1.0, duration=0.25)), Func(self.goSound.play), Wait(0.5), Parallel(LerpFunc(self.countDownLabel.setPos, fromData=normalPos, toData=aboveScreenPos, duration=0.25), LerpFunc(self.countDownLabel.setAlphaScale, fromData=1.0, toData=0.0, duration=0.25)), Func(self.request, 'Game'), name='RepairMincroGame.introSequence')
        normalPos = Vec3(RepairGlobals.Common.youWinPos[self.name])
        normalScorePos = Vec3(RepairGlobals.Common.scorePos[self.name])
        belowScreenPos = Vec3(normalPos.getX(), normalPos.getY(), normalPos.getZ() - 0.25)
        aboveScreenPos = Vec3(normalPos.getX(), normalPos.getY(), normalPos.getZ() + 0.25)
        belowScreenScorePos = Vec3(normalScorePos.getX(), normalScorePos.getY(), normalScorePos.getZ() - 0.25)
        aboveScreenScorePos = Vec3(normalScorePos.getX(), normalScorePos.getY(), normalScorePos.getZ() + 0.25)
        self.outroSequence = Sequence(Func(self.winLabel.setAlphaScale, 0), Func(self.scoreLabel.setAlphaScale, 0), Func(self.postWinLabel.setAlphaScale, 0), Func(self.winLabel.setPos, belowScreenPos), Func(self.scoreLabel.setPos, belowScreenScorePos), Func(self.postWinLabel.setPos, belowScreenPos), Func(self.setScoreLabelText), Func(self.winLabel.unstash), Func(self.scoreLabel.unstash), Func(self.postWinLabel.unstash), Parallel(LerpFunc(self.scoreLabel.setPos, fromData=belowScreenScorePos, toData=normalScorePos, duration=0.25), LerpFunc(self.scoreLabel.setAlphaScale, fromData=0.0, toData=1.0, duration=0.25), LerpFunc(self.winLabel.setPos, fromData=belowScreenPos, toData=normalPos, duration=0.25), LerpFunc(self.winLabel.setAlphaScale, fromData=0.0, toData=1.0, duration=0.25)), Func(self.completeSound.play), Wait(1.0), Parallel(LerpFunc(self.winLabel.setPos, fromData=normalPos, toData=aboveScreenPos, duration=0.25), LerpFunc(self.winLabel.setAlphaScale, fromData=1.0, toData=0.0, duration=0.25), LerpFunc(self.scoreLabel.setPos, fromData=normalScorePos, toData=aboveScreenScorePos, duration=0.25), LerpFunc(self.scoreLabel.setAlphaScale, fromData=1.0, toData=0.0, duration=0.25)), Func(self.winLabel.stash), Func(self.scoreLabel.stash), Func(self.stashPostWinLabelIfCycleComplete), Wait(0.25), Parallel(LerpFunc(self.postWinLabel.setPos, fromData=belowScreenPos, toData=normalPos, duration=0.25), LerpFunc(self.postWinLabel.setAlphaScale, fromData=0.0, toData=1.0, duration=0.25)), name='outroSequence')
        self.cleanupSequence = Sequence(Parallel(LerpFunc(self.postWinLabel.setPos, fromData=normalPos, toData=aboveScreenPos, duration=0.5), LerpFunc(self.postWinLabel.setAlphaScale, fromData=1.0, toData=0.0, duration=0.5), LerpFunc(self.scoreLabel.setAlphaScale, fromData=1.0, toData=0.0, duration=0.5)), Func(self.scoreLabel.stash), Func(self.postWinLabel.stash), name='cleanupSequence')

    def updatePostWinLabel(self):
        if self.repairGame.isThereAnOpenGame():
            self.postWinLabel['text'] = PLocalizer.Minigame_Repair_Pick_New_Game
        else:
            self.postWinLabel['text'] = PLocalizer.Minigame_Repair_Waiting_For_Players
        self.postWinLabel.setText()

    def setScoreLabelText(self):
        labelSet = False
        for i in [0, 1, 2]:
            if not labelSet:
                percent = self.difficulty / self.repairGame.difficultyMax
                dif = RepairGlobals.Common.speedThresholds[self.name][i][1] - RepairGlobals.Common.speedThresholds[self.name][i][0]
                goalTime = RepairGlobals.Common.speedThresholds[self.name][i][0] + dif * percent
                if self.repairGame.repairClock.gameTime < goalTime:
                    labelSet = True
                    self.scoreLabel['text'] = PLocalizer.Minigame_Repair_Speed_Thresholds[i]

        if not labelSet:
            self.scoreLabel['text'] = PLocalizer.Minigame_Repair_Speed_Thresholds[3]

    def stashPostWinLabelIfCycleComplete(self):
        if self.repairGame.isCycleComplete():
            self.postWinLabel.stash()

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

    def setCountDown(self, text):
        self.countDownLabel['text'] = text
        self.countDownLabel.setText()
        self.countDownLabel.setAlphaScale(0.0)

    def destroy(self):
        DirectFrame.destroy(self)
        self.countDownLabel.destroy()
        del self.countDownLabel
        self.winLabel.destroy()
        del self.winLabel
        self.introSequence.clearToInitial()
        del self.introSequence
        self.outroSequence.clearToInitial()
        del self.outroSequence
        self.cleanupSequence.clearToInitial()
        del self.cleanupSequence
        del self.repairGame
        self.cleanup()

    def reset(self):
        self.complete = False
        self.repairGame.repairClock.stop()

    def enterIdle(self):
        self.stash()

    def exitIdle(self):
        pass

    def enterIntro(self):
        self.unstash()
        self.countDownLabel.unstash()
        self.introSequence.start()
        self.reset()
        self.countDownLabel.reparentTo(self)

    def exitIntro(self):
        self.countDownLabel.stash()
        self.introSequence.clearToInitial()

    def enterGame(self):
        self.repairGame.repairClock.restart()

    def exitGame(self):
        self.repairGame.repairClock.pause()

    def enterOutro(self):
        self.outroSequence.start()
        self.complete = True

    def exitOutro(self):
        self.outroSequence.finish()
        self.cleanupSequence.start()
        self.reset()
        self.repairGame.gui.clearTutorial()
        self.repairGame.gui.clearTitle()

    def enterFinal(self):
        pass