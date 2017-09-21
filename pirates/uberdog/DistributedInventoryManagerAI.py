from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType

class DistributedInventoryManagerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryManagerAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

        self.inventories = {}

    def hasInventory(self, inventoryId):
        return inventoryId in self.inventories

    def addInventory(self, inventory):
        if self.hasInventory(inventory.doId):
            return self.notify.warning('Tried to add an already existing inventory %d!' % inventory.doId)

        self.inventories[inventory.doId] = inventory

    def removeInventory(self, inventory):
        if not self.hasInventory(inventory.doId):
            return self.notify.warning('Tried to remove a non-existant inventory %d!' % inventory.doId)

        del self.inventories[inventory.doId]

    def getInventory(self, avatarId):
        for inventory in self.inventories:

            if inventory.getOwnerId() == avatarId:
                return inventory

        return None

    def requestInventory(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        def queryAvatar(dclass, fields):
            if not dclass or not fields:
                return self.notify.warning('Failed to query avatar %d!' % avatar.doId)

            inventoryId, = fields.get('setInventoryId', (0,))

            if not inventoryId:
                return self.notify.warning('Invalid inventory found for avatar %d!' % avatar.doId)

            self.__sendInventory(avatar, self.inventories.get(inventoryId))

        self.air.dbInterface.queryObject(self.air.dbId, avatar.doId, callback=queryAvatar,
            dclass=self.air.dclassesByName['DistributedPlayerPirateAI'])

    def __sendInventory(self, avatar, inventory):
        if not inventory:
            return self.notify.warning('Failed to retrieve inventory for avatar %d!' % avatar.doId)

        inventory.b_setStackLimit(InventoryType.Hp, avatar.getMaxHp())
        inventory.b_setStackLimit(InventoryType.Mojo, avatar.getMaxMojo())
        inventory.b_setAccumulator(*inventory.getAccumulator(InventoryType.OverallRep))

        inventory.d_requestInventoryComplete()
