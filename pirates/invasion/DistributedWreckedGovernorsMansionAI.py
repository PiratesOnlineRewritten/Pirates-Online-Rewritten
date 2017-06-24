from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedWreckedGovernorsMansionAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWreckedGovernorsMansionAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)