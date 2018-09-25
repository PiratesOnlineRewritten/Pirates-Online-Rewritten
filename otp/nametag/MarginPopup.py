from panda3d.core import *

from otp.nametag import NametagGlobals


class MarginPopup(PandaNode):

    def __init__(self):
        PandaNode.__init__(self, 'popup')

        self.managed = False
        self.visible = False
        self.np = None
        self.cell_width = 1.0
        self.seq = NametagGlobals._margin_prop_seq

    def getCellWidth(self):
        return self.cell_width

    def setManaged(self, value):
        self.managed = value
        if value:
            self.np = NodePath.anyPath(self)

        else:
            self.np = None

    def isManaged(self):
        return self.managed

    def setVisible(self, value):
        self.visible = value

    def isVisible(self):
        return self.visible

    def getScore(self):
        return 0.0

    def getObjectCode(self):
        return 0

    def considerVisible(self):
        if self.seq != NametagGlobals._margin_prop_seq:
            self.seq = NametagGlobals._margin_prop_seq
            self.updateContents()

    def updateContents(self):
        pass

    def frameCallback(self):
        pass
