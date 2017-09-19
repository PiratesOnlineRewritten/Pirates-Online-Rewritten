from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedBattleAvatarAI import DistributedBattleAvatarAI

class DistributedBattleNPCAI(DistributedBattleAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleNPCAI')

    def __init__(self, air):
        DistributedBattleAvatarAI.__init__(self, air)

        self.name = ''
        self.spawnPos = [0, 0, 0]
        self.spawnPosIndex = ''
        self.associatedQuests = []
        self.actorAnims = ['', '', '', '']
        self.collisionMode = 0
        self.initZ = 0
        self.isPet = False

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setSpawnPos(self, x, y, z):
        self.spawnPos = [x, y, z]

    def d_setSpawnPos(self, x, y, z):
        self.sendUpdate('setSpawnPos', [x, y, z])

    def b_setSpawnPos(self, x, y, z):
        self.setSpawnPos(x, y, z)
        self.d_setSpawnPos(x, y, z)

    def getSpawnPos(self):
        return self.spawnPos

    def setSpawnPosIndex(self, spawnPosIndex):
        self.spawnPosIndex = spawnPosIndex

    def d_setSpawnPosIndex(self, spawnPosIndex):
        self.sendUpdate('setSpawnPosIndex', [spawnPosIndex])

    def b_setSpawnPosIndex(self, spawnPosIndex):
        self.setSpawnPosIndex(spawnPosIndex)
        self.d_setSpawnPosIndex(spawnPosIndex)

    def getSpawnPosIndex(self):
        return self.spawnPosIndex

    def setAssociatedQuests(self, associatedQuests):
        self.associatedQuests = associatedQuests

    def d_setAssociatedQuests(self, associatedQuests):
        self.sendUpdate('setAssociatedQuests', [associatedQuests])

    def b_setAssociatedQuests(self, associatedQuests):
        self.setAssociatedQuests(associatedQuests)
        self.d_setAssociatedQuests(associatedQuests)

    def getAssociatedQuests(self):
        return self.associatedQuests

    def setActorAnims(self, animSet, notice1, notice2, greet):
        self.actorAnims = [animSet, notice1, notice2, greet]

    def d_setActorAnims(self, animSet, notice1, notice2, greet):
        self.sendUpdate('setActorAnims', [animSet, notice1, notice2, greet])

    def b_setActorAnims(self, animSet, notice1, notice2, greet):
        self.setActorAnims(animSet, notice1, notice2, greet)
        self.d_setActorAnims(animSet, notice1, notice2, greet)

    def getActorAnims(self):
        return self.actorAnims

    def setCollisionMode(self, collisionMode):
        self.collisionMode = collisionMode

    def d_setCollisionMode(self, collisionMode):
        self.sendUpdate('setCollisionMode', [collisionMode])

    def b_setCollisionMode(self, collisionMode):
        self.setCollisionMode(collisionMode)
        self.d_setCollisionMode(collisionMode)

    def getCollisionMode(self):
        return self.collisionMode

    def setInitZ(self, initZ):
        self.initZ = initZ

    def d_setInitZ(self, initZ):
        self.sendUpdate('setInitZ', [initZ])

    def b_setInitZ(self, initZ):
        self.setInitZ(initZ)
        self.d_setInitZ(initZ)

    def getInitZ(self):
        return self.initZ

    def setIsPet(self, isPet):
        self.isPet = isPet

    def d_setIsPet(self, isPet):
        self.sendUpdate('setIsPet', [isPet])

    def b_setIsPet(self, isPet):
        self.setIsPet(isPet)
        self.d_setIsPet(isPet)

    def getIsPet(self):
        return self.isPet
