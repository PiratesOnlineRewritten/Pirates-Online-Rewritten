import random
import math
from panda3d.core import CullBinManager
from pandac.PandaModules import NodePath, CardMaker, Point3, LineSegs, Vec3, Vec4, Vec2, GraphicsStateGuardian
from direct.interval.IntervalGlobal import Sequence, Parallel, Wait, Func
from direct.interval.MetaInterval import Parallel
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.ProjectileInterval import ProjectileInterval
from direct.showbase import DirectObject
from direct.actor.Actor import Actor
from direct.task import Task
from otp.otpgui import OTPDialog
from direct.gui.DirectGui import DirectWaitBar, DGG
from direct.gui.DirectGui import DirectButton, DirectFrame
from direct.interval.IntervalGlobal import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.inventory import ItemGlobals
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import TODGlobals
import FishingGlobals
from FishingGameFSM import FishingGameFSM
from FishManager import FishManager
from FishingGameGUI import FishingGameGUI
from LegendaryFishingGameGUI import LegendaryFishingGameGUI
from FishLure import FishLure
from FishingTutorialManager import FishingTutorialManager
from LegendaryFishingGameFSM import LegendaryFishingGameFSM
from pirates.effects.SeaBottomBubbleEffect import SeaBottomBubbleEffect
from pirates.effects.LureHittingWaterBubbleEffect import LureHittingWaterBubbleEffect
from pirates.effects.PooledEffect import PooledEffect
from pirates.effects.LightRay import LightRay
from pandac.PandaModules import MouseButton
from pirates.minigame.LegendaryTellGUI import LegendaryTellGUI
from pirates.world.LocationConstants import LocationIds
from direct.fsm.FSM import RequestDenied
from pirates.seapatch.Water import Water

class FishingGame(DirectObject.DirectObject):

    def __init__(self, distributedFishingSpot=None):
        base.fishingGame = self
        self.accept('onCodeReload', self.codeReload)
        self.lureAngle = 0
        self.lureForceTarget = 0
        self.lureCurrForce = 0
        self.wantLeg = False
        self.forceTarget = Vec2(-0.1, 0.1)
        self.currForce = Vec2(0, 0)
        self.boundaryTarget = Vec2(0, 0)
        self.currBoundary = Vec2(0, 0)
        self.cbm = CullBinManager.getGlobalPtr()
        self.distributedFishingSpot = distributedFishingSpot
        self.fishingSpot = NodePath('fishingSpot')
        self.gui = FishingGameGUI(self)
        self.lfgGui = LegendaryFishingGameGUI(self)
        self.setupScene()
        self.fishManager = FishManager(self)
        base.loadingScreen.beginStep('rest', 3, 20)
        self.tutorialManager = FishingTutorialManager()
        PooledEffect.poolLimit = 50
        self.currentFishingLevel = self.getPlayerFishingLevel()
        self.setupCamera()
        base.loadingScreen.tick()
        base.localAvatar.bindAnim('fsh_smallCast')
        base.localAvatar.bindAnim('fsh_bigCast')
        base.localAvatar.bindAnim('fsh_idle')
        base.localAvatar.bindAnim('fsh_smallSuccess')
        base.localAvatar.bindAnim('fsh_bigSuccess')
        if self.distributedFishingSpot.onABoat:
            waterOffset = FishingGlobals.waterLevelOffset['boat']
        else:
            waterOffset = FishingGlobals.waterLevelOffset['land']
        self.boatFishingCameraOffset = Point3(0.0, 0.0, 0.0)
        if self.distributedFishingSpot.onABoat:
            if self.distributedFishingSpot.index == 0:
                self.distributedFishingSpot.oceanOffset = 13.3
                self.boatFishingCameraOffset = FishingGlobals.boatSpotIndexToCameraOffset[self.distributedFishingSpot.index]
            if self.distributedFishingSpot.index == 1:
                self.distributedFishingSpot.oceanOffset = 13.3
                self.boatFishingCameraOffset = FishingGlobals.boatSpotIndexToCameraOffset[self.distributedFishingSpot.index]
            if self.distributedFishingSpot.index == 2:
                self.distributedFishingSpot.oceanOffset = 13.3
                self.boatFishingCameraOffset = FishingGlobals.boatSpotIndexToCameraOffset[self.distributedFishingSpot.index]
            if self.distributedFishingSpot.index == 3:
                self.distributedFishingSpot.oceanOffset = 13.3
                self.boatFishingCameraOffset = FishingGlobals.boatSpotIndexToCameraOffset[self.distributedFishingSpot.index]
            if self.distributedFishingSpot.index == 4:
                self.distributedFishingSpot.oceanOffset = 13.3
                self.boatFishingCameraOffset = FishingGlobals.boatSpotIndexToCameraOffset[self.distributedFishingSpot.index]
            if self.distributedFishingSpot.index == 5:
                self.distributedFishingSpot.oceanOffset = 13.3
                self.boatFishingCameraOffset = FishingGlobals.boatSpotIndexToCameraOffset[self.distributedFishingSpot.index]
        self.waterLevel = waterOffset - self.distributedFishingSpot.oceanOffset
        self.castDistance = 0.0
        self.stateToNextStateWhenLureIsDone = {'Reeling': 'PlayerIdle','QuickReel': 'PlayerIdle','Fishing': 'PlayerIdle','ReelingFish': 'Reward','FishOnHook': 'Reward','Lose': 'PlayerIdle'}
        base.loadingScreen.tick()
        self.levelAtCastStart = None
        self.lineHealth = FishingGlobals.maxLineHealth
        self.resetSceneParallel = None
        self.castSeq = None
        self.rewardSequence = None
        self.hookedIt = False
        self.reelVelocityMultiplier = 1.0
        self.attractionCollisionVisualsVisible = False
        self.avoidanceCollisionVisualsVisible = False
        self.scareFish = False
        self.oceanEye = False
        self.restoreFish = False
        self.prevClickingTime = 0.0
        self.initClicking = False
        self.halfwayAround = False
        self.lastRodRotationValue = 0.0
        self.dragHandleMode = False
        self.initDrag = False
        self.elapsedReelingTime = 0.0
        self.legendaryFishShowSequence = Sequence()
        self.lfgFishingHandleGrabSequence = Sequence()
        self.enterReelingFishStateSequence = Sequence()
        self.lfgReelingFishInterval = None
        self.lightRays = []
        self.lureStallTime = 0
        self.fsm = FishingGameFSM(self)
        self.lfgFsm = LegendaryFishingGameFSM(self)
        self.fsm.request('Offscreen')
        base.loadingScreen.endStep('rest')
        self.accept('open_main_window', self.windowChanged)
        self.accept('inventoryQuantity-%s-%s' % (localAvatar.getInventoryId(), InventoryType.RegularLure), self.gui.updateLureQuantities)
        self.accept('inventoryQuantity-%s-%s' % (localAvatar.getInventoryId(), InventoryType.LegendaryLure), self.gui.updateLureQuantities)
        return

    def shaderTickUpdate(self, task):
        dt = globalClock.getDt()
        time = globalClock.getFrameTime()
        tick = time % 10
        render.setShaderInput('timeInfo', Vec4(dt, time, tick, 0.0))
        return task.cont

    def handleSpinningSpeedBaseOnFishStamina(self, dt):
        return FishingGlobals.handleSpinningSpeed * self.fishManager.activeFish.myData['speed'] * self.fishManager.activeFish.staminaPercentage() * dt * 20.0

    def getFishStruggleForceBaseOnStamina(self, dt):
        return FishingGlobals.fishingRodInclineDegree * self.fishManager.activeFish.myData['strength'] * (1 + self.fishManager.activeFish.staminaPercentage() * 0.6) * dt * 20.0

    def fishingRodPullbyHumanDegree(self):
        return FishingGlobals.humanPulledfishingRodBackDegree * 0.4

    def getSwimSpeedBaseOnFishStamina(self, currentState, dt):
        return FishingGlobals.lureVelocities[currentState] * dt * (self.fishManager.activeFish.staminaPercentage() * 0.5 + 0.5)

    def setAsOceanEyeMode(self):
        if self.oceanEye:
            return
        self.toggleOceanEye()

    def swapFSM(self, a, b):
        return (
         b, a)

    def changeCameraPosHpr(self):
        base.cam.setPos(FishingGlobals.cameraPosLegendaryFinal)
        base.cam.setHpr(FishingGlobals.cameraHprLegendaryFinal)

    def cleanLegendaryFishingGameFlags(self):
        self.dragHandleMode = False
        self.elapsedReelingTime = 0.0

    def cleanLegendaryFishingGameGUI(self):
        if self.lfgGui is None:
            return
        self.lfgGui.hideAllGUI()
        base.localAvatar.guiMgr.combatTray.skillTray.show()
        return

    def setLegendaryRodDangerSound(self, playSound):
        if playSound:
            if self.sfx['legendaryRed'].status() != 2:
                self.sfx['legendaryRed'].setLoop(True)
                self.sfx['legendaryRed'].play()
            a = FishingGlobals.loseFishingRodAngle
            b = FishingGlobals.struggleDangerThreshold
            c = self.lfgGui.fishingRod.getR()
            if c == a:
                return
            percentToFail = (c - b) / float(a - b)
            base.musicMgr.requestChangeVolume(SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_MUSIC, 0.1, percentToFail * 0.2 + 0.6)
            self.sfx['legendaryRed'].setVolume(percentToFail * 4)
        else:
            if self.sfx['legendaryRed'].status() is 1:
                return
            self.sfx['legendaryRed'].stop()
            base.musicMgr.requestChangeVolume(SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_MUSIC, 0.1, 0.6)

    def testForLegendaryFish(self, task=None):
        if self.distributedFishingSpot.onABoat and self.fsm.state == 'Fishing' and (self.wantLeg or self.fishManager.caughtFish > 0 and self.lure.currentLureType is not None and self.lure.currentLureType is 'legendary') and self.lure.getX() > FishingGlobals.lurePositionRangesForLegendaryFishingGame['xRange'][0] and self.lure.getX() < FishingGlobals.lurePositionRangesForLegendaryFishingGame['xRange'][1] and self.lure.getZ() < FishingGlobals.lurePositionRangesForLegendaryFishingGame['zRange'][0] and self.lure.getZ() > FishingGlobals.lurePositionRangesForLegendaryFishingGame['zRange'][1]:
            if self.wantLeg or random.random() < FishingGlobals.legendaryFishShowChance:
                self.startLegendaryFishingGame(self.wantLeg)
                taskMgr.remove('testLegendaryFishingGameLaterTask')
                return
        taskMgr.doMethodLater(FishingGlobals.timeBetweenLegendaryFishTests, self.testForLegendaryFish, self.distributedFishingSpot.uniqueName('testLegendaryFishingGameLaterTask'))
        return

    def startLegendaryFishingGame(self, whichFish=None):
        if self.fsm.getCurrentOrNextState() == 'LegendaryFish' or self.fishManager.activeFish is not None:
            return
        self.gui.hideGui()
        base.localAvatar.guiMgr.combatTray.skillTray.hide()
        self.fsm.request('LegendaryFish')
        self.lfgFsm.request('LegdFishShow', whichFish)
        taskMgr.remove('testLegendaryFishingGameLaterTask')
        return

    def pauseLegendaryFishingGame(self):
        self.lfgGui.hideAllGUI()
        self.fsm, self.oldFSM = self.swapFSM(self.fsm, self.oldFSM)
        oldState = self.oldFSM.getCurrentOrNextState()
        self.oldFSM.request('Pause')
        self.fsm.request(oldState)

    def resumeLegendaryFishingGame(self):
        self.fsm, self.oldFSM = self.swapFSM(self.fsm, self.oldFSM)
        self.oldFSM.request('Pause')
        self.fsm.request('Fishing')
        self.lfgGui.showAllGUI()

    def loseLegendaryFishingGame(self):
        self.fishManager.activeFish.fsm.request('Offscreen')
        self.sfx['legendaryFail'].play()
        self.lfgFsm.request('Offscreen')
        self.fsm.request('Lose')
        self.fishManager.loadFish()
        self.restoreFish = True

    def legendaryFishShow(self, whichFish=None):
        self.fishManager.scareAwayNormalFish()
        self.legendaryFishShowSequence = Sequence(Wait(FishingGlobals.legendaryMusicIntroDuration), Func(self.setAsOceanEyeMode), Wait(FishingGlobals.legendaryFishArrivalDelay), Func(self.fishManager.startLegendaryFish, whichFish), name=self.distributedFishingSpot.uniqueName('legendaryFishShowSequence'))
        self.legendaryFishShowSequence.start()

    def initMouseClickingFlags(self):
        self.saveFishingRod = 0
        self.prevClickingTime = globalClock.getFrameTime()
        self.startStruggleTime = globalClock.getFrameTime()
        taskMgr.doMethodLater(0.05, self.checkStruggle, 'checkStruggle')

    def checkForMouseClickRate(self):
        now = globalClock.getFrameTime()
        elapsedTime = now - self.prevClickingTime
        self.prevClickingTime = now
        if elapsedTime < FishingGlobals.clickingRateThreshold:
            self.saveFishingRod += 1

    def moveRodBasedOnClicks(self, task):
        return Task.cont

    def fishingHandleTurning(self, dt, currentState):
        if not base.mouseWatcherNode.hasMouse():
            return
        newR = math.degrees(math.atan2(self.lfgGui.fishingHandle.getX() - base.mouseWatcherNode.getMouseX(), self.lfgGui.fishingHandle.getZ() - base.mouseWatcherNode.getMouseY()))
        self.lfgGui.fishingHandle.setR(newR)
        if not self.halfwayAround:
            if self.lastRodRotationValue > 120.0 and newR < 120.0:
                self.halfwayAround = True
        elif self.lastRodRotationValue < 0.0 and newR > 0.0 and newR < 90.0:
            weight = self.fishManager.activeFish.weight
            newX = max(FishingGlobals.leftLureBarrier, self.lure.getX() + (15.0 - weight) * self.reelVelocityMultiplier * FishingGlobals.lureVelocities[currentState][0] * dt)
            newZ = max(-self.castDistance, min(self.lure.getZ() + (15.0 - weight) * self.reelVelocityMultiplier * FishingGlobals.lureVelocities[currentState][2] * dt, self.waterLevel))
            duration = self.elapsedReelingTime
            self.elapsedReelingTime = 0.0
            self.lfgReelingFishInterval = LerpPosInterval(self.lure, duration, Point3(newX, -1.0, newZ), self.lure.getPos(), blendType='easeInOut', name=self.distributedFishingSpot.uniqueName('lfgReelingFishInterval'))
            self.lfgReelingFishInterval.start()
            self.halfwayAround = False
        self.lastRodRotationValue = newR
        self.elapsedReelingTime += dt

    def toggleAvoidanceCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            self.avoidanceCollisionVisualsVisible = not self.avoidanceCollisionVisualsVisible
            if self.avoidanceCollisionVisualsVisible:
                self.fishManager.showAvoidanceCollisionVisuals()
            else:
                self.fishManager.hideAvoidanceCollisionVisuals()

    def toggleAttractionCollisionVisuals(self):
        if FishingGlobals.wantDebugCollisionVisuals:
            self.attractionCollisionVisualsVisible = not self.attractionCollisionVisualsVisible
            if self.attractionCollisionVisualsVisible:
                self.fishManager.showAttractionCollisionVisuals()
                self.lure.showCollisionVisuals()
            else:
                self.fishManager.hideAttractionCollisionVisuals()
                self.lure.hideCollisionVisuals()

    def codeReload(self):
        reload(FishingGlobals)
        self.fishManager.loseInterest()
        if FishingGlobals.wantDebugCollisionVisuals:
            self.fishManager.reloadCollisions()
        self.fishManager.codeReload()
        self.setupCamera()

    def windowChanged(self):
        base.cam.reparentTo(self.fishingSpot)

    def setupCamera(self):
        if self.distributedFishingSpot.onABoat:
            self.fishingSpot.reparentTo(self.distributedFishingSpot)
            self.fishingSpot.setPos(self.distributedFishingSpot.getPos())
        else:
            self.fishingSpot.reparentTo(localAvatar.getParent())
            self.fishingSpot.setPos(self.distributedFishingSpot.getPos(localAvatar.getParent()))
            self.fishingSpot.setHpr(self.distributedFishingSpot.getHpr(localAvatar.getParent()))
            self.fishingSpot.setH(self.fishingSpot.getH() - 90.0)

    def delete(self):
        self.ignoreAll()
        if self.backdropTransitionIval:
            self.backdropTransitionIval.pause()
            self.backdropTransitionIval = None
        self.stopLightRays()
        self.stopSeaBottomBubbles()
        PooledEffect.poolLimit = 30
        if self.fsm.getCurrentOrNextState() not in ['Offscreen', 'Off']:
            self.fsm.request('Offscreen')
        self.gui.destroy()
        self.gui = None
        self.fishManager.destroy()
        self.lfgGui.hideAllGUI()
        self.lfgGui.destroy()
        self.lfgGui = None
        self.fishingSpot.removeNode()
        self.backdrop.removeNode()
        self.lure.destroy()
        self.fishingLine.removeNode()
        self.distributedFishingSpot = None
        taskMgr.remove('checkStruggle')
        taskMgr.remove('stopOceanEyeTask')
        taskMgr.remove('stopPullTask')
        taskMgr.remove('stopLureStallTask')
        taskMgr.remove('stopLureSinkTask')
        return

    def setupScene(self):
        base.loadingScreen.beginStep('SetupScene', 3, 20)
        self.sfx = {'biteLarge': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_BITE_LARGE),'biteSmall': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_BITE_SMALL),'biteAlert': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_BITE_ALERT),'fishEscape': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_FISH_ESCAPE),'fishFight01': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_FISH_FIGHT_01),'fishFight02': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_FISH_FIGHT_02),'fishOutLarge01': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_FISH_OUT_LARGE_01),'fishOutLarge02': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_FISH_OUT_LARGE_02),'fishOutLarge03': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_FISH_OUT_LARGE_03),'fishOutSmall01': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_FISH_OUT_SMALL_01),'fishOutSmall02': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_FISH_OUT_SMALL_02),'fishOutSmall03': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_FISH_OUT_SMALL_03),'fishOutMedium01': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_FISH_OUT_MEDIUM_01),'fishOutMedium02': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_FISH_OUT_MEDIUM_02),'castLarge': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_CAST_LARGE),'castSmall': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_CAST_SMALL),'lureEquip': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_LURE_EQUIP),'successCaught': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_SUCCESS_CAUGHT),'usability': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_USABILITY),'ambience': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_AMBIENCE),'legendaryReelSpin': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_REEL_SPIN),'lineReelFast': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_LINE_REEL_FAST),'lineReelSlow': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_LINE_REEL_SLOW),'legendaryGreen': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_GREEN),'legendaryRed': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_RED),'legendarySuccess': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_SUCCESS),'legendaryFail': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_LEGENDARY_FAIL),'lureHit': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_LURE_HIT),'lureOut': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_LURE_OUT),'reelEnd': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_REEL_END),'rodOut': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_ROD_OUT),'rodPutAway': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_ROD_PUT_AWAY),'fishingSkill': loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_SKILL)}
        base.loadingScreen.tick()
        self.backdrop = loader.loadModel('models/minigames/pir_m_gam_fsh_fishEnvironment')
        self.backdrop.findAllMatches('**/lightRay*').detach()
        self.backdrop.reparentTo(self.fishingSpot)
        self.backdrop.setTransparency(1, 1000)
        self.backdrop.setFogOff()
        self.backdrop.setLightOff()
        self.backdropTransitionIval = None
        self.transitionBackdrop()
        if self.distributedFishingSpot.onABoat:
            self.backdrop.setPos(35.0, 8.0, -86.0 - self.distributedFishingSpot.oceanOffset)
        else:
            self.backdrop.setPos(25.0, 8.0, -86.0 - self.distributedFishingSpot.oceanOffset)
        self.backdrop.setHpr(0.0, 0.0, 0.0)
        self.seaBottomBubbleEffects = []
        self.cbm.addBin('fishingGame', CullBinManager.BTFixed, 30)
        self.backdrop.setBin('fishingGame', 0)
        self.backdrop.find('**/environment').setBin('fishingGame', 1)
        self.backdrop.setDepthWrite(True)
        self.backdrop.setDepthTest(True)
        base.loadingScreen.tick()
        self.lure = FishLure(self, 'regular')
        self.lure.lureModel.setBin('fishingGame', 10)
        self.setupLine(Point3(0, 0, 0), Point3(0, 1, 0))
        self.sandfloors = render.findAllMatches('**/sandfloor')
        base.loadingScreen.endStep('SetupScene')
        return None

    def startSeaBottomBubbles(self):
        fishBarrierDist = FishingGlobals.rightFishBarrier - FishingGlobals.leftFishBarrier
        numEmitters = 9
        startX = FishingGlobals.leftFishBarrier - 1.0
        zDepth = -75
        spread = fishBarrierDist / numEmitters
        for i in range(numEmitters):
            effect = SeaBottomBubbleEffect.getEffect(unlimited=True)
            if effect:
                self.seaBottomBubbleEffects.append(effect)
                effect.startLoop()
                effect.p0.factory.setLifespanBase(30)
                effect.reparentTo(self.fishingSpot)
                effect.setPos(spread * i + startX, 0, zDepth)
                effect.particleDummy.setBin('fishingGame', 5)

        numEmitters = 5
        startX = FishingGlobals.leftFishBarrier + 3.5
        zDepth = -50
        spread = fishBarrierDist / numEmitters
        for i in range(numEmitters):
            effect = SeaBottomBubbleEffect.getEffect(unlimited=True)
            if effect:
                self.seaBottomBubbleEffects.append(effect)
                effect.startLoop()
                effect.p0.factory.setLifespanBase(22)
                effect.reparentTo(self.fishingSpot)
                effect.setPos(spread * i + startX, 0, zDepth)
                effect.particleDummy.setBin('fishingGame', 5)

        numEmitters = 6
        startX = FishingGlobals.leftFishBarrier - 5.0
        zDepth = -35
        spread = (fishBarrierDist + 15.0) / numEmitters
        for i in range(numEmitters):
            effect = SeaBottomBubbleEffect.getEffect(unlimited=True)
            if effect:
                self.seaBottomBubbleEffects.append(effect)
                effect.startLoop()
                effect.p0.factory.setLifespanBase(16)
                effect.reparentTo(self.fishingSpot)
                effect.setPos(spread * i + startX, 0, -35)
                effect.particleDummy.setBin('fishingGame', 5)

    def stopSeaBottomBubbles(self):
        for effect in self.seaBottomBubbleEffects:
            effect.detachNode()
            effect.stopLoop()

        self.seaBottomBubbleEffects = []

    def hideSeaBottomBubbles(self):
        for effect in self.seaBottomBubbleEffects:
            effect.hide()

    def showSeaBottomBubbles(self):
        for effect in self.seaBottomBubbleEffects:
            effect.show()

    def resetScene(self):
        self.lure.resetLureModel()
        self.lure.wrtReparentTo(self.endOfRod)
        self.lure.setHpr(0.0, 0.0, 0.0)
        lureResetInterval = LerpPosInterval(self.lure, FishingGlobals.resetDuration, Point3(0.0, 0.0, 0.0))
        self.fishingLine.show()
        self.lure.show()
        self.resetSceneParallel = Parallel(lureResetInterval, name='resetScene')
        self.resetSceneParallel.start()

    def hideScene(self):
        self.oceanEye = False
        base.cam.reparentTo(self.fishingSpot)
        if self.resetSceneParallel is not None:
            self.resetSceneParallel.pause()
            self.resetSceneParallel.clearToInitial()
        if self.castSeq is not None:
            self.castSeq.pause()
            self.castSeq.clearToInitial()
        if self.rewardSequence is not None:
            self.rewardSequence.pause()
            self.rewardSequence.clearToInitial()
        self.backdrop.reparentTo(hidden)
        self.lure.resetLureModel()
        self.lure.reparentTo(hidden)
        self.fishingLine.reparentTo(hidden)
        for floor in self.sandfloors:
            floor.show()

        self.stopLightRays()
        self.stopSeaBottomBubbles()
        self.verifyWaterReflections()
        self.ignore('options_reflections_change')
        return

    def showScene(self):
        self.backdrop.reparentTo(self.fishingSpot)
        self.endOfRod = base.localAvatar.find('**/fishingRod').find('**/end_of_rod')
        self.endOfRod.wrtReparentTo(base.localAvatar.find('**/fishingRod'))
        base.localAvatar.find('**/fishingRod').setHpr(0.0, 0.0, -90.0)
        self.lure.reparentTo(self.endOfRod)
        self.fishingLine.reparentTo(self.fishingSpot)
        base.cam.setPos(FishingGlobals.stateToCameraOffsetInfo['PlayerIdle'][0] + self.boatFishingCameraOffset)
        self.lure.resetLureModel()
        self.lure.reparentTo(self.endOfRod)
        self.lure.setScale(1, 1, 1)
        self.lure.setPosHpr(0, 0, 0, 0, 0, 0)
        for floor in self.sandfloors:
            floor.hide()

        self.startLightRays()
        self.startSeaBottomBubbles()

    def hideFishAndBackdrop(self):
        for fish in self.fishManager.uncaughtFish:
            fish.hide()

        self.backdrop.hide()
        self.hideLightRays()
        self.hideSeaBottomBubbles()
        self.verifyWaterReflections()
        self.ignore('options_reflections_change')

    def showFishAndBackdrop(self):
        for fish in self.fishManager.uncaughtFish:
            fish.show()

        self.backdrop.show()
        self.showLightRays()
        self.showSeaBottomBubbles()
        self.turnWaterReflectionsOff()
        self.accept('options_reflections_change', self.turnWaterReflectionsOff)

    def updateLine(self, startPoint, endPoint, color):
        self.fishingLine.setPos(startPoint)
        self.fishingLine.lookAt(endPoint)
        self.lengthOfLine = (endPoint - startPoint).length()
        self.fishingLine.setScale(1, self.lengthOfLine, 1)
        self.fishingLine.setColorScale(*color)

    def setupLine(self, startPoint, endPoint):
        self.line = LineSegs()
        self.fishingLine = None
        self.line.setColor(*FishingGlobals.defaultFishingLineColor)
        self.line.setThickness(FishingGlobals.fishingLineThickness)
        self.line.moveTo(startPoint)
        self.line.drawTo(endPoint)
        self.fishingLine = self.fishingSpot.attachNewNode(self.line.create())
        self.fishingLine.setTransparency(True)
        self.fishingLine.setBin('fishingGame', 10)
        self.fishingLine.setDepthWrite(False)
        self.fishingLine.setDepthTest(False)
        self.fishingLine.setLightOff()
        return

    def getLineColorBasedOnHealth(self):
        return FishingGlobals.fishingLineHealthToColor[int(self.lineHealth / 100.0 * (len(FishingGlobals.fishingLineHealthToColor) - 1))]

    def updateFishingGame(self, task):
        dt = task.time
        currentState = None
        if self.fsm.state in ['PlayerIdle', 'ChargeCast', 'Reward']:
            self.lureAngle = 0
        else:
            lureVec = self.lure.getPos() - self.endOfRod.getPos()
            lureVec.normalize()
            self.lureAngle = -(180 - math.degrees(math.atan2(lureVec.getX(), lureVec.getZ())))
        lureR = self.lure.lureModel.getR()
        if lureR > self.lureAngle:
            lureSign = 1
            self.lureForceTarget -= 5
        else:
            lureSign = 0
            self.lureForceTarget += 5
        self.lureCurrForce += (self.lureForceTarget - self.lureCurrForce) * 0.5
        self.lure.lureModel.setR(self.lure.lureModel.getR() + self.lureCurrForce * dt)
        if self.lure.lureModel.getR() > self.lureAngle and not lureSign or self.lure.lureModel.getR() < self.lureAngle and lureSign:
            if abs(self.lureForceTarget) > 10:
                self.lureForceTarget *= 0.6
                self.lureCurrForce *= 0.6
        if self.fsm.getCurrentOrNextState() == 'LegendaryFish':
            currentState = self.lfgFsm.getCurrentOrNextState()
            if currentState in ['ReelingFish']:
                self.fishingHandleTurning(dt, currentState)
                if int(self.lure.getX()) <= int(FishingGlobals.leftLureBarrier) and int(self.lure.getZ()) >= int(self.waterLevel):
                    self.lfgFsm.request('Win')
            elif currentState in ['Struggle']:
                self.lfgGui.fishingRod.setR(self.lfgGui.fishingRod.getR() + self.getFishStruggleForceBaseOnStamina(dt))
                currentTime = globalClock.getFrameTime()
                timeLeft = int(math.ceil(FishingGlobals.maxStruggleTime - (currentTime - self.startStruggleTime)))
                percent = (FishingGlobals.maxStruggleTime - (currentTime - self.startStruggleTime)) / FishingGlobals.maxStruggleTime
                self.lfgGui.updateStruggleTimerText(timeLeft, percent)
                if self.lfgGui.fishingRod.getR() > FishingGlobals.struggleDangerThreshold or timeLeft <= FishingGlobals.struggleTimeDangerThreshold:
                    self.setLegendaryRodDangerSound(True)
                else:
                    self.setLegendaryRodDangerSound(False)
                if self.lfgGui.fishingRod.getR() >= FishingGlobals.loseFishingRodAngle:
                    self.lfgFsm.request('Transition', 'CatchIt')
                    self.fishManager.activeFish.fsm.request('PullingLure')
                elif currentTime - self.startStruggleTime > FishingGlobals.maxStruggleTime:
                    self.lfgFsm.request('Transition', 'CatchIt')
                    self.fishManager.activeFish.fsm.request('PullingLure')
            elif currentState in ['CatchIt']:
                moveSpeed = self.getSwimSpeedBaseOnFishStamina(currentState, dt)
                speed = self.fishManager.activeFish.myData['speed']
                newX = max(FishingGlobals.leftLureBarrier, self.lure.getX() + speed * moveSpeed[0])
                newZ = min(max(FishingGlobals.fishingLevelBoundariesBoat[len(FishingGlobals.fishingLevelBoundariesBoat) - 1], self.lure.getZ() + speed * moveSpeed[2]), self.waterLevel)
                self.lure.setPos(newX, -1.0, newZ)
                self.lfgGui.fishingHandle.setR(self.lfgGui.fishingHandle.getR() - self.handleSpinningSpeedBaseOnFishStamina(dt))
                if self.lure.getX() >= FishingGlobals.rightFishBarrier:
                    self.loseLegendaryFishingGame()
        else:
            currentState = self.fsm.getCurrentOrNextState()
            if currentState in ['Fishing', 'Reeling', 'QuickReel', 'ReelingFish', 'Lose', 'FishOnHook']:
                self.currBoundary += (self.boundaryTarget - self.currBoundary) * 0.25
                self.currForce += (self.forceTarget - self.currForce) * 0.25
                if (self.forceTarget - self.currForce).length() < 0.01:
                    self.forceTarget = Vec2(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1))
                newX = self.lure.getX() + (self.reelVelocityMultiplier * FishingGlobals.lureVelocities[currentState][0] + self.currBoundary[0] + self.currForce[0]) * dt
                if newX < FishingGlobals.leftLureBarrier:
                    self.boundaryTarget[0] += 0.3
                elif self.boundaryTarget[0] > 0:
                    self.boundaryTarget[0] = max(0, self.boundaryTarget[0] - 0.4)
                newZ = min(self.lure.getZ() + (self.reelVelocityMultiplier * FishingGlobals.lureVelocities[currentState][2] + self.currBoundary[1] + self.currForce[1]) * dt, self.waterLevel)
                if newZ < -self.castDistance or currentState == 'Fishing' and newZ < FishingGlobals.fishingLevelBoundaries[self.getRodLevel() - 1]:
                    self.boundaryTarget[1] += 0.1
                elif self.boundaryTarget[1] > 0:
                    self.boundaryTarget[1] = max(0, self.boundaryTarget[1] - 0.3)
                self.lure.setPos(newX, -1.0, newZ)
                if int(self.lure.getX()) <= int(FishingGlobals.leftLureBarrier) and int(self.lure.getZ()) >= int(self.waterLevel):
                    self.sfx['lureOut'].play()
                    self.sfx['reelEnd'].play()
                    self.fsm.request(self.stateToNextStateWhenLureIsDone[currentState])
            else:
                if currentState in ['LureSink']:
                    newZ = max(-self.castDistance, min(self.lure.getZ() + self.reelVelocityMultiplier * FishingGlobals.lureVelocities[currentState][2] * dt, self.waterLevel))
                    newZ = max(newZ, FishingGlobals.fishingLevelBoundaries[len(FishingGlobals.fishingLevelBoundaries) - 1])
                    self.lure.setPos(self.lure.getX(), -1.0, newZ)
                elif currentState in ['FishFighting']:
                    newX = self.lure.getX() + FishingGlobals.lureVelocities[currentState][0] * dt * self.fishManager.activeFish.myData['speed']
                    self.lure.setX(newX)
                    if newX > FishingGlobals.rightLureBarrier:
                        self.fsm.request('Lose')
                        return Task.again
                    if base.mouseWatcherNode.isButtonDown(MouseButton.one()):
                        self.lineHealth = self.lineHealth - self.fishManager.activeFish.myData['strength']
                        self.gui.updateLineHealthMeter(self.lineHealth)
                        if self.lineHealth <= 0:
                            self.fsm.request('Lose')
                            return Task.again
                        if self.lineHealth <= FishingGlobals.maxLineHealth * 0.5:
                            self.tutorialManager.showTutorial(InventoryType.FishingLineHealth)
                lineLength = self.lure.getDistance(self.endOfRod)
                currentState = self.fsm.getCurrentOrNextState()
                if currentState != 'Lose':
                    self.gui.lineLengthLabel.showText(str(int(lineLength)), (1, 1,
                                                                             1, 1))
            startPoint = self.endOfRod.getPos(self.fishingSpot)
            endPoint = self.lure.lureModel.getPos(self.fishingSpot)
            currentState = self.fsm.getCurrentOrNextState()
            if currentState in ['FishOnHook', 'ReelingFish', 'FishFighting', 'LegendaryFish']:
                endPoint = self.lure.lureModel.getPos(self.fishingSpot)
                self.updateLine(startPoint, endPoint, self.getLineColorBasedOnHealth())
            else:
                endPoint = self.lure.getPos(self.fishingSpot)
                self.updateLine(startPoint, endPoint, Vec4(0.3, 0.3, 1.0, 0.5))
            self.fishManager.update(dt)
            if self.lfgFsm.getCurrentOrNextState() in ['Win', 'FarewellLegendaryFish']:
                return Task.again
            camPos = base.cam.getPos()
            cameraOffset = FishingGlobals.stateToCameraOffsetInfo[currentState][0] + self.boatFishingCameraOffset
            if self.oceanEye:
                goalPos = Point3(*FishingGlobals.oceanEyeCameraPosition)
                camRange = (0, 1, 2)
            elif FishingGlobals.stateToCameraOffsetInfo[currentState][2]:
                goalPos = self.lure.getPos()
                goalPos[1] = cameraOffset[1]
                camRange = (0, 1, 2)
            elif FishingGlobals.stateToCameraOffsetInfo[currentState][1] and self.fishManager.activeFish is not None:
                goalPos = self.fishManager.activeFish.mouthJoint.getPos(self.fishingSpot)
                if self.fishManager.activeFish.myData['size'] == 'large':
                    goalPos[1] = cameraOffset[1] - 5.0
                elif self.fishManager.activeFish.myData['size'] == 'medium':
                    goalPos[1] = cameraOffset[1]
                else:
                    goalPos[1] = cameraOffset[1] + 5.0
                camRange = (0, 1, 2)
            else:
                goalPos = Point3(cameraOffset)
                camRange = (0, 1, 2)
            for i in camRange:
                goalPos[i] = camPos[i] * (1.0 - dt * 5.0) + goalPos[i] * dt * 5.0

        base.cam.setPos(goalPos)
        return Task.again

    def checkStruggle(self, task=None):
        currentState = self.lfgFsm.getCurrentOrNextState()
        if currentState != 'Struggle':
            return Task.done
        self.lfgGui.fishingRod.setR(self.lfgGui.fishingRod.getR() - self.fishingRodPullbyHumanDegree() * self.saveFishingRod)
        self.saveFishingRod = 0
        if self.lfgGui.fishingRod.getR() <= FishingGlobals.saveFishingRodAngle:
            self.lfgFsm.request('Transition', 'ReelingFish')
            self.fishManager.activeFish.fsm.request('Hooked')
            self.sfx['legendaryGreen'].play()
            return Task.done
        return Task.cont

    def toggleOceanEye(self):
        self.oceanEye = not self.oceanEye

    def castLure(self):
        self.levelAtCastStart = self.getPlayerFishingLevel()
        if self.gui.castMeterBar.getSz() * 100.0 < FishingGlobals.minimumCastDistance:
            self.gui.castMeterBar.setSz(FishingGlobals.minimumCastDistance / 100)
        if self.restoreFish:
            self.restoreFish = False
            self.fishManager.startup()
        self.castDistance = self.gui.castMeterBar.getSz() * 100 * FishingGlobals.castDistanceMultiplier[localAvatar.currentWeaponId]
        if self.distributedFishingSpot.onABoat:
            self.castDistance += FishingGlobals.minimumCastDistanceOnABoat
        else:
            self.castDistance += FishingGlobals.minimumCastDistance
        if self.castDistance > FishingGlobals.maxCastDistance:
            self.castDistance = FishingGlobals.maxCastDistance
        bestRod = self.getAvatarsBestRod()
        if bestRod == -1:
            notify.error('Somehow the avatar got into the fishing game without a rod in their inventory!')
        castAnim = 'fsh_smallCast'
        if bestRod == ItemGlobals.FISHING_ROD_3:
            if self.gui.castMeterBar.getSz() * 100 > 50:
                castAnim = 'fsh_bigCast'
        self.castTime = FishingGlobals.lureFlightDuration[castAnim] + self.castDistance * 0.01
        FishingGlobals.stateToCameraOffsetInfo['Cast'][2] = False
        if self.distributedFishingSpot.onABoat:
            FishingGlobals.stateToCameraOffsetInfo['Cast'][0][1] = -48.0
            self.castTime += 0.5
        self.castSeq = Sequence(Func(localAvatar.play, castAnim), Wait(FishingGlobals.castReleaseDelay[castAnim]), Func(self.lureTrajectory, castAnim), Parallel(Wait(self.castTime), Sequence(Wait(self.castTime - 1.0), Func(self.startHitWaterBubbleEffect))), Func(self.sfx['lureHit'].play), Func(self.fsm.request, 'Fishing'), name='castLure')
        self.castSeq.start()

    def startHitWaterBubbleEffect(self):
        self.hitWaterBubbleEffect = LureHittingWaterBubbleEffect.getEffect(unlimited=True)
        if self.hitWaterBubbleEffect:
            self.hitWaterBubbleEffect.reparentTo(self.fishingSpot)
            self.hitWaterBubbleEffect.setPos(self.castDistance - 1.5, 0.0, self.waterLevel + 1.5)
            self.hitWaterBubbleEffect.particleDummy.setBin('fishingGame', 5)
            self.hitWaterBubbleEffect.play()

    def lureTrajectory(self, anim):
        self.lure.wrtReparentTo(self.fishManager.objectsWithCaustics)
        self.lure.setHpr(0.0, 0.0, 0.0)
        trajectory = ProjectileInterval(self.lure, startPos=self.lure.getPos(), endPos=Point3(self.castDistance, 0.0, self.waterLevel), duration=self.castTime)
        trajectory.start()
        FishingGlobals.stateToCameraOffsetInfo['Cast'][2] = True

    def checkForHookSuccess(self):
        if self.fishManager.activeFish.fsm.getCurrentOrNextState() == 'Biting':
            self.fishManager.activeFish.fishStatusIconTextNode.setText('!')
            self.fishManager.activeFish.fishStatusIconTextNode.setTextColor(1.0, 0.0, 0.0, 1.0)
            self.hookedIt = True
            self.checkForHooked()

    def checkForHooked(self):
        if self.fsm.getCurrentOrNextState() == 'LegendaryFish':
            self.attachFishToLure()
            self.fishManager.activeFish.fishStaminaConsume()
            self.fishManager.loseInterest()
            self.lfgFsm.request('Transition', 'Struggle')
        elif self.fsm.getCurrentOrNextState() == 'FishBiting':
            if self.hookedIt:
                self.hookedIt = False
                self.attachFishToLure()
                if base.mouseWatcherNode.isButtonDown(MouseButton.one()):
                    self.fsm.request('ReelingFish')
                else:
                    self.fsm.request('FishOnHook')
                self.fishManager.loseInterest()
            else:
                if self.fishManager.activeFish.fsm.getCurrentOrNextState() != 'Flee':
                    self.fishManager.activeFish.fsm.request('Flee')
                self.lure.showHelpText(PLocalizer.Minigame_Fishing_Lure_Alerts['scaredOff'])
                if self.fishManager.activeFish.myData['size'] != 'small':
                    self.fsm.request('Lose')
                else:
                    self.fishManager.activeFish = None
                    if base.mouseWatcherNode.isButtonDown(MouseButton.one()):
                        self.fsm.request('Reeling')
                    else:
                        self.fsm.request('Fishing')
                self.fishManager.activeFish = None
        else:
            if self.fishManager.activeFish.fsm and self.fishManager.activeFish.fsm.getCurrentOrNextState() != 'Flee':
                self.fishManager.activeFish.fsm.request('Flee')
            self.fishManager.activeFish = None
        return

    def attachFishToLure(self):
        self.fishManager.activeFish.fsm.request('Hooked')
        self.lure.lureModel.hide()
        self.lure.lureModel.reparentTo(self.fishManager.activeFish.mouthJoint)
        self.fishManager.activeFish.reparentTo(self.lure)
        self.fishManager.activeFish.setPos(self.fishManager.activeFish.mouthJoint.getPos() * -1.0)
        self.fishManager.activeFish.setHpr(0.0, 0.0, 0.0)

    def playRewardSequence(self):
        self.lure.wrtReparentTo(self.endOfRod)
        self.fishManager.activeFish.setPos(self.fishManager.activeFish.mouthJoint.getPos() * -1.0)
        self.gui.showRewardDialog(self.fishManager.activeFish)
        self.rewardSequence = Parallel(self.lure.hprInterval(FishingGlobals.rewardSequenceReelItInDuration, Point3(*FishingGlobals.fishToLureHprOffset)), self.lure.posInterval(FishingGlobals.rewardSequenceReelItInDuration, Point3(0.0, 0.0, 0.0)), name='FishingGameRewardSequence')
        self.rewardSequence.start()

    def useAbility(self, skillId):
        self.lure.enableLureGlow(skillId)
        self.sfx['fishingSkill'].play()
        if skillId == InventoryType.FishingRodStall:
            try:
                self.fsm.request('LureStall')
            except RequestDenied:
                raise StandardError, 'Requesting LureStall from state %s\nTime Difference between LureStall Requests: %s' % (self.fsm.getCurrentOrNextState(), globalClock.getFrameTime() - self.lureStallTime)

            self.lureStallTime = globalClock.getFrameTime()
        if skillId == InventoryType.FishingRodPull:
            speedMult = FishingGlobals.fishingLevelToPullSpeedBoost.get(self.currentFishingLevel, 1.0)
            if speedMult == 1.0 and self.currentFishingLevel > 20:
                speedMult = FishingGlobals.fishingLevelToPullSpeedBoost.get(20, 1.0)
            self.reelVelocityMultiplier = speedMult
            taskMgr.doMethodLater(FishingGlobals.pullDuration, self.stopPullTask, 'stopPullTask')
        if skillId == InventoryType.FishingRodHeal:
            amountToHeal = FishingGlobals.fishingLevelToHealAmount.get(self.currentFishingLevel, 1.0)
            if amountToHeal == 1.0 and self.currentFishingLevel > 20:
                amountToHeal = FishingGlobals.fishingLevelToHealAmount.get(20, 1.0)
            self.lineHealth += amountToHeal
            if self.lineHealth > FishingGlobals.maxLineHealth:
                self.lineHealth = FishingGlobals.maxLineHealth
            self.gui.updateLineHealthMeter(self.lineHealth)
        if skillId == InventoryType.FishingRodTug:
            if self.fsm.getCurrentOrNextState() in ['FishFighting']:
                self.fishManager.activeFish.fsm.request('Hooked')
        if skillId == InventoryType.FishingRodSink:
            self.fsm.request('LureSink')
        if skillId == InventoryType.FishingRodOceanEye:
            self.toggleOceanEye()
            taskMgr.doMethodLater(FishingGlobals.oceanEyeDuration, self.stopOceanEyeTask, 'stopOceanEyeTask')

    def stopLureStallTask(self, task):
        self.fsm.request('Fishing')
        return Task.done

    def stopLureSinkTask(self, task):
        self.fsm.request('Fishing')
        return Task.done

    def stopOceanEyeTask(self, task):
        self.toggleOceanEye()
        return Task.done

    def stopPullTask(self, task):
        self.reelVelocityMultiplier = 1.0
        return Task.done

    def chooseLure(self, type):
        if type == InventoryType.RegularLure:
            self.lure.setLureType('regular')
        elif type == InventoryType.LegendaryLure:
            self.lure.setLureType('legendary')
        self.lure.lureModel.setBin('fishingGame', 10)

    def pickWeightedItem(self, itemList):
        x = random.uniform(0, 100)
        for item, weight in itemList:
            if x < weight:
                break
            x = x - weight

        return item

    def canCast(self):
        if self.hasLures():
            if self.lure.currentLureType is not None:
                self.fsm.request('ChargeCast')
            else:
                localAvatar.guiMgr.createWarning(PLocalizer.FishingNoLureEquipped, PiratesGuiGlobals.TextFG6)
        else:
            localAvatar.guiMgr.createWarning(PLocalizer.FishingNoLuresWarning, PiratesGuiGlobals.TextFG6)
        return

    def hasLures(self):
        inv = localAvatar.getInventory()
        regular = inv.getStackQuantity(InventoryType.RegularLure)
        legendary = inv.getStackQuantity(InventoryType.LegendaryLure)
        if regular + legendary <= 0:
            return False
        else:
            return True

    def getRodLevel(self):
        inv = localAvatar.getInventory()
        return inv.getItemQuantity(InventoryType.FishingRod)

    def getAvatarsBestRod(self):
        inv = localAvatar.getInventory()
        rodLvl = inv.getItemQuantity(InventoryType.FishingRod)
        if rodLvl == 3:
            return ItemGlobals.FISHING_ROD_3
        if rodLvl == 2:
            return ItemGlobals.FISHING_ROD_2
        if rodLvl == 1:
            return ItemGlobals.FISHING_ROD_1
        return -1

    def getPlayerFishingLevel(self):
        inv = localAvatar.getInventory()
        repAmt = inv.getAccumulator(InventoryType.FishingRep)
        repLvl = ReputationGlobals.getLevelFromTotalReputation(InventoryType.FishingRep, repAmt)
        return repLvl[0]

    def getPredictedPlayerFishingLevel(self, repIncrease):
        inv = localAvatar.getInventory()
        repAmt = inv.getAccumulator(InventoryType.FishingRep) + repIncrease
        repLvl = ReputationGlobals.getLevelFromTotalReputation(InventoryType.FishingRep, repAmt)
        return repLvl[0]

    def startLightRays(self):
        self.lightRays = []
        xOffset = 0
        if self.distributedFishingSpot.onABoat:
            waterLevel = self.waterLevel + 10.0
        else:
            waterLevel = self.waterLevel
        for i in range(16):
            lightRay = LightRay.getEffect()
            if lightRay:
                lightRay.reparentTo(self.fishingSpot)
                lightRay.setBin('fishingGame', 3)
                lightRay.setPos(xOffset, random.randint(20, 32), waterLevel)
                lightRay.setR(-25)
                lightRay.startLoop()
                self.lightRays.append(lightRay)
                xOffset += random.randint(5, 10)

    def stopLightRays(self):
        for ray in self.lightRays:
            ray.stopLoop()

        self.lightRays = []

    def showLightRays(self):
        for ray in self.lightRays:
            ray.show()

    def hideLightRays(self):
        for ray in self.lightRays:
            ray.hide()

    def transitionBackdrop(self, stateId=None, stateDuration=0.0, elapsedTime=0.0, transitionTime=0.0):
        if self.backdropTransitionIval:
            self.backdropTransitionIval.pause()
            self.backdropTransitionIval = None
        todMgr = base.cr.timeOfDayManager
        fromState = todMgr.lastState
        toState = todMgr.currentState
        usesShader = base.config.GetBool('want-shaders', 1) and base.win and base.win.getGsg() and base.win.getGsg().getShaderModel() >= GraphicsStateGuardian.SM20
        if usesShader and self.distributedFishingSpot.onABoat:
            usesShader = 2
        elif usesShader and localAvatar.getParentObj().getUniqueId() == LocationIds.DEL_FUEGO_ISLAND:
            usesShader = 3
        fromColor = FishingGlobals.todBackdropColor[fromState][usesShader]
        toColor = FishingGlobals.todBackdropColor[toState][usesShader]
        if not elapsedTime and todMgr.transitionIval:
            elapsedTime = todMgr.transitionIval.getT()
        if not transitionTime and todMgr.transitionIval:
            transitionTime = todMgr.transitionIval.getDuration()
        self.backdropTransitionIval = LerpFunctionInterval(self.backdrop.setColorScale, duration=transitionTime, toData=toColor, fromData=fromColor)
        self.backdropTransitionIval.start(elapsedTime)
        self.accept('timeOfDayChange', self.transitionBackdrop)
        return

    def turnWaterReflectionsOff(self, setting=0):
        Water.all_reflections_off()

    def verifyWaterReflections(self):
        reflectionSetting = base.options.reflection
        if reflectionSetting == 0:
            Water.all_reflections_off()
        elif reflectionSetting == 1:
            Water.all_reflections_show_through_only()
        elif reflectionSetting == 2:
            Water.all_reflections_on()

    def bumpLure(self):
        lureR = self.lure.lureModel.getR()
        if lureR > self.lureAngle:
            self.lureCurrForce -= 40
            self.lureForceTarget -= 40
        else:
            self.lureCurrForce += 40
            self.lureForceTarget += 40

    def checkLures(self):
        inv = localAvatar.getInventory()
        if not inv or not inv.getStackQuantity(InventoryType.RegularLure):
            self.lure.setLureType(None)
            self.gui.toggleLureSelectionDialog()
        return

    def updateResultsScreen(self):
        self.gui.resultsScreen.updateGoldAndXpBonus()