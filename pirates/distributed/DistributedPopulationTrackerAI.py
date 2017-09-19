from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPopulationTrackerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPopulationTrackerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.shardId = 0
        self.population = 0
        self.popLimits = [0, 0]

    def setShardId(self, shardId):
        self.shardId = shardId

    def d_setShardId(self, shardId):
        self.sendUpdate('setShardId', [shardId])

    def b_setShardId(self, shardId):
        self.setShardId(shardId)
        self.d_setShardId(shardId)

    def getShardId(self):
        return self.shardId

    def setPopulation(self, population):
        self.population = population

    def d_setPopulation(self, population):
        self.sendUpdate('setPopulation', [population])

    def b_setPopulation(self, population):
        self.setPopulation(population)
        self.d_setPopulation(population)

    def getPopulation(self):
        return self.population

    def setPopLimits(self, min, max):
        self.popLimits = [min, max]

    def d_setPopLimits(self, min, max):
        self.sendUpdate('setPopLimits', [min, max])

    def b_setPopLimits(self, min, max):
        self.setPopLimits(min, max)
        self.d_setPopLimits(min, max)

    def getPopLimits(self):
        return self.popLimits
