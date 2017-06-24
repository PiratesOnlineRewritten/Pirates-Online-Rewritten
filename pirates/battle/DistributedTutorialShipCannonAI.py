from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTutorialShipCannonAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTutorialShipCannonAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)