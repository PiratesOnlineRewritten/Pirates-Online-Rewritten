from direct.fsm import FSM
from otp.otpbase import OTPGlobals
import sys
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from otp.otpbase import OTPLocalizer

class PChatInputTyped(FSM.FSM, DirectEntry):
    notify = DirectNotifyGlobal.directNotify.newCategory('PChatInputTyped')
    ExecNamespace = None

    def __init__(self, parent=None, **kw):
        FSM.FSM.__init__(self, 'PChatInputTyped')
        optiondefs = (('parent', parent, None), ('relief', DGG.SUNKEN, None), ('scale', 0.03, None), ('frameSize', (-0.2, 25.3, -0.5, 1.2), None), ('borderWidth', (0.1, 0.1), None), ('frameColor', (0.9, 0.9, 0.85, 0.8), None), ('entryFont', OTPGlobals.getInterfaceFont(), None), ('width', 25, None), ('numLines', 1, None), ('cursorKeys', 1, None), ('backgroundFocus', 0, None), ('suppressKeys', 1, None), ('suppressMouse', 1, None), ('command', self.sendChat, None), ('focus', 0, None), ('text', '', None))
        self.defineoptions(kw, optiondefs)
        DirectEntry.__init__(self, parent=parent, **kw)
        self.initialiseoptions(PChatInputTyped)
        self.whisperId = None
        self.bind(DGG.OVERFLOW, self.chatOverflow)
        self.bind(DGG.ERASE, self.chatErased)
        wantHistory = 0
        if __dev__:
            wantHistory = 1
        self.wantHistory = __dev__ or base.config.GetBool('exec-chat', 0) or localAvatar.isGM() or base.cr.wantMagicWords or base.config.GetBool('want-chat-history', wantHistory)
        self.history = [
         '']
        self.historySize = base.config.GetInt('chat-history-size', 10)
        self.historyIndex = 0
        self.wantSlidingWindow = base.config.GetBool('want-sliding-chat', 1)
        self.maxSavedLength = 100
        self.slideDistance = 10
        self.savedStringLeft = ''
        self.savedStringRight = ''
        self.fillToLength = 0
        return

    def delete(self):
        self.ignore('uber-control-arrow_up')
        self.ignore('uber-control-arrow_down')

    def requestMode(self, mode, *args):
        self.request(mode, *args)

    def defaultFilter(self, request, *args):
        if request == 'AllChat':
            if not base.talkAssistant.checkOpenTypedChat():
                messenger.send('Chat-Failed open typed chat test')
                return None
        elif request == 'PlayerWhisper':
            whisperId = args[0][0]
            if not base.talkAssistant.checkWhisperTypedChatPlayer(whisperId):
                messenger.send('Chat-Failed player typed chat test')
                return None
        elif request == 'AvatarWhisper':
            whisperId = args[0][0]
            if not base.talkAssistant.checkWhisperTypedChatAvatar(whisperId):
                messenger.send('Chat-Failed avatar typed chat test')
                return None
        return FSM.FSM.defaultFilter(self, request, *args)

    def enterOff(self):
        self.deactivate()

    def exitOff(self):
        self.activate()

    def enterAllChat(self):
        self['focus'] = 1
        self.show()

    def exitAllChat(self):
        pass

    def enterGuildChat(self):
        self['focus'] = 1
        self.show()

    def exitGuildChat(self):
        pass

    def enterShipPVPChat(self):
        self['focus'] = 1
        self.show()

    def exitShipPVPChat(self):
        pass

    def enterCrewChat(self):
        self['focus'] = 1
        self.show()

    def exitCrewChat(self):
        pass

    def enterPlayerWhisper(self, whisperId):
        self.tempText = self.get()
        self.activate()
        self.whisperId = whisperId

    def exitPlayerWhisper(self):
        self.set(self.tempText)
        self.whisperId = None
        return

    def enterAvatarWhisper(self, whisperId):
        self.tempText = self.get()
        self.activate()
        self.whisperId = whisperId

    def exitAvatarWhisper(self):
        self.set(self.tempText)
        self.whisperId = None
        return

    def activate(self):
        self.set('')
        self['focus'] = 1
        self.accept('uber-escape', self.handleEscape)
        if self.wantHistory:
            self.accept('uber-control-arrow_up', self.setPrevHistory)
            self.accept('uber-control-arrow_down', self.setNextHistory)
            self.historyIndex = None
        if self.wantSlidingWindow:
            self.accept('uber-arrow_right', self.movingRight)
            self.accept('uber-arrow_left', self.movingLeft)
            self.accept('uber-backspace', self.movingLeft)
            self.accept('uber-home', self.fullSlideLeft)
            self.accept('uber-end', self.fullSlideRight)
        self.show()
        return

    def handleEscape(self):
        localAvatar.chatMgr.deactivateChat()

    def deactivate(self):
        self.set('')
        self.savedStringLeft = ''
        self.savedStringRight = ''
        self['focus'] = 0
        self.ignore('uber-escape')
        self.ignore('uber-control-arrow_up')
        self.ignore('uber-control-arrow_down')
        self.ignore('uber-arrow_right')
        self.ignore('uber-arrow_left')
        self.ignore('uber-backspace')
        self.ignore('uber-home')
        self.ignore('uber-end')
        self.hide()

    def sendChat(self, text, overflow=False):
        text = self.savedStringLeft + text + self.savedStringRight
        self.savedStringLeft = self.savedStringRight = ''
        if text:
            self.set('')
            if base.config.GetBool('exec-chat', 0) and text[0] == '>':
                text = self.__execMessage(text[1:])
                base.localAvatar.setChatAbsolute(text, CFSpeech | CFTimeout)
                return
            elif base.config.GetBool('want-slash-commands', 1) and text[0] == '/':
                base.talkAssistant.executeSlashCommand(text)
            elif (localAvatar.isGM() or base.cr.wantMagicWords) and text[0] == '`':
                base.talkAssistant.executeGMCommand(text)
            else:
                self.sendChatByMode(text)
            if self.wantHistory:
                self.addToHistory(text)
        else:
            localAvatar.chatMgr.deactivateChat()
        if not overflow:
            self.hide()
            localAvatar.chatMgr.messageSent()

    def sendChatByMode(self, text):
        messenger.send('sentRegularChat')
        state = self.getCurrentOrNextState()
        if state == 'PlayerWhisper':
            base.talkAssistant.sendAccountTalk(text, self.whisperId)
        elif state == 'AvatarWhisper':
            base.talkAssistant.sendWhisperTalk(text, self.whisperId)
        elif state == 'GuildChat':
            base.talkAssistant.sendGuildTalk(text)
        elif state == 'CrewChat':
            base.talkAssistant.sendPartyTalk(text)
        elif state == 'ShipPVPChat':
            base.talkAssistant.sendShipPVPCrewTalk(text)
        else:
            base.talkAssistant.sendOpenTalk(text)

    def checkKey(self, key):
        print 'key typed: %s' % key.getKeycode()

    def movingRight(self):
        if self.guiItem.getCursorPosition() == self.guiItem.getNumCharacters():
            if len(self.savedStringRight) > 0:
                self.slideBack(self.get())

    def movingLeft(self):
        if self.guiItem.getCursorPosition() == 0:
            if len(self.savedStringLeft) > 0:
                self.slideFront(self.get())

    def fullSlideLeft(self):
        while len(self.savedStringLeft) > 0:
            self.slideFront(self.get())

        self.guiItem.setCursorPosition(0)

    def fullSlideRight(self):
        while len(self.savedStringRight) > 0:
            self.slideBack(self.get())

        self.guiItem.setCursorPosition(self.guiItem.getNumCharacters())

    def chatOverflow(self, overflowText):
        if overflowText.hasKeycode():
            newText = self.get() + chr(overflowText.getKeycode())
            if not self.wantSlidingWindow:
                self.sendChat(newText, overflow=True)
            else:
                self.fillToLength = self.guiItem.getNumCharacters() - 3
                if len(self.savedStringLeft) + len(self.savedStringRight) + self.slideDistance <= self.maxSavedLength:
                    self.slideBack(newText)

    def chatErased(self, key):
        if not self.wantSlidingWindow:
            return
        while self.guiItem.getNumCharacters() < self.fillToLength and (len(self.savedStringRight) > 0 or len(self.savedStringLeft) > 0):
            if len(self.savedStringRight) > 0:
                self.set(self.get() + self.savedStringRight[0])
                self.savedStringRight = self.savedStringRight[1:]
            elif len(self.savedStringLeft) > 0:
                self.set(self.savedStringLeft[-1] + self.get())
                self.savedStringLeft = self.savedStringLeft[0:-1]
                self.guiItem.setCursorPosition(self.guiItem.getCursorPosition() + 1)

    def slideBack(self, inputText):
        if len(self.savedStringRight) < 1:
            self.savedStringLeft += inputText[0:self.slideDistance]
            self.set(inputText[self.slideDistance:] + self.savedStringRight[0:self.slideDistance])
        else:
            self.savedStringLeft += inputText[0:self.slideDistance]
            self.set(inputText[self.slideDistance:] + self.savedStringRight[0:self.slideDistance])
            self.savedStringRight = self.savedStringRight[self.slideDistance:]
            self.guiItem.setCursorPosition(self.guiItem.getNumCharacters() - self.slideDistance)
        print '%s + %s + %s' % (self.savedStringLeft, self.get(), self.savedStringRight)

    def slideFront(self, inputText):
        self.savedStringRight = inputText[-1 * self.slideDistance:] + self.savedStringRight
        self.set(self.savedStringLeft[-1 * self.slideDistance:] + inputText[:-1 * self.slideDistance])
        self.savedStringLeft = self.savedStringLeft[0:-1 * self.slideDistance]
        self.guiItem.setCursorPosition(self.slideDistance)
        print '%s + %s + %s' % (self.savedStringLeft, self.get(), self.savedStringRight)

    def addToHistory(self, text):
        self.history = [
         text] + self.history[:self.historySize - 1]
        self.historyIndex = 0

    def setPrevHistory(self):
        if self.historyIndex is None:
            self.historyIndex = -1
        self.historyIndex += 1
        self.historyIndex %= len(self.history)
        self.set(self.history[self.historyIndex])
        return

    def setNextHistory(self):
        if self.historyIndex is None:
            self.historyIndex = len(self.history) - 1
        self.historyIndex -= 1
        self.historyIndex %= len(self.history)
        self.set(self.history[self.historyIndex])
        return

    def importExecNamespace(self):
        pass

    def __execMessage(self, message):
        if not PChatInputTyped.ExecNamespace:
            PChatInputTyped.ExecNamespace = {}
            exec 'from pandac.PandaModules import *' in globals(), self.ExecNamespace
            self.importExecNamespace()
        try:
            return str(eval(message, globals(), PChatInputTyped.ExecNamespace))
        except SyntaxError:
            try:
                exec message in globals(), PChatInputTyped.ExecNamespace
                return 'ok'
            except:
                exception = sys.exc_info()[0]
                extraInfo = sys.exc_info()[1]
                if extraInfo:
                    return str(extraInfo)
                else:
                    return str(exception)

        except:
            exception = sys.exc_info()[0]
            extraInfo = sys.exc_info()[1]
            if extraInfo:
                return str(extraInfo)
            else:
                return str(exception)