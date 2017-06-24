from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedKillerGhostAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedKillerGhostAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)