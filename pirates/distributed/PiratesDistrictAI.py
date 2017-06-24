from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PiratesDistrictAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesDistrictAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)