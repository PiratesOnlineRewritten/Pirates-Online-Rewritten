from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class KrakenAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)