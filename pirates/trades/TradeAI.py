from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class TradeAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TradeAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)