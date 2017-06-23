from pirates.piratesbase import PiratesGlobals
from pirates.teleport.AreaTeleportActorOV import AreaTeleportActorOV

class DoorTeleportActorOV(AreaTeleportActorOV):

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, cr, name='DoorTeleportActorOV'):
        AreaTeleportActorOV.__init__(self, cr, name)

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterCompleteShow(self, *args):
        base.cr.loadingScreen.show()
        self.b_requestFSMState(None, 'ShowComplete')
        return