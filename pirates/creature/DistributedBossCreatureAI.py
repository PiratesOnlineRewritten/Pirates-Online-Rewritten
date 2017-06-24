from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBossCreatureAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossCreatureAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)