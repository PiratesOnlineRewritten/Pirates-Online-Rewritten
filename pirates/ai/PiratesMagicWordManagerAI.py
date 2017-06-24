from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PiratesMagicWordManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesMagicWordManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)