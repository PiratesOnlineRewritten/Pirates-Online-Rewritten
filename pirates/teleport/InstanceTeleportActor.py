from pirates.teleport.DistributedTeleportActor import DistributedTeleportActor

class InstanceTeleportActor(DistributedTeleportActor):

    def __init__(self, cr):
        DistributedTeleportActor.__init__(self, cr, 'InstanceTeleportActor')