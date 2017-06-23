from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.friends.AvatarFriendsManager import AvatarFriendsManager
from pirates.friends.PCFriendAvatarInfo import PCFriendAvatarInfo

class PCAvatarFriendsManager(AvatarFriendsManager):
    notify = directNotify.newCategory('PCAvatarFriendsManager')

    def __init__(self, cr):
        AvatarFriendsManager.__init__(self, cr)
        self.avatarId2ShipState = {}
        self.avatarId2ShipId = {}
        self.shipId2ShipState = {}

    def updateAvatarFriend(self, id, info):
        pcinfo = PCFriendAvatarInfo.makeFromFriendInfo(info)
        AvatarFriendsManager.updateAvatarFriend(self, id, pcinfo)

    def removeAvatarFriend(self, avId):
        AvatarFriendsManager.removeAvatarFriend(self, avId)
        self.avatarId2ShipState.pop(avId, None)
        shipId = self.avatarId2ShipId.get(avId, 0)
        if shipId:
            self.shipId2ShipState.pop(avId, None)
        self.avatarId2ShipId.pop(avId, None)
        return

    def setShipState(self, avatarId, onShip, shipId):
        if not hasattr(base, 'localAvatar'):
            self.notify.warning("setShipState: But I don't have a base.localAvatar!  gameFSM in state: %s" % base.cr.gameFSM.getCurrentState().getName())
            return
        self.avatarId2ShipState[avatarId] = onShip
        self.avatarId2ShipId[avatarId] = shipId
        self.shipId2ShipState[shipId] = onShip
        base.localAvatar.guiMgr.socialPanel.updateAvOnAll(avatarId)

    def getShipId2State(self, shipId):
        return self.shipId2ShipState.get(shipId, 0)

    def getShipState(self, avatarId):
        return self.avatarId2ShipState.get(avatarId, 0)

    def getShipId(self, avatarId):
        return self.avatarId2ShipId.get(avatarId, 0)

    def setBandId(self, avatarId, bandMgrId, bandId):
        info = self.avatarId2Info.get(avatarId)
        if info:
            info.setBandId(bandMgrId, bandId)

    def getBandId(self, avatarId):
        info = self.avatarId2Info.get(avatarId)
        if info:
            return info.getBandId()