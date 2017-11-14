from panda3d.core import *
from otp.nametag import NametagGlobals

class Nametag(PandaNode):
    CName = NametagGlobals.CName
    CSpeech = NametagGlobals.CSpeech
    CThought = NametagGlobals.CThought

    IS_3D = True
    NAME_PADDING = 0.2
    CHAT_ALPHA = 1.0
    DEFAULT_CHAT_WORDWRAP = 10.0

    def __init__(self):
        PandaNode.__init__(self, self.__class__.__name__)

        self.innerNP = NodePath.anyPath(self).attachNewNode('nametag_contents')
        self.icon = None

        self.avatar = None
        self.font = None
        self.name = ''
        self.displayName = ''
        self.contents = 0
        self.active = False
        self.qtColor = VBase4(1, 1, 1, 1)
        self.nameFg = VBase4(0, 0, 0, 1)
        self.nameBg = VBase4(1, 1, 1, 1)
        self.chatFg = VBase4(0, 0, 0, 1)
        self.chatBg = VBase4(1, 1, 1, 1)
        self.chatFlags = 0
        self.chatString = ''
        self.wordWrap = 7.5
        self.chatWordWrap = None

    def setAvatar(self, avatar):
        self.avatar = avatar

    def getAvatar(self):
        return self.avatar

    def setFont(self, font):
        self.font = font

    def getFont(self):
        return self.font

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setDisplayName(self, displayName):
        self.displayName = displayName

    def getDisplayName(self):
        return self.displayName

    def setContents(self, contents):
        self.contents = contents

    def getContents(self):
        return self.contents

    def setActive(self, active):
        self.active = active

    def getActive(self):
        return self.active

    def tick(self):
        pass

    def update(self):
        self.innerNP.node().removeAllChildren()

        if self.contents & self.CThought and self.chatFlags & NametagGlobals.CFThought:
            self.showThought()
        elif self.contents & self.CSpeech and self.chatFlags & NametagGlobals.CFSpeech:
            self.showSpeech()
        elif self.contents & self.CName and self.displayName:
            self.showName()

    def showBalloon(self, balloon, text):
        if not self.font:
            return

        color = self.qtColor if (self.chatFlags & NametagGlobals.CFQuicktalker) else self.chatBg
        if color[3] > self.CHAT_ALPHA:
            color = (color[0], color[1], color[2], self.CHAT_ALPHA)

        reversed = (self.IS_3D and (self.chatFlags & NametagGlobals.CFReversed))
        balloon, frame = balloon.generate(text, self.font, textColor=self.chatFg, balloonColor=color, wordWrap=self.chatWordWrap or \
            self.DEFAULT_CHAT_WORDWRAP, reversed=reversed)

        balloon.reparentTo(self.innerNP)
        self.frame = frame

    def showThought(self):
        self.showBalloon(self.getThoughtBalloon(), self.chatString)

    def showSpeech(self):
        self.showBalloon(self.getSpeechBalloon(), self.chatString)

    def showName(self):
        if not self.font:
            return

        self.innerNP.attachNewNode(self.icon.node())
