from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBossVoodooZombieAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossVoodooZombieAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)