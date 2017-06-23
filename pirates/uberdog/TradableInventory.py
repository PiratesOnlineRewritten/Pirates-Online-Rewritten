from pirates.uberdog.TradableInventoryBase import TradableInventoryBase, InvItem
from pirates.uberdog.UberDogGlobals import prepareSwitchField, receiveSwitchField, InventoryType
from pirates.inventory.InventoryGlobals import Locations, getEquipRanges, getLocationChangeMsg, getAnyChangeMsg, getCategoryChangeMsg, getCategoryQuantChangeMsg, getOverflowChangeMsg

class TradableInventory(TradableInventoryBase):

    def __init__(self, repository):
        TradableInventoryBase.__init__(self, repository)

    def locatableItem(self, status, item):
        modification = False
        itemFields = InvItem(item[0])
        itemLocation = itemFields.getLocation()
        origStatus = status
        if status == self.STATUS_ITEM_MODIFIED or status == self.STATUS_ITEM_MODIFIED_OVERFLOW:
            if itemFields[self.ITEM_CAT_IDX] == 0:
                status = self.STATUS_ITEM_REMOVED
            elif not self._locatableItems.has_key(itemLocation):
                status = self.STATUS_ITEM_ADDED
        if status == self.STATUS_ITEM_ADDED:
            self._locatableItems[itemLocation] = itemFields
            modification = True
        else:
            if status == self.STATUS_ITEM_REMOVED:
                if self._locatableItems.has_key(itemLocation):
                    del self._locatableItems[itemLocation]
                modification = True
            elif status == self.STATUS_ITEM_MODIFIED or status == self.STATUS_ITEM_MODIFIED_OVERFLOW:
                self._locatableItems.pop(itemLocation, None)
                self._locatableItems[itemLocation] = itemFields
                modification = True
            if modification:
                self.notify.debug('sending inventoryLocation message for %s' % itemLocation)
                messenger.send(getLocationChangeMsg(self.doId), [itemLocation])
                if origStatus == self.STATUS_ITEM_MODIFIED_OVERFLOW:
                    messenger.send(getOverflowChangeMsg(self.doId), [itemLocation])
                if itemFields.getCat():
                    messenger.send(getCategoryChangeMsg(self.doId, itemFields.getCat()), [
                     itemFields.getType()])
                    messenger.send(getCategoryQuantChangeMsg(self.doId, itemFields.getCat()), [
                     itemFields.getCount()])
                messenger.send(getAnyChangeMsg(self.doId))
        return

    def swapItems(self, location1, location2):
        item1 = self._locatableItems.get(location1)
        item2 = self._locatableItems.get(location2)
        item1prepared = (
         (
          0, 0, location1),)
        if item1:
            item1prepared = prepareSwitchField([item1])[0]
        item2prepared = (
         (
          0, 0, location2),)
        if item2:
            item2prepared = prepareSwitchField([item2])[0]
        self.sendUpdate('moveLocatables', [item1prepared, item2prepared])

    def getEquippedWeapons(self, equipped):
        equippedLen = len(equipped)
        weaponRanges = getEquipRanges(InventoryType.ItemTypeWeapon, None)
        for weaponRange in weaponRanges:
            for currEquipSlot in range(weaponRange[0], weaponRange[1] + 1):
                idx = currEquipSlot - weaponRange[0]
                weapon = self._locatableItems.get(currEquipSlot)
                if weapon:
                    if idx < equippedLen:
                        equipped[idx] = weapon.getType()
                    else:
                        self.notify.warning('getEquippedWeapons: invalid range supplied for query %s %s' % (idx, equippedLen))

        return