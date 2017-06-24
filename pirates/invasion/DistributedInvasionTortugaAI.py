from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInvasionTortugaAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInvasionTortugaAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)