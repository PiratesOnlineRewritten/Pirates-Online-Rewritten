from direct.distributed.DistributedObject import DistributedObject
from pirates.piratesgui.StatRowHeadingGui import StatRowHeadingGui
from pirates.piratesgui.StatRowGui import StatRowGui
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PLocalizer
from pirates.pvp import PVPGlobals

class Scoreboard(DistributedObject):

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self._scores = {}
        self._names = {}
        self._teams = {}
        self._types = {}
        self._stats = {}

    def delete(self):
        self.ignore('`')
        self.ignore('`-up')
        localAvatar.guiMgr.removeSiegeStatus()
        self._scores = None
        del self._scores
        self._names = None
        del self._names
        self._teams = None
        del self._teams
        self._types = None
        del self._types
        self._stats = None
        del self._stats
        DistributedObject.delete(self)
        return

    def generate(self):
        DistributedObject.generate(self)
        localAvatar.guiMgr.createSiegeStatus(self)
        self.accept('`', localAvatar.guiMgr.showSiegeStatus)
        self.accept('`-up', localAvatar.guiMgr.hideSiegeStatus)

    def addScore(self, id, name, score, team, type, stats):
        self._scores[id] = score
        self._names[id] = name
        self._teams[id] = team
        self._types[id] = type
        for stat, value in stats:
            self._stats[stat][id] = value

    def setScore(self, id, score):
        self._scores[id] = score
        messenger.send(self.taskName('scoreChanged'))

    def getScore(self, id):
        return self._scores[id]

    def setStat(self, id, stat, value):
        self._stats[stat][id] = value
        messenger.send(self.taskName('scoreChanged'))

    def getStat(self, id, stat):
        return self._stats[stat][id]

    def resetScores(self):
        self._scores = {}
        self._names = {}
        self._teams = {}
        self._types = {}
        for stat, dict in self._stats.iteritems():
            dict = {}

    def setScores(self, scores):
        self.resetScores()
        for id, name, score, team, type, stats in scores:
            self.addScore(id, name, score, team, type, stats)

        messenger.send(self.taskName('scoreChanged'))

    def setStats(self, stats):
        for stat in stats:
            self._stats[stat] = {}

    def sortTeamScores(self, item1, item2):
        return item2.get('Score') - item1.get('Score')

    def getTeamScores(self, team):
        scores = []
        for id, score in self._scores.iteritems():
            if self._teams[id] == team and self._types[id] == PVPGlobals.SHIP_SCORE:
                scores.append({'ID': id,'Score': score})

        scores.sort(self.sortTeamScores)
        return scores

    def getTeamName(self, team):
        return PVPGlobals.siegeTeamNames[team]

    def getColumnLabels(self):
        columns = [
         PLocalizer.PVPShip, PLocalizer.PVPScore]
        for stat in self._stats.keys():
            columns.append(PVPGlobals.statText[stat])

        return columns

    def createNewItem(self, item, parent, itemType=None, columnWidths=[], color=None):
        if itemType == PiratesGuiGlobals.UIListItemType_ColumHeadings:
            newItem = StatRowHeadingGui(item, self.getColumnLabels(), parent, textScale=0.06, itemHeight=PiratesGuiGlobals.TMCompletePageHeight / 16, itemWidth=columnWidths[0] + columnWidths[1] * 2 - PiratesGuiGlobals.BorderWidth[0] * 2, itemWidths=columnWidths, frameColor=(0.0,
                                                                                                                                                                                                                                                                                   0.0,
                                                                                                                                                                                                                                                                                   0.0,
                                                                                                                                                                                                                                                                                   0.0))
        else:
            newItem = StatRowGui(item, self.getColumnLabels(), parent, itemHeight=PiratesGuiGlobals.TMCompletePageHeight / 16, itemWidth=columnWidths[0] + columnWidths[1] * 2 - PiratesGuiGlobals.BorderWidth[0] * 2, itemWidths=columnWidths, txtColor=color, frameColor=(0.0,
                                                                                                                                                                                                                                                                            0.0,
                                                                                                                                                                                                                                                                            0.0,
                                                                                                                                                                                                                                                                            0.0))
        newItem.setup()
        return newItem

    def getItemChangeMsg(self):
        return self.taskName('scoreChanged')

    def getItemList(self, team):
        sortedScores = self.getTeamScores(team)
        displayScores = []
        for scoreItemDict in sortedScores:
            id = scoreItemDict.get('ID')
            score = scoreItemDict.get('Score')
            stats = [['Score', str(score)]]
            for stat, dict in self._stats.iteritems():
                stats.append([PVPGlobals.statText[stat], str(dict.get(id))])

            if localAvatar.getShip() and localAvatar.getShip().doId == id:
                displayScores.append([self._names[id], stats, ['color', (1, 1, 1, 1)]])
            else:
                displayScores.append([self._names[id], stats, ['color', PVPGlobals.getSiegeColor(self._teams[id])]])

        displayScores.insert(0, self.getColumnLabels())
        return displayScores

    def getRowTextColor(self, rowHeading):
        return self.game.rowColors.get(rowHeading)