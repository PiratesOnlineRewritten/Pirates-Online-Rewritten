from direct.fsm.StatePush import FunctionCall, StateVar
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.distributed.DistributedInteractive import DistributedInteractive
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.effects.PotionTableSmoke import PotionTableSmoke
import PotionTableMsgPanel
import time

class DistributedPotionCraftingTable(DistributedInteractive):
    notify = directNotify.newCategory('DistributedPotionCraftingTable')
    _MIN_EXIT_DELAY = 1.0

    def __init__(self, cr):
        DistributedInteractive.__init__(self, cr)
        self.interactRadius = 15
        self.diskRadius = 25
        self.lastExitRequest = time.time()

    def generate(self):
        DistributedInteractive.generate(self)
        NodePath.__init__(self, 'RepairBench')
        self.setInteractOptions(proximityText=PLocalizer.CraftPotionInstructions, sphereScale=self.interactRadius, diskRadius=self.diskRadius)

    def announceGenerate(self):
        DistributedInteractive.announceGenerate(self)
        self.setAllowInteract(1)
        self.effect = PotionTableSmoke.getEffect()
        if self.effect:
            self.effect.setPos(1.3, 0.1, 3.5)
            self.effect.setEffectScale(0.25)
            self.effect.setEffectColor(Vec4(0.6, 0.4, 1.0, 1.0))
            self.effect.reparentTo(self)
            self.effect.play()

    def disable(self):
        DistributedInteractive.disable(self)
        if self.effect:
            self.effect.cleanUpEffect()

        self.detachNode()

    def requestInteraction(self, avId, interactType=0):
        if localAvatar.isUndead():
            localAvatar.guiMgr.createWarning(PLocalizer.NoPotionsWhileUndeadWarning, PiratesGuiGlobals.TextFG6)
        else:
            DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        DistributedInteractive.rejectInteraction(self)

    def requestExit(self):
        base.localAvatar.guiMgr.setIgnoreEscapeHotKey(True)
        now = time.time()
        if now - self.lastExitRequest > self._MIN_EXIT_DELAY:
            self.sendUpdate('checkExit')
            self.lastExitRequest = now

        DistributedInteractive.requestExit(self)

    def enterWaiting(self):
        localAvatar.motionFSM.off()
        DistributedInteractive.enterWaiting(self)

    def exitWaiting(self):
        localAvatar.motionFSM.on()
        DistributedInteractive.exitWaiting(self)

    def enterUse(self):
        DistributedInteractive.enterUse(self)
        localAvatar.b_setGameState('PotionCrafting')
        self.gameInterest = self.cr.addInterest(self.doId, localAvatar.doId, 'potiongame')

    def reallyRequestInteraction(self, avId, interactType):
        DistributedInteractive.requestInteraction(self, avId, interactType)

    def exitUse(self):
        if self.gameInterest:
            self.cr.removeInterest(self.gameInterest)
            self.gameInterest = None

        localAvatar.guiMgr.setIgnoreEscapeHotKey(False)
        localAvatar.b_setGameState('LandRoam')
        DistributedInteractive.exitUse(self)
