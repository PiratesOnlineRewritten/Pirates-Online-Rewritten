from pirates.world.AreaBuilderBaseAI import AreaBuilderBaseAI
from direct.directnotify.DirectNotifyGlobal import directNotify

class GridAreaBuilderAI(AreaBuilderBaseAI):
    notify = directNotify.newCategory('GridAreaBuilderAI')

    def __init__(self, air, parent):
        AreaBuilderBaseAI.__init__(self, air, parent)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic):
        newObj = None

        return newObj