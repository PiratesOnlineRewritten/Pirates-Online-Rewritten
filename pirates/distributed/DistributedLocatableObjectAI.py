from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedLocatableAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLocatableAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def requestRegionUpdate(self, todo):
        pass

    def enterAreaSphere(self, todo0, todo1):
        pass

    def leaveAreaSphere(self, todo0, todo1):
        pass

    def d_locationChange(self, location):
        self.sendUpdate('locationChange', [location])