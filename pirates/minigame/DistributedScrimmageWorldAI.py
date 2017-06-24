from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedScrimmageWorldAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedScrimmageWorldAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)