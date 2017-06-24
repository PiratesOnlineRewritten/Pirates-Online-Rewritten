from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPotionCraftingTableAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPotionCraftingTableAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)