from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedCDSteeringWheelAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCDSteeringWheelAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)