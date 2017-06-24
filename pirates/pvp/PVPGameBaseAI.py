from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PVPGameBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGameBaseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)