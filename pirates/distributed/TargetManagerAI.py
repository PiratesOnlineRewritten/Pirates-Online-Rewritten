from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.TargetManagerBase import TargetManagerBase

class TargetManagerAI(DistributedObjectAI, TargetManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('TargetManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        TargetManagerBase.__init__(self)
