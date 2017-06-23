from pirates.pirate.PAvatarHandle import PAvatarHandle

class CrewMatchHandle(PAvatarHandle):

    def __init__(self, avId, avName):
        self.avatarId = avId
        self.avatarName = avName
        self.accountId = None
        self.accountName = None
        return

    def getName(self):
        return self.avatarName

    def isUnderstandable(self):
        return False

    def isOnline(self):
        return False

    def getBandId(self):
        return (0, 0)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        base.cr.crewMatchManager.d_requestTeleportQuery(sendToId, localBandMgrId, localBandId, localGuildId, localShardId)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        base.cr.crewMatchManager.d_requestTeleportResponse(sendToId, available, shardId, instanceDoId, areaDoId)