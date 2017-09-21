from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryType
import PotionRecipeData
import PotionGlobals

class DistributedPotionGameAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPotionGameAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.table = None
        self.avatar = None

        self.__workingRecipe = -1
        self.__numIngredients = 0

    def getColorSet(self):
        return 0

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
                targetAvId=avatar.doId,
                expected=avatar.doId)

        return verified

    def completeRecipe(self, recipeId, clearNewFlag):
        if not self.__verifySender():
            return

        if self.__workingRecipe == -1:

            if not self.recipes.get(recipeId):
                self.notify.warning('Received complete Recipe for an invalid recipe %d!' % recipeId)

                self.air.writeServerEvent('suspicious-event',
                    message='Received complete Recipe for an invalid recipe.',
                    targetAvId=avatar.doId,
                    recipeId=recipeId)

                return

            self.__workingRecipe = recipeId

        elif self.__workingRecipe != recipeId:
            self.notify.warning('Attempted to complete recipe that has not been started!')

            self.air.writeServerEvent('suspicious-event',
                message='Attempted to complete recipe that has not been started!',
                targetAvId=avatar.doId,
                recipeId=recipeId)

            return

        self.__numIngredients += 1
        recipeData = PotionRecipeData.get(recipeId)

        if self.__numIngredients >= len(recipeData['ingredients']):
            self.notify.debug('%s completed recipe %d!' % (self.avatar.doId, recipeId))


            inventory = self.air.inventoryManager.getInventory(self.avatar.doId)
            success = True
            if not inventory:
                self.notify.warning('Failed to get inventory for avatar %d!' % avatar.doId)
                success = False

            rep = PotionGlobals.getPotionBuffXP(recipeId) + 25

            if not success:

                # Log failure for Game Masters 
                self.air.writeServerEvent('recipe-error',
                    message='Failed to give player potion game rewards.',
                    targetAvId=avatar.doId,
                    recipeId=recipeId,
                    rep=rep,
                    potionId=potionId)

                self.reset()

                return 

            #TODO give out potion

            inventory.b_setAccumulator(InventoryType.PotionsRep, inventory.getAccumulator(InventoryType.PotionsRep)[1] + rep)

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