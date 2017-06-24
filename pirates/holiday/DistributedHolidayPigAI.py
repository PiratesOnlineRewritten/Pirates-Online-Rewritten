from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedHolidayPigAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHolidayPigAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)