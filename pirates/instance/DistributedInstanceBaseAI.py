from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInstanceBaseAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInstanceBaseAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)