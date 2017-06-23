from pirates.teleport.DistributedTeleportActorOV import DistributedTeleportActorOV

class InstanceTeleportActorOV(DistributedTeleportActorOV):

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, cr, name='InstanceTeleportActorOV', doEffect=True):
        DistributedTeleportActorOV.__init__(self, cr, name, doEffect=doEffect)

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterOpenWorld(self, worldLocations, worldDoId):
        self.worldDoId = worldDoId
        self._requestWhenInterestComplete('WorldOpen')
        self.cr.setWorldStack(worldLocations, event='WorldOpen')

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterOpenGame(self, areaDoId, spawnPt):
        self.areaDoId = areaDoId
        self.spawnPt = spawnPt
        world = self.cr.getDo(self.worldDoId)
        if not world:
            self.notify.warning('enterOpenGame: world %s not found, probably got removed already' % self.worldDoId)
            self.sendUpdate('clientAbort')
            return
        world.goOnStage()
        area = self.cr.getDo(areaDoId)
        area.goOnStage()
        self._requestWhenInterestComplete('GameOpen')
        localAvatar.reparentTo(area)
        localAvatar.setPosHpr(area, *self.spawnPt)
        area.parentObjectToArea(localAvatar)
        localAvatar.enableGridInterest()
        area.manageChild(localAvatar)
        localAvatar.sendCurrentPosition()

    @report(types=['args'], dConfigParam=['dteleport'])
    def exitOpenGame(self):
        self._cancelInterestCompleteRequest()

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterStartShow(self, *args):
        self.cr.loadingScreen.hide()
        base.transitions.fadeIn()
        localAvatar.b_setGameState('LandRoam')
        self.b_requestFSMState(None, 'Done')
        return