from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedRavenAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRavenAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)