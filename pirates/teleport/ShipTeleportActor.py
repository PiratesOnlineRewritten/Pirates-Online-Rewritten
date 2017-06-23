from pirates.teleport.DistributedTeleportActor import DistributedTeleportActor

class ShipTeleportActor(DistributedTeleportActor):

    def __init__(self, cr):
        DistributedTeleportActor.__init__(self, cr, 'ShipTeleportActor')