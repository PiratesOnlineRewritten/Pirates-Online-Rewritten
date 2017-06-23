from panda3d.core import PandaNode
from otp.nametag import NametagGlobals

class Nametag(PandaNode):
    CName = NametagGlobals.CName
    CSpeech = NametagGlobals.CSpeech
    CThought = NametagGlobals.CThought

    def __init__(self):
        PandaNode.__init__(self, self.__class__.__name__)

        self.contents = 0

    def setContents(self, contents):
        self.contents = contents

    def getContents(self):
        return self.contents
