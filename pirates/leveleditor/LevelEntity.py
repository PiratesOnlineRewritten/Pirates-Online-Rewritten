from panda3d.core import NodePath

class LevelEntity(NodePath):

    def __init__(self):
        NodePath.__init__(self, 'LevelEntity')

    def setProperty(self, propertyName, propertyValue):
        if propertyName == 'None':
            pass

    def cleanUp(self):
        pass