from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PiratesTimeManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesTimeManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)