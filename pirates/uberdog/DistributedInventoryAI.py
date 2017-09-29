from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType

class DistributedInventoryAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.ownerId = 0
        self.accumulators = []
        self.stackLimits = []
        self.stacks = []

    def generate(self):
        self.air.inventoryManager.addInventory(self)

        DistributedObjectAI.generate(self)

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def d_setOwnerId(self, ownerId):
        self.sendUpdate('setOwnerId', [ownerId])

    def b_setOwnerId(self, ownerId):
        self.setOwnerId(ownerId)
        self.d_setOwnerId(ownerId)

    def getOwnerId(self):
        return self.ownerId

    def setAccumulators(self, accumulators):
        self.accumulators = accumulators

    def getAccumulators(self):
        return self.accumulators

    def setStackLimits(self, stackLimits):
        self.stackLimits = stackLimits

    def getStackLimits(self):
        return self.stackLimits

    def setStacks(self, stacks):
        self.stacks = stacks

    def getStacks(self):
        return self.stacks

    def setAccumulator(self, accumulatorType, quantity):
        accumulator = self.getAccumulator(accumulatorType)

        if accumulator:
            self.accumulators[self.accumulators.index(accumulator)] = [accumulatorType, quantity]
        else:
            self.accumulators.append([accumulatorType, quantity])

        self.sendUpdate('setAccumulators', [self.accumulators])

    def d_setAccumulator(self, accumulatorType, quantity):
        self.sendUpdateToAvatarId(self.ownerId, 'accumulator', [accumulatorType, quantity])

    def b_setAccumulator(self, accumulatorType, quantity):
        self.setAccumulator(accumulatorType, quantity)
        self.d_setAccumulator(accumulatorType, quantity)

    def getAccumulator(self, accumulatorType):
        for accumulator in self.accumulators:

            if accumulator[0] == accumulatorType:
                return accumulator

        return None

    def setStackLimit(self, stackType, limit):
        stackLimit = self.getStackLimit(stackType)

        if stackLimit:
            self.stackLimits[self.stackLimits.index(stackLimit)] = [stackType, limit]
        else:
            self.stackLimits.append([stackType, limit])

        self.sendUpdate('setStackLimits', [self.stackLimits])

    def d_setStackLimit(self, stackType, limit):
        self.sendUpdateToAvatarId(self.ownerId, 'stackLimit', [stackType, limit])

    def b_setStackLimit(self, stackType, limit):
        self.setStackLimit(stackType, limit)
        self.d_setStackLimit(stackType, limit)

    def getStackLimit(self, stackType):
        for stackLimit in self.stackLimits:

            if stackLimit[0] == stackType:
                return stackLimit

        return None

    def setStack(self, stackType, quantity):
        stack = self.getStack(stackType)

        if stack:
            self.stacks[self.stacks.index(stack)] = [stackType, quantity]
        else:
            self.stacks.append([stackType, quantity])

        self.sendUpdate('setStacks', [self.stacks])

    def d_setStack(self, stackType, quantity):
        self.sendUpdateToAvatarId(self.ownerId, 'stack', [stackType, quantity])

    def b_setStack(self, stackType, quantity):
        self.setStack(stackType, quantity)
        self.d_setStack(stackType, quantity)

    def getStack(self, stackType):
        for stack in self.stacks:

            if stack[0] == stackType:
                return stack

        return None

    def d_setTemporaryInventory(self, temporaryInventory):
        self.sendUpdateToAvatarId(self.ownerId, 'setTemporaryInventory', [temporaryInventory])

    def sendMaxHp(self, limit, avId):
        avatar = self.air.doId2do.get(self.ownerId)

        if not avatar:
            return

        avatar.b_setHp(avatar.getMaxHp(), 0)

    def sendMaxMojo(self, limit, avId):
        avatar = self.air.doId2do.get(self.ownerId)

        if not avatar:
            return

        avatar.b_setMojo(avatar.getMaxMojo())

    def d_requestInventoryComplete(self):
        self.sendUpdateToAvatarId(self.ownerId, 'requestInventoryComplete', [])

    def setGoldInPocket(self, quantity):
        self.b_setStack(InventoryType.ItemTypeMoney, quantity)

    def getGoldInPocket(self):
        item = self.getStack(InventoryType.ItemTypeMoney)

        if not item:
            return 0

        return item[1]

    def setOverallRep(self, quantity):
        self.b_setAccumulator(InventoryType.OverallRep, quantity)

    def getOverallRep(self):
        item = self.getAccumulator(InventoryType.OverallRep)

        if not item:
            return 0

        return item[1]

    def setPotionsRep(self, quantity):
        self.b_setAccumulator(InventoryType.PotionsRep, quantity)

    def getPotionsRep(self):
        item = self.getAccumulator(InventoryType.PotionsRep)

        if not item:
            return 0

        return item[1]

    def setFishingRep(self, quantity):
        self.b_setAccumulator(InventoryType.FishingRep, quantity)

    def getFishingRep(self):
        item = self.getAccumulator(InventoryType.FishingRep)

        if not item:
            return 0

        return item[1]

    def delete(self):
        self.air.inventoryManager.removeInventory(self)

        DistributedObjectAI.delete(self)
