from pirates.teleport.DistributedFSM import DistributedFSM

class DistributedTeleportActor(DistributedFSM):

    def __init__(self, cr, name):
        DistributedFSM.__init__(self, cr, name)