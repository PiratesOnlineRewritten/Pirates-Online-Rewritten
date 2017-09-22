from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.world.DistributedDoorAI import DistributedDoorAI

class DistributedBuildingDoorAI(DistributedDoorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuildingDoorAI')

    def __init__(self, air):
        DistributedDoorAI.__init__(self, air)
        self.interiorDoId = 0
        self.interiorUid = ''
        self.interiorWorldParentId = 0
        self.interiorWorldZoneId = 0

    def setInteriorId(self, interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId):
        self.interiorDoId = interiorDoId
        self.interiorUid = interiorUid
        self.interiorWorldParentId = interiorWorldParentId
        self.interiorWorldZoneId = interiorWorldZoneId

    def d_setInteriorId(self, interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId):
        self.sendUpdate('setInteriorId', [interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId])

    def b_setInteriorId(self, interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId):
        self.setInteriorId(interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId)
        self.d_setInteriorId(interiorDoId, interiorUid, interiorWorldParentId, interiorWorldZoneId)

    def getInteriorId(self):
        return [self.interiorDoId, self.interiorUid, self.interiorWorldParentId, self.interiorWorldZoneId]

    def requestPrivateInteriorInstance(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        self.sendUpdateToAvatarId(avatar.doId, 'setPrivateInteriorInstance', [self.interiorWorldParentId, self.interiorWorldZoneId,
            self.interiorDoId, True])

        avatar.b_setLocation(self.interiorDoId, self.interiorWorldZoneId)
