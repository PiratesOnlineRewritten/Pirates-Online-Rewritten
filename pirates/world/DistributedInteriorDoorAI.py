from pirates.world.DistributedDoorAI import DistributedDoorAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInteriorDoorAI(DistributedDoorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteriorDoorAI')

    def __init__(self, air):
        DistributedDoorAI.__init__(self, air)

        self.interiorDoId = 0
        self.interiorParentId = 0
        self.interiorZoneId = 0
        self.exteriorDoId = 0
        self.exteriorWorldParentId = 0
        self.exteriorWorldZoneId = 0
        self.buildingDoorId = 0

    def setInteriorId(self, interiorDoId, interiorParentId, interiorZoneId):
        self.interiorDoId = interiorDoId
        self.interiorParentId = interiorParentId
        self.interiorZoneId = interiorZoneId

    def d_setInteriorId(self, interiorDoId, interiorParentId, interiorZoneId):
        self.sendUpdate('setInteriorId', [interiorDoId, interiorParentId, interiorZoneId])

    def b_setInteriorId(self, interiorDoId, interiorParentId, interiorZoneId):
        self.setInteriorId(interiorDoId, interiorParentId, interiorZoneId)
        self.d_setInteriorId(interiorDoId, interiorParentId, interiorZoneId)

    def getInteriorId(self):
        return [self.interiorDoId, self.interiorParentId, self.interiorZoneId]

    def setExteriorId(self, exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId):
        self.exteriorDoId = exteriorDoId
        self.exteriorWorldParentId = exteriorWorldParentId
        self.exteriorWorldZoneId = exteriorWorldZoneId

    def d_setExteriorId(self, exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId):
        self.sendUpdate('setExteriorId', [exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId])

    def b_setExteriorId(self, exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId):
        self.setExteriorId(exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId)
        self.d_setExteriorId(exteriorDoId, exteriorWorldParentId, exteriorWorldZoneId)

    def getExteriorId(self):
        return [self.exteriorDoId, self.exteriorWorldParentId, self.exteriorWorldZoneId]

    def setBuildingDoorId(self, buildingDoorId):
        self.buildingDoorId = buildingDoorId

    def d_setBuildingDoorId(self, buildingDoorId):
        self.sendUpdate('setBuildingDoorId', [buildingDoorId])

    def b_setBuildingDoorId(self, buildingDoorId):
        self.setBuildingDoorId(buildingDoorId)
        self.d_setBuildingDoorId(buildingDoorId)

    def getBuildingDoorId(self):
        return self.buildingDoorId
