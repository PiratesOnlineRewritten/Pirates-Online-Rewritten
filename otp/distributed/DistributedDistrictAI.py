from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedDistrictAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDistrictAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.name = 'NotGiven'
        self.available = 0

    def setName(self, name):
        self.name = name

    def d_setName(self, name):
        self.sendUpdate('setName', [name])

    def b_setName(self, name):
        self.setName(name)
        self.d_setName(name)

    def getName(self):
        return self.name

    def setAvailable(self, available):
        self.available = available

    def d_setAvailable(self, available):
        self.sendUpdate('setAvailable', [available])

    def b_setAvailable(self, available):
        self.setAvailable(available)
        self.d_setAvailable(available)

    def getAvailable(self):
        return self.available
