from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedBlackjackTableAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBlackjackTableAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)