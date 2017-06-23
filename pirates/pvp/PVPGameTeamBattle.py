from pirates.pvp.PVPGameBase import PVPGameBase
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase
from pirates.pvp.MiniScoreItemGui import MiniScoreItemGui
from pirates.pvp import PVPGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class PVPGameTeamBattle(PVPGameBase):
    notify = directNotify.newCategory('PVPGameTeamBattle')

    def __init__(self, cr):
        PVPGameBase.__init__(self, cr)
        self.teamScore = 0
        self.carryingScore = 0
        self.otherTeamScore = 0
        self.shipsNearBase = {}
        self.maxTeamScore = 0
        self.prevTeamScore = None
        self.depositSound = loadSfx(SoundGlobals.SFX_PVP_TREASURE_DEPOSIT)
        self.maxCarry = None
        self.pendingInstanceRequest = None
        return

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
        return PLocalizer.TBTGame

    def getInstructions(self):
        return PLocalizer.PVPTeamBattleInstructions

    def handleUseKey(self, interactiveObj):
        pass

    def setMaxTeamScore(self, maxScore):
        self.maxTeamScore = maxScore

    def complete(self):
        PVPGameBase.complete(self)
        self.prevTeamScore = None
        return

    def setResults(self, stats, rank):
        for playerId, playerStats in stats:
            for stat, value in playerStats:
                self.stats[playerId][stat] = value

        self.statsChanged()
        localAvatar.guiMgr.createPVPCompleteUI(self.instance)
        localAvatar.guiMgr.setPVPResult('team', rank)
        localAvatar.guiMgr.showPVPCompleteUI()

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
            if playerId in base.cr.doId2do:
                playerTeam = base.cr.doId2do.get(playerId).getTeam()
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
            itemColorScale = PVPGlobals.TEAM_COLOR[team]
        else:
            itemColorScale = (1, 1, 1, 1)
        return MiniScoreItemGui(item, parent, self.instance, itemColorScale, self.instance.gameRules, blink)

    def getScoreText(self, scoreValue):
        team = scoreValue.get('Team')
        score = scoreValue.get('Score')
        if team == localAvatar.getTeam():
            maxTeamScore = str(self.maxTeamScore)
            return PLocalizer.PVPYourTeam + str(score)
        elif team == localAvatar.getDoId():
            maxCarry = str(self.maxCarry)
            return PLocalizer.PVPYourScoreIs + str(score)
        else:
            maxTeamScore = str(self.maxTeamScore)
            return PLocalizer.PVPOtherTeam + str(score)

    def getColumnStats(self):
        return [
         PVPGlobals.SCORE, PVPGlobals.DEATHS]

    def getColumnLabels(self):
        return [
         PLocalizer.PVPPlayer, PLocalizer.PVPScore, PLocalizer.PVPTimesDefeated]

    def addPlayer(self, playerId):
        self.stats[playerId] = {PVPGlobals.SCORE: 0,PVPGlobals.KILLS: 0,PVPGlobals.DEATHS: 0,PVPGlobals.TEAM: 0}
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

    def getStats(self):
        return self.getTeamStats()