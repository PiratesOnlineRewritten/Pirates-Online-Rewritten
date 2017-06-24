from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class TestObjectAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TestObjectAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)