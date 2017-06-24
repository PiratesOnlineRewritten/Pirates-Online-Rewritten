from panda3d.core import PandaNode

class SeaPatchNode(PandaNode):

    def __init__(self, name, patch):
        PandaNode.__init__(self, name)

        self.patch = patch

        self.wantReflect = False
        self.wantColor = False
        self.wantNormal = False
        self.wantUv = False

    def setWantReflect(self, wantReflect):
        self.wantReflect = wantReflect

    def getWantReflect(self):
        return self.wantReflect

    def setWantColor(self, wantColor):
        self.wantColor = wantColor

    def getWantColor(self):
        return self.wantColor

    def setWantNormal(self, wantNormal):
        self.wantNormal = wantNormal

    def getWantNormal(self):
        return self.wantNormal

    def setWantUv(self, wantUv):
        self.wantUv = wantUv

    def getWantUv(self):
        return self.wantUv

    def collectGeometry(self):
        pass
