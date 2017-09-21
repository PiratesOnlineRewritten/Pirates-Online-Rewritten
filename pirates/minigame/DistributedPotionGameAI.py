from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryType
import PotionRecipeData
import PotionGlobals

class DistributedPotionGameAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPotionGameAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.colorSet = 0
        self.table = None
        self.avatar = None

        self.__workingRecipe = -1
        self.__numIngredients = 0

    def setColorSet(self, colorSet):
        self.colorSet = colorSet

    def getColorSet(self):
        return self.colorSet

    def setTable(self, table):
        self.table = table

    def getTable(self):
        return self.table

    def setAvatar(self, avatar):
        self.avatar = avatar

    def getAvatar(self):
        return self.avatar

    def __verifySender(self):
        sender = self.air.getAvatarIdFromSender()
        verified = sender == self.avatar.doId
        if not verified:
            self.notify.warning('Received update from an unexpected avatar (%d); Expected %d' % (sender, avatar.doId))

            self.air.writeServerEvent('suspicious-event',
                message='Received update from an unexpected avatar while playing Potions.',
                targetAvId=sender,
                expected=self.avatar.doId)

        return verified

    def completeRecipe(self, recipeId, clearNewFlag):
        if not self.__verifySender():
            return

        if self.__workingRecipe == -1:

            if not PotionRecipeData.getPotionData(recipeId):
                self.notify.warning('Received complete Recipe for an invalid recipe %d!' % recipeId)

                self.air.writeServerEvent('suspicious-event',
                    message='Received complete Recipe for an invalid recipe.',
                    targetAvId=self.avatar.doId,
                    recipeId=recipeId)

                return

            self.__workingRecipe = recipeId

        # Is this still the same recipe?
        elif self.__workingRecipe != recipeId:
            self.notify.warning('Attempted to complete recipe that has not been started!')

            self.air.writeServerEvent('suspicious-event',
                message='Attempted to complete recipe that has not been started!',
                targetAvId=self.avatar.doId,
                recipeId=recipeId)

            return

        self.__numIngredients += 1

        if self.__numIngredients >= PotionRecipeData.getNumIngredients(recipeId):

            # Perform disabled potion sanity check
            if PotionRecipeData.getDisabled(recipeId):
                self.notify.warning('%d completed a disabled potion recipe! (%d)' % (self.avatar.doId, recipeId))

                self.air.writeServerEvent('suspicious-event',
                    message='Attempted to complete a disabled recipe!',
                    targetAvId=self.avatar.doId,
                    recipeId=recipeId)

                self.reset()

                return

            self.notify.debug('%s completed recipe %d!' % (self.avatar.doId, recipeId))

            inventory = self.air.inventoryManager.getInventory(self.avatar.doId)
            success = True
            if not inventory:
                self.notify.warning('Failed to get inventory for avatar %d!' % avatar.doId)

                # Log failure for Game Masters 
                self.air.writeServerEvent('recipe-error',
                    message='Failed to give player potion game rewards.',
                    targetAvId=self.avatar.doId,
                    recipeId=recipeId,
                    rep=rep,
                    potionId=potionId)

                self.reset()

                return

            potionRep = inventory.getAccumulator(InventoryType.PotionsRep)[1] if inventory.getAccumulator(InventoryType.PotionsRep) != None else 1

            # Perform potion level sanity check
            requiredLevel = PotionRecipeData.getPotionData(recipeId)['level']
            if potionRep < requiredLevel:
                self.notify.warning('%d completed a potion they are not a high enough level for! (%d); Requires %s. Has %s' % (self.avatar.doId, recipeId, requiredLevel, potionRep))

                self.air.writeServerEvent('suspicious-event',
                    message='Attempted to complete a potion they are not a high enough level for!',
                    targetAvId=self.avatar.doId,
                    recipeId=recipeId,
                    level=potionRep,
                    required=requiredLevel)

                self.reset()

                return

            # Set have made flag
            if clearNewFlag:
                madeType = PotionGlobals.getPotionHaveMadeFlag(recipeId)
                madeCounter = inventory.getStack(madeType)[1] if inventory.getStack(madeType) != None else 0
                madeCounter += 1
                inventory.b_setStack(madeType, madeCounter)

            # Aware XP
            rep = PotionGlobals.getPotionBuffXP(recipeId)
            potionId = PotionGlobals.potionBuffIdToInventoryTypeId(recipeId)
            inventory.b_setAccumulator(InventoryType.PotionsRep, potionRep + rep)

            #TODO give out potion
            self.notify.warning('TODO: Implement potion rewards; PotionId: %d!' % potionId)

            self.reset()

    def claimXPBonus(self, bonusLevel):
        if not self.__verifySender():
            return

        print 'BONUS: %s' % bonusLevel

    def completeSurvival(self, ingredients, tiles):
        if not self.__verifySender():
            return

        print 'INGREDIENTS %s TILES %s' % (ingredients, tiles)

    def reset(self):
        if not self.__verifySender():
            return

        self.__workingRecipe = -1
        self.__numIngredients = 0

    def finish(self):
        if not self.__verifySender():
            return

        self.reset()