from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDefendWorldAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDefendWorldAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)