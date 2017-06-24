from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class Distributed7StudTableAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('Distributed7StudTableAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)