from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal

class DistributedTravelAgentAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def initiateTeleport(self, avatarId, isTutorial):

        def handleGenerated(avatar):
            if not avatar:
                return

            avatar.d_relayTeleportLoc(self.air.districtId, 0, 0)

        self.acceptOnce('generate-%d' % avatarId, handleGenerated)
        self.air.setAI(avatarId, self.air.ourChannel)
