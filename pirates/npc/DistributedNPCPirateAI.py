from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedNPCPirateAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCPirateAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)