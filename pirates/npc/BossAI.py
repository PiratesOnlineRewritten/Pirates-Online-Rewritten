from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class BossAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('BossAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)