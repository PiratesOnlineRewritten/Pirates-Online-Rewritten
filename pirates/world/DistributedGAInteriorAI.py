from direct.distributed.DistributedCartesianGridAI import DistributedCartesianGridAI
from direct.directnotify import DirectNotifyGlobal
from pirates.world.DistributedGameAreaAI import DistributedGameAreaAI
from pirates.world.InteriorAreaBuilderAI import InteriorAreaBuilderAI
from pirates.world.WorldGlobals import *

class DistributedGAInteriorAI(DistributedCartesianGridAI, DistributedGameAreaAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGAInteriorAI')

    def __init__(self, air):
        DistributedCartesianGridAI.__init__(self, air, GAME_AREA_INTERIOR_STARTING_ZONE, GAME_AREA_INTERIOR_GRID_SIZE,
            GAME_AREA_INTERIOR_GRID_RADIUS, GAME_AREA_INTERIOR_CELL_SIZE)

        DistributedGameAreaAI.__init__(self, air)

        self.connectorId = 0
        self.interiorDoor = None
        self.exteriorDoor = None
        self.builder = InteriorAreaBuilderAI(air, self)

    def setConnectorId(self, connectorId):
        self.connectorId = connectorId

    def d_setConnectorId(self, connectorId):
        self.sendUpdate('setConnectorId', [connectorId])

    def b_setConnectorId(self, connectorId):
        self.setConnectorId(connectorId)
        self.d_setConnectorId(connectorId)

    def getConnectorId(self):
        return self.connectorId

    def setInteriorDoor(self, interiorDoor):
        self.interiorDoor = interiorDoor

    def getInteriorDoor(self):
        return self.interiorDoor

    def setExteriorDoor(self, exteriorDoor):
        self.exteriorDoor = exteriorDoor

    def getExteriorDoor(self):
        return self.exteriorDoor

    def delete(self):
        self.air.deallocateZone(self.zoneId)

        DistributedCartesianGridAI.delete(self)
        DistributedGameAreaAI.delete(self)
