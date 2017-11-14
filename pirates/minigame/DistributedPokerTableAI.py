from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.minigame import TableGlobals

class DistributedPokerTableAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPokerTableAI')

    AVAILABLE_SEATS = 7
    TABLE_AI = 3

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self.potSize = 0
        self.anteList = []
        self.tableState = (0, 0, [], [], [], [0, 0, 0, 0, 0, 0, 0, 0])
        self.setTableType(TableGlobals.CARD_TABLE)

    def setGameType(self, gameType):
        self.gameType = gameType

    def getGameType(self):
        return self.gameType

    def setBetMultiplier(self, multiplier):
        self.betMultiplier = multiplier

    def d_setBetMultiplier(self, multiplier):
        self.sendUpdate('setBetMultiplier', [multiplier])

    def b_setBetMultiplier(self, multiplier):
        self.setBetMultiplier(multiplier)
        self.d_setBetMultiplier(multiplier)

    def getBetMultiplier(self):
        return self.betMultiplier

    def setAnteList(self, list):
        self.anteList = list

    def d_setAnteList(self, list):
        self.sendUpdate('setAnteList', [list])

    def b_setAnteList(self, list):
        self.setAnteList(list)
        self.d_setAnteList(list)

    def getAnteList(self):
        return self.anteList

    def setTableState(self, round, buttonSeat, communityCards, playerHands, totalWinningsArray, chipsCount):
        self.tableState = (round, buttonSeat, communityCards, playerHands, totalWinningsArray, chipsCount)

    def getTableState(self):
        return self.tableState

    def setPotSize(self, potSize):
        self.potSize = potSize

    def d_setPotSize(self, potSize):
        self.sendUpdate('setPotSize', [potSize])

    def b_setPotSize(self, potSize):
        self.setPotSize(potSize)
        self.d_setPotSize(potSize)

    def getPotSize(self):
        return self.potSize