from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBountyHunterAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBountyHunterAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)