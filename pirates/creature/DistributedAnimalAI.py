from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedAnimalAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAnimalAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)