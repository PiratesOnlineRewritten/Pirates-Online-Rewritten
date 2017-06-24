from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedWreckedFaithfulBrideAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWreckedFaithfulBrideAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)