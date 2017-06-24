from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTutorialSimpleShipAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTutorialSimpleShipAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)