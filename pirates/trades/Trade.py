from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from pirates.uberdog.UberDogGlobals import *
from pirates.piratesbase import PiratesGlobals

class Trade(DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('Trade')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.firstAvatarId = None
        self.firstAvatarStatus = 0
        self.firstAvatarGiving = []
        self.secondAvatarId = None
        self.secondAvatarStatus = 0
        self.secondAvatarGiving = []
        return

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        messenger.send(PiratesGlobals.TradeIncomingEvent, [self])

    def disable(self):
        DistributedObject.disable(self)
        messenger.send(PiratesGlobals.TradeFinishedEvent, [self])

    def tradeCompleted(self):
        messenger.send('tradeCompleted-%s' % (self.doId,), [])

    def tradeFailed(self):
        messenger.send('tradeFailed-%s' % (self.doId,), [])

    def tradeCanceled(self):
        messenger.send('tradeCanceled-%s' % (self.doId,), [])

    def sendRequestChangeGiving(self, giving):
        self.sendUpdate('requestChangeGiving', [giving])

    def rejectChangeGiving(self, reason):
        messenger.send('tradeRejectChangeGiving-%s' % (self.doId,), [reason])

    def getGiving(self):
        if localAvatar.doId == self.firstAvatarId:
            return self.firstAvatarGiving
        elif localAvatar.doId == self.secondAvatarId:
            return self.secondAvatarGiving
        else:
            self.notify.error('looking at wrong trade')

    def getOtherGiving(self):
        if localAvatar.doId == self.firstAvatarId:
            return self.secondAvatarGiving
        elif localAvatar.doId == self.secondAvatarId:
            return self.firstAvatarGiving
        else:
            self.notify.error('looking at wrong trade')

    def sendRequestChangeStatus(self, isTradeApproved):
        self.sendUpdate('requestChangeStatus', [isTradeApproved])

    def rejectChangeStatus(self, reason):
        messenger.send('tradeRejectChangeStatus-%s' % (self.doId,), [reason])

    def getStatus(self):
        if localAvatar.doId == self.firstAvatarId:
            return self.firstAvatarStatus
        elif localAvatar.doId == self.secondAvatarId:
            return self.secondAvatarStatus
        else:
            self.notify.error('looking at wrong trade')

    def getOtherStatus(self):
        if localAvatar.doId == self.firstAvatarId:
            return self.secondAvatarStatus
        elif localAvatar.doId == self.secondAvatarId:
            return self.firstAvatarStatus
        else:
            self.notify.error('looking at wrong trade')

    def sendRequestRemoveTrade(self):
        self.sendUpdate('requestRemoveTrade', [])

    def rejectRemoveTrade(self, reason):
        messenger.send('rejectRemoveTrade-%s' % (self.doId,), [reason])

    def getFirstAvatarId(self):
        return self.firstAvatarId

    def setFirstAvatarId(self, avatarId):
        self.firstAvatarId = avatarId

    def getFirstAvatarStatus(self):
        return self.firstAvatarStatus

    def setFirstAvatarStatus(self, avatarStatus):
        self.firstAvatarStatus = avatarStatus
        messenger.send(PiratesGlobals.TradeChangedEvent)

    def getFirstAvatarGiving(self):
        return self.firstAvatarGiving

    def setFirstAvatarGiving(self, giving):
        self.firstAvatarGiving = giving
        messenger.send(PiratesGlobals.TradeChangedEvent)

    def getSecondAvatarId(self):
        return self.secondAvatarId

    def setSecondAvatarId(self, avatarId):
        self.secondAvatarId = avatarId

    def getSecondAvatarStatus(self):
        return self.secondAvatarStatus

    def setSecondAvatarStatus(self, avatarStatus):
        self.secondAvatarStatus = avatarStatus
        messenger.send(PiratesGlobals.TradeChangedEvent)

    def getSecondAvatarGiving(self):
        return self.secondAvatarGiving

    def setSecondAvatarGiving(self, giving):
        self.secondAvatarGiving = giving
        messenger.send(PiratesGlobals.TradeChangedEvent)