from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.leveleditor import ObjectList
from direct.distributed.GridParent import GridParent

class AreaBuilderBaseAI(DirectObject):
    notify = directNotify.newCategory('AreaBuilderBaseAI')

    def __init__(self, air, parent):
        self.air = air
        self.parent = parent
        self.objectList = {}

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None

        if objType == ObjectList.AREA_TYPE_ISLAND:
            newObj = self.__createIsland(objectData, parent, parentUid, objKey, dynamic)
        else:
            parent = self.air.worldCreator.world.uidMgr.justGetMeMeObject(parentUid)

            if not parent:
                return newObj

            newObj = parent.builder.createObject(objType, objectData, parent, parentUid, objKey, dynamic)

        return newObj

    def __createIsland(self, objectData, parent, parentUid, objKey, dynamic):
        from pirates.world.DistributedIslandAI import DistributedIslandAI

        worldIsland = self.air.worldCreator.getIslandWorldDataByUid(objKey)

        island = DistributedIslandAI(self.air)
        island.setUniqueId(objKey)
        island.setName(worldIsland.get('Name', ''))
        island.setModelPath(worldIsland['Visual']['Model'])
        island.setPos(worldIsland.get('Pos', (0, 0, 0)))
        island.setHpr(worldIsland.get('Hpr', (0, 0, 0)))
        island.setScale(worldIsland.get('Scale', 1))
        island.setUndockable(worldIsland.get('Undockable', False))

        if 'Objects' in worldIsland:
            for obj in worldIsland['Objects'].values():
                if obj['Type'] == 'LOD Sphere':
                    island.setZoneSphereSize(*obj['Radi'])

        self.parent.generateChildWithRequired(island, island.startingZone)
        self.addObject(island)

        return island

    def addObject(self, object):
        if not object:
            self.notify.warning('Cannot add an invalid object!')
            return

        if object.doId in self.objectList:
            self.notify.warning('Cannot add an already existing object %d!' % object.doId)
            return

        self.parent.uidMgr.addUid(object.getUniqueId(), object.doId)
        self.objectList[object.doId] = object

    def removeObject(self, object):
        if not object:
            self.notify.warning('Cannot remove an invalid object!')
            return

        if object.doId not in self.objectList:
            self.notify.warning('Cannot remove a non-existant object %d!' % object.doId)
            return

        self.parent.uidMgr.removeUid(object.getUniqueId())
        del self.objectList[object.doId]

    def deleteObject(self, doId):
        object = self.objectList.get(doId)

        if not object:
            self.notify.warning('Cannot delete an invalid object!')
            return

        object.requestDelete()
        self.removeObject(object)

    def broadcastObjectPosition(self, object):
        if not object:
            self.notify.warning('Failed to broadcast position for non-existant object!')
            return

        object.d_setPos(*object.getPos())
        object.d_setHpr(*object.getHpr())
