from pirates.world.AreaBuilderBaseAI import AreaBuilderBaseAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import PiratesGlobals
from pirates.world.DistributedInteriorDoorAI import DistributedInteriorDoorAI

class InteriorAreaBuilderAI(AreaBuilderBaseAI):
    notify = directNotify.newCategory('GridAreaBuilderAI')

    def __init__(self, air, parent):
        AreaBuilderBaseAI.__init__(self, air, parent)
        self.wantParlorGames = config.GetBool('want-parlor-games', True)

        self.doorCounter = 0

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic):
        newObj = None

        if objType == 'Parlor Game' and self.wantParlorGames:
            pass

        return newObj

    def useChildPositioning(self):
        return False