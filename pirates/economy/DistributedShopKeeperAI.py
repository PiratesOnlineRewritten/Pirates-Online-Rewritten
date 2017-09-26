from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

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

        if inventory.getGoldInPocket() < 5:
            return

        if not inventory:
            self.notify.warning('Failed to get inventory for avatar %d!' % avatar.doId)
            return

        self.__logShopTransaction(type='music', avatarId=avatar.doId, musicId=music)
        inventory.setGoldInPocket(inventory.getGoldInPocket() - 5)
        self.sendUpdate('playMusic', [music])