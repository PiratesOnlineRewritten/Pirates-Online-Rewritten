from pandac.PandaModules import *
from direct.distributed import DistributedObject
from direct.distributed.GridChild import GridChild

class DistributedPostInvasionObject(DistributedObject.DistributedObject, GridChild):
    notify = directNotify.newCategory('DistributedWreckedGovernorsMansion')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        GridChild.__init__(self)
        self.postInvasionObjs = []
        self.onFire = False

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.notify.debug('generate')

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)

    def disable(self):
        self.stopBurning()
        self.postInvasionObjs = []
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        DistributedObject.DistributedObject.delete(self)
        GridChild.__init__(self)

    def setOnFire(self, onFire):
        self.onFire = onFire
        if self.onFire:
            self.startBurning()
        else:
            self.stopBurning()

    def startBurning(self):
        pass

    def stopBurning(self):
        pass