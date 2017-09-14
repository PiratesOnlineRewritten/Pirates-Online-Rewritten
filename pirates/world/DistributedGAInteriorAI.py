from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world.WorldGlobals import *

class DistributedGAInteriorAI(DistributedCartesianGridAI, DistributedGameAreaAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGAInteriorAI')

    def __init__(self, air):
        DistributedCartesianGridAI.__init__(self, air, GAME_AREA_INTERIOR_STARTING_ZONE, GAME_AREA_INTERIOR_GRID_SIZE,
            GAME_AREA_INTERIOR_GRID_RADIUS, GAME_AREA_INTERIOR_CELL_SIZE)

        DistributedGameAreaAI.__init__(self, air)
        self.connectorId = 0

    def delete(self):
        # since our current zone was allocated, we need to free the zone
        # so it can be used for another building interior instance.
        self.air.deallocateZone(self.zoneId)

        DistributedCartesianGridAI.delete(self)
        DistributedGameAreaAI.delete(self)

    def setConnectorId(self, connectorId):
        self.connectorId = connectorId

    def d_setConnectorId(self, connectorId):
        self.sendUpdate('setConnectorId', [connectorId])

    def b_setConnectorId(self, connectorId):
        self.setConnectorId(connectorId)
        self.d_setConnectorId(connectorId)

    def getConnectorId(self):
        return self.connectorId