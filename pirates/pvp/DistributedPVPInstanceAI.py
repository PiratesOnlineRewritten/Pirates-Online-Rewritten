from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedPVPInstanceAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPVPInstanceAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)