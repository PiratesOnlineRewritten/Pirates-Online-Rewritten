import string
import sys
from direct.showbase import DirectObject
from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PLocalizer
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from otp.speedchat import SCDecoders
from pandac.PandaModules import *
from otp.chat.ChatGlobals import *
from otp.chat.TalkGlobals import *
from otp.speedchat import SpeedChatGlobals
from otp.chat.TalkMessage import TalkMessage
from otp.chat.TalkAssistant import TalkAssistant
from pirates.ai import NewsManager
import time
from pirates.speedchat import PSCDecoders
from pirates.chat.PTalkHandle import PTalkHandle
from pirates.chat.PiratesTalkGlobals import CANNON_DEFENSE
import random
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals

class PTalkAssistant(TalkAssistant):
    notify = DirectNotifyGlobal.directNotify.newCategory('PTalkAssistant')

    def __init__(self):
        TalkAssistant.__init__(self)
        self.SCDecoder = PSCDecoders

    def clearHistory(self):
        TalkAssistant.clearHistory(self)
        self.historyParty = []
        self.historyPVP = []
        self.labelParty = OTPLocalizer.TalkParty
        self.labelPVP = OTPLocalizer.TalkPVP

    def checkShipPVPTypedChat(self):
        if not hasattr(localAvatar.ship, 'getSiegeTeam'):
            return False
        if localAvatar.ship.getSiegeTeam():
            return True
        return False

    def checkShipPVPSpeedChat(self):
        if not hasattr(localAvatar.ship, 'getSiegeTeam'):
            return False
        if localAvatar.ship.getSiegeTeam():
            return True
        return False

    def checkPartyTypedChat(self):
        if localAvatar.bandMember:
            return True
        return False

    def checkPartySpeedChat(self):
        if localAvatar.bandMember:
            return True
        return False

    def doWhiteListWarning(self):
        self.receiveGameMessage(PLocalizer.WhiteListWarning)

    def fillWithTestText(self):
        hold = self.floodThreshold
        self.floodThreshold = 1000.0
        self.receiveOpenTalk(1001, 'Bob the Ghost', None, None, 'Hello from the machine')
        self.receiveShipPVPMessage(1001, None, 'Bob the Ghost', 'Your team', "Just remember I'm on your side!")
        self.receiveOpenTalk(1001, 'Bob the Ghost', None, None, 'Hope this makes life easier')
        self.receiveOpenTalk(1002, 'Doug the Spirit', None, None, 'Now we need some longer text that will spill over onto two lines')
        self.receiveOpenTalk(1002, 'Doug the Spirit', None, None, 'Maybe I will tell you')
        self.receiveOpenTalk(1001, 'Bob the Ghost', None, None, 'If you are seeing this text it is because you are cool, yes I am')
        self.receiveOpenTalk(1002, 'Doug the Spirit', None, None, "That's right, there is no need to call tech support")
        self.receiveOpenTalk(localAvatar.doId, localAvatar.getName(), None, None, "Okay I won't call tech support, because I am cool, how about that!")
        self.receiveFriendAccountUpdate(2001, "Doug's Player", 1)
        self.receiveFriendUpdate(1002, 'Doug the Spirit', 1)
        self.receiveGuildUpdate(1001, 'Bob the Ghost', 1)
        self.receiveGuildTalk(1001, None, 'Bob the Ghost', 'Did you know I am in your guild?')
        self.receivePartyTalk(1001, None, 'Bob the Ghost', 'Did you know I am in your crew?')
        self.receivePartyTalk(1001, None, 'Bob the Ghost', 'But it is a lot easier than typing it in every time')
        self.receiveGameMessage('Here is a game message for good measure')
        self.receiveSystemMessage('and this is a system message')
        self.receiveOpenTalk(localAvatar.doId, localAvatar.getName(), None, None, 'All this text sure helps me test things, like chat boxes and such!')
        self.receiveGuildTalk(1001, None, 'Bob the Ghost', 'Yes that was the idea')
        self.receiveGuildTalk(1001, None, 'Bob the Ghost', 'I hope you like it!')
        self.receiveGameMessage('Blue Warrior shot the food!')
        self.receiveGameMessage('Red Wizard is about to die!')
        self.receivePartyTalk(1001, None, 'Bob the Ghost', 'It sure took a while to add all this made up text')
        self.receiveWhisperTalk(1001, 'Bob the Ghost', None, None, localAvatar.doId, localAvatar.getName(), 'Would you like to order some pizza?')
        self.receiveOpenTalk(1001, 'Bob the Ghost', None, None, 'More text for ya!')
        self.floodThreshold = hold
        self.receiveGMTalk(1003, 'G Money', None, None, 'Good because I have seen it already')
        return

    def executeGMCommand(self, text):
        words = text[1:].split(' ')
        comm = words[0].lower()
        argStr = ' '.join(words[1:])
        valid = True
        if comm in ('boo', ):
            if not hasattr(self, 'booToggle'):
                self.booToggle = 0
            if self.booToggle:
                self.booToggle = 0
            else:
                self.booToggle = 7
            typeIndex = 1
            if len(words) > 1 and words[1]:
                typeIndex = int(words[1])
                typeIndex = bound(typeIndex, 0, 7)
            localAvatar.sendUpdate('requestGhostGM', [self.booToggle])
            localAvatar.sendUpdate('requestGhostColor', [typeIndex])
        elif comm in ('fubar', ):
            pass

    def executeSlashCommand(self, text):
        words = text[1:].split(' ')
        comm = words[0].lower()
        argStr = ' '.join(words[1:])
        valid = True
        if comm in ('afk', 'away'):
            localAvatar.toggleAFK()
        else:
            if comm in PLocalizer.EmoteCommands.keys():
                emoteCode = PLocalizer.EmoteCommands[comm]
                if type(emoteCode) == type((0, )):
                    emoteCode = random.choice(emoteCode)
                messenger.send(SpeedChatGlobals.SCEmoteMsgEvent, [emoteCode])
            elif comm == 'quit':
                if not base.config.GetBool('location-kiosk', 0):
                    import sys
                    sys.exit(0)
            elif comm in ('lfc', 'lfg', 'lookingforcrew'):
                localAvatar.toggleLookingForCrewSign()
            elif comm in ('code', 'redeemcode'):
                if localAvatar.getTutorialState() < PiratesGlobals.TUT_MET_JOLLY_ROGER:
                    localAvatar.guiMgr.createWarning(PLocalizer.CannotRedeemYet, PiratesGuiGlobals.TextFG6, duration=8.0)
                else:
                    localAvatar.submitCodeToServer(argStr)
                    base.talkAssistant.receiveGameMessage(PLocalizer.CodeSubmitting % argStr)
            elif comm in ('holiday', 'holidays', 'holidaylist', 'event'):
                base.cr.newsManager.displayHolidayStatus()
            elif comm in ('x2', 'x2bonus'):
                timeRemain = localAvatar.getTempDoubleXPReward()
                if timeRemain:
                    timeRemain = int(timeRemain)
                    minutes, seconds = divmod(timeRemain, 60)
                    hours, minutes = divmod(minutes, 60)
                    base.talkAssistant.receiveGameMessage(PLocalizer.TEMP_DOUBLE_REP_CHAT % (hours, minutes))
                else:
                    base.talkAssistant.receiveGameMessage(PLocalizer.NO_TEMP_DOUBLE_REP)
            elif comm == 'crewhud':
                localAvatar.guiMgr.crewHUD.toggleHUD()
            elif comm == 'time':
                messenger.send('requestServerTime')
            else:
                valid = False
            if valid:
                base.cr.centralLogger.writeClientEvent(('slash command - %s(%s)' % (comm, argStr))[:255])

    def addHandle(self, doId, message):
        if doId == localAvatar.doId:
            return
        handle = self.handleDict.get(doId)
        if not handle:
            handle = PTalkHandle(doId, message)
            self.handleDict[doId] = handle
        else:
            handle.addMessageInfo(message)

    def receiveOpenTalk(self, avatarId, avatarName, accountId, accountName, message, scrubbed=0):
        if hasattr(base, 'localAvatar') and base.localAvatar.getDoId() == avatarId:
            for playerId in base.localAvatar.playersNearby.keys():
                chatFlags = base.localAvatar.playersNearby[playerId]
                if chatFlags[0] or chatFlags[1]:
                    if scrubbed:
                        player = base.cr.doId2do.get(playerId)
                        if player:
                            player.requestConfusedText(True)
                    elif not chatFlags[1]:
                        player = base.cr.doId2do.get(playerId)
                        if player:
                            player.requestConfusedText(False)

        TalkAssistant.receiveOpenTalk(self, avatarId, avatarName, accountId, accountName, message, scrubbed)

    def receivePartyTalk(self, senderAvId, fromAC, avatarName, message, scrubbed=0):
        error = None
        if not self.isThought(message):
            accountName = self.findName(fromAC, 1)
            newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, senderAvId, avatarName, fromAC, accountName, None, None, None, None, TALK_PARTY, None)
            reject = self.addToHistoryDoId(newMessage, senderAvId)
            if reject == 1:
                newMessage.setBody(OTPLocalizer.AntiSpamInChat)
            if reject != 2:
                isSpam = self.spamDictByDoId.get(senderAvId) and reject
                if not isSpam:
                    self.historyComplete.append(newMessage)
                    self.historyParty.append(newMessage)
                    messenger.send('NewOpenMessage', [newMessage])
                if newMessage.getBody() == OTPLocalizer.AntiSpamInChat:
                    self.spamDictByDoId[senderAvId] = 1
                else:
                    self.spamDictByDoId[senderAvId] = 0
        return error

    def receiveOpenSpeedChat(self, msgType, messageIndex, senderAvId, name=None):
        error = None
        if not name and senderAvId:
            name = self.findName(senderAvId, 0)
        messageType = TALK_OPEN
        message = None
        if msgType == SPEEDCHAT_NORMAL:
            message = self.SCDecoder.decodeSCStaticTextMsg(messageIndex)
        else:
            if msgType == SPEEDCHAT_EMOTE:
                message = self.SCDecoder.decodeSCEmoteWhisperMsg(messageIndex, name)
                if not message:
                    if senderAvId == localAvatar.doId:
                        message = PLocalizer.EmoteMessagesSelf.get(messageIndex)
                        messageType = INFO_OPEN
                    else:
                        message = PLocalizer.EmoteMessagesThirdPerson.get(messageIndex)
                        messageType = INFO_OPEN
            elif msgType == SPEEDCHAT_CUSTOM:
                message = self.SCDecoder.decodeSCCustomMsg(messageIndex)
            if message in (None, ''):
                return
            newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, senderAvId, name, None, None, None, None, None, None, messageType, None)
            reject = self.addToHistoryDoId(newMessage, senderAvId)
            if reject == 1:
                newMessage.setBody(OTPLocalizer.AntiSpamInChat)
            if reject != 2:
                isSpam = self.spamDictByDoId.get(senderAvId) and reject
                if not isSpam:
                    self.historyComplete.append(newMessage)
                    self.historyOpen.append(newMessage)
                    messenger.send('NewOpenMessage', [newMessage])
                if newMessage.getBody() == OTPLocalizer.AntiSpamInChat:
                    self.spamDictByDoId[senderAvId] = 1
                else:
                    self.spamDictByDoId[senderAvId] = 0
        return error

    def receiveSystemMessage(self, message):
        base.localAvatar.guiMgr.messageStack.addTextMessage(message, seconds=20, priority=0, color=(0.5,
                                                                                                    0,
                                                                                                    0,
                                                                                                    1), icon=('admin',
                                                                                                              ''))
        TalkAssistant.receiveSystemMessage(self, message)

    def receivePartyMessage(self, message, senderAvId, senderName):
        error = None
        if not self.isThought(message):
            newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, senderAvId, senderName, None, None, None, None, None, None, TALK_PARTY, None)
            reject = self.addToHistoryDoId(newMessage, senderAvId)
            if reject == 1:
                newMessage.setBody(OTPLocalizer.AntiSpamInChat)
            if reject != 2:
                isSpam = self.spamDictByDoId.get(senderAvId) and reject
                if not isSpam:
                    self.historyComplete.append(newMessage)
                    self.historyParty.append(newMessage)
                    messenger.send('NewOpenMessage', [newMessage])
                if newMessage.getBody() == OTPLocalizer.AntiSpamInChat:
                    self.spamDictByDoId[senderAvId] = 1
                else:
                    self.spamDictByDoId[senderAvId] = 0
        return error

    def receiveShipPVPMessage(self, senderAvId, fromAC, avatarName, teamName, message, scrubbed=0):
        error = None
        if not self.isThought(message):
            accountName = self.findName(fromAC, 1)
            newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, senderAvId, avatarName, fromAC, None, None, None, None, None, TALK_PVP, teamName)
            reject = 0
            if senderAvId:
                reject = self.addToHistoryDoId(newMessage, senderAvId, scrubbed)
            if reject == 1:
                newMessage.setBody(OTPLocalizer.AntiSpamInChat)
            if reject != 2:
                isSpam = self.spamDictByDoId.get(senderAvId) and reject
                if not isSpam:
                    self.historyComplete.append(newMessage)
                    self.historyPVP.append(newMessage)
                    messenger.send('NewOpenMessage', [newMessage])
                if newMessage.getBody() == OTPLocalizer.AntiSpamInChat:
                    self.spamDictByDoId[senderAvId] = 1
                else:
                    self.spamDictByDoId[senderAvId] = 0
        return error

    def receivePartyUpdate(self, memberId, memberName, isOnline):
        if isOnline:
            onlineMessage = OTPLocalizer.FriendOnline % memberName
        else:
            onlineMessage = OTPLocalizer.FriendOffline % memberName
        newMessage = TalkMessage(self.countMessage(), self.stampTime(), onlineMessage, memberId, memberName, None, None, None, None, None, None, UPDATE_PARTY, None)
        self.historyComplete.append(newMessage)
        self.historyUpdates.append(newMessage)
        self.historyParty.append(newMessage)
        messenger.send('NewOpenMessage', [newMessage])
        return

    def sendPartyTalk(self, message):
        error = None
        if self.checkPartyTypedChat():
            localAvatar.bandMember.sendTalk(0, 0, '', message, 0, 0)
        else:
            print 'Party chat error'
            error = ERROR_NO_CREW_CHAT
        return error

    def sendShipPVPCrewTalk(self, message):
        error = None
        if self.checkShipPVPTypedChat():
            base.cr.distributedDistrict.siegeManager.sendTalk(message)
        else:
            print 'Ship PVP chat error: Crew typed Chat'
            error = ERROR_NO_SHIPPVP_CHAT
        return error

    def sendSCQuestChat(self, msgType, questInt, taskNum):
        error = None
        messenger.send(SCQuestEvent)
        messenger.send('chatUpdateSCQuest', [questInt, msgType, taskNum])
        return

    def sendPartySpeedChat(self, type, msgIndex):
        error = None
        if self.checkPartySpeedChat():
            localAvatar.bandMember.b_setSpeedChat(msgIndex)
        else:
            print 'Party chat error'
            error = ERROR_NO_CREW_CHAT
        return error

    def sendPartySCQuestChat(self, msgType, questInt, taskNum):
        error = None
        if self.checkPartySpeedChat():
            localAvatar.bandMember.b_setSCQuestChat(questInt, msgType, taskNum)
        else:
            print 'Quest Party chat error'
            error = ERROR_NO_CREW_CHAT
        msgIndex = taskNum
        return error

    def sendGuildSCQuestChat(self, msgType, questInt, taskNum):
        error = None
        if self.checkGuildSpeedChat():
            base.cr.guildManager.sendSCQuest(questInt, msgType, taskNum)
        else:
            print 'Quest Guild chat error'
            error = ERROR_NO_GUILD_CHAT
        return error

    def sendShipPVPCrewSpeedChat(self, type, msgIndex):
        error = None
        if self.checkShipPVPSpeedChat():
            base.cr.distributedDistrict.siegeManager.sendSC(msgIndex)
        else:
            print 'Ship PVP chat error: Crew Speed Chat'
            error = ERROR_NO_SHIPPVP_CHAT
        return error

    def sendShipPVPCrewSCQuestChat(self, msgType, questInt, taskNum):
        error = None
        if self.checkShipPVPSpeedChat():
            base.cr.distributedDistrict.siegeManager.sendSCQuest(msgType, questInt, taskNum)
        else:
            print 'Ship PVP chat error: SCQuest Chat'
            error = ERROR_NO_SHIPPVP_CHAT
        return error

    def sendAvatarWhisperQuestSpeedChat(self, questInt, msgType, taskNum, receiverId):
        error = None
        base.localAvatar.whisperSCQuestTo(questInt, msgType, taskNum, receiverId)
        message = PSCDecoders.decodeSCQuestMsgInt(questInt, msgType, taskNum)
        if self.logWhispers:
            receiverName = self.findName(receiverId, 0)
            newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, localAvatar.doId, localAvatar.getName(), localAvatar.DISLid, localAvatar.DISLname, receiverId, receiverName, None, None, TALK_WHISPER, None)
            self.historyComplete.append(newMessage)
            self.addToHistoryDoId(newMessage, localAvatar.doId)
            self.addToHistoryDISLId(newMessage, base.cr.accountDetailRecord.playerAccountId)
            messenger.send('NewOpenMessage', [newMessage])
        return error

    def sendPlayerWhisperQuestSpeedChat(self, questInt, msgType, taskNum, receiverId):
        error = None
        base.cr.speedchatRelay.sendQuestSpeedchat(receiverId, questInt, msgType, taskNum)
        message = PSCDecoders.decodeSCQuestMsgInt(questInt, msgType, taskNum)
        if self.logWhispers:
            receiverName = self.findName(receiverId, 1)
            newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, localAvatar.doId, localAvatar.getName(), localAvatar.DISLid, localAvatar.DISLname, None, None, receiverId, receiverName, TALK_ACCOUNT, None)
            self.historyComplete.append(newMessage)
            self.addToHistoryDoId(newMessage, localAvatar.doId)
            self.addToHistoryDISLId(newMessage, base.cr.accountDetailRecord.playerAccountId)
            messenger.send('NewOpenMessage', [newMessage])
        return error

    def receiveCannonDefenseMessage(self, message, senderName):
        error = None
        if not self.isThought(message):
            newMessage = TalkMessage(self.countMessage(), self.stampTime(), message, None, senderName, None, None, localAvatar.doId, localAvatar.getName(), localAvatar.DISLid, localAvatar.DISLname, CANNON_DEFENSE, None)
            self.historyComplete.append(newMessage)
            self.historyUpdates.append(newMessage)
            messenger.send('NewOpenMessage', [newMessage])
        return error