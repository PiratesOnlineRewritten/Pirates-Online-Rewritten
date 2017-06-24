from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInvasionDelFuegoAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInvasionDelFuegoAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)