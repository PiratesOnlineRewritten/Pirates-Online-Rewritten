from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals
from direct.showbase import RandomNumGen

class BattleRandom():
    notify = DirectNotifyGlobal.directNotify.newCategory('BattleRandom')

    def __init__(self, avId):
        self.avId = avId
        self.mainRandomGen = RandomNumGen.RandomNumGen(self.avId)
        self.attackRandomGen = RandomNumGen.RandomNumGen(self.avId)
        self.mainCounter = 0
        self.attackCounter = 0

    def delete(self):
        del self.mainRandomGen
        del self.attackRandomGen

    def advanceAttackSeed(self):
        seedVal = self.mainRandomGen.randint(0, (1 << 16) - 1)
        self.mainCounter += 1
        self.attackCounter = 0
        self.attackRandomGen = RandomNumGen.RandomNumGen(seedVal)

    def getRandom(self, debugString='Unknown', range=[1, 100]):
        minVal = range[0]
        maxVal = range[1]
        randVal = self.attackRandomGen.randint(minVal, maxVal)
        self.attackCounter += 1
        return randVal

    def makeRandomChoice(self, rList):
        self.attackCounter += 1
        return self.attackRandomGen.choice(rList)

    def resync(self, seed=None):
        if seed is None:
            seed = self.avId
        self.mainRandomGen = RandomNumGen.RandomNumGen(self.avId)
        self.attackRandomGen = RandomNumGen.RandomNumGen(self.avId)
        self.mainCounter = 0
        self.attackCounter = 0
        return