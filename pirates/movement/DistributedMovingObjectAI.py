from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedSmoothNodeAI import DistributedSmoothNodeAI
from pirates.distributed.DistributedTargetableObjectAI import DistributedTargetableObjectAI

class DistributedMovingObjectAI(DistributedSmoothNodeAI, DistributedTargetableObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMovingObjectAI')

    def __init__(self, air):
        DistributedSmoothNodeAI.__init__(self, air)
        DistributedTargetableObjectAI.__init__(self, air)
        self.maxSpeed = 0
        self.startState = ''
        self.aggroRadius = 0
        self.aggroMode = 0

    def setMaxSpeed(self, maxSpeed):
        self.maxSpeed = maxSpeed

    def d_setMaxSpeed(self, maxSpeed):
        self.sendUpdate('setMaxSpeed', [maxSpeed])

    def b_setMaxSpeed(self, maxSpeed):
        self.setMaxSpeed(maxSpeed)
        self.d_setMaxSpeed(maxSpeed)

    def getMaxSpeed(self):
        return self.maxSpeed

    def setStartState(self, startState):
        self.startState = startState

    def d_setStartState(self, startState):
        self.sendUpdate('setStartState', [startState])

    def b_setStartState(self, startState):
        self.setStartState(startState)
        self.d_setStartState(startState)

    def getStartState(self):
        return self.startState

    def setAggroRadius(self, aggroRadius):
        self.aggroRadius = aggroRadius

    def d_setAggroRadius(self, aggroRadius):
        self.sendUpdate('setAggroRadius', [aggroRadius])

    def b_setAggroRadius(self, aggroRadius):
        self.setAggroRadius(aggroRadius)
        self.d_setAggroRadius(aggroRadius)

    def getAggroRadius(self):
        return self.aggroRadius

    def setAggroMode(self, aggroMode):
        self.aggroMode = aggroMode

    def d_setAggroMode(self, aggroMode):
        self.sendUpdate('setAggro', [aggroMode])

    def b_setAggroMode(self, aggroMode):
        self.setAggroMode(aggroMode)
        self.d_setAggroMode(aggroMode)

    def getAggroMode(self):
        return self.aggroMode