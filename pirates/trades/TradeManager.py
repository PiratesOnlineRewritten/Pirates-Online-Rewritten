from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from pirates.uberdog.UberDogGlobals import *

class TradeManager(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('TradeManager')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cr.tradeManager = self

    def delete(self):
        self.ignoreAll()
        if self.cr.tradeManager == self:
            self.cr.tradeManager = None
        DistributedObject.delete(self)
        return

    def sendRequestCreateTrade(self, otherAvatarId):
        self.sendUpdate('requestCreateTrade', [otherAvatarId])

    def rejectCreateTrade(self, otherAvatarId, reasonCode):
        messenger.send('rejectCreateTrade-%s' % (otherAvatarId,), [reasonCode])

    def createTradeResponse(self, otherAvatarId, tradeId):
        self.addInterest(tradeId)