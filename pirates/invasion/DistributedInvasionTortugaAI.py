from direct.directnotify import DirectNotifyGlobal
from pirates.invasion.DistributedInvasionObjectAI import DistributedInvasionObjectAI

class DistributedInvasionTortugaAI(DistributedInvasionObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInvasionTortugaAI')

    MESSAGES = {30: 13, 20: 14, 10: 15, 5: 16, 1: 17}

    def __init__(self, air, holidayId):
        DistributedInvasionObjectAI.__init__(self, air, holidayId)