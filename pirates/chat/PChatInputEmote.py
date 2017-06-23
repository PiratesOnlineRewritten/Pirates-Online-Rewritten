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
scStructure = []

class PChatInputEmote(DirectObject.DirectObject):
    DefaultSCColorScheme = SCColorScheme(arrowColor=(1, 1, 1), rolloverColor=(1, 1,
                                                                              1))

    def __init__(self):
        self.whisperId = None
        self.toPlayer = 0
        structure = []
        structure.append([SCEmoteMenu, OTPLocalizer.SCMenuEmotions])
        self.emoteMenuIdx = len(structure) - 1
        structure.append([SCCustomMenu, OTPLocalizer.SCMenuCustom])
        structure += scStructure
        if base.config.GetInt('want-emotes', 1):
            emote_structure = None
            emote_dance_structure = None
            emote_general_structure = None
            emote_music_structure = None
            emote_expressions_structure = None
            avatar_gender = base.emoteGender
            idList = EmoteGlobals.emotes.keys()
            idList.sort()
            for id in idList:
                emote = EmoteGlobals.emotes.get(id)
                emote_group = EmoteGlobals.getEmoteGroup(id)
                emote_gender = EmoteGlobals.getEmoteGender(id)
                if id in [EmoteGlobals.EMOTE_VALENTINES, EmoteGlobals.EMOTE_NOISEMAKER, EmoteGlobals.EMOTE_HALLOWEEN, EmoteGlobals.EMOTE_COIN_TAILS]:
                    continue
                if not emote_structure:
                    emote_structure = [
                     OTPLocalizer.Emotes_Root]
                if not emote_dance_structure:
                    emote_dance_structure = [
                     OTPLocalizer.Emotes_Dances]
                    structure.append(emote_dance_structure)
                if not emote_general_structure:
                    emote_general_structure = [
                     OTPLocalizer.Emotes_General]
                    structure.append(emote_general_structure)
                if not emote_music_structure:
                    emote_music_structure = [
                     OTPLocalizer.Emotes_Music]
                    structure.append(emote_music_structure)
                if not emote_expressions_structure:
                    emote_expressions_structure = [
                     OTPLocalizer.Emotes_Expressions]
                    structure.append(emote_expressions_structure)
                if emote_gender == avatar_gender or emote_gender is None:
                    if emote_group == OTPLocalizer.Emotes_Dances:
                        emote_dance_structure.append(id)
                    elif emote_group == OTPLocalizer.Emotes_General:
                        structure.append(id)
                    elif emote_group == OTPLocalizer.Emotes_Music:
                        emote_music_structure.append(id)
                    elif emote_group == OTPLocalizer.Emotes_Expressions:
                        emote_expressions_structure.append(id)

            if emote_structure:
                structure.insert(0, emote_structure)
        self.createSpeedChatObject(structure)

        def listenForSCEvent(eventBaseName, handler, self=self):
            eventName = self.speedChat.getEventName(eventBaseName)
            self.accept(eventName, handler)

        listenForSCEvent(SpeedChatGlobals.SCTerminalLinkedEmoteEvent, self.handleLinkedEmote)
        self.fsm = ClassicFSM.ClassicFSM('SpeedChat', [
         State.State('off', self.enterOff, self.exitOff, [
          'active']),
         State.State('active', self.enterActive, self.exitActive, [
          'off'])], 'off', 'off')
        self.fsm.enterInitialState()
        self.mode = 'AllChat'
        self.whisperId = None
        return

    def updateEmoteList(self):
        idList = EmoteGlobals.emotes.keys()
        idList.sort()
        for emoteId in idList:
            if EmoteGlobals.getEmotePrereqs(emoteId):
                for prereq in EmoteGlobals.getEmotePrereqs(emoteId):
                    if not prereq.avIsReady(localAvatar) and emoteId in self.structure:
                        self.removeEmote(emoteId)
                    elif prereq.avIsReady(localAvatar) and emoteId not in self.structure:
                        self.addEmote(emoteId)

        self.createSpeedChatObject(self.structure)

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
        bounds = self.speedChat.getTightBounds()
        zSize = bounds[1][2] - bounds[0][2]
        self.speedChat.setPos(Point3(0.025, 0, zSize + 0.07))
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

    def sendChatByMode(self, msgType, textId, questInt=0, taskNum=0, questFlag=0):
        messenger.send('sentSpeedChat')
        if msgType == SPEEDCHAT_EMOTE:
            base.talkAssistant.sendOpenSpeedChat(msgType, textId)
            return
        if msgType == GMCHAT:
            gmHandler = SpeedChatGMHandler.SpeedChatGMHandler()
            base.talkAssistant.sendOpenTalk(gmHandler.getPhrase(textId))
            return
        if self.mode == 'PlayerWhisper':
            if questFlag:
                base.talkAssistant.sendPlayerWhisperQuestSpeedChat(questInt, msgType, taskNum, self.whisperId)
            else:
                base.talkAssistant.sendPlayerWhisperSpeedChat(msgType, textId, self.whisperId)
        elif self.mode == 'AvatarWhisper':
            if questFlag:
                pass
            else:
                base.talkAssistant.sendAvatarWhisperSpeedChat(msgType, textId, self.whisperId)
        elif self.mode == 'GuildChat':
            if questFlag:
                base.talkAssistant.sendGuildSCQuestChat(msgType, questInt, taskNum)
            else:
                base.talkAssistant.sendGuildSpeedChat(msgType, textId)
        elif self.mode == 'CrewChat':
            if questFlag:
                base.talkAssistant.sendPartySCQuestChat(msgType, questInt, taskNum)
            else:
                base.talkAssistant.sendPartySpeedChat(msgType, textId)
        elif self.mode == 'ShipPVP':
            if questFlag:
                base.talkAssistant.sendShipPVPCrewSCQuestChat(questInt, msgType, taskNum)
            else:
                base.talkAssistant.sendShipPVPCrewSpeedChat(msgType, textId)
        elif questFlag:
            base.talkAssistant.sendSCQuestChat(msgType, questInt, taskNum)
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
        self.sendChatByMode(3, textId)
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
                self.sendChatByMode(1, emoteId)
            else:
                self.sendChatByMode(2, emoteId)
        self.hide()

    def handleQuestMsg(self, questInt, toNpcId, msgType, taskNum):
        self.sendChatByMode(msgType, '', questInt, taskNum, 1)
        self.hide()

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
        gmHandler = SpeedChatGMHandler.SpeedChatGMHandler()
        self.structure.insert(0, gmHandler.getStructure())
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

    def addEmote(self, emoteId):
        emote = EmoteGlobals.emotes.get(emoteId)
        emote_group = EmoteGlobals.getEmoteGroup(emoteId)
        if emote is None:
            return
        if emoteId not in self.structure:
            self.structure.append(emoteId)
        self.createSpeedChatObject(self.structure)
        return

    def removeEmote(self, emoteId):
        emote = EmoteGlobals.emotes.get(emoteId)
        emote_group = EmoteGlobals.getEmoteGroup(emoteId)
        if emote is None:
            return
        if emoteId in self.structure:
            self.structure.remove(emoteId)
        self.createSpeedChatObject(self.structure)
        return