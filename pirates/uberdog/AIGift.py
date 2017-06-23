from AITradeBase import AITradeBase
from pirates.uberdog.UberDogGlobals import *
from pirates.reputation import ReputationGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import Freebooter

class AIGift(AITradeBase):
    notify = directNotify.newCategory('AIGift')

    def __init__(self, distObj, giftOrigin, fromId, avatarId=None, inventoryId=None, timeout=4.0):
        self.giftOrigin = giftOrigin
        self.fromId = fromId
        AITradeBase.__init__(self, distObj, avatarId, inventoryId, timeout=4.0)

    def _checkRules(self, givingLimitChanges, givingStacks, givingAccumulators, givingDoIds, givingLocatable, takingLimitChanges, takingStacks, takingAccumulators, takingDoIds, takingLocatable):
        pass

    def giveCategoryLimit(self, category, addToLimit):
        pass

    def takeDoId(self, category, doId):
        pass

    def takeStack(self, stackType, quantity):
        pass

    def takeGoldInPocket(self, amount):
        pass

    def giveNewQuest(self, dClassName, questValues):
        self.giveNewDistObj(InventoryCategory.QUESTS, dClassName, questValues)
        self.takeStack(InventoryType.OpenQuestSlot, 1)

    def giveQuest(self, questDoId):
        self.giveDoId(InventoryCategory.QUESTS, questDoId)
        self.takeStack(InventoryType.OpenQuestSlot, 1)

    def giveNewTreasureMap(self, dClassName, values=None):
        self.giveNewDistObj(InventoryCategory.TREASURE_MAPS, dClassName, values)

    def giveTreasureMap(self, treasureMapDoID):
        self.giveDoId(InventoryCategory.TREASURE_MAPS, treasureMapDoID)

    def givePlayingCard(self, card):
        self.giveStack(card, 1)

    def giveReputation(self, category, amount):
        if self.avatarId:
            av = self.air.doId2do.get(self.avatarId)
            if av:
                inv = av.getInventory()
                avExpMult = av.getExpMult()
                amount = int(avExpMult * amount)
                if inv:
                    if category == InventoryType.OverallRep:
                        curLevel = av.getLevel()
                        if Freebooter.getPaidStatusAI(self.avatarId):
                            levelCap = ReputationGlobals.GlobalLevelCap
                        else:
                            levelCap = Freebooter.FreeOverallLevelCap
                        if amount > 0 and curLevel < levelCap:
                            curRepTotal = inv.getAccumulator(InventoryType.OverallRep)
                            newLevel, left = ReputationGlobals.getLevelFromTotalReputation(InventoryType.OverallRep, curRepTotal + amount)
                            if newLevel >= levelCap:
                                amount = max(0, amount - left)
                            self.giveAccumulatorAddition(category, amount)
                    elif category == InventoryType.GeneralRep:
                        self.giveAccumulatorAddition(category, amount)
                    else:
                        if Freebooter.getPaidStatusAI(self.avatarId):
                            if category in [InventoryType.PotionsRep, InventoryType.FishingRep]:
                                levelCap = ReputationGlobals.MinigameLevelCap
                            else:
                                levelCap = ReputationGlobals.LevelCap
                        else:
                            levelCap = Freebooter.FreeLevelCap
                        repAmt = inv.getAccumulator(category)
                        curLevel, curLeft = ReputationGlobals.getLevelFromTotalReputation(category, repAmt)
                        if curLevel >= levelCap:
                            amount = 0
                        expLevel, left = ReputationGlobals.getLevelFromTotalReputation(category, repAmt + amount)
                        if expLevel >= levelCap and curLevel < levelCap:
                            amount = max(0, amount - left)
                        self.giveAccumulatorAddition(category, amount)

    def giveShip(self, shipDoId):
        self.giveDoId(InventoryCategory.SHIPS, shipDoId)

    def getOrigin(self):
        return self.giftOrigin