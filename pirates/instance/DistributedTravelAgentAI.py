from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals

class DistributedTravelAgentAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentAI')

    def __init__(self, air):
        DistributedObjectGlobalAI.__init__(self, air)

    def initiateTeleport(self, avatarId, isTutorial):

        def avatarGenerated(avatar):
            if not avatar:
                self.notify.warning('Cannot initiate teleport for non-existant avatar!')
                return

            avatar.d_relayTeleportLoc(self.air.districtId, 0, self.air.teleportMgr.doId)

        self.acceptOnce('generate-%d' % avatarId, avatarGenerated)
        self.air.setAI(avatarId, self.air.ourChannel)
