from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBomberZombieAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBomberZombieAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)