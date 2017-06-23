from direct.distributed import DistributedObjectOV
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from otp.otpbase import OTPLocalizer

class DistributedBandMemberOV(DistributedObjectOV.DistributedObjectOV):
    notify = directNotify.newCategory('PirateBand')

    def __init__(self, cr):
        DistributedObjectOV.DistributedObjectOV.__init__(self, cr)
        base.localAvatar.bandMember = self

    def delete(self):
        if base.localAvatar.bandMember == self:
            base.localAvatar.bandMember = None
        DistributedObjectOV.DistributedObjectOV.delete(self)
        return

    def sendTalk(self, fromAV, fromAC, avatarName, message, mods, flags):
        self.sendUpdate('setTalk', [0, 0, '', message, [], 0])

    def d_setSpeedChat(self, msgIndex):
        self.sendUpdate('setSpeedChat', [base.localAvatar.getDoId(), msgIndex])

    def b_setSpeedChat(self, msgIndex):
        localObj = self.cr.doId2do.get(self.doId, None)
        if localObj is not None:
            localObj.setSpeedChat(base.localAvatar.getDoId(), msgIndex)
        self.d_setSpeedChat(msgIndex)
        return

    def d_setSCQuestChat(self, questInt, msgType, taskNum):
        self.sendUpdate('setSCQuestChat', [base.localAvatar.getDoId(), questInt, msgType, taskNum])

    def b_setSCQuestChat(self, questInt, msgType, taskNum):
        localObj = self.cr.doId2do.get(self.doId, None)
        if localObj is not None:
            localObj.setSCQuestChat(base.localAvatar.getDoId(), questInt, msgType, taskNum)
        self.d_setSCQuestChat(questInt, msgType, taskNum)
        return

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def teleportQuery(self, requesterId, requesterGuildId, requesterShardId):
        bandMgr, bandId = localAvatar.getBandId() or (0, 0)
        self.cr.teleportMgr.handleAvatarTeleportQuery(requesterId, bandMgr, bandId, requesterGuildId, requesterShardId)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def teleportResponse(self, responderId, available, shardId, instanceDoId, areaDoId):
        self.cr.teleportMgr.handleAvatarTeleportResponse(responderId, available, shardId, instanceDoId, areaDoId)