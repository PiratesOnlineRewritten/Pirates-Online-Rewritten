import DistributedMiniGameWorld
from pirates.piratesgui.CannonDefenseCountdownUI import CannonDefenseCountdownUI
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesConfirm
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.world import WorldGlobals

class DistributedScrimmageWorld(DistributedMiniGameWorld.DistributedMiniGameWorld):

    def __init__(self, cr):
        DistributedMiniGameWorld.DistributedMiniGameWorld.__init__(self, cr)
        self._countdownUI = None
        self.confirm = None
        return

    def generate(self):
        DistributedMiniGameWorld.DistributedMiniGameWorld.generate(self)

    def announceGenerate(self):
        DistributedMiniGameWorld.DistributedMiniGameWorld.announceGenerate(self)
        self._countdownUI = CannonDefenseCountdownUI()
        self._countdownUI.reparentTo(base.a2dTopCenter)
        self._countdownUI.setPos(0.0, 0, -0.23)
        localAvatar.b_setTeleportFlag(PiratesGlobals.TFInScrimmage)

    def disable(self):
        DistributedMiniGameWorld.DistributedMiniGameWorld.disable(self)
        if self._countdownUI:
            self._countdownUI.removeNode()
            self._countdownUI = None
        self.cleanUpConfirm()
        localAvatar.b_clearTeleportFlag(PiratesGlobals.TFInScrimmage)
        return

    def updateCountdown(self, timeLeft):
        if self._countdownUI:
            self._countdownUI.setTime(timeLeft - 1)

    def localAvEnterDeath(self, av):
        DistributedMiniGameWorld.DistributedMiniGameWorld.localAvEnterDeath(self, av)
        self.cr.teleportMgr.initiateTeleport(PiratesGlobals.INSTANCE_MAIN, WorldGlobals.PiratesWorldSceneFileBase)

    def cleanUpConfirm(self):
        if self.confirm:
            self.confirm.destroy()
            self.confirm = None
        return

    def sendRoundComplete(self, round):
        localAvatar.skillDiary.clearRecharging(InventoryType.UseItem)
        localAvatar.guiMgr.combatTray.tonicButton.skillRingIval.finish()
        self.confirm = PiratesConfirm.PiratesConfirm(PLocalizer.ScrimmageRoundComplete % round, PLocalizer.ScrimmageRoundContinue, self.onCloseContinue)
        self.confirm.bNo['command'] = self.onCloseQuit

    def onCloseContinue(self):
        self.cleanUpConfirm()
        self.sendUpdate('requestContinueScrimmage', [])

    def onCloseQuit(self):
        self.cleanUpConfirm()
        self.sendUpdate('requestLeaveScrimmage', [])