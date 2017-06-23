from AITradeBase import AITradeBase
from pirates.uberdog.UberDogGlobals import *
from pirates.reputation import ReputationGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.piratesbase import Freebooter

class AITrade(AITradeBase):
    notify = directNotify.newCategory('AITrade')

    def __init__(self, distObj, avatarId=None, inventoryId=None, timeout=4.0):
        AITradeBase.__init__(self, distObj, avatarId, inventoryId, timeout=timeout)

    def giveQuestCategoryLimit(self, addToLimit):
        self.giveCategoryLimit(InventoryCategory.QUESTS, addToLimit)
        self.giveCategoryLimit(InventoryCategory.QUEST_SLOTS, addToLimit)

    def giveNewQuest(self, dClassName, questValues):
        self.giveNewDistObj(InventoryCategory.QUESTS, dClassName, questValues)
        self.takeStack(InventoryType.OpenQuestSlot, 1)

    def giveQuest(self, questDoId):
        self.giveDoId(InventoryCategory.QUESTS, questDoId)
        self.takeStack(InventoryType.OpenQuestSlot, 1)

    def takeQuest(self, questDoId):
        self.takeDoId(InventoryCategory.QUESTS, questDoId)
        self.giveStack(InventoryType.OpenQuestSlot, 1)

    def giveTreasureMapCategoryLimit(self, addToLimit):
        self.giveCategoryLimit(InventoryCategory.TREASURE_MAPS, addToLimit)

    def giveNewTreasureMap(self, dClassName, values=None):
        self.giveNewDistObj(InventoryCategory.TREASURE_MAPS, dClassName, values)

    def giveTreasureMap(self, treasureMapDoID):
        self.giveDoId(InventoryCategory.TREASURE_MAPS, treasureMapDoID)

    def takeTreasureMap(self, treasureMapDoID):
        self.takeDoId(InventoryCategory.TREASURE_MAPS, treasureMapDoID)

    def giveShipCategoryLimit(self, addToLimit):
        self.giveCategoryLimit(InventoryCategory.SHIPS, addToLimit)

    def giveShip(self, shipDoId):
        self.giveDoId(InventoryCategory.SHIPS, shipDoId)

    def takeShip(self, shipDoId):
        self.takeDoId(InventoryCategory.SHIPS, shipDoId)

    def giveWagerCategoryLimit(self, addToLimit):
        self.giveCategoryLimit(InventoryCategory.WAGERS, addToLimit)

    def giveWager(self, wagerDoId):
        self.giveDoId(InventoryCategory.WAGERS, wagerDoId)

    def takeWager(self, wagerDoId):
        self.takeDoId(InventoryCategory.WAGERS, wagerDoId)

    def giveMoneyCategories(self, addToLimit):
        self.giveCategoryLimit(InventoryCategory.MONEY, addToLimit)

    def giveGoldInPocketLimit(self, addToLimit):
        self.giveStackableTypeLimit(InventoryType.GoldInPocket, addToLimit)

    def takeNewPlayerToken(self, amount=1):
        self.takeStack(InventoryType.NewPlayerToken, amount)

    def takeNewShipToken(self, amount=1):
        self.takeStack(InventoryType.NewShipToken, amount)

    def giveNewShipToken(self, amount=1):
        self.giveStack(InventoryType.NewShipToken, amount)

    def giveDinghy(self, amount=1):
        self.giveStack(InventoryType.Dinghy, amount)

    def canTeleportTo(self, av, token):
        inv = av.getInventory()
        if not (inv and inv.isReady()):
            return False
        amt = inv.getStackQuantity(token)
        if amt == 1:
            return True
        else:
            return False

    def grantTeleportToken(self, token):
        if token == TortugaTeleportToken:
            self.giveTortugaTeleportToken()
        elif token == KingsheadTeleportToken:
            self.giveTortugaTeleportToken()
        elif token == PortRoyalTeleportToken:
            self.givePortRoyalTeleportToken()
        elif token == CubaTeleportToken:
            self.giveCubaTeleportToken()
        elif token == PadresDelFuegoTeleportToken:
            self.givePadresDelFuegoTeleportToken()
        else:
            print 'AITrade.grantTeleportToken() encountered an unexpected error'

    def takeTortugaTeleportToken(self, amount=1):
        self.takeStack(InventoryType.TortugaTeleportToken, amount)

    def giveTortugaTeleportToken(self, amount=1):
        self.giveStack(InventoryType.TortugaTeleportToken, amount)

    def takeKingsheadTeleportToken(self, amount=1):
        self.takeStack(InventoryType.KingsheadTeleportToken, amount)

    def giveKingsheadTeleportToken(self, amount=1):
        self.giveStack(InventoryType.KingsheadTeleportToken, amount)

    def takeRavensCoveTeleportToken(self, amount=1):
        self.takeStack(InventoryType.RavensCoveTeleportToken, amount)

    def giveRavensCoveTeleportToken(self, amount=1):
        self.giveStack(InventoryType.RavensCoveTeleportToken, amount)

    def takePortRoyalTeleportToken(self, amount=1):
        self.takeStack(InventoryType.PortRoyalTeleportToken, amount)

    def givePortRoyalTeleportToken(self, amount=1):
        self.giveStack(InventoryType.PortRoyalTeleportToken, amount)

    def takeCubaTeleportToken(self, amount=1):
        self.takeStack(InventoryType.CubaTeleportToken, amount)

    def giveCubaTeleportToken(self, amount=1):
        self.giveStack(InventoryType.CubaTeleportToken, amount)

    def takePadresDelFuegoTeleportToken(self, amount=1):
        self.takeStack(InventoryType.PadresDelFuegoTeleportToken, amount)

    def givePadresDelFuegoTeleportToken(self, amount=1):
        self.giveStack(InventoryType.PadresDelFuegoTeleportToken, amount)

    def takeNewWeaponToken(self, amount=1):
        self.takeStack(InventoryType.NewWeaponToken, amount)

    def giveCutlassWeapon(self, amount=1):
        self.giveStack(InventoryType.CutlassWeapon, amount)

    def givePistolWeapon(self, amount=1):
        self.giveStack(InventoryType.PistolWeapon, amount)

    def giveMusketWeapon(self, amount=1):
        self.giveStack(InventoryType.MusketWeapon, amount)

    def giveDaggersWeapon(self, amount=1):
        self.giveStack(InventoryType.DaggersWeapon, amount)

    def giveGrenadeWeapon(self, amount=1):
        self.giveStack(InventoryType.GrenadeWeapon, amount)

    def giveDollWeapon(self, amount=1):
        self.giveStack(InventoryType.DollWeapon, amount)

    def giveWandWeapon(self, amount=1):
        self.giveStack(InventoryType.WandWeapon, amount)

    def giveKettleWeapon(self, amount=1):
        self.giveStack(InventoryType.KettleWeapon, amount)

    def giveCannonWeapon(self, amount=1):
        self.giveStack(InventoryType.CannonWeapon, amount)

    def giveCutlassTraining(self, amount=1):
        self.giveStack(InventoryType.CutlassToken, amount)

    def givePistolTraining(self, amount=1):
        self.giveStack(InventoryType.PistolToken, amount)

    def giveMusketTraining(self, amount=1):
        self.giveStack(InventoryType.MusketToken, amount)

    def giveDaggersTraining(self, amount=1):
        self.giveStack(InventoryType.DaggerToken, amount)

    def giveGrenadeTraining(self, amount=1):
        self.giveStack(InventoryType.GrenadeToken, amount)

    def giveDollTraining(self, amount=1):
        self.giveStack(InventoryType.DollToken, amount)

    def giveWandTraining(self, amount=1):
        self.giveStack(InventoryType.WandToken, amount)

    def giveKettleTraining(self, amount=1):
        self.giveStack(InventoryType.KettleToken, amount)

    def giveCutlassSlash(self, amount=1):
        self.giveStack(InventoryType.CutlassSlash, amount)

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

    def setAccumulator(self, accumulatorType, quantity):
        setAccumulator = InventoryId.getLimitChange(accumulatorType)
        self.giving.append((setAccumulator, quantity))

    def setReputation(self, category, amount):
        self.setAccumulator(category, amount)

    def takeReputation(self, category, amount):
        self.takeAccumulatorAddition(category, amount)

    def giveMaxHitPoints(self, amount):
        self.giveStack(InventoryType.Hp, amount)

    def giveMaxMojo(self, amount):
        self.giveStack(InventoryType.Mojo, amount)

    def takeShipRepairToken(self, amount=1):
        self.takeStack(InventoryType.ShipRepairToken, amount)

    def giveShipRepairToken(self, amount=1):
        self.giveStack(InventoryType.ShipRepairToken, amount)

    def takePlayerHealToken(self, amount=1):
        self.takeStack(InventoryType.PlayerHealToken, amount)

    def givePlayerHealToken(self, amount=1):
        self.giveStack(InventoryType.PlayerHealToken, amount)

    def takePlayerMojoHealToken(self, amount=1):
        self.takeStack(InventoryType.PlayerHealMojoToken, amount)

    def givePlayerMojoHealToken(self, amount=1):
        self.giveStack(InventoryType.PlayerHealMojoToken, amount)

    def takeTonic(self, tonicId, amount=1):
        self.takeStack(tonicId, amount)

    def takeShipRepairKit(self, amount=1):
        self.takeStack(InventoryType.ShipRepairKit, amount)