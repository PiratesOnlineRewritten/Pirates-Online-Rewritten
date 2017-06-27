from panda3d.core import PandaNode
from otp.nametag import NametagGlobals

class Nametag(PandaNode):
    CName = NametagGlobals.CName
    CSpeech = NametagGlobals.CSpeech
    CThought = NametagGlobals.CThought

    def __init__(self):
        PandaNode.__init__(self, self.__class__.__name__)

        self.avatar = None
        self.font = None
        self.name = ''
        self.displayName = ''
        self.contents = 0
        self.active = False

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
