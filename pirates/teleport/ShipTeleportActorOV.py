from pirates.teleport.DistributedTeleportActorOV import DistributedTeleportActorOV
from pirates.piratesbase import PiratesGlobals

class ShipTeleportActorOV(DistributedTeleportActorOV):

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, cr, name='ShipTeleportActorOV', doEffect=True):
        DistributedTeleportActorOV.__init__(self, cr, name, doEffect=doEffect)

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterOpenWorld(self, worldLocations, worldDoId):
        self.worldDoId = worldDoId
        self._requestWhenInterestComplete('WorldOpen')
        self.cr.setWorldStack(worldLocations, event='WorldOpen')

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterOpenGame(self, shipParentId, shipZoneId, shipDoId):
        self.shipDoId = shipDoId
        world = self.cr.getDo(self.worldDoId)
        world.goOnStage()
        self.cr.relatedObjectMgr.requestObjects((self.shipDoId,), allCallback=self.shipInterestReady, timeout=30, timeoutCallback=self.shipTimedOut)
        self.oceanInterest = self.cr.addTaggedInterest(shipParentId, shipZoneId, self.cr.ITAG_GAME, 'ocean')

    @report(types=['args'], dConfigParam=['dteleport'])
    def shipTimedOut(self, doIds):
        self.sendUpdate('clientAbort')

    @report(types=['args'], dConfigParam=['dteleport'])
    def shipInterestReady(self, shipList):
        ship = shipList[0]
        self.cr.queueAllInterestsCompleteEvent()
        self.cr.setAllInterestsCompleteCallback(self.shipZoneComplete)

    @report(types=['args'], dConfigParam=['dteleport'])
    def shipZoneComplete(self):
        if self.getCurrentOrNextState() != 'OpenGame':
            return
        if self.cr == None:
            return
        ship = self.cr.getDo(self.shipDoId)
        if ship:
            self._requestWhenInterestComplete('GameOpen')
            ship.placeLocalAvatar(localAvatar)
            localAvatar.b_setLocation(ship.getDoId(), PiratesGlobals.ShipZoneOnDeck)
            localAvatar.sendCurrentPosition()
            self.cr.removeTaggedInterest(self.oceanInterest)
            self.oceanInterest = None
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def exitOpenGame(self):
        self.cr.removeTaggedInterest(self.oceanInterest)
        self.oceanInterest = None
        self._cancelInterestCompleteRequest()
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterStartShow(self, *args):
        self.cr.loadingScreen.hide()
        base.transitions.fadeIn()
        localAvatar.b_setGameState('LandRoam')
        self.b_requestFSMState(None, 'Done')
        return