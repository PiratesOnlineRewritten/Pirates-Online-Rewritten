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

    def createObject(self, object, parent, parentUid, objKey, dynamic, parentIsObj=False, fileName=None, actualParentObj=None):
        objType = WorldCreatorBase.createObject(self, object, parent, parentUid, objKey, dynamic, parentIsObj, fileName, actualParentObj)

        if not objType:
            return (None, None)

        newObj = None
        objParent = None

        if objType == ObjectList.AREA_TYPE_WORLD_REGION:
            self.world = self.__createWorldInstance(object, parent, parentUid, objKey, dynamic)
        else:
            newObj = self.world.builder.createObject(objType, object, parent, parentUid, objKey, dynamic)

        return (newObj, objParent)
    
    def __createWorldInstance(self, objectData, parent, parentUid, objKey, dynamic):
        instance = DistributedMainWorldAI(self.air)
        instance.setUniqueId(objKey)
        instance.setName(objectData.get('Name', 'region'))
        instance.generateWithRequired(PiratesGlobals.InstanceUberZone)
        self.air.uidMgr.addUid(instance.getUniqueId(), instance.doId)

        return instance