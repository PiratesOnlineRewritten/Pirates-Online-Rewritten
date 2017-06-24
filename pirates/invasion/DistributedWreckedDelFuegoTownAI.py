from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedWreckedDelFuegoTownAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWreckedDelFuegoTownAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)