from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class TargetManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TargetManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)