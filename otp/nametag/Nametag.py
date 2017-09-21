from panda3d.core import PandaNode, NodePath
from otp.nametag import NametagGlobals

class Nametag(PandaNode):
    CName = NametagGlobals.CName
    CSpeech = NametagGlobals.CSpeech
    CThought = NametagGlobals.CThought

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
        self.chatFlags = 0
        self.chatString = ''

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

    def showThought(self):
        pass

    def showSpeech(self):
        pass

    def showName(self):
        if not self.font:
            return

        self.innerNP.attachNewNode(self.icon.node())
