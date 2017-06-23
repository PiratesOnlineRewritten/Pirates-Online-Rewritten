from pirates.teleport.DistributedTeleportActor import DistributedTeleportActor

class JailTeleportActor(DistributedTeleportActor):

    def __init__(self, cr):
        JailTeleportActor.__init__(self, cr, 'JailTeleportActor')