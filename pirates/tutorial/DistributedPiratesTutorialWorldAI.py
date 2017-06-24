from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPiratesTutorialWorldAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPiratesTutorialWorldAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)