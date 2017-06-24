from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PVPManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)