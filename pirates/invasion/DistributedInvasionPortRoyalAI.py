from direct.directnotify import DirectNotifyGlobal
from pirates.invasion.DistributedInvasionObjectAI import DistributedInvasionObjectAI

class DistributedInvasionPortRoyalAI(DistributedInvasionObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInvasionPortRoyalAI')

    MESSAGES = {30: 8, 20: 9, 10: 10, 5: 11, 1: 12}

    def __init__(self, air, holidayId):
        DistributedInvasionObjectAI.__init__(self, air, holidayId)