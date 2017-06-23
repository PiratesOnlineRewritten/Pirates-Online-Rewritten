from pirates.pvp.PVPGameBase import PVPGameBase
from pirates.piratesbase import PiratesGlobals
from pirates.pvp import PVPGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase
from pirates.pvp.MiniScoreItemGui import MiniScoreItemGui

class PVPGameBattle(PVPGameBase):
    notify = directNotify.newCategory('PVPGameBattle')

    def __init__(self, cr):
        PVPGameBase.__init__(self, cr)
        self.pendingInstanceRequest = None
        return

    def generate(self):
        PVPGameBase.generate(self)

    def announceGenerate(self):
        PVPGameBase.announceGenerate(self)
        self.pendingInstanceRequest = base.cr.relatedObjectMgr.requestObjects([self.instanceId], eachCallback=self.instanceGenerated)

    def instanceGenerated(self, instanceObj):
        self.instance = instanceObj

    def disable(self):
        PVPGameBase.disable(self)
        if self.pendingInstanceRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingInstanceRequest)
            self.pendingInstanceRequest = None
        base.localAvatar.guiMgr.hidePVPUI()
        return

    def delete(self):
        self.ignoreAll()
        PVPGameBase.delete(self)

    def getTitle(self):
        return PLocalizer.BTLGame

    def getInstructions(self):
        return PLocalizer.PVPBattleInstructions

    def complete(self):
        PVPGameBase.complete(self)
        self.prevTeamScore = None
        return

    def hasTimeLimit(self):
        return True

    def getTimeLimit(self):
        return self._timeLimit

    def setTimeLimit(self, timeLimit):
        self._timeLimit = timeLimit

    def getScoreList(self):
        scoreList = []
        for playerId, stats in self.stats.items():
            scoreList.append({'Player': playerId,'Score': stats[PVPGlobals.SCORE]})

        scoreList.sort(self.sortScores)
        return scoreList

    def createScoreboardItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        itemColorScale = None
        player = item.get('Player')
        score = item.get('Score')
        team = None
        name = '???'
        if player in base.cr.doId2do:
            avatar = base.cr.doId2do.get(player)
            team = avatar.getTeam()
            name = avatar.getName()
        if player == localAvatar.doId:
            itemColorScale = (1, 1, 1, 1)
        elif team != None:
            itemColorScale = PVPGlobals.TEAM_COLOR[team]
        item['Player'] = name
        return MiniScoreItemGui(item, parent, self.instance, itemColorScale, self.instance.gameRules)

    def getScoreText(self, scoreValue):
        return '     ' + str(scoreValue.get('Score')) + ' ' + str(scoreValue.get('Player'))

    def getColumnStats(self):
        return [
         PVPGlobals.SCORE, PVPGlobals.DEATHS]

    def getColumnLabels(self):
        return [
         PLocalizer.PVPPlayer, PLocalizer.PVPScore, PLocalizer.PVPTimesDefeated]

    def addPlayer(self, playerId):
        self.stats[playerId] = {PVPGlobals.SCORE: 0,PVPGlobals.KILLS: 0,PVPGlobals.DEATHS: 0}
        PVPGameBase.addPlayer(self, playerId)

    def setPlayerStat(self, playerId, stat, value):
        if playerId in base.cr.doId2do:
            playerName = base.cr.doId2do.get(playerId).getName()
        self.stats[playerId][stat] = value
        self.statsChanged()
        if stat == PVPGlobals.SCORE:
            self.scoreChanged()

    def sortStats(self, stats):
        return sorted(sorted(stats, key=lambda x: int(x[1][1][1])), key=lambda x: int(x[1][0][1]), reverse=True)