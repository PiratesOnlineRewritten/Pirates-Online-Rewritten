from panda3d.core import *

from otp.nametag import NametagGlobals
from otp.nametag.Nametag2d import Nametag2d
from otp.nametag.Nametag3d import Nametag3d
from otp.nametag.NametagConstants import *


class NametagGroup:
    CCNormal = 0
    CCNoChat = 1
    CCNonPlayer = 2
    CCSuit = 3
    CCToonBuilding = 4
    CCSuitBuilding = 5
    CCHouseBuilding = 6
    CCSpeedChat = 7
    CCFreeChat = 8

    _unique_index = 0

    def __init__(self):
        self.nametags = []

        self.name_font = None
        self.chat_font = None

        self.avatar = None
        self.node = None

        self.name = ''
        self.display_name = ''

        self.chat_pages = []
        self.stomp_text = ''
        self.unique_name = ''

        self.region_seq = 0

        self.name_icon = NodePath.anyPath(PandaNode('icon'))
        self.name_frame = Vec4(0, 0, 0, 0)

        self.wordwrap = -1.0
        self.color_code = 0
        self.qt_color = NametagGlobals._default_qt_color
        self.balloon_color = NametagGlobals._balloon_modulation_color
        self.shadow = (0, 0)
        self.has_shadow = False

        self.timeout = 0.0
        self.timeout_start = 0.0
        self.has_timeout = False
        self.stomp_time = 0.0
        self.stomp_chat_flags = None
        self.chat_flags = 0
        self.page_number = 0
        self.stomp_delay = 0.5
        self.chat_stomp = 0

        self.unique_name = 'nametag-%d' % NametagGroup._unique_index
        NametagGroup._unique_index += 1

        self.object_code = 0
        self.nametag3d_flag = 0
        self.manager = None

        self.region_seq += 1

        self.contents = CFSpeech | CFThought | CFQuicktalker
        self.is_active = 1
        self.active = NametagGlobals._master_nametags_active
        self.visible = NametagGlobals._master_nametags_visible

        self.tag2d = Nametag2d()
        self.tag3d = Nametag3d()
        self.addNametag(self.tag2d)
        self.addNametag(self.tag3d)

    def setFont(self, font):
        self.setNameFont(font)
        self.setChatFont(font)

    def setNameFont(self, font):
        self.name_font = font

    def getNameFont(self):
        return self.name_font

    def setChatFont(self, font):
        self.chat_font = font

    def getChatFont(self):
        return self.chat_font

    def setAvatar(self, avatar):
        self.avatar = avatar

    def getAvatar(self):
        return self.avatar

    def setNameIcon(self, icon):
        self.name_icon = icon

    def getNameIcon(self):
        return self.name_icon

    def setColorCode(self, code):
        self.color_code = code

    def getColorCode(self):
        return self.color_code

    def setContents(self, contents):
        self.contents = contents

    def getContents(self):
        return self.contents

    def setDisplayName(self, name):
        self.display_name = name

        if name and self.name_font:
            text_node = NametagGlobals.getTextNode()
            text_node.setFont(self.name_font)
            text_node.setWordwrap(self.getNameWordwrap())
            text_node.setAlign(TextNode.ACenter)
            text_node.setText(name)
            gen = text_node.generate()
            self.node = gen
            self.name_frame = text_node.getCardActual()

            if self.has_shadow:
                self.node = PandaNode('name')
                self.node.addChild(gen)

                pos = Point3(self.shadow[0], 0, -self.shadow[1])
                attached = NodePath.anyPath(self.node).attachNewNode(gen.copySubgraph())
                attached.setPos(pos)
                attached.setColor(0, 0, 0, 1)

        else:
            self.node = None

        self.updateContentsAll()

    def getDisplayName(self):
        return self.display_name

    def setName(self, name):
        self.name = name
        self.setDisplayName(name)

    def getName(self):
        return self.name

    def getNameFrame(self):
        return self.name_frame

    def setNameWordwrap(self, wordwrap):
        self.wordwrap = wordwrap
        self.setDisplayName(self.display_name)

    def getNameWordwrap(self):
        if self.wordwrap > 0.0:
            return self.wordwrap

        wordwrap = NametagGlobals.getNameWordwrap()
        return {self.CCToonBuilding: 8.0,
                self.CCSuitBuilding: 8.0,
                self.CCHouseBuilding: 10.0}.get(self.color_code, wordwrap)

    def getNametag(self, index):
        return self.nametags[index]

    def getNametag2d(self):
        return self.tag2d

    def getNametag3d(self):
        return self.tag3d

    def setNametag3dFlag(self, flag):
        self.nametag3d_flag = flag

    def getNametag3dFlag(self):
        return self.nametag3d_flag

    def getNumChatPages(self):
        return len(self.chat_pages)

    def getNumNametags(self):
        return len(self.nametags)

    def setObjectCode(self, code):
        self.object_code = code

    def getObjectCode(self):
        return self.object_code

    def setPageNumber(self, page):
        if self.page_number == page:
            return

        self.page_number = page
        if self.willHaveButton():
            self.timeout_start = globalClock.getFrameTime() + 0.2
            self.has_timeout = True

        self.updateContentsAll()

    def getPageNumber(self):
        return self.page_number

    def getBalloonModulationColor(self):
        return self.balloon_color

    def setQtColor(self, color):
        self.qt_color = color

    def getQtColor(self):
        return self.qt_color

    def getRegionSeq(self):
        return self.region_seq

    def setShadow(self, shadow):
        self.shadow = shadow

    def getShadow(self):
        return self.shadow

    def getStompDelay(self):
        return self.stomp_delay

    def getStompText(self):
        return self.stomp_text

    def setUniqueId(self, name):
        self.unique_name = name

    def getUniqueId(self):
        return self.unique_name

    def hasButton(self):
        if self.has_timeout:
            return False

        return self.willHaveButton()

    def hasNoQuitButton(self):
        return (not self.has_timeout) and self.chat_flags & CFSpeech

    def hasQuitButton(self):
        return (not self.has_timeout) and self.chat_flags & CFQuitButton

    def hasPageButton(self):
        return (not self.has_timeout) and self.chat_flags & CFPageButton

    def hasShadow(self):
        return self.has_shadow

    def clearShadow(self):
        self.has_shadow = False

    def incrementNametag3dFlag(self, flag):
        self.nametag3d_flag = max(self.nametag3d_flag, flag)

    def isManaged(self):
        return self.manager is not None

    def manage(self, manager):
        if not self.manager:
            self.manager = manager
            for nametag in self.nametags:
                nametag.manage(manager)

    def unmanage(self, manager):
        if self.manager:
            self.manager = None
            for nametag in self.nametags:
                nametag.unmanage(manager)

    def addNametag(self, nametag):
        if nametag.group:
            print 'Attempt to add %s twice to %s.' % (nametag.__class__.__name__, self.name)
            return

        nametag.group = self
        nametag.updateContents()
        self.nametags.append(nametag)

        if self.manager:
            nametag.manage(self.manager)

    def removeNametag(self, nametag):
        if not nametag.group:
            print 'Attempt to removed %s twice from %s.' % (nametag.__class__.__name__, self.name)
            return

        if self.manager:
            nametag.unmanage(self.manager)

        nametag.group = None
        nametag.updateContents()
        self.nametags.remove(nametag)

    def setActive(self, active):
        self.is_active = active

    def isActive(self):
        return self.active

    def updateContentsAll(self):
        for nametag in self.nametags:
            nametag.updateContents()

    def updateRegions(self):
        for nametag in self.nametags:
            nametag.updateRegion(self.region_seq)

        self.region_seq += 1

        now = globalClock.getFrameTime()
        if self.stomp_time < now and self.chat_stomp > 1:
            self.chat_stomp = 0
            self.setChat(self.stomp_text, self.stomp_chat_flags, self.page_number)

        if self.chat_flags & CFTimeout and now >= self.timeout:
            self.clearChat()
            self.chat_stomp = 0

        v7 = False
        if self.has_timeout and now >= self.timeout_start:
            self.has_timeout = 0
            v7 = True

        if self.active != NametagGlobals._master_nametags_active:
            self.active = NametagGlobals._master_nametags_active
            v7 = True

        if self.visible == NametagGlobals._master_nametags_visible:
            if not v7:
                return

        else:
            self.visible = NametagGlobals._master_nametags_visible

        self.updateContentsAll()

    def willHaveButton(self):
        return self.chat_flags & (CFPageButton | CFQuitButton)

    def setChat(self, chat, chat_flags, page_number=0):
        self.chat_flags = chat_flags
        self.page_number = page_number

        now = globalClock.getFrameTime()
        must_split = True
        if chat_flags and chat:
            self.chat_stomp += 1
            if self.chat_stomp >= 2 and self.stomp_delay >= 0.05:
                self.stomp_text = chat
                self.stomp_chat_flags = self.chat_flags
                self.stomp_time = now + self.stomp_delay
                self.chat_flags = 0
                must_split = False

        else:
            self.chat_flags = 0
            self.chat_stomp = 0
            must_split = False

        if must_split:
            self.chat_pages = chat.split('\x07')
        else:
            self.chat_pages = []

        if self.chat_flags & CFTimeout and self.stomp_time < now:
            timeout = len(chat) * 0.5
            timeout = min(12.0, max(timeout, 4.0))
            self.timeout = timeout + now

        if self.willHaveButton():
            self.has_timeout = True
            self.timeout_start = now + 0.2

        else:
            self.has_timeout = False
            self.timeout_start = 0.0

        self.updateContentsAll()

    def getChat(self):
        if self.chat_pages:
            return self.chat_pages[self.page_number]

        return ''

    def clearChat(self):
        self.setChat('', 0, 0)

    def getChatStomp(self):
        return self.chat_stomp

    def clearAuxNametags(self):
        for nametag in self.nametags[:]:
            if nametag not in (self.tag2d, self.tag3d):
                self.removeNametag(nametag)

    def click(self):
        messenger.send(self.unique_name)

    def copyNameTo(self, to):
        return to.attachNewNode(self.node.copySubgraph())

    def displayAsActive(self):
        if self.is_active and NametagGlobals._master_nametags_active:
            return 1

        return self.hasButton()

    def frameCallback(self):
        # This should be in Nametag2d
        # I have no idea where libotp called it
        # so I'm doing it in MarginManager.update
        self.updateRegions()
