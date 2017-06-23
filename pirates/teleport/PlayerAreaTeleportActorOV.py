from pirates.piratesbase import PiratesGlobals
from pirates.teleport.AreaTeleportActorOV import AreaTeleportActorOV

class PlayerAreaTeleportActorOV(AreaTeleportActorOV):

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, cr, name='PlayerAreaTeleportActorOV'):
        AreaTeleportActorOV.__init__(self, cr, name)