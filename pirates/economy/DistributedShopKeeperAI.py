from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from otp.uberdog.RejectCode import RejectCode
from pirates.economy import EconomyGlobals

class DistributedShopKeeperAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShopKeeperAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def __logShopTransaction(self, type, avatar, **kwargs):
        self.notify.debug('ShopTransaction: transactionType: %s avatarId: %s args: %s' % (type, avatar.doId, str(kwargs)))
        self.air.writeServerEvent('shop-transaction',
            transactionType=type,
            avatarId=avatar.doId,
            **kwargs)

    def requestMusic(self, music):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)

        if not inventory:
            self.notify.warning('Failed to get inventory for avatar %d!' % avatar.doId)
            return

        if inventory.getGoldInPocket() < 5:
            
            self.air.logPotentialHacker(
                message='Attempted to make sale without sufficent gold',
                accountId=self.air.getAccountIdFromSender(),
                pirateGold=inventory.getGoldInPocket(),
                requiredGold=requiredGold)

            return

        self.__logShopTransaction(type='music', avatar=avatar.doId, musicId=music)
        inventory.setGoldInPocket(inventory.getGoldInPocket() - 5)
        self.sendUpdate('playMusic', [music])

    def requestMakeShipSale(self, buying, selling, names):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)

        if not inventory:
            self.notify.warning('Failed to get inventory for avatar %d!' % avatar.doId)
            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])
            return

        if len(buying) == 0:
            self.notify.warning('Failed to process ship sale; Received an empty list!')
            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])
            return

        itemData = buying[0]
        shipId = itemData[0]
        requiredGold = EconomyGlobals.getItemCost(shipId)
        if requiredGold > inventory.getGoldInPocket():

            self.air.logPotentialHacker(
                message='Attempted to make sale without sufficent gold',
                accountId=self.air.getAccountIdFromSender(),
                pirateGold=inventory.getGoldInPocket(),
                requiredGold=requiredGold)

            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [0])
            return

        resultCode = 0

        #TODO check if there is an open slot

        if resultCode == 0:
            self.__logShopTransaction(type='ship', avatar=avatar.doId, shipId=shipId, name=names)
            inventory.setGoldInPocket(inventory.getGoldInPocket() - requiredGold)

            #TODO issue ship

        self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [resultCode])