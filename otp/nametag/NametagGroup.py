from panda3d.core import *
from otp.nametag import NametagGlobals
from otp.nametag.Nametag2d import Nametag2d
from otp.nametag.Nametag3d import Nametag3d

class NametagGroup(object):
    CCNormal = NametagGlobals.CCNormal
    CCNoChat = NametagGlobals.CCNoChat
    CCNonPlayer = NametagGlobals.CCNonPlayer
    CCSuit = NametagGlobals.CCSuit
    CCToonBuilding = NametagGlobals.CCToonBuilding
    CCSuitBuilding = NametagGlobals.CCSuitBuilding
    CCHouseBuilding = NametagGlobals.CCHouseBuilding
    CCSpeedChat = NametagGlobals.CCSpeedChat
    CCFreeChat = NametagGlobals.CCFreeChat

    CHAT_TIMEOUT_MAX = 12.0
    CHAT_TIMEOUT_MIN = 4.0
    CHAT_TIMEOUT_PROP = 0.5

    def __init__(self):
        self.avatar = None
        self.font = None
        self.name = ''
        self.displayName = ''
        self.colorCode = 0
        self.active = False
        self.icon = NodePath('icon')
        self.nameWordwrap = 0
        self.chatFlags = 0
        self.chatString = ''
        self.chatPage = 0

        self.nametag2d = Nametag2d()
        self.nametag3d = Nametag3d()

        self.chatPages = []
        self.nametags = [self.nametag2d, self.nametag3d]

        self.tickTask = taskMgr.add(self.__tick, self.getUniqueName('tick'), sort=45)
        self.stompTask = None
        self.stompText = None
        self.stompFlags = 0
        self.chatTimeoutTask = None

    def getUniqueId(self):
        return 'NametagGroup-%s' % id(self)

    def getUniqueName(self, name):
        return '%s-%s' % (self.getUniqueId(), name)

    def getNametag2d(self):
        return self.nametag2d

    def getNametag3d(self):
        return self.nametag3d

    def hasNametag(self, nametag):
        return nametag in self.nametags

    def addNametag(self, nametag):
        if self.hasNametag(nametag):
            return

        self.nametags.append(nametag)

    def removeNametag(self, nametag):
        if not self.hasNametag(nametag):
            return

        self.nametags.remove(nametag)

    def manage(self, manager):
        pass

    def unmanage(self, manager):
        pass

    def getNumChatPages(self):
        return len(self.chatPages)

    def getChatStomp(self):
        return bool(self.stompTask)

    def getChat(self):
        if self.chatPage >= len(self.chatPages):
            return ''

        return self.chatPages[self.chatPage]

    def getStompText(self):
        return self.stompText

    def getStompDelay(self):
        return 0.2

    def setChat(self, chatString, chatFlags):
        if not self.chatFlags & NametagGlobals.CFSpeech:
            # We aren't already displaying some chat. Therefore, we don't have
            # to stomp.
            self._setChat(chatString, chatFlags)
        else:
            # Stomp!
            self.clearChat()
            self.stompText = chatString
            self.stompFlags = chatFlags
            self.stompTask = taskMgr.doMethodLater(self.getStompDelay(), self.__updateStomp, self.getUniqueName('chat'))

    def _setChat(self, chatString, chatFlags):
        if chatString:
            self.chatPages = chatString.split('\x07')
            self.chatFlags = chatFlags
            self.chatString = chatString
        else:
            self.chatPages = []
            self.chatFlags = 0

        self.setPageNumber(0)
        self._stopChatTimeout()
        if chatFlags & NametagGlobals.CFTimeout:
            self._startChatTimeout()

    def __updateStomp(self, task):
        self._setChat(self.stompText, self.stompFlags)
        self.stompTask = None

    def clearChat(self):
        self._setChat('', 0)
        if self.stompTask:
            self.stompTask.remove()

    def _startChatTimeout(self):
        length = len(self.getChat())
        timeout = min(max(length*self.CHAT_TIMEOUT_PROP, self.CHAT_TIMEOUT_MIN), self.CHAT_TIMEOUT_MAX)
        self.chatTimeoutTask = taskMgr.doMethodLater(timeout, self.__doChatTimeout, self.getUniqueName('chat-timeout'))

    def __doChatTimeout(self, task):
        self._setChat('', 0)
        return task.done

    def _stopChatTimeout(self):
        if self.chatTimeoutTask:
            taskMgr.remove(self.chatTimeoutTask)

    def setPageNumber(self, chatPage):
        self.chatPage = chatPage
        self.updateTags()

    def setAvatar(self, avatar):
        self.avatar = avatar
        self.updateTags()

    def getAvatar(self):
        return self.avatar

    def setFont(self, font):
        self.font = font
        self.updateTags()

    def getFont(self):
        return self.font

    def setName(self, name):
        self.name = name
        self.updateTags()

    def getName(self):
        return self.name

    def setDisplayName(self, displayName):
        self.displayName = displayName
        self.updateTags()

    def getDisplayName(self):
        return self.displayName

    def setColorCode(self, colorCode):
        self.colorCode = colorCode
        self.updateTags()

    def getColorCode(self):
        return self.colorCode

    def setActive(self, active):
        self.active = active
        self.updateTags()

    def getActive(self):
        return self.active

    def setContents(self, contents):
        for nametag in self.nametags:
            nametag.setContents(contents)

    def getNameIcon(self):
        return self.icon

    def setNameWordwrap(self, nameWordwrap):
        self.nameWordwrap = nameWordwrap
        self.updateTags()

    def getNameWordwrap(self):
        return self.nameWordwrap

    def __tick(self, task):
        for nametag in self.nametags:
            nametag.tick()

        return task.cont

    def updateTags(self):
        for nametag in self.nametags:
            self.updateTag(nametag)

    def updateTag(self, nametag):
        nametag.avatar = self.avatar
        nametag.font = self.font
        nametag.name = self.name
        nametag.displayName = self.displayName
        nametag.icon = self.icon
        nametag.chatFlags = self.chatFlags
        nametag.chatString = self.chatString
        nametag.update()
