from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.speedchat.SpeedChatTypes import *
from pirates.speedchat.PSpeedChatTypes import *
from otp.speedchat.SpeedChat import SpeedChat
from otp.speedchat import SpeedChatGlobals
from pirates.speedchat import PSpeedChatGlobals
from direct.showbase import DirectObject
from direct.fsm import ClassicFSM
from direct.fsm import State
import string
import random
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from otp.chat.ChatGlobals import *
from pirates.ai import HolidayGlobals
from otp.otpbase import OTPLocalizer
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import EmoteGlobals
from pirates.speedchat.PSpeedChatQuestMenu import PSpeedChatQuestMenu
from otp.speedchat import SpeedChatGMHandler
scStructure = [
 [
  OTPLocalizer.PSCMenuExpressions, [OTPLocalizer.PSCMenuGreetings, 50700, 50701, 50702, 50703, 50704], [OTPLocalizer.PSCMenuGoodbyes, 50800, 50801, 50802], [OTPLocalizer.PSCMenuFriendly, 50900], [OTPLocalizer.PSCMenuHappy, 51000, 51001], [OTPLocalizer.PSCMenuSad, 51100], [OTPLocalizer.PSCMenuSorry, 51200, 51201, 51202, 51203, 51204], 50105, 50100, 50101, 50102, 50103, 50104, 50106, 50107, 50108, 50109, 50110, 50111, 50112, 50113], [OTPLocalizer.PSCMenuCombat, 51300, 51301, 51302, 51303, 51304, 51305, 51306, 51307, 51308], [OTPLocalizer.PSCMenuSeaCombat, 51400, 51401, 51402, 51403, 51404, 51405, 51406, 51407, 51408, 51409, 51410, 51411, 51412, 51413, 51414, 51415, 51416, 51417, 51418, 51419, 51420, 51421], [OTPLocalizer.PSCMenuPlaces, [OTPLocalizer.PSCMenuLetsSail, 51500, 51501, 51502, 51503, 51504, 51505, 51506, 51507, 51508, 51509, 51510, 51511, 51512], [OTPLocalizer.PSCMenuLetsHeadTo, [OTPLocalizer.PSCMenuHeadToPortRoyal, 51800, 51801], 51600, 51601, 51602], [OTPLocalizer.PSCMenuWhereIs, 52500], 50400, 50401], [OTPLocalizer.PSCMenuDirections, 51700, 51701, 51702, 51703, 51704, 51705, 51706, 51707], [OTPLocalizer.PSCMenuInsults, 50200, 50201, 50202, 50203, 50204, 50205, 50206, 50207, 50208, 50209, 50210, 50211], [OTPLocalizer.PSCMenuCompliments, 50300, 50301, 50302, 50303, 50304, 50305, 50306], [OTPLocalizer.PSCMenuCardGames, [OTPLocalizer.PSCMenuPoker, 51900, 51901, 51902, 51903, 51904], [OTPLocalizer.PSCMenuBlackjack, 52600, 52601], 52400, 52401, 52402], [OTPLocalizer.PSCMenuMinigames, [OTPLocalizer.PSCMenuFishing, 53101, 53102, 53103, 53104, 53105, 53106, 53107, 53110, 53111, 53112, 53113, 53114], [OTPLocalizer.PSCMenuCannonDefense, 53120, 53121, 53122, 53123, 53124, 53125, 53126, 53127, 53128, 53129], [OTPLocalizer.PSCMenuPotions, 53141, 53142, 53143, 53144, 53145, 53146], [OTPLocalizer.PSCMenuRepair, 53160, 53161, 53162, 53163, 53164, 53165, 53166, 53167, 53168]], [OTPLocalizer.PSCMenuInvitations, [OTPLocalizer.PSCMenuVersusPlayer, 52300, 52301, 52302, 52303, 52304], [OTPLocalizer.PSCMenuHunting, 52200, 52201], [OTPLocalizer.PSCMenuMinigames, 52350, 52351, 52352, 52353, 52354, 52355, 52356, 52357, 52358], 52100, 52101], [PSpeedChatQuestMenu, OTPLocalizer.PSCMenuQuests], 50005, 50001, 50002, 50003, 50004]

class PChatInputSpeedChat(DirectObject.DirectObject):
    DefaultSCColorScheme = SCColorScheme(arrowColor=(1, 1, 1), rolloverColor=(1, 1,
                                                                              1))

    def __init__(self):
        self.whisperId = None
        self.toPlayer = 0
        structure = []
        structure = scStructure
        self.createSpeedChatObject(structure)

        def listenForSCEvent(eventBaseName, handler, self=self):
            eventName = self.speedChat.getEventName(eventBaseName)
            self.accept(eventName, handler)

        listenForSCEvent(SpeedChatGlobals.SCStaticTextMsgEvent, self.handleStaticTextMsg)
        listenForSCEvent(SpeedChatGlobals.SCGMTextMsgEvent, self.handleGMTextMsg)
        listenForSCEvent(SpeedChatGlobals.SCCustomMsgEvent, self.handleCustomMsg)
        listenForSCEvent(SpeedChatGlobals.SCEmoteMsgEvent, self.handleEmoteMsg)
        listenForSCEvent(SpeedChatGlobals.SCEmoteNoAccessEvent, self.handleEmoteNoAccess)
        listenForSCEvent('SpeedChatStyleChange', self.handleSpeedChatStyleChange)
        listenForSCEvent(PSpeedChatGlobals.PSpeedChatQuestMsgEvent, self.handleQuestMsg)
        self.fsm = ClassicFSM.ClassicFSM('SpeedChat', [
         State.State('off', self.enterOff, self.exitOff, [
          'active']),
         State.State('active', self.enterActive, self.exitActive, [
          'off'])], 'off', 'off')
        self.fsm.enterInitialState()
        self.mode = 'AllChat'
        self.whisperId = None
        self.gmHandler = None
        return

    def reparentTo(self, newParent):
        self.baseFrame.reparentTo(newParent)

    def delete(self):
        self.ignoreAll()
        self.speedChat.destroy()
        del self.speedChat
        del self.fsm

    def setWhisperTo(self, whisperId, toPlayer=False):
        self.whisperId = whisperId
        self.toPlayer = toPlayer

    def show(self):
        self.speedChat.show()
        self.speedChat.setPos(Point3(0.11, 0, 0.92))
        self.fsm.request('active')

    def hide(self):
        self.fsm.request('off')

    def enterOff(self):
        self.speedChat.hide()

    def exitOff(self):
        pass

    def requestMode(self, mode, whisperId=None):
        if mode == 'AllChat' and not base.talkAssistant.checkOpenSpeedChat():
            messenger.send('Chat-Failed open typed chat test')
            return None
        elif mode == 'PlayerWhisper':
            if not base.talkAssistant.checkWhisperSpeedChatPlayer(whisperId):
                messenger.send('Chat-Failed player typed chat test')
                return None
        elif mode == 'AvatarWhisper':
            if not base.talkAssistant.checkWhisperSpeedChatAvatar(whisperId):
                messenger.send('Chat-Failed avatar typed chat test')
                return None
        self.mode = mode
        self.whisperId = whisperId
        return None

    def enterActive(self):

        def handleCancel():
            localAvatar.chatMgr.speedChatDone(success=False)

        self.acceptOnce('mouse1', handleCancel)

        def selectionMade(self=self):
            localAvatar.chatMgr.speedChatDone()

        self.terminalSelectedEvent = self.speedChat.getEventName(SpeedChatGlobals.SCTerminalSelectedEvent)
        self.accept(self.terminalSelectedEvent, selectionMade)
        self.speedChat.reparentTo(base.a2dBottomLeft, DGG.FOREGROUND_SORT_INDEX)
        pos = self.speedChat.getPos()
        self.speedChat.setWhisperMode(self.whisperId != None)
        self.speedChat.enter()
        return

    def exitActive(self):
        self.ignore('mouse1')
        self.ignore(self.terminalSelectedEvent)
        self.speedChat.exit()
        self.speedChat.detachNode()

    def handleLinkedEmote(self, emoteId):
        if self.whisperId is None:
            lt = base.localAvatar
            lt.b_setEmoteState(emoteId, animMultiplier=lt.animMultiplier)
        return

    def sendChatByMode(self, msgType, textId, questMsgType=0, questInt=0, taskNum=0, questFlag=0):
        messenger.send('sentSpeedChat')
        if msgType == SPEEDCHAT_EMOTE:
            base.talkAssistant.sendOpenSpeedChat(msgType, textId)
            return
        if msgType == GMCHAT:
            if self.gmHandler:
                base.talkAssistant.sendOpenTalk(self.gmHandler.getPhrase(textId))
            return
        if self.mode == 'PlayerWhisper':
            if questFlag:
                base.talkAssistant.sendPlayerWhisperQuestSpeedChat(questInt, questMsgType, taskNum, self.whisperId)
            else:
                base.talkAssistant.sendPlayerWhisperSpeedChat(msgType, textId, self.whisperId)
        elif self.mode == 'AvatarWhisper':
            if questFlag:
                base.talkAssistant.sendAvatarWhisperQuestSpeedChat(questInt, questMsgType, taskNum, self.whisperId)
            else:
                base.talkAssistant.sendAvatarWhisperSpeedChat(msgType, textId, self.whisperId)
        elif self.mode == 'GuildChat':
            if questFlag:
                base.talkAssistant.sendGuildSCQuestChat(questMsgType, questInt, taskNum)
            else:
                base.talkAssistant.sendGuildSpeedChat(msgType, textId)
        elif self.mode == 'CrewChat':
            if questFlag:
                base.talkAssistant.sendPartySCQuestChat(questMsgType, questInt, taskNum)
            else:
                base.talkAssistant.sendPartySpeedChat(msgType, textId)
        elif self.mode == 'ShipPVP':
            if questFlag:
                base.talkAssistant.sendShipPVPCrewSCQuestChat(questInt, questMsgType, taskNum)
            else:
                base.talkAssistant.sendShipPVPCrewSpeedChat(msgType, textId)
        elif questFlag:
            base.talkAssistant.sendSCQuestChat(questMsgType, questInt, taskNum)
        else:
            base.talkAssistant.sendOpenSpeedChat(msgType, textId)

    def handleStaticTextMsg(self, textId):
        if textId in PLocalizer.EmoteMessagesSelf:
            self.handleEmoteMsg(textId)
        elif textId == EmoteGlobals.EMOTE_VALENTINES:
            self.handleEmoteMsg(textId)
        else:
            self.sendChatByMode(SPEEDCHAT_NORMAL, textId)
            self.hide()

    def handleGMTextMsg(self, textId):
        self.sendChatByMode(GMCHAT, textId)
        self.hide()

    def handleCustomMsg(self, textId):
        self.sendChatByMode(SPEEDCHAT_CUSTOM, textId)
        self.hide()

    def handleEmoteMsg(self, emoteId):
        sendText = True
        for prereq in EmoteGlobals.getEmotePrereqs(emoteId):
            if not prereq.avIsReady(localAvatar):
                return

        if emoteId in OTPLocalizer.Emotes:
            sendText = localAvatar.requestEmote(emoteId)
        if sendText:
            if emoteId == EmoteGlobals.EMOTE_VALENTINES:
                emoteId = random.choice([EmoteGlobals.EMOTE_VALENTINES_A, EmoteGlobals.EMOTE_VALENTINES_B, EmoteGlobals.EMOTE_VALENTINES_D, EmoteGlobals.EMOTE_VALENTINES_E])
                self.sendChatByMode(SPEEDCHAT_NORMAL, emoteId)
            else:
                self.sendChatByMode(SPEEDCHAT_EMOTE, emoteId)
        self.hide()

    def handleEmoteNoAccess(self):
        if self.whisperId is None:
            self.emoteNoAccessPanel.setPos(0, 0, 0)
        else:
            self.emoteNoAccessPanel.setPos(0.37, 0, 0)
        self.emoteNoAccessPanel.reparentTo(aspect2d)
        return

    def handleEmoteNoAccessDone(self):
        self.emoteNoAccessPanel.detachNode()

    def handleQuestMsg(self, msgType, questInt, toNpcId, taskNum):
        self.sendChatByMode(None, None, questMsgType=msgType, questInt=questInt, taskNum=taskNum, questFlag=1)
        self.hide()
        return

    def handleSpeedChatStyleChange(self):
        nameKey, arrowColor, rolloverColor, frameColor = speedChatStyles[base.localAvatar.getSpeedChatStyleIndex()]
        newSCColorScheme = SCColorScheme(arrowColor=arrowColor, rolloverColor=rolloverColor, frameColor=frameColor)
        self.speedChat.setColorScheme(newSCColorScheme)

    def createSpeedChatObject(self, structure):
        if hasattr(self, 'speedChat'):
            self.speedChat.exit()
            self.speedChat.destroy()
            del self.speedChat
        self.speedChat = SpeedChat(structure=structure, backgroundModelName='models/gui/SpeedChatPanel', guiModelName='models/textureCards/speedchatIcons')
        self.speedChat.setScale(0.04)
        self.speedChat.setBin('gui-popup', 0)
        self.speedChat.setTopLevelOverlap(0.0)
        self.speedChat.setSubmenuOverlap(0.0)
        self.speedChat.setColorScheme(self.DefaultSCColorScheme)
        self.speedChat.finalizeAll()
        self.structure = structure

    def addGMSpeedChat(self):
        if not self.gmHandler:
            self.gmHandler = SpeedChatGMHandler.SpeedChatGMHandler()
            self.structure.insert(0, self.gmHandler.getStructure())
            self.speedChat.rebuildFromStructure(self.structure)

    def addFactoryMenu(self):
        fMenu = PSCFactoryMenu()
        fMenuHolder = SCMenuHolder(OTPLocalizer.SCMenuFactory, menu=fMenu)
        self.speedChat[2:2] = [fMenuHolder]

    def removeFactoryMenu(self):
        fMenu = self.speedChat[2]
        del self.speedChat[2]
        fMenu.destroy()

    def addCogMenu(self, indices):
        fMenu = PSCCogMenu(indices)
        fMenuHolder = SCMenuHolder(OTPLocalizer.SCMenuCog, menu=fMenu)
        self.speedChat[2:2] = [fMenuHolder]

    def removeCogMenu(self):
        fMenu = self.speedChat[2]
        del self.speedChat[2]
        fMenu.destroy()