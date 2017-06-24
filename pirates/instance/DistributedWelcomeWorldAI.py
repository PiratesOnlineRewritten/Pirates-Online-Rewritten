from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedWelcomeWorldAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWelcomeWorldAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)