from direct.distributed.DistributedObject import DistributedObject
from pirates.pvp.SiegeManagerBase import SiegeManagerBase
from otp.speedchat import SCDecoders
from pirates.speedchat import PSCDecoders
from pirates.piratesbase import PLocalizer
from direct.fsm.StatePush import FunctionCall

class SiegeManager(DistributedObject, SiegeManagerBase):
    TeamJoinableChangedEvent = 'PVPTeamJoinableChanged'

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        SiegeManagerBase.__init__(self)

    def generate(self):
        self._announcerInterest = None
        self._siegeTeam = 0
        self._siegeTeamUpdater = FunctionCall(self._setSiegeTeam, localAvatar._siegeTeamSV)
        self._siegeTeamUpdater.pushCurrentState()
        DistributedObject.generate(self)
        self._pvpTeamJoinable = {}
        base.cr.distributedDistrict.siegeManager = self
        return

    def delete(self):
        self._siegeTeamUpdater.destroy()
        del self._siegeTeamUpdater
        self._removeAnnouncerInterest()
        del self._pvpTeamJoinable
        del base.cr.distributedDistrict.siegeManager
        DistributedObject.delete(self)

    def setPvpEnabled(self, enabled):
        self._pvpEnabled = enabled

    def getPvpEnabled(self):
        return self._pvpEnabled

    def setTeamsJoinable(self, teamJoinableItems):
        for teamId, joinable in teamJoinableItems:
            self._pvpTeamJoinable[teamId] = joinable

        messenger.send(SiegeManager.TeamJoinableChangedEvent)

    def teamIsJoinable(self, teamId):
        if not config.GetBool('want-pvp-team-balance', 1):
            return True
        return self._pvpTeamJoinable.get(teamId, True)

    def sendTalk(self, message):
        print 'Seige Manager Sending Message %s' % message
        self.sendUpdate('setTalkGroup', [0, 0, '', message, [], 0])

    def sendWLChat(self, message):
        self.sendUpdate('sendWLChat', [message, 0, 0])

    def sendSC(self, msgIndex):
        self.sendUpdate('sendSC', [msgIndex])

    def setTalkGroup(self, fromAv, fromAC, avatarName, chat, mods, flags):
        print 'Seige Manager- SetTalkGroup %s' % chat
        teamName = self.getPVPChatTeamName(localAvatar.getSiegeTeam())
        message, scrubbed = localAvatar.scrubTalk(chat, mods)
        base.talkAssistant.receiveShipPVPMessage(fromAv, fromAC, avatarName, teamName, message, scrubbed)

    def recvChat(self, avatarId, message, chatFlags, DISLid, name):
        teamName = self.getPVPChatTeamName(localAvatar.getSiegeTeam())
        if not self.cr.avatarFriendsManager.checkIgnored(avatarId):
            displayMess = '%s %s %s' % (name, self.getPVPChatTeamName(localAvatar.getSiegeTeam()), message)
            base.talkAssistant.receiveShipPVPMessage(avatarId, DISLid, name, teamName, message)

    def recvWLChat(self, avatarId, message, chatFlags, DISLid, name):
        teamName = self.getPVPChatTeamName(localAvatar.getSiegeTeam())
        if not self.cr.avatarFriendsManager.checkIgnored(avatarId):
            displayMess = '%s %s %s' % (name, self.getPVPChatTeamName(localAvatar.getSiegeTeam()), message)
            base.talkAssistant.receiveShipPVPMessage(avatarId, DISLid, name, teamName, message)

    def recvSpeedChat(self, avatarId, msgIndex, name):
        print 'siege manager recvSpeedChat'
        if not self.cr.avatarFriendsManager.checkIgnored(avatarId):
            displayMess = '%s %s %s' % (name, self.getPVPChatTeamName(localAvatar.getSiegeTeam()), SCDecoders.decodeSCStaticTextMsg(msgIndex))
            message = SCDecoders.decodeSCStaticTextMsg(msgIndex)
            teamName = self.getPVPChatTeamName(localAvatar.getSiegeTeam())
            base.talkAssistant.receiveShipPVPMessage(avatarId, 0, name, teamName, message)

    def sendSCQuest(self, questInt, msgType, taskNum):
        self.sendUpdate('sendSCQuest', [questInt, msgType, taskNum])

    def recvSCQuest(self, avName, senderId, questInt, msgType, taskNum):
        senderName = avName
        message = base.talkAssistant.SCDecoder.decodeSCQuestMsgInt(questInt, msgType, taskNum)
        if not self.cr.avatarFriendsManager.checkIgnored(senderId):
            teamName = self.getPVPChatTeamName(localAvatar.getSiegeTeam())
            displayMess = '%s %s %s' % (avName, teamName, message)
            base.talkAssistant.receiveShipPVPMessage(senderId, 0, avName, teamName, message)

    def getPVPChatTeamName(self, teamId):
        if teamId == 2:
            return PLocalizer.PVPSpanish
        elif teamId == 1:
            return PLocalizer.PVPFrench
        else:
            return PLocalizer.PVPPrefix

    def _addAnnouncerInterest(self):
        if not self._announcerInterest:
            self._announcerInterest = self.cr.addTaggedInterest(self.doId, self.ANNOUNCER_ZONE, self.cr.ITAG_GAME, 'siegeAnnouncer')

    def _removeAnnouncerInterest(self):
        if self._announcerInterest:
            self.cr.removeTaggedInterest(self._announcerInterest)
            self._announcerInterest = None
        return

    def _setSiegeTeam(self, siegeTeam):
        if siegeTeam and not self._siegeTeam:
            self._addAnnouncerInterest()
        elif not siegeTeam and self._siegeTeam:
            self._removeAnnouncerInterest()
        self._siegeTeam = siegeTeam