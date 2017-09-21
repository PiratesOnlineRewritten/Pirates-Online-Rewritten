from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryType

class DistributedPotionGameAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPotionGameAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.table = None
        self.avatar = None

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
