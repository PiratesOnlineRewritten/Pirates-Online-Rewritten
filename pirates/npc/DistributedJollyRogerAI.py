from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedJollyRogerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedJollyRogerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)