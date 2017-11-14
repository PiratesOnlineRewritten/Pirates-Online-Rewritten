from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI

class DistributedBlackjackTableAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackjackTableAI')
    AVAILABLE_SEATS = 7
    TABLE_AI = 3

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self.pendingStakes = 0
        self.activeStakes = 0
        self.runningStakes = 0
        self.betMultiplier = 1
        self.hands = []
        self.chipsCount = [0] * self.AVAILABLE_SEATS

    def setPendingStakes(self, pending):
        self.pendingStakes = pending

    def d_setPendingStakes(self, pending):
        self.sendUpdate('setPendingStakes', [pending])

    def b_setPendingStakes(self, pending):
        self.setPendingStakes(pending)
        self.d_setPendingStakes(pending)

    def getPendingStakes(self):
        return self.pendingStakes

    def setActiveStakes(self, stakes):
        self.activeStakes = stakes

    def d_setActiveStakes(self, stakes):
        self.sendUpdate('setActiveStakes', [stakes])

    def b_setActiveStakes(self, stakes):
        self.setActiveStakes(stakes)
        self.d_setActiveStakes(stakes)

    def getActiveStakes(self):
        return self.activeStakes

    def setTableState(self, hands, chipsCount):
        self.hands = hands
        self.chipsCount = chipsCount

    def d_setTableState(self, hands, chipsCount):
        self.sendUpdate('setTableState', [hands, chipsCount])

    def b_setTableState(self, hands, chipsCount):
        self.setTableState(hands, chipsCount)
        self.d_setTableState(hands, chipsCount)

    def getTableState(self):
        return (self.hands, self.chipsCount)

    def setBetMultiplier(self, multiplier):
        self.betMultiplier = multiplier

    def getBetMultiplier(self):
        return self.betMultiplier