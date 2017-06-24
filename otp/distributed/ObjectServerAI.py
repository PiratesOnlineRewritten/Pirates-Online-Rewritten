from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class ObjectServerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('ObjectServerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)