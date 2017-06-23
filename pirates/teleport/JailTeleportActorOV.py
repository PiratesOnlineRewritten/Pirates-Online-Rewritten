from pirates.teleport.DistributedTeleportActorOV import DistributedTeleportActorOV

class JailTeleportActorOV(DistributedTeleportActorOV):

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, cr, doEffect=True):
        DistributedTeleportActorOV.__init__(self, cr, 'JailTeleportActorOV', doEffect=doEffect)