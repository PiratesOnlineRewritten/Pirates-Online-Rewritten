from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal
from pirates.world.WorldGlobals import *
from pirates.piratesbase.UniqueIdManager import UniqueIdManager

class DistributedOceanGridAI(DistributedCartesianGridAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedOceanGridAI')

    def __init__(self, air):
        DistributedCartesianGridAI.__init__(self, air, OCEAN_GRID_STARTING_ZONE, OCEAN_GRID_SIZE,
            OCEAN_GRID_RADIUS, OCEAN_CELL_SIZE)

        self.uidMgr = UniqueIdManager(self.air)

    def generateChildWithRequired(self, do, zoneId, optionalFields=[]):
        do.generateWithRequiredAndId(self.air.allocateChannel(), self.doId, zoneId, optionalFields)