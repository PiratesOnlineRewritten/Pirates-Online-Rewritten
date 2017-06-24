from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBossTownfolkAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBossTownfolkAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)