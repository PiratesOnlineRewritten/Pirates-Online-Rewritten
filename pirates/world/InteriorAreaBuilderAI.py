from pirates.world.AreaBuilderBaseAI import AreaBuilderBaseAI
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import PiratesGlobals
from pirates.leveleditor import ObjectList
from pirates.world.DistributedInteriorDoorAI import DistributedInteriorDoorAI

class InteriorAreaBuilderAI(AreaBuilderBaseAI):
    notify = directNotify.newCategory('GridAreaBuilderAI')

    def __init__(self, air, parent):
        AreaBuilderBaseAI.__init__(self, air, parent)

        self.wantParlorGames = config.GetBool('want-parlor-games', True)

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic):
        newObj = None

        if objType == ObjectList.DOOR_LOCATOR_NODE:
            newObj = self.__createDoorLocatorNode(objectData, parent, parentUid, objKey)
        elif objType == 'Parlor Game' and self.wantParlorGames:
            pass

        return newObj

    def __createDoorLocatorNode(self, objectData, parent, parentUid, objKey):
        exteriorDoor = self.parent.getExteriorDoor()

        if not exteriorDoor:
            self.notify.warning('Cannot create interior door for interior %d, with no exterior door!' % self.parent.doId)
            return

        interiorDoor = DistributedInteriorDoorAI(self.air)
        interiorDoor.setUniqueId(objKey)
        interiorDoor.setHpr(objectData.get('Hpr', (0, 0, 0)))
        interiorDoor.setHpr(objectData.get('Hpr', (0, 0, 0)))
        interiorDoor.setScale(objectData.get('Scale', 1))
        interiorDoor.setInteriorId(self.parent.doId, self.parent.parentId, self.parent.zoneId)
        interiorDoor.setExteriorId(exteriorDoor.parentId, exteriorDoor.getParentObj().parentId, exteriorDoor.zoneId)
        interiorDoor.setBuildingDoorId(exteriorDoor.doId)

        self.parent.setInteriorDoor(interiorDoor)
        self.parent.generateChildWithRequired(interiorDoor, PiratesGlobals.InteriorDoorZone)
        self.addObject(interiorDoor)

        return interiorDoor
