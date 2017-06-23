import random
from direct.interval.IntervalGlobal import Sequence, Parallel, Wait, Func
from pirates.uberdog.UberDogGlobals import InventoryType
from FishingGameFSM import FishingGameFSM
import FishingGlobals
from pirates.audio import SoundGlobals
from direct.fsm import FSM

class LegendaryFishingGameFSM(FSM.FSM):

    def __init__(self, gameObject):
        self.gameObject = gameObject
        FSM.FSM.__init__(self, 'LegendaryFishingGameFSM')
        self.defaultTransitions = {'Offscreen': ['LegdFishShow'],'LegdFishShow': ['Transition', 'Offscreen', 'Win'],'Struggle': ['Transition', 'Offscreen', 'Win'],'ReelingFish': ['Transition', 'Offscreen', 'Win'],'CatchIt': ['GrabHandle', 'Transition', 'Lose', 'Offscreen', 'Win'],'Transition': ['Struggle', 'ReelingFish', 'CatchIt', 'Offscreen', 'Win'],'Win': ['FarewellLegendaryFish', 'Offscreen'],'FarewellLegendaryFish': ['Offscreen']}

    def enterOffscreen(self):
        self.gameObject.lfgGui.resetInterval()
        self.gameObject.cleanLegendaryFishingGameGUI()
        self.gameObject.legendaryFishShowSequence.pause()
        self.gameObject.legendaryFishShowSequence.clearToInitial()
        self.gameObject.lfgFishingHandleGrabSequence.pause()
        self.gameObject.lfgFishingHandleGrabSequence.clearToInitial()
        self.gameObject.cleanLegendaryFishingGameFlags()
        self.gameObject.sfx['legendarySuccess'].stop()
        self.gameObject.sfx['legendaryFail'].stop()

    def exitOffscreen(self):
        self.gameObject.lfgGui.fishingHandleBaseFrame.hide()
        self.gameObject.lfgGui.meterFrame.hide()

    def enterLegdFishShow(self, whichFish=None):
        self.gameObject.tutorialManager.showTutorial(InventoryType.FishingLegendAppear)
        self.gameObject.legendaryFishShow(whichFish)
        base.transitions.loadLetterbox()
        base.transitions.letterboxOn()

    def exitLegdFishShow(self):
        self.gameObject.lfgGui.showAllGUI()
        base.transitions.letterboxOff()

    def enterTransition(self, nextState):
        self.gameObject.lfgGui.setTransitionText(nextState)
        self.lfgMouseInteractionTransitionSequence = Sequence(self.gameObject.lfgGui.transitionTextMovingSequence, Func(self.request, nextState), name=self.gameObject.distributedFishingSpot.uniqueName('lfgMouseInteractionTransitionSequence'))
        self.lfgMouseInteractionTransitionSequence.start()

    def exitTransition(self):
        self.lfgMouseInteractionTransitionSequence.pause()
        self.lfgMouseInteractionTransitionSequence.clearToInitial()

    def enterStruggle(self):
        self.gameObject.lfgGui.fishingRod.setR(FishingGlobals.fishingRodInitSlope)
        self.gameObject.tutorialManager.showTutorial(InventoryType.FishingLegendStruggle)
        self.gameObject.initMouseClickingFlags()
        self.gameObject.fishManager.activeFish.fsm.request('HookedFighting')
        self.gameObject.lfgGui.meterFadeInInterval.start()
        self.accept('mouse1', self.gameObject.checkForMouseClickRate)

    def exitStruggle(self):
        self.ignore('mouse1')
        self.gameObject.sfx['legendaryRed'].stop()
        base.musicMgr.request(SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_MUSIC, priority=0, volume=0.6)
        self.gameObject.lfgGui.meterFadeOutInterval.start()
        self.gameObject.lfgGui.fishingHandleButton.setScale(0.45)

    def enterReelingFish(self):
        self.gameObject.tutorialManager.showTutorial(InventoryType.FishingLegendReel)
        self.gameObject.sfx['lineReelSlow'].setLoop(True)
        self.gameObject.sfx['lineReelSlow'].play()
        self.gameObject.lfgGui.luiArrowRotatingSequence.start()
        self.gameObject.lfgGui.rodFadeInInterval.start()
        lFish = self.gameObject.fishManager.activeFish
        taskName = '%s_StartFighting' % lFish.getName()
        delay = (2.0 - lFish.staminaPercentage()) * random.uniform(lFish.myData['restDurationRange'][0], lFish.myData['restDurationRange'][1])
        if random.random() < lFish.myData['chanceItWillMakeABreakForIt']:
            taskMgr.doMethodLater(delay / 2.0, self.requestNext, name=self.gameObject.distributedFishingSpot.uniqueName(taskName), extraArgs=['Transition', 'CatchIt'])
        else:
            taskMgr.doMethodLater(delay, self.requestNext, name=self.gameObject.distributedFishingSpot.uniqueName(taskName), extraArgs=['Transition', 'Struggle'])

    def requestNext(self, state, nextState):
        if nextState == 'CatchIt':
            self.gameObject.fishManager.activeFish.fsm.request('PullingLure')
        self.request(state, nextState)

    def exitReelingFish(self):
        self.gameObject.sfx['lineReelSlow'].stop()
        self.gameObject.lfgGui.rodFadeOutInterval.start()
        self.gameObject.dragHandleMode = False
        if self.gameObject.lfgReelingFishInterval is not None:
            self.gameObject.lfgReelingFishInterval.pause()
            self.gameObject.lfgReelingFishInterval.clearToInitial()
        return

    def enterCatchIt(self):
        self.gameObject.sfx['legendaryReelSpin'].setLoop(True)
        self.gameObject.sfx['legendaryReelSpin'].play()
        self.gameObject.lfgGui.rodFadeInInterval.start()

    def exitCatchIt(self):
        self.gameObject.sfx['legendaryReelSpin'].stop()
        self.gameObject.lfgGui.rodFadeOutInterval.start()

    def enterWin(self):
        fishId = int(self.gameObject.fishManager.activeFish.myData['id'])
        self.gameObject.distributedFishingSpot.d_caughtFish(fishId, random.randint(self.gameObject.fishManager.activeFish.myData['weightRange'][0] * 100, self.gameObject.fishManager.activeFish.myData['weightRange'][1] * 100))
        self.gameObject.tutorialManager.showTutorial(InventoryType.FishingLegendCaught)
        fishName = self.gameObject.fishManager.activeFish.myData['name']
        self.gameObject.fishManager.activeFish.fsm.request('Offscreen')
        self.lfgWinScreenSequence = Sequence(Func(self.gameObject.distributedFishingSpot.fadeOut), Func(base.musicMgr.requestFadeOut, SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_MUSIC), Wait(self.gameObject.distributedFishingSpot.fadeTime), Func(self.gameObject.distributedFishingSpot.fadeIn), Func(self.gameObject.lfgGui.showWinImage, self.gameObject.fishManager.activeFish), Func(self.gameObject.sfx['legendarySuccess'].play), name=self.gameObject.distributedFishingSpot.uniqueName('lfgWinScreenSequence'))
        self.lfgWinScreenSequence.start()

    def exitWin(self):
        self.lfgWinScreenSequence.pause()
        self.lfgWinScreenSequence.clearToInitial()

    def enterFarewellLegendaryFish(self):
        self.gameObject.hideFishAndBackdrop()
        self.gameObject.fishingLine.hide()
        self.gameObject.lure.hide()
        duration = self.gameObject.fishManager.activeFish.actor.getDuration('swimIdle') * 2
        self.lfgFarewellSequence = Sequence(Func(self.gameObject.distributedFishingSpot.fadeOut), Wait(self.gameObject.distributedFishingSpot.fadeTime), Func(self.gameObject.changeCameraPosHpr), Parallel(Func(self.gameObject.distributedFishingSpot.fadeIn), Func(self.gameObject.fishManager.activeFish.fsm.request, 'FinalBackToSea'), Func(localAvatar.loop, 'emote_wave'), Wait(FishingGlobals.waveToLegendaryFishDuration)), Func(self.gameObject.distributedFishingSpot.requestExit), name=self.gameObject.distributedFishingSpot.uniqueName('lfgFarewellSequence'))
        self.lfgFarewellSequence.start()

    def exitFarewellLegendaryFish(self):
        self.gameObject.sfx['legendarySuccess'].stop()
        self.lfgFarewellSequence.pause()
        self.lfgFarewellSequence.clearToInitial()