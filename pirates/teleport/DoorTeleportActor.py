from pirates.teleport.AreaTeleportActor import AreaTeleportActor

class DoorTeleportActor(AreaTeleportActor):

    def __init__(self, cr, name='DoorTeleportActor'):
        AreaTeleportActor.__init__(self, cr, name)