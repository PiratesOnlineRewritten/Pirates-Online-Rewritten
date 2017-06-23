import random
import math
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.fsm import FSM
from direct.task import Task
from direct.showbase.PythonUtil import lerp, report, getShortestRotation
from direct.directnotify.DirectNotifyGlobal import directNotify
from libotp import NametagGlobals
from pirates.battle import WeaponGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import EmoteGlobals
from pirates.reputation import ReputationGlobals
from pirates.interact import InteractiveBase
from pirates.inventory import ItemGlobals
from pirates.effects.TeleportTwister import TeleportTwister
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui.RewardPanel import RewardPanel
from PlayerPirateGameFSM import PlayerPirateGameFSM
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class LocalPirateGameFSM(PlayerPirateGameFSM):
    notify = directNotify.newCategory('LocalPirateGameFSM')

    def __init__(self, av):
        PlayerPirateGameFSM.__init__(self, av, 'LocalPirateGameFSM')
        self.enterBattleEvent = 'enemyTargeted'
        self.setDefaultGameState()
        self.teleportTrack = None
        self.teleportEffect = None
        self.doorWalkTrack = None
        self.kickTrack = None
        self.enterTunnelSequence = None
        self.preTunnelState = None
        self.lockFSM = False
        self.camIval = None
        self.savedPos = None
        self.savedHpr = None
        self.savedNPCHpr = None
        self.interactNPC = None
        self.rewardPanel = None
        return

    def cleanup(self):
        PlayerPirateGameFSM.cleanup(self)
        if self.teleportTrack:
            self.teleportTrack.pause()
            self.teleportTrack = None
        if self.teleportEffect:
            self.teleportEffect.cleanUpEffect()
            self.teleportEffect = None
        if self.doorWalkTrack:
            self.doorWalkTrack.pause()
            self.doorWalkTrack = None
        if self.kickTrack:
            self.kickTrack.pause()
            self.kickTrack = None
        if self.deathTrack:
            self.deathTrack.pause()
            self.deathTrack = None
        if self.camIval:
            self.camIval.pause()
            self.camIval = None
        return

    def turnNameTagsOff(self):
        self.av.guiMgr.profilePage.hide()
        for n in render.findAllMatches('**/*nametag3d*'):
            n.hide()

    def turnNameTagsOn(self):
        self.av.guiMgr.profilePage.show()
        for n in render.findAllMatches('**/*nametag3d*'):
            n.show()

    def setDefaultGameState(self, state='LandRoam'):
        self.defaultState = state

    def defaultFilter(self, request, args):
        if self.lockFSM:
            if request in ('LandRoam', 'NPCInteract', 'Emote'):
                return None
        if request == 'Battle':
            noBattleStates = ('Death', 'ShipBoarding', 'Ensnared', 'Thrown', 'Knockdown',
                              'ThrownInJail', 'Unconcious', 'ParlorGame', 'Fishing',
                              'PVPWait', 'EnterTunnel', 'Injured', 'Dying')
            if self.defaultState not in ('Battle', ):
                noBattleStates += ('WaterRoam', )
            if self.state in noBattleStates:
                return None
            if self.state in ('Cannon', 'NPCInteract', 'Digging', 'Searching', 'ShipPilot',
                              'DinghyInteract', 'ShipRepair', 'BenchRepair', 'PotionCrafting'):
                messenger.send(InteractiveBase.END_INTERACT_EVENT)
                return ('Battle', ) + args
            if self.state in 'Dialog':
                return ('Battle', ) + args
        if self.state == 'Death':
            if request not in ('Off', 'ThrownInJail', 'Unconcious', 'TeleportIn', 'TeleportOut',
                               'LandRoam', 'PVPWait', 'PVPComplete'):
                return None
        elif self.state == 'TeleportOut':
            if request in ('NPCInteract', 'DinghyInteract', 'DoorInteract'):
                return None
        return PlayerPirateGameFSM.defaultFilter(self, request, args)

    def enterOff(self, extraArgs=[]):
        self.av.cameraFSM.request('Off')
        PlayerPirateGameFSM.enterOff(self, extraArgs)

    @report(types=['deltaStamp'], dConfigParam='teleport')
    def enterLandRoam(self, extraArgs=[]):
        PlayerPirateGameFSM.enterLandRoam(self)
        self.accept('localAvatarEnterWater', self.handleLocalAvatarEnterWater)
        base.cr.interactionMgr.start()
        self.av.speedIndex = PiratesGlobals.SPEED_NORMAL_INDEX
        self.av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[self.av.speedIndex])
        self.av.guiMgr.request('Interface')
        self.av.controlManager.use('walk', self.av)
        self.av.controlManager.get('walk').lifter.setGravity(32.174 * 2.0)
        self.av.collisionsOn()
        self.av.startListenAutoRun()
        self.av.setLifterDelayFrames(3)
        self.av.cameraFSM.request('FPS')
        self.av.startChat()
        self.av.show()
        self.accept(WeaponGlobals.LocalAvatarUseItem, self.av.composeRequestTargetedSkill)
        if self.av.ship:
            self.av.setSurfaceIndex(PiratesGlobals.SURFACE_WOOD)
        else:
            self.av.setSurfaceIndexFromLevelDefault()
        self.av.guiMgr.combatTray.showWeapons()
        self.av.enableMouseWeaponDraw()
        self.av.updatePlayerSpeed()
        self.av.delayAFK()

    def exitLandRoam(self):
        self.ignore('localAvatarEnterWater')
        base.cr.interactionMgr.stop()
        self.ignore(WeaponGlobals.LocalAvatarUseItem)
        PlayerPirateGameFSM.exitLandRoam(self)
        self.av.disableMouseWeaponDraw()
        self.av.stopListenAutoRun()

    def enterWaterRoam(self, extraArgs=[]):
        self.accept('localAvatarExitWater', self.handleLocalAvatarExitWater)
        if self.av.setWeaponIval and self.av.setWeaponIval.isPlaying():
            self.av.setWeaponIval.finish()
        self.av.speedIndex = PiratesGlobals.SPEED_NORMAL_INDEX
        self.av.guiMgr.request('Interface')
        self.av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[self.av.speedIndex])
        self.av.controlManager.use('walk', self.av)
        self.av.controlManager.get('walk').setGravity(0.0)
        self.av.controlManager.get('walk').setVelocity(0.0)
        self.av.physControls.disableJump()
        self.av.startBobSwimTask()
        self.av.startListenAutoRun()
        base.cr.interactionMgr.start()
        self.av.cameraFSM.request('FPS')
        self.av.show()
        self.av.setSurfaceIndex(PiratesGlobals.SURFACE_WATER)
        self.av.b_setTeleportFlag(PiratesGlobals.TFInWater, self.av.confirmSwimmingTeleport)
        PlayerPirateGameFSM.enterWaterRoam(self)
        self.av.updatePlayerSpeed()
        self.av.delayAFK()

    def exitWaterRoam(self):
        self.ignore('localAvatarExitWater')
        self.av.controlManager.get('walk').setGravity(32.174 * 2.0)
        self.av.physControls.enableJump()
        self.av.stopBobSwimTask()
        self.av.stopListenAutoRun()
        base.cr.interactionMgr.stop()
        self.ignore(WeaponGlobals.LocalAvatarUseItem)
        self.av.b_clearTeleportFlag(PiratesGlobals.TFInWater)
        PlayerPirateGameFSM.exitWaterRoam(self)

    def enterUnconcious(self, extraArgs=[]):
        PlayerPirateGameFSM.enterUnconcious(self)
        self.av.collisionsOff()
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('Control')
        base.transitions.letterboxOn()
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.lock()
        self.av.stopAutoRun()
        camera.setPos(self.av, 0.5, -14, 6)
        camera.wrtReparentTo(self.av.getParent())
        camera.lookAt(self.av.headNode)
        task = taskMgr.add(self.trackNode, 'cameraPlayerTracking')
        task.lookAtNode = self.av.headNode
        task.lookAtOffset = Point3(0)

    def exitUnconcious(self):
        PlayerPirateGameFSM.exitUnconcious(self)
        self.av.collisionsOn()
        base.transitions.letterboxOff()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        taskMgr.remove('cameraPlayerTracking')

    def enterSpawn(self, extraArgs=[]):
        PlayerPirateGameFSM.enterSpawn(self)
        self.av.show(invisibleBits=PiratesGlobals.INVIS_DEATH)
        self.av.setScale(1, 1, 1)
        self.spawnIval = Sequence(Func(base.transitions.fadeOut, 0), Func(self.av.guiMgr.request, 'Interface'), Func(self.av.cameraFSM.request, 'Control'), Func(base.transitions.fadeIn, 2), Func(self.av.b_setGameState, self.defaultState))
        self.spawnIval.start()

    def exitSpawn(self):
        PlayerPirateGameFSM.exitSpawn(self)
        self.spawnIval.pause()
        del self.spawnIval

    def enterHalt(self, extraArgs=[]):
        messenger.send('localAV-enterHalt')
        self.accept('localAvatarEnterWater', self.handleLocalAvatarEnterWater)
        self.av.speedIndex = PiratesGlobals.SPEED_NOMOVE_INDEX
        self.av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[self.av.speedIndex])
        self.av.updatePlayerSpeed()
        self.av.delayAFK()
        localAvatar.motionFSM.request('MoveLock')

    def exitHalt(self):
        messenger.send('localAV-exitHalt')
        self.ignore('localAvatarEnterWater')
        base.cr.interactionMgr.stop()
        self.ignore(WeaponGlobals.LocalAvatarUseItem)
        self.av.disableMouseWeaponDraw()

    def enterBattle(self, extraArgs=[]):
        if base.cr.activeWorld == None:
            return
        self.accept('localAvatarEnterWater', self.handleLocalAvatarEnterWater)
        self.av.speedIndex = PiratesGlobals.SPEED_BATTLE_INDEX
        self.av.guiMgr.request('Interface')
        self.av.guiMgr.combatTray.showWeapons()
        self.av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[self.av.speedIndex])
        self.av.startListenAutoRun()
        self.av.controlManager.use('walk', self.av)
        base.cr.targetMgr.startFollowAim()
        base.cr.interactionMgr.start()
        self.av.hideName()
        self.av.cameraFSM.request('FPS')
        self.av.cameraFSM.fpsCamera.avFaceCamera()
        self.av.show()
        self.accept(WeaponGlobals.LocalAvatarUseTargetedSkill, self.av.composeRequestTargetedSkill)
        self.accept(WeaponGlobals.LocalAvatarUseProjectileSkill, self.av.composeRequestProjectileSkill)
        self.accept(WeaponGlobals.LocalAvatarUseItem, self.av.composeRequestTargetedSkill)
        self.accept('requestGearExit', self.av.requestExitBattle)
        self.accept(InteractiveBase.END_INTERACT_EVENT, self.av.requestExitBattle)
        self.av.guiMgr.combatTray.showSkills()
        PlayerPirateGameFSM.enterBattle(self)
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)
        NametagGlobals.setMasterNametagsActive(0)
        self.accept('shift', NametagGlobals.setMasterNametagsActive, [1])
        self.accept('shift-up', NametagGlobals.setMasterNametagsActive, [0])
        self.av.updatePlayerSpeed()
        return

    def exitBattle(self):
        self.ignore('localAvatarEnterWater')
        self.av.guiMgr.combatTray.clearQueues()
        if base.cr.targetMgr:
            base.cr.targetMgr.stopFollowAim()
        self.av.stopListenAutoRun()
        base.cr.interactionMgr.stop()
        self.av.sendRequestRemoveEffects(self.av.stickyTargets)
        self.av.setStickyTargets([])
        self.av.showName()
        self.av.l_setCurrentWeapon(self.av.currentWeaponId, 0, self.av.currentWeaponSlotId)
        self.av.d_requestCurrentWeapon(self.av.currentWeaponId, 0)
        self.av.setAimMod(0)
        self.av.stopLookAtTarget()
        self.ignore(WeaponGlobals.LocalAvatarUseTargetedSkill)
        self.ignore(WeaponGlobals.LocalAvatarUseProjectileSkill)
        self.ignore(WeaponGlobals.LocalAvatarUseItem)
        self.ignore('requestGearExit')
        self.ignore(InteractiveBase.END_INTERACT_EVENT)
        self.av.guiMgr.setIgnoreEscapeHotKey(True)
        self.av.guiMgr.setIgnoreEscapeHotKey(False)
        self.av.guiMgr.combatTray.hideSkills()
        self.av.guiMgr.combatTray.disableTray()
        PlayerPirateGameFSM.exitBattle(self)
        self.ignore('wheel_up')
        self.ignore('wheel_down')
        self.ignore('shift')
        self.ignore('shift-up')
        NametagGlobals.setMasterNametagsActive(1)

    def enterLandTreasureRoam(self, extraArgs=[]):
        self.accept('localAvatarEnterWater', self.handleLocalAvatarEnterWater)
        self.av.speedIndex = PiratesGlobals.SPEED_CARRY_INDEX
        self.av.guiMgr.request('Interface')
        self.av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[self.av.speedIndex])
        self.av.controlManager.use('walk', self.av)
        base.cr.interactionMgr.start()
        messenger.send('carryingTreasure')
        PlayerPirateGameFSM.enterLandTreasureRoam(self)
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)
        self.av.updatePlayerSpeed()

    def exitLandTreasureRoam(self):
        self.ignore('localAvatarEnterWater')
        base.cr.interactionMgr.stop()
        messenger.send('notCarryingTreasure')
        PlayerPirateGameFSM.exitLandTreasureRoam(self)
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def enterWaterTreasureRoam(self, extraArgs=[]):
        self.accept('localAvatarExitWater', self.handleLocalAvatarExitWater)
        self.av.speedIndex = PiratesGlobals.SPEED_CARRY_INDEX
        self.av.guiMgr.request('Interface')
        self.av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[self.av.speedIndex])
        self.av.controlManager.use('walk', self.av)
        self.av.controlManager.get('walk').setGravity(0.0)
        self.av.controlManager.get('walk').setVelocity(0.0)
        self.av.physControls.disableJump()
        self.av.startBobSwimTask()
        base.cr.interactionMgr.start()
        self.av.cameraFSM.request('FPS')
        self.av.b_setTeleportFlag(PiratesGlobals.TFInWater, self.av.confirmSwimmingTeleport)
        PlayerPirateGameFSM.enterWaterTreasureRoam(self)
        self.av.updatePlayerSpeed()

    def exitWaterTreasureRoam(self):
        self.ignore('localAvatarExitWater')
        self.av.stopBobSwimTask()
        self.av.guiMgr.request('Interface')
        self.av.controlManager.get('walk').setGravity(32.174 * 2.0)
        self.av.physControls.enableJump()
        base.cr.interactionMgr.stop()
        self.av.b_clearTeleportFlag(PiratesGlobals.TFInWater)
        PlayerPirateGameFSM.exitWaterTreasureRoam(self)

    def enterTeleportOut(self, extraArgs=[]):
        self.notify.debug('enterTeleportOut() for avId: %d' % self.av.getDoId())
        self.av.motionFSM.request('MoveLock')
        self.av.controlManager.get('walk').setGravity(0.0)
        self.av.guiMgr.request('Cutscene')
        self.av.cameraFSM.request('FPS')
        base.cr.interactionMgr.stop(endCurrent=True)
        base.cr.interactionMgr.lock()
        self.av.nametag3d.hide()
        self.av.stopAutoRun()
        timeOffset = 0.0
        if len(extraArgs) >= 1:
            timeOffset = extraArgs[0]
        if len(extraArgs) >= 2:
            doneEvent = extraArgs[1]
        else:
            doneEvent = ''
        if len(extraArgs) >= 3:
            doEffect = extraArgs[2]
        else:
            doEffect = True
        if doEffect:
            if not self.teleportEffect:
                teleportAnimPlayRate = 1.5
                teleportAnimLength = self.av.getDuration('teleport') / teleportAnimPlayRate
                twisterFadeLength = 1.0
                totalLength = teleportAnimLength + twisterFadeLength
                avFadeOutLength = 2.0
                avFlyTime = 1.5
                avFlyHeight = 7
                screenFadeLength = 0.5

                def setRelZ(t):
                    self.av.getGeomNode().setZ(lerp(0, avFlyHeight, t))

                teleportTrack = Sequence()
                teleportPar = Parallel()
                self.teleportEffect = TeleportTwister.getEffect()
                self.teleportSfx = loadSfx(SoundGlobals.SFX_AVATAR_TELEPORT)
                if self.teleportEffect:
                    teleportTrack.append(Func(self.teleportEffect.reparentTo, self.av.getEffectParent()))

                def playTeleportAnim():
                    self.av.play('teleport', blendOutT=0.0)
                    self.av.setPlayRate(teleportAnimPlayRate, 'teleport')
                    if self.teleportEffect and self.teleportEffect.p0:
                        self.teleportEffect.play()

                def playTeleportSfx():
                    self.teleportSfx.play()

                teleportPar.append(Func(playTeleportAnim))
                teleportPar.append(Func(playTeleportSfx))
                teleportPar.append(Sequence(Wait(teleportAnimLength - avFadeOutLength), Func(self.av.setTransparency, 1, 1001), LerpFunc(self.av.setColorScale, duration=avFadeOutLength, toData=Vec4(1, 1, 1, 0), fromData=Vec4(1, 1, 1, 1))))
                teleportPar.append(Sequence(Wait(avFlyTime), LerpFunc(setRelZ, duration=teleportAnimLength - avFlyTime)))
                teleportPar.append(Sequence(Wait(totalLength - screenFadeLength), Func(base.transitions.fadeOut), Wait(0.5), Func(base.cr.loadingScreen.show, waitForLocation=True)))
                teleportTrack.append(teleportPar)
                teleportTrack.append(Func(self.av.controlManager.collisionsOff))
                self.teleportTrack = teleportTrack
            self.teleportTrack.setDoneEvent(doneEvent)
            self.teleportTrack.start(timeOffset)
        elif doneEvent:
            messenger.send(doneEvent)

    def exitTeleportOut(self):
        self.notify.debug('exitTeleportOut() for avId: %d' % self.av.getDoId())
        self.ignore(base.cr.getAllInterestsCompleteEvent())
        if self.teleportTrack:
            self.teleportTrack.finish()
        if self.teleportEffect:
            self.teleportEffect.cleanUpEffect()
            self.teleportEffect = None
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        self.av.getGeomNode().setZ(0)
        self.av.clearColorScale()
        self.av.clearTransparency()
        self.av.nametag3d.show()
        if base.cr.tutorial:
            if self.av.style.getTutorial():
                base.transitions.noFade()
        else:
            base.transitions.noFade()
        return

    def enterTeleportIn(self, extraArgs=[]):
        self.notify.debug('enterTeleportIn() for avId: %d' % self.av.getDoId())
        self.av.guiMgr.request('Cutscene')
        self.av.motionFSM.request('MoveLock')
        self.acceptOnce(base.transitions.FadeInEvent, self.av.b_setGameState, ['LandRoam'])
        base.transitions.fadeIn()
        self.av.stopAutoRun()

    def exitTeleportIn(self):
        self.ignore(base.transitions.FadeInEvent)
        self.notify.debug('exitTeleportIn() for avId: %d' % self.av.getDoId())
        base.cr.loadingScreen.hide()

    def enterShipPilot(self, extraArgs=[]):
        ship = extraArgs[1]
        s = MiniLogSentry(ship.miniLog, 'enterShipPilot')
        self.av.guiMgr.request('Interface')
        self.av.guiMgr.hideSeaChest()
        self.av.guiMgr.combatTray.initCombatTray(InventoryType.SailingRep)
        self.av.guiMgr.combatTray.showCharm()
        self.av.stopAutoRun()
        self.accept(WeaponGlobals.LocalAvatarUseTargetedSkill, self.av.composeRequestTargetedSkill)
        self.accept(WeaponGlobals.LocalAvatarUseProjectileSkill, self.av.composeRequestProjectileSkill)
        self.accept(WeaponGlobals.LocalAvatarUseItem, self.av.composeRequestTargetedSkill)
        self.accept(WeaponGlobals.LocalAvatarUseShipSkill, self.av.composeRequestShipSkill)
        self._usingRepairKit = False
        if localAvatar.getSiegeTeam():
            self.accept(self.av.cr.distributedDistrict.siegeManager.getUseRepairKitEvent(), self._handleUseRepairKit)
            self._handleUseRepairKit(self.av.cr.distributedDistrict.siegeManager.getUseRepairKit())
        if localAvatar.getParentObj() is not ship or __dev__:
            if ship.miniLog:
                ship.miniLog.appendLine("localAvatar's parent: (%s)" % (localAvatar.getParentObj(),))
            logBlock(3, ship.miniLog)
        ship.resetMiniLog()
        self.av.stopPosHprBroadcast()
        ship.placeAvatarAtWheel(self.av)
        self.av.sendCurrentPosition()
        PlayerPirateGameFSM.enterShipPilot(self, [ship])

    def _handleUseRepairKit(self, useRepairKit):
        if useRepairKit and not self._usingRepairKit:
            localAvatar.guiMgr.combatTray.enableShipRepair()
        elif not useRepairKit and self._usingRepairKit:
            localAvatar.guiMgr.combatTray.disableShipRepair()
        self._usingRepairKit = useRepairKit

    def exitShipPilot(self):
        self.av.startPosHprBroadcast()
        self._handleUseRepairKit(False)
        self.av.guiMgr.combatTray.disableTray()
        self.av.guiMgr.combatTray.showWeapons()
        self.ignore(WeaponGlobals.LocalAvatarUseShipSkill)
        self.ignore(WeaponGlobals.LocalAvatarUseItem)
        self.ignore(WeaponGlobals.LocalAvatarUseTargetedSkill)
        self.ignore(WeaponGlobals.LocalAvatarUseProjectileSkill)
        PlayerPirateGameFSM.exitShipPilot(self)

    def enterDigging(self, extraArgs=[]):
        PlayerPirateGameFSM.enterDigging(self)
        base.musicMgr.request(SoundGlobals.MUSIC_SEARCHING, looping=0, priority=2)
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('FPS')
        base.transitions.letterboxOn()
        self.av.stopAutoRun()
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)

    def exitDigging(self):
        PlayerPirateGameFSM.exitDigging(self)
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_SEARCHING)
        base.transitions.letterboxOff()
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def enterSearching(self, extraArgs=[]):
        PlayerPirateGameFSM.enterSearching(self)
        base.musicMgr.request(SoundGlobals.MUSIC_SEARCHING, looping=0, priority=2)
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('FPS')
        base.transitions.letterboxOn()
        self.av.stopAutoRun()
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)

    def exitSearching(self):
        PlayerPirateGameFSM.exitSearching(self)
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_SEARCHING)
        base.transitions.letterboxOff()
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def enterHealing(self, extraArgs=[]):
        self.av.stopAutoRun()
        PlayerPirateGameFSM.enterHealing(self, extraArgs)
        if not self.av.isInInvasion():
            base.musicMgr.request(SoundGlobals.MUSIC_SEARCHING, looping=0, priority=2)
        self.av.guiMgr.request('Interaction')
        self.av.cameraFSM.request('FPS')
        base.transitions.letterboxOn()
        taskMgr.doMethodLater(PiratesGlobals.TIME_TO_REVIVE + 5.0, self.cancelHealing, self.av.uniqueName('healingTimeout'))
        self.av.stopAutoRun()
        healingAv = base.cr.interactionMgr.getCurrent()
        if healingAv:
            self.disableEvent = healingAv.uniqueName('disable')
            self.acceptOnce(self.disableEvent, self.cancelHealing)
            healingAv.hideHpMeter()

    def cancelHealing(self, task=None):
        from pirates.interact import InteractiveBase
        self.ignore(self.disableEvent)
        self.av.stopHealing()
        if task:
            return task.done

    def exitHealing(self):
        taskMgr.remove(self.av.uniqueName('healingTimeout'))
        PlayerPirateGameFSM.exitHealing(self)
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_SEARCHING)
        base.transitions.letterboxOff()
        base.cr.interactionMgr.requestExitCurrent()
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def enterStealing(self, extraArgs=[]):
        PlayerPirateGameFSM.enterStealing(self)
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('FPS')
        base.transitions.letterboxOn()
        self.av.stopAutoRun()
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)

    def exitStealing(self):
        PlayerPirateGameFSM.exitStealing(self)
        base.transitions.letterboxOff()
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def enterOOBEmote(self, extraArgs=[]):
        PlayerPirateGameFSM.enterEmote(self)
        base.transitions.letterboxOn()
        self.av.guiMgr.request('Interface', [True, False])
        self.av.guiMgr.toggleGuiForNpcInteraction(0)
        self.av.stopAutoRun()
        self.av.motionFSM.request('Off')
        timeElapsed, emoteId, panelType = extraArgs
        dummy = localAvatar.attachNewNode('dummy')
        dummy.setPos(localAvatar.headNode.getX(localAvatar) - 8, localAvatar.headNode.getY(localAvatar) + 10, localAvatar.headNode.getZ(localAvatar) + 2)
        dummy.wrtReparentTo(render)
        dummy.lookAt(localAvatar, localAvatar.headNode.getX(localAvatar), localAvatar.headNode.getY(localAvatar), localAvatar.headNode.getZ(localAvatar) * 0.8)
        camPos = dummy.getPos()
        camHpr = dummy.getHpr()
        dummy.detachNode()
        camera.wrtReparentTo(render)
        camH = camera.getH() % 360
        h = camHpr[0] % 360
        if camH > h:
            h += 360
        if h - camH > 180:
            h -= 360
        camHpr.setX(h)
        camera.setH(camH)
        emoteName = EmoteGlobals.getEmoteAnim(emoteId)
        duration = self.av.getDuration(emoteName)
        self.camIval = Sequence(camera.posHprInterval(1.0, pos=camPos, hpr=camHpr, blendType='easeOut'), Func(self.av.playEmote, emoteId))
        if panelType:

            def createRewardPanel(type):
                self.rewardPanel = RewardPanel(aspect2d, type=type, doneCallback=self.handleExitOOBEmote)

            dummy = localAvatar.attachNewNode('dummy')
            dummy.setPos(localAvatar.headNode.getX(localAvatar) - 4, localAvatar.headNode.getY(localAvatar) + 11, localAvatar.headNode.getZ(localAvatar) + 2)
            dummy.wrtReparentTo(render)
            camPos = dummy.getPos()
            dummy.detachNode()
            dummy = localAvatar.attachNewNode('dummy')
            dummy.setPos(localAvatar.headNode.getX(localAvatar), localAvatar.headNode.getY(localAvatar) + 11, localAvatar.headNode.getZ(localAvatar) + 2)
            dummy.wrtReparentTo(render)
            dummy.lookAt(localAvatar, localAvatar.headNode.getX(localAvatar), localAvatar.headNode.getY(localAvatar), localAvatar.headNode.getZ(localAvatar) * 0.8)
            camHpr = dummy.getHpr()
            dummy.detachNode()
            self.camIval.append(Wait(duration * 0.9))
            self.camIval.append(Parallel(camera.posHprInterval(0.5, pos=camPos, hpr=camHpr, blendType='easeOut'), Func(createRewardPanel, panelType)))
        else:
            self.camIval.append(Wait(duration))
            self.camIval.append(Func(self.handleExitOOBEmote))
        base.musicMgr.request(SoundGlobals.MUSIC_REWARD_WEAPON, priority=4, looping=0, volume=0.6)
        self.av.cameraFSM.request('Control')
        self.camIval.start()

    def exitOOBEmote(self):
        PlayerPirateGameFSM.exitEmote(self)
        self.av.guiMgr.subtitler.clearText()
        self.av.guiMgr.toggleGuiForNpcInteraction(1)
        self.av.motionFSM.request('On')
        base.transitions.letterboxOff()
        if self.camIval:
            self.camIval.pause()
            self.camIval = None
        if self.rewardPanel:
            self.rewardPanel.cleanup()
            self.rewardPanel = None
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_REWARD_WEAPON)
        return

    def handleExitOOBEmote(self):
        if self.getCurrentOrNextState() == 'LandRoam':
            if self.rewardPanel:
                self.rewardPanel.cleanup()
                self.rewardPanel = None
        if self.av:
            self.av.b_setGameState('LandRoam')
        return

    def enterNPCInteract(self, extraArgs=[]):
        if len(extraArgs) != 4:
            self.notify.error('Unexpected number of extraArgs!')
            return
        timeElapsed, npc, hasMenu, dialogMode = extraArgs
        self.interactNPC = npc
        self.notify.debug('enterNPCInteract %s' % npc.doId)
        PlayerPirateGameFSM.enterNPCInteract(self)
        npc.abortNotice()
        if dialogMode:
            npc.ignore(InteractiveBase.END_INTERACT_EVENT)
            taskMgr.doMethodLater(0.25, self.startDialogNPCInteract, 'startDialogNPCInteract', extraArgs=[npc])
        else:
            self.startNPCInteract(npc, hasMenu)

    def startDialogNPCInteract(self, npc, task=None):
        base.transitions.letterboxOn()
        messenger.send('localAvatarEntersDialog')
        self.av.duringDialog = True
        self.av.guiMgr.request('Interface', [True, False])
        self.av.guiMgr.toggleGuiForNpcInteraction(0)
        self.av.stopAutoRun()
        self.av.cameraFSM.request('Control')
        npc.playInteraction(hasMenu=True)
        self.savedPos = localAvatar.getPos(localAvatar.getParentObj())
        self.savedHpr = localAvatar.getHpr(localAvatar.getParentObj())
        self.av.stopPosHprBroadcast()
        self.av.setPos(npc, 6, 4, 0)
        self.savedNPCHpr = npc.getHpr()
        npc.motionFSM.off(lock=True)
        pos1 = self.av.getPos(render)
        pos2 = npc.getPos(render)
        dummy = render.attachNewNode('cameraDummy')
        dummy.setPos((pos1 + pos2) / 2.0)
        dummy.lookAt(npc)
        dummy.setZ(dummy.getZ() + 4.0)
        dummy.setH(dummy.getH() + 90)
        distance = math.sqrt(math.pow(pos1[0] - pos2[0], 2) + math.pow(pos1[1] - pos2[1], 2) + math.pow(pos1[2] - pos2[2], 2))
        dummy2 = dummy.attachNewNode('cameraDummy')
        dummy2.setPos(-4.5, -distance * 1.0, 0.5)
        camera.wrtReparentTo(render)
        camera.setPos(dummy2.getPos(render))
        camera.lookAt(dummy)
        self.av.lookAt(npc)
        npc.lookAt(self.av)
        dummy2.detachNode()
        dummy.detachNode()

    def startNPCInteract(self, npc, hasMenu=True):
        base.transitions.letterboxOn()
        self.av.guiMgr.request('Interface', [True, False])
        self.av.guiMgr.toggleGuiForNpcInteraction(0)
        self.av.stopAutoRun()
        npc.playInteraction(hasMenu=hasMenu)
        if npc.interactCamPosHpr:
            camPos = npc.interactCamPosHpr[0]
            camHpr = npc.interactCamPosHpr[1]
        else:
            npc.waitPending()
            dummy = npc.attachNewNode('dummy')
            dummy.setPos(npc.headNode.getX(npc), npc.headNode.getY(npc) + 4.5, npc.headNode.getZ(npc) + 1)
            dummy.wrtReparentTo(render)
            dummy.lookAt(npc, npc.headNode.getX(npc), npc.headNode.getY(npc), npc.headNode.getZ(npc) * 0.95)
            if hasMenu:
                dummy.setH(dummy, 15)
            camPos = dummy.getPos()
            camHpr = dummy.getHpr()
            dummy.detachNode()
        camera.wrtReparentTo(render)
        camH = camera.getH() % 360
        h = camHpr[0] % 360
        if camH > h:
            h += 360
        if h - camH > 180:
            h -= 360
        camHpr.setX(h)
        camera.setH(camH)
        if self.camIval:
            self.camIval.pause()
        t = 1.5
        self.camIval = Parallel(camera.posHprInterval(t, pos=camPos, hpr=camHpr, blendType='easeOut'), Sequence(Func(self.av.setTransparency, 1), self.av.colorScaleInterval(t / 2, VBase4(1, 1, 1, 0)), Func(self.av.hide)))
        self.av.cameraFSM.request('Control')
        self.camIval.start()

    def exitNPCInteract(self):
        self.av.duringDialog = False
        messenger.send('localAvatarExitsDialog')
        taskMgr.remove('startDialogNPCInteract')
        PlayerPirateGameFSM.exitNPCInteract(self)
        self.endNPCInteract()

    def endNPCInteract(self):
        messenger.send('endDialogNPCInteract')
        if self.savedPos:
            self.av.setPos(localAvatar.getParentObj(), self.savedPos)
            self.av.setHpr(localAvatar.getParentObj(), self.savedHpr)
            self.av.startPosHprBroadcast()
            self.savedPos = None
            self.savedHpr = None
        if self.interactNPC and self.savedNPCHpr:
            self.interactNPC.setHpr(self.savedNPCHpr)
            self.savedNPCHpr = None
            self.interactNPC.motionFSM.unlock()
        self.av.guiMgr.subtitler.clearText()
        base.transitions.letterboxOff()
        self.av.guiMgr.toggleGuiForNpcInteraction(1)
        if self.camIval:
            self.camIval.pause()
            self.camIval = None
        self.av.setColorScale(1, 1, 1, 1)
        self.av.setTransparency(0)
        self.av.show()
        return

    def enterDinghyInteract(self, extraArgs=[]):
        if len(extraArgs) != 2:
            self.notify.warning('Unexpected number of extraArgs!')
            return
        timestamp, dinghy = extraArgs
        self.notify.debug('enterDinghyInteract')
        PlayerPirateGameFSM.enterDinghyInteract(self)
        base.transitions.letterboxOn()
        self.av.guiMgr.request('Interface')
        self.av.guiMgr.toggleGuiForNpcInteraction(0)
        self.av.stopAutoRun()
        self.av.cameraFSM.request('Control')

    def exitDinghyInteract(self):
        PlayerPirateGameFSM.exitDinghyInteract(self)
        base.transitions.letterboxOff()
        self.av.guiMgr.toggleGuiForNpcInteraction(1)
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.start()

    def enterDoorInteract(self, extraArgs=[]):
        self.av.guiMgr.request('Cutscene')
        self.av.motionFSM.off()
        self.av.collisionsOn()
        base.transitions.letterboxOn()
        self.av.stopAutoRun()

    def exitDoorInteract(self):
        self.av.motionFSM.on()
        if self.doorWalkTrack:
            self.doorWalkTrack.pause()
            self.doorWalkTrack = None
        base.transitions.letterboxOff()
        return

    def enterCutscene(self, extraArgs=[]):
        self.av.guiMgr.request('Cutscene')
        self.av.cameraFSM.request('Control')
        self.av.guiMgr._hideCursor()
        self.av.motionFSM.off()
        base.transitions.letterboxOff()
        if base.camLens.getAspectRatio() < 1.6:
            base.transitions.letterboxOn()
        self.av.stopAutoRun()
        self.av.questIndicator.hideEffect()

    def exitCutscene(self):
        self.av.motionFSM.on()
        base.transitions.letterboxOff()
        if not self.av.guiMgr.ignoreAllKeys:
            self.av.guiMgr.showTrays()
        self.av.guiMgr._showCursor()
        self.av.questIndicator.showEffect()

    def enterDialog(self, extraArgs=[]):
        self.av.stopAutoRun()
        if self.av.currentDialogMovie is None or not self.av.currentDialogMovie.enableCameraLock:
            self.av.cameraFSM.request('Control')
        self.av.motionFSM.off()
        return

    def exitDialog(self):
        pass

    @report(types=['args'], dConfigParam='dteleport')
    def enterShipBoarding(self, extraArgs=[]):
        PlayerPirateGameFSM.enterShipBoarding(self, extraArgs)
        self.av.cameraFSM.request('Control')
        self.av.guiMgr.request('Cutscene')
        self.av.stopAutoRun()
        self.av.motionFSM.off()
        self.av.controlManager.collisionsOff()
        self.av.sendCurrentPosition()
        self.av.stopPosHprBroadcast()
        base.transitions.letterboxOn()

    @report(types=['args'], dConfigParam='dteleport')
    def exitShipBoarding(self):
        PlayerPirateGameFSM.exitShipBoarding(self)
        self.av.controlManager.collisionsOn()
        self.av.motionFSM.on()
        base.transitions.letterboxOff()

    def enterCannon(self, extraArgs=[]):
        self.notify.debug('enterCannon for avId: %d' % self.av.getDoId())
        PlayerPirateGameFSM.enterCannon(self)
        base.cr.interactionMgr.stop()
        self.av.guiMgr.request('Interface')
        self.av.guiMgr.combatTray.hideSkills()
        self.av.guiMgr.combatTray.showCharm()
        NametagGlobals.setMasterNametagsActive(0)
        self.av.stopAutoRun()

    def exitCannon(self):
        self.notify.debug('exitCannon for avId: %d' % self.av.getDoId())
        PlayerPirateGameFSM.exitCannon(self)
        base.cr.interactionMgr.start()
        self.av.guiMgr.combatTray.showWeapons()
        NametagGlobals.setMasterNametagsActive(1)

    def enterEnsnared(self, extraArgs=[]):
        PlayerPirateGameFSM.enterEnsnared(self)
        self.av.guiMgr.request('Cutscene')
        self.av.collisionsOff()
        self.av.cameraFSM.request('Control')
        base.transitions.letterboxOn()
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.lock()
        self.av.stopAutoRun()
        camera.setPos(self.av, 0.5, -14, 6)
        camera.wrtReparentTo(self.av.getParent())
        camera.lookAt(self.av.headNode)
        task = taskMgr.add(self.trackNode, 'cameraPlayerTracking')
        task.lookAtNode = self.av.headNode
        task.lookAtOffset = Point3(0)

    def filterEnsnared(self, request, args=[]):
        if request == 'Ensnared':
            return
        return self.defaultFilter(request, args)

    def exitEnsnared(self):
        PlayerPirateGameFSM.exitEnsnared(self)
        self.av.collisionsOn()
        base.transitions.letterboxOff()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        taskMgr.remove('cameraPlayerTracking')

    def enterThrown(self, extraArgs=[]):
        PlayerPirateGameFSM.enterThrown(self)
        self.av.stopAutoRun()

    def exitThrown(self):
        PlayerPirateGameFSM.exitThrown(self)

    def enterKnockdown(self, extraArgs=[]):
        PlayerPirateGameFSM.enterKnockdown(self)
        self.av.guiMgr.request('Interface')
        if self.av.controlManager.currentControls:
            self.av.collisionsOff()
        self.av.cameraFSM.request('Control')
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.lock()
        task = taskMgr.add(self.trackNode, 'cameraPlayerTracking')
        task.lookAtNode = self.av.headNode
        task.lookAtOffset = Point3(0)

    def exitKnockdown(self):
        PlayerPirateGameFSM.exitKnockdown(self)
        if self.av.controlManager.currentControls:
            self.av.collisionsOn()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        taskMgr.remove('cameraPlayerTracking')

    def enterInjured(self, extraArgs=[]):
        messenger.send('show_injured_gui', [])
        self.acceptOnce('asked_for_jail', self.sendJailRequest)
        PlayerPirateGameFSM.enterInjured(self, extraArgs)
        localAvatar.b_setTeleportFlag(PiratesGlobals.TFInjured)

    def exitInjured(self):
        localAvatar.b_clearTeleportFlag(PiratesGlobals.TFInjured)
        self.ignore('asked_for_jail')
        messenger.send('local_pirate_exiting_injured_state')
        PlayerPirateGameFSM.exitInjured(self)

    def enterDying(self, extraArgs=[]):
        timeStamp = extraArgs[0]
        self.av.loop('injured_idle')
        self.injuredTrack = self.av.getDyingTrack(timeStamp)
        if self.injuredTrack:
            if self.av.motionFSM:
                self.av.motionFSM.off()
            timeStamp = extraArgs[0]
            self.av.stopSmooth()
            self.injuredTrack.start()
        localAvatar.b_setTeleportFlag(PiratesGlobals.TFInjured)

    def exitDying(self):
        self.av.b_clearTeleportFlag(PiratesGlobals.TFInjured)
        self.av.show(invisibleBits=PiratesGlobals.INVIS_DEATH)
        PlayerPirateGameFSM.exitDying(self)
        base.cr.activeWorld.localAvEnterDeath(self.av)

    def sendJailRequest(self):
        self.av.sendUpdate('requestGotoJailWhileInjured', [])

    @report(types=['frameCount', 'args'], dConfigParam='jail')
    def enterDeath(self, extraArgs=[]):
        timeOffset = 0.0
        if len(extraArgs) >= 1:
            timeOffset = extraArgs[0]
        if self.av.motionFSM:
            self.av.motionFSM.off()
        self.av.deleteBattleCollisions()
        if self.av.guiMgr.targetStatusTray.doId == self.av.doId:
            self.av.guiMgr.targetStatusTray.fadeOut()
        self.av.cameraFSM.request('Control')
        base.transitions.letterboxOn()
        curInteractive = base.cr.interactionMgr.getCurrentInteractive()
        if curInteractive:
            curInteractive.requestExit()
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.lock()
        self.av.stopAutoRun()
        if self.av.ship and self.av.ship.gameFSM and self.av.ship.gameFSM.getCurrentOrNextState() == 'Sunk':
            base.cr.activeWorld.localAvEnterDeath(self.av)
            return
        camera.setPos(self.av, 0.5, -14, 6)
        camera.wrtReparentTo(self.av.getParent())
        camera.lookAt(self.av.headNode)
        task = taskMgr.add(self.trackNode, 'cameraPlayerTracking')
        task.lookAtNode = self.av.headNode
        task.lookAtOffset = Point3(0)
        self.av.stopCombatMusic()
        self.av.guiMgr.request('Cutscene')
        base.musicMgr.request(SoundGlobals.MUSIC_DEATH, priority=3, looping=0)
        if self.deathTrack:
            self.deathTrack.finish()
            self.deathTrack = None
        self.deathTrack = Sequence(self.av.getDeathTrack(), Wait(2))
        if self.av.getSiegeTeam():
            self.deathTrack.append(Func(self.av.b_setGameState, 'LandRoam'))
        else:
            self.deathTrack.append(Func(base.transitions.fadeOut, 1))
            self.deathTrack.append(Func(base.cr.activeWorld.localAvEnterDeath, self.av))
        self.deathTrack.start(timeOffset)
        self.av.refreshStatusTray()
        return

    @report(types=['frameCount'], dConfigParam='jail')
    def exitDeath(self):
        if self.deathTrack:
            self.deathTrack.finish()
            self.deathTrack = None
        self.av.collisionsOn()
        base.transitions.letterboxOff()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        base.transitions.fadeIn(0)
        taskMgr.remove('cameraPlayerTracking')
        if base.cr.activeWorld:
            self.deathTrack = Sequence(Func(base.cr.activeWorld.localAvExitDeath, self.av))
            self.deathTrack.start()
        self.av.show(invisibleBits=PiratesGlobals.INVIS_DEATH)
        base.musicMgr.requestFadeOut(SoundGlobals.MUSIC_DEATH)
        self.av.refreshStatusTray()
        return

    @report(types=['frameCount'], dConfigParam='jail')
    def enterThrownInJail(self, extraArgs=[]):
        self.av.stopAutoRun()
        if self.jailTrack:
            self.jailTrack.finish()
        self.av.guiMgr.request('Cutscene')
        self.av.cameraFSM.request('FPS')
        self.av.motionFSM.off()
        self.av.collisionsOn()
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.lock()
        base.transitions.letterboxOn()
        base.cr.loadingScreen.show()
        self.av.hide()

        @report(types=['frameCount'], dConfigParam='jail')
        def receivedSpawnPt():
            spawnInfo = self.av.cr.activeWorld.spawnInfo
            parent = self.av.getParentObj()
            if not isinstance(parent, NodePath):
                logBlock(4, 'Player(%s) in jail, but parentObj is %s' % (self.av.doId, parent))
                return
            self.av.setPosHpr(self.av.getParentObj(), *spawnInfo[0])
            self.av.spawnWiggle()

            def reqDefState():
                if not self.isInTransition():
                    self.av.b_setGameState(self.defaultState)

            self.av.stop()
            self.av.loop('idle')
            self.jailTrack = Sequence(Func(self.av.hide), Wait(3), Func(base.transitions.fadeIn, 1.25), Wait(0.25), Func(base.cr.loadingScreen.hide), Wait(1.75), Func(self.av.show, None, PiratesGlobals.INVIS_DEATH), self.av.actorInterval('jail_dropinto', blendOutT=0), self.av.actorInterval('jail_standup', blendInT=0), Func(reqDefState))
            self.jailTrack.start()
            return

        self.spawnPtEvent = self.av.cr.activeWorld.uniqueName('spawnInfoReceived')
        self.acceptOnce(self.spawnPtEvent, receivedSpawnPt)
        self.acceptOnce('localAvatar-setLocation', self.av.getParentObj().handleAvatarSetLocation)

    @report(types=['frameCount'], dConfigParam='jail')
    def exitThrownInJail(self):
        self.ignore(self.spawnPtEvent)
        self.ignore('localAvatar-setLocation')
        if self.jailTrack:
            self.jailTrack.finish()
        self.av.show(invisibleBits=PiratesGlobals.INVIS_DEATH)
        self.av.motionFSM.on()
        base.cr.interactionMgr.unlock()
        base.cr.interactionMgr.start()
        base.transitions.letterboxOff()
        self.av.displayMoraleMessage()

    def enterDoorKicking(self, extraArgs=[]):
        self.av.guiMgr.request('Cutscene')
        self.av.cameraFSM.request('FPS')
        self.av.motionFSM.off()
        base.transitions.letterboxOn()
        kickT = self.av.getDuration('kick_door_loop')
        self.kickSfx = loadSfx(SoundGlobals.SFX_AVATAR_KICK_DOOR)
        self.kickTrack = Sequence(Func(messenger.send, self.av.kickEvents[0]), Func(base.playSfx, self.kickSfx, node=self.av), Wait(kickT), Func(messenger.send, self.av.kickEvents[1]))
        self.kickTrack.loop()
        self.av.loop('kick_door_loop')
        self.av.stopAutoRun()
        self.accept('wheel_up', self.av.guiMgr.combatTray.togglePrevWeapon)
        self.accept('wheel_down', self.av.guiMgr.combatTray.toggleNextWeapon)

    def exitDoorKicking(self):
        self.kickTrack.pause()
        self.kickTrack = None
        loader.unloadSfx(self.kickSfx)
        del self.kickSfx
        self.av.motionFSM.on()
        base.transitions.letterboxOff()
        self.ignore('wheel_up')
        self.ignore('wheel_down')
        return

    def handleLocalAvatarEnterWater(self):
        world = base.cr.getActiveWorld()
        if world:
            world.handleLocalAvatarEnterWater()

    def handleLocalAvatarExitWater(self):
        world = base.cr.getActiveWorld()
        if world:
            world.handleLocalAvatarExitWater()

    def enterEmote(self, extraArgs=[]):
        self.accept('localAvatarExitEmote', self.handleLocalAvatarExitEmote)
        PlayerPirateGameFSM.enterEmote(self)

    def exitEmote(self, extraArgs=[]):
        self.ignore('localAvatarExitEmote')
        PlayerPirateGameFSM.exitEmote(self)

    def handleLocalAvatarExitEmote(self):
        if self.av:
            self.av.b_setGameState('LandRoam')

    def enterParlorGame(self, extraArgs=[]):
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('Control')
        self.av.hideName()
        self.av.b_setTeleportFlag(PiratesGlobals.TFParlorGame)
        PlayerPirateGameFSM.enterParlorGame(self)
        self.av.stopAutoRun()

    def exitParlorGame(self):
        self.av.showName()
        self.av.b_clearTeleportFlag(PiratesGlobals.TFParlorGame)
        PlayerPirateGameFSM.exitParlorGame(self)

    def enterFishing(self, extraArgs=[]):
        self.av.stopTransformAnims()
        self.av.lockRegen()
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('Control')
        self.av.b_setTeleportFlag(PiratesGlobals.TFFishing)
        self.av.motionFSM.off(lock=True)
        self.av.stopAutoRun()
        base.cr.interactionMgr.stop()
        self.av.guiMgr.radarGui.hide()
        self.av.guiMgr.hideTrackedQuestInfo()
        inv = self.av.getInventory()
        rodLvl = inv.getStackQuantity(InventoryType.FishingRod)
        if rodLvl == 3:
            bestRod = ItemGlobals.FISHING_ROD_3
        else:
            if rodLvl == 2:
                bestRod = ItemGlobals.FISHING_ROD_2
            elif rodLvl == 1:
                bestRod = ItemGlobals.FISHING_ROD_1
            localAvatar.d_requestCurrentWeapon(bestRod, 1)
            localAvatar.l_setCurrentWeapon(bestRod, 1, -1)
            localAvatar.guiMgr.combatTray.toggleWeapon(bestRod, -1)
            if localAvatar.guiMgr.combatTray.slotDisplay:
                localAvatar.guiMgr.combatTray.slotDisplay.hide()
        PlayerPirateGameFSM.enterFishing(self)
        localAvatar.guiMgr.setIgnoreAllButSkillHotKey(True)
        self.turnNameTagsOff()

    def filterFishing(self, request, args=[]):
        if request in ('Emote', ):
            return None
        else:
            return self.defaultFilter(request, args)
        return None

    def exitFishing(self):
        self.av.b_clearTeleportFlag(PiratesGlobals.TFFishing)
        self.av.motionFSM.on(unlock=True)
        self.av.unlockAndRegen(force=False)
        base.cr.interactionMgr.start()
        self.av.guiMgr.combatTray.show()
        if base.localAvatar.getTutorialState() >= PiratesGlobals.TUT_GOT_COMPASS:
            self.av.guiMgr.radarGui.show()
        self.av.guiMgr.showTrackedQuestInfo()
        self.av.d_requestCurrentWeapon(0, 0)
        self.av.l_setCurrentWeapon(0, 0, 0)
        if localAvatar.guiMgr.combatTray.slotDisplay:
            localAvatar.guiMgr.combatTray.slotDisplay.show()
        PlayerPirateGameFSM.exitFishing(self)
        localAvatar.guiMgr.setIgnoreAllButSkillHotKey(False)
        self.turnNameTagsOn()

    def enterMakeAPirate(self, extraArgs=[]):
        self.av.guiMgr.request('Interface')
        self.av.cameraFSM.request('Off')
        self.av.motionFSM.off()
        self.av.stopAutoRun()

    def exitMakeAPirate(self):
        pass

    @report(types=['args', 'frameCount'], dConfigParam='dteleport')
    def enterEnterTunnel(self, extraArgs=[]):
        self.av.b_setTeleportFlag(PiratesGlobals.TFInTunnel)
        self.startLocalSequence()
        timestamp, entryLocator = extraArgs
        camera.wrtReparentTo(render)
        self.av.lookAt(entryLocator, -50, 0, localAvatar.getZ(entryLocator))
        camera.wrtReparentTo(localAvatar)
        distance = 40
        speed = PiratesGlobals.PirateSpeeds[self.av.speedIndex][0]
        duration = distance / speed
        self.av.startPosHprBroadcast()
        moveSequence = Sequence(Parallel(self.moveForwardInterval(distance), Sequence(Wait(duration - 0.8), Func(base.transitions.fadeOut, 0.75), Wait(0.75))), Func(base.cr.loadingScreen.show, waitForLocation=True), Func(messenger.send, 'EnterTunnelFinished'))
        cameraY = camera.getY()
        if cameraY < 13:
            cameraY = 13
        self.enterTunnelSequence = Parallel(self.lookMoveCameraSequence(duration / 2.0, Point3(0, -abs(cameraY), self.av.getHeight()), lookAtNode=self.av, lookAtOffset=Point3(0, 0, self.av.getHeight()), blendType='easeIn'), moveSequence)
        self.enterTunnelSequence.start()

    def exitEnterTunnel(self):
        if self.enterTunnelSequence:
            self.enterTunnelSequence.finish()
            self.enterTunnelSequence = None
        self.av.stopPosHprBroadcast()
        return

    def moveForwardInterval(self, distance, *args, **kw):
        dummy = NodePath('dummy')
        dummy.reparentTo(render)
        dummy.setPos(self.av, 0, 0, 0)
        dummy.setHpr(self.av, 0, 0, 0)
        speed = PiratesGlobals.PirateSpeeds[self.av.speedIndex][0]
        duration = distance / speed

        def gravityMoveForward(t, parent):
            self.av.setY(parent, t)

        return Sequence(Func(self.av.loop, 'run'), LerpFunc(gravityMoveForward, fromData=0, toData=distance, extraArgs=[dummy], duration=duration), Func(dummy.removeNode))

    @report(types=['args', 'frameCount'], dConfigParam='dteleport')
    def enterLeaveTunnel(self, extraArgs=[]):
        if len(extraArgs) < 4:
            return
        timestamp, tunnel, area, cutscene = extraArgs
        self.startLocalSequence()

        def continueLeaveTunnel():
            tunnel.reparentConnectorToArea(area)
            tunnelVisNode = area.builder.largeObjects.get(tunnel.uniqueId)
            if tunnelVisNode:
                tunnelVisNode.unstash()
                area.builder.setVisZoneLock(True)
                self.av.motionFSM.stopCheckUnderWater()
            else:
                self.notify.warning('enterLeaveTunnel: could not find tunnel in new area')
            self.av.reparentTo(tunnel.getEntranceNode(area))
            self.av.setPosHpr(0, 0, 0, -90, 0, 0)
            self.av.setY(self.av, -5)
            self.av.wrtReparentTo(area)
            localAvatar.setScale(1)
            area.parentObjectToArea(self.av)
            if cutscene:
                self.av.enableGridInterest()
                area.manageChild(self.av)
                area.builder.setVisZoneLock(False)
                return
            self.av.motionFSM.request('MoveLock')
            self.av.cameraFSM.fpsCamera.setHpr(0, 0, 0)
            self.av.cameraFSM.request('FPS')
            cameraFinalPos = camera.getPos(self.av)
            cameraFinalHpr = camera.getHpr(self.av)
            self.av.cameraFSM.request('Control')
            camera.reparentTo(self.av)
            camera.setPos(0, -13, self.av.getHeight() / 2)
            camera.lookAt(self.av.headNode)
            distance = 30
            speed = PiratesGlobals.PirateSpeeds[self.av.speedIndex][0]
            duration = distance / speed
            leaveSequence = Sequence(Func(self.av.startPosHprBroadcast), Func(base.cr.loadingScreen.hide), Parallel(self.moveForwardInterval(distance, blendType='easeOut', area=area), Func(base.transitions.fadeIn, 0.75), Sequence(Wait(duration / 2.0), self.rotateMoveCameraSequence(duration / 2.0, cameraFinalPos, hpr=cameraFinalHpr))), Func(self.av.enableGridInterest), Func(messenger.send, 'LeaveTunnelFinished'), Func(self.av.b_clearTeleportFlag, PiratesGlobals.TFInTunnel), Func(self.av.b_setGameState, 'LandRoam'), Func(area.builder.setVisZoneLock, False), Func(self.av.motionFSM.startCheckUnderWater))
            leaveSequence.start()
            area.manageChild(self.av)

        if hasattr(area, 'setZoneLevel') and area.lastZoneLevel != 0:
            area.setZoneLevel(0)
            area.setConnectorsHereCallback(continueLeaveTunnel)
        else:
            continueLeaveTunnel()

    def exitLeaveTunnel(self):
        self.av.stopPosHprBroadcast()
        self.av.cameraFSM.fpsCamera.setHpr(0, 0, 0)
        self.av.motionFSM.on()
        self.endLocalSequence()

    def enterPVPWait(self, extraArgs=[]):
        self.av.motionFSM.request('MoveLock')

    def exitPVPWait(self):
        self.av.motionFSM.on()

    def enterPVPComplete(self, extraArgs=[]):
        self.av.motionFSM.request('MoveLock')

    def filterPVPComplete(self, request, args=[]):
        return self.defaultFilter(request, args)

    def exitPVPComplete(self):
        self.av.motionFSM.on()

    def enterPotionCrafting(self, extraArgs=[]):
        PlayerPirateGameFSM.enterPotionCrafting(self, extraArgs)
        self.av.guiMgr.radarGui.hide()
        self.av.guiMgr.hideTrackedQuestInfo()
        self.av.guiMgr.gameGui.hide()
        self.av.guiMgr.crewHUD.setHUDOff()
        self.av.guiMgr.combatTray.hide()
        messenger.send('enteringMinigame', [])
        self.av.stopAutoRun()
        self.turnNameTagsOff()
        self.av.b_setTeleportFlag(PiratesGlobals.TFPotionCrafting)
        base.transitions.setFadeColor(0, 0, 0)
        if not base.transitions.fadeOutActive():
            base.transitions.fadeOut(0.1, Func(self.turnCamNodesOff))

    def turnCamNodesOff(self):
        if base.cam:
            base.cam.node().setActive(False)
        if base.enviroCam:
            base.enviroCam.node().setActive(False)
        base.loadingScreen.showTarget(potionCrafting=True)
        base.loadingScreen.show()

    def filterPotionCrafting(self, request, args=[]):
        if request in ('Emote', ):
            return None
        else:
            return self.defaultFilter(request, args)
        return None

    def exitPotionCrafting(self):
        if base.cam:
            base.cam.node().setActive(True)
        if base.enviroCam:
            base.enviroCam.node().setActive(True)
        self.av.guiMgr.radarGui.show()
        self.av.guiMgr.showTrackedQuestInfo()
        self.av.guiMgr.gameGui.show()
        self.av.guiMgr.crewHUD.setHUDOn()
        self.av.guiMgr.combatTray.show()
        messenger.send('exitingMinigame', [])
        self.turnNameTagsOn()
        self.av.b_clearTeleportFlag(PiratesGlobals.TFPotionCrafting)
        base.cr.loadingScreen.hide()
        base.transitions.setFadeColor(0, 0, 0)
        base.transitions.fadeIn(0.1)
        PlayerPirateGameFSM.exitPotionCrafting(self)

    def enterShipRepair(self, extraArgs=[]):
        PlayerPirateGameFSM.enterShipRepair(self, extraArgs)
        self.av.stopAutoRun()
        self.av.cameraFSM.request('Control')
        base.cr.interactionMgr.stop()
        self.av.guiMgr.combatTray.hide()
        self.av.guiMgr.hideTrackedQuestInfo()
        self.av.guiMgr.radarGui.show()
        self.turnNameTagsOff()

    def filterShipRepair(self, request, args=[]):
        if request in ('Emote', ):
            return None
        else:
            return self.defaultFilter(request, args)
        return None

    def exitShipRepair(self):
        PlayerPirateGameFSM.exitShipRepair(self)
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.start()
        self.av.guiMgr.combatTray.show()
        self.av.guiMgr.radarGui.show()
        self.av.guiMgr.showTrackedQuestInfo()
        self.turnNameTagsOn()

    def enterBenchRepair(self, extraArgs=[]):
        PlayerPirateGameFSM.enterBenchRepair(self, extraArgs)
        self.av.stopAutoRun()
        self.av.cameraFSM.request('Control')
        base.cr.interactionMgr.stop()
        self.av.guiMgr.combatTray.hide()
        self.av.guiMgr.hideTrackedQuestInfo()
        self.av.guiMgr.radarGui.show()
        self.turnNameTagsOff()

    def filterBenchRepair(self, request, args=[]):
        if request in ('Emote', ):
            return None
        else:
            return self.defaultFilter(request, args)
        return None

    def exitBenchRepair(self):
        PlayerPirateGameFSM.exitBenchRepair(self)
        base.cr.interactionMgr.stop()
        base.cr.interactionMgr.start()
        self.av.guiMgr.combatTray.show()
        self.av.guiMgr.radarGui.show()
        self.av.guiMgr.showTrackedQuestInfo()
        self.turnNameTagsOn()

    def enterTentacleTargeted(self, extraArgs=[]):
        PlayerPirateGameFSM.enterTentacleTargeted(self, extraArgs)
        tentacle = extraArgs[1]
        self.startLocalSequence()
        self.av.stopPosHprBroadcast()
        camParent = self.av.getShip().getModelRoot()
        camera.wrtReparentTo(camParent)
        pos = camParent.getRelativePoint(tentacle.creature, Point3(120, 120, 0) * 0.6)
        pos.setZ(80 * 0.6)
        self.camIval = self.lookMoveCameraSequence(2, pos)

    def exitTentacleTargeted(self):
        self.camIval.finish()
        base.transitions.letterboxOff()
        if not self.av.guiMgr.ignoreAllKeys:
            self.av.guiMgr.showTrays()
        self.av.guiMgr._showCursor()
        self.av.cameraFSM.request('FPS')
        PlayerPirateGameFSM.exitTentacleTargeted(self)

    def enterTentacleGrabbed(self, extraArgs=[]):
        PlayerPirateGameFSM.enterTentacleGrabbed(self, extraArgs)

    def filterTentacleGrabbed(self, request, args=[]):
        if request in ('TentacleGrabbed', 'Emote'):
            return None
        else:
            return self.defaultFilter(request, args)
        return None

    def exitTentacleGrabbed(self):
        self.av.startCompassEffect()
        PlayerPirateGameFSM.exitTentacleGrabbed(self)

    def enterCamera(self, extraArgs=[]):
        PlayerPirateGameFSM.enterCamera(self)
        self.av.cameraFSM.request('Control')
        self.av.guiMgr.hideTrays()

    def exitCamera(self):
        self.av.guiMgr.showTrays()
        PlayerPirateGameFSM.exitCamera(self)

    def startLocalSequence(self):
        self.av.guiMgr._hideCursor()
        self.av.motionFSM.off()
        self.av.stopAutoRun()
        self.av.guiMgr.request('Cutscene')
        self.av.cameraFSM.request('Control')
        base.transitions.letterboxOn()

    def endLocalSequence(self):
        base.transitions.letterboxOff()
        if not self.av.guiMgr.ignoreAllKeys:
            self.av.guiMgr.showTrays()
        self.av.guiMgr._showCursor()
        self.av.motionFSM.on()

    def rotateMoveCameraSequence(self, duration, pos, hpr, blendType='easeInOut'):
        start, end = getShortestRotation(camera.getH(), hpr[0])
        camera.setH(start)
        hpr.setX(end)
        return LerpPosHprInterval(camera, duration, pos, hpr, blendType=blendType)

    def lookMoveCameraSequence(self, duration, pos, wrtNode=None, lookAtNode=None, lookAtOffset=Point3(0), blendType='easeInOut'):

        def addTask(taskName):
            task = taskMgr.add(self.trackNode, taskName)
            task.lookAtNode = lookAtNode or self.av
            task.lookAtOffset = lookAtOffset

        return Sequence(Func(addTask, 'cameraPlayerTracking'), LerpPosInterval(camera, duration, pos, blendType=blendType, other=wrtNode), Func(taskMgr.remove, 'cameraPlayerTracking'))

    def trackNode(self, task):
        camera.lookAt(task.lookAtNode, task.lookAtOffset)
        return task.cont