from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.piratesbase import PiratesGlobals
import random

class DistributedGameTableAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameTableAI')
    AVAILABLE_SEATS = 1
    TABLE_AI = 1

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.gameVariation = PiratesGlobals.VILLAGER_TEAM
        self.dealerType = PiratesGlobals.VILLAGER_TEAM
        self.tableType = 1
        self.dealerName = 'Dealer'
        self.aiList = []

    def setTableType(self, type):
        self.tableType = type

    def getTableType(self):
        return self.tableType

    def setGameVariation(self, variant):
        self.gameVariation = variant

    def d_setGameVariation(self, variant):
        self.sendUpdate('setGameVariation', [variant])

    def b_setGameVariant(self, variant):
        self.setGameVariation(variant)
        self.d_setGameVariation(variant)

    def getGameVariation(self):
        return self.gameVariation

    def setDealerName(self, name):
        self.dealerName = name

    def d_setDealerName(self, name):
        self.sendUpdate('setDealerName', [name])

    def b_setDealerName(self, name):
        self.setDealerName(name)
        self.d_setDealerName(name)

    def getDealerName(self):
        return self.dealerName

    def setDealerType(self, type):
        self.dealerType = type

    def d_setDealerType(self, type):
        self.sendUpdate('setDealerType', [type])

    def b_setDealerType(self, type):
        self.setDealerType(type)
        self.d_setDealerType(type)

    def getDealerType(self):
        return self.dealerType

    def setAIList(self, list):
        self.aiList = list

    def d_setAIList(self, list):
        self.sendUpdate('setAIList', [list])

    def b_setAIList(self, list):
        self.setAIList(list)
        self.d_setAIList(list)

    def getAIList(self):
        return self.aiList

    def requestExit(self):
        self.notify.info("Request exit")

    def generatePlayers(self, seats=7, ai=3, available=[PiratesGlobals.VILLAGER_TEAM]):
        players = [0] * seats

        randomGen = random.Random()
        randomGen.seed(self.getUniqueId()) 

        if (ai > seats):
            self.notify.warning("Cannot have more ai then seats! reducing to 5")
            ai = 5

        for i in range(0, ai):
            aiType = randomGen.choice(available)
            players[i] = aiType

        randomGen.shuffle(players)
        self.setAIList(players)