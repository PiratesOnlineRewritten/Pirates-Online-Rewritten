from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class SiegeAnnouncerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('SiegeAnnouncerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)