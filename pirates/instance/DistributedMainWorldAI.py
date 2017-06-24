from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedMainWorldAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMainWorldAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)