from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedSearchableContainerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSearchableContainerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)