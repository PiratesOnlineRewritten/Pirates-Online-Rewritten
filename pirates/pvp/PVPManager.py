from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from pirates.uberdog.UberDogGlobals import *
from pirates.piratesbase import PiratesGlobals

class PVPManager(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPManager')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cr.pvpManager = self

    def delete(self):
        self.ignoreAll()
        if self.cr.pvpManager == self:
            self.cr.pvpManager = None
        DistributedObject.delete(self)
        return

    def sendRequestChallenge(self, challengeeId):
        self.sendUpdate('requestChallenge', [challengeeId])

    def sendAcceptChallenge(self, challengerId):
        self.sendUpdate('acceptChallenge', [challengerId])

    def challengeFrom(self, avId):
        messenger.send(PiratesGlobals.PVPChallengedEvent, [avId])

    def challengeAccepted(self, avId):
        messenger.send(PiratesGlobals.PVPAcceptedEvent, [avId])