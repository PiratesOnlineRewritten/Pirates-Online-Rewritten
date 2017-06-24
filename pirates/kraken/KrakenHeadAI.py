from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class KrakenHeadAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenHeadAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)