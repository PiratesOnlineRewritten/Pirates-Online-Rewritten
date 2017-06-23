from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.task.Task import Task
from pandac.PandaModules import *
from direct.distributed.ClockDelta import *
from direct.showbase import PythonUtil
from pirates.pirate import HumanDNA
from pirates.piratesbase import PiratesGlobals
from pirates.minigame import DistributedGameTable
from pirates.minigame import BishopsHandGame
from pirates.minigame import BishopsHandGlobals

class ResultsFrame(DirectFrame):

    def __init__(self, *args, **kwargs):
        DirectFrame.__init__(self, *args, **kwargs)
        self.initialiseoptions(ResultsFrame)
        self.textLabel = DirectLabel(parent=self, relief=None, pos=(0, 0, 0.5), scale=0.2, text='')
        return


class DistributedBishopsHandTable(DistributedGameTable.DistributedGameTable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBishopsHandTable')
    SeatInfo = (
     (
      Vec3(-4, 6.5, 0), Vec3(180, 0, 0)), (Vec3(-11, 0, 0), Vec3(-90, 0, 0)), (Vec3(-4, -6.5, 0), Vec3(0, 0, 0)), (Vec3(0, -6.5, 0), Vec3(0, 0, 0)), (Vec3(4, -6.5, 0), Vec3(0, 0, 0)), (Vec3(11, 0, 0), Vec3(90, 0, 0)), (Vec3(4, 6.5, 0), Vec3(180, 0, 0)))
    NumSeats = 7

    def __init__(self, cr):
        DistributedGameTable.DistributedGameTable.__init__(self, cr)
        self.pendingStakes = 0
        self.activeStakes = 0
        self.runningStakes = 0
        self.seatStatus = [ [0, -1] for x in range(self.NumSeats) ]
        dna = HumanDNA.HumanDNA()
        self.dealer = self.createDealer('Dealer', dna, Vec3(0, 6.5, 0), Vec3(180, 0, 0))
        self.timerLabel = None
        self.resultsFrame = None
        self.game = None
        return

    def generate(self):
        DistributedGameTable.DistributedGameTable.generate(self)
        self.setName(self.uniqueName('DistributedBishopsHandTable'))
        self.reparentTo(render)

    def announceGenerate(self):
        DistributedGameTable.DistributedGameTable.announceGenerate(self)
        self.timerLabel = DirectLabel(relief=None, text='', text_fg=(1, 1, 1, 1), text_shadow=(0,
                                                                                               0,
                                                                                               0,
                                                                                               1), textMayChange=1, text_font=PiratesGlobals.getPirateOutlineFont())
        self.timerLabel.setZ(5)
        self.timerLabel.setBillboardPointEye()
        self.timerLabel.reparentTo(self)
        self.resultsFrame = ResultsFrame()
        return

    def delete(self):
        self.__stopGameTimer()
        self.timerLabel.destroy()
        self.timerLabel = None
        DistributedGameTable.DistributedGameTable.delete(self)
        self.dealer.delete()
        del self.dealer
        return

    def getTableModel(self):
        table = loader.loadModel('models/props/Cardtable_Pill')
        table.setScale(2.5, 2.5, 1)
        return table

    def localAvatarSatDown(self, seatIndex):
        self.notify.debug('LocalAvatarSatDown')
        DistributedGameTable.DistributedGameTable.localAvatarSatDown(self, seatIndex)
        camera.setPosHpr(self, 0, -10, 20, 0, -65, 0)
        base.camLens.setMinFov(55)
        self.game = BishopsHandGame.BishopsHandGame(self.gameCallback, seatIndex)
        self.game.request('SeatedUnjoined')

    def localAvatarGotUp(self, seatIndex):
        DistributedGameTable.DistributedGameTable.localAvatarGotUp(self, seatIndex)
        self.game.destroy()
        self.game = None
        return

    def isLocalAvatarPlaying(self):
        if self.isLocalAvatarSeated():
            if self.seatStatus[self.localAvatarSeat][1] >= 2:
                return True
        return False

    def __stopGameTimer(self):
        taskMgr.remove('BHT-game-timer')
        self.timerLabel['text'] = ''

    def abortRound(self):
        taskMgr.remove('BHT-start-round')

    def gameCallback(self, action, *args):
        if action == BishopsHandGlobals.PLAYER_ACTIONS.JoinGame:
            self.d_clientAction([action, 0])
            self.game.request('SeatedJoined')
        elif action == BishopsHandGlobals.PLAYER_ACTIONS.UnjoinGame:
            self.d_clientAction([action, 0])
            self.game.request('SeatedUnjoined')
        elif action == BishopsHandGlobals.PLAYER_ACTIONS.RejoinGame:
            self.d_clientAction([action, 0])
        elif action == BishopsHandGlobals.PLAYER_ACTIONS.Continue:
            self.d_clientAction([action, 0])
        elif action == BishopsHandGlobals.PLAYER_ACTIONS.Resign:
            self.d_clientAction([action, 0])
        elif action == BishopsHandGlobals.PLAYER_ACTIONS.Leave:
            self.d_clientAction([action, 0])
        elif action == BishopsHandGlobals.PLAYER_ACTIONS.Progress:
            progress = args[0]
            self.d_sendProgress(progress)
        elif action == -1:
            self.requestExit()
        else:
            self.notify.error('gameCallback: unknown action: %s' % action)

    def d_clientAction(self, action):
        self.sendUpdate('clientAction', [action])

    def d_sendRoundResults(self, results):
        self.sendUpdate('receiveRoundResults', results)

    def d_sendProgress(self, progress):
        self.sendUpdate('receiveProgress', progress)

    def askForClientAction(self, action, delay, timestamp):
        act, data = action
        if act == BishopsHandGlobals.GAME_ACTIONS.AskForContinue:
            if self.game:
                localTimestamp = globalClockDelta.networkToLocalTime(timestamp)
                localTime = globalClock.getFrameTime()
                timePassed = localTime - localTimestamp
                timeLeft = delay - timePassed
                if data == BishopsHandGlobals.CONTINUE_OPTIONS.Resign:
                    self.game.request('WaitingForRound')
                    self.game.startTimer(timeLeft)
                elif data == BishopsHandGlobals.CONTINUE_OPTIONS.Continue:
                    self.game.request('Continue')
                    self.game.startTimer(timeLeft)
                elif data == BishopsHandGlobals.CONTINUE_OPTIONS.Rejoin:
                    self.game.request('Rejoin')
                    self.game.startTimer(timeLeft)
                elif data == BishopsHandGlobals.CONTINUE_OPTIONS.Leave:
                    self.game.request('Leave')
                    self.game.startTimer(timeLeft)
                else:
                    self.notify.error('askForClientAction-Continue() specified invalid data.')
        if act == BishopsHandGlobals.GAME_ACTIONS.NotifyOfWin:
            if data:
                self.notify.debug('Win!')
            else:
                self.notify.debug('Lost!')

    def setTableState(self, tableState, seatStatus):
        if self.isLocalAvatarPlaying():
            self.notify.debug('localAv is playing')
            self.game.setTableState(tableState, self.seatStatus, seatStatus)
        elif self.isLocalAvatarSeated():
            self.game.setTableState(tableState, self.seatStatus, seatStatus)
        self.seatStatus = seatStatus

    def setPendingStakes(self, amount):
        self.pendingStakes = amount

    def setActiveStakes(self, amount):
        self.activeStakes = amount

    def setRunningStakes(self, amount):
        self.runningStakes = amount

    def setGameTimer(self, time, timestamp):
        networkTime = globalClockDelta.networkToLocalTime(timestamp)
        localTime = globalClock.getFrameTime()
        timePassed = localTime - networkTime
        timeLeft = time - timePassed
        self.notify.debug('\ntime:\t%f\nnet:\t%f\nlocal:\t%f\npassed:\t%f\nleft:\t%f' % (time, networkTime, localTime, timePassed, timeLeft))
        self.__stopGameTimer()
        if timeLeft > 0:

            def timerTask(task):
                if task.time < task.timer:
                    self.timerLabel['text'] = `(int(PythonUtil.bound(task.timer - task.time, 0, time) + 1.0))`
                    return Task.cont
                else:
                    self.timerLabel['text'] = ''
                    return Task.done

            t = taskMgr.add(timerTask, 'BHT-game-timer')
            t.timer = timeLeft

    def startRound(self, sequence, delay, timestamp):
        self.notify.debug('startRound')
        self.game.request('WaitingForRound')
        self.notify.debug('Received sequence: ' + `sequence`)
        if self.isLocalAvatarPlaying():
            self.notify.debug('initing round')
            self.game.initRound(sequence)
        localTimestamp = globalClockDelta.networkToLocalTime(timestamp)
        localTime = globalClock.getFrameTime()
        timePassed = localTime - localTimestamp
        timeLeft = delay - timePassed

        def beginPlay():
            self.game.request('PlayingRound')
            self.game.startRound()

        taskMgr.doMethodLater(timeLeft, beginPlay, 'BHT-start-round', extraArgs=[])
        self.game.startTimer(timeLeft)

    def leftGame(self):
        self.notify.debug('leftGame')
        self.abortRound()
        if self.game:
            self.game.stopRound()
            if self.seatStatus[self.localAvatarSeat][1] > 0:
                self.game.request('SeatedJoined')
            else:
                self.game.request('SeatedUnjoined')

    def setProgressReport(self, report):
        if self.game:
            self.game.reportProgress(report)