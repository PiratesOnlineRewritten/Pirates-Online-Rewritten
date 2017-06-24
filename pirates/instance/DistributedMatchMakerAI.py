from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedMatchMakerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMatchMakerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)