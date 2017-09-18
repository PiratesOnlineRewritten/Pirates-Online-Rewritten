from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTravelAgentAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def initiateTeleport(self, avatarId, isTutorial):

        def avatarGenerated(avatar):
            if not avatar:
                return self.notify.warning('Failed to initiate teleport for non-existant avatar!')

            avatar.d_relayTeleportLoc(self.air.districtId, 0, self.air.teleportMgr.doId)

        self.acceptOnce('generate-%d' % avatarId, avatarGenerated)
        self.air.setAI(avatarId, self.air.ourChannel)
