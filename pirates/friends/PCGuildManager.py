from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from otp.friends.GuildManager import GuildManager
from pirates.piratesgui import PiratesGuiGlobals
GUILDRANK_VETERAN = 4
GUILDRANK_GM = 3
GUILDRANK_OFFICER = 2
GUILDRANK_MEMBER = 1

class PCGuildManager(GuildManager):

    def sendSCQuest(self, questInt, msgType, taskNum):
        self.notify.debugCall()
        print 'GuildManager.sendSCQuest() called'
        self.sendUpdate('sendSCQuest', [questInt, msgType, taskNum])

    def recvSCQuest(self, senderId, questInt, msgType, taskNum):
        self.notify.debugCall()
        senderName = self.id2Name.get(senderId, None)
        message = decodeSCQuestMsgInt(questInt, msgType, taskNum)
        if senderName:
            displayMess = '%s %s %s' % (senderName, OTPLocalizer.GuildPrefix, message)
            base.talkAssistant.receiveGuildMessage(displayMess, senderId, senderName)
        else:
            self.pendingMsgs.append([senderId, message])
            self.memberList()
        return

    def recvMemberAdded(self, memberInfo, inviterId, inviterName):
        avatarId, avatarName, rank, isOnline, bandManagerId, bandId = memberInfo
        if avatarId != localAvatar.getDoId():
            if inviterId == localAvatar.getDoId():
                base.talkAssistant.receiveGuildUpdateMessage(OTPLocalizer.GuildInviterFriendInvitedP, inviterId, PLocalizer.You, avatarId, avatarName)
            elif inviterId:
                base.talkAssistant.receiveGuildUpdateMessage(OTPLocalizer.GuildInviterFriendInvited, inviterId, inviterName, avatarId, avatarName)
        GuildManager.recvMemberAdded(self, memberInfo, inviterId, inviterName)

    def recvMemberRemoved(self, avatarId, senderId, avatarName, senderName):
        if avatarId != localAvatar.getDoId():
            if senderId == localAvatar.getDoId():
                base.talkAssistant.receiveGuildUpdateMessage(OTPLocalizer.GuildInviterFriendKickedOutP, senderId, PLocalizer.You, avatarId, avatarName)
            elif senderId == avatarId:
                base.talkAssistant.receiveGuildUpdateMessage(OTPLocalizer.GuildInviterFriendsNoMore, senderId, senderName, 0, '')
            elif senderId:
                base.talkAssistant.receiveGuildUpdateMessage(OTPLocalizer.GuildInviterFriendKickedOut, senderId, senderName, avatarId, avatarName)
        messenger.send('kickedFromGuild-%s' % avatarId)
        GuildManager.recvMemberRemoved(self, avatarId, senderId, avatarName, senderName)

    def recvMemberUpdateRank(self, avatarId, senderId, avatarName, senderName, rank, promote):
        doShow = 1
        if avatarId == localAvatar.getDoId():
            avatarName = PLocalizer.LowerYou
        elif senderId == localAvatar.getDoId():
            senderName = PLocalizer.LowerYou
        if promote:
            if senderId == localAvatar.getDoId():
                senderName = PLocalizer.You
            if rank == GUILDRANK_GM:
                if senderId == localAvatar.getDoId():
                    message = OTPLocalizer.GuildInviterFriendPromotedGMP
                else:
                    message = OTPLocalizer.GuildInviterFriendPromotedGM
            elif senderId == localAvatar.getDoId():
                message = OTPLocalizer.GuildInviterFriendPromotedP
            else:
                message = OTPLocalizer.GuildInviterFriendPromoted
        else:
            if senderId == localAvatar.getDoId():
                senderName = PLocalizer.You
            if self.id2Rank.get(avatarId) == GUILDRANK_GM:
                doShow = 0
                if senderId == localAvatar.getDoId():
                    message = OTPLocalizer.GuildInviterFriendDemotedGMP
                else:
                    message = OTPLocalizer.GuildInviterFriendDemotedGM
            elif senderId == localAvatar.getDoId():
                message = OTPLocalizer.GuildInviterFriendDemotedP
            else:
                message = OTPLocalizer.GuildInviterFriendDemoted
            if doShow:
                base.talkAssistant.receiveGuildUpdateMessage(message, senderId, senderName, avatarId, avatarName, [PLocalizer.GuildRankNames[rank]])
        GuildManager.recvMemberUpdateRank(self, avatarId, senderId, avatarName, senderName, rank, promote)

    def notifyGuildKicksMaxed(self):
        localAvatar.guiMgr.createWarning(PLocalizer.GuildKicksMaxed, PiratesGuiGlobals.TextFG6)