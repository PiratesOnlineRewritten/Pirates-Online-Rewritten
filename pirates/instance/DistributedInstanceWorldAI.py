from pirates.instance.DistributedInstanceBaseAI import DistributedInstanceBaseAI
from direct.directnotify import DirectNotifyGlobal
from pirates.world import WorldGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.world.DistributedOceanGridAI import DistributedOceanGridAI

class DistributedInstanceWorldAI(DistributedInstanceBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInstanceWorldAI')

    def __init__(self, air):
        DistributedInstanceBaseAI.__init__(self, air)

        self.fileName = WorldGlobals.PiratesWorldSceneFileBase
        self.type = PiratesGlobals.INSTANCE_GENERIC

    def generate(self):
        DistributedInstanceBaseAI.generate(self)

        self.oceanGrid = DistributedOceanGridAI(self.air)
        self.generateChildWithRequired(self.oceanGrid, self.oceanGrid.startingZone)
