from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from DistributedRepairGameBase import DistributedRepairGameBase
from DistributedRepairGameBase import GAME_OPEN, GAME_ORDER, DIFFICULTY_MAX, ON_LAND
from RepairClock import RepairClock
from RepairGameGUI import RepairGameGUI
from RepairGameFSM import RepairGameFSM
from RepairMousePicker import RepairMousePicker
import RepairGlobals
from pirates.audio import SoundGlobals

class DistributedRepairGame(DistributedRepairGameBase, DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRepairGame')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        DistributedRepairGameBase.__init__(self)
        self.accept('onCodeReload', self.codeReload)
        self.gameFSM = None
        self.goldBonus = 0
        return

    def codeReload(self):
        reload(RepairGlobals)

    def setGoldBonus(self, goldBonusAmount):
        self.goldBonus = goldBonusAmount

    def getGoldBonus(self):
        return self.goldBonus

    def start(self, location):
        self.notify.debug('starting DistributedRepairGame')
        if self.gameFSM:
            self.gameFSM.request('Off')
        self.location = location
        if location == ON_LAND:
            base.loadingScreen.showTarget(benchRepair=True)
        else:
            base.loadingScreen.showTarget(shipRepair=True)
        base.cr.loadingScreen.show()
        self.gameIndexRequested = -1
        self.gameProgress = [GAME_OPEN] * self.getGameCount()
        self.gameFSM = RepairGameFSM(self)
        self.gameFSM.request('Init')
        self.difficultyMax = DIFFICULTY_MAX + 0.0
        self.doIds2Rewards = {}
        self.cycleCompleteTime = 0
        self.currentGame = None
        self.gui = RepairGameGUI(self)
        base.loadingScreen.beginStep('left')
        self.repairClock = RepairClock(self)
        self.mousePicker = RepairMousePicker()
        self.games = []
        self.avIds2CurrentGameIndex = {}
        base.loadingScreen.endStep('left')
        base.loadingScreen.beginStep('games', 1, 48)
        for gameClass in GAME_ORDER[self.location]:
            self.games.append(gameClass(self))

        base.loadingScreen.endStep('games')
        self.gui.setGames(self.games)
        base.loadingScreen.beginStep('Intro')
        self.gameFSM.request('Intro')
        base.loadingScreen.endStep('Intro')
        base.loadingScreen.hide()
        return

    def stop(self):
        if not self.gameFSM:
            return
        self.notify.debug('stop')
        if self.gameFSM.getCurrentOrNextState() in ['Idle', 'MincroGame', 'CycleComplete']:
            self.gameFSM.request('Outro')
        else:
            self.cleanup()

    def cleanup(self):
        if not self.gameFSM:
            return
        if self.gameFSM.getCurrentOrNextState() != 'Off':
            self.gameFSM.request('Off')
            if not self.gameFSM:
                return
        self.gameIndexRequested = None
        del self.gameProgress[:]
        del self.gameProgress
        self.gameFSM.destroy()
        self.gameFSM = None
        self.mousePicker.destroy()
        self.mousePicker = None
        if hasattr(self, 'gui'):
            self.gui.destroy()
            self.gui = None
        if hasattr(self, 'repairClock'):
            self.repairClock.destroy()
            self.repairClock = None
        if hasattr(self, 'games'):
            for game in self.games:
                game.destroy()

            del self.games[:]
            del self.games
        shipRepairMusic = [
         SoundGlobals.MUSIC_PERFORMERS_02, SoundGlobals.MUSIC_PERFORMERS_07, SoundGlobals.MUSIC_PERFORMERS_09]
        for song in shipRepairMusic:
            base.musicMgr.stop(song)

        return

    def isCycleComplete(self):
        cycleComplete = True
        for progress in self.gameProgress:
            if progress != 100:
                cycleComplete = False
                break

        return cycleComplete

    def isThereAnOpenGame(self):
        isOpenGame = False
        for progress in self.gameProgress:
            if progress == -1:
                isOpenGame = True
                break

        return isOpenGame

    def d_requestMincroGame(self, gameIndex):
        if self.gameFSM.state in ['Idle', 'MincroGame']:
            self.gameIndexRequested = gameIndex
            self.sendUpdate('requestMincroGame', [gameIndex])

    def requestMincroGameResponse(self, success, difficulty):
        self.notify.debug('requestMincroGameResponse was %i' % success)
        if success:
            self.gameFSM.request('MincroGame', self.gameIndexRequested, difficulty)
            self.gui.setDifficulty(difficulty)
        else:
            self.notify.debug('MincroGame request denied')

    def d_reportMincroGameProgress(self, progress, rating=0):
        gameIndex = self.gameIndexRequested
        self.sendUpdate('reportMincroGameProgress', [gameIndex, progress, rating])

    def setMincroGameProgress(self, gameIndex, progress):
        self.notify.debug('setMincroGameProgress (%i, %i)' % (gameIndex, progress))
        if hasattr(self, 'gui') and self.gui:
            self.gui.setProgress(gameIndex, progress)
        if hasattr(self, 'gameProgress'):
            self.gameProgress[gameIndex] = progress
        if hasattr(self, 'currentGame') and self.currentGame:
            self.currentGame.updatePostWinLabel()

    def setAvIds2CurrentGameList(self, gameIndexList, doIdList):
        if hasattr(self, 'avIds2CurrentGameIndex'):
            self.avIds2CurrentGameIndex.clear()
            for i in range(len(gameIndexList)):
                self.avIds2CurrentGameIndex[doIdList[i]] = gameIndexList[i]

            self.gui.updatePirateNamesPerMincrogame(self.avIds2CurrentGameIndex)

    def setAllMincroGameProgress(self, progressList):
        for i in range(len(progressList)):
            self.setMincroGameProgress(i, progressList[i])

    def d_reportMincroGameScore(self, score):
        gameIndex = self.gameIndexRequested
        self.sendUpdate('reportMincroGameScore', [gameIndex, score])

    def cycleComplete(self, difficulty=0, doIds=[], rewards=[], totalTime=0):
        if self.gameFSM == None:
            return
        if self.gameFSM.state == 'Intro':
            self.resetMincroGameProgress()
            self.gui.setDifficulty(difficulty)
            return
        self.setRewards(doIds, rewards)
        self.setCycleCompleteTime(totalTime)
        self.gameFSM.request('CycleComplete')
        self.gui.setDifficulty(difficulty)
        return

    def setRewards(self, doIds, rewards):
        self.doIds2Rewards.clear()
        if len(doIds) == len(rewards):
            for i in range(len(doIds)):
                self.doIds2Rewards[doIds[i]] = rewards[i]

        else:
            self.notify.warning('List of players and list of rewards are a different length doIds:%d and rewards:%d' % (len(doIds), len(rewards)))

    def getReward(self, doId):
        if doId in self.doIds2Rewards:
            return self.doIds2Rewards[doId]
        else:
            self.notify.warning("doId: %i isn't in self.doIds2Rewards" % doId)
            return -1

    def setCycleCompleteTime(self, totalTime):
        self.cycleCompleteTime = totalTime

    def getCycleCompleteTime(self):
        return self.cycleCompleteTime

    def shipDamaged(self, wasGrapeshot=False, difficulty=0):
        if hasattr(self, 'gui') and self.gui:
            self.gui.onShipDamaged(wasGrapeshot)
            self.gui.setDifficulty(difficulty)

    def resetMincroGameProgress(self):
        self.setAllMincroGameProgress([GAME_OPEN] * self.getGameCount())

    def delete(self):
        DistributedObject.delete(self)
        self.ignore('onCodeReload')
        if hasattr(self, 'gameFSM'):
            self.cleanup()

    def handleArrivedOnShip(self, ship):
        pass

    def handleLeftShip(self, ship):
        pass