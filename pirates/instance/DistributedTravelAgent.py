from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from pirates.piratesbase import PiratesGlobals

class DistributedTravelAgent(DistributedObjectGlobal):
    notify = directNotify.newCategory('DistributedTravelAgent')

    @report(types=['args'], dConfigParam='dteleport')
    def d_requestTutorialTeleport(self):
        self.sendUpdate('requestTutorialTeleport')

    @report(types=['args'], dConfigParam='dteleport')
    def d_requestWelcomeWorldTeleport(self):
        self.sendUpdate('requestWelcomeWorldTeleport')

    @report(types=['args'], dConfigParam='dteleport')
    def d_requestLoginTeleport(self, shardId=0):
        self.sendUpdate('requestLoginTeleport', [shardId])
