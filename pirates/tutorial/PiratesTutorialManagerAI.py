from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PiratesTutorialManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesTutorialManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)