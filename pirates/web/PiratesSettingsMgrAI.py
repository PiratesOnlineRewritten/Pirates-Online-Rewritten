from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PiratesSettingsMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesSettingsMgrAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)