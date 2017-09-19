from direct.directnotify import DirectNotifyGlobal
from pirates.invasion.DistributedInvasionObjectAI import DistributedInvasionObjectAI

class DistributedInvasionDelFuegoAI(DistributedInvasionObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInvasionDelFuegoAI')

    MESSAGES = {30: 19, 20: 20, 10: 21, 5: 2, 1: 23}

    def __init__(self, air, holidayId):
        DistributedInvasionObjectAI.__init__(self, air, holidayId)