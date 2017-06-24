from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class LootableAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('LootableAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)