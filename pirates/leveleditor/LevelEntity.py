from pandac.PandaModules import *

class LevelEntity(NodePath):

    def __init__(self):
        NodePath.NodePath.__init__(self, 'LevelEntity')

    def setProperty(self, propertyName, propertyValue):
        if propertyName == 'None':
            pass

    def cleanUp(self):
        pass