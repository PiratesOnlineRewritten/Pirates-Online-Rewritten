from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPirateBandManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPirateBandManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)