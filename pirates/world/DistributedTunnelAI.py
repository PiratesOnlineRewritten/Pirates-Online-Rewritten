from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTunnelAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTunnelAI')

    def __init__(self, air):
         DistributedNodeAI.__init__(self, air)

    def getParentingRules(self):
        return ['', '']

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId

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

    def requestArea(self, linkIndex):
        pass

    def setArea(self, worldStack, areaDoId, autoFadeIn):
        pass

    def sendLeaveTunnelDone(self):
        pass