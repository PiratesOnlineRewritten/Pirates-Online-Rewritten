from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.gui.OnscreenText import OnscreenText
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.PythonUtil import Functor, ScratchPad, report, lerp, quickProfile
from direct.distributed.ClockDelta import *
from direct.task import Task
from otp.otpbase import OTPRender
from otp.otpbase import OTPGlobals
from pirates.movement.DistributedMovingObject import DistributedMovingObject
from pirates.ship.DistributedFlagship import DistributedFlagship
from pirates.battle.Teamable import Teamable
from pirates.map.MinimapObject import GridMinimapObject
from pirates.battle import WeaponGlobals
from pirates.battle import DistributedShipCannon
from pirates.battle import DistributedBattleAvatar
from pirates.battle import CannonGlobals
from pirates.battle import EnemyGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import TeamUtils
from pirates.piratesbase import Freebooter
from pirates.piratesgui.ShipStatusDisplay import ShipStatusDisplay
from pirates.piratesgui import ShipTargetPanel
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import ShipFrameBoard
from pirates.piratesgui import PVPRankGui
from pirates.pvp import PVPGlobals
from pirates.ship import ShipCameraParams
from pirates.ship.GameFSMShip import GameFSMShip
from pirates.ship import ShipRocker
from pirates.ship import ShipPilot
from pirates.ship import ShipGlobals
from pirates.shipparts.WheelInteractive import WheelInteractive
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui.ShipTargets import ShipTargets, Target
from direct.controls import ControlManager
from pirates.audio import SoundGlobals
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.ShockwaveHit import ShockwaveHit
from pirates.audio.SoundGlobals import loadSfx
from pirates.inventory import ItemGlobals
from pirates.piratesgui import PVPRankGui
from direct.fsm.StatePush import FunctionCall
import ShipBalance
from pirates.effects import TextEffect
from pirates.piratesbase import TODGlobals
from pirates.ship import HighSeasGlobals
import random
import re
import math
STOP = 0
FWD = 1
BACK = -1
RIGHT = 1
LEFT = -1

def getRamSfx():
    hitSfxs = (
     loadSfx(SoundGlobals.SFX_FX_WOOD_IMPACT_01), loadSfx(SoundGlobals.SFX_FX_WOOD_IMPACT_03))
    return hitSfxs


class DistributedSimpleShip(DistributedMovingObject, Teamable, DistributedFlagship):
    notify = directNotify.newCategory('DistributedSimpleShip')
    deferrable = True
    fullBroadsides = config.GetBool('want-full-broadsides', 0)
    distantBreakSfx = None
    woodBreakSfx = None
    sailTearSfx = None
    SAIL_READY_DELAY = 1.4
    HpTextGenerator = TextNode('HpTextGenerator')
    hpModifier = 1.0
    cargoModifier = 0.0
    expModifier = 1.0
    Sp2indices = {ShipGlobals.SamplePoints.FL: (-1, 1),ShipGlobals.SamplePoints.F: (0, 1),ShipGlobals.SamplePoints.FR: (1, 1),ShipGlobals.SamplePoints.L: (-1, 0),ShipGlobals.SamplePoints.C: (0, 0),ShipGlobals.SamplePoints.R: (1, 0),ShipGlobals.SamplePoints.BL: (-1, -1),ShipGlobals.SamplePoints.B: (0, -1),ShipGlobals.SamplePoints.BR: (1, -1)}
    ActiveShips = set()
    NearbyShips = set()
    CannonFireDist = config.GetInt('cannon-fire-dist', PiratesGlobals.AI_CANNON_DIST_RANGE)
    CannonFireBroadsideDist = config.GetInt('cannon-fire-broadside-dist', PiratesGlobals.AI_CANNON_DIST_RANGE)
    ShipWakeDist = config.GetInt('ship-wake-dist', 3800)
    ShipRockDist = config.GetInt('ship-rock-dist', 1000)
    threatIconDict = None
    hunterIcon = None

    def __init__(self, cr):
        self.actorNode = ActorNode('simpleShip-physicsActor')
        self.shipClass = 0
        self.modelClass = 0
        self.initialGameState = None
        self.gameFSM = None
        self.broadsidePoints = []
        self.pendingCannons = None
        NodePath.__init__(self, self.actorNode)
        Teamable.__init__(self)
        DistributedMovingObject.__init__(self, cr)
        DistributedFlagship.__init__(self, cr)
        self.ownerId = 0
        self.steeringAvId = 0
        self.pilot = 0
        self.captainId = 0
        self.uniqueId = ''
        self.captainId = 0
        self.sinkTimeScale = 1.0
        self.armor = []
        self.mastStates = []
        self.mastHealth = []
        self.maxMastHealth = []
        self.repairSpots = {}
        self.sailsDown = False
        self.isFishing = False
        self.model = None
        self.crew = []
        self.boarders = []
        self.shipClass = None
        self.level = 0
        self.isFlagship = 0
        self.isNpc = 0
        self.wheel = None
        self.textEffects = []
        self.name = ''
        self._boardingTimer = None
        self.cannons = {}
        self.broadside = None
        self.zoneLocalShip = None
        self.maxHp = 0
        self.Hp = 0
        self.maxSp = 0
        self.Sp = 0
        self.cargo = []
        self.maxCargo = 0
        self.steeringAvId = 0
        self.isStatusDisplayVisible = 0
        self.autoSailing = False
        self.__readySails()
        self.stats = None
        self.boardableShipId = None
        self.pendingGrappledShip = None
        self.landedGrapples = []
        self.landedGrappleNodes = []
        self.boardingPanel = None
        self.boardingInProgress = 0
        self.skillEffects = {}
        self.enableAutoSail = 0
        self.lockedSails = False
        self.efficiency = False
        self.hideMask = BitMask32.allOff()
        self.localOnboard = False
        self.hideBoarded = False
        self.pendingDoMovie = None
        self.curAttackAnim = None
        self.controlManager = None
        self._shipCamParams = None
        self.respectDeployBarriers = False
        self.bandId = (0, 0)
        self.guildId = 0
        self.miniLog = None
        self.kraken = None
        self.krakenLocators = []
        self.oldZoom = None
        self.baseSpeedMod = 1.0
        self.speedUpgrade = 1.0
        self.turnUpgrade = 1.0
        self.sailMod = 1.0
        self.targets = ShipTargets(self)
        self.target = Target(self)
        self.minimapObj = None
        self.sinkTime = 0
        self.sinkTimestamp = 0
        self.shipTargetPanel = None
        self.nametag = None
        self.nametag3d = None
        self.shipStatusDisplay = None
        self.renownDisplay = None
        self.ownerId = 0
        self.badge = None
        self.worldVelocity = Vec3.zero()
        self.currentTurning = 0
        self.fullsailSfx = None
        self.rammingSfx = None
        if not self.sailTearSfx:
            DistributedSimpleShip.sailTearSfx = (
             loadSfx(SoundGlobals.SFX_SHIP_SAIL_TEAR),)
        if not self.woodBreakSfx:
            DistributedSimpleShip.woodBreakSfx = (
             loadSfx(SoundGlobals.SFX_FX_WOOD_IMPACT_01), loadSfx(SoundGlobals.SFX_FX_WOOD_IMPACT_02), loadSfx(SoundGlobals.SFX_FX_WOOD_IMPACT_03), loadSfx(SoundGlobals.SFX_FX_WOOD_IMPACT_04))
        if not self.distantBreakSfx:
            DistributedSimpleShip.distantBreakSfx = (
             loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_01), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_02), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_03), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_04), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_05), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_06), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_07), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_08), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_09), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_10))
        self.threatCounter = 0
        self.speedboost = 0
        self.speednerf = 0
        self.interactTube = None
        self.cAggroNodePath = None
        self.cAggroNode = None
        self.cAggro = None
        self._rocker = ShipRocker.ShipRocker()
        self.rockingTask = None
        self.iconNodePath = None
        self.collHandler = None
        self.rammingSphereNodePath = None
        self.shoutTextEffect = None
        self.cannonsVisible = False
        self.distanceToLocalShip = 99999
        self.shipDistanceCheck = None
        self.localAvPresent = False
        self.logo = ShipGlobals.Logos.Undefined
        self.style = ShipGlobals.Styles.Undefined
        self.logoOverride = None
        self.styleOverride = None
        if not self.threatIconDict:
            self.threatIconDict = {}
            threatCard = loader.loadModel('models/gui/ship_threat_icons')
            tpMgr = TextPropertiesManager.getGlobalPtr()
            for threatIconKey in EnemyGlobals.THREAT_ICON_DICT:
                threatIconName = EnemyGlobals.THREAT_ICON_DICT.get(threatIconKey)
                if threatIconName:
                    icon = threatCard.find('**/%s*' % threatIconName)
                    icon.setScale(2.0)
                    iconKey = 'threat-%s' % threatIconKey
                    self.threatIconDict[iconKey] = icon
                    tg = TextGraphic(icon, -0.25, 0.75, -0.31, 0.69)
                    tpMgr.setGraphic(iconKey, tg)

        if not self.hunterIcon:
            threatCard = loader.loadModel('models/gui/ship_threat_icons')
            tpMgr = TextPropertiesManager.getGlobalPtr()
            hunterIconName = 'threat_hunter'
            if threatIconName:
                icon = threatCard.find('**/%s*' % hunterIconName)
                icon.setScale(1.5)
                iconKey = 'hunterTAG'
                self.hunterIcon = icon
                tg = TextGraphic(icon, -0.25, 0.75, -0.31, 0.69)
                tpMgr.setGraphic(iconKey, tg)
        return

    def generate(self):
        DistributedMovingObject.generate(self)
        self.shipSunkEvent = self.uniqueName('shipSunk')

    def announceGenerate(self):
        self.actorNode.setName('ship-physicsactor-%d' % self.doId)
        DistributedSimpleShip.ActiveShips.add(self.doId)
        self.__initDistance()
        base.cr.loadingScreen.tick()
        self.hide(OTPRender.MainCameraBitmask)
        self.showThrough(OTPRender.EnviroCameraBitmask)
        self.calculateLook()
        self.buildShip()
        self.mastHealth = [ x[0] * (x[1] / 100.0) for x in zip(self.maxMastHealth, self.mastStates) ]
        self.armor = [ x[0] * (x[1] / 100.0) for x in zip(self.maxArmor, self.armorStates) ]
        self.Sp = sum(self.mastHealth)
        self.model.demandMastStates(self.mastStates, self.maxMastHealth)
        if self.model:
            self.model.setOwner(self)
        self.gameFSM = GameFSMShip(self)
        if self.initialGameState:
            self.requestGameState(self.initialGameState[0], *self.initialGameState[1])
            self.initialGameState = None
        modelRoot = self.getTransNode()
        if modelRoot:
            modelRoot.reparentTo(self)
        self.deckName = self.uniqueName('deck')
        self.railingName = self.uniqueName('railing')
        self.loadInterface()
        self.steeringSphereEvent = self.uniqueName('steeringSphere')
        self.steeringSphereEnterEvent = 'enter' + self.steeringSphereEvent
        self.exitWorldEvent = 'exitWorldBoundsSphere'
        self.accept('hide-ship-nametags', self.hideNametag)
        self.accept('show-ship-nametags', self.showNametag)
        self.zoneDistance = self.cr.addTaggedInterest(self.getDoId(), PiratesGlobals.ShipZoneDistance, self.cr.ITAG_GAME, self.uniqueName('distance'))
        self.showDebugName()
        self.setName(self.name)
        self.understandable = 1
        self.setPlayerType(NametagGroup.CCNormal)
        self.gameFSM.createGrappleProximitySphere()
        self.speedUpdate = FunctionCall(self.setSpeedMods, ShipBalance.SpeedModifier).pushCurrentState()
        self.setupSmoothing()
        if self.model:
            self.model.computeDimensions()
        self.avCannonNode = None
        self.avCannonRotate = None
        self.avCannonView = None
        self.avCannonPivot = None
        self.interactionCollisions = None
        modelRoot = self.getModelRoot()
        if modelRoot:
            self.avCannonNode = modelRoot.attachNewNode(ModelNode('avCannonNode'))
            self.avCannonRotate = self.avCannonNode.attachNewNode(ModelNode('avCannonRotate'))
            self.avCannonView = self.avCannonRotate.attachNewNode(ModelNode('avCannonView'))
            self.avCannonPivot = self.avCannonRotate.attachNewNode(ModelNode('avCannonPivot'))
            self.interactionCollisions = modelRoot.attachNewNode(ModelNode('interactCol'))
        self.lookAtDummy = self.attachNewNode('lookAtDummy')
        self.bow = None
        self.stern = None
        self._samplePoints = None
        self._sampleNPs = {}
        self.setupRocking()
        if self.modelClass in [ShipGlobals.SKEL_WARSHIPL3, ShipGlobals.SKEL_INTERCEPTORL3]:
            self.model.playStormEffect()
        self.updateShipEffects()
        DistributedMovingObject.announceGenerate(self)
        if self.sailsDown:
            self.model.instantSailing()
        else:
            self.model.instantDocked()
        self.checkMakeNametag(True)
        self.accept('localAvatar-BoardedShip', self.handleLocalBoarded)
        self.handleLocalBoarded(localAvatar.boardedShip)
        return

    def requestShow(self, hideMask=None):
        if hideMask:
            old = self.hideMask
            self.hideMask = self.hideMask ^ hideMask
        if self.hideMask == BitMask32.allOff():
            self.show()

    def requestHide(self, hideMask=None):
        if hideMask:
            old = self.hideMask
            self.hideMask = self.hideMask | hideMask
        if self.hideMask != BitMask32.allOff():
            self.hide()

    def handleLocalBoarded(self, hideBoarded):
        if hideBoarded != self.hideBoarded:
            self.hideBoarded = hideBoarded
            if hideBoarded:
                self.requestHide(PiratesGlobals.INVIS_EFFECIENCY)
            else:
                self.requestShow(PiratesGlobals.INVIS_EFFECIENCY)
        if localAvatar.doId in self.crew or localAvatar.doId in self.boarders or self.localOnboard:
            self.requestShow(PiratesGlobals.INVIS_EFFECIENCY)

    def getSkillBoost(self, skillId):
        return 0

    def setupRocking(self):
        if config.GetInt('ships-rock', 1) > 0 and self.allowedToRock():
            self._rocker.reset()
            self._rocker.setFakeMass(ShipGlobals.TiltFakeMass[self.modelClass])
            showSamplePoints = config.GetBool('show-ship-sample-points', False)
            self._samplePoints = self.attachNewNode('samplePoints')
            if showSamplePoints:
                axis = loader.loadModel('models/misc/xyzAxis')
            gx, gy = ShipGlobals.SamplePointOffsets[self.modelClass][0]
            for sp in ShipGlobals.SamplePoints:
                np = self._samplePoints.attachNewNode(ShipGlobals.SamplePoints.getString(sp))
                np.setX(gx + ShipGlobals.SamplePointOffsets[self.modelClass][1][sp][0])
                np.setY(gy + ShipGlobals.SamplePointOffsets[self.modelClass][1][sp][1])
                self._sampleNPs[sp] = np
                if showSamplePoints:
                    axis.instanceTo(np)

            self._maxSampleDistance = abs(self._sampleNPs[ShipGlobals.SamplePoints.C].getY() - self._sampleNPs[ShipGlobals.SamplePoints.F].getY())

    def setupBoardingSphere(self, bitmask=PiratesGlobals.RadarShipBitmask):
        self.removeBoardingSphere()
        tubeName = self.uniqueName('proximityCollision')
        result = self.createShipTube(tubeName, bitmask)
        self.interactTube = result[2]
        self.interactTube.setTag('objType', str(PiratesGlobals.COLL_AV))
        self.interactTube.setTag('avId', str(self.doId))
        sphereScale = ShipGlobals.getBoardingSphereScale(self.modelClass)
        spherePosH = ShipGlobals.getBoardingSpherePosH(self.modelClass)
        self.interactTube.setY(spherePosH[0][1])
        self.proximityCollisionEnterEvent = 'enter' + tubeName

    def removeBoardingSphere(self):
        if self.interactTube:
            self.interactTube.removeNode()

    def createShipTube(self, tubeName, bitmask, tangible=0):
        tubeSize = ShipGlobals.getBoardingSphereScale(self.modelClass)
        unboardTube = CollisionTube(0, -tubeSize, tubeSize * 0.4, 0, tubeSize, tubeSize * 0.4, tubeSize)
        unboardTube.setTangible(tangible)
        cSphereNode = CollisionNode(tubeName)
        cSphereNode.addSolid(unboardTube)
        unboardTubeNodePath = self.interactionCollisions.attachNewNode(cSphereNode)
        cSphereNode.setFromCollideMask(BitMask32.allOff())
        cSphereNode.setIntoCollideMask(bitmask)
        return [
         unboardTube, cSphereNode, unboardTubeNodePath]

    def disable(self):
        if self.model.sinkTrack:
            self.model.sinkTrack.pause()
            self.model.sinkTrack = None
            self.model.endSinkEffects()
        DistributedSimpleShip.ActiveShips.discard(self.doId)
        DistributedSimpleShip.NearbyShips.discard(self.doId)
        self.distanceToLocalShip = 9999999
        self._registerLocalDistance()
        self.stopDistanceChecks()
        self.removeDeckInterest()
        taskMgr.remove(self.getReadySailsTaskName())
        self.__readySails()
        if self.controlManager:
            self.controlManager.delete()
            self.controlManager = None
        if self.pendingCannons:
            self.cr.relatedObjectMgr.abortRequest(self.pendingCannons)
            self.pendingCannons = None
        if self.pendingDoMovie:
            self.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
            self.pendingDoMovie = None
        if self.pendingGrappledShip:
            self.cr.relatedObjectMgr.abortRequest(self.pendingGrappledShip)
            self.pendingGrappledShip = None
        self.removeLandedGrapples()
        self.cleanUpShipEffects()
        self.ignoreAll()
        self.stopAutoSailing()
        self.avCannonNode = None
        self.avCannonRotate = None
        self.avCannonView = None
        self.avCannonPivot = None
        self.interactionCollisions = None
        self._sampleNPs = {}
        if self._samplePoints:
            self._samplePoints.removeNode()
            self._samplePoints = None
        DistributedMovingObject.disable(self)
        self.unloadInterface()
        self.steeringAvId = 0
        self.kraken = None
        if self.zoneDistance:
            self.cr.removeTaggedInterest(self.zoneDistance, self.uniqueName('distance'))
            self.zoneDistance = None
        return

    def delete(self):
        if self.model:
            self.model.cleanup()
            self.model = None
        self.repairSpots = {}
        self.deleteNametag3d()
        if self.iconNodePath:
            self.iconNodePath.removeNode()
            self.iconNodePath = None
        if self.lookAtDummy:
            self.lookAtDummy.removeNode()
            self.lookAtDummy = None
        self.curAttackAnim = None
        self.broadside = None
        self.cannons = {}
        self.wheel = None
        self.fullsailSfx = None
        self.rammingSfx = None
        self._rocker.destroy()
        DistributedMovingObject.delete(self)
        self.targets.destroy()
        self.targets = None
        self.removeNode()
        self.gameFSM.cleanup()
        self.gameFSM = None
        DistributedFlagship.delete(self)
        return

    def setHullInfo(self, hullTextures, hullColors, stripeTextures, stripeColors, patternTextures, patternColors):
        self.hullInfo = [
         [
          hullTextures, hullColors], [stripeTextures, stripeColors], [patternTextures, patternColors]]

    def getSpawnPos(self):
        boardingSpots = []
        if self.model:
            boardingSpots = self.model.findAllMatches('**/boarding_spot_*;+s').asList()
        if len(boardingSpots) > 0:
            return boardingSpots[0].getPos() + Vec3(1, 0, 0)
        else:
            return Vec3(20, 0, 0)

    def localAvatarIncoming(self):
        if self.model:
            self.model.unstashPlaneCollisions()

    def getOpenPort(self):
        return 0

    def getThreatLevel(self):
        return 0

    def getHunterLevel(self):
        return 0

    def handleOutOfRange(self, entry):
        print '[DistributedSimpleShip] handleOutOfRange'
        if self.redirectTrack:
            self.redirectTrack.pause()
            self.redirectTrack = None
        oldHpr = self.getHpr()
        self.lookAt(0, 0, 0)
        newHpr = self.getHpr()
        self.redirectTrack = Sequence(LerpHprInterval(self, 5, newHpr, startHpr=oldHpr))
        self.redirectTrack.start()
        return

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='shipboard')
    def setCrew(self, crewArray):
        if self.crew != crewArray:
            messenger.send('setShipCrew-%s' % self.getDoId(), [
             crewArray, self.maxCrew])
        self.crew = crewArray
        self.updatePickable()

    def getCrew(self):
        return self.crew

    def setBoarders(self, boarders):
        self.boarders = boarders

    def startSteering(self, pilotId):
        print '[DistributedSimpleShip] startSteering %s' % pilot
        if localAvatar.doId == pilotId:
            localAvatar.b_setGameState('ShipPilot', [self])
            self.accept(self.exitWorldEvent, self.handleOutOfRange)

    def canTakeWheel(self, wheel, avId=None):
        if self.pilot:
            return False
        return True

    def sinkingBegin(self):
        self.minimapObj.removeFromMap()
        messenger.send(self.uniqueName('shipSinking'))
        if self.model:
            self.model.sinkTimeScale = self.sinkTimeScale
            self.model.sinkingBegin()
        self.removeTarget()
        self.stopShipRocking()
        self.hideNametag()
        if self.modelClass in [ShipGlobals.SKEL_WARSHIPL3, ShipGlobals.SKEL_INTERCEPTORL3]:
            self.model.stopStormEffect()
        if self.isInCrew(localAvatar.doId):
            self.disableOnDeckInteractions()

    def sinkingEnd(self):
        if self.model:
            self.model.sinkingEnd()
        self.unloadInterface()
        messenger.send(self.shipSunkEvent)

    def setLevel(self, level):
        self.level = level

    def getLevel(self):
        return self.level

    def buildShip(self):
        self.model = base.shipFactory.getShip(self.shipClass, self.getStyle(), self.getLogo(), detailLevel=base.options.terrain_detail_level)

    def calculateLook(self):
        stats = ShipGlobals.getShipConfig(self.shipClass)
        self.style = self.styleOverride or stats['defaultStyle']
        self.logo = self.logoOverride or stats['sailLogo']

    def getStyle(self):
        return self.style

    def getLogo(self):
        return self.logo

    def setLogoOverride(self, logoOverride):
        if logoOverride != ShipGlobals.Logos.Undefined:
            self.logoOverride = logoOverride

    def setStyleOverride(self, styleOverride):
        if styleOverride != ShipGlobals.Styles.Undefined:
            self.styleOverride = styleOverride

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam=['shipboard', 'shipsink'])
    def setGameState(self, stateName, avId, timeStamp, localChange=0):
        if stateName == 'ClientSteering':
            s = MiniLogSentry(self.miniLog, 'setGameState', stateName, avId, timeStamp)
            self.requestGameState(stateName, avId)
        elif stateName == 'AISteering':
            self.requestGameState(stateName, avId)
        else:
            self.requestGameState(stateName)

    def requestGameState(self, state, *args):
        if self.gameFSM:
            self.gameFSM.request(state, *args)
        else:
            self.initialGameState = (
             state, args)

    def getGameState(self):
        if self.gameFSM:
            return self.gameFSM.state
        elif self.initialGameState:
            return self.initialGamesState[0]
        else:
            return None
        return None

    def stash(self, *args, **kw):
        if not self:
            return
        DistributedMovingObject.stash(self, *args, **kw)

    def unstash(self, *args, **kw):
        if not self:
            return
        DistributedMovingObject.unstash(self, *args, **kw)

    def getActorNode(self):
        return None

    def registerMainBuiltFunction(self, func, extraArgs=[], extraKwArgs={}):
        func(*extraArgs, **extraKwArgs)

    def removeTarget(self, shipId=0):
        pass

    def isInCrew(self, avId):
        return avId in self.getCrew()

    def isInBoarders(self, avId):
        return avId in self.boarders

    def onThisShip(self, avId):
        return self.isInCrew(avId) or self.isInBoarders(avId)

    def createWake(self):
        if self.model and not self.model.hasWake():
            self.model.createWake()

    def removeWake(self):
        if self.model and self.model.hasWake():
            self.model.removeWake()

    def findLocators(self, name):
        if self.model:
            return self.model.locators.findAllMatches(name)
        else:
            return NodePathCollection()

    def findLocator(self, name):
        if self.model:
            return self.model.locators.find(name)
        else:
            return NodePath()

    def getModelRoot(self):
        if self.model:
            return self.model.modelRoot
        else:
            return NodePath()

    def getShipRoot(self):
        if self.model:
            return self.model.shipRoot
        else:
            return NodePath()

    def getLODRoot(self):
        if self.model:
            return self.model.lod
        else:
            return NodePath()

    def getTransNode(self):
        if self.model:
            return self.model.transRoot
        else:
            return NodePath()

    def hideSmoke(self):
        pass

    def showSmoke(self):
        pass

    def listenForFloorEvents(self, on):
        pass

    def getInventory(self):
        return None

    def printExpText(self, totalExp, colorSetting, basicPenalty, crewBonus, doubleXPbonus, holidayBonus, potionBonus):
        taskMgr.doMethodLater(0.5, self.showHpText, self.taskName('printExp'), [
         totalExp, colorSetting, 6.0, 1.0, 0, basicPenalty, crewBonus, doubleXPbonus, holidayBonus, potionBonus])

    def showHpText(self, number, bonus=0, duration=2.0, scale=1.0, pos=None, basicPenalty=0, crewBonus=0, doubleXPBonus=0, holidayBonus=0, potionBonus=0, itemEffects=[]):
        if self.isEmpty():
            return
        distance = camera.getDistance(self)
        scale *= max(1.0, distance / 25.0)
        posAndScale = self.getDebugNamePosScale()
        height = posAndScale[0][2]
        startPos = (0, 0, height / 4)
        destPos = (0, 0, height / 2)
        if pos:
            startPos = pos
            destPos = (pos[0], pos[1], pos[2] + height / 4)
        newEffect = None

        def cleanup():
            if newEffect in self.textEffects:
                self.textEffects.remove(newEffect)

        mods = {}
        if basicPenalty > 0:
            mods[TextEffect.MOD_BASICPENALTY] = basicPenalty
        if crewBonus > 0:
            mods[TextEffect.MOD_CREWBONUS] = crewBonus
        if doubleXPBonus > 0:
            mods[TextEffect.MOD_2XPBONUS] = doubleXPBonus
        if holidayBonus > 0:
            mods[TextEffect.MOD_HOLIDAYBONUS] = holidayBonus
        if ItemGlobals.CRITICAL in itemEffects:
            scale *= 1.5
        effect = TextEffect.genTextEffect(self, self.HpTextGenerator, number, bonus, self.isNpc, Functor(self.removeEffect, newEffect), startPos, destPos, scale, modifiers=mods, effects=itemEffects)
        if effect:
            self.textEffects.append(effect)
        return

    def removeEffect(self, effect):
        if effect in self.textEffects:
            self.textEffects.remove(effect)

    def addGrappleTarget(self, target, locator, offset):
        modelRoot = self.getModelRoot()
        if modelRoot:
            target.setPos(locator.getPos())
            target.setX(target.getX() - offset)
            target.reparentTo(modelRoot)

    @report(types=['args'], dConfigParam=['dteleport'])
    def placeLocalAvatar(self, av, posh=None):
        if not posh:
            posh = self.getRandomBoardingPosH()
        av.reparentTo(self.getModelRoot())
        av.setPosHpr(posh[0], posh[1], posh[2], posh[3], 0, 0)
        av.cnode.broadcastPosHprFull()

    def placeLocalAvatarForSwinging(self, av):
        pos = av.getPos(self.getModelRoot())
        h = av.getH(self.getModelRoot())
        self.placeLocalAvatar(av, (pos[0], pos[1], pos[2], h))

    def boardShip(self, boardingSpot):
        localAvatar.b_boardShip(self.getDoId(), boardingSpot)

    def swingToShip(self, boardingSpot):
        localAvatar.b_swingToShip(self.getDoId(), boardingSpot)

    def getBuildComplete(self):
        return True

    def enableOnDeckInteractions(self):
        self.notify.debug('enableOnDeckInteractions')
        for cannon in self.cannons.values():
            if cannon[1]:
                cannon[1].setAllowInteract(1)
                cannon[1].checkInUse()
                cannon[1].refreshState()

        if self.wheel:
            if self.wheel[1]:
                self.wheel[1].setAllowInteract(1)
                self.wheel[1].checkInUse()
                self.wheel[1].refreshState()
        for spot in self.repairSpots.values():
            spot.setAllowInteract(1)
            spot.checkInUse()
            spot.refreshState()

    def disableOnDeckInteractions(self):
        self.notify.debug('disableOnDeckInteractions')
        for cannon in self.cannons.values():
            if cannon[1]:
                cannon[1].setAllowInteract(0, forceOff=True)
                cannon[1].refreshState()

        if self.wheel:
            if self.wheel[1]:
                self.wheel[1].setAllowInteract(0, forceOff=True)
                self.wheel[1].refreshState()
        for spot in self.repairSpots.values():
            spot.setAllowInteract(0, forceOff=True)
            spot.refreshState()

    def setupFloatTask(self):
        if base.cr.activeWorld:
            self.startShipRocking(startOffset=random.uniform(0, 360))

    def cleanupFloatTask(self, water=None):
        self.stopShipRocking()

    def startShipRocking(self, startOffset=0, wantRocking=1):
        if self.rockingTask:
            return
        task = taskMgr.add(self.shipRockingTask, self.uniqueName('shipRocking'), priority=24)
        task.sRockT = random.random() * 1000.0
        self.rockingTask = task

    def stopShipRocking(self):
        if self.rockingTask:
            self.rockingTask.remove()
            self.rockingTask = None
        return

    def shipRockingTask(self, task):
        shipsRock = config.GetInt('ships-rock', 1) and self.allowedToRock()
        if shipsRock == 0 or shipsRock == 2 and localAvatar.ship is not self:
            if config.GetBool('want-compass-task', 1):
                loadPrcFileData('', '%s %s' % ('want-compass-task', 0))
            return task.cont
        transNode = self.getTransNode()
        if transNode == None:
            return task.cont
        if not self._sampleNPs:
            self.setupRocking()
        world = self.cr.getActiveWorld()
        water = None
        if world:
            water = world.getWater()
        if not water:
            return task.again
        lrAngle = [
         0.0]
        fbAngle = [0.0]
        avgWaveHeight = [0.0]
        shipModelHeightOffset = self.getShipModelHeightOffset()

        def calcWithoutWaves():
            shipsRock = config.GetInt('ships-rock-without-waves', 1)
            if shipsRock == 1 or shipsRock == 2 and localAvatar.ship is self:
                flatWellScale = water.calcFlatWellScale(node=self)
                frontBackPeriod = 14.7
                leftRightPeriod = 14.7
                upDownPeriod = 7.1
                elapsed = task.time
                speed = (self.getPrevTransform().getPos() - self.getPos()).length()
                task.sRockT += globalClock.getDt() + speed * 0.05
                twoPi = 2.0 * math.pi
                q = elapsed * twoPi
                q2 = q / 0.7
                udQ = task.sRockT * twoPi
                udQ2 = udQ / 0.7
                fbQ = 2.0 * task.sRockT * twoPi
                fbQ2 = fbQ / 0.7
                fbTheta = fbQ / frontBackPeriod
                fbTheta2 = fbQ2 / frontBackPeriod
                lrTheta = q / leftRightPeriod
                lrTheta2 = q2 / leftRightPeriod
                udTheta = udQ / upDownPeriod
                udTheta2 = udQ2 / upDownPeriod
                sineMagnitude = flatWellScale * 6.0 / self._tiltFakeMass
                sineMagnitude2 = flatWellScale * sineMagnitude * 0.25
                fbAngle[0] = sineMagnitude * math.sin(fbTheta) + sineMagnitude2 * math.sin(fbTheta2)
                lrAngle[0] = sineMagnitude * math.sin(lrTheta) + sineMagnitude2 * math.sin(lrTheta2)
                avgWaveHeight[0] = 0.1 * (sineMagnitude * math.sin(udTheta) + sineMagnitude2 * math.sin(udTheta2))
                return True
            return False

        avgLRheight = [
         0.0, 0.0, 0.0]
        avgFBheight = [0.0, 0.0, 0.0]

        def calcWithWaves():
            for sp, node in self._sampleNPs.items():
                height = water.calcFilteredHeight(minWaveLength=3.0 * self._maxSampleDistance, node=node)
                if height == 0:
                    if config.GetBool('ships-rock-fakely', 0):
                        calcWithoutWaves()
                    return False
                avgWaveHeight[0] += height
                lrIndex, fbIndex = DistributedSimpleShip.Sp2indices[sp]
                avgLRheight[lrIndex] += height
                avgFBheight[fbIndex] += height

            avgWaveHeight[0] /= len(self._sampleNPs)
            fl = self._sampleNPs[ShipGlobals.SamplePoints.FL]
            lrDist = abs(fl.getX())
            fbDist = abs(fl.getY())
            a = (avgLRheight[0] - avgLRheight[-1]) / 3.0
            b = (avgLRheight[1] - avgLRheight[0]) / 3.0
            lrAvg = (a + b) / 2.0
            a = (avgFBheight[0] - avgFBheight[-1]) / 3.0
            b = (avgFBheight[1] - avgFBheight[0]) / 3.0
            fbAvg = (a + b) / 2.0
            lrAngle[0], fbAngle[0] = self.debugFunc(lrAvg, fbAvg, lrDist, fbDist)
            return True

        if not water.patch.getAnimateHeight():
            rocking = calcWithoutWaves()
        else:
            rocking = calcWithWaves()

        def capRocking(targetP=0, targetR=0, targetZ=0):
            maxAdjustP = 0.38
            maxAdjustR = 0.52
            maxAdjustZ = 0.5
            currP = transNode.getP()
            currR = transNode.getR()
            currZ = transNode.getZ()
            maxP = max(min(targetP - currP, maxAdjustP), -maxAdjustP)
            maxR = max(min(targetR - currR, maxAdjustR), -maxAdjustR)
            maxZ = max(min(targetZ - currZ, maxAdjustZ), -maxAdjustZ)
            transNode.setP(currP + maxP)
            transNode.setR(currR + maxR)
            transNode.setZ(currZ + maxZ)

        if not rocking:
            capRocking(targetZ=shipModelHeightOffset)
            return Task.cont
        maxSpd = 40.0
        velVec = self.actorNode.getPhysicsObject().getVelocity()
        speed = velVec.length()
        normSpeed = min(speed / maxSpd, 1.0)
        velVec.normalize()
        rotMat = Mat3.rotateMatNormaxis(self.getH(), Vec3.up())
        fwdVec = rotMat.xform(Vec3.forward())
        rightVec = rotMat.xform(Vec3.right())
        leanValue = -40.0 * clampScalar(velVec.dot(rightVec) * 2.0, -1.0, 1.0) * normSpeed
        tiltMult = lerp(0.9, 0.4, normSpeed)
        if not hasattr(base, 'localAvatar') or base.localAvatar.ship == self and self.steeringAvId != localAvatar.doId:
            tiltMult *= 0.1
        if self.gameFSM.state == 'KrakenPinned':
            rollAngle = self.kraken.getRollAngle()
            tiltMult *= 1 - self.kraken.getDampenAmount()
        else:
            rollAngle = self._rocker.getRollAngle()
        rollAngle += leanValue
        capRocking(tiltMult * fbAngle[0], tiltMult * (lrAngle[0] + rollAngle), avgWaveHeight[0] + shipModelHeightOffset)
        return Task.cont

    def getShipModelHeightOffset(self):
        rockInfo = ShipGlobals.SamplePointOffsets.get(self.modelClass, [])
        if len(rockInfo) > 2:
            return rockInfo[2]
        else:
            return 0

    @exceptionLogged()
    def debugFunc(self, lrAvg, fbAvg, lrDist, fbDist):
        return (
         -math.atan(lrAvg / lrDist) * 180.0 / math.pi, math.atan(fbAvg / fbDist) * 180.0 / math.pi)

    def forceZoneLevel(self, level):
        pass

    def turnOn(self):
        pass

    def disableAllLODSpheres(self):
        pass

    def enableAllLODSpheres(self):
        pass

    def clearAllEnabled(self, resetLastZoneLevel=False):
        pass

    def setZoneLevel(self, level, entry=None):
        pass

    def registerBuildCompleteFunction(self, func, extraArgs=[], extraKwArgs={}):
        func(*extraArgs, **extraKwArgs)

    def setArmorStates(self, rear, left, right):
        self.armorStates = [
         rear, left, right]
        self.armor = [ x[0] * (x[1] / 100.0) for x in zip(self.maxArmor, self.armorStates) ]
        self.adjustArmorDisplay()
        self.updateShipEffects()

    def getArmorStates(self):
        return self.armorStates

    def setHealthState(self, health):
        self.healthState = health
        self.Hp = self.maxHp * (self.healthState / 100.0)
        messenger.send('setShipHp-%s' % self.getDoId(), [self.Hp, self.maxHp])
        if self.shipTargetPanel:
            self.shipTargetPanel.hpMeter['range'] = self.maxHp
            self.shipTargetPanel.hpMeter['value'] = self.Hp
        self.updateShipEffects()

    def getHealthState(self):
        return self.healthState

    def setMastStates(self, mainMast1, mainMast2, mainMast3, aftMast, foreMast):
        newMastStates = [
         mainMast1, mainMast2, mainMast3, aftMast, foreMast]
        if not self.mastStates:
            self.mastStates = newMastStates
        elif newMastStates == self.mastStates:
            return
        for i in range(5):
            if self.maxMastHealth[i]:
                newVal = newMastStates[i]
                oldVal = self.mastStates[i]
                if newVal != oldVal:
                    if newVal == 0:
                        self.model.breakMast(i)
                    elif oldVal == 0:
                        self.model.restoreMast(i)

        self.mastStates = newMastStates
        self.mastHealth = [ x[0] * (x[1] / 100.0) for x in zip(self.maxMastHealth, self.mastStates) ]
        self.Sp = sum(self.mastHealth)
        if self.shipTargetPanel:
            self.shipTargetPanel.speedMeter['range'] = self.maxSp
            self.shipTargetPanel.speedMeter['value'] = self.Sp
        messenger.send('setShipSp-%s' % self.getDoId(), [self.Sp, self.maxSp])
        self.calcModifiedStats()
        messenger.send(self.uniqueName('update-mast-health'), self.mastHealth)

    def getMastStates(self):
        return self.mastStates

    def setIsFlagship(self, isFlagship):
        if isFlagship != self.isFlagship:
            self.isFlagship = isFlagship

    def queryGameState(self):
        return self.gameFSM.getCurrentOrNextState()

    def isSailable(self):
        return self.queryGameState() not in ('FadeOut', 'Sunk', 'Sinking', 'PutAway',
                                             'Off')

    def setUniqueId(self, uid):
        if self.uniqueId != '' and uid != self.uniqueId:
            base.cr.uidMgr.removeUid(self.uniqueId)
        self.uniqueId = uid
        base.cr.uidMgr.addUid(self.uniqueId, self.getDoId())

    def getUniqueId(self):
        return self.uniqueId

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='shipboard')
    def setMovie(self, mode, avId, fromShipId, instant, timestamp):
        self.notify.debug('setMovie %s, %s, %s, %s, %s' % (mode, avId, fromShipId, instant, timestamp))

        def doMovie(args):
            fromShip = None
            av = None
            if args[0] == None or args[1] == None:
                return
            av, fromShip = args
            if timestamp is None:
                ts = 0.0
            else:
                ts = globalClockDelta.localElapsedTime(timestamp)
            currentState = av.gameFSM.getCurrentOrNextState()
            if currentState != 'ShipBoarding':
                av.gameFSM.request('ShipBoarding', [self, fromShip, ts])
            return

        if self.pendingDoMovie:
            self.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
            self.pendingDoMovie = None
        self.pendingDoMovie = self.cr.relatedObjectMgr.requestObjects([avId], eachCallback=doMovie, timeout=60)
        return

    def grappledShip(self, ship):
        self.engagedFlagship()
        if self.isInCrew(localAvatar.doId):
            localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.FlagshipGrappleLerpingInstructions)

    def setLandedGrapples(self, landedGrapples):

        def setGrapplesOnModel(ship):
            if ship:
                self.model.setLandedGrapples(ship, landedGrapples)

        if landedGrapples:
            if self.pendingGrappledShip:
                self.cr.relatedObjectMgr.abortRequest(self.pendingGrappledShip)
                self.pendingGrappledShip = None
            shipId = landedGrapples[0][0]
            self.pendingGrappledShip = self.cr.relatedObjectMgr.requestObjects([shipId], eachCallback=setGrapplesOnModel, timeout=60)
        else:
            self.removeLandedGrapples()
        return

    def removeLandedGrapples(self):
        if self.pendingGrappledShip:
            self.cr.relatedObjectMgr.abortRequest(self.pendingGrappledShip)
            self.pendingGrappledShip = None
        self.model.removeLandedGrapples()
        return

    def setSinkTimer(self, duration, timestamp):
        self.sinkTime = duration
        self.sinkTimestamp = timestamp
        dt = globalClockDelta.localElapsedTime(self.sinkTimestamp)
        if self.shipTargetPanel:
            if self.sinkTime > dt >= 0:
                self.shipTargetPanel.setTimer(self.sinkTime - dt)
                self.shipTargetPanel.timer.countdown(self.sinkTime - dt)
            else:
                self.shipTargetPanel.stopTimer()

    def rammingOn(self):
        base.cTrav.addCollider(self.rammingSphereNodePath, self.collHandler)

    def rammingOff(self):
        base.cTrav.removeCollider(self.rammingSphereNodePath)

    def setupRammingCollisions(self):
        enterCollEvent = self.uniqueName('enterRammingEvent')
        exitCollEvent = self.uniqueName('exitRammingEvent')
        if not self.rammingSphereNodePath:
            x, y, z, s = ShipGlobals.getRammingSphereScale(self.modelClass)
            cSphere = CollisionSphere(x, y, z, s)
            cSphere.setTangible(0)
            rammingEvent = self.uniqueName('ShipRammingEvent')
            cSphereNode = CollisionNode(rammingEvent)
            cSphereNode.setFromCollideMask(PiratesGlobals.ShipCollideBitmask)
            cSphereNode.setIntoCollideMask(BitMask32.allOff())
            cSphereNode.addSolid(cSphere)
            self.rammingSphereNodePath = self.interactionCollisions.attachNewNode(cSphereNode)
            self.rammingSphereNodePath.stash()
            self.collHandler = CollisionHandlerEvent()
            self.collHandler.addInPattern(enterCollEvent)
            self.collHandler.addOutPattern(exitCollEvent)
        self.accept(enterCollEvent, self.enterShipEvent)
        self.accept(exitCollEvent, self.exitShipEvent)

    def cleanupRammingCollisions(self, stash=False):
        enterCollEvent = self.uniqueName('enterRammingEvent')
        exitCollEvent = self.uniqueName('exitRammingEvent')
        self.ignore(enterCollEvent)
        self.ignore(exitCollEvent)
        if not stash:
            if self.collHandler:
                base.cTrav.removeCollider(self.rammingSphereNodePath)
                self.collHandler = None
            if self.rammingSphereNodePath:
                self.rammingSphereNodePath.remove()
                self.rammingSphereNodePath = None
        return

    def isRamming(self):
        for buffKeyId in self.skillEffects.keys():
            buffId = self.skillEffects[buffKeyId][0]
            if WeaponGlobals.C_RAM == buffId:
                return True

        return False

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='shipboard')
    def clientSteeringBegin(self, avId):
        self.steeringAvId = avId
        av = self.cr.doId2do.get(self.steeringAvId)
        if not av:
            return
        if av.isLocal() and self.wheel:
            s = MiniLogSentry(self.miniLog, 'clientSteeringBegin', avId)
            self.calcModifiedStats()
            if base.options.terrain_detail_level != 2:
                self.model.forceLOD(1)
            if self.broadside:
                if self.broadside[1]:
                    self.broadside[1].setLocalAvatarUsingWeapon(1)
                    self.broadside[1].av = av
            self.wheel[1].acceptInteraction()
            base.localAvatar.guiMgr.setIgnoreEscapeHotKey(True)
            localAvatar.b_setGameState('ShipPilot', [self])
            self.accept(self.exitWorldEvent, self.handleOutOfRange)
            self.enableShipControls()
            self.setupRammingCollisions()
            collNPs = self.getModelCollisionRoot().findAllMatches('**/+CollisionNode')
            self.disabledCollisionBits = {}
            for np in collNPs:
                cMask = np.node().getIntoCollideMask()
                disabledBits = BitMask32()
                if not (cMask & PiratesGlobals.CameraBitmask).isZero():
                    cMask ^= PiratesGlobals.CameraBitmask
                    disabledBits |= PiratesGlobals.CameraBitmask
                if not (cMask & PiratesGlobals.FloorBitmask).isZero():
                    cMask ^= PiratesGlobals.FloorBitmask
                    disabledBits |= PiratesGlobals.FloorBitmask
                if not disabledBits.isZero():
                    np.node().setIntoCollideMask(cMask)
                    self.disabledCollisionBits[np] = disabledBits

            if self.broadside:
                if self.broadside[1]:
                    self.broadside[1].localPirate = 1
            self.checkAbleDropAnchor()
            self.accept('w', self.startAutoSailing)
            self.accept('arrow_up', self.startAutoSailing)
            av.stopSmooth()
            base.avatarPhysicsMgr.attachPhysicalNode(self.actorNode)

    @report(types=['frameCount', 'deltaStamp'], dConfigParam=['shipboard', 'shipsink'])
    def clientSteeringEnd(self):
        if not self.steeringAvId:
            return
        av = base.cr.doId2do.get(self.steeringAvId)
        if not av:
            self.notify.warning('avId: %s not found' % self.steeringAvId)
            return
        if av.isLocal():
            self.stopAutoSailing()
            self.model.clearForceLOD()
            if self.broadside:
                if self.broadside[1]:
                    self.broadside[1].setLocalAvatarUsingWeapon(0)
                    self.broadside[1].av = None
            base.localAvatar.guiMgr.setIgnoreEscapeHotKey(False)
            self.ignore('escape')
            self.ignore(self.stopSteeringEvent)
            self.ignore(self.exitWorldEvent)
            taskMgr.remove(self.getReadySailsTaskName())
            self.__readySails()
            self.cleanupRammingCollisions(stash=True)
            self.disableShipControls()
            localAvatar.cameraFSM.getOrbitCamera().setSubject(None)
            if self.shipStatusDisplay:
                self.shipStatusDisplay.disableAnchorButton()
                self.shipStatusDisplay.hideWrongPort()
            if localAvatar.getGameState() == 'ShipPilot':
                localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
            for np, disabledBits in self.disabledCollisionBits.items():
                cMask = np.node().getIntoCollideMask()
                cMask |= disabledBits
                np.node().setIntoCollideMask(cMask)

            self.disabledCollisionBits = {}
            if self.broadside:
                if self.broadside[1]:
                    self.broadside[1].localPirate = 0
            modelRoot = self.getModelRoot()
            if modelRoot:
                av.wrtReparentTo(modelRoot)
            av.startSmooth()
            wheelpost = self.findLocator('**/location_wheel;+s')
            if modelRoot:
                av.setPos(wheelpost.getPos(modelRoot) - Vec3(0.56, 3.0, 0))
                av.setH(0)
            base.avatarPhysicsMgr.removePhysicalNode(self.actorNode)
        self.steeringAvId = 0
        self.ignore('arrow_up')
        self.ignore('w')
        return

    def enableShipControls(self):
        base.cr.activeWorld.worldGrid.visAvatar = self
        localAvatar.controlManager.stop()
        if not self.controlManager:
            self.setupControls()
        self.controlManager.enable()
        self.controlManager.use('ship', self)
        self.controlManager.currentControls.enableAvatarControls()
        self.controlManager.setTag('avId', str(localAvatar.getDoId()))
        self.controlManager.setTag('shipId', str(self.getDoId()))
        localAvatar.cameraFSM.request('Orbit', self)
        localAvatar.cameraFSM.orbitCamera.pushParams()
        camParams = self.retrieveCamParams()
        if not camParams:
            camParams = ShipCameraParams.ShipModelClass2CameraParams[self.modelClass]
        camParams.applyTo(localAvatar.cameraFSM.orbitCamera)
        localAvatar.cameraFSM.orbitCamera.popToIdealDistance()
        base.localAvatar.guiMgr.combatTray.initCombatTray(InventoryType.SailingRep)
        base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTray(rep=InventoryType.SailingRep, weaponMode=WeaponGlobals.SAILING)

    def disableShipControls(self):
        if localAvatar.cameraFSM.getOrbitCamera().getSubject():
            curParams = localAvatar.cameraFSM.orbitCamera.popParams()
            self.storeCamParams(curParams)
        else:
            self.notify.warning('disableShipControls: no orbitCam subject, cannot preserve ship camera settings')
        controls = self.controlManager.currentControls
        if controls:
            controls.disableAvatarControls()
        self.controlManager.disable()
        if base.cr.activeWorld.worldGrid:
            base.cr.activeWorld.worldGrid.visAvatar = localAvatar
        self.ignore('avatarZoneChanged')
        base.localAvatar.guiMgr.combatTray.skillTray.hideSkillTray()
        base.localAvatar.guiMgr.combatTray.initCombatTray(localAvatar.currentWeaponId)

    def loadInterface(self):
        self.stopSteeringEvent = self.uniqueName('stopSteering')
        self.stopCannonEvent = self.uniqueName('stopCannon')

    def loadShipStatusDisplay(self):
        if self.shipStatusDisplay or base.cr.tutorial:
            return
        if base.config.GetBool('want-sea-infamy', 0) and not self.renownDisplay:
            self.renownDisplay = PVPRankGui.PVPRankGui(parent=base.a2dBottomRight, displayType=PVPRankGui.SHIP_RENOWN_DISPLAY)
            self.renownDisplay.reparentTo(base.a2dBottomRight, sort=-1)
        self.shipStatusDisplay = ShipStatusDisplay(parent=base.a2dTopLeft, shipId=self.getDoId(), shipName=(self.name, self.getTeam()), shipClass=self.shipClass, shipHp=(self.Hp, self.maxHp), shipSp=(self.Sp, self.maxSp), shipCargo=(self.cargo, self.maxCargo), shipCrew=(self.crew, self.maxCrew), ownShip=base.cr.hasOwnerViewDoId(self.getDoId()) or self.isFishing and self.isCaptain(localAvatar.getDoId()))
        self.adjustArmorDisplay()
        self.shipStatusDisplay.hide()
        if self.renownDisplay:
            self.renownDisplay.hide()
        self.refreshStatusTray()

    def loadShipTargetPanel(self):
        if self.shipTargetPanel or base.cr.tutorial:
            return
        self.loadShipStatusDisplay()
        self.shipTargetPanel = ShipTargetPanel.ShipTargetPanel(self)
        self.shipTargetPanel.hide()
        self.adjustArmorDisplay()

    def showStatusDisplay(self):
        self.loadShipStatusDisplay()
        self.isStatusDisplayVisible += 1
        self.__checkStatusDisplayVisible()

    def hideStatusDisplay(self):
        self.isStatusDisplayVisible = max(self.isStatusDisplayVisible - 1, 0)
        self.__checkStatusDisplayVisible()

    def __checkStatusDisplayVisible(self):
        if self.shipStatusDisplay:
            if self.isStatusDisplayVisible > 0:
                self.shipStatusDisplay.show()
                if self.getSiegeTeam() and self.renownDisplay:
                    self.renownDisplay.show()
            else:
                self.shipStatusDisplay.hide()
                if self.renownDisplay:
                    self.renownDisplay.hide()

    def showTargets(self):
        if self.targets:
            self.targets.show()

    def hideTargets(self):
        if self.targets:
            self.targets.hide()

    def unloadInterface(self):
        if self.target:
            self.target.destroy()
            self.target = None
        if self.shipTargetPanel:
            self.shipTargetPanel.destroy()
            self.shipTargetPanel = None
        if self.shipStatusDisplay:
            self.shipStatusDisplay.destroy()
            self.shipStatusDisplay = None
        if self.renownDisplay:
            self.renownDisplay.destroy()
            self.renownDisplay = None
        return

    def addDeckInterest(self):
        self.zoneLocalShip = self.cr.addTaggedInterest(self.getDoId(), PiratesGlobals.ShipZoneOnDeck, self.cr.ITAG_GAME, self.uniqueName('localShip'))

    def removeDeckInterest(self):
        if self.zoneLocalShip:
            self.cr.removeTaggedInterest(self.zoneLocalShip)

    @report(types=['args'], dConfigParam=['dteleport'])
    def handleChildArrive(self, child, zoneId):
        DistributedMovingObject.handleChildArrive(self, child, zoneId)
        child.handleArrivedOnShip(self)

    @report(types=['args'], dConfigParam=['dteleport'])
    def battleAvatarArrived(self, av):
        av.wrtReparentTo(self.getModelRoot())

    @report(types=['args'], dConfigParam=['dteleport'])
    def battleNpcArrived(self, av):
        av.onShipWithLocalAv(self.localAvPresent)

    @report(types=['args'], dConfigParam=['dteleport'])
    def playerPirateArrived(self, av):
        pass

    @report(types=['args'], dConfigParam=['dteleport'])
    def localPirateArrived(self, av):
        self.localAvPresent = True
        self.enableGridInterest()
        base.enableZoneLODs(render)
        self.addDeckInterest()
        messenger.send('settingLocalShip', [True])
        self.unstashPlaneCollisions()
        self.setupControls()
        for avId in self.crew + self.boarders:
            av = self.cr.getDo(avId)
            if av:
                av.onShipWithLocalAv(True)

        self.gameFSM.initAudio()
        self.hideName()
        self.startDistanceChecks()
        messenger.send(self.uniqueName('localAvBoardedShip'))
        self.sendUpdate('shipBoarded')

    def handleChildLeave(self, child, zoneId):
        DistributedMovingObject.handleChildLeave(self, child, zoneId)
        child.handleLeftShip(self)

    @report(types=['args'], dConfigParam=['dteleport'])
    def battleAvatarLeft(self, av):
        pass

    @report(types=['args'], dConfigParam=['dteleport'])
    def battleNpcLeft(self, av):
        av.onShipWithLocalAv(False)

    @report(types=['args'], dConfigParam=['dteleport'])
    def playerPirateLeft(self, av):
        pass

    @report(types=['args'], dConfigParam=['dteleport'])
    def localPirateLeft(self, av):
        self.localAvPresent = False
        if not self.boardableShipId or self.isNpc:
            self.enableGridInterest(False)
        messenger.send('settingLocalShip', [False])
        base.disableZoneLODs()
        self.removeDeckInterest()
        if self.model:
            self.model.sinkingEnd()
        self.stopDistanceChecks()
        if av and self.isFlagship:
            av.b_clearTeleportFlag(PiratesGlobals.TFFlagshipBattle)
        for avId in self.crew + self.boarders:
            av = self.cr.getDo(avId)
            if av:
                av.onShipWithLocalAv(False)

        self.gameFSM.clearAudio()
        if self.gameFSM:
            self.gameFSM.stopCurrentMusic()
        if self.nametag and not base.cr.tutorial:
            self.showName()
        self.hideStatusDisplay()
        self.stashPlaneCollisions()
        if self.isGenerated() and self.cr.activeWorld and self.cr.activeWorld.getType() == PiratesGlobals.INSTANCE_PVP and ShipGlobals.INTERCEPTORL1 <= self.modelClass <= ShipGlobals.INTERCEPTORL4:
            self.findAllMatches('**/*collision_mast*').unstash()
        self.disableOnDeckInteractions()
        self.removeControls()

    def enterShipEvent(self, entry):
        eventObject = entry.getIntoNodePath()
        objType = eventObject.getNetTag('objType')
        if not objType:
            return
        objType = int(objType)
        if objType == PiratesGlobals.COLL_NEWSHIP and self.isRamming():
            targetId = eventObject.getNetPythonTag('ship').doId
            pos = entry.getSurfacePoint(self)
            self.composeRequestShipRam(targetId, pos)

    def exitShipEvent(self, entry):
        eventObject = entry.getIntoNodePath()
        objType = eventObject.getNetTag('objType')
        if not objType:
            return
        objType = int(objType)
        if objType == PiratesGlobals.COLL_NEWSHIP:
            pass

    def composeRequestShipRam(self, targetId, pos):
        target = self.cr.doId2do.get(targetId)
        if not target:
            return
        if not TeamUtils.damageAllowed(target, self):
            localAvatar.guiMgr.createWarning(PLocalizer.FriendlyFireWarning, PiratesGuiGlobals.TextFG6)
            return
        for buffKeyId in self.skillEffects.keys():
            buffId = self.skillEffects[buffKeyId][0]
            if WeaponGlobals.C_RAM == buffId:
                self.sendRequestShipRam(targetId, pos)
                deleteMe = []
                for buffKeyId in self.skillEffects:
                    buffId = self.skillEffects[buffKeyId][0]
                    attackerId = self.skillEffects[buffKeyId][3]
                    if buffId == WeaponGlobals.C_RAM:
                        deleteMe.append((buffKeyId, buffId, attackerId))

                for buffKeyId, buffId, attackerId in deleteMe:
                    del self.skillEffects[buffKeyId]
                    self.removeStatusEffect(buffId, attackerId)

                self.refreshStatusTray()

        self.addShipTarget(target, 2)
        if self.isInCrew(base.localAvatar.doId):
            cameraShakerEffect = CameraShaker()
            cameraShakerEffect.wrtReparentTo(self)
            cameraShakerEffect.setPos(self, 0, 0, 0)
            cameraShakerEffect.shakeSpeed = 0.08
            cameraShakerEffect.shakePower = 2.0
            cameraShakerEffect.numShakes = 4
            cameraShakerEffect.scalePower = 1
            cameraShakerEffect.play(500.0)

    def sendRequestShipRam(self, targetId, pos):
        timestamp32 = globalClockDelta.getFrameNetworkTime(bits=32)
        self.sendUpdate('requestShipRam', [targetId, [pos[0], pos[1], pos[2]], timestamp32])

    def useShipRam(self, pos):
        power = 1000
        if pos != [0, 0, 0]:
            pos = Vec3(pos[0], pos[1], pos[2])
            pos.setZ(0.0)
            distance = pos.length()
            dot = pos.dot(Vec3.right())
            if dot < 0.0:
                power = -power
        else:
            x, y, z, s = ShipGlobals.getRammingSphereScale(self.modelClass)
            pos = Vec3(x, y, z)
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            shipSplintersAEffect = ShipSplintersA.getEffect()
            if shipSplintersAEffect:
                shipSplintersAEffect.reparentTo(self)
                shipSplintersAEffect.setPos(self, pos)
                shipSplintersAEffect.play()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            smokeCloudEffect = SmokeCloud.getEffect()
            if smokeCloudEffect:
                smokeCloudEffect.wrtReparentTo(self)
                smokeCloudEffect.setPos(self, pos)
                smokeCloudEffect.setScale(3.0)
                smokeCloudEffect.spriteScale = 4.0
                smokeCloudEffect.radius = 10.0
                smokeCloudEffect.play()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            shockwaveRingEffect = ShockwaveHit.getEffect()
            if shockwaveRingEffect:
                shockwaveRingEffect.wrtReparentTo(self)
                shockwaveRingEffect.setPos(self, pos)
                shockwaveRingEffect.size = 200
                shockwaveRingEffect.play()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            if self.isInCrew(base.localAvatar.doId):
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.wrtReparentTo(self)
                cameraShakerEffect.setPos(self, pos)
                cameraShakerEffect.shakeSpeed = 0.08
                cameraShakerEffect.shakePower = 2.0
                cameraShakerEffect.numShakes = 4
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(500.0)
        self.setRockTarget(power)
        soundFx = random.choice(getRamSfx())
        base.playSfx(soundFx, node=self, cutoff=2500)

    def setupAggroCollisions(self):
        self.cAggro = CollisionSphere(0, 0, 0, self.getInstantAggroSphereSize())
        self.cAggro.setTangible(0)
        self.cAggroNode = CollisionNode(self.uniqueName('AggroSphere'))
        self.cAggroNode.setFromCollideMask(BitMask32.allOff())
        self.cAggroNode.setIntoCollideMask(PiratesGlobals.ShipCollideBitmask)
        self.cAggroNode.addSolid(self.cAggro)
        self.cAggroNodePath = self.attachNewNode(self.cAggroNode)
        if base.config.GetBool('show-aggro-radius', 0):
            self.cAggroNodePath.show()
        self.cHighAggro = CollisionSphere(0, 0, 0, self.getInstantAggroSphereSize())
        self.cHighAggro.setTangible(0)
        self.cHighAggroNode = CollisionNode(self.uniqueName('HighAggroSphere'))
        self.cHighAggroNode.setFromCollideMask(BitMask32.allOff())
        self.cHighAggroNode.setIntoCollideMask(PiratesGlobals.ShipCollideBitmask)
        self.cHighAggroNode.addSolid(self.cHighAggro)
        self.cHighAggroNodePath = self.attachNewNode(self.cHighAggroNode)
        enterCollEvent = self.uniqueName('enter' + 'AggroSphere')
        enterHighCollEvent = self.uniqueName('enter' + 'HighAggroSphere')
        self.accept(enterCollEvent, self._handleEnterAggroSphere)
        self.accept(enterHighCollEvent, self._handleEnterHighAggroSphere)
        self.accept('LocalAvatar_Ship_ThreatLevel_Update', self._handleThreatLevelChange)
        self.cHighAggroNodePath.stash()
        self.cAggroNodePath.unstash()
        if localAvatar.ship and localAvatar.ship.getThreatLevel() >= EnemyGlobals.SHIP_THREAT_CALL_FOR_HELP:
            self.cHighAggroNodePath.unstash()
            self.cAggroNodePath.stash()

    def cleanupAggroCollisions(self):
        if self.cAggroNodePath:
            base.cTrav.removeCollider(self.cAggroNodePath)
            self.cAggroNodePath.removeNode()
            self.cAggroNodePath = None
        if self.cAggroNode:
            self.cAggroNode = None
        if self.cAggro:
            self.cAggro = None
        if self.cHighAggroNodePath:
            base.cTrav.removeCollider(self.cHighAggroNodePath)
            self.cHighAggroNodePath.removeNode()
            self.cHighAggroNodePath = None
        if self.cHighAggroNode:
            self.cHighAggroNode = None
        if self.cHighAggro:
            self.cHighAggro = None
        return

    def _handleThreatLevelChange(self, threatLevel):
        if threatLevel >= EnemyGlobals.SHIP_THREAT_CALL_FOR_HELP:
            self.cHighAggroNodePath.unstash()
            self.cAggroNodePath.stash()
        else:
            self.cHighAggroNodePath.stash()
            self.cAggroNodePath.unstash()

    def _handleEnterHighAggroSphere(self, collEntry):
        self._handleEnterAggroSphere(collEntry)

    def _handleEnterAggroSphere(self, collEntry):
        otherCollNode = collEntry.getFromNodePath()
        myCollNode = collEntry.getIntoNodePath()
        if localAvatar.ship and localAvatar.ship.getThreatLevel() > EnemyGlobals.SHIP_THREAT_NONE or self.getTeam() in [PiratesGlobals.UNDEAD_TEAM, PiratesGlobals.FRENCH_UNDEAD_TEAM, PiratesGlobals.SPANISH_UNDEAD_TEAM, PiratesGlobals.VOODOO_ZOMBIE_TEAM]:
            self.sendRequestClientAggro()

    def getInstantAggroSphereSize(self):
        return EnemyGlobals.SHIP_INSTANT_AGGRO_RADIUS

    def getInstantHighAggroSphereSize(self):
        return EnemyGlobals.SHIP_INSTANT_HIGH_AGGRO_RADIUS

    def sendRequestClientAggro(self):
        self.sendUpdate('requestClientAggro', [])

    def getForwardVelocity(self):
        velocity = 0
        if hasattr(self, 'worldVelocity'):
            if self.isLocalCaptain():
                rotMat = Mat3.rotateMatNormaxis(self.getH(), Vec3.up())
                fwdVec = rotMat.xform(Vec3.forward())
                velocity = self.worldVelocity.dot(fwdVec)
            velocity += self.smoother.getSmoothForwardVelocity()
        return velocity

    def getRotationalVelocity(self):
        return self.currentTurning + self.smoother.getSmoothRotationalVelocity()

    def loadStats(self):
        if self.stats:
            return
        if not self.shipClass:
            return
        if self.getTeam() == PiratesGlobals.INVALID_TEAM:
            self.notify.warning('Tried to load ship stats without a team %s' % self)
            return
        self.stats = ShipGlobals.getShipConfig(self.shipClass)
        self.acceleration = self.stats['acceleration']
        self.maxSpeed = self.stats['maxSpeed']
        self.reverseAcceleration = self.stats['reverseAcceleration']
        self.maxReverseSpeed = self.stats['maxReverseSpeed']
        self.turnRate = self.stats['turn']
        self.maxTurn = self.stats['maxTurn']
        self.rammingPower = self.stats['rammingPower']
        self.baseAcceleration = self.acceleration
        self.acceleration *= self.baseSpeedMod
        self.baseMaxSpeed = self.maxSpeed
        self.maxSpeed *= self.baseSpeedMod
        self.baseReverseAcceleration = self.reverseAcceleration
        self.reverseAcceleration *= self.baseSpeedMod
        self.baseMaxReverseSpeed = self.maxReverseSpeed
        self.maxReverseSpeed *= self.baseSpeedMod
        self.baseTurnRate = self.turnRate
        self.turnRate *= self.baseSpeedMod
        self.baseMaxTurn = self.maxTurn
        self.maxTurn *= self.baseSpeedMod

    def autoFireCannons(self, side):
        if self.broadside:
            if self.broadside[1]:
                target = self.autoAimBroadside(side)
                self.broadside[1].fireBroadside(side, target)

    def playProjectileHitSfx(self, ammoSkillId, hitSail):
        if not hitSail:
            if localAvatar.ship == self:
                sfx = random.choice(self.woodBreakSfx)
                base.playSfx(sfx, node=self, cutoff=4000)
            else:
                sfx = random.choice(self.distantBreakSfx)
                base.playSfx(sfx, node=self, cutoff=6000)
        else:
            sfx = random.choice(self.sailTearSfx)
            base.playSfx(sfx, node=self, cutoff=2000)

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker, itemEffects=[]):
        if not codes:
            codes = (255, 255, 0)
        hullCode, mastCode, hitSail = codes
        self.playProjectileHitSfx(ammoSkillId, hitSail)
        if attacker:
            if hasattr(attacker, '_isShip') and attacker._isShip():
                attackShip = attacker
            elif attacker.getShip():
                attackShip = attacker.getShip()
            else:
                return
            if self.isInCrew(localAvatar.doId):
                localAvatar.addShipTarget(attackShip, 1)
                localAvatar.guiMgr.radarGui.flashRadarObjectTimed(attackShip.doId)
            elif attackShip.isInCrew(localAvatar.doId):
                localAvatar.addShipTarget(self, 2)
        if mastCode != 255:
            self.model.mastHit(mastCode)

    def damage(self, damage, pos, attackerId, itemEffects):
        if attackerId and localAvatar.doId == attackerId and damage != 0:
            self.showHpText(damage, pos=pos, itemEffects=itemEffects)
        offset = Vec3(*pos)
        offset.setZ(0.0)
        distance = offset.length()
        dot = offset.dot(Vec3.right())
        power = abs(damage) / 20.0
        if dot < 0.0:
            power = -power
        self.setRockTarget(power)

    def setRockTarget(self, power, timestamp=None):
        if timestamp == None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        self.addRoll(-power)
        return

    def addRoll(self, roll):
        self._rocker.addRoll(roll)

    def adjustArmorDisplay(self):
        rear, left, right = self.getArmorStates()
        if self.shipStatusDisplay:
            self.shipStatusDisplay.setArmorStatus(ShipGlobals.ARMOR_LEFT, 1 - left / 100.0)
            self.shipStatusDisplay.setArmorStatus(ShipGlobals.ARMOR_RIGHT, 1 - right / 100.0)
            self.shipStatusDisplay.setArmorStatus(ShipGlobals.ARMOR_REAR, 1 - rear / 100.0)
        if self.shipTargetPanel:
            self.shipTargetPanel.setArmorStatus(ShipGlobals.ARMOR_LEFT, 1 - left / 100.0)
            self.shipTargetPanel.setArmorStatus(ShipGlobals.ARMOR_RIGHT, 1 - right / 100.0)
            self.shipTargetPanel.setArmorStatus(ShipGlobals.ARMOR_REAR, 1 - rear / 100.0)
        if hasattr(base, 'localAvatar') and self.getCaptainId() == base.localAvatar.getDoId():
            if left <= 0.0:
                base.localAvatar.sendRequestContext(InventoryType.BrokenHull, 1)
            elif right <= 0.0:
                base.localAvatar.sendRequestContext(InventoryType.BrokenHull, 2)

    def checkAbleDropAnchor(self):
        if self.isLocalCaptain():
            if self.shipStatusDisplay:
                if localAvatar.getPort():
                    self.shipStatusDisplay.enableAnchorButton()
                else:
                    self.shipStatusDisplay.disableAnchorButton()
                    self.shipStatusDisplay.hideWrongPort()

    def requestDropAnchor(self):
        self.sendUpdate('dropAnchor', [localAvatar.getPort()])

    def setBoardableShipId(self, shipId):
        self.boardableShipId = shipId
        if shipId == 0:
            self.clearedFlagship()
        if self.isInCrew(localAvatar.getDoId()):
            self.notify.debug('ship %s is boardable' % shipId)

    def getBoardableShip(self):
        return self.cr.getDo(self.boardableShipId)

    def getNearestRopeAnchorNode(self, node):
        booms = []
        for mast, distMast in self.masts.values():
            booms.extend(mast.locators.findAllMatches('**/joint_anchor_net_*;+s'))

        booms = sorted([ (node.getDistance(boom), boom) for boom in booms ])
        dist, closest = booms[0]
        return closest

    def setBadge(self, titleId, rank):
        if titleId < 0 or rank < 0:
            self.badge = None
        else:
            self.badge = (
             titleId, rank)
        self.updateNametag()
        return

    def setName(self, name):
        if name == self.name:
            return
        self.name = name
        messenger.send('setName-%s' % self.getDoId(), [self.name, self.getTeam()])
        self.checkMakeNametag(self.isGenerated())

    def checkMakeNametag(self, generated):
        if not self.shipClass:
            return
        if not self.name:
            return
        if not generated:
            return
        if not self.nametag:
            self.createNametag(self.name)
            self.updateNametag()
            if self.initializeNametag3d():
                self.addActive()
            if base.hideShipNametags:
                self.hideNametag()
            else:
                self.showNametag()
            return

    def updateNametag(self):
        badgeText = ''
        threatText = ''
        if self.badge and (base.config.GetBool('want-land-infamy', 0) or base.config.GetBool('want-sea-infamy', 0)):
            badgeText = ' \x01white\x01\x05badge-%s-%s\x05\x02 ' % (self.badge[0], self.badge[1])
        if base.config.GetBool('want-ship-threat', 1) and not self.getSiegeTeam():
            if self.getThreatLevel():
                threatText = '\x01white\x01\x05threat-%s\x05\x02\n\n' % self.getThreatLevel()
            elif self.getHunterLevel():
                hunterName = HighSeasGlobals.HUNTER_LEVEL_NAME_DICT.get(self.getHunterLevel(), '')
                threatText = '\x01white\x01\x05hunterTAG\x05\x02 \x01red\x01%s\x02\n\n' % hunterName
        if self.nametag:
            self.nametag.setName(self.name + badgeText + threatText)
            self.nametag.setDisplayName('        ')
        if self.nametag3d:
            if self.nameText:
                self.nameText['text'] = threatText + badgeText + self.name
                if threatText:
                    self.nameText.setPos(0, 2)
                else:
                    self.nameText.setPos(0, 0)
            if self.classNameText:
                className = PLocalizer.ShipClassNames.get(self.modelClass)
                if self.getTeam() != PiratesGlobals.PLAYER_TEAM:
                    self.classNameText['text'] = PLocalizer.Lv + str(self.level) + ' ' + className
                else:
                    self.classNameText['text'] = className

    def getName(self):
        return self.name

    def getNameVisible(self):
        return self.__nameVisible

    def setNameVisible(self, bool):
        self.__nameVisible = bool
        if bool:
            self.showName()
        if not bool:
            self.hideName()

    def hideName(self):
        if not self.nametag:
            return
        self.nametag.getNametag3d().setContents(Nametag.CSpeech | Nametag.CThought)

    def showName(self):
        if not self.nametag:
            return
        if self.__nameVisible:
            self.nametag.getNametag3d().setContents(Nametag.CName | Nametag.CSpeech | Nametag.CThought)

    def updatePickable(self):
        if self.isInCrew(base.localAvatar.doId):
            self.setPickable(0)
        else:
            self.setPickable(1)

    def setPickable(self, flag):
        if self.nametag:
            self.nametag.setActive(flag)

    def clickedNametag(self):
        if localAvatar.chatMgr.active and base.config.GetBool('allow-doid-paste', 0):
            currTxt = localAvatar.chatMgr.whiteListEntry.get()
            currTxtLen = len(currTxt)
            if currTxtLen and currTxt[currTxtLen - 1] != ' ':
                separator = ' '
            else:
                separator = ''
            localAvatar.chatMgr.whiteListEntry.set(currTxt + separator + str(self.doId))
            localAvatar.chatMgr.whiteListEntry.setCursorPosition(len(localAvatar.chatMgr.whiteListEntry.get()))

    def initializeNametag3d(self):
        if not self.nametag:
            return 0
        self.deleteNametag3d()
        nametagNode = self.nametag.getNametag3d().upcastToPandaNode()
        self.nametag3d.attachNewNode(nametagNode)
        self.nametag3d.setLightOff()
        self.iconNodePath = self.nametag.getNameIcon()
        if self.iconNodePath.isEmpty():
            self.notify.warning('empty iconNodePath in initializeNametag3d')
            return 0
        if self.nameText:
            self.nameText.reparentTo(self.iconNodePath)
        if self.classNameText:
            self.classNameText.reparentTo(self.iconNodePath)
        if self.isFlagship:
            modelPath = EnemyGlobals.getFlagshipIconModelPath(self.getTeam())
            if modelPath:
                flagshipIcon = loader.loadModel(modelPath)
                flagshipIcon.setPos(0, 0, 2)
                flagshipIcon.setScale(1.5)
                flagshipIcon.reparentTo(self.iconNodePath)
                flagshipIcon.flattenLight()
        return 1

    def deleteNametag3d(self):
        if self.nametag3d:
            children = self.nametag3d.getChildren()
            for i in range(children.getNumPaths()):
                children[i].removeNode()

    def addActive(self):
        if base.wantNametags and self.nametag:
            self.nametag.manage(base.marginManager)
            self.accept(self.nametag.getUniqueId(), self.clickedNametag)

    def removeActive(self):
        if base.wantNametags and self.nametag:
            self.nametag.unmanage(base.marginManager)

    def createNametag(self, name):
        if self.shipClass == ShipGlobals.STUMPY_SHIP:
            return
        self.__nameVisible = 1
        self.nametag = NametagGroup()
        self.nametag.setAvatar(self)
        self.nametag.setFont(PiratesGlobals.getPirateBoldOutlineFont())
        self.nametag2dContents = Nametag.CName
        self.nametag2dDist = Nametag.CName
        self.nametag2dNormalContents = Nametag.CName
        self.nametag3d = self.attachNewNode('nametag3d')
        self.nametag3d.setTag('cam', 'nametag')
        self.nametag3d.setFogOff()
        self.nametag3d.setLightOff()
        self.setNametagScale(12)
        name = PLocalizer.Lv + str(self.level) + ' ' + name
        self.nametag.setName(name)
        self.nametag.setNameWordwrap(PiratesGlobals.NAMETAG_WORDWRAP)
        OTPRender.renderReflection(False, self.nametag3d, 'p_ship_nametag', None)
        posAndScale = self.getDebugNamePosScale()
        self.nametag3d.setPos(0, 0, posAndScale[0][2])
        self.updatePickable()
        if self.getSiegeTeam():
            color = PVPGlobals.getSiegeColor(self.getSiegeTeam())
        else:
            color = EnemyGlobals.getShipNametagColor(self.getTeam())
        self.nameText = OnscreenText(fg=color, bg=Vec4(0, 0, 0, 0), scale=0.95, align=TextNode.ACenter, mayChange=1, font=PiratesGlobals.getPirateBoldOutlineFont())
        self.nameText.setTransparency(TransparencyAttrib.MDual, 2)
        self.nameText.setColorScaleOff(100)
        self.nameText.setLightOff()
        self.nameText.setFogOff()
        self.classNameText = OnscreenText(pos=(0, -0.85), fg=Vec4(0.9, 0.9, 0.9, 1), bg=Vec4(0, 0, 0, 0), scale=0.6, align=TextNode.ACenter, mayChange=1, font=PiratesGlobals.getPirateBoldOutlineFont())
        self.classNameText.setTransparency(TransparencyAttrib.MDual, 2)
        self.classNameText.setColorScaleOff(100)
        self.classNameText.setLightOff()
        self.classNameText.setFogOff()
        return

    def removeNametag(self):
        if self.nametag:
            self.classNameText.removeNode()
            self.nameText.removeNode()
            self.nametag = None
            self.nametag3d.removeNode()
        return

    def getNametagScale(self):
        return self.nametagScale

    def setNametagScale(self, scale):
        self.nametagScale = scale
        if self.nametag3d:
            self.nametag3d.setScale(scale)

    def setPlayerType(self, playerType):
        self.playerType = playerType
        if self.nametag:
            self.nametag.setColorCode(self.playerType)

    def setShipClass(self, val):
        self.shipClass = val
        self.modelClass = ShipGlobals.getModelClass(val)
        self.setupLocalStats()
        self._tiltFakeMass = ShipGlobals.TiltFakeMass[self.modelClass]

    def getHp(self):
        return self.Hp

    def getMaxHp(self):
        return self.maxHp

    def setCargo(self, cargo):
        self.cargo = cargo
        messenger.send('setShipCargo-%s' % self.getDoId(), [self.cargo, self.maxCargo])

    def setMaxCargo(self, maxCargo):
        self.maxCargo = maxCargo

    def getMaxCargo(self):
        return self.maxCargo

    def setMaxCrew(self, val):
        self.maxCrew = val

    def getMaxCrew(self):
        return self.maxCrew

    def getSp(self):
        return self.Sp

    def getMaxSp(self):
        return self.maxSp

    def getNPCship(self):
        return False

    def notifyReceivedLoot(self, lootList):
        if self.getCrew().count(base.localAvatar.doId):
            if base.localAvatar.style.getTutorial() >= PiratesGlobals.TUT_MET_JOLLY_ROGER:
                base.localAvatar.guiMgr.messageStack.showLoot(lootList)

    def setSpeedMods(self, baseMod=None, speedUpgradeMod=None, turnUpgradeMod=None, sailMod=None):
        if baseMod != None:
            self.baseSpeedMod = baseMod
        if speedUpgradeMod != None:
            self.speedUpgrade = speedUpgradeMod
        if turnUpgradeMod != None:
            self.turnUpgrade = turnUpgradeMod
        if sailMod != None:
            self.sailMod = sailMod
        self.maxSpeed = self.baseMaxSpeed * self.baseSpeedMod * self.speedUpgrade * self.sailMod
        self.acceleration = self.baseAcceleration * self.baseSpeedMod * self.speedUpgrade * self.sailMod
        self.reverseAcceleration = self.baseReverseAcceleration * self.baseSpeedMod * self.speedUpgrade * self.sailMod
        self.maxReverseSpeed = self.baseMaxReverseSpeed * self.baseSpeedMod * self.speedUpgrade * self.sailMod
        self.turnRate = self.baseTurnRate * self.baseSpeedMod * self.turnUpgrade * self.sailMod
        self.maxTurn = self.baseMaxTurn * self.baseSpeedMod * self.turnUpgrade * self.sailMod
        return

    def setLockSails(self, val):
        self.lockedSails = val

    def stopSmooth(self):
        if self.smoothStarted:
            taskName = self.taskName('smooth')
            taskMgr.remove(taskName)
            self.smoothStarted = 0

    def getDebugNamePosScale(self):
        if self.modelClass in [ShipGlobals.INTERCEPTORL1, ShipGlobals.MERCHANTL1, ShipGlobals.WARSHIPL1, ShipGlobals.BRIGL1]:
            return [(0, 0, 150), 50.0]
        elif self.modelClass in [ShipGlobals.INTERCEPTORL2, ShipGlobals.MERCHANTL2, ShipGlobals.WARSHIPL2, ShipGlobals.BRIGL2, ShipGlobals.SKEL_INTERCEPTORL3, ShipGlobals.QUEEN_ANNES_REVENGE]:
            return [
             (0, 0, 250), 100.0]
        elif self.modelClass in [ShipGlobals.INTERCEPTORL3, ShipGlobals.MERCHANTL3, ShipGlobals.WARSHIPL3, ShipGlobals.BRIGL3, ShipGlobals.BLACK_PEARL, ShipGlobals.SKEL_WARSHIPL3]:
            return [(0, 0, 350), 125.0]
        elif self.modelClass == ShipGlobals.SHIP_OF_THE_LINE:
            return [(0, 0, 450), 2.0]
        elif self.modelClass == ShipGlobals.GOLIATH:
            return [(0, 0, 450), 2.0]
        else:
            return [
             (0, 0, 50), 2.0]

    def useShipSkill(self, skillId, ammoSkillId, skillResult, targetId, attackerEffects, targetEffects, timestamp, localSignal=0):
        effectId = WeaponGlobals.getSkillEffectFlag(skillId)
        newPriority = WeaponGlobals.getBuffPriority(effectId)
        newCategory = WeaponGlobals.getBuffCategory(effectId)
        if newPriority:
            for buffKeyId in self.skillEffects.keys():
                buffId = self.skillEffects[buffKeyId][0]
                priority = WeaponGlobals.getBuffPriority(buffId)
                category = WeaponGlobals.getBuffCategory(buffId)
                if newPriority < priority and category == newCategory:
                    return

        helmsman = self.cr.doId2do.get(self.steeringAvId)
        if helmsman:
            if helmsman.isNpc:
                return
            if not helmsman.isLocal() or localSignal:
                self.playSkillMovie(skillId, ammoSkillId)
            if helmsman.isLocal():
                if self.broadside:
                    if skillId == InventoryType.SailBroadsideRight:
                        self.autoFireCannons(ShipGlobals.BROADSIDE_RIGHT)
                    elif skillId == InventoryType.SailBroadsideLeft:
                        self.autoFireCannons(ShipGlobals.BROADSIDE_LEFT)

    def playSkillMovie(self, skillId, ammoSkillId):
        skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
        anim = skillInfo[WeaponGlobals.PLAYABLE_INDEX]
        helmsman = self.cr.doId2do.get(self.steeringAvId)
        if helmsman:
            if helmsman.isNpc:
                return
        self.curAttackAnim = getattr(self.cr.combatAnims, anim)(helmsman, skillId, ammoSkillId)
        if self.curAttackAnim:
            self.curAttackAnim.start()

    def setSkillEffects(self, buffs):
        for effectId, attackerId, timestamp, duration, timeLeft, recur, buffData in buffs:
            buffKeyId = '%s-%s' % (effectId, attackerId)
            if buffKeyId not in self.skillEffects.keys():
                self.skillEffects[buffKeyId] = [
                 effectId, attackerId, duration, timeLeft, timestamp, buffData[0]]
                self.addStatusEffect(effectId, attackerId, duration, timeLeft, timestamp, buffData[0])
            else:
                effect = self.skillEffects[buffKeyId]
                effect[3] = timeLeft
                effect[4] = timestamp

        killList = []
        for buffKeyId in self.skillEffects.keys():
            foundEntry = 0
            for entry in buffs:
                id = '%s-%s' % (entry[0], entry[1])
                if buffKeyId == id:
                    foundEntry = 1

            if not foundEntry:
                killList.append((buffKeyId, self.skillEffects[buffKeyId][0], self.skillEffects[buffKeyId][1]))

        for buffKeyId, effectId, attackerId in killList:
            del self.skillEffects[buffKeyId]
            self.removeStatusEffect(effectId, attackerId)

        self.refreshStatusTray()

    def getSkillEffects(self):
        buffIds = []
        for buffKeyId in self.skillEffects.keys():
            buffId = self.skillEffects[buffKeyId][0]
            if buffId not in buffIds:
                buffIds.append(buffId)

        return buffIds

    def addStatusEffect(self, effectId, attackerId, duration=0, timeLeft=0, timestamp=0, buffData=[0]):
        if effectId == WeaponGlobals.C_FULLSAIL:
            if self.isLocalCaptain():
                if self.queryGameState() != 'Docked':
                    if self.autoSailing:
                        pass
                    else:
                        self.startAutoSailing()
            if self.fullsailSfx:
                base.playSfx(self.fullsailSfx, node=self, cutoff=2000)
            if self.model:
                self.model.playFullSailEffect()
        elif effectId == WeaponGlobals.C_COMEABOUT:
            if self.model:
                self.model.playComeAboutEffect()
        elif effectId == WeaponGlobals.C_RAM:
            if self.isLocalCaptain():
                self.rammingOn()
                if self.queryGameState() != 'Docked':
                    if self.autoSailing:
                        pass
                    else:
                        self.startAutoSailing()
            if self.rammingSfx:
                base.playSfx(self.rammingSfx, node=self, cutoff=2000)
            if self.model:
                self.model.playRamEffect()
        elif effectId == WeaponGlobals.C_RECHARGE:
            if self.isInCrew(localAvatar.doId):
                localAvatar.guiMgr.combatTray.skillTray.addPowerRechargeEffect()
                if localAvatar.cannon:
                    localAvatar.cannon.updateReloadBar()
            if self.model:
                self.model.playRechargeEffect()
        elif effectId == WeaponGlobals.C_SPAWN:
            if self.model:
                self.model.playSpawnEffect()
        elif effectId == WeaponGlobals.C_TAKECOVER:
            if self.model:
                self.model.playTakeCoverEffect()
        elif effectId == WeaponGlobals.C_OPENFIRE:
            if self.model:
                self.model.playOpenFireEffect()
        self.calcModifiedStats()

    def removeStatusEffect(self, effectId, attackerId):
        if self.findAllBuffCopyKeys(effectId):
            return
        if effectId == WeaponGlobals.C_RAM:
            if self.model:
                self.model.stopRamEffect()
            if self.isLocalCaptain():
                self.rammingOff()
        else:
            if effectId == WeaponGlobals.C_RECHARGE:
                if self.isInCrew(localAvatar.doId):
                    localAvatar.guiMgr.combatTray.skillTray.removePowerRechargeEffect()
                    if localAvatar.cannon:
                        localAvatar.cannon.updateReloadBar()
                if self.model:
                    self.model.stopRechargeEffect()
            elif effectId == WeaponGlobals.C_SPAWN:
                if self.model:
                    self.model.stopSpawnEffect()
            elif effectId == WeaponGlobals.C_TAKECOVER:
                if self.model:
                    self.model.stopTakeCoverEffect()
            elif effectId == WeaponGlobals.C_OPENFIRE:
                if self.model:
                    self.model.stopOpenFireEffect()
            slowDown = True
            for buffKeyId in self.skillEffects.keys():
                buffId = self.skillEffects[buffKeyId][0]
                if WeaponGlobals.C_FULLSAIL == buffId or WeaponGlobals.C_RAM == buffId:
                    slowDown = False

        self.calcModifiedStats()

    def findAllBuffCopyKeys(self, effectId):
        buffCopies = []
        for buffKeyId in self.skillEffects.keys():
            if self.skillEffects[buffKeyId][0] == effectId:
                buffCopies.append(buffKeyId)

        return buffCopies

    def startAutoSailing(self):
        if self.enableAutoSail:
            return
        if not self.sailsReady:
            return
        self.enableAutoSail = 1
        self.setIsAutoSailing(1)
        self.accept('arrow_down', self.stopAutoSailing)
        self.accept('s', self.stopAutoSailing)
        self.sailsReady = 0
        taskMgr.remove(self.getReadySailsTaskName())
        taskMgr.doMethodLater(self.SAIL_READY_DELAY, self.__readySails, self.getReadySailsTaskName())

    def stopAutoSailing(self):
        if not self.enableAutoSail:
            return
        if not self.sailsReady:
            return
        for buffId in self.getSkillEffects():
            if WeaponGlobals.C_RAM == buffId:
                return

        self.enableAutoSail = 0
        self.setIsAutoSailing(0)
        self.ignore('arrow_down')
        self.ignore('s')
        self.sailsReady = 0
        taskMgr.remove(self.getReadySailsTaskName())
        taskMgr.doMethodLater(self.SAIL_READY_DELAY, self.__readySails, self.getReadySailsTaskName())

    def setIsAutoSailing(self, value):
        if self.lockedSails:
            return
        self.autoSailing = value
        if value:
            self.sailsDown = True
            self.l_rolldownSails()
            self.sendUpdate('setSailsDown', [True])
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                localAvatar.enableCloudScudEffect()
        else:
            self.sailsDown = False
            self.l_rollupSails()
            self.sendUpdate('setSailsDown', [False])
            localAvatar.disableCloudScudEffect()

    def getIsAutoSailing(self):
        return self.autoSailing

    def l_rolldownSails(self):
        if self.model:
            self.model.startSailing()

    def l_rollupSails(self):
        if self.model:
            self.model.stopSailing()

    def setSailsDown(self, down):
        if down:
            self.sailsDown = True
            self.l_rolldownSails()
        else:
            self.sailsDown = False
            self.l_rollupSails()

    def refreshStatusTray(self):
        if self.shipStatusDisplay:
            self.shipStatusDisplay.updateStatusEffects(self.skillEffects)

    def calcModifiedStats(self):
        self.stats = None
        self.loadStats()
        passiveSkills = []
        for skillId in range(InventoryType.begin_SkillSailing, InventoryType.end_SkillSailing):
            if WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.PASSIVE_SKILL_INDEX:
                passiveSkills.append(skillId)

        spPercent = max(1, self.Sp) / float(max(1, self.maxSp))
        sailModifier = spPercent * 0.25 + 0.75
        self.setSpeedMods(sailMod=sailModifier)
        self.speednerf = sailModifier
        helmsman = self.cr.doId2do.get(self.steeringAvId)
        if helmsman:
            if not helmsman.isNpc:
                inventory = helmsman.getInventory()
                if inventory:
                    for skillId in passiveSkills:
                        self.addPassiveSkill(skillId, inventory)

        for buffKeyId in self.skillEffects:
            buffId = self.skillEffects[buffKeyId][0]
            if WeaponGlobals.C_RAM == buffId:
                self.acceleration += ShipGlobals.defaultAcceleration * 1.0
                self.maxSpeed += ShipGlobals.defaultMaxSpeed * 1.0
                self.turnRate = 0.0
                self.maxTurn = 0.0
            elif WeaponGlobals.C_COMEABOUT == buffId:
                self.turnRate += ShipGlobals.defaultTurn * 0.35
                self.maxTurn += ShipGlobals.defaultMaxTurn * 0.35
            elif WeaponGlobals.C_FULLSAIL == buffId:
                self.acceleration += ShipGlobals.defaultAcceleration * 0.5
                self.maxSpeed += ShipGlobals.defaultMaxSpeed * 0.5

        return

    def addPassiveSkill(self, skillId, inventory):
        skillLvl = max(0, inventory.getStackQuantity(skillId) - 1)
        effects = WeaponGlobals.getShipEffects(skillId)
        if effects != [0, 0, 0, 0, 0, 0]:
            self.acceleration += self.baseAcceleration * effects[0] * skillLvl
            self.maxSpeed += self.baseMaxSpeed * effects[1] * skillLvl
            self.reverseAcceleration += self.baseReverseAcceleration * effects[2] * skillLvl
            self.maxReverseSpeed += self.baseMaxReverseSpeed * effects[3] * skillLvl
            self.turnRate += self.baseTurnRate * effects[4] * skillLvl
            self.maxTurn += self.baseMaxTurn * effects[5] * skillLvl

    def setupControls(self):
        if not self.controlManager:
            self.controlManager = ControlManager.ControlManager(enable=False)
            controls = ShipPilot.ShipPilot()
            modelRoot = self.getModelRoot()
            bow, port, starboard, stern = self.model.getPartNodes()
            controls.initializeCollisions(base.cTrav, modelRoot, bow, stern, starboard, port)
            wallBitMask = PiratesGlobals.ShipCollideBitmask | PiratesGlobals.GoldBitmask
            if self.respectDeployBarriers:
                wallBitMask |= PiratesGlobals.ShipDeployBitmask
            controls.setWallBitMask(wallBitMask)
            controls.setFloorBitMask(BitMask32().allOff())
            self.controlManager.add(controls, 'ship')

    def removeControls(self):
        if self.controlManager:
            self.controlManager.delete()
            self.controlManager = None
        return

    def getReadySailsTaskName(self):
        return 'readySails-%s' % self.doId

    def __readySails(self, args=None):
        self.sailsReady = 1

    def generateBroadsidePoints(self):
        for side in self.broadside[0]:
            minY = 1000
            maxY = -1000
            avgX = 0
            avgZ = 0
            bCount = 0
            for port in side:
                if port:
                    bCount += 1
                    pos = port.locator.getPos(self)
                    if minY > pos[1]:
                        minY = pos[1]
                    if maxY < pos[1]:
                        maxY = pos[1]
                    avgX += pos[0]
                    avgZ += pos[2]

            avgX /= float(bCount)
            avgZ /= float(bCount)
            self.broadsidePoints.append([Vec3(avgX, minY, avgZ), Vec3(avgX, maxY, avgZ)])

    def autoAimBroadside(self, side):
        targetList = []
        for shipId in self.NearbyShips:
            ship = self.cr.getDo(shipId)
            if ship and ship is not self and ship.getHp() > 0 and TeamUtils.damageAllowed(ship, self):
                dist = self.checkBroadsideAlignment(ship, side)
                if dist:
                    targetList.append((dist, shipId))

        if targetList:
            targetList.sort()
            return targetList[0][1]
        return 0

    def visualizeBroadsides(self):
        cm = CardMaker('cm')
        cm.setFrame(-0.001, 0.001, 0, 1)
        a1 = self.attachNewNode('a')
        if self.fullBroadsides:
            a1.setPos(self.broadsidePoints[0][1])
        else:
            a1.setPos(0, 0, 0)
        a = NodePath(cm.generate())
        a.reparentTo(a1)
        a.setScale(2000)
        a.setP(-90)
        a1.setH(65)
        a1.setZ(5)
        self.a1 = a1
        b1 = self.attachNewNode('b')
        if self.fullBroadsides:
            b1.setPos(self.broadsidePoints[0][0])
        else:
            b1.setPos(0, 0, 0)
        b = NodePath(cm.generate())
        b.reparentTo(b1)
        b.setScale(2000)
        b.setP(-90)
        b1.setH(115)
        b1.setZ(5)
        self.b1 = b1
        c1 = self.attachNewNode('c')
        if self.fullBroadsides:
            c1.setPos(self.broadsidePoints[1][1])
        else:
            c1.setPos(0, 0, 0)
        c = NodePath(cm.generate())
        c.reparentTo(c1)
        c.setScale(2000)
        c.setP(-90)
        c1.setH(-65)
        c1.setZ(5)
        self.c1 = c1
        d1 = self.attachNewNode('d')
        if self.fullBroadsides:
            d1.setPos(self.broadsidePoints[1][0])
        else:
            d1.setPos(0, 0, 0)
        d = NodePath(cm.generate())
        d.reparentTo(d1)
        d.setScale(2000)
        d.setP(-90)
        d1.setH(-115)
        d1.setZ(5)
        self.d1 = d1

    def checkBroadsideAlignment(self, target, side):
        if self.lookAtDummy == None:
            return 0
        if not target:
            return 0
        withinLeft = False
        withinRight = False
        if not self.broadsidePoints:
            self.generateBroadsidePoints()
        distToTgt = self.getDistance(target)
        if distToTgt > ShipGlobals.BROADSIDE_MAX_AUTOAIM_DIST:
            return 0
        self.lookAtDummy.setPos(0, 0, 0)
        bow, port, starboard, stern = target.model.getPartNodes()
        if bow and stern:
            if side == ShipGlobals.BROADSIDE_LEFT:
                minHeading = 65
                maxHeading = 115
                if self.fullBroadsides:
                    points = self.broadsidePoints[0]
                    self.lookAtDummy.setPos(points[1])
                    self.lookAtDummy.lookAt(bow)
                    targetHeading = self.lookAtDummy.getH()
                    if targetHeading > minHeading:
                        withinLeft = True
                    self.lookAtDummy.lookAt(stern)
                    targetHeading = self.lookAtDummy.getH()
                    if targetHeading > minHeading:
                        withinLeft = True
                    self.lookAtDummy.setPos(points[0])
                    self.lookAtDummy.lookAt(bow)
                    targetHeading = self.lookAtDummy.getH()
                    if targetHeading < maxHeading:
                        withinRight = True
                    self.lookAtDummy.lookAt(stern)
                    targetHeading = self.lookAtDummy.getH()
                    if targetHeading < maxHeading:
                        withinRight = True
                else:
                    self.lookAtDummy.lookAt(bow)
                    targetHeading = self.lookAtDummy.getH(self.getModelRoot())
                    if targetHeading > minHeading:
                        withinLeft = True
                    if targetHeading < maxHeading:
                        withinRight = True
                    self.lookAtDummy.lookAt(stern)
                    targetHeading = self.lookAtDummy.getH(self.getModelRoot())
                    if targetHeading > minHeading:
                        withLeft = True
                    if targetHeading < maxHeading:
                        withinRight = True
            elif side == ShipGlobals.BROADSIDE_RIGHT:
                minHeading = -115
                maxHeading = -65
                if self.fullBroadsides:
                    points = self.broadsidePoints[1]
                    self.lookAtDummy.setPos(points[0])
                    self.lookAtDummy.lookAt(bow)
                    targetHeading = self.lookAtDummy.getH()
                    if targetHeading > minHeading:
                        withinLeft = True
                        self.lookAtDummy.lookAt(stern)
                        targetHeading = self.lookAtDummy.getH()
                        if targetHeading > minHeading:
                            withinLeft = True
                        self.lookAtDummy.setPos(points[1])
                        self.lookAtDummy.lookAt(bow)
                        targetHeading = self.lookAtDummy.getH()
                        if targetHeading < maxHeading:
                            withinRight = True
                        self.lookAtDummy.lookAt(stern)
                        targetHeading = self.lookAtDummy.getH()
                        if targetHeading < maxHeading:
                            withinRight = True
                else:
                    self.lookAtDummy.lookAt(bow)
                    targetHeading = self.lookAtDummy.getH(self.getModelRoot())
                    if targetHeading > minHeading:
                        withinLeft = True
                    if targetHeading < maxHeading:
                        withinRight = True
                    self.lookAtDummy.lookAt(stern)
                    targetHeading = self.lookAtDummy.getH(self.getModelRoot())
                    if targetHeading > minHeading:
                        withLeft = True
                    if targetHeading < maxHeading:
                        withinRight = True
            else:
                self.notify.error('bad broadside setup')
            if withinRight and withinLeft:
                return distToTgt
        else:
            self.lookAtDummy.lookAt(target)
            targetHeading = self.lookAtDummy.getH(self.getModelRoot())
            if targetHeading > 65 and targetHeading < 115 and side == ShipGlobals.BROADSIDE_LEFT:
                return distToTgt
            elif targetHeading < -65 and targetHeading > -115 and side == ShipGlobals.BROADSIDE_RIGHT:
                return distToTgt
        return 0

    def setRepairCount(self, val):
        self.repairCount = val

    def getRepairCount(self):
        return self.repairCount

    def setCaptainId(self, val):
        self.captainId = val

    def getCaptainId(self):
        return self.captainId

    def isCaptain(self, avId):
        return avId == self.captainId

    @report(types=['args'], dConfigParam=['dteleport'])
    def getRandomBoardingSpot(self):
        count = len(self.findLocators('**/boarding_spot_*;+s'))
        return random.randint(0, count - 1)

    @report(types=['args'], dConfigParam=['dteleport'])
    def getBoardingLocator(self, spotIndex):
        return self.findLocator('**/boarding_spot_%s;+s' % spotIndex)

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='shipboard')
    def getRandomBoardingPosH(self):
        allBoardingSpots = self.findLocators('**/boarding_spot_*;+s')
        if not allBoardingSpots:
            return None
        boardingSpot = random.choice(allBoardingSpots)
        pos = boardingSpot.getPos()
        h = boardingSpot.getH()
        return (
         pos[0], pos[1], pos[2], h)

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='shipboard')
    def getClosestBoardingPos(self):
        allBoardingSpots = self.findLocators('**/boarding_spot_*;+s')
        if not allBoardingSpots:
            return None
        closestBoardingSpot = allBoardingSpots[0]
        for locator in allBoardingSpots:
            dist = locator.getDistance(base.localAvatar)
            currentClosestDist = closestBoardingSpot.getDistance(base.localAvatar)
            if dist < currentClosestDist:
                closestBoardingSpot = locator

        return closestBoardingSpot.getPos() + Vec3(0.13, -0.16, 0)

    @report(types=['frameCount', 'deltaStamp'], dConfigParam='shipboard')
    def getClosestBoardingPosH(self):
        if not self.isGenerated():
            self.notify.error('getClosestBoardingPosH: not generated')
        allBoardingSpots = self.findLocators('**/boarding_spot_*;+s')
        if not allBoardingSpots:
            return (Vec3(0, 0, 0), 0)
        closestBoardingSpot = allBoardingSpots[0]
        for locator in allBoardingSpots:
            dist = locator.getDistance(base.localAvatar)
            currentClosestDist = closestBoardingSpot.getDistance(base.localAvatar)
            if dist < currentClosestDist:
                closestBoardingSpot = locator

        return (
         closestBoardingSpot.getPos() + Vec3(0, 0, 6), closestBoardingSpot.getH() + 180)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam=['shipdeploy', 'shipboard'])
    def setRespectDeployBarriers(self, respect, barrierId):
        self.respectDeployBarriers = respect
        if not self.controlManager:
            return
        controls = self.controlManager.get('ship')
        if controls:
            if respect:
                controls.adjustWallBitMask(BitMask32.allOff(), PiratesGlobals.ShipDeployBitmask)
            else:
                controls.adjustWallBitMask(PiratesGlobals.ShipDeployBitmask, BitMask32.allOff())

    def getRespectDeployBarriers(self):
        return self.respectDeployBarriers

    def placeAvatarAtWheel(self, av):
        modelRoot = self.getModelRoot()
        if modelRoot:
            wheelpost = self.getLocator('**/location_wheel')
            av.setPos(wheelpost.getPos(modelRoot) - Vec3(0.0, 2.0, 0))
            av.setHpr(0, 0, 0)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='shipboard')
    def setClientController(self, avId):
        self.clientController = avId
        if avId != 0 and avId == localAvatar.doId:
            self.setupControls()
            shipControls = self.controlManager.get('ship')
            shipControls.setShip(self)
            self.controlManager.setTag('avId', str(avId))
            self.controlManager.setTag('shipId', str(self.getDoId()))
            self.forceToTruePosition()
            self.stopSmooth()
            self.startPosHprBroadcast()
            grid = self.getParentObj()
            grid.manageChild(self)
        else:
            grid = self.getParentObj()
            grid.ignoreChild(self)
            self.stopPosHprBroadcast()
            if self.controlManager:
                shipControls = self.controlManager.get('ship')
                shipControls.setShip(None)
            self.startSmooth()
        return

    def getShipInfo(self):
        return [
         self.doId, self.getName(), self.shipClass, ShipGlobals.getMastSetup(self.shipClass)]

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='shipboard')
    def confirmSameCrewTeleport(self, toFrom, incomingAvId=0, bandMgrId=0, bandId=0, guildId=0):
        if toFrom == 'from':
            return True
        else:
            if not self.isGenerated():
                self.notify.warning('confirmSameCrewTeleport(%s)' % localAvatar.getShipString())
                return False
            return False

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='shipboard')
    def confirmOnShipTeleport(self, toFrom, incomingAvId=0, bandMgrId=0, bandId=0, guildId=0):
        if toFrom == 'from':
            if self.getSiegeTeam() and localAvatar.avId == self.ownerId:
                return False
            else:
                return True
        else:
            return self.hasSpace(incomingAvId, bandMgrId, bandId, guildId)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='shipboard')
    def confirmSiegeCaptainTeleport(self, toFrom, incomingAvId=0, bandMgrId=0, bandId=0, guildId=0):
        if toFrom == 'from':
            return not self.getSiegeTeam() or localAvatar.doId != self.ownerId
        else:
            return True

    def hasSpace(self, avId=0, bandMgrId=0, bandId=0, guildId=0):
        return False

    def hideNametag(self):
        if self.nametag3d:
            self.nametag3d.stash()

    def showNametag(self):
        if self.nametag3d:
            self.nametag3d.unstash()

    def setBandId(self, bandManagerId, bandId):
        self.bandId = (bandManagerId, bandId)

    def getBandId(self):
        return self.bandId

    def resetMiniLog(self, name=None):
        self.miniLog = name and MiniLog(name)

    def requestShipSkill(self, skillId, ammoSkillId):
        self.sendUpdate('requestSkillEvent', [skillId, ammoSkillId])

    def recordSkillEvent(self, skillId, ammoSkillId):
        if self.isInCrew(localAvatar.doId):
            localAvatar.skillDiary.startRecharging(skillId, ammoSkillId)
            localAvatar.guiMgr.combatTray.skillTray.updateSkillIval(skillId)

    def setupKrakenLocators(self):
        if not self.krakenLocators and self.kraken:
            self.findAllMatches('**/kraken-*').detach()
            self.waterlineNode = self.model.modelRoot.attachNewNode('waterline-node')
            self.waterlineNode.setPos(0, 0, ShipGlobals.WaterlineOffsets[self.modelClass])
            locatorInfo = ShipGlobals.KrakenLocators.get(self.modelClass)
            for x, (pos, scale, rPos, rScale) in enumerate(locatorInfo):
                pos.setX(pos[0] + 30)
                locator = self.attachNewNode('kraken-%s' % (x,))
                locator.setPosHprScale(pos, VBase3(-90, 0, 0), VBase3(scale))
                locator.wrtReparentTo(self.waterlineNode)
                rangeParent = locator.attachNewNode('rangeParent')
                rangeParent.setPos(rPos)
                rangeParent.setScale(VBase3(rScale, rScale, 1))
                self.krakenLocators.insert(x, locator)
                x += len(locatorInfo)
                pos.setX(-pos[0])
                rPos.setX(-rPos[0])
                locator = self.attachNewNode('kraken-%s' % (x,))
                locator.setPosHprScale(pos, VBase3(90, 0, 0), VBase3(scale))
                locator.wrtReparentTo(self.waterlineNode)
                rangeParent = locator.attachNewNode('rangeParent')
                rangeParent.setPos(rPos)
                rangeParent.setScale(VBase3(rScale, rScale, 1))
                self.krakenLocators.append(locator)

    def getKrakenGrabberLocator(self, locatorId):
        self.setupKrakenLocators()
        return self.krakenLocators[locatorId]

    def getKrakenHolderLocator(self, locatorId):
        return self.model.locators.find('**/holder_%s' % locatorId)

    def getKrakenRangeParent(self, locatorId):
        locator = self.getKrakenGrabberLocator(locatorId)
        return locator

    def setKraken(self, kraken):
        self.kraken = kraken

    def addShipTarget(self, ship, priority=0):
        if self.getBuildComplete() and ship.getBuildComplete():
            self.targets.add(ship.getTarget(), priority)

    def getTarget(self):
        if not self.target:
            self.target = Target(self)
        return self.target

    def getTargetPanel(self):
        if not self.shipTargetPanel:
            self.loadShipTargetPanel()
        return self.shipTargetPanel

    def isLocalCaptain(self):
        return self.steeringAvId == localAvatar.doId

    def setupSmoothing(self):
        self.activateSmoothing(1, 0)
        self.smoother.setDelay(OTPGlobals.NetworkLatency * 1.5)
        broadcastPeriod = 0.3
        self.smoother.setMaxPositionAge(broadcastPeriod * 1.25 * 10)
        self.smoother.setExpectedBroadcastPeriod(broadcastPeriod)
        self.smoother.setDefaultToStandingStill(False)

    def getLocator(self, locatorName):
        if self.model:
            return self.model.locators.find('**/%s;+s' % locatorName)
        else:
            return NodePath()

    def getLocatorTransform(self, locatorName):
        if self.model:
            return self.getLocator(locatorName).getTransform(self.getModelRoot())
        else:
            return None
        return None

    def getModelCollisionRoot(self):
        if self.model:
            return self.model.modelCollisions
        else:
            return NodePath()

    def getLowDetail(self):
        if self.model:
            return self.model.modelRoot
        else:
            return NodePath()

    def getMediumDetail(self):
        if self.model:
            return self.model.modelRoot
        else:
            return NodePath()

    def getHighDetail(self):
        if self.model:
            return self.model.modelRoot
        else:
            return NodePath()

    def setWheelInUse(self, wheelInUse):
        pass

    def storeCamParams(self, shipCamParams):
        self._shipCamParams = shipCamParams

    def retrieveCamParams(self):
        return self._shipCamParams

    def setGuildId(self, guildId):
        self.guildId = guildId

    def getGuildId(self):
        return self.guildId

    def engagedFlagship(self):
        if self.isInCrew(localAvatar.doId):
            localAvatar.b_setTeleportFlag(PiratesGlobals.TFFlagshipBattle)

    def clearedFlagship(self):
        if self.isInCrew(localAvatar.doId) or self.isInBoarders(localAvatar.doId):
            localAvatar.b_clearTeleportFlag(PiratesGlobals.TFFlagshipBattle)

    def _isShip(self):
        return True

    def getMinimap(self):
        ocean = self.getParentObj()
        return ocean.getMinimap()

    def getMinimapObject(self):
        if not self.minimapObj and not self.isDisabled():
            self.minimapObj = MinimapShip(self)
        return self.minimapObj

    def destroyMinimapObject(self):
        if self.minimapObj:
            self.minimapObj.removeFromMap()
            self.minimapObj = None
        return

    def setOwnerId(self, doId):
        self.ownerId = doId

    def getOwnerId(self):
        return self.ownerId

    def rollupSails(self):
        if self.model:
            self.model.stopSailing()

    def getInteractCollisionRoot(self):
        if self.model:
            return self.model.modelCollisions
        else:
            return NodePath()

    def getWallCollisions(self):
        if self.model:
            return self.model.shipCollWall
        else:
            return NodePath()

    def hideMasts(self):
        self.model.hideMasts()

    def showMasts(self):
        self.model.showMasts()

    def recoverFromSunk(self):
        self.getParentObj().minimap.addObject(self.minimapObj)
        if self.isStatusDisplayVisible > 0:
            self.loadShipStatusDisplay()
            self.__checkStatusDisplayVisible()
        self.target = Target(self)
        self._undoSinking()
        self.createWake()
        if self.kraken and self.kraken.doomTentacle:
            self.kraken.doomTentacle.detachNode()
            self.kraken.doomTentacle = None
        if self.isInCrew(localAvatar.doId):
            base.localAvatar.b_setGameState('LandRoam')
            base.transitions.fadeIn()
            base.cr.loadingScreen.hide()
        self.enableOnDeckInteractions()
        return

    def _undoSinking(self):
        if self.model:
            self.model.undoSinking()
        self.showNametag()
        self.classNameText.setColorScale(Vec4(1, 1, 1, 1))
        self.nameText.setColorScale(Vec4(1, 1, 1, 1))

    def enableFloors(self):
        pass

    def ignoreFloors(self):
        pass

    def stashPlaneCollisions(self):
        if self.model:
            self.model.stashPlaneCollisions()

    def unstashPlaneCollisions(self):
        if self.model:
            self.model.unstashPlaneCollisions()

    def enableWheelInteraction(self):
        if self.wheel:
            if self.wheel[1]:
                self.wheel[1].setAllowInteract(1)
                self.wheel[1].checkInUse()

    def disableWheelInteraction(self):
        if self.wheel:
            if self.wheel[1]:
                self.wheel[1].setAllowInteract(0, forceOff=True)
                self.wheel[1].refreshState()

    def getWake(self):
        if self.model:
            return self.model.wake
        else:
            return NodePath()

    def playTextEffect(self, message):
        if self.shoutTextEffect:
            self.shoutTextEffect.finish()
            self.shoutTextEffect = None
        self.HpTextGenerator.setFont(PiratesGlobals.getPirateOutlineFont())
        duration = 4.0
        self.HpTextGenerator.setText(message)
        self.HpTextGenerator.clearShadow()
        self.HpTextGenerator.setAlign(TextNode.ACenter)
        color = Vec4(1, 1, 0, 1)
        hpTextDummy = self.attachNewNode('hpTextDummy')
        self.HpTextGenerator.setTextColor(color)
        textNode = self.HpTextGenerator.generate()
        hpText = hpTextDummy.attachNewNode(textNode)
        hpText.setScale(1.0)
        hpText.setBillboardPointEye(3.0)
        hpText.setBin('fixed', 100)
        hpText.setDepthWrite(0)
        hpText.setFogOff()
        hpText.setLightOff()
        hpText.setPos(0, 0, 2.0)
        OTPRender.renderReflection(False, hpText, 'p_text_effect', None)
        height = self.model.dimensions[2] * 1.27
        hpTextDummy.setPos(self, 0, 0, height)
        hpTextDummy.headsUp(base.camera)
        hpTextDummy.setH(hpTextDummy.getH() + 180)
        tgtColor = Vec4(color[0], color[1], color[2], 0)
        scaleUp = hpTextDummy.scaleInterval(duration * 0.003, self.model.dimensions[1] / 10.0)
        fadeIn = hpTextDummy.colorScaleInterval(0.0, color, startColorScale=tgtColor)
        noFade = hpTextDummy.colorScaleInterval(0.5, color, startColorScale=color)
        fadeOut = hpTextDummy.colorScaleInterval(2.0, tgtColor, startColorScale=Vec4(color))
        trackParallel = Parallel(scaleUp, Sequence(fadeIn, noFade, fadeOut))
        self.shoutTextEffect = Sequence(trackParallel, Func(self.cleanupTextEffect, hpTextDummy))
        self.shoutTextEffect.start()
        return

    def cleanupTextEffect(self, hpTextDummy):
        if hpTextDummy:
            hpTextDummy.hide()
            hpTextDummy.removeNode()

    def setupLocalStats(self):
        shipStats = ShipGlobals.getShipConfig(self.shipClass)
        self.maxHp = shipStats['hp'] * self.hpModifier
        self.maxSp = shipStats['sp']
        self.maxMastHealth = ShipGlobals.getMastHealth(self.shipClass, self.maxSp)
        self.maxArmor = ShipGlobals.getHullArmor(self.modelClass)
        self.setMaxCargo(shipStats['maxCargo'])
        self.setMaxCrew(shipStats['maxCrew'])

    def setCannons(self, cannons, broadsideId):
        self.cannonIds = cannons
        self.broadsideId = broadsideId
        if cannons or broadsideId:
            self.pendingCannons = self.cr.relatedObjectMgr.requestObjects(self.cannonIds + [self.broadsideId], allCallback=self.cannonsArrived)

    def cannonsArrived(self, cannonList):
        self.pendingCannons = None
        self.mybroadside = cannonList[-1]
        self.mycannons = cannonList[:-1]
        self.model.setupCannons(self.cannons, self.broadside, base.options.terrain_detail_level)
        return

    def isInInvasion(self):
        return False

    def getArmorScale(self):
        return 1.0

    def updateShipEffects(self):
        if self.model:
            self.model.updateDamageEffects(self.healthState, self.armorStates[0], self.armorStates[1], self.armorStates[2])

    def cleanUpShipEffects(self):
        for currTextEffect in self.textEffects:
            if currTextEffect:
                currTextEffect.finish()

        self.textEffects = []
        if self.shoutTextEffect:
            self.shoutTextEffect.finish()
            self.shoutTextEffect = None
        if self.model:
            self.model.cleanUpDamageEffects()
        return

    def enterCannonVis(self):
        self.cannonVis = True

    def exitCannonVis(self):
        self.cannonVis = False

    def startDistanceChecks(self):

        def checkDistances(task=None):
            for shipId in self.ActiveShips:
                ship = self.cr.getDo(shipId)
                if ship:
                    ship._calcLocalDistance(self)

            return Task.again

        self.stopDistanceChecks()
        checkDistances()
        self.shipDistanceCheck = taskMgr.doMethodLater(base.config.GetInt('ship-dist-delay', 5), checkDistances, self.uniqueName('shipDistanceCheck'))
        return

    def stopDistanceChecks(self):
        if self.shipDistanceCheck:
            taskMgr.remove(self.shipDistanceCheck)
            self.shipDistanceCheck = None
        return

    def __initDistance(self):
        if hasattr(base, 'localAvatar') and base.localAvatar.ship:
            self._calcLocalDistance(base.localAvatar.ship)

    def _calcLocalDistance(self, otherShip):
        prevDist = self.distanceToLocalShip
        self.distanceToLocalShip = self.getDistance(otherShip)
        self._registerLocalDistance()

    def _registerLocalDistance(self):
        if self.showWake():
            self.createWake()
        else:
            self.removeWake()
        if self.showRocking():
            self.setupFloatTask()
        else:
            self.cleanupFloatTask()
        if self.canAimBroadside():
            self.NearbyShips.add(self.doId)
        else:
            self.NearbyShips.discard(self.doId)

    def getDistanceToLocalShip(self):
        return self.distanceToLocalShip

    def showCannonsFiring(self, broadsides=False):
        return broadsides and self.distanceToLocalShip < DistributedSimpleShip.CannonFireBroadsideDist or not broadsides and self.distanceToLocalShip < DistributedSimpleShip.CannonFireDist

    def showWake(self):
        return self.distanceToLocalShip < DistributedSimpleShip.ShipWakeDist and self.gameFSM and self.isSailable()

    def showRocking(self):
        return self.distanceToLocalShip < DistributedSimpleShip.ShipRockDist and self.gameFSM and self.isSailable()

    def allowedToRock(self):
        return base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium or self.onThisShip(localAvatar.doId)

    def canAimBroadside(self):
        return self.distanceToLocalShip <= ShipGlobals.BROADSIDE_MAX_AUTOAIM_DIST + 1000.0

    def validateMastCode(self, mastCode):
        if mastCode == 255:
            return
        if self.maxMastHealth[mastCode] > 0:
            return True
        else:
            self.notify.error('Mast Issue! %s,%s,%s,%s' % (mastCode, self.shipClass, self.maxMastHealth, self.mastStates))


class MinimapShip(GridMinimapObject):
    ICON = None
    ICON_TRACKED = None
    DEFAULT_COLOR = VBase4(1.0, 0.0, 0.0, 1)

    def __init__(self, ship):
        if not MinimapShip.ICON:
            gui = loader.loadModel('models/gui/gui_main')
            MinimapShip.ICON = gui.find('**/icon_ship')
            MinimapShip.ICON.clearTransform()
            MinimapShip.ICON.setHpr(0, -90, 0)
            MinimapShip.ICON.setScale(1000)
            MinimapShip.ICON.flattenStrong()
            MinimapShip.ICON_TRACKED = gui.find('**/icon_objective_grey')
            MinimapShip.ICON_TRACKED.setScale(1.25)
            MinimapShip.ICON_TRACKED.setColorScale(Vec4(1, 1, 0, 1), 1)
            MinimapShip.ICON_TRACKED.flattenStrong()
        GridMinimapObject.__init__(self, ship.getName(), ship, MinimapShip.ICON)
        self.trackedNode = NodePath(ship.getName())
        self.trackedIcon = MinimapShip.ICON_TRACKED.copyTo(self.trackedNode)
        self.trackedIcon.reparentTo(self.mapGeom, sort=-1)
        self.trackedIcon.hide()
        self.isTracked = False
        self.isLocalAvShip = False
        self.siegeTeam = 0
        self.refreshIconColor()

    def setIsTracked(self, isTracked):
        self.isTracked = isTracked
        if self.isTracked:
            self.trackedIcon.show()
        else:
            self.trackedIcon.hide()

    def setAsLocalAvShip(self, isLocalAvShip):
        self.isLocalAvShip = isLocalAvShip
        self.refreshIconColor()

    def refreshIconColor(self):
        if PVPGlobals.FrenchTeam == self.siegeTeam:
            self.setIconColor(PiratesGuiGlobals.TextFG5, PiratesGuiGlobals.TextFG2, PiratesGuiGlobals.TextFG6)
        elif PVPGlobals.SpanishTeam == self.siegeTeam:
            self.setIconColor(PiratesGuiGlobals.TextFG6, PiratesGuiGlobals.TextFG8, PiratesGuiGlobals.TextFG6)
        elif self.isLocalAvShip:
            self.setIconColor(PiratesGuiGlobals.TextOV14)
        else:
            self.setIconColor()

    @report(types=['args'], dConfigParam='shipdeploy')
    def setIconColor(self, top=None, mid=None, bot=None):
        top = top or self.DEFAULT_COLOR
        mid = mid or top
        bot = bot or top
        self.mapGeom.find('**/icon_ship_top').setColorScale(top, 1)
        self.mapGeom.find('**/icon_ship_mid').setColorScale(mid, 1)
        self.mapGeom.find('**/icon_ship_bottom').setColorScale(bot, 1)

    def _zoomChanged(self, radius):
        self.mapGeom.setScale(radius / 1000.0)