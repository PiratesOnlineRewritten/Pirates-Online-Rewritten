from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedVoodooZombieAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedVoodooZombieAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)