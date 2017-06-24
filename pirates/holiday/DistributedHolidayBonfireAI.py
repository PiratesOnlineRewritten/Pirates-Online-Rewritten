from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedHolidayBonfireAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHolidayBonfireAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)