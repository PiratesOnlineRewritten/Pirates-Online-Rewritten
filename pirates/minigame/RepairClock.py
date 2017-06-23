from direct.interval.IntervalGlobal import Sequence, Func
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.task import Task
from pandac.PandaModules import *
from pandac.PandaModules import CardMaker
from direct.fsm import FSM
from pirates.piratesbase import PiratesGlobals

class RepairClock(DirectFrame, FSM.FSM):

    def __init__(self, repairGame):
        DirectFrame.__init__(self, parent=repairGame.gui, relief=None)
        FSM.FSM.__init__(self, 'RepairClockFSM')
        self._initVars()
        self._initGUI()
        self._initIntervals()
        self.setPos(0.0, 0.0, -0.34)
        return

    def _initVars(self):
        self.gameTimes = {}
        self.gameTime = 0.0
        self.cycleTime = 0.0
        self.totalTime = 0.0

    def _initGUI(self):
        self.secondsLabel = DirectLabel(text='', text_fg=(1.0, 1.0, 1.0, 1.0), text_font=PiratesGlobals.getPirateFont(), scale=(0.09,
                                                                                                                                0.09,
                                                                                                                                0.09), relief=None, textMayChange=1, parent=self)
        return

    def _initIntervals(self):
        pass

    def pause(self):
        taskMgr.remove('RepairClock.update')

    def stop(self):
        taskMgr.remove('RepairClock.update')
        self.reset()
        self.stash()

    def start(self):
        taskMgr.add(self.update, 'RepairClock.update')
        self.unstash()

    def reset(self):
        self.gameTime = 0.0
        self.secondsLabel['text'] = '%i' % self.gameTime
        self.secondsLabel.setText()
        self.unstash()

    def restart(self):
        self.stop()
        self.start()

    def update(self, task):
        dt = globalClock.getDt()
        self.gameTime += dt
        minutes = int(self.gameTime / 60.0)
        seconds = self.gameTime % 60
        if minutes == 0:
            self.secondsLabel['text'] = '%i' % seconds
        elif seconds < 10:
            self.secondsLabel['text'] = '%i:0%i' % (minutes, seconds)
        else:
            self.secondsLabel['text'] = '%i:%i' % (minutes, seconds)
        self.secondsLabel.setText()
        return Task.cont

    def getTime(self):
        return self.gameTime

    def destroy(self):
        self.stop()
        DirectFrame.destroy(self)
        del self.gameTimes
        self.secondsLabel.destroy()
        del self.secondsLabel
        self.cleanup()

    def enterIdle(self):
        pass

    def exitIdle(self):
        pass

    def enterClean(self):
        pass

    def exitClean(self):
        pass