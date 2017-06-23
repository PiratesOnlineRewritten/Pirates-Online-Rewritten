from otp.avatar.AvatarHandle import AvatarHandle

class PAvatarHandle(AvatarHandle):
    dclassName = 'PAvatarHandle'

    def getBandId(self):
        if __dev__:
            pass
        return (0, 0)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        if __dev__:
            pass

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        if __dev__:
            pass