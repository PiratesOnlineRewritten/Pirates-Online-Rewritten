from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedTravelAgentUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTravelAgentUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def requestTutorialTeleport(self):
        self.d_initiateTeleport(self.air.getAvatarIdFromSender(), isTutorial=True)

    def requestWelcomeWorldTeleport(self):
        self.d_initiateTeleport(self.air.getAvatarIdFromSender())

    def requestLoginTeleport(self, shardId):
        self.d_initiateTeleport(self.air.getAvatarIdFromSender(), shardId=shardId)

    def d_initiateTeleport(self, avatarId, isTutorial=False, shardId=None):
        if not avatarId:
            self.notify.warning('Cannot initiate teleport for a non-existant avatar from %d!' % self.air.getMsgSender())
            return
 
        if not shardId:
            self.sendUpdate('initiateTeleport', [avatarId, isTutorial])
        else:
            self.sendUpdateToChannel(shardId, 'initiateTeleport', [avatarId, isTutorial])
