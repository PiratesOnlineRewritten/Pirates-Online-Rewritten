from direct.distributed.DistributedObject import DistributedObject
from pirates.piratesbase import PLocalizer
from pirates.pvp import PVPGlobals

class SiegeAnnouncer(DistributedObject):

    def _otherTeam(self, team):
        if team == 1:
            return 2
        else:
            return 1

    def _makeTeamsDisplayable(self, team, assistTeam, sunkTeam):
        if not team:
            if assistTeam:
                team = assistTeam
            elif sunkTeam:
                team = self._otherTeam(sunkTeam)
        if not assistTeam and assistTeam is not None:
            if team:
                assistTeam = team
            elif sunkTeam:
                assistTeam = self._otherTeam(sunkTeam)
        if not sunkTeam and sunkTeam is not None:
            if team:
                sunkTeam = self._otherTeam(team)
            elif assistTeam:
                sunkTeam = self._otherTeam(assistTeam)
        if team == sunkTeam:
            team = self._otherTeam(sunkTeam)
        return (team, assistTeam, sunkTeam)

    def announceSink(self, team, shipName, sunkTeam, sunkShipName):
        team, assistTeam, sunkTeam = self._makeTeamsDisplayable(team, None, sunkTeam)
        stringDict = {'teamName': PVPGlobals.siegeTeamNames[team],'shipName': shipName,'sunkTeamName': PVPGlobals.siegeTeamNames[sunkTeam],'sunkShipName': sunkShipName}
        msg = PLocalizer.PVPSinkAnnouncement % stringDict
        base.talkAssistant.receiveGameMessage(msg)
        return

    def announceSinkWithAssist(self, team, shipName, assistTeam, assistShipName, sunkTeam, sunkShipName):
        team, assistTeam, sunkTeam = self._makeTeamsDisplayable(team, assistTeam, sunkTeam)
        stringDict = {'teamName': PVPGlobals.siegeTeamNames[team],'shipName': shipName,'assistTeamName': PVPGlobals.siegeTeamNames[assistTeam],'assistShipName': assistShipName,'sunkTeamName': PVPGlobals.siegeTeamNames[sunkTeam],'sunkShipName': sunkShipName}
        msg = PLocalizer.PVPSinkWithAssistAnnouncement % stringDict
        base.talkAssistant.receiveGameMessage(msg)

    def announceSinkStreak(self, team, shipName, amount):
        team, assistTeam, sunkTeam = self._makeTeamsDisplayable(team, None, None)
        stringDict = {'teamName': PVPGlobals.siegeTeamNames[team],'shipName': shipName,'amount': amount}
        msg = PLocalizer.PVPSinkStreakAnnouncement % stringDict
        base.talkAssistant.receiveGameMessage(msg)
        return