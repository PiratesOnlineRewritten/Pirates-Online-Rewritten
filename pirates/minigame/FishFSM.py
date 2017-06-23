import random
import math
from pirates.piratesbase import PLocalizer
from pandac.PandaModules import Point3, Vec3
from direct.fsm import FSM
from direct.interval.IntervalGlobal import Sequence, Parallel, Wait, Func, SoundInterval
from direct.interval.LerpInterval import LerpFunc, LerpPosInterval
from direct.task import Task
from pandac.PandaModules import MouseButton
from pirates.uberdog.UberDogGlobals import InventoryType
import FishingGlobals
import MinigameUtils

class FishFSM(FSM.FSM):

    def __init__(self, fish):
        FSM.FSM.__init__(self, 'FishFSM')
        self.fish = fish
        self.defaultTransitions = {'Offscreen': ['Swimming', 'TurnAround', 'ScareAway', 'Flee'],'Swimming': ['Offscreen', 'TurnAround', 'Biting', 'ScareAway', 'Flee', 'Eating', 'BeingEaten'],'TurnAround': ['ScareAway', 'Swimming', 'Flee', 'Offscreen'],'Biting': ['Offscreen', 'ScareAway', 'Swimming', 'TurnAround', 'Hooked', 'Flee'],'Hooked': ['AboutToFight', 'Offscreen'],'AboutToFight': ['HookedFighting', 'Offscreen'],'HookedFighting': ['Hooked', 'Offscreen', 'Flee'],'Flee': ['ScareAway', 'Swimming', 'Offscreen', 'TurnAround'],'ScareAway': ['TurnAround', 'Swimming', 'Offscreen'],'Eating': ['ScareAway', 'TurnAround', 'Swimming', 'Flee', 'Offscreen'],'BeingEaten': ['ScareAway', 'TurnAround', 'Offscreen']}

    def enterOffscreen(self):
        if self.fish in self.fish.fishManager.uncaughtFish:
            self.fish.fishManager.deadFish.append(self.fish)
        self.fish.cleanFishData()
        self.fish.actor.stop()
        self.fish.setPosHpr(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        self.fish.reparentTo(hidden)
        if self.fish.fishMoveSequence:
            self.fish.fishMoveSequence.pause()
            self.fish.fishMoveSequence.clearToInitial()

    def exitOffscreen(self):
        self.fish.reparentTo(self.fish.fishManager.objectsWithCaustics)
        self.fish.myZ = self.fish.getZ()

    def enterSwimming(self):
        self.fish.setHpr(0.0, 0.0, 0.0)
        self.fish.startIdleBubbleEffect()
        if self.fish.movingRight:
            self.fish.actor.changeAnimationTo('swimIdle')
        else:
            self.fish.actor.changeAnimationTo('swimIdleOpposite')

    def exitSwimming(self):
        self.fish.stopIdleBubbleEffect()

    def enterTurnAround(self, nextState, shouldMoveRight):
        self.fish.turnAround(nextState, shouldMoveRight)

    def exitTurnAround(self):
        if self.fish.fishMoveSequence:
            self.fish.fishMoveSequence.pause()

    def enterBiting(self):
        self.fish.startBiteBubbleEffect()
        if self.fish.myData['size'] == 'small':
            biteSFX = self.fish.fishManager.gameObject.sfx['biteSmall']
        else:
            if self.fish.myData['size'] == 'medium':
                biteSFX = self.fish.fishManager.gameObject.sfx['biteSmall']
            else:
                if self.fish.myData['size'] == 'large':
                    biteSFX = self.fish.fishManager.gameObject.sfx['biteLarge']
                elif self.fish.myData['size'] == 'super':
                    biteSFX = self.fish.fishManager.gameObject.sfx['biteLarge']
                if self.fish.getX() < self.fish.fishManager.gameObject.lure.getX():
                    self.fish.actor.changeAnimationTo('bite', False)
                    biteOffset = self.fish.mouthJoint.getPos() * -1.0 * self.fish.actor.getSx()
                self.fish.actor.changeAnimationTo('biteOpposite', False)
                biteOffset = self.fish.mouthJoint.getPos() * -1.0 * self.fish.actor.getSx()
            self.fish.fishManager.activeFish = self.fish
            if self.fish.fishMoveSequence:
                self.fish.fishMoveSequence.pause()
        biteDuration = 1.083
        self.fish.fishManager.gameObject.lureAngle = 0
        self.fish.wrtReparentTo(self.fish.fishManager.gameObject.lure)
        self.fish.fishStatusIconNodePath.setScale(1.0)
        (self.fish.fishStatusIconNodePath.show(),)
        self.fish.fishStatusIconTextNode.setText('?')
        self.fish.fishStatusIconTextNode.setTextColor(1.0, 1.0, 0.0, 1.0)
        self.fish.fishManager.gameObject.sfx['biteAlert'].play()
        self.fish.fishManager.gameObject.scareFish = False
        self.fish.fishMoveSequence = Sequence(Parallel(Sequence(Wait(biteDuration * FishingGlobals.biteWindowStartPercentage), Func(self.checkForBite), Func(self.fish.fishStatusIconNodePath.show), Func(self.fish.fishStatusIconTextNode.setText, '!'), Func(self.fish.fishStatusIconTextNode.setTextColor, 0.0, 1.0, 0.0, 1.0), Func(base.playSfx, biteSFX), Wait(biteDuration * FishingGlobals.biteWindowFinishPercentage), Func(self.fish.fishManager.gameObject.checkForHooked)), self.fish.posInterval(biteDuration / 2.0, biteOffset)), name='%s_MoveSequence' % self.fish.getName())
        self.fish.fishMoveSequence.start()

    def checkForBite(self):
        if self.getCurrentOrNextState() != 'Flee':
            if not self.fish.fishManager.gameObject.scareFish:
                self.fish.fishManager.gameObject.lure.showHelpText(None)
                self.fish.fishManager.gameObject.fsm.request('FishBiting')
            else:
                if self.fish.fishMoveSequence:
                    self.fish.fishMoveSequence.pause()
                    self.fish.fishMoveSequence.clearToInitial()
                self.fish.fishManager.activeFish = None
                if self.getCurrentOrNextState() != 'Flee':
                    self.request('Flee')
                self.fish.fishManager.gameObject.lure.showHelpText(PLocalizer.Minigame_Fishing_Lure_Alerts['scaredOff'])
        return

    def exitBiting(self):
        self.fish.fishStatusIconNodePath.hide()
        self.fish.fishStatusIconTextNode.setText('?')
        self.fish.fishStatusIconTextNode.setTextColor(1.0, 0.0, 0.0, 1.0)
        if self.fish.fishMoveSequence:
            self.fish.fishMoveSequence.pause()
        self.fish.myZ = self.fish.getZ()
        self.fish.wrtReparentTo(self.fish.fishManager.objectsWithCaustics)

    def enterHooked(self):
        if self.fish.fishMoveSequence:
            self.fish.fishMoveSequence.pause()
        self.fish.actor.changeAnimationTo('reelIdle')
        delay = random.randint(int(math.floor(self.fish.myData['restDurationRange'][0])), int(math.ceil(self.fish.myData['restDurationRange'][1])))
        taskMgr.doMethodLater(delay, self.requestNext, name='%s_StartFighting' % self.fish.getName(), extraArgs=['AboutToFight'])

    def exitHooked(self):
        taskMgr.remove('%s_StartFighting' % self.fish.getName())

    def enterAboutToFight(self):
        if self.fish.myData['size'] == 'small' or self.fish.myData['size'] == 'medium':
            if self.fish.myData['size'] == 'small':
                self.fish.fishStatusIconNodePath.setScale(0.4)
            self.fish.fishStatusIconNodePath.show()
            self.fish.fishStatusIconTextNode.setText('!')
        else:
            self.fish.fishStatusIconNodePath.hide()
        if self.fish.fishManager.gameObject.distributedFishingSpot.showTutorial:
            self.fish.fishManager.gameObject.lure.showHelpText(PLocalizer.Minigame_Fishing_Lure_Alerts['letgo'])
        if random.randint(0, 1) == 0:
            self.fish.fishManager.gameObject.sfx['fishFight01'].play()
        else:
            self.fish.fishManager.gameObject.sfx['fishFight02'].play()
        taskMgr.doMethodLater(FishingGlobals.fightWarningDurations[self.fish.myData['size']], self.requestNext, name='%s_GoFighting' % self.fish.getName(), extraArgs=['HookedFighting'])

    def exitAboutToFight(self):
        taskMgr.remove('%s_GoFighting' % self.fish.getName())

    def enterHookedFighting(self):
        self.fish.startFightBubbleEffect()
        self.fish.actor.changeAnimationTo('fightIdle')
        self.fish.fishManager.gameObject.fsm.request('FishFighting')
        delay = random.randint(int(math.floor(self.fish.myData['fightDurationRange'][0])), int(math.ceil(self.fish.myData['fightDurationRange'][1])))
        taskMgr.doMethodLater(delay, self.requestNext, name='%s_StopFighting' % self.fish.getName(), extraArgs=['Hooked'])

    def exitHookedFighting(self):
        self.fish.stopFightBubbleEffect()
        self.fish.fishStatusIconNodePath.hide()
        taskMgr.remove('%s_StopFighting' % self.fish.getName())
        if self.getCurrentOrNextState() not in ['Offscreen', 'Flee']:
            if base.mouseWatcherNode.isButtonDown(MouseButton.one()):
                self.fish.fishManager.gameObject.fsm.request('ReelingFish')
            else:
                self.fish.fishManager.gameObject.fsm.request('FishOnHook')

    def enterFlee(self):
        taskMgr.doMethodLater(FishingGlobals.fleeDuration, self.requestNext, name='%s_StopFleeing' % self.fish.getName(), extraArgs=['Swimming'])
        self.fish.myZ = self.fish.getZ()
        self.fish.setHpr(0.0, 0.0, 0.0)
        if self.fish.movingRight:
            self.fish.actor.changeAnimationTo('swimIdle', blend=False)
        else:
            self.fish.actor.changeAnimationTo('swimIdleOpposite', blend=False)
        self.fish.fishManager.gameObject.sfx['fishEscape'].play()

    def exitFlee(self):
        taskMgr.remove('%s_StopFleeing' % self.fish.getName())

    def enterScareAway(self):
        self.fish.velocity[0] = -FishingGlobals.baseFishVelocity[0] * self.fish.myData['speed']

    def exitScareAway(self):
        pass

    def enterEating(self, weightOfFishEaten):
        if self.fish.movingRight:
            self.fish.actor.changeAnimationTo('bite', False)
        else:
            self.fish.actor.changeAnimationTo('biteOpposite', False)
        self.fish.weight += weightOfFishEaten
        self.fish.fishMoveSequence = Sequence(Wait(self.fish.actor.getDuration('bite')), Func(self.request, 'Swimming'), name='%s_MoveSequence' % self.fish.getName())
        self.fish.fishMoveSequence.start()

    def exitEating(self):
        if self.fish.fishMoveSequence:
            self.fish.fishMoveSequence.pause()
            self.fish.fishMoveSequence.clearToInitial()

    def enterBeingEaten(self, fishThatWillEat):
        self.fish.wrtReparentTo(fishThatWillEat.mouthJoint)
        self.fish.fishMoveSequence = Sequence(Parallel(self.fish.posInterval(0.5, Point3(0.0, 0.0, 0.0)), self.fish.scaleInterval(0.5, Point3(0.05, 0.05, 0.05))), Func(self.request, 'Offscreen'), name='%s_MoveSequence' % self.fish.getName())
        self.fish.fishMoveSequence.start()

    def exitBeingEaten(self):
        self.fish.setScale(1.0, 1.0, 1.0)
        if self.fish.fishMoveSequence:
            self.fish.fishMoveSequence.pause()
            self.fish.fishMoveSequence.clearToInitial()

    def requestNext(self, nextState):
        self.request(nextState)