from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPotionCraftingTableAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPotionCraftingTableAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)