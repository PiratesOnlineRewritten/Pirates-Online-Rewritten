from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify.DirectNotifyGlobal import directNotify
from otp.otpbase import OTPGlobals
from otp.friends.PlayerFriendsManager import PlayerFriendsManager
from pirates.friends.PCFriendPlayerInfo import PCFriendPlayerInfo

class PCPlayerFriendsManager(PlayerFriendsManager):
    notify = directNotify.newCategory('PCPlayerFriendsManager')

    def __init__(self, cr):
        PlayerFriendsManager.__init__(self, cr)
        self.playerId2ShipState = {}
        self.playerId2ShipId = {}
        self.shipId2ShipState = {}

    def updatePlayerFriend(self, id, info, isNewFriend):
        pcinfo = PCFriendPlayerInfo.makeFromFriendInfo(info)
        PlayerFriendsManager.updatePlayerFriend(self, id, pcinfo, isNewFriend)

    def removePlayerFriend(self, id):
        PlayerFriendsManager.removePlayerFriend(self, id)
        self.playerId2ShipState.pop(id, None)
        shipId = self.playerId2ShipId.get(id, 0)
        if shipId:
            self.shipId2ShipState.pop(id, None)
        self.playerId2ShipId.pop(id, None)
        return

    def setShipState(self, playerId, onShip, shipId):
        self.playerId2ShipState[playerId] = onShip
        self.playerId2ShipId[playerId] = shipId
        self.shipId2ShipState[shipId] = onShip
        localAvatar.guiMgr.socialPanel.updateAll()

    def getShipState(self, playerId):
        return self.playerId2ShipState.get(playerId, 0)

    def getShipId2State(self, shipId):
        return self.shipId2ShipState.get(shipId, 0)

    def getShipId(self, playerId):
        return self.playerId2ShipId.get(playerId, 0)

    def setBandId(self, playerId, bandMgrId, bandId):
        info = self.playerId2Info.get(playerId)
        if info:
            info.setBandId(bandMgrId, bandId)

    def getBandId(self, playerId):
        info = self.playerId2Info.get(playerId)
        if info:
            return info.getBandId()