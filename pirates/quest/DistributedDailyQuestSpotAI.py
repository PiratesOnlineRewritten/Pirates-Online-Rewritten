from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDailyQuestSpotAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDailyQuestSpotAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)