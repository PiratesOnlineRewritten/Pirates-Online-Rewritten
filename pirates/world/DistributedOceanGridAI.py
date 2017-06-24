from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedOceanGridAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedOceanGridAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)