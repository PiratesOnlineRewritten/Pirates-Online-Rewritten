from pirates.teleport.DistributedTeleportActor import DistributedTeleportActor

class TutorialTeleportActor(DistributedTeleportActor):

    def __init__(self, cr):
        TutorialTeleportActor.__init__(self, cr, 'TutorialTeleportActor')