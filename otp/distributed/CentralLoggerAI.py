from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class CentralLoggerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('CentralLoggerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)