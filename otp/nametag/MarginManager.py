from panda3d.core import PandaNode

class MarginManager(PandaNode):

    def __init__(self):
        PandaNode.__init__(self, 'MarginManager')

    def addGridCell(self, x, y, left, right, bottom, top):
        pass
