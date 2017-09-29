from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from otp.uberdog.RejectCode import RejectCode
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryId
from pirates.uberdog import UberDogGlobals
from pirates.economy import EconomyGlobals
import cPickle

class DistributedShopKeeperAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShopKeeperAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def __reverseSwitchStatement(self, values):
        ready = []
        for value in values:
            ready.append(cPickle.loads(value[0]))
        return ready

    def requestMusic(self, music):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)

        if not inventory:
            self.notify.warning('Failed to get inventory for avatar %d!' % avatar.doId)
            return

        foundSong = inventory.getStack(music)
        if not foundSong and not (self.air.holidayMgr.isHolidayActive(21) and music in InventoryType.WinterHolidaySongs):
            self.air.logPotentialHacker(
                message='Attempted to play a song they dont have',
                musicId=music)

            return

        if inventory.getGoldInPocket() < 5:
            
            self.air.logPotentialHacker(
                message='Attempted to make sale without sufficent gold',
                pirateGold=inventory.getGoldInPocket(),
                requiredGold=requiredGold)

            return

        self.air.writeServerEvent('shop-transaction',
            transactionType='music',
            avatarId=avatar.doId,
            musicId=music)

        inventory.setGoldInPocket(inventory.getGoldInPocket() - 5)
        self.sendUpdate('playMusic', [music])

    def requestMakeSale(self, buying, selling):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)

        if not inventory:
            self.notify.warning('Failed to get inventory for avatar %d!' % avatar.doId)
            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])
            return

        buying = self.__reverseSwitchStatement(buying)
        selling = self.__reverseSwitchStatement(selling)

        for buy in buying:
            item = buy[0]
            quantity = buy[1]

            cost = EconomyGlobals.getItemCost(item)
            if not cost:
                self.notify.warning('Unable to locate price for item: %s!' % item)
                self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])

            if not inventory.getGoldInPocket() >= cost:
                self.air.logPotentialHacker(
                    message='Attempted to make sale without sufficent gold',
                    pirateGold=inventory.getGoldInPocket(),
                    requiredGold=cost)

                self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [0])

                return

            itemType = InventoryId.LOCATABLE
            resultCode = 0
            if not UberDogGlobals.isLocatable(item):
                itemType == InventoryId.STACK

            if itemType == InventoryId.LOCATABLE:
                self.notify.warning('Attempted to make purchase for unsupported item type: LOCATABLE')
                self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [RejectCode.TIMEOUT])
                return

            elif itemType == InventoryId.STACK:
                pass


            if resultCode == 0:

                self.air.writeServerEvent('shop-transaction',
                    transactionType='generic',
                    buying=buying,
                    selling=selling)

                inventory.setGoldInPocket(inventory.getGoldInPocket() - cost)

            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [resultCode])

        for sell in selling:
            pass #TODO          

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
                pirateGold=inventory.getGoldInPocket(),
                requiredGold=requiredGold)

            self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [0])
            return

        resultCode = 0

        #TODO check if there is an open slot
        openSlot = False
        if not openSlot:
            resultCode = RejectCode.OVERFLOW

        if resultCode == 0:

            self.air.writeServerEvent('shop-transaction',
                transactionType='ship',
                shipId=shipId,
                name=names)

            inventory.setGoldInPocket(inventory.getGoldInPocket() - requiredGold)

            #TODO issue ship

        self.sendUpdateToAvatarId(avatar.doId, 'makeSaleResponse', [resultCode])