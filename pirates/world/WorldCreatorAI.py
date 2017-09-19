from pirates.world.WorldCreatorBase import WorldCreatorBase
from direct.showbase.DirectObject import DirectObject
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import PiratesGlobals
from pirates.leveleditor import ObjectList
from pirates.instance.DistributedMainWorldAI import DistributedMainWorldAI

class WorldCreatorAI(WorldCreatorBase, DirectObject):
    notify = directNotify.newCategory('WorldCreatorAI')

    def __init__(self, air):
        self.air = air
        self.world = None

        WorldCreatorBase.__init__(self, air)

    @classmethod
    def isObjectInCurrentGamePhase(cls, object):
        return True

    def loadObjectsFromFile(self, filename, parentIsObj=False):
        return WorldCreatorBase.loadObjectsFromFile(self, filename, self.air, parentIsObj)

    def getIslandWorldDataByUid(self, uid, world=None):
        if world is None:
            world = self.world
        regionUid = world.getUniqueId()
        objects = self.getObjectDataByUid(regionUid).get('Objects', {})
        if uid in objects:
            return objects[uid]
        return None

    def createObject(self, object, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        objType = WorldCreatorBase.createObject(self, object, parent, parentUid, objKey, dynamic, parentIsObj, fileName, actualParentObj)

        if not objType:
            return (None, None)

        newObj = None
        objParent = None

        if objType == ObjectList.AREA_TYPE_WORLD_REGION:
            objParent = self.__createWorldInstance(object, parent, parentUid, objKey, dynamic, fileName)
        else:
            newObj = self.world.builder.createObject(objType, object, parent, parentUid, objKey, dynamic, parentIsObj, fileName, actualParentObj)

        return (newObj, objParent)

    def __createWorldInstance(self, objectData, parent, parentUid, objKey, dynamic, fileName):
        self.world = DistributedMainWorldAI(self.air)
        self.world.setUniqueId(objKey)
        self.world.setName(objectData.get('Name', 'region'))
        self.world.generateWithRequired(PiratesGlobals.InstanceUberZone)

        self.air.uidMgr.addUid(self.world.getUniqueId(), self.world.doId)
        return self.world
