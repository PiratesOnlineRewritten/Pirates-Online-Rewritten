from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInteractivePropAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractivePropAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)