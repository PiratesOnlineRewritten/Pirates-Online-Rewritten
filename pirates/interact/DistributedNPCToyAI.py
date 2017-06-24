from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedNPCToyAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCToyAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)