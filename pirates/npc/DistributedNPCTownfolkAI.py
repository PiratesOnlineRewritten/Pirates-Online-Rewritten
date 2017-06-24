from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedNPCTownfolkAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCTownfolkAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)