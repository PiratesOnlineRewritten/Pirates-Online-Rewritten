from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.GridParent import GridParent
from pirates.leveleditor import ObjectList
from direct.distributed.GridParent import GridParent
from panda3d.core import Point3, NodePath

class AreaBuilderBaseAI(DirectObject):
    notify = directNotify.newCategory('AreaBuilderBaseAI')
    AREAZONE = 0

    def __init__(self, air, parent):
        self.air = air
        self.parent = parent
        self.objectList = {}

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None


        if objType == ObjectList.AREA_TYPE_ISLAND:
            newObj = self.__createIsland(objectData, parent, parentUid, objKey, dynamic)
        else:
            if not parent or not hasattr(parent, 'builder'):
                areaParent = self.air.worldCreator.world.uidMgr.justGetMeMeObject(parentUid)

                if not areaParent:
                    return newObj
            else:
                areaParent = parent

            newObj = areaParent.builder.createObject(objType, objectData, parent, parentUid, objKey, dynamic)

        return newObj

    def parentObjectToCell(self, object, zoneId=None):
        if not object:
            self.notify.warning('Failed to parent to cell for non-existant object!')
            return

        if zoneId is None:
            zoneId = self.parent.getZoneFromXYZ(object.getPos())

        cell = GridParent.getCellOrigin(self, zoneId)
        originalPos = object.getPos()

        object.reparentTo(cell)
        object.setPos(self.parent, originalPos)

        self.broadcastObjectPosition(object)


    def isChildObject(self, objKey, parentUid):
        return self.air.worldCreator.getObjectParentUid(objKey) != parentUid

    def getObjectTruePosAndParent(self, objKey, parentUid, objectData):
        if self.isChildObject(objKey, parentUid):
            parentUid = self.air.worldCreator.getObjectParentUid(objKey)
            parentData = self.air.worldCreator.getObjectDataByUid(parentUid)
            
            if parentData['Type'] == 'Island':
                return objectData.get('Pos'), NodePath()

            parentObject = NodePath('psuedo-%s' % parentUid)

            if not 'GridPos' in objectData:
                parentObject.setPos(parentData.get('Pos', Point3(0, 0, 0)))
                parentObject.setHpr(parentData.get('Hpr', Point3(0, 0, 0)))

            objectPos = objectData.get('GridPos', objectData.get('Pos', Point3(0, 0, 0)))
            return objectPos, parentObject
        return objectData.get('Pos'), NodePath()

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

    def addObject(self, object, uniqueId=None):
        if not object:
            self.notify.warning('Cannot add an invalid object!')
            return

        if object.doId in self.objectList:
            self.notify.warning('Cannot add an already existing object %d!' % object.doId)
            return

        self.parent.uidMgr.addUid(uniqueId or object.getUniqueId(), object.doId)
        self.objectList[object.doId] = object

    def removeObject(self, object, uniqueId=None):
        if not object:
            self.notify.warning('Cannot remove an invalid object!')
            return

        if object.doId not in self.objectList:
            self.notify.warning('Cannot remove a non-existant object %d!' % object.doId)
            return

        self.parent.uidMgr.removeUid(uniqueId or object.getUniqueId())
        del self.objectList[object.doId]

    def getObject(self, doId=None, uniqueId=None):
        for object in self.objectList:
            if object.doId == doId or object.getUniqueId() == uniqueId:
                return object

        return None

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
