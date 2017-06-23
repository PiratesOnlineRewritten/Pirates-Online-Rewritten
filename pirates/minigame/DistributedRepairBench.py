from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from panda3d.core import TextNode
from pirates.distributed.DistributedInteractive import DistributedInteractive
from pirates.piratesbase import PLocalizer
import RepairGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
DifficultyText = {0: PLocalizer.Minigame_Repair_Table_Interact_Text_Easy,5: PLocalizer.Minigame_Repair_Table_Interact_Text_Medium,9: PLocalizer.Minigame_Repair_Table_Interact_Text_Hard}

class DistributedRepairBench(DistributedInteractive):
    notify = directNotify.newCategory('DistributedRepairBench')

    def __init__(self, cr):
        DistributedInteractive.__init__(self, cr)
        self.interactRadius = 15
        self.diskRadius = 25
        self.difficulty = 0
        self.repairBenchDifficultyTextNode = None
        self.repairBenchDifficultyNodePath = None
        return

    def generate(self):
        DistributedInteractive.generate(self)
        NodePath.__init__(self, 'RepairBench')
        self.setInteractOptions(proximityText=PLocalizer.InteractRepairBench, sphereScale=self.interactRadius, diskRadius=self.diskRadius)
        self.requestDifficulty()

    def delete(self):
        self.repairBenchDifficultyTextNode = None
        DistributedInteractive.delete(self)
        return

    def requestDifficulty(self):
        self.sendUpdate('requestDifficulty')

    def setDifficulty(self, difficulty):
        self.proximityText = PLocalizer.InteractRepairBench + ' (' + DifficultyText[difficulty] + ')'
        self.difficulty = difficulty

    def announceGenerate(self):
        DistributedInteractive.announceGenerate(self)
        self.setAllowInteract(1)
        self.checkInUse()

    def disable(self):
        if self.userId == localAvatar.doId:
            self.stopRepairing()
        DistributedInteractive.disable(self)
        self.detachNode()

    def _evalUsableState(self, fullShipHealth, steeringWheelInUse):
        pass

    def requestInteraction(self, avId, interactType=0):
        if localAvatar.isUndead():
            localAvatar.guiMgr.createWarning(PLocalizer.Minigame_Repair_UndeadWarning, PiratesGuiGlobals.TextFG6)
        else:
            DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        localAvatar.guiMgr.createWarning(PLocalizer.Minigame_Repair_GenericBenchWarning)
        localAvatar.motionFSM.on()
        DistributedInteractive.rejectInteraction(self)

    def kickInteraction(self):
        localAvatar.guiMgr.createWarning(PLocalizer.Minigame_Repair_KickedFromBenchWarning)
        localAvatar.motionFSM.on()
        DistributedInteractive.rejectInteraction(self)

    def finishInteraction(self):
        localAvatar.motionFSM.on()
        DistributedInteractive.rejectInteraction(self)

    def startRepairing(self):
        localAvatar.b_setGameState('BenchRepair')

    def stopRepairing(self):
        if localAvatar.getGameState() == 'BenchRepair':
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
            base.localAvatar.motionFSM.on()

    def requestExit(self):
        DistributedInteractive.requestExit(self)
        self.stopRepairing()

    def enterWaiting(self):
        DistributedInteractive.enterWaiting(self)
        localAvatar.motionFSM.off()

    def exitWaiting(self):
        DistributedInteractive.exitWaiting(self)

    def enterUse(self):
        DistributedInteractive.enterUse(self)
        self.startRepairing()

    def exitUse(self):
        self.stopRepairing()
        DistributedInteractive.exitUse(self)

    def setUserId(self, avId):
        DistributedInteractive.setUserId(self, avId)
        self.checkInUse()

    def checkInUse(self):
        if self.userId and localAvatar.getDoId() != self.userId:
            self.setAllowInteract(0)
        else:
            self.setAllowInteract(1)