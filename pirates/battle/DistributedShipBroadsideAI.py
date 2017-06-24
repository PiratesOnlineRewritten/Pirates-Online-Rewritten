from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedShipBroadsideAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipBroadsideAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)