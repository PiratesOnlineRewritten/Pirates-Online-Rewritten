from pirates.teleport.DistributedTeleportActor import DistributedTeleportActor

class AreaTeleportActor(DistributedTeleportActor):

    def __init__(self, cr):
        AreaTeleportActor.__init__(self, cr, 'AreaTeleportActor')