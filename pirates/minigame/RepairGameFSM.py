from MinigameFSM import MinigameFSM
from direct.directnotify import DirectNotifyGlobal

class RepairGameFSM(MinigameFSM):

    def __init__(self, gameObject):
        self.gameObject = gameObject
        notify = DirectNotifyGlobal.directNotify.newCategory('RepairGameFSM')
        MinigameFSM.__init__(self, 'RepairGameFSM')
        self.defaultTransitions = {'Init': ['Intro', 'Final', 'Off'],'Intro': ['Idle', 'Complete', 'Final', 'Off'],'Idle': ['MincroGame', 'CycleComplete', 'Final', 'Outro', 'Intro', 'Off'],'MincroGame': ['MincroGame', 'CycleComplete', 'Idle', 'Final', 'Outro', 'Off'],'CycleComplete': ['Outro', 'Idle', 'Final', 'Off'],'Outro': ['Off', 'Final'],'Final': ['Off'],'Off': []}

    def enterOff(self):
        self.notify.info("enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState))

    def exitOff(self):
        self.notify.info("exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState))

    def enterInit(self):
        self.notify.info("enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState))

    def exitInit(self):
        self.notify.info("exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState))

    def enterIntro(self):
        self.notify.info("enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState))
        self.gameObject.gui.introSequence.start()

    def exitIntro(self):
        self.notify.info("exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState))
        self.gameObject.gui.introSequence.clearToInitial()
        self.gameObject.gui.repairGamePicker.setEnabled(True)

    def enterIdle(self):
        self.notify.info("enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState))
        self.gameObject.gui.showIdleMessage()
        self.gameObject.gui.setRepairTitle()

    def exitIdle(self):
        self.notify.info("exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState))
        self.gameObject.gui.hideIdleMessage()
        self.gameObject.gui.clearTitle()

    def enterMincroGame(self, gameIndex, difficulty):
        self.notify.info("enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState))
        self.gameObject.currentGame = self.gameObject.games[gameIndex]
        self.gameObject.currentGame.setDifficulty(difficulty)
        self.gameObject.currentGame.request('Intro')

    def exitMincroGame(self):
        self.notify.info("exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState))
        if self.gameObject.currentGame.complete:
            pass
        else:
            index = self.gameObject.games.index(self.gameObject.currentGame)
        self.gameObject.currentGame.demand('Idle')
        self.gameObject.currentGame = None
        self.gameObject.repairClock.stop()
        return

    def enterCycleComplete(self):
        self.notify.info("enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState))
        self.gameObject.gui.setRepairTitle()
        self.gameObject.gui.cycleCompleteSequence.start()

    def exitCycleComplete(self):
        self.notify.info("exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState))
        self.gameObject.gui.clearTitle()

    def enterOutro(self):
        self.notify.info("enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState))
        self.gameObject.gui.cycleCompleteSequence.clearToInitial()
        self.gameObject.gui.outroSequence.start()

    def exitOutro(self):
        self.notify.info("exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState))
        self.gameObject.gui.outroSequence.finish()

    def enterFinal(self):
        self.notify.info("enter%s: '%s' -> '%s'" % (self.newState, self.oldState, self.newState))
        seq = Sequence(Wait(0.01), Func(self.gameObject.cleanUp))
        seq.start()

    def exitFinal(self):
        self.notify.info("exit%s: '%s' -> '%s'" % (self.oldState, self.oldState, self.newState))