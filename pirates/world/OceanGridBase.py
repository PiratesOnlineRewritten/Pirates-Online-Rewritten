from pandac.PandaModules import *

class OceanGridBase():

    def __init__(self):
        NodePath.__init__(self, 'OceanGrid')

    def setWorld(self, world):
        self.world = world
        self.parentNP = world.getInstanceNodePath()
        self.reparentTo(self.parentNP)