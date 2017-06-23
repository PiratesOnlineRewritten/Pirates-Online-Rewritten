from pirates.teleport.DistributedTeleportActorOV import DistributedTeleportActorOV

class AreaTeleportActorOV(DistributedTeleportActorOV):

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, cr, name='AreaTeleportActorOV', doEffect=True):
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
        world.goOnStage()
        area = self.cr.getDo(areaDoId)
        area.goOnStage()
        self._requestWhenInterestComplete('GameOpen')
        localAvatar.reparentTo(area)
        localAvatar.setPosHpr(area, *self.spawnPt)
        localAvatar.spawnWiggle()
        area.parentObjectToArea(localAvatar)
        localAvatar.enableGridInterest()
        area.manageChild(localAvatar)
        try:
            localAvatar.sendCurrentPosition()
        except ValueError:
            localAvatar.reverseLs()
            self.notify.error('avatar placed at bad position %s in area %s (%s) at spawnPt %s' % (str(localAvatar.getPos()), area, area.uniqueId, str(self.spawnPt)))

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