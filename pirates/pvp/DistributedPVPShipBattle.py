from pirates.pvp.DistributedPVPInstance import DistributedPVPInstance
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase
from pirates.pvp.MiniScoreItemGui import MiniScoreItemGui
from pirates.pvp import PVPGlobals

class DistributedPVPShipBattle(DistributedPVPInstance):
    notify = directNotify.newCategory('DistributedPVPShipBattle')

    def __init__(self, cr):
        DistributedPVPInstance.__init__(self, cr)
        self.prevTeamScore = None
        self.localShip = None
        self.teleportCallback = None
        return

    def announceGenerate(self):
        DistributedPVPInstance.announceGenerate(self)

    def disable(self):
        DistributedPVPInstance.disable(self)
        base.localAvatar.guiMgr.hidePVPUI()

    def getTitle(self):
        return PLocalizer.SBTGame

    def getInstructions(self):
        return PLocalizer.PVPShipBattleInstructions

    def complete(self):
        DistributedPVPInstance.complete(self)
        ship = base.localAvatar.ship
        if self.localShip:
            if self.localShip.sinkTrack:
                self.localShip.sinkTrack.pause()
                self.localShip.sinkTrack = None
        self.prevTeamScore = None
        return

    def setShipDoId(self, shipId):
        print '_shipId %s' % shipId
        self.shipRequest = base.cr.relatedObjectMgr.requestObjects([shipId], eachCallback=self._shipArrived)

    def _shipArrived(self, ship):
        self.localShip = ship
        ship.registerBuildCompleteFunction(Functor(self._boardShip, ship))

    def _boardShip(self, ship):
        print '_boardShip %s' % ship.doId
        self.acceptOnce(ship.uniqueName('localAvBoardedShip'), self._boardShipDone)
        localAvatar.placeOnShip(ship, pvp=True)

    def _boardShipDone(self):
        self.sendUpdate('setBoarded', [])
        localAvatar.motionFSM.on()
        base.cr.loadingScreen.hide()

    def updateShipProximityText(self, ship):
        ship.b_setIsBoardable(ship.isBoardable)

    def respawn(self):
        posHpr = self.instance.cr.activeWorld.spawnInfo[0]
        localAvatar.setPos(posHpr[0], posHpr[1], posHpr[2])

    def hasTimeLimit(self):
        return True

    def getTimeLimit(self):
        return self._timeLimit

    def setTimeLimit(self, timeLimit):
        self._timeLimit = timeLimit

    def sortScores(self, item1, item2):
        team1 = item1.get('Team')
        team2 = item2.get('Team')
        if team1 == localAvatar.getDoId():
            return 1000
        else:
            return item2.get('Score') - item1.get('Score')

    def getScoreList(self):
        scoreList = []
        teamScores = {}
        for playerId, stats in self.stats.items():
            playerScore = stats[PVPGlobals.SCORE]
            playerTeam = self.teams[playerId]
            if playerTeam in teamScores:
                teamScores[playerTeam] += playerScore
            else:
                teamScores[playerTeam] = playerScore
            if playerId == localAvatar.doId:
                scoreList.append({'Team': playerId,'Score': playerScore})

        for teamName, teamScore in teamScores.items():
            scoreList.append({'Team': teamName,'Score': teamScore})

        scoreList.sort(self.sortScores)
        return scoreList

    def createScoreboardItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        itemColorScale = None
        blink = False
        team = item.get('Team')
        score = item.get('Score')
        if team == localAvatar.getTeam():
            if self.prevTeamScore != None and score < self.prevTeamScore:
                blink = True
            self.prevTeamScore = score
        if team != localAvatar.doId:
            itemColorScale = PVPGlobals.getTeamColor(team)
        else:
            itemColorScale = (1, 1, 1, 1)
        return MiniScoreItemGui(item, parent, self, itemColorScale, blink)

    def getScoreText(self, scoreValue):
        team = scoreValue.get('Team')
        score = scoreValue.get('Score')
        if team == localAvatar.getTeam():
            return PLocalizer.PVPYourTeam + str(score)
        elif team == localAvatar.getDoId():
            return PLocalizer.PVPYourScoreIs + str(score)
        else:
            return PLocalizer.PVPOtherTeam + str(score)

    def getColumnStats(self):
        return [
         PVPGlobals.SCORE, PVPGlobals.DEATHS]

    def getColumnLabels(self):
        return [
         PLocalizer.PVPPlayer, PLocalizer.PVPScore, PLocalizer.PVPTimesDefeated]

    def addPlayerStats(self, playerId):
        self.stats[playerId] = {PVPGlobals.SCORE: 0,PVPGlobals.KILLS: 0,PVPGlobals.DEATHS: 0,PVPGlobals.TEAM: 0}

    def setPlayerStat(self, playerId, stat, value):
        playerName = self.names[playerId]
        self.stats[playerId][stat] = value
        self.statsChanged()
        if stat == PVPGlobals.SCORE:
            self.scoreChanged()

    def sortStats(self, stats):
        return sorted(sorted(stats, key=lambda x: int(x[1][1][1])), key=lambda x: int(x[1][0][1]), reverse=True)

    def getStats(self):
        return self.getTeamStats()