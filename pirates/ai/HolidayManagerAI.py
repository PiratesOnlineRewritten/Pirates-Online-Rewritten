from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class HolidayManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('HolidayManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)