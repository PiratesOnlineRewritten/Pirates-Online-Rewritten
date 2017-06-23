from pirates.pvp.DistributedPVPInstance import DistributedPVPInstance
from pirates.piratesbase import PiratesGlobals
from pirates.pvp import PVPGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase
from pirates.pvp.MiniScoreItemGui import MiniScoreItemGui

class DistributedPVPBattle(DistributedPVPInstance):
    notify = directNotify.newCategory('DistributedPVPBattle')

    def __init__(self, cr):
        DistributedPVPInstance.__init__(self, cr)

    def generate(self):
        DistributedPVPInstance.generate(self)

    def announceGenerate(self):
        DistributedPVPInstance.announceGenerate(self)

    def disable(self):
        DistributedPVPInstance.disable(self)
        base.localAvatar.guiMgr.hidePVPUI()

    def delete(self):
        self.ignoreAll()
        DistributedPVPInstance.delete(self)

    def getTitle(self):
        return PLocalizer.BTLGame

    def getInstructions(self):
        return PLocalizer.PVPBattleInstructions

    def hasTimeLimit(self):
        return True

    def getTimeLimit(self):
        return self._timeLimit

    def setTimeLimit(self, timeLimit):
        self._timeLimit = timeLimit

    def getScoreList(self):
        scoreList = []
        for playerId, stats in self.stats.items():
            if playerId not in self.names:
                continue
            scoreList.append({'Player': playerId,'Score': stats[PVPGlobals.SCORE]})

        scoreList.sort(self.sortScores)
        return scoreList

    def createScoreboardItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        itemColorScale = None
        player = item.get('Player')
        score = item.get('Score')
        playerName = self.names[player]
        playerTeam = self.teams[player]
        if player == localAvatar.doId:
            itemColorScale = (1, 1, 1, 1)
        elif playerTeam != None:
            itemColorScale = PVPGlobals.getTeamColor(playerTeam)
        item['Player'] = playerName
        return MiniScoreItemGui(item, parent, self, itemColorScale)

    def getScoreText(self, scoreValue):
        return '     ' + str(scoreValue.get('Score')) + ' ' + str(scoreValue.get('Player'))

    def getColumnStats(self):
        return [
         PVPGlobals.SCORE, PVPGlobals.DEATHS]

    def getColumnLabels(self):
        return [
         PLocalizer.PVPPlayer, PLocalizer.PVPScore, PLocalizer.PVPTimesDefeated]

    def addPlayerStats(self, playerId):
        self.stats[playerId] = {PVPGlobals.SCORE: 0,PVPGlobals.KILLS: 0,PVPGlobals.DEATHS: 0}

    def setPlayerStat(self, playerId, stat, value):
        if playerId not in self.names or playerId not in self.stats:
            return
        playerName = self.names[playerId]
        self.stats[playerId][stat] = value
        self.statsChanged()
        if stat == PVPGlobals.SCORE:
            self.scoreChanged()

    def sortStats(self, stats):
        return sorted(sorted(stats, key=lambda x: int(x[1][1][1])), key=lambda x: int(x[1][0][1]), reverse=True)