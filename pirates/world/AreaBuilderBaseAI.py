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
        self.wantObjectPrintout = config.GetBool('want-object-printout', False)

    def parentToCellOrigin(self, parent, instance):
        if not instance:
            return self.notify.warning('Cannot parent invalid instance type to %r!' % parent)

        instance.reparentTo(parent)

        instance.d_setPos(*instance.getPos())
        instance.d_setHpr(*instance.getHpr())

        return instance

    def createObject(self, objType, objectData, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        newObj = None

        if objType == ObjectList.AREA_TYPE_ISLAND:
            newObj = self.__createIsland(objectData, parent, parentUid, objKey, dynamic)
        else:
            parent = self.air.worldCreator.world.uidMgr.justGetMeMeObject(parentUid)

            if not parent:
                return newObj

            newObj = parent.builder.createObject(objType, objectData, parent, parentUid, objKey, dynamic)

        if newObj is not None and objType != 'Building Exterior' and objType != ObjectList.AREA_TYPE_ISLAND and self.wantObjectPrintout:
            indent = '- '
            if 'Island' not in fileName:
                indent = '-- '
            print('%sGenerated %s (%s) in zone %s with doId %d' % (indent, newObj.__class__.__name__, objKey, newObj.zoneId, newObj.doId))

        return newObj

    def __createIsland(self, objectData, parent, parentUid, objKey, dynamic):
        from pirates.world.DistributedIslandAI import DistributedIslandAI

        worldIsland = self.air.worldCreator.getIslandWorldDataByUid(objKey)

        island = DistributedIslandAI(self.air)
        island.setUniqueId(objKey)
        island.setName(worldIsland.get('Name', 'island'))
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

        if self.air.worldCreator.wantPrintout:
            print '-' * 100
            print 'Generated Island %s (%s) in zone %d with doId %d' % (island.getLocalizerName(), objKey, island.zoneId, island.doId)

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

        if not doId:
            self.notify.warning('Cannot delete an invalid object!')
            return

        object.requestDelete()
        self.removeObject(object)
