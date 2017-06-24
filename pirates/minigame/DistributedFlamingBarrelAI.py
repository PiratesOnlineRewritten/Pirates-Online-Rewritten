from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedFlamingBarrelAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFlamingBarrelAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)