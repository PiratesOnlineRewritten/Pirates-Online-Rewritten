import random
from pandac.PandaModules import Point3
from direct.fsm import FSM
from direct.interval.IntervalGlobal import Sequence, Wait, Func
from direct.interval.LerpInterval import LerpPosInterval
from direct.task import Task
from FishFSM import FishFSM
import FishingGlobals

class LegendaryFishFSM(FishFSM):

    def __init__(self, fish):
        FishFSM.__init__(self, fish)
        self.defaultTransitions = {'Offscreen': ['FinalBackToSea', 'Swimming', 'TurnAround', 'HookedFighting', 'AboutToBiteLure'],'Swimming': ['TurnAround', 'Biting', 'AboutToBiteLure', 'Offscreen'],'AboutToBiteLure': ['Swimming', 'Biting', 'Offscreen'],'TurnAround': ['AboutToBiteLure', 'Swimming', 'Offscreen'],'Biting': ['Swimming', 'PullingLure', 'Hooked', 'Flee', 'Offscreen'],'Hooked': ['HookedFighting', 'PullingLure', 'Offscreen'],'PullingLure': ['Hooked', 'HookedFighting', 'Flee', 'Offscreen'],'HookedFighting': ['PullingLure', 'Hooked', 'Flee', 'Offscreen'],'Flee': ['Swimming', 'TurnAround', 'Offscreen'],'FinalBackToSea': ['Offscreen']}

    def enterAboutToBiteLure(self):
        self.fish.initVariables()
        self.fish.showStaminaBar()
        self.fish.actor.clearControlEffectWeights()
        self.fish.reparentTo(self.fish.fishManager.objectsWithCaustics)
        self.fish.setPos(FishingGlobals.rightFishBarrier + FishingGlobals.fullyOffscreenXOffset, 0.0, max(-63.0, self.fish.fishManager.gameObject.lure.getZ()))
        self.fish.actor.changeAnimationTo('swimIdleOpposite')
        self.lfChaseLureSequence = Sequence(self.fish.posInterval(self.fish.myData['swimLeftDuration'], Point3(self.fish.myData['fishTurnX'], 0.0, self.fish.getZ())), Func(self.fish.actor.changeAnimationTo, 'turnOpposite', False), Wait(self.fish.actor.getDuration('turnOpposite') / 4.0), Func(self.fish.actor.changeAnimationTo, 'swimIdle'), self.fish.posInterval(self.fish.myData['swimRightDuration'], Point3(self.fish.fishManager.gameObject.lure.getX() - self.fish.myData['biteXOffset'], 0.0, self.fish.getZ())), Func(self.request, 'Biting'), name=self.fish.fishManager.gameObject.distributedFishingSpot.uniqueName('lfChaseLureSequence'))
        self.lfChaseLureSequence.start()

    def exitAboutToBiteLure(self):
        self.lfChaseLureSequence.pause()
        self.lfChaseLureSequence.clearToInitial()

    def checkForBite(self):
        pass

    def enterHooked(self):
        self.fish.fishMoveSequence.pause()
        self.fish.actor.changeAnimationTo('reelIdle')

    def exitHooked(self):
        taskName = '%s_StartFighting' % self.fish.getName()
        taskMgr.remove(self.fish.fishManager.gameObject.distributedFishingSpot.uniqueName(taskName))
        self.fish.lfStruggleSequence.pause()
        self.fish.lfStruggleSequence.clearToInitial()

    def enterHookedFighting(self):
        self.fish.actor.changeAnimationTo('fightIdle')

    def exitHookedFighting(self):
        pass

    def enterPullingLure(self):
        self.fish.actor.changeAnimationTo('fightIdle')

    def exitPullingLure(self):
        self.fish.setY(0.0)

    def enterFinalBackToSea(self):
        self.fish.setPosHpr(self.fish.myData['goodbyePosHpr'][0], self.fish.myData['goodbyePosHpr'][1])
        self.fish.actor.changeAnimationTo('swimIdle')
        self.farewellInterval = LerpPosInterval(self.fish, FishingGlobals.waveToLegendaryFishDuration, pos=self.fish.myData['swimmingDistance'], startPos=self.fish.getPos(), name='%s_farewellInterval' % self.fish.getName())
        self.farewellInterval.start()

    def exitFinalBackToSea(self):
        self.farewellInterval.pause()
        self.farewellInterval.clearToInitial()