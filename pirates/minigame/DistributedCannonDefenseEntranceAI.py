from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedCannonDefenseEntranceAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCannonDefenseEntranceAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)