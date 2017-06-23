

class Lootable():

    def __init__(self):
        pass

    def startLooting(self, plunderList, itemsToTake=0, timer=0, autoShow=False, customName=None):
        self.itemsToTake = itemsToTake
        localAvatar.setPlundering(self.getDoId())
        localAvatar.guiMgr.inventoryUIManager.openPlunder(plunderList, self, customName, timer=timer, autoShow=autoShow)

    def stopLooting(self):
        if localAvatar.getPlundering() == self.getDoId():
            localAvatar.setPlundering(0)
            localAvatar.guiMgr.inventoryUIManager.closePlunder()

    def d_requestItem(self, itemInfo):
        self.sendUpdate('requestItem', [itemInfo])

    def d_requestItems(self, items):
        self.sendUpdate('requestItems', [items])

    def subtractItemsToTake(self, itemsToTake):
        self.itemsToTake -= itemsToTake

    def getItemsToTake(self):
        return self.itemsToTake

    def doneTaking(self):
        self.sendUpdate('doneTaking', [])

    def getRating(self):
        return -1

    def getTypeName(self):
        return ''