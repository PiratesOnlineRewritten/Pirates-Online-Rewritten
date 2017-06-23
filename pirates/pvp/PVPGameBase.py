from direct.distributed.ClockDelta import globalClockDelta
from direct.distributed.DistributedObject import DistributedObject
from direct.fsm import FSM
from pirates.piratesbase import PLocalizer
from pirates.pvp import PVPGlobals
from pirates.piratesgui import PiratesGuiGlobals
import PVPRulesPanel
import random
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.StatRowGui import StatRowGui
from pirates.piratesgui.StatRowHeadingGui import StatRowHeadingGui

class ScoreboardHolder():

    def __init__(self, gameRules):
        self.gameRules = gameRules

    def getItemList(self):
        return self.gameRules.getScoreList()

    def getItemChangeMsg(self):
        return self.gameRules.taskName('scoreChanged')

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        return self.gameRules.createScoreboardItem(item, parent, itemType=None, columnWidths=[], color=None)


class StatsHolder():

    def __init__(self, gameRules):
        self.gameRules = gameRules

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        if itemType == PiratesGuiGlobals.UIListItemType_ColumHeadings:
            newItem = StatRowHeadingGui(item, self.gameRules.getColumnLabels(), parent, itemHeight=PiratesGuiGlobals.TMCompletePageHeight / 16, itemWidths=columnWidths)
        else:
            newItem = StatRowGui(item, self.gameRules.getColumnLabels(), parent, itemHeight=PiratesGuiGlobals.TMCompletePageHeight / 16, itemWidths=columnWidths, txtColor=color)
        newItem.setup()
        return newItem

    def getItemChangeMsg(self):
        return self.gameRules.taskName('statsChanged')

    def getItemList(self):
        return self.gameRules.getStats()

    def getRowTextColor(self, rowHeading):
        return self.gameRules.rowColors.get(rowHeading)


class PVPGameBase(DistributedObject, FSM.FSM):
    notify = directNotify.newCategory('PVPGameBase')
    RulesDoneEvent = 'rulesDone'

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        FSM.FSM.__init__(self, 'PVPGameBase')
        base.cr.gameRules = self
        self.scoreboardHolder = ScoreboardHolder(self)
        self.statsHolder = StatsHolder(self)
        self.stats = {}
        self.rowColors = {}
        localAvatar.guiMgr.radarGui.request('On')
        self.request('Init')

    def delete(self):
        self.ignoreAll()
        base.cr.gameRules = None
        DistributedObject.delete(self)
        return

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.eventRng = random.Random(self.doId)
        self.request('WaitForServerStart')

    def enterInit(self):
        pass

    def exitInit(self):
        pass

    def showRules(self):
        self.rulesPanel = PVPRulesPanel.PVPRulesPanel('PVPRulesPanel', self.getTitle(), self.getInstructions())

    def hideRules(self):
        self.rulesPanel.hide()
        self.rulesPanel.destroy()

    def enterWaitForServerStart(self):
        self.showRules()

    def exitWaitForServerStart(self):
        self.hideRules()

    def enterGame(self):
        pass

    def exitGame(self):
        pass

    def enterScoreScreen(self):
        pass

    def exitScoreScreen(self):
        pass

    def enterAvatarExited(self):
        pass

    def exitAvatarExited(self):
        pass

    def enterCleanup(self):
        pass

    def exitCleanup(self):
        pass

    def allPresent(self, avIdList):
        for playerId in avIdList:
            self.addPlayer(playerId)

        localAvatar.guiMgr.createPVPUI(self.scoreboardHolder)
        localAvatar.guiMgr.createPVPStatus(self.statsHolder)

    def setGameStart(self, timestamp):
        self.gameStartTime = globalClockDelta.networkToLocalTime(timestamp)
        localAvatar.guiMgr.showPVPTimer(self)
        localAvatar.guiMgr.showPVPTeamIcon()
        localAvatar.guiMgr.createPVPUI(self.scoreboardHolder)
        localAvatar.guiMgr.createPVPStatus(self.statsHolder)
        self.statsChanged()
        self.scoreChanged()
        localAvatar.guiMgr.showPVPUI()
        self.accept('tab', localAvatar.guiMgr.showPVPStatus)
        self.accept('tab-up', localAvatar.guiMgr.hidePVPStatus)
        self.request('Game')

    def setGameAbort(self):
        self.notify.warning('BASE: setGameAbort: Aborting game')
        self.normalExit = 0
        self.request('Cleanup')

    def getTitle(self):
        return PLocalizer.PVPDefaultTitle

    def getInstructions(self):
        return PLocalizer.PVPDefaultInstructions

    def setInstanceId(self, instanceId):
        self.instanceId = instanceId
        self.instance = self.cr.doId2do.get(self.instanceId)

    def replay(self):
        localAvatar.guiMgr.createPVPUI(self.scoreboardHolder)

    def complete(self):
        self.ignore('tab')
        self.ignore('tab-up')
        localAvatar.guiMgr.removePVPUI()

    def respawn(self):
        self.instance.teleportToPosStep1()

    def handleUseKey(self, interactiveObj):
        pass

    def setResults(self, stats, rank):
        for playerId, playerStats in stats:
            for stat, value in playerStats:
                self.stats[playerId][stat] = value

        self.statsChanged()
        localAvatar.guiMgr.createPVPCompleteUI(self.instance)
        localAvatar.guiMgr.setPVPResult('player', rank)
        localAvatar.guiMgr.showPVPCompleteUI()

    def hasTimeLimit(self):
        return False

    def getTimeLimit(self):
        return 0

    def scoreChanged(self):
        messenger.send(self.taskName('scoreChanged'))

    def sortScores(self, item1, item2):
        return item2.get('Score') - item1.get('Score')

    def getScoreList(self):
        return None

    def createScoreboardItem(self):
        return None

    def getScoreText(self, scoreValue):
        return ''

    def statsChanged(self):
        messenger.send(self.taskName('statsChanged'))

    def getColumnStats(self):
        return [
         PVPGlobals.KILLS, PVPGlobals.DEATHS]

    def getColumnLabels(self):
        return [
         PLocalizer.PVPPlayer, PLocalizer.PVPEnemiesDefeated, PLocalizer.PVPTimesDefeated]

    def addPlayer(self, playerId):
        if playerId in base.cr.doId2do:
            player = base.cr.doId2do.get(playerId)
            playerName = player.getName()
            playerTeam = player.getTeam()
            teamColor = PVPGlobals.TEAM_COLOR[playerTeam]
            if playerId == localAvatar.doId:
                teamColor = (1, 1, 1, 1)
            self.rowColors[playerName] = teamColor

    def sortStats(self, stats):
        stats = sorted(stats, key=lambda x: x[1][PVPGlobals.SCORE])

    def setPlayerStat(self, playerId, stat, value):
        if playerId in base.cr.doId2do:
            playerName = base.cr.doId2do.get(playerId).getName()
        self.stats[playerId][stat] = value
        self.statsChanged()

    def setStats(self, stats):
        for playerId, playerStats in stats:
            for stat, value in playerStats:
                self.stats[playerId][stat] = value

        self.statsChanged()

    def sortStats(self, stats):
        return sorted(stats, key=lambda x: x[1][PVPGlobals.SCORE])

    def getStats(self):
        return self.getPlayerStats()

    def getPlayerStats(self):
        displayStats = []
        for playerId, stats in self.stats.items():
            if playerId in base.cr.doId2do:
                player = base.cr.doId2do.get(playerId)
                playerName = player.getName()
                playerTeam = player.getTeam()
            else:
                playerName = '???'
                playerTeam = 0
            playerStats = []
            for stat in self.getColumnStats():
                playerStats.append([PVPGlobals.statText[stat], str(stats[stat])])

            if playerId == localAvatar.doId:
                playerColor = (1, 1, 1, 1)
            else:
                playerColor = PVPGlobals.TEAM_COLOR[playerTeam]
            displayStats.append([playerName, playerStats, ['color', playerColor]])

        displayStats = self.sortStats(displayStats)
        displayStats.insert(0, self.getColumnLabels())
        return displayStats

    def getTeamStats(self):
        displayStats = []
        teams = {}
        for playerId, stats in self.stats.items():
            if playerId in base.cr.doId2do:
                player = base.cr.doId2do.get(playerId)
                playerName = player.getName()
            else:
                playerName = '???'
            if not teams.get(stats[PVPGlobals.TEAM]):
                teams[stats[PVPGlobals.TEAM]] = []
            playerStats = []
            for stat in self.getColumnStats():
                playerStats.append([PVPGlobals.statText[stat], str(stats[stat])])

            if playerId == localAvatar.doId:
                playerColor = (1, 1, 1, 1)
            else:
                playerColor = None
            teams[stats[PVPGlobals.TEAM]].append([playerName, playerStats, ['color', playerColor]])

        for team, teamStats in teams.items():
            teamTotals = []
            for stat in self.getColumnStats():
                teamTotals.append([PVPGlobals.statText[stat], 0])

            for playerName, playerStats, color in teamStats:
                for i in range(len(playerStats)):
                    teamTotals[i][1] = str(int(teamTotals[i][1]) + int(playerStats[i][1]))

            teamStat = [
             'Team %s' % team, teamTotals, ['color', PVPGlobals.TEAM_COLOR[team]]]
            teamStats = self.sortStats(teamStats)
            teamStats.insert(0, teamStat)
            displayStats += teamStats

        displayStats.insert(0, self.getColumnLabels())
        return displayStats

    def setPvpEvent(self, eventId, data):
        if eventId is PVPGlobals.EventDefeat:
            defeaterId, defeatedId = data
            self.handleDefeatEvent(defeaterId, defeatedId)

    def handleDefeatEvent(self, defeaterId, defeatedId):
        if defeaterId == defeatedId:
            thirdPersonMsgs = [PLocalizer.PVPSuicide]
            if defeatedId == localAvatar.doId:
                firstPersonMsgs = [
                 PLocalizer.PVPYouSuicide]
            else:
                firstPersonMsgs = None
        else:
            thirdPersonMsgs = [
             PLocalizer.PVPDefeat]
            if defeatedId == localAvatar.doId:
                firstPersonMsgs = [
                 PLocalizer.PVPYouWereDefeated]
            else:
                if defeaterId == localAvatar.doId:
                    firstPersonMsgs = [
                     PLocalizer.PVPYouDefeated]
                else:
                    firstPersonMsgs = None
                firstPersonMsg = None
                if firstPersonMsgs:
                    firstPersonMsg = self.eventRng.choice(firstPersonMsgs)
                thirdPersonMsg = self.eventRng.choice(thirdPersonMsgs)
                defeaterName = base.cr.doId2do.get(defeaterId).getName()
                defeatedName = base.cr.doId2do.get(defeatedId).getName()
                d = {'defeater': defeaterName,'defeated': defeatedName}
                if firstPersonMsg:
                    firstPersonMsg = firstPersonMsg % d
            thirdPersonMsg = thirdPersonMsg % d
            if firstPersonMsg:
                localAvatar.guiMgr.messageStack.addTextMessage(firstPersonMsg)
        base.talkAssistant.receiveSystemMessage(thirdPersonMsg)
        return