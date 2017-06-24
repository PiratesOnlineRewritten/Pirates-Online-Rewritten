from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedSteeringWheelAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSteeringWheelAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)