from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedCrewMatchManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCrewMatchManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)