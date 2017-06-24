from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInvasionPortRoyalAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInvasionPortRoyalAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)