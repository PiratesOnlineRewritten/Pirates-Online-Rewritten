from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPiratesTutorialAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPiratesTutorialAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)