from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase.UniqueIdManager import UniqueIdManager
from pirates.world.GridAreaBuilderAI import GridAreaBuilderAI

class DistributedGameAreaAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameAreaAI')

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)

        self.modelPath = ''
        self.links = []
        self.uniqueId = ''
        self.name = ''
        self.uidMgr = UniqueIdManager(self.air)
        self.builder = GridAreaBuilderAI(self.air, self)

    def setModelPath(self, modelPath):
        self.modelPath = modelPath

    def d_setModelPath(self, modelPath):
        self.sendUpdate('setModelPath', [modelPath])

    def b_setModelPath(self, modelPath):
        self.setModelPath(modelPath)
        self.d_setModelPath(modelPath)

    def getModelPath(self):
        return self.modelPath

    def setLinks(self, links):
        self.links = links

    def d_setLinks(self, links):
        self.sendUpdate('setLinks', [links])

    def b_setLinks(self, links):
        self.setLinks(links)
        self.d_setLinks(links)

    def getLinks(self):
        return self.links

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def d_addSpawnTriggers(self, triggerSpheres):
        self.sendUpdate('addSpawnTriggers', [triggerSpheres])

    def spawnNPC(self, spawnPtId, doId):
        pass
    
    def generateChildWithRequired(self, do, zoneId, optionalFields=[]):
        do.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, zoneId, optionalFields)