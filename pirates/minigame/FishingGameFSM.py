import random
from pirates.piratesbase import PLocalizer, PiratesGlobals
from direct.interval.IntervalGlobal import Sequence, Parallel, Wait, Func
from pirates.uberdog.UberDogGlobals import InventoryType
import FishingGlobals
from direct.fsm import FSM
from pirates.audio import SoundGlobals

class FishingGameFSM(FSM.FSM):

    def __init__(self, gameObject):
        self.gameObject = gameObject
        FSM.FSM.__init__(self, 'FishingGameFSM')
        self.defaultTransitions = {'Offscreen': ['PlayerIdle'],'PlayerIdle': ['ChargeCast', 'Offscreen', 'Recap'],'ChargeCast': ['Cast', 'Offscreen', 'Recap'],'Cast': ['Fishing', 'FishBiting', 'Offscreen', 'Recap'],'Fishing': ['Reeling', 'QuickReel', 'FishBiting', 'Offscreen', 'Recap', 'LureStall', 'LureSink', 'PlayerIdle', 'LegendaryFish', 'Lose'],'Reeling': ['PlayerIdle', 'Fishing', 'QuickReel', 'FishBiting', 'Offscreen', 'Recap', 'LureStall', 'LureSink', 'Lose'],'LureStall': ['Fishing', 'Reeling', 'FishBiting', 'Offscreen', 'LureSink', 'Recap', 'QuickReel'],'LureSink': ['Fishing', 'Reeling', 'FishBiting', 'Offscreen', 'LureStall', 'Recap', 'QuickReel'],'QuickReel': ['PlayerIdle', 'Offscreen', 'Recap'],'FishBiting': ['ReelingFish', 'Offscreen', 'FishOnHook', 'Recap', 'Fishing', 'Reeling', 'LureStall', 'LureSink', 'Lose'],'FishFighting': ['FishOnHook', 'ReelingFish', 'Lose', 'Reward', 'Offscreen'],'FishOnHook': ['FishFighting', 'ReelingFish', 'PulledIn', 'Lose', 'Reward', 'Offscreen', 'Recap'],'ReelingFish': ['FishFighting', 'FishOnHook', 'PulledIn', 'Lose', 'Reward', 'Offscreen', 'Recap'],'Lose': ['Offscreen', 'PlayerIdle', 'Recap'],'Reward': ['PlayerIdle', 'Offscreen', 'Recap'],'PulledIn': ['Recap', 'Offscreen'],'Recap': ['Offscreen'],'LegendaryFish': ['PlayerIdle', 'Lose', 'Offscreen']}
        self.animationSequence = Sequence()
        self.loseCount = 0
        self.firstLineBreak = True

    def enterOffscreen(self):
        taskMgr.remove('mainFishingGameUpdate')
        taskMgr.remove('stopOceanEyeTask')
        taskMgr.remove('stopPullTask')
        taskMgr.remove(self.gameObject.distributedFishingSpot.uniqueName('testLegendaryFishingGameLaterTask'))
        base.localAvatar.guiMgr.gameGui.show()
        if base.localAvatar.getTutorialState() >= PiratesGlobals.TUT_GOT_COMPASS:
            base.localAvatar.guiMgr.radarGui.show()
        base.localAvatar.guiMgr.targetStatusTray.show()
        base.localAvatar.guiMgr.crewHUD.setHUDOn()
        base.localAvatar.guiMgr.crewHUDTurnedOff = False
        base.localAvatar.guiMgr.profilePage.show()
        base.localAvatar.guiMgr.showTrackedQuestInfo()
        base.localAvatar.guiMgr.combatTray.tonicButton.show()
        base.localAvatar.guiMgr.showTrays()
        base.localAvatar.guiMgr.setIgnoreEscapeHotKey(True)
        base.localAvatar.fishingGameHook = None
        self.gameObject.hideScene()
        self.gameObject.gui.hideGui()
        self.gameObject.fishManager.shutdown()
        self.gameObject.oceanEye = False
        self.gameObject.lure.showHelpText(None)
        self.gameObject.sfx['ambience'].stop()
        self.animationSequence.pause()
        self.animationSequence.clearToInitial()
        base.cam.reparentTo(self.gameObject.fishingSpot)
        if self.gameObject.lfgFsm.getCurrentOrNextState() != 'Offscreen':
            self.gameObject.lfgFsm.request('Offscreen')
        base.musicMgr.requestFadeOut(SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_MUSIC)
        for n in render.findAllMatches('**/*nametag3d*'):
            n.show()

        if localAvatar.ship:
            localAvatar.ship.showMasts()
        return

    def exitOffscreen(self):
        self.loseCount = 0
        base.localAvatar.guiMgr.gameGui.hide()
        base.localAvatar.guiMgr.radarGui.hide()
        base.localAvatar.guiMgr.targetStatusTray.hide()
        base.localAvatar.guiMgr.contextTutPanel.hide()
        base.localAvatar.guiMgr.crewHUD.setHUDOff()
        base.localAvatar.guiMgr.crewHUDTurnedOff = True
        base.localAvatar.guiMgr.hideMinimap()
        base.localAvatar.guiMgr.profilePage.hide()
        base.localAvatar.guiMgr.hideTrackedQuestInfo()
        base.localAvatar.guiMgr.combatTray.tonicButton.hide()
        base.localAvatar.guiMgr.moneyDisplay.hide()
        if base.localAvatar.getCrewShip():
            base.localAvatar.getCrewShip().hideStatusDisplay()
            base.localAvatar.getCrewShip().hideTargets()
        if self.gameObject.distributedFishingSpot.onABoat:
            localAvatar.ship.shipStatusDisplay.hide()
        if base.localAvatar.guiMgr.mainMenu:
            base.localAvatar.guiMgr.mainMenu.abruptHide()
        base.localAvatar.guiMgr.setIgnoreEscapeHotKey(False)
        base.localAvatar.fishingGameHook = self.gameObject
        self.gameObject.hookedIt = False
        self.gameObject.showScene()
        self.gameObject.gui.showGui()
        self.gameObject.fishManager.startup()
        for n in render.findAllMatches('**/*nametag3d*'):
            n.hide()

        if localAvatar.ship:
            localAvatar.ship.hideMasts()
        taskMgr.add(self.gameObject.updateFishingGame, sort=30, name='mainFishingGameUpdate')

    def enterPlayerIdle(self):
        taskMgr.remove(self.gameObject.distributedFishingSpot.uniqueName('testLegendaryFishingGameLaterTask'))
        taskMgr.remove('shaderTickUpdate')
        self.gameObject.lure.lureModel.setR(-20)
        self.gameObject.tutorialManager.showTutorial(InventoryType.FishingEnterGame)
        self.gameObject.lure.showHelpText(None)
        self.animationSequence.pause()
        self.animationSequence.clearToInitial()
        self.gameObject.resetScene()
        self.gameObject.gui.resetGui()
        self.gameObject.fishManager.reset()
        self.gameObject.legendaryFishingGameEnable = False
        self.gameObject.oceanEye = False
        base.cam.reparentTo(self.gameObject.fishingSpot)
        self.gameObject.sfx['ambience'].stop()
        self.gameObject.fishManager.deadFish = []
        self.gameObject.hideFishAndBackdrop()
        if self.gameObject.rewardSequence is not None:
            self.gameObject.rewardSequence.finish()
        localAvatar.loop('fsh_idle')
        self.accept('mouse1', self.gameObject.canCast)
        return

    def exitPlayerIdle(self):
        self.gameObject.resetSceneParallel.pause()
        self.gameObject.resetSceneParallel.clearToInitial()
        self.gameObject.gui.tackleBoxButton.hide()
        self.gameObject.gui.lureSelectionPanel.hide()
        taskMgr.add(self.gameObject.shaderTickUpdate, 'shaderTickUpdate')
        self.ignore('mouse1')

    def enterChargeCast(self):
        self.gameObject.lineHealth = FishingGlobals.maxLineHealth
        if self.gameObject.resetSceneParallel is not None:
            self.gameObject.resetSceneParallel.finish()
        self.gameObject.gui.startPowerMeter()
        taskMgr.add(self.gameObject.gui.updateCastPowerMeterTask, 'updateCastPowerMeterTask')
        self.accept('mouse1', self.request, ['Cast'])
        return

    def exitChargeCast(self):
        taskMgr.remove('updateCastPowerMeterTask')
        self.ignore('mouse1')

    def enterCast(self):
        self.gameObject.lureAngle = FishingGlobals.lureSinkingAngles['Cast']
        self.gameObject.castLure()
        self.gameObject.sfx['castSmall'].play()

    def exitCast(self):
        self.gameObject.lure.setHpr(0.0, 0.0, 0.0)
        self.gameObject.castSeq.pause()
        self.gameObject.castSeq.clearToInitial()
        self.gameObject.testForLegendaryFish()

    def enterFishing(self):
        if self.gameObject.fishManager.activeFish is None:
            self.gameObject.lureAngle = FishingGlobals.lureSinkingAngles['Fishing']
        self.gameObject.tutorialManager.showTutorial(InventoryType.FishingAfterCast)
        self.gameObject.gui.toggleGuiElements()
        self.gameObject.showFishAndBackdrop()
        if self.gameObject.sfx['ambience'].status() == 1:
            self.gameObject.sfx['ambience'].setLoop(True)
            self.gameObject.sfx['ambience'].play()
        self.accept('mouse1', self.request, ['Reeling'])
        self.accept('space', self.request, ['QuickReel'])
        return

    def exitFishing(self):
        self.gameObject.lure.setHpr(0.0, 0.0, 0.0)
        self.ignore('mouse1')
        self.ignore('space')

    def enterReeling(self):
        self.gameObject.bumpLure()
        if self.gameObject.fishManager.activeFish is None:
            self.gameObject.lureAngle = FishingGlobals.lureSinkingAngles['Reeling']
        self.gameObject.fishManager.enterReeling()
        self.gameObject.scareFish = True
        self.gameObject.sfx['lineReelSlow'].setLoop(True)
        self.gameObject.sfx['lineReelSlow'].play()
        reelSpeed = FishingGlobals.fishingLevelToReelSpeed.get(self.gameObject.currentFishingLevel, 1.0)
        if reelSpeed == 1.0 and self.gameObject.currentFishingLevel > 20:
            reelSpeed = FishingGlobals.fishingLevelToReelSpeed.get(20, 1.0)
        self.gameObject.reelVelocityMultiplier = reelSpeed
        self.accept('mouse1-up', self.request, ['Fishing'])
        self.accept('space', self.request, ['QuickReel'])
        return

    def exitReeling(self):
        self.gameObject.lure.setHpr(0.0, 0.0, 0.0)
        self.gameObject.sfx['lineReelSlow'].stop()
        self.gameObject.reelVelocityMultiplier = 1.0
        self.ignore('mouse1-up')
        self.ignore('space')

    def enterLureStall(self):
        stallTime = FishingGlobals.fishingLevelToStallDuration.get(self.gameObject.currentFishingLevel, 1.0)
        if stallTime == 1.0 and self.gameObject.currentFishingLevel > 20:
            stallTime = FishingGlobals.fishingLevelToStallDuration.get(20, 1.0)
        taskMgr.doMethodLater(stallTime, self.gameObject.stopLureStallTask, name='stopLureStallTask')
        self.accept('mouse1', self.request, ['Reeling'])
        self.accept('space', self.request, ['QuickReel'])

    def exitLureStall(self):
        taskMgr.remove('stopLureStallTask')
        self.ignore('mouse1')
        self.ignore('space')

    def enterLureSink(self):
        taskMgr.doMethodLater(FishingGlobals.lureSinkDuration, self.gameObject.stopLureSinkTask, name='stopLureSinkTask')
        self.accept('mouse1', self.request, ['Reeling'])
        self.accept('space', self.request, ['QuickReel'])

    def exitLureSink(self):
        taskMgr.remove('stopLureSinkTask')
        self.ignore('mouse1')
        self.ignore('space')

    def enterQuickReel(self):
        self.gameObject.lureAngle = FishingGlobals.lureSinkingAngles['QuickReel']
        self.gameObject.fishManager.loseInterest()
        self.gameObject.sfx['lineReelFast'].setLoop(True)
        self.gameObject.sfx['lineReelFast'].play()

    def exitQuickReel(self):
        self.gameObject.lure.setHpr(0.0, 0.0, 0.0)
        self.gameObject.sfx['lineReelFast'].stop()

    def enterFishBiting(self):
        self.gameObject.tutorialManager.showTutorial(InventoryType.FishingAboutToBite)
        if self.gameObject.distributedFishingSpot.showTutorial:
            self.gameObject.lure.showHelpText(PLocalizer.Minigame_Fishing_Lure_Alerts['click'])
        self.accept('mouse1', self.gameObject.checkForHookSuccess)

    def exitFishBiting(self):
        if self.gameObject.distributedFishingSpot.showTutorial:
            if self.getCurrentOrNextState() in ['ReelingFish', 'FishOnHook']:
                self.gameObject.lure.showHelpText(PLocalizer.Minigame_Fishing_Lure_Alerts['perfect'])
            else:
                self.gameObject.lure.showHelpText(PLocalizer.Minigame_Fishing_Lure_Alerts['toolate'])
        self.ignore('mouse1')

    def enterReward(self):
        taskMgr.remove('shaderTickUpdate')
        self.loseCount = 0
        base.cam.reparentTo(self.gameObject.fishingSpot)
        self.gameObject.tutorialManager.showTutorial(InventoryType.FishingCaughtFish)
        self.gameObject.lure.showHelpText(None)
        self.gameObject.distributedFishingSpot.showTutorial = False
        self.gameObject.sfx['ambience'].stop()
        if self.gameObject.fishManager.activeFish.myData['size'] in ['small', 'medium']:
            self.animationSequence = Sequence(Wait(0.4), Func(localAvatar.loop, 'fsh_smallSuccess'), Wait(localAvatar.getDuration('fsh_smallSuccess')), Func(localAvatar.loop, 'fsh_idle'), Wait(1.0))
            self.animationSequence.loop()
        else:
            localAvatar.loop('fsh_bigSuccess')
        i = random.randint(0, 2)
        if self.gameObject.fishManager.activeFish.myData['size'] == 'small':
            if i == 0:
                self.gameObject.sfx['fishOutSmall01'].play()
            elif i == 1:
                self.gameObject.sfx['fishOutSmall02'].play()
            else:
                self.gameObject.sfx['fishOutSmall03'].play()
        elif self.gameObject.fishManager.activeFish.myData['size'] == 'medium':
            if i == 0:
                self.gameObject.sfx['fishOutMedium01'].play()
            elif i == 1:
                self.gameObject.sfx['fishOutMedium02'].play()
            else:
                self.gameObject.sfx['fishOutMedium01'].play()
        elif self.gameObject.fishManager.activeFish.myData['size'] == 'large':
            if i == 0:
                self.gameObject.sfx['fishOutLarge01'].play()
            elif i == 1:
                self.gameObject.sfx['fishOutLarge02'].play()
            else:
                self.gameObject.sfx['fishOutLarge03'].play()
        self.gameObject.sfx['successCaught'].play()
        fishId = int(self.gameObject.fishManager.activeFish.myData['id'])
        self.gameObject.distributedFishingSpot.d_caughtFish(fishId, self.gameObject.fishManager.activeFish.weight)
        self.gameObject.oceanEye = False
        self.gameObject.playRewardSequence()
        self.gameObject.fishManager.activeFish.actor.loop('reelIdle')
        self.gameObject.fishManager.activeFish.setY(0.0)
        self.gameObject.fishManager.activeFish.setHpr(0.0, 0.0, 0.0)
        self.gameObject.fishManager.activeFish.fishStatusIconNodePath.hide()
        self.gameObject.hideFishAndBackdrop()
        self.gameObject.fishManager.activeFish.show()
        self.gameObject.fishManager.activeFish.actor.show()
        taskMgr.remove('%s_StartFighting' % self.gameObject.fishManager.activeFish.getName())
        taskMgr.remove('%s_StopFighting' % self.gameObject.fishManager.activeFish.getName())
        taskMgr.remove('%s_GoFighting' % self.gameObject.fishManager.activeFish.getName())
        return

    def exitReward(self):
        self.gameObject.fishManager.caughtFish += 1
        self.gameObject.fishManager.replaceFish(self.gameObject.fishManager.activeFish)
        localAvatar.guiMgr.combatTray.skillTray.rebuildSkillTray()
        localAvatar.guiMgr.combatTray.initCombatTray()

    def enterFishOnHook(self):
        self.gameObject.tutorialManager.showTutorial(InventoryType.FishingFishOnLine)
        self.accept('mouse1', self.request, ['ReelingFish'])

    def exitFishOnHook(self):
        self.ignore('mouse1')

    def enterReelingFish(self):
        self.gameObject.sfx['lineReelSlow'].setLoop(True)
        self.gameObject.sfx['lineReelSlow'].play()
        self.accept('mouse1-up', self.request, ['FishOnHook'])

    def exitReelingFish(self):
        self.gameObject.sfx['lineReelSlow'].stop()
        self.ignore('mouse1-up')

    def enterFishFighting(self):
        pass

    def exitFishFighting(self):
        if self.gameObject.distributedFishingSpot.showTutorial:
            self.gameObject.lure.showHelpText(PLocalizer.Minigame_Fishing_Lure_Alerts['clickhold'])

    def enterLose(self):
        taskMgr.remove('stopOceanEyeTask')
        taskMgr.remove('stopPullTask')
        taskMgr.remove('stopLureStallTask')
        taskMgr.remove('stopLureSinkTask')
        inv = localAvatar.getInventory()
        rodLvl = inv.getItemQuantity(InventoryType.FishingRod)
        self.loseCount += 1
        if self.loseCount >= FishingGlobals.resetTutorialCount:
            self.gameObject.distributedFishingSpot.showTutorial = True
            if self.firstLineBreak:
                self.firstLineBreak = False
                self.gameObject.tutorialManager.showTutorial(InventoryType.FishingLineBroken, 2)
            else:
                self.gameObject.tutorialManager.showTutorial(InventoryType.FishingLineBroken2, 2)
        self.gameObject.lineHealth = FishingGlobals.maxLineHealth
        self.gameObject.sfx['ambience'].stop()
        type = self.gameObject.lure.currentLureType
        if type == 'regular':
            lureId = InventoryType.RegularLure
        if type == 'legendary':
            lureId = InventoryType.LegendaryLure
        self.gameObject.distributedFishingSpot.d_lostLure(lureId)
        self.gameObject.lure.setLureType(None)
        if self.gameObject.fishManager.activeFish.fsm.getCurrentOrNextState() not in ['Offscreen', 'Flee']:
            self.gameObject.fishManager.activeFish.wrtReparentTo(self.gameObject.fishingSpot)
            self.gameObject.fishManager.activeFish.setHpr(0.0, 0.0, 0.0)
            self.gameObject.fishManager.activeFish.fsm.request('Flee')
            self.gameObject.fishManager.activeFish = None
        self.gameObject.lure.showHelpText(PLocalizer.Minigame_Fishing_Lure_Alerts['snap'])
        return

    def exitLose(self):
        self.gameObject.sfx['legendaryFail'].stop()

    def enterPulledIn(self):
        self.gameObject.enterPulledIn()

    def exitPulledIn(self):
        self.gameObject.exitPulledIn()

    def enterRecap(self):
        self.gameObject.enterRecap()

    def exitRecap(self):
        self.gameObject.exitRecap()

    def enterLegendaryFish(self):
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_MINIGAME_FISHING)
        base.musicMgr.request(SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_MUSIC, priority=2, volume=0.6)

    def exitLegendaryFish(self):
        base.musicMgr.requestFadeOut(SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_MUSIC)
        base.musicMgr.request(SoundGlobals.MUSIC_MINIGAME_FISHING, looping=True, priority=1)