from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedIslandAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedIslandAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)