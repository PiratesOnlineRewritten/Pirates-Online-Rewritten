from pirates.piratesbase import PiratesGlobals
from pirates.teleport.TeleportGlobals import TeleportErrors
from pirates.teleport.DistributedFSMOV import DistributedFSMOV

class DistributedTeleportActorOV(DistributedFSMOV):

    @report(types=['args'], dConfigParam=['dteleport'])
    def __init__(self, cr, name, doEffect=True):
        DistributedFSMOV.__init__(self, cr, name)
        self._requestCallback = None
        localAvatar.b_clearTeleportFlag(PiratesGlobals.TFLookoutJoined)
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def _requestWhenInterestComplete(self, state, *args):
        self._cancelInterestCompleteRequest()
        self._requestCallback = Functor(self.b_requestFSMState, None, state, *args)
        self.cr.queueAllInterestsCompleteEvent()
        self.cr.setAllInterestsCompleteCallback(self._requestCallback)
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def _cancelInterestCompleteRequest(self):
        if self._requestCallback:
            self.cr.removeAllInterestsCompleteCallback(self._requestCallback)
            self._requestCallback = None
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def announceGenerate(self):
        DistributedFSMOV.announceGenerate(self)

    @report(types=['args'], dConfigParam=['dteleport'])
    def disable(self):
        DistributedFSMOV.disable(self)
        self._cancelInterestCompleteRequest()
        if self.cr.teleportMgr:
            self.cr.teleportMgr.clearAmInTeleport()
        messenger.send('localAvTeleportFinished')
        base.cr.loadingScreen.hide()

    @report(types=['args'], dConfigParam=['dteleport'])
    def setFSMState(self, stateContext, stateData):
        if not DistributedFSMOV.setFSMState(self, stateContext, stateData):
            self.d_fsmRequestResponse(stateContext, TeleportErrors.Interrupted)

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterCompleteShow(self, *args):

        def continueTeleport():
            base.cr.loadingScreen.show()
            self.b_requestFSMState(None, 'ShowComplete')
            return

        self.acceptOnce('avatarTeleportEffect-done', continueTeleport)
        doEffect = args[0] and not localAvatar.testTeleportFlag(PiratesGlobals.TFInInitTeleport) and not localAvatar.testTeleportFlag(PiratesGlobals.TFInWater)
        if doEffect == False and localAvatar.gameFSM.state == 'TeleportOut':
            self.ignore('avatarTeleportEffect-done')
            continueTeleport()
        else:
            localAvatar.b_setGameState('TeleportOut', ['avatarTeleportEffect-done', doEffect])

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterGoToOldQuietZone(self, *args):
        localAvatar.b_setLocation(self.cr.distributedDistrict.doId, PiratesGlobals.QuietZone)
        self.b_requestFSMState(None, 'InOldQuietZone')
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterCloseGame(self, *args):
        self.cr.getActiveWorld().goOffStage()
        worldStack = self.cr.getWorldStack()
        self._requestWhenInterestComplete('GameClosed', worldStack)
        self.cr.removeInterestTag(self.cr.ITAG_GAME)

    @report(types=['args'], dConfigParam=['dteleport'])
    def exitCloseGame(self):
        self._cancelInterestCompleteRequest()

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterGameClosed(self, *args):
        pass

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterCloseWorld(self, *args):
        self._requestWhenInterestComplete('WorldClosed')
        self.cr.setWorldStack([])
        self.cr.removeInterestTag(self.cr.ITAG_WORLD)

    @report(types=['args'], dConfigParam=['dteleport'])
    def exitCloseWorld(self):
        self._cancelInterestCompleteRequest()

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterWorldClosed(self, *args):
        pass

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterCloseShard(self, *args):
        self._requestWhenInterestComplete('ShardClosed')
        self.cr.closeShard()
        self.cr.removeInterestTag(self.cr.ITAG_SHARD)

    @report(types=['args'], dConfigParam=['dteleport'])
    def exitCloseShard(self):
        self._cancelInterestCompleteRequest()

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterShardClosed(self, *args):
        pass

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterGoToQuietZone(self, shardId):
        localAvatar.b_setLocation(shardId, PiratesGlobals.QuietZone)
        self.b_requestFSMState(None, 'InQuietZone')
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterOpenShard(self, *args):
        shardId = self.cr.getShardId()

        def shardIsReady():
            self.b_requestFSMState(None, 'ShardOpen')
            messenger.send('shardSwitchComplete')
            return

        self.acceptOnce('shardReady-%s' % (shardId,), shardIsReady)
        self.cr.shardFSM.request('OpenShard')

    @report(types=['args'], dConfigParam=['dteleport'])
    def exitOpenShard(self):
        self.ignore('shardReady-%s' % (self.cr.getShardId(),))

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterShardOpen(self, *args):
        pass

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterOpenWorld(self, *args):
        self.b_requestFSMState(None, 'WorldOpen')
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterOpenGame(self, *args):
        self.b_requestFSMState(None, 'GameOpen')
        return

    @report(types=['args'], dConfigParam=['dteleport'])
    def enterStartShow(self, *args):
        self.b_requestFSMState(None, 'Done')
        localAvatar.b_setGameState('TeleportIn')
        return