import math
import random
import types
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import LerpFunc, Sequence
from direct.showbase.PythonUtil import lerp, clampScalar
from direct.interval.IntervalGlobal import *
from direct.distributed.ClockDelta import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.fsm import FSM
from direct.controls import BattleWalker
from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from direct.showutil import Rope
from direct.actor import Actor
from direct.task import Task
from direct.showbase.PythonUtil import report
from otp.otpbase import OTPGlobals
from pirates.piratesbase import TeamUtils
from pirates.reputation.DistributedReputationAvatar import DistributedReputationAvatar
from pirates.piratesbase import PiratesGlobals
from pirates.battle import WeaponGlobals
from pirates.minigame import PotionGlobals
from pirates.battle import Pistol
from pirates.movement import MotionFSM
from pirates.pirate import Human
from pirates.pirate import AvatarTypes
from pirates.reputation import ReputationGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.economy.EconomyGlobals import *
from pirates.reputation import ReputationGlobals
from pirates.economy import EconomyGlobals
from pirates.battle import BattleRandom
from pirates.battle.WeaponBase import WeaponBase
from pirates.battle import EnemyGlobals
from pirates.battle import EnemySkills
from pirates.effects.AttuneEffect import AttuneEffect
from pirates.effects.SpectralSmoke import SpectralSmoke
from pirates.effects.SmokeWisps import SmokeWisps
from pirates.effects.Flame import Flame
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from pirates.inventory import ItemGlobals
from pirates.piratesbase import EmoteGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.effects.CannonExplosion import CannonExplosion
from pirates.effects.CannonSplash import CannonSplash
from pirates.effects.DirtClod import DirtClod
from pirates.effects.DustCloud import DustCloud
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.RockShower import RockShower
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.DustRing import DustRing
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.ExplosionCloud import ExplosionCloud
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.FireTrail import FireTrail
from pirates.effects.Fire import Fire
from pirates.effects.GreenBlood import GreenBlood
from pirates.effects.HitFlashA import HitFlashA
from pirates.effects.ShipDebris import ShipDebris
from pirates.effects.WoodShards import WoodShards
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.effects.GraveShackles import GraveShackles
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.PoisonEffect import PoisonEffect
from pirates.effects.GroundDirt import GroundDirt
from pirates.effects.AttuneSmoke import AttuneSmoke
from pirates.effects.StunEffect import StunEffect
from pirates.effects.SlowEffect import SlowEffect
from pirates.effects.VoodooAura import VoodooAura
from pirates.effects.ToxinEffect import ToxinEffect
from pirates.effects.FreezeBlast import FreezeBlast
from pirates.effects.JRSpawn import JRSpawn
from pirates.effects.DarkPortal import DarkPortal
from pirates.effects.JRDeath import JRDeath
from pirates.effects.JRDeathBlast import JRDeathBlast
from pirates.effects.HealRays import HealRays
from pirates.effects.HealSparks import HealSparks
from pirates.effects import PolyTrail
from pirates.effects import TextEffect
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from otp.otpbase import OTPRender
from pirates.map.MinimapObject import GridMinimapObject
from pirates.battle.Teamable import Teamable
from pirates.battle.PotionStatusEffectManager import PotionStatusEffectManager
from pirates.piratesgui.CrewBuffDisplay import CrewBuffDisplay
from pirates.effects.GhostAura import GhostAura
from pirates.effects.EvilEyeGlow import EvilEyeGlow
from pirates.effects.MonkeyPanic import MonkeyPanic
from pirates.effects.ProtectionSpiral import ProtectionSpiral
from pirates.effects.HitPulse import HitPulse
from pirates.effects.FlashEffect import FlashEffect
from pirates.effects.PulseEffect import PulseEffect
from pirates.effects.GhostGlowShadow import GhostGlowShadow
from pirates.effects.ProtectionDome import ProtectionDome
if base.config.GetBool('want-pstats', 0):
    import profile
    import pstats

class DistributedBattleAvatar(DistributedReputationAvatar, WeaponBase, Teamable):
    Count = 0
    DiskUseColor = (1, 0, 0, 1)
    DiskWaitingColor = (1, 0, 0, 1)
    ManagesNametagAmbientLightChanged = False
    notify = directNotify.newCategory('DistributedBattleAvatar')
    PlayersInvulnerable = base.config.GetBool('players-invulnerable', 0)
    ShowUnderstandable = base.config.GetBool('show-understandable', 0)
    WantHpCheck = base.config.GetBool('want-hp-check', 1)

    def __init__(self, cr):
        DistributedReputationAvatar.__init__(self, cr)
        WeaponBase.__init__(self)
        Teamable.__init__(self)
        self.visZone = ''
        self.level = 0
        self.money = 0
        self.bossIcon = None
        self.bankMoney = 0
        self.maxMoney = 0
        self.maxBankMoney = 0
        self.weight = None
        self.battleIval = None
        self.skillIval = None
        self.setWeaponIval = None
        self.skillEffects = {}
        self.durationTask = None
        self.ensnaredTargetId = 0
        self.attuneEffect = None
        self.shacklesEffect = None
        self.smokeWispEffect = None
        self.gunSmokeEffect = None
        self.poisonEffect = None
        self.toxinEffect = None
        self.slowEffect = None
        self.slowEffect2 = None
        self.stunEffect = None
        self.stunEffect2 = None
        self.compassFX = None
        self.fireEffect = None
        self.voodooAttuneEffect = None
        self.voodooSmokeEffect = None
        self.voodooAttuneSound = None
        self.healRaysEffect = None
        self.healSparksEffect = None
        self.ghostGuardEffect = None
        self.ghostGuardPulseIval = None
        self.ghostTransitionIval = None
        self.furyEffect = None
        self.pulseEffect = None
        self.chatIcon = None
        self.crewBuffDisplay = None
        self.invisibleMask = BitMask32(0)
        self.battleTubeNodePaths = []
        self.aimTubeNodePaths = []
        self.height = 5.0
        self.battleTubeRadius = 2.0
        self.battleTubeHeight = 2.0
        self.battleCollisionBitmask = PiratesGlobals.WallBitmask | PiratesGlobals.TargetBitmask | PiratesGlobals.RadarAvatarBitmask
        self.battleTube = None
        self.consumable = None
        self.enemyId = None
        self.currentWeaponId = 0
        self.isWeaponDrawn = 0
        self.currentAmmo = 0
        self.secondWeapon = None
        self.currentTarget = None
        self.currentCharm = 0
        if self.WantHpCheck:
            self.__hp = 0
            self.__maxHp = 0
        else:
            self.hp = 0
            self.maxHp = 0
        self.power = 0
        self.maxPower = 0
        self.luck = 0
        self.maxLuck = 0
        self.mojo = 0
        self.maxMojo = 0
        self.swiftness = 0
        self.maxSwiftness = 0
        self.powerMod = 0
        self.luckMod = 0
        self.mojoMod = 0
        self.swiftnessMod = 0.0
        self.stunMod = 0.0
        self.tireMod = 0.0
        self.hasteMod = 0.0
        self.combo = 0
        self.comboDamage = 0
        self.lastComboTime = 0
        self.blinded = 0
        self.currentAttack = []
        self.ship = 0
        self.pendingSetShip = None
        self.cannon = None
        self.setNpc(0)
        self.nametagScale = 1.0
        self.setNametagScale(self.nametagScale)
        self.hpTextNodes = []
        self.hpTextIvals = []
        self.textEffects = []
        self.ouchAnim = None
        self.curAttackAnim = None
        self.rope = None
        self.ropeActor = None
        self.ambientSfx = None
        self.ambientFx = 0
        self.bobbing = False
        self.aimMod = 0
        self.creatureTransformation = False
        self.floorNorm = Vec3(0, 0, 1)
        self.tracksTerrain = None
        self.gNodeFwdPt = None
        self.minimapObj = None
        self.isTracked = False
        self.gameFSM = None
        self.ghostEffect = None
        self.ghostShadowEffect = None
        self.isGhost = 0
        self.ghostDelay = 0
        self.ghostBaseColor = None
        self.ghostBaseNegative = 0
        self.ghostGeomGenerated = 0
        self.ghostEyeGlowR = None
        self.ghostEyeGlowL = None
        self.depthGeom = None
        self.invisibleFlickerSeq = None
        self.inInvasion = False
        self.armorScale = 1.0
        self.monkeyPanic = None
        self.potionStatusEffectManager = None
        self.trackStats = 0
        if base.config.GetBool('want-pstats', 0):
            self.trackStats = 1
            if not hasattr(base, 'visList'):
                base.visList = []
                base.visCount = 0
                base.npcList = []
                base.npcCount = 0
            self.pstatsFPS = PStatCollector('Battle Avatars:fps')
            self.pstatsTotal = PStatCollector('Battle Avatars:Avatars Unseen')
            self.pstatsVisible = PStatCollector('Battle Avatars:Avatars Seen')
            self.pstatsTotal.setLevel(0)
            self.pstatsVisible.setLevel(0)
        self.emoteId = 0
        self.emoteTrack = None
        self.emoteAnimIval = None
        self.emoteProp = None
        self.emoteEffect = None
        self.battleCollisionsDisabled = False
        self.protectionEffect = None
        self.efficiency = False
        return

    if WantHpCheck:

        def get_hp(self):
            return self.__hp

        def set_hp(self, hp):
            if type(hp) in [types.IntType, types.FloatType]:
                self.__hp = hp
            else:
                self.__hp = 0

        hp = property(get_hp, set_hp)

        def get_maxHp(self):
            return self.__maxHp

        def set_maxHp(self, maxHp):
            if type(maxHp) in [types.IntType, types.FloatType]:
                self.__maxHp = maxHp
            else:
                self.__maxHp = 1

        maxHp = property(get_maxHp, set_maxHp)

    def generate(self):
        DistributedReputationAvatar.generate(self)
        WeaponBase.generate(self)
        self.lookAroundTaskName = self.taskName('lookAround')
        self.createGameFSM()
        self.motionFSM = MotionFSM.MotionFSM(self)
        self.battleRandom = BattleRandom.BattleRandom(self.doId)
        self.accept(''.join(['trackBackstab-', str(self.doId)]), self.newBackstab)
        self.accept('localAvatarActiveQuestId', self.setIsTracked)
        if base.options.getCharacterDetailSetting() == 0 and not self.isLocal():
            self.wantsActive = 0

    def announceGenerate(self):
        DistributedBattleAvatar.Count += 1
        self.handleLocalAvatarVisZoneChanged()
        self.accept('localAvatarVisZoneChanged', self.handleLocalAvatarVisZoneChanged)
        yieldThread('battle av start')
        DistributedReputationAvatar.announceGenerate(self)
        yieldThread('rep av gen')
        WeaponBase.announceGenerate(self)
        yieldThread('wb/start battle gen')
        self.initializeBattleCollisions()
        yieldThread('batttle collisions')
        if not self.isLocal() and self.canMove:
            self.showDebugName()
            self.startSmooth()
        yieldThread('smoothing')
        self.setCurrentWeapon(self.currentWeaponId, self.isWeaponDrawn)
        yieldThread('current weapon')
        self.setHeight(self.height)
        yieldThread('set Height')
        if self.ambientSfx:
            self.ambientFx = SoundInterval(self.ambientSfx, node=self)
            self.ambientFx.loop()
            yieldThread('sound')
        if self.dropShadow:
            self.dropShadow.setPos(self, (0, 0, 0))
        self.setIsTracked(localAvatar.activeQuestId)
        if self.trackStats:
            base.npcList.append(self.doId)
            base.npcCount = len(base.npcList)
            onScreenDebug.add('Avatar Count', base.npcCount)
            self.pstatsTotal.setLevel(base.npcCount - (base.visCount + 1))
            self.pstatsVisible.setLevel(base.visCount)
            if base.options.character_detail_level == PiratesGlobals.CD_LOW and not self.isLocal():
                self.setLODAnimation(100, 5, 0.1)
        if self.isGhost:
            self.startGhost(self.isGhost)
        if self.isInvisible():
            if self.isInteractiveMasked():
                self.requestHideTarget()
            self.activateInvisibleEffect()

    def setLocation(self, parentId, zoneId):
        DistributedReputationAvatar.setLocation(self, parentId, zoneId)

        if self.parentId:
            self.wrtReparentTo(self.getParentObj())

    def disable(self):
        DistributedBattleAvatar.Count -= 1
        if self.trackStats:
            if self.doId in base.npcList:
                base.npcList.remove(self.doId)
                base.npcCount = len(base.npcList)
                while self.doId in base.visList:
                    base.visList.remove(self.doId)

                base.visCount = len(base.visList)
            onScreenDebug.add('Avatar Count', base.npcCount)
            onScreenDebug.add('Avatar Vis Count', base.visCount)
            self.pstatsTotal.setLevel(base.npcCount - (base.visCount + 1))
            self.pstatsVisible.setLevel(base.visCount)
        if self.isGhost:
            holdGhost = self.isGhost
            self.setIsGhost(0, override=1)
            self.isGhost = holdGhost
        self.ignoreAll()
        self.detachNode()
        self.stopSmooth()
        taskMgr.remove(self.taskName('usingSkill'))
        taskMgr.removeTasksMatching(self.taskName('playMotionAnim*'))
        taskMgr.remove(self.taskName('playHitSoundTask'))
        taskMgr.remove(self.taskName('playOuchTask'))
        taskMgr.remove(self.taskName('playBonusOuchTask'))
        taskMgr.remove(self.taskName('showMissTask'))
        taskMgr.remove(self.taskName('endBlind'))
        taskMgr.remove(self.taskName('printExp'))
        taskMgr.remove(self.taskName('playMpDamage'))
        if not self.isLocal():
            self.deleteBattleCollisions()
        if hasattr(self, 'stopLookAroundTask'):
            self.stopLookAroundTask()
        self.stopBobSwimTask()
        taskMgr.remove(self.uniqueName('InvisibleFlicker'))
        if self.invisibleFlickerSeq:
            self.invisibleFlickerSeq.clearToInitial()
            self.invisibleFlickerSeq = None
        if self.potionStatusEffectManager:
            self.disablePotionFx()
        self.ship = 0
        if self.pendingSetShip:
            self.cr.relatedObjectMgr.abortRequest(self.pendingSetShip)
            self.pendingSetShip = None
        self._removePoisonEffect(cleanup=True)
        self._removeHoldEffect(cleanup=True)
        self._removeToxinEffect(cleanup=True)
        self._removeMonkeyPanicEffect(cleanup=True)
        self._removeAcidEffect()
        self._removeOnFireEffect()
        self._removeSlowEffect()
        self._removeStunEffect()
        self._removeRegenEffect()
        self._removeGhostGuardEffect()
        self._removeFuryEffect()
        if self.crewBuffDisplay:
            self.crewBuffDisplay.stop()
            self.crewBuffDisplay.destroy()
            self.crewBuffDisplay = None
        if self.isLocal():
            self.guiMgr.hideDirtPanel()
            self.guiMgr.hideSmokePanel()
        if self.ouchAnim:
            self.ouchAnim.finish()
            self.ouchAnim = None
        if self.curAttackAnim:
            self.curAttackAnim.pause()
            self.curAttackAnim = None
        self.stopCompassEffect()
        self.destroyMinimapObject()
        taskMgr.remove(self.taskName('sendSwitchMsgTask'))
        taskMgr.remove(self.taskName('pullOutWeaponTask'))
        for ival in self.hpTextIvals:
            if ival:
                ival.pause()

        self.hpTextIvals = []
        for hpText in self.hpTextNodes:
            if hpText:
                hpText.removeNode()

        self.hpTextNodes = []
        for currTextEffect in self.textEffects:
            if currTextEffect:
                currTextEffect.finish()

        self.textEffects = []
        self.hideHpMeter(0.0)
        self.gameFSM.cleanup()
        self.gameFSM = None
        self.motionFSM.cleanup()
        del self.motionFSM
        if self.setWeaponIval:
            self.setWeaponIval.pause()
            self.setWeaponIval = None
        if self.currentWeapon:
            self.currentWeapon.delete()
            self.currentWeapon = None
        if self.secondWeapon:
            self.secondWeapon.removeNode()
            self.secondWeapon = None
        self.currentWeaponId = 0
        self.isWeaponDrawn = 0
        self.currentTarget = None
        DistributedReputationAvatar.disable(self)
        WeaponBase.disable(self)
        if self.ambientFx:
            self.ambientFx.pause()
        self.ambientFx = None
        self.cleanupEmote()
        del self.battleRandom
        return

    def delete(self):
        self.ropeActor = None
        self.rope = None
        taskMgr.remove(self.getSwimTaskName())
        DistributedReputationAvatar.delete(self)
        WeaponBase.delete(self)
        return

    def getBroadcastPeriod(self):
        return PiratesGlobals.AI_MOVEMENT_PERIOD

    def startSmooth(self):
        if not self.isLocal():
            broadcastPeriod = 2.0
            self.smoother.setMaxPositionAge(broadcastPeriod * 1.25 * 10)
            self.smoother.setExpectedBroadcastPeriod(self.getBroadcastPeriod())
            self.smoother.setAcceptClockSkew(False)
            self.smoother.setDefaultToStandingStill(False)
            self.smoother.setDelay(OTPGlobals.NetworkLatency * 1.5)
        DistributedReputationAvatar.startSmooth(self)

    def setAvatarType(self, avatarType):
        self.avatarType = avatarType
        self.height = EnemyGlobals.getHeight(avatarType)
        self.battleTubeHeight = max(10.0, self.height)
        self.battleTubeRadius = EnemyGlobals.getBattleTubeRadius(avatarType)

    def smoothPosition(self):
        DistributedSmoothNode.smoothPosition(self)
        if self.getGameState() == 'WaterRoam':
            if self.cr.wantSeapatch:
                world = self.cr.getActiveWorld()
                if world:
                    water = world.getWater()
                else:
                    water = None
                if water:
                    zWater, normal = water.calcHeightAndNormal(node=self)
                    self.setZ(render, zWater)
                    geom = self.getGeomNode()
                    geom.setP(render, normal[1] * 90 - 7)
        if self.getGameState() not in ('Injured', 'Dying', 'Healing'):
            self.updateMyAnimState(self.smoother.getSmoothForwardVelocity(), self.smoother.getSmoothRotationalVelocity(), self.smoother.getSmoothLateralVelocity())
        return

    def updateMyAnimState(self, forwardVel, rotationVel, lateralVel):
        self.motionFSM.motionAnimFSM.updateAnimState(forwardVel, rotationVel, lateralVel)

    def setNpc(self, isNpc):
        self.isNpc = isNpc

    def setAmbush(self, ambush):
        self.ambushEnemy = ambush

    def setShipId(self, shipId):
        if self.pendingSetShip:
            self.cr.relatedObjectMgr.abortRequest(self.pendingSetShip)
            self.pendingSetShip = None
        if shipId:
            self.pendingSetShip = self.cr.relatedObjectMgr.requestObjects([shipId], eachCallback=self._setShip)
        else:
            self._setShip(0)
            if self.crewBuffDisplay and self.isLocal():
                self.crewBuffDisplay.stop()
                self.crewBuffDisplay.destroy()
        return

    def getShipId(self):
        return self.ship and self.ship.doId or 0

    def _setShip(self, ship):
        self.ship = ship

    def getShip(self):
        return self.ship

    def setName(self, name):
        DistributedReputationAvatar.setName(self, name)
        self.refreshStatusTray()
        self.nametag.setDisplayName('        ')
        nameText = self.getNameText()
        if nameText:
            if self.isNpc:
                if not self.avatarType.isA(AvatarTypes.Townfolk):
                    self.accept('weaponChange', self.setMonsterNameTag)
                    self.setMonsterNameTag()
                else:                    nameText['text'] = self.name
                color2 = EnemyGlobals.getNametagColor(self.avatarType)
                if self.isBoss() and not self.bossIcon and not self.avatarType.isA(AvatarTypes.Townfolk):
                    color2 = (0.95, 0.1, 0.1, 1)
                    self.bossIcon = loader.loadModel('models/gui/flag_boss')
                    self.bossIcon.setScale(3.5)
                    self.bossIcon.flattenLight()
                    self.bossIcon.setBillboardPointEye()
                    self.bossIcon.setPos(-0.75, 0, 2.6)
                    self.bossIcon.reparentTo(nameText)
                nameText['fg'] = color2

    def getNameText(self):
        pass

    def setMonsterNameTag(self):
        if self.level:
            color = self.cr.battleMgr.getExperienceColor(base.localAvatar, self)
            name = '%s  %s\x01smallCaps\x01%s%s\x02\x02' % (self.name, color, PLocalizer.Lv, self.level)
        else:
            name = self.name

        if self.getNameText():
            self.getNameText()['text'] = name

    def considerUnderstandable(self):
        DistributedReputationAvatar.considerUnderstandable(self)
        if self.ShowUnderstandable and not self.isNpc and self.iconNodePath and self.isUnderstandable() and not self.chatIcon and base.localAvatar.getDoId() != self.getDoId():
            self.chatIcon = loader.loadModel('models/textureCards/flagIcons')
            self.chatIcon.setScale(2.5, 1.5, 1.5)
            self.chatIcon.setPos(5, 0, -1.0)
            self.chatIcon.reparentTo(self.iconNodePath)

    def refreshStatusTray(self):
        statusTray = localAvatar.guiMgr.targetStatusTray
        if localAvatar.currentTarget == self or statusTray.doId == self.doId:
            statusTray.updateHp(self.hp, self.maxHp, self.doId)
            statusTray.updateVoodoo(self.mojo, self.maxMojo, self.doId)
            statusTray.updateStatusEffects(self.skillEffects)
            statusTray.updateSkill(self.currentAttack, self.doId)
            sticky = localAvatar.currentTarget == self and localAvatar.hasStickyTargets()
            statusTray.updateSticky(sticky)
            if self.hp > 0:
                statusTray.show()
            else:
                self.hideHpMeter(1.0)

    def showProximityInfo(self):
        if not hasattr(base, 'tutorial'):
            DistributedReputationAvatar.showProximityInfo(self)

    def initializeBattleCollisions(self):
        if self.battleTubeNodePaths or self.battleCollisionsDisabled:
            return

        self.battleTubeEvent = self.uniqueName('battleAvatarTube')
        self.battleTube = CollisionTube(0, 0, 0, 0, 0, self.battleTubeHeight, self.battleTubeRadius)
        self.battleTube.setTangible(1)
        battleTubeNode = CollisionNode(self.battleTubeEvent)
        battleTubeNode.addSolid(self.battleTube)
        battleTubeNode.setIntoCollideMask(self.battleCollisionBitmask)
        battleTubeNodePath = self.attachNewNode(battleTubeNode)
        battleTubeNodePath.setTag('objType', str(PiratesGlobals.COLL_AV))
        battleTubeNodePath.setTag('avId', str(self.doId))
        self.battleTubeNodePaths.append(battleTubeNodePath)
        if self.isBattleable():
            self.aimTubeEvent = self.uniqueName('aimTube')
            aimTube = CollisionTube(0, 0, -max(10, self.battleTubeHeight), 0, 0, max(10, self.battleTubeHeight), self.battleTubeRadius * 1.5)
            aimTube.setTangible(0)
            aimTubeNode = CollisionNode(self.aimTubeEvent)
            aimTubeNode.addSolid(aimTube)
            aimTubeNode.setIntoCollideMask(PiratesGlobals.BattleAimBitmask)
            aimTubeNodePath = self.attachNewNode(aimTubeNode)
            aimTubeNodePath.setTag('objType', str(PiratesGlobals.COLL_AV))
            aimTubeNodePath.setTag('avId', str(self.doId))
            self.cr.targetMgr.addTarget(aimTubeNodePath.get_key(), self)
            self.aimTubeNodePaths.append(aimTubeNodePath)

    def disableBattleCollisions(self):
        self.deleteBattleCollisions()
        self.battleCollisionsDisabled = True

    def enableBattleCollisions(self):
        self.battleCollisionsDisabled = False
        self.initializeBattleCollisions()

    def deleteBattleCollisions(self):
        if not self.battleTubeNodePaths:
            return
        if self.battleTube:
            self.battleTube = None
        for np in self.battleTubeNodePaths:
            np.removeNode()

        self.battleTubeNodePaths = []
        if self.isBattleable():
            for np in self.aimTubeNodePaths:
                if hasattr(self.cr, 'targetMgr') and self.cr.targetMgr:
                    self.cr.targetMgr.removeTarget(np.get_key())
                np.removeNode()

            self.aimTubeNodePaths = []
        return

    def stashBattleCollisions(self):
        for tube in self.battleTubeNodePaths:
            tube.stash()

        for tube in self.aimTubeNodePaths:
            tube.stash()

    def unstashBattleCollisions(self):
        for tube in self.battleTubeNodePaths:
            tube.unstash()

        for tube in self.aimTubeNodePaths:
            tube.unstash()

    def createHitTrack(self, parent, explosionPoint=Point3(0)):
        explosion = loader.loadModel('models/sea/splash.bam')
        explosion.setScale(0.4)
        explosion.setColorScale(0, 1, 1, 1)
        explosion.setBillboardPointWorld()
        return Sequence(Func(explosion.reparentTo, parent), Func(explosion.setPos, explosionPoint), Wait(0.6), Func(explosion.detachNode))

    def isBattleable(self):
        return 1

    def canAggro(self):
        return True

    def requestInteraction(self, avId, interactType=0):
        if self.isLocal():
            self.notify.warning('We are hearing our own requestInteraction bounced back to us')
            return
        DistributedReputationAvatar.requestInteraction(self, avId, interactType)
        if not self.isBattleable():
            return
        if not self.canAggro():
            return
        skillEffects = self.getSkillEffects()
        if WeaponGlobals.C_SPAWN in skillEffects:
            return
        base.localAvatar.setCurrentTarget(self.doId)

    def requestExit(self):
        if self.isLocal():
            self.notify.warning('We are hearing our own requestExit bounced back to us')
            return
        DistributedReputationAvatar.requestExit(self)

    def setCurrentTarget(self, targetId):
        if self.currentTarget:
            if targetId == None:
                self.currentTarget.resetComboLevel()
        self.currentTarget = self.cr.doId2do.get(targetId)
        if hasattr(self, 'undead') and self.undead:
            self.skeleton.currentTarget = self.currentTarget
        return

    def setLocalTarget(self, on):
        DistributedReputationAvatar.setLocalTarget(self, on)
        return
        if not self.isLocal():
            if on:
                self.battleTubeNodePath.stash()
            else:
                self.battleTubeNodePath.unstash()

    def isInvisible(self):
        skillEffects = self.getSkillEffects()
        if WeaponGlobals.C_INVISIBILITY_LVL1 in skillEffects or WeaponGlobals.C_INVISIBILITY_LVL2 in skillEffects:
            return 1
        else:
            return 0

    def fakeEnemyAggroTask(self, task):
        currControls = self.controlManager.currentControls
        if currControls == None:
            return
        colliderExists = base.shadowTrav.hasCollider(currControls.cWallSphereNodePath) or currControls.cTrav.hasCollider(currControls.cWallSphereNodePath)
        if colliderExists:
            currControls.cTrav.removeCollider(currControls.cWallSphereNodePath)
            base.shadowTrav.removeCollider(currControls.cWallSphereNodePath)
            currControls.pusher.addInPattern('enter%in')
            currControls.pusher.addOutPattern('exit%in')
        else:
            currControls.pusher.clearInPatterns()
            currControls.pusher.clearOutPatterns()
            base.shadowTrav.addCollider(currControls.cWallSphereNodePath, currControls.event)
        return Task.done

    def setIsInvisible(self, setInvisible):
        if not self.isGenerated():
            return
        if setInvisible:
            if self.isInteractiveMasked():
                self.requestHideTarget()
            self.activateInvisibleEffect()
        else:
            self.deactivateInvisibleEffect()
            if self.isLocal():
                taskMgr.doMethodLater(0.1, self.fakeEnemyAggroTask, 'fakeEnemyAggroTask')
                self.fakeEnemyAggroTask(None)
        if hasattr(self, 'refreshName'):
            self.refreshName()
        if self.minimapObj:
            if setInvisible:
                self.minimapObj.mapGeom.hide()
            else:
                self.minimapObj.mapGeom.show()
        return

    def activateInvisibleEffect(self):
        self.deleteDropShadow()
        geom = self.getGeomNode()
        self.ghostColorMult = 1.0
        ghostColor = self.ghostBaseColor * self.ghostColorMult
        if self.isLocal():
            geom.setTransparency(1)
            geom.setDepthWrite(0)
            geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            geom.setColorScale(ghostColor)
            geom.setBin('pre-additive', 4)
            geom.setLightOff()
            geom.setAttrib(DepthTestAttrib.make(DepthTestAttrib.MLessEqual))
            geom.setAlphaScale(0.4)
            self.depthGeom = geom.getParent().attachNewNode('depthGeom')
            geom.instanceTo(self.depthGeom)
            self.depthGeom.setTransparency(0, 1)
            self.depthGeom.setTextureOff(1)
            self.depthGeom.setAttrib(ColorWriteAttrib.make(0))
            self.depthGeom.setDepthWrite(1, 1)
            self.depthGeom.setBin('pre-additive', 1, 1)
            self.addInvisibleFlickerSeq()
            if self.invisibleFlickerSeq:
                self.invisibleFlickerSeq.loop()
        else:
            geom.setTransparency(1)
            geom.setDepthWrite(0)
            geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            geom.setColorScale(VBase4(0.0, 0.0, 0.0, 0.0))

    def deactivateInvisibleEffect(self):
        geom = self.getGeomNode()
        geom.clearDepthWrite()
        geom.clearDepthTest()
        geom.clearTransparency()
        geom.clearTwoSided()
        geom.clearTexture()
        geom.clearBin()
        geom.clearAttrib(ColorBlendAttrib.getClassType())
        geom.clearAttrib(ColorWriteAttrib.getClassType())
        geom.clearColorScale()
        geom.clearLight()
        self.initializeDropShadow()
        if self.isLocal():
            taskMgr.remove(self.uniqueName('InvisibleFlicker'))
            self.depthGeom.removeNode()
        else:
            geom.setRenderModeFilled()
        if self.invisibleFlickerSeq:
            self.invisibleFlickerSeq.clearToInitial()
            self.invisibleFlickerSeq = None
        return

    def addInvisibleFlickerSeq(self):
        if self.invisibleFlickerSeq:
            self.invisibleFlickerSeq.finish()
            del self.invisibleFlickerSeq
            self.invisibleFlickerSeq = None
        geom = self.getGeomNode()
        self.invisibleFlickerSeq = Sequence(LerpFunc(geom.setAlphaScale, duration=1.0, toData=0.5, fromData=0.3), LerpFunc(geom.setAlphaScale, duration=1.0, toData=0.3, fromData=0.5))
        return

    def setGhostColor(self, ghostColor):
        self.ghostColor = ghostColor
        self.ghostBaseNegative = 0
        if self.ghostColor or self.ghostBaseColor == None:
            if self.ghostColor == 1:
                self.ghostBaseColor = VBase4(0.2, 0.7, 1.0, 1.0)
            elif self.ghostColor == 2:
                self.ghostBaseColor = VBase4(1.0, 0.5, 0.0, 1.0)
            elif self.ghostColor == 3:
                self.ghostBaseColor = VBase4(0.45, 0.8, 0.1, 1.0)
            elif self.ghostColor == 4:
                self.ghostBaseColor = VBase4(1.0, 0.0, 0.0, 1.0)
            elif self.ghostColor == 5:
                self.ghostBaseColor = VBase4(0.2, 0.7, 1.0, 1.0)
            elif self.ghostColor == 7:
                self.ghostBaseColor = VBase4(0, 0, 0, 1.0)
            elif self.ghostColor == 8:
                self.ghostBaseColor = VBase4(0.1, 0, 0.3, 1.0)
            elif self.ghostColor == 9:
                self.ghostBaseColor = VBase4(0.65, 0.85, 0.1, 1.0)
            elif self.ghostColor == 13:
                self.ghostBaseColor = VBase4(1.0, 1.0, 1.0, 1.0)
                self.ghostBaseNegative = 1
            else:
                self.ghostBaseColor = VBase4(0.0, 1.0, 1.0, 1.0)
        if self.isGhost:
            self.stopGhost(self.isGhost)
            self.startGhost(self.isGhost)
        return

    def setIsGhost(self, isGhost, override=0):
        if self.ghostBaseColor == None:
            self.ghostBaseColor = VBase4(0.3, 1.0, 0.75, 1.0)
        if self.isGhost == isGhost and not self.ghostDelay:
            return
        else:
            if self.isGenerated() == False and not override:
                self.isGhost = isGhost
                self.ghostDelay = 1
                return
            self.stopGhost(self.isGhost)
            if isGhost:
                self.isGhost = isGhost
                self.startGhost(isGhost)
                if self.isInteractiveMasked():
                    self.requestHideTarget()
        self.isGhost = isGhost
        if hasattr(self, 'refreshName'):
            self.refreshName()
        if self.minimapObj:
            if self.isInvisibleGhost():
                self.minimapObj.mapGeom.hide()
            else:
                self.minimapObj.mapGeom.show()
        return

    def isInteractiveMasked(self):
        return self.isInvisible() or self.isInvisibleGhost()

    def isInvisibleGhost(self):
        if self.isGhost in [3, 4]:
            return 1
        else:
            return 0

    def startGhost(self, effectNumber):
        if effectNumber == 7:
            return
        if self.ghostGeomGenerated == 0:
            if self.style:
                self.generateHuman(self.style.getGender(), base.cr.human)
            else:
                self.generateHuman('n', base.cr.human)
            self.ghostGeomGenerated = 1
            state = self.gameFSM.getCurrentOrNextState()
            if state in ['Battle']:
                redraw = 0
                if self.isLocal() and localAvatar.isWeaponDrawn:
                    redraw = 1
                self.gameFSM.request('LandRoam')
                self.gameFSM.request('Battle')
                if self.isLocal() and redraw:
                    localAvatar.toggleWeapon(localAvatar.currentWeaponId, localAvatar.currentWeaponSlotId)
        self.deleteDropShadow()
        if self.currentWeapon:
            if hasattr(self.currentWeapon, 'removeTrail'):
                self.currentWeapon.removeTrail()
        geom = self.getGeomNode()
        self.ghostColorMult = 1.0
        ghostColor = self.ghostBaseColor * self.ghostColorMult
        if effectNumber == 1:
            geom.setTransparency(1)
            geom.setDepthWrite(0)
            geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            geom.setColorScale(ghostColor)
            geom.setRenderModeFilled()
            geom.findAllMatches('**/teeth*').hide()
            geom.findAllMatches('**/eyes').hide()
            geom.setBin('pre-additive', 4)
            geom.setLightOff()
            geom.setAttrib(DepthTestAttrib.make(DepthTestAttrib.MLessEqual))
            self.depthGeom = geom.getParent().attachNewNode('depthGeom')
            geom.instanceTo(self.depthGeom)
            self.depthGeom.setTransparency(0, 1)
            self.depthGeom.setTextureOff(1)
            self.depthGeom.setAttrib(ColorWriteAttrib.make(0))
            self.depthGeom.setDepthWrite(1, 1)
            self.depthGeom.setBin('pre-additive', 1, 1)
            if self.addGhostEffect(ghostColor):
                self.ghostEffect.startLoop()
                self.ghostShadowEffect.startLoop()
                self.ghostEffect.beNormal()
                if self.ghostBaseNegative:
                    self.ghostEffect.beNegative()
                else:
                    self.ghostEffect.bePositive()
            taskMgr.add(self.ghostFlicker, self.uniqueName('GhostFlicker'))
        elif effectNumber == 2:
            geom.setTransparency(1)
            geom.setTransparency(0, 1)
            geom.setRenderModeFilled()
            if self.ghostBaseNegative:
                geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MInvSubtract, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            else:
                geom.setAttrib(ColorWriteAttrib.make(0))
            geom.setDepthWrite(1, 1)
            geom.setLightOff()
            geom.setBin('pre-additive', 1, 1)
            if self.addGhostEffect(ghostColor):
                self.ghostEffect.startLoop()
                self.ghostShadowEffect.startLoop()
                self.ghostEffect.beThick()
                self.ghostEffect.beWide()
                if self.ghostBaseNegative and 0:
                    self.ghostEffect.beNegative()
                else:
                    self.ghostEffect.bePositive()
            npCollection = geom.findAllMatches('**/eyes')
            for np in npCollection:
                np.setColorScale(VBase4(1.0, 0.0, 0.0, 1.0), 4)
                np.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CAll), 1)
                np.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne), 1)
                np.setTextureOff(1)
                np.setBin('pre-additive', 2, 2)
                np.show()

            eyeGlow = EvilEyeGlow.getEffect(1)
            if eyeGlow:
                self.ghostEyeGlowR = eyeGlow
                self.ghostEyeGlowR.setTextureOff(0)
                self.ghostEyeGlowR.setColorScale(VBase4(0.5, 0.0, 0.0, 1.0), 5)
                self.ghostEyeGlowR.setBin('pre-additive', 0, 2)
                self.ghostEyeGlowR.startLoop()
            eyeGlow = EvilEyeGlow.getEffect(1)
            if eyeGlow:
                self.ghostEyeGlowL = eyeGlow
                self.ghostEyeGlowR.setTextureOff(0)
                self.ghostEyeGlowL.setColorScale(VBase4(0.5, 0.0, 0.0, 1.0), 5)
                self.ghostEyeGlowL.setBin('pre-additive', 0, 2)
                self.ghostEyeGlowL.startLoop()
            if self.ghostEyeGlowL and self.ghostEyeGlowR:
                if self.style.gender == 'f':
                    self.ghostEyeGlowL.setPos(0.175, -0.13, -0.25)
                    self.ghostEyeGlowR.setPos(0.175, 0.13, -0.25)
                else:
                    self.ghostEyeGlowL.setPos(0.275, -0.13, -0.35)
                    self.ghostEyeGlowR.setPos(0.275, 0.13, -0.35)
                self.ghostEyeGlowL.reparentTo(self.headNode)
                self.ghostEyeGlowR.reparentTo(self.headNode)
                self.ghostEyeGlowL.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CAll), 1)
                self.ghostEyeGlowL.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne), 1)
                self.ghostEyeGlowR.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CAll), 1)
                self.ghostEyeGlowR.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne), 1)
        elif effectNumber == 3:
            geom.setTransparency(1)
            geom.setDepthWrite(0)
            geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            geom.setColorScale(VBase4(0.0, 0.0, 0.0, 0.0))
            geom.setRenderModeFilled()
            if self.addGhostEffect(ghostColor):
                self.ghostEffect.beThick()
                self.ghostEffect.beOrb()
                self.ghostEffect.startLoop()
                self.ghostShadowEffect.lodDistance = 300
                self.ghostShadowEffect.startLoop()
                if self.ghostBaseNegative:
                    self.ghostEffect.beNegative()
                else:
                    self.ghostEffect.bePositive()
        elif effectNumber == 4:
            geom.setTransparency(1)
            geom.setDepthWrite(0)
            geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            if self.isLocal() or localAvatar.isGM():
                geom.setColorScale(ghostColor)
                geom.setRenderModeWireframe()
            else:
                geom.setRenderModeFilled()
                geom.setColorScale(VBase4(0.0, 0.0, 0.0, 0.0))
        elif effectNumber == 5:
            if self.isLocal():
                geom.setTransparency(1)
                geom.setDepthWrite(0)
                geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                geom.setColorScale(ghostColor)
                geom.setRenderModeFilled()
                geom.setBin('pre-additive', 4)
                geom.setLightOff()
                geom.setAttrib(DepthTestAttrib.make(DepthTestAttrib.MLessEqual))
                geom.setAlphaScale(0.4)
                self.depthGeom = geom.getParent().attachNewNode('depthGeom')
                geom.instanceTo(self.depthGeom)
                self.depthGeom.setTransparency(0, 1)
                self.depthGeom.setTextureOff(1)
                self.depthGeom.setAttrib(ColorWriteAttrib.make(0))
                self.depthGeom.setDepthWrite(1, 1)
                self.depthGeom.setBin('pre-additive', 1, 1)
                self.addInvisibleFlickerSeq()
                if self.invisibleFlickerSeq:
                    self.invisibleFlickerSeq.loop()
            else:
                geom.setTransparency(1)
                geom.setDepthWrite(0)
                geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                geom.setColorScale(VBase4(0.0, 0.0, 0.0, 0.0))
                geom.setRenderModeFilled()

    def fadeOutGhost(self):
        if self.addGhostEffect(self.ghostBaseColor):
            self.ghostEffect.beThick()
            self.ghostEffect.beOrb()
            self.ghostEffect.moveDown()
            self.ghostEffect.play()
        taskMgr.remove(self.uniqueName('GhostFlicker'))
        taskMgr.remove(self.uniqueName('InvisibleFlicker'))
        self.ghostTransitionIval = Sequence(Func(self.getGeomNode().setTransparency, 1), LerpColorScaleInterval(self.getGeomNode(), 1.5, VBase4(1, 1, 1, 0)))
        self.ghostTransitionIval.start()

    def addGhostEffect(self, ghostColor):
        if self.ghostEffect:
            self.ghostEffect.stopLoop()
            self.ghostEffect = None
        if self.ghostShadowEffect:
            self.ghostShadowEffect.stopLoop()
            self.ghostShadowEffect = None
        self.ghostEffect = GhostAura.getEffect(unlimited=1)
        if not self.ghostEffect:
            self.ghostEffect = None
            return 0
        self.ghostEffect.reparentTo(self)
        if self.ghostBaseNegative and 0:
            self.ghostEffect.p0.renderer.setColor(Vec4(1.0 - ghostColor[0], 1.0 - ghostColor[1], 1.0 - ghostColor[2], ghostColor[3]))
        else:
            self.ghostEffect.p0.renderer.setColor(ghostColor)
        self.ghostEffect.setBin('additive', 4)
        self.ghostEffect.beNormal()
        self.ghostShadowEffect = GhostGlowShadow.getEffect(unlimited=1)
        if self.ghostBaseNegative and 0:
            self.ghostShadowEffect.effectColor = Vec4(1.0 - ghostColor[0], 1.0 - ghostColor[1], 1.0 - ghostColor[2], 0.5)
        else:
            self.ghostShadowEffect.effectColor = Vec4(ghostColor[0], ghostColor[1], ghostColor[2], 0.5)
        self.ghostShadowEffect.lodDistance = 50
        self.ghostShadowEffect.reparentTo(self)
        return 1

    def postAsyncLoadFix(self):
        if self.isGhost == 2 and self.ghostEyeGlowL and self.ghostEyeGlowR:
            self.ghostEyeGlowL.reparentTo(self.headNode)
            self.ghostEyeGlowR.reparentTo(self.headNode)

    def ghostFlicker(self, task):
        geom = self.getGeomNode()
        if geom:
            ghostChange = -0.1 + random.random() * 0.2
            self.ghostColorMult += ghostChange
            self.ghostColorMult = max(min(1.0, self.ghostColorMult), 0.5)
            ghostColor = self.ghostBaseColor * self.ghostColorMult
            geom.setColorScale(ghostColor)
        return task.cont

    def stopGhost(self, effectNumber, isDev=False):
        if effectNumber == 7:
            return
        geom = self.getGeomNode()
        geom.clearDepthWrite()
        geom.clearDepthTest()
        geom.clearTransparency()
        geom.setRenderModeFilled()
        geom.clearTwoSided()
        geom.clearTexture()
        geom.clearBin()
        geom.clearAttrib(ColorBlendAttrib.getClassType())
        geom.clearAttrib(ColorWriteAttrib.getClassType())
        geom.clearColorScale()
        geom.clearLight()
        if hasattr(self, 'creature') and self.creature:
            self.creature.initializeDropShadow()
        else:
            self.initializeDropShadow()
        if self.currentWeapon:
            if hasattr(self.currentWeapon, 'createTrail'):
                self.currentWeapon.createTrail(self)
        if effectNumber == 1:
            taskMgr.remove(self.uniqueName('GhostFlicker'))
            geom.findAllMatches('**/teeth*').show()
            geom.findAllMatches('**/eyes').show()
            if self.depthGeom:
                self.depthGeom.removeNode()
        else:
            if effectNumber == 2:
                npCollection = geom.findAllMatches('**/eyes')
                for np in npCollection:
                    np.clearColorScale()
                    np.clearBin()
                    np.clearTwoSided()
                    np.clearAttrib(ColorBlendAttrib.getClassType())
                    np.clearAttrib(ColorWriteAttrib.getClassType())
                    np.setTextureOff(0)

                if self.depthGeom:
                    self.depthGeom.removeNode()
            else:
                if effectNumber == 3:
                    pass
                else:
                    if effectNumber == 4:
                        geom.setRenderModeFilled()
                    elif effectNumber == 5:
                        if self.isLocal():
                            taskMgr.remove(self.uniqueName('InvisibleFlicker'))
                            self.depthGeom.removeNode()
                        else:
                            geom.setRenderModeFilled()
                    if self.invisibleFlickerSeq:
                        self.invisibleFlickerSeq.finish()
                        del self.invisibleFlickerSeq
                        self.invisibleFlickerSeq = None
                    localAvatar.removeWobbleId(self.doId)
                    if self.ghostEffect:
                        self.ghostEffect.stopLoop()
                        self.ghostEffect = None
                    if self.ghostShadowEffect:
                        self.ghostShadowEffect.stopLoop()
                        self.ghostShadowEffect = None
                if self.ghostEyeGlowR:
                    self.ghostEyeGlowR.stopLoop()
                    self.ghostEyeGlowR.destroy()
                    self.ghostEyeGlowR = None
            if self.ghostEyeGlowL:
                self.ghostEyeGlowL.stopLoop()
                self.ghostEyeGlowL.destroy()
                self.ghostEyeGlowL = None
        return

    def doScare(self):
        geom = self.getGeomNode()

        def ghostWorld():
            base.cr.timeOfDayManager.skyGroup.hide()
            render.setColorScale(VBase4(0.5, 0.0, 0.0, 1.0))
            render.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            geom.clearAttrib(ColorBlendAttrib.getClassType())
            geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))

        def normalWorld():
            geom.clearAttrib(ColorBlendAttrib.getClassType())
            render.clearAttrib(ColorBlendAttrib.getClassType())
            render.clearColorScale()
            base.cr.timeOfDayManager.skyGroup.show()

        def zombieAnim():
            pass

        self.stopGhost()
        orgFov = base.camLens.getFov() * 1.0
        crazyFov = orgFov * 1.8
        self.scareIval = Parallel(Sequence(LerpFunctionInterval(self.setCamFov, fromData=orgFov, toData=crazyFov, duration=2.0, blendType='easeOut'), Func(self.setCamFov, orgFov)), Sequence(Func(ghostWorld), Func(zombieAnim), Wait(2.0), Func(normalWorld), Func(self.startGhost)))
        self.scareIval.start()

    def getCurrentWeapon(self):
        return (
         self.currentWeaponId, self.isWeaponDrawn)

    def setCurrentWeapon(self, currentWeaponId, isWeaponDrawn):
        self.checkWeaponSwitch(currentWeaponId, isWeaponDrawn)
        weaponIds = base.localAvatar.equippedWeapons

    def setSecondWeapon(self, weapon):
        if weapon == self.secondWeapon:
            return
        if self.secondWeapon:
            self.secondWeapon.removeNode()
        if not self.isNpc and self.currentWeapon and self.currentWeapon.getParent() == self.leftHandNode:
            self.currentWeapon.reparentTo(self.rightHandNode)
        self.secondWeapon = weapon

    def checkWeaponSwitch(self, currentWeaponId, isWeaponDrawn):
        yieldThread('setCurrentWeapon begin')
        if isWeaponDrawn == self.isWeaponDrawn and currentWeaponId == self.currentWeaponId:
            return
        if isWeaponDrawn and not self.isWeaponDrawn:
            self.isWeaponDrawn = isWeaponDrawn
            self.currentWeaponId = currentWeaponId
            self.__initWeaponChange()
            self.__doDrawWeapon()
            self.__endWeaponChange()
        elif isWeaponDrawn and self.isWeaponDrawn and currentWeaponId != self.currentWeaponId:
            self.__initWeaponChange()
            self.__doPutAwayWeapon()
            self.isWeaponDrawn = isWeaponDrawn
            self.currentWeaponId = currentWeaponId
            self.__doDrawWeapon()
            self.__endWeaponChange()
        elif not isWeaponDrawn and self.isWeaponDrawn:
            self.isWeaponDrawn = isWeaponDrawn
            self.currentWeaponId = currentWeaponId
            self.__initWeaponChange()
            self.__doPutAwayWeapon()
            self.__endWeaponChange()
        else:
            self.currentWeaponId = currentWeaponId

    def __initWeaponChange(self):
        if self.isLocal():
            if hasattr(self.cr, 'targetMgr') and self.cr.targetMgr:
                self.cr.targetMgr.stopFollowAim()
        if self.setWeaponIval:
            self.setWeaponIval.finish()
            self.setWeaponIval = None
        self.setWeaponIval = Sequence()
        if self.isLocal():
            self.setWeaponIval.append(Func(messenger.send, 'drawStarted'))
        return

    def __endWeaponChange(self):
        if self.isLocal():
            self.setWeaponIval.append(Func(messenger.send, 'drawFinished'))
        self.setWeaponIval.start()
        if self.isNpc:
            if self.currentWeaponId:
                rep = WeaponGlobals.getRepId(self.currentWeaponId)
                if rep == InventoryType.DollRep:
                    if self.isWeaponDrawn:
                        self.showVoodooDollAttuned()
                    else:
                        self.showVoodooDollUnattuned()

    def __doPutAwayWeapon(self):
        if self.isLocal():
            taskMgr.remove('usageTask')
            localAvatar.guiMgr.combatTray.ignoreInput()
            localAvatar.guiMgr.combatTray.disableTray()
            localAvatar.stopAllDefenceEffects()
        if self.currentWeapon and not (self.isNpc and self.hp <= 0):
            if localAvatar.getStyle().getTutorial() > 1:
                ival = self.putAwayCurrentWeapon(blendInT=0.3, blendOutT=0)
                if ival:
                    self.setWeaponIval.append(ival)
                    self.setWeaponIval.append(Func(self.currentWeapon.delete))
            else:
                self.currentWeapon.detachFrom(localAvatar)
                self.currentWeapon.delete

    def __doDrawWeapon(self):
        weaponClass = WeaponGlobals.getWeaponClass(self.currentWeaponId)
        if weaponClass:
            self.currentWeapon = weaponClass(self.currentWeaponId)
            if ItemGlobals.getSubtype(self.currentWeaponId) == ItemGlobals.MUSKET:
                bayonetPart = self.currentWeapon.find('**/bayonet')
                if bayonetPart:
                    bayonetPart.stash()
            if not self.isLocal() and ItemGlobals.getType(self.currentWeaponId) == ItemGlobals.FISHING:
                self.currentWeapon.setR(-90)
            ammoSkillId = 0
            if self.currentWeaponId == ItemGlobals.GRENADE_POUCH:
                if self.currentAmmo:
                    ammoSkillId = self.currentAmmo
            ival = self.pullOutCurrentWeapon(ammoSkillId=ammoSkillId, blendInT=0, blendOutT=0.3)
            if ival:
                self.setWeaponIval.append(ival)
            if self.isLocal():
                if hasattr(self.cr, 'targetMgr'):
                    self.setWeaponIval.append(Func(self.cr.targetMgr.startFollowAim))
                if self.currentWeaponId:
                    rep = WeaponGlobals.getRepId(self.currentWeaponId)
                    self.setWeaponIval.append(Func(localAvatar.guiMgr.combatTray.initCombatTray, rep))

    def showVoodooDollAttuned(self):
        if not self.isNpc:
            return
        if not self.attuneEffect:
            self.attuneEffect = VoodooAura.getEffect()
        if self.attuneEffect:
            self.attuneEffect.reparentTo(self.rightHandNode)
            self.attuneEffect.setPos(0, 0, 0)
            self.attuneEffect.particleDummy.reparentTo(self.rightHandNode)
            self.attuneEffect.setEffectColor(Vec4(0.2, 0.1, 0.5, 1))
            self.attuneEffect.startLoop()

    def showVoodooDollUnattuned(self):
        if not self.isNpc:
            return
        if self.attuneEffect:
            self.attuneEffect.stopLoop()
            self.attuneEffect = None
        return

    def isCurrentWeapon(self, weaponId):
        if self.currentWeaponId:
            return self.currentWeaponId == weaponId
        return 0

    def getCurrentAmmo(self):
        return self.currentAmmo

    def setCurrentAmmo(self, currentAmmo, init=0):
        if currentAmmo == self.currentAmmo and not init:
            return
        oldCurrentAmmo = self.currentAmmo
        self.currentAmmo = currentAmmo
        if hasattr(self, 'undead') and self.undead:
            self.skeleton.currentAmmo = self.currentAmmo
        if self.isNpc:
            self.currentAmmo = currentAmmo
            if hasattr(self, 'undead') and self.undead:
                self.skeleton.currentAmmo = self.currentAmmo
        if self.currentWeapon:
            if self.setWeaponIval:
                self.setWeaponIval.finish()
                self.setWeaponIval = None
            self.setWeaponIval = Sequence()
            ival = self.changeAmmunition()
            if ival:
                self.setWeaponIval.append(ival)
            self.setWeaponIval.start()
        return

    def getCurrentCharm(self):
        return self.currentCharm

    def setCurrentCharm(self, currentCharm):
        self.currentCharm = currentCharm

    def pullOutCurrentWeapon(self, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        self.setWalkForWeapon()
        if hasattr(self, 'undead') and self.undead:
            drawIval = self.currentWeapon.getDrawIval(self.skeleton, ammoSkillId, blendInT, blendOutT)
        else:
            drawIval = self.currentWeapon.getDrawIval(self, ammoSkillId, blendInT, blendOutT)
        return drawIval

    def putAwayCurrentWeapon(self, blendInT=0.1, blendOutT=0.1):
        if hasattr(self, 'undead') and self.undead:
            returnIval = self.currentWeapon.getReturnIval(self.skeleton, blendInT, blendOutT)
        else:
            returnIval = self.currentWeapon.getReturnIval(self, blendInT, blendOutT)
        return returnIval

    def changeAmmunition(self):
        if hasattr(self, 'undead') and self.undead:
            returnIval = self.currentWeapon.getAmmoChangeIval(self.skeleton, 0, self.currentAmmo, 0, None)
        else:
            returnIval = self.currentWeapon.getAmmoChangeIval(self, 0, self.currentAmmo, 0, None)
        return returnIval

    def setWalkForWeapon(self):
        if self.currentWeapon:
            walkAnim, runAnim, reverseAnim, neutralAnim, strafeLeftAnim, strafeRightAnim, strafeDiagLeftAnim, strafeDiagRightAnim, strafeRevDiagLeftAnim, strafeRevDiagRightAnim, fallGroundAnim, fallWaterAnim, spinLeftAnim, spinRightAnim = self.currentWeapon.getWalkForWeapon(self)
            self.motionFSM.setAnimInfo(((neutralAnim, 1.0), (walkAnim, 1.5), (runAnim, 1.0), (reverseAnim, -1.5), (strafeLeftAnim, 1.0), (strafeRightAnim, 1.0), (strafeDiagLeftAnim, 1.0), (strafeDiagRightAnim, 1.0), (strafeRevDiagLeftAnim, 1.0), (strafeRevDiagRightAnim, 1.0), (fallGroundAnim, 1.0), (fallWaterAnim, -1.0), (spinLeftAnim, 1.0), (spinRightAnim, 1.0)))

    def getSkillQuantity(self, skillId):
        inv = self.getInventory()
        if inv:
            return inv.getStackQuantity(skillId)
        else:
            return 0

    def getAmmoQuantity(self, ammoInvId):
        inv = self.getInventory()
        if inv:
            return inv.getStackQuantity(ammoInvId)
        else:
            return 0

    def useTargetedSkill(self, skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, itemEffects, timestamp, pos, charge=0, localSignal=0):
        DistributedReputationAvatar.useTargetedSkill(self, skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, itemEffects, timestamp, pos, charge, localSignal)
        WeaponBase.useTargetedSkill(self, skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, itemEffects, timestamp, pos, charge)

    def useProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, charge):
        WeaponBase.useProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, charge)
        if not self.isLocal():
            self.playSkillMovie(skillId, ammoSkillId, WeaponGlobals.RESULT_DELAY, charge)

    def packMultiHitEffects(self, targetEffects, numHits):
        if numHits <= 1:
            return targetEffects
        divDamage = int(targetEffects[0] / numHits + 1)
        multiHitEffects = []
        multiHitEffects.append(list(targetEffects))
        multiHitEffects[0][0] = divDamage
        for i in range(numHits - 2):
            multiHitEffects.append([divDamage, 0, 0, 0, 0])

        multiHitEffects.append([targetEffects[0] - divDamage * (numHits - 1), 0, 0, 0, 0])
        return multiHitEffects

    def toonUp(self, hpGained):
        if self.hp == None or hpGained < 0:
            return
        if hpGained > 0:
            self.showHpText(hpGained)
            self.hpChange(quietly=0)
        return

    def mojoUp(self, mojoGained):
        if self.mojo == None or mojoGained < 0:
            return
        if self.mojo + mojoGained > self.maxMojo:
            mojoGained = self.maxMojo - self.mojo
        if mojoGained > 0:
            self.showHpText(mojoGained, bonus=10)
        return

    def takeDamage(self, hpLost, pos, bonus=0, itemEffects=[]):
        if self.hp == None or hpLost < 0:
            return
        if hpLost > 0:
            self.showHpText(-hpLost, pos, bonus, itemEffects=itemEffects)
            self.hpChange(quietly=0)
        return

    def takeMpDamage(self, mpLost, pos, bonus=3):
        if self.mojo == None or mpLost < 0 or self.mojo <= 0:
            return
        self.refreshStatusTray()
        if self.mojo < mpLost:
            mpLost = self.mojo
        if mpLost > 0:
            self.showHpText(-mpLost, pos, bonus)
        return

    def playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, itemEffects=[], multihit=0, targetBonus=0, skillResult=0):
        if self.isDisabled():
            return
        DistributedReputationAvatar.playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, multihit=multihit, targetBonus=targetBonus, skillResult=skillResult)
        targetHp, targetPower, targetEffect, targetMojo, targetSwiftness = targetEffects
        if self.PlayersInvulnerable and targetHp < 0 and not self.isNpc:
            pass
        else:
            if targetHp < 0:
                self.takeDamage(-targetHp, pos, bonus=targetEffects[1], itemEffects=itemEffects)
            elif targetHp > 0:
                self.toonUp(targetHp)
            if targetMojo < 0 and not attacker == self:
                taskMgr.doMethodLater(WeaponGlobals.MP_DAMAGE_DELAY, self.takeMpDamage, self.taskName('playMpDamage'), extraArgs=[-targetMojo, pos])
            elif targetMojo > 0:
                self.mojoUp(targetMojo)
            messenger.send('pistolHitTarget')

    def playSkillMovie(self, skillId, ammoSkillId, skillResult, charge, targetId=0, areaIdList=[]):
        self.cleanupOuchIval()
        skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
        if not skillInfo:
            return

        anim = skillInfo[WeaponGlobals.PLAYABLE_INDEX]
        if self.curAttackAnim:
            if self.curAttackAnim.isPlaying() and WeaponGlobals.getIsInstantSkill(skillId, ammoSkillId):
                return
            else:
                self.curAttackAnim.pause()
                self.curAttackAnim = None

        if self.secondWeapon:
            self.secondWeapon.removeNode()
            self.secondWeapon = None

        timestamp = globalClockDelta.getFrameNetworkTime()
        self.currentAttack = [skillId, ammoSkillId, timestamp]
        self.refreshStatusTray()
        target = self.cr.doId2do.get(targetId)
        if WeaponGlobals.getIsAreaAnimSkill(skillId):
            areaList = []
            for areaId in areaIdList:
                if id == targetId:
                    continue
                area = self.cr.doId2do.get(areaId)
                if area:
                    areaList.append(area)

            self.curAttackAnim = getattr(self.cr.combatAnims, anim)(self, skillId, ammoSkillId, charge, target, skillResult, areaList)
        else:
            self.curAttackAnim = getattr(self.cr.combatAnims, anim)(self, skillId, ammoSkillId, charge, target, skillResult)

        if localAvatar.duringDialog:
            self.curAttackAnim = None

        self.preprocessAttackAnim()
        if self.curAttackAnim != None:
            self.curAttackAnim.start()

        if not self.isLocal():
            if WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.DEFENSE_SKILL_INDEX:
                newZ = self.getZ(localAvatar)
                pos = Vec3(0, 0, newZ + self.height * 0.666)
                if skillId == EnemySkills.EnemySkills.MISC_VOODOO_REFLECT:
                    self.showEffectString(PLocalizer.AttackReflected)
                else:
                    self.showEffectString(PLocalizer.AttackBlocked)

    def preprocessAttackAnim(self):
        pass

    def cleanupOuchIval(self):
        DistributedReputationAvatar.cleanupOuchIval(self)
        if self.ouchAnim != None:
            self.ouchAnim.finish()
            self.ouchAnim = None
        return

    def getFadeInTrack(self):
        parent = self.getParentObj()
        if not parent:
            return None
        dclassName = parent.dclass.getName()
        if dclassName == 'DistributedGAInterior':
            return None
        if self.getNameText():
            fadeInIval = Sequence(Func(self.setTransparency, TransparencyAttrib.MAlpha), Func(self.setAlphaScale, 0.0), Func(self.getNameText().setAlphaScale, 0.0), Parallel(LerpFunctionInterval(self.setAlphaScale, 1.0, fromData=0.0, toData=1.0), LerpFunctionInterval(self.getNameText().setAlphaScale, 1.0, fromData=0.0, toData=1.0)), Func(self.clearTransparency), Func(self.clearColorScale), Func(self.getNameText().clearColorScale))
        else:
            fadeInIval = Sequence(Func(self.setTransparency, TransparencyAttrib.MAlpha), Func(self.setAlphaScale, 0.0), LerpFunctionInterval(self.setAlphaScale, 1.0, fromData=0.0, toData=1.0), Func(self.clearTransparency), Func(self.clearColorScale))
        return fadeInIval

    def getSpawnTrack(self):
        avatarTeam = self.getTeam()
        if avatarTeam in [PiratesGlobals.UNDEAD_TEAM, PiratesGlobals.FRENCH_UNDEAD_TEAM, PiratesGlobals.SPANISH_UNDEAD_TEAM] and not self.avatarType.isA(AvatarTypes.Ghost):

            def startSFX():
                sfx = self.getSfx('spawn')
                if sfx:
                    base.playSfx(sfx, node=self, cutoff=100)

            def startVFX():
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effectScale = EnemyGlobals.getEffectScale(self)
                    spawnEffect = JRSpawn.getEffect()
                    if spawnEffect:
                        spawnEffect.reparentTo(render)
                        spawnEffect.setPos(self.getPos(render))
                        spawnEffect.setScale(effectScale)
                        spawnEffect.play()
                    portal = DarkPortal.getEffect()
                    if portal:
                        portal.reparentTo(render)
                        portal.setPos(self.getPos(render))
                        portal.size = effectScale * 10.0
                        portal.holdTime = 3.0
                        portal.play()

            if self.getAnimControl('intro'):
                duration = self.getDuration('intro')
                introIval = Parallel(Func(self.hide), self.actorInterval('intro'), Sequence(Wait(0.25), Func(self.show)))
            else:
                duration = 1.5
                scaleUp = LerpFunctionInterval(self.setAvatarScale, 2.0, fromData=0.1, toData=self.getAvatarScale())
                fadeIn = LerpFunctionInterval(self.setAlphaScale, 2.0, fromData=0.0, toData=1.0)
                introIval = Sequence(Func(self.setTransparency, 1), Parallel(scaleUp, fadeIn), Func(self.clearTransparency), Func(self.clearColorScale))
            if self.isInInvasion():
                spawnIval = Sequence(Func(startSFX), introIval)
            else:
                spawnIval = Sequence(Func(startSFX), Func(startVFX), introIval)
            spawnIval.append(Func(self.ambushIntroDone))
            return spawnIval
        else:
            if self.getAnimControl('intro'):
                introIval = self.actorInterval('intro')
            else:
                fadeIn = LerpFunctionInterval(self.setAlphaScale, 2.0, fromData=0.0, toData=1.0)
                introIval = Sequence(Func(self.setTransparency, 1), fadeIn, Func(self.clearTransparency), Func(self.clearColorScale))
            introIval.append(Func(self.ambushIntroDone))
            return introIval

    def getGetupTrack(self):
        return None

    def getDyingTrack(self):
        return None

    def getDeathTrack(self):
        av = self
        if hasattr(self, 'creature') and self.creature:
            av = self.creature
        animName = av.getDeathAnimName()
        duration = av.getDuration(animName)
        frames = av.getNumFrames(animName)
        if duration is None or frames is None:
            base.cr.centralLogger.writeClientEvent('Invalid Death: %s,%s' % (self, animName))
            return Sequence()
        from pirates.pirate.Biped import Biped
        if isinstance(self, Biped):
            delay = {'death': 0.8,'death2': 1.2,'death3': 1.8,'death4': 1.6}.get(animName, 1.0)
        else:
            delay = 0.0

        def startSFX():
            sfx = self.getSfx('death')
            if sfx:
                base.playSfx(sfx, node=self, cutoff=60)

        def stopSmooth():
            if self.smoothStarted:
                taskName = self.taskName('smooth')
                taskMgr.remove(taskName)
                self.smoothStarted = 0

        avatarTeam = self.getTeam()
        if avatarTeam in [PiratesGlobals.UNDEAD_TEAM, PiratesGlobals.FRENCH_UNDEAD_TEAM, PiratesGlobals.SPANISH_UNDEAD_TEAM] and not self.avatarType.isA(AvatarTypes.Ghost):

            def startVFX():
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                    effectScale = EnemyGlobals.getEffectScale(self)
                    offset = EnemyGlobals.getEffectOffset(self)
                    root = av.headNode
                    if root.isEmpty():
                        root = av
                    deathEffect = JRDeath.getEffect()
                    if deathEffect:
                        deathEffect.reparentTo(render)
                        deathEffect.setPos(root, offset)
                        deathEffect.setScale(effectScale)
                        deathEffect.play()
                    deathBlast = JRDeathBlast.getEffect()
                    if deathBlast:
                        deathBlast.reparentTo(render)
                        deathBlast.setPos(root, offset)
                        deathBlast.setScale(effectScale)
                        deathBlast.play()

            def startGlow():
                geom = av.getGeomNode()
                model = loader.loadModel('models/effects/particleMaps')
                tex = model.find('**/effectWindBlur').findAllTextures()[0]
                geom.setTransparency(1)
                geom.setTexture(tex, 100)
                geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                geom.setColorScale(VBase4(0.8, 1, 0.1, 1))
                self.animNode = NodePath('animNode')
                anim = LerpPosInterval(self.animNode, startPos=VBase3(0, 0, 0), pos=VBase3(0.0, -5.0, 0.0), duration=5.0)
                geom.setTexProjector(geom.findAllTextureStages()[0], self.animNode, NodePath())
                anim.start()

            deathIval = Parallel()
            deathIval.append(Sequence(Wait(delay), Func(startSFX), Func(startGlow)))
            deathIval.append(Sequence(Func(stopSmooth), Func(av.disableMixing), av.actorInterval(animName, startFrame=0.0, endFrame=frames - 1.0, blendOutT=0.0, blendInT=0.0), Func(av.pose, animName, frames - 2, blendT=0.0), Func(av.setTransparency, 1), Func(startVFX), LerpColorScaleInterval(self, 1.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(1.0, 1.0, 1.0, 1.0)), Func(av.nametag3d.reparentTo, av), Func(self.hide, 0, PiratesGlobals.INVIS_DEATH), Func(av.clearColorScale), Func(av.clearTransparency)))
        else:
            deathIval = Parallel(Func(stopSmooth), Func(self.setTransparency, 1), av.actorInterval(animName, blendOutT=0.0), Sequence(Wait(duration / 2.0), Func(self.stopGhost, 0), LerpColorScaleInterval(av, duration / 2.0, Vec4(1, 1, 1, 0), startColorScale=Vec4(1)), Func(self.hide, 0, PiratesGlobals.INVIS_DEATH), Func(self.clearColorScale), Func(self.clearTransparency)), Sequence(Wait(delay), Func(startSFX)))
        return deathIval

    def ambushIntroDone(self):
        if hasattr(self, 'ambushEnemy'):
            self.sendUpdate('ambushIntroDone')

    def b_setGameState(self, gameState, localArgs=[]):
        timestamp = globalClockDelta.getFrameNetworkTime()
        state = self.getGameState()
        self.setGameState(gameState, timestamp, localArgs, localChange=1)
        if state != self.getGameState():
            self.d_setGameState(gameState, timestamp)

    def d_setGameState(self, gameState, timestamp):
        self.sendUpdate('setGameState', [gameState, timestamp])

    @report(types=['frameCount', 'args'], dConfigParam='jail')
    def setGameState(self, gameState, timestamp=None, localArgs=[], localChange=0):
        self.notify.debug('setGameState: %s state: %s' % (self.doId, gameState))
        if timestamp is None:
            ts = 0.0
        else:
            ts = globalClockDelta.localElapsedTime(timestamp)
        if self.gameFSM and not self.gameFSM.isInTransition():
            if self.gameFSM.getCurrentOrNextState() != gameState and gameState != '':
                self.gameFSM.request(gameState, [ts] + localArgs)
        return

    def getGameState(self):
        return self.gameFSM.getCurrentOrNextState()

    @report(types=['args', 'deltaStamp'], dConfigParam=['jump'])
    def b_setAirborneState(self, airborneState):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.setAirborneStateLocal(airborneState, timestamp)
        self.d_setAirborneState(airborneState, timestamp)

    @report(types=['args', 'deltaStamp'], dConfigParam=['jump'])
    def d_setAirborneState(self, airborneState, timestamp):
        self.sendUpdate('setAirborneState', [airborneState, timestamp])

    @report(types=['args', 'deltaStamp'], dConfigParam=['jump'])
    def setAirborneStateLocal(self, airborneState, timestamp):
        self.motionFSM.motionAnimFSM.setAirborneState(airborneState)

    @report(types=['args', 'deltaStamp'], dConfigParam=['jump'])
    def setAirborneState(self, airborneState, timestamp):
        wait = self.smoother.getDelay() - globalClockDelta.localElapsedTime(timestamp)

        def wrap():
            self.motionFSM.motionAnimFSM.setAirborneState(airborneState)
            self.motionFSM.motionAnimFSM.updateAnimState(self.smoother.getSmoothForwardVelocity(), self.smoother.getSmoothRotationalVelocity(), self.smoother.getSmoothLateralVelocity())

        taskMgr.doMethodLater(wait, wrap, self.taskName('playMotionAnim-%s-%d' % (airborneState, timestamp)), [])

    @report(types=['args', 'deltaStamp'], dConfigParam=['jump'])
    def b_playMotionAnim(self, anim):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.d_playMotionAnim(anim, timestamp)
        self.l_playMotionAnim(anim, timestamp)

    @report(types=['args', 'deltaStamp'], dConfigParam=['jump'])
    def d_playMotionAnim(self, anim, timestamp):
        self.sendCurrentPosition()
        self.sendUpdate('playMotionAnim', [anim, timestamp])

    @report(types=['args', 'deltaStamp'], dConfigParam=['jump'])
    def l_playMotionAnim(self, anim, timestamp):
        self.motionFSM.motionAnimFSM.playMotionAnim(anim, local=True)

    @report(types=['args', 'deltaStamp'], dConfigParam=['jump'])
    def playMotionAnim(self, anim, timestamp):
        wait = self.smoother.getDelay() - globalClockDelta.localElapsedTime(timestamp)
        taskMgr.doMethodLater(wait, self.motionFSM.motionAnimFSM.playMotionAnim, self.taskName('playMotionAnim-%s-%d' % (anim, timestamp)), [
         anim, False])

    def b_setGroundState(self, groundState):
        timestamp = globalClockDelta.getFrameNetworkTime()
        self.setGroundStateLocal(groundState, timestamp)
        self.d_setGroundState(groundState, timestamp)

    def d_setGroundState(self, groundState, timestamp):
        self.sendUpdate('setGroundState', [groundState, timestamp])

    def setGroundStateLocal(self, groundState, timestamp):
        self.motionFSM.motionAnimFSM.setGroundState(groundState)

    def setGroundState(self, groundState, timestamp):
        wait = self.smoother.getDelay() - globalClockDelta.localElapsedTime(timestamp)
        if wait > 0:
            taskMgr.doMethodLater(wait, self.motionFSM.motionAnimFSM.setGroundState, self.taskName('playMotionAnim-%s-%d' % (groundState, timestamp)), [
             groundState])

    def getSwimTaskName(self):
        return self.taskName('swimBobTask')

    def startBobSwimTask(self):
        swimTaskName = self.getSwimTaskName()
        task = taskMgr.add(self.bobTask, swimTaskName, priority=35)
        task.zPosTime = PiratesGlobals.SWIM_WALK_TRANSITION_TIME
        task.zStart = self.getZ(render)
        self.bobbing = True

    def bobTask(self, task):
        world = self.cr.getActiveWorld()
        if world:
            water = world.getWater()
        else:
            water = None
        if self.cr.wantSeapatch and water:
            zWater, normal = water.calcHeightAndNormal(node=self)
        else:
            zWater = 0.0
            normal = Vec3(0, 0, 1)
        if self.bobbing:
            zWater = lerp(task.zStart, zWater, clampScalar(0.0, 1.0, task.time / task.zPosTime))
            if task.time >= task.zPosTime:
                self.bobbing = False
        self.setZ(render, zWater)
        geom = self.getGeomNode()
        geom.setP(render, normal[1] * 90)
        return task.cont

    def stopBobSwimTask(self):
        swimTaskName = self.getSwimTaskName()
        taskMgr.remove(swimTaskName)
        self.bobbing = False
        geom = self.getGeomNode()
        geom.setP(0)
        geom.setR(0)

    def getTotalHp(self):
        if self.hp is None:
            return 0

        return self.hp

    def hpChange(self, quietly=0):
        pass

    def setMaxHp(self, hp):
        DistributedReputationAvatar.setMaxHp(self, hp)
        self.refreshStatusTray()

    def setHp(self, hp, quietly=0):
        justRanOutOfHp = hp is not None and self.hp is not None and self.hp - hp > 0 and hp <= 0
        self.hp = hp
        self.refreshStatusTray()
        localAvatar.guiMgr.attuneSelection.update()
        self.hpChange(quietly=1)
        if justRanOutOfHp:
            self.died()

    def getTotalLuck(self):
        return self.luck + self.luckMod

    def getLuck(self):
        return self.luck

    def setLuck(self, luck):
        self.luck = luck

    def setLuckMod(self, luck):
        self.luckMod = luck

    def getMaxLuck(self):
        return self.maxLuck

    def setMaxLuck(self, maxLuck):
        self.maxLuck = maxLuck

    def getTotalPower(self):
        return self.power + self.powerMod

    def getPower(self):
        return self.power

    def setPower(self, power):
        self.power = power

    def setPowerMod(self, power):
        self.notify.debug('setPowerMod %s' % power)
        self.powerMod = power

    def setMaxPower(self, maxPower):
        self.maxPower = maxPower

    def getTotalMojo(self):
        return self.mojo + self.mojoMod

    def setMojo(self, mojo):
        self.mojo = mojo
        self.refreshStatusTray()
        base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTrayStates()

    def setMojoMod(self, mojo):
        self.mojoMod = mojo
        self.refreshStatusTray()
        base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTrayStates()

    def setMaxMojo(self, maxMojo):
        self.maxMojo = maxMojo
        self.refreshStatusTray()

    def getMaxMojo(self):
        return self.maxMojo

    def getMojo(self):
        return self.mojo

    def getTotalSwiftness(self):
        return self.swiftness + self.swiftnessMod

    def setSwiftness(self, swiftness):
        self.swiftness = swiftness

    def setSwiftnessMod(self, swiftness):
        self.notify.debug('setSwiftnessMod %s' % swiftness)
        self.swiftnessMod = swiftness

    def setStunMod(self, stun):
        self.notify.debug('setStunMod %s' % stun)
        self.stunMod = stun

    def setHasteMod(self, haste):
        self.notify.debug('setHasteMod %s' % haste)
        self.hasteMod += haste

    def setAimMod(self, stun):
        self.notify.debug('setAimMod %s' % stun)
        self.aimMod = stun

    def setTireMod(self, tire):
        self.tireMod = tire

    def attackTire(self, seconds=3.0):
        pass

    def setMaxSwiftness(self, maxSwiftness):
        self.maxSwiftness = maxSwiftness

    def getCombo(self):
        return (
         self.combo, self.isTeamCombo, self.comboDamage)

    def setCombo(self, combo, teamCombo, comboDamage, attackerId=0):
        DistributedReputationAvatar.setCombo(self, combo, teamCombo, comboDamage, attackerId=attackerId)
        if attackerId == base.localAvatar.getDoId():
            return
        self.combo = combo
        if teamCombo:
            self.isTeamCombo = teamCombo
        self.comboDamage = comboDamage
        if base.localAvatar.currentTarget == self:
            messenger.send('trackCombo', [self.combo, self.isTeamCombo, self.comboDamage])

    def resetComboLevel(self, args=None):
        DistributedReputationAvatar.resetComboLevel(self, args)
        self.isTeamCombo = 0
        self.setCombo(0, 0, 0)
        self.comboAttackers = {}

    def isDeathPenaltyActive(self):
        inv = self.getInventory()
        if not inv:
            return False
        ptLoss = inv.getStackQuantity(InventoryType.Vitae_Level)
        if ptLoss > 0:
            return True
        else:
            return False

    def getSkills(self, weaponId):
        if self.getInventory() is None:
            self.notify.warning('Inventory not created yet!')
            return {}
        return self.getInventory().getSkills(weaponId)

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

    def findAllBuffCopyKeys(self, effectId):
        buffCopies = []
        for buffKeyId in self.skillEffects.keys():
            if self.skillEffects[buffKeyId][0] == effectId:
                buffCopies.append(buffKeyId)

        return buffCopies

    def getSkillEffects(self):
        buffIds = []
        for buffKeyId in self.skillEffects.keys():
            buffId = self.skillEffects[buffKeyId][0]
            if buffId not in buffIds:
                buffIds.append(buffId)

        return buffIds

    def addStatusEffect(self, effectId, attackerId, duration, timeLeft, timestamp, buffData):
        if effectId == WeaponGlobals.C_BLIND:
            self._addBlindEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_DIRT:
            self._addDirtEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_POISON:
            self._addPoisonEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_ACID:
            self._addAcidEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_WOUND:
            self._addWoundEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_TAUNT:
            self._addTauntEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_ON_FIRE:
            self._addOnFireEffect(attackerId, timeLeft)
            if self.fireEffect:
                self.fireEffect.setDefaultColor()
        elif effectId == WeaponGlobals.C_ON_CURSED_FIRE:
            self._addOnFireEffect(attackerId, timeLeft)
            if self.fireEffect:
                self.fireEffect.setCursedColor()
        elif effectId == WeaponGlobals.C_SLOW:
            self._addSlowEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_STUN:
            if self.getGameState() not in ('Injured', ):
                self._addStunEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_HOLD:
            self._addHoldEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_ATTUNE:
            self._addAttuneEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_VOODOO_STUN:
            self._addVoodooStunEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_VOODOO_HEX_STUN:
            self._addVoodooHexStunEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_INTERRUPTED:
            self._addInterruptedEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_OPENFIRE:
            self._addOpenFireEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_TAKECOVER:
            self._addTakeCoverEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_TOXIN:
            self._addToxinEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_FREEZE:
            self._addFreezeEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_MONKEY_PANIC:
            self._addMonkeyPanicEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_MASTERS_RIPOSTE:
            self._addMastersRiposteEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_QUICKLOAD:
            self._addQuickloadEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_REGEN:
            self._addRegenEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_FURY:
            self._addFuryEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_MELEE_SHIELD:
            self._addMeleeShieldEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_MISSILE_SHIELD:
            self._addMissileShieldEffect(attackerId, timeLeft)
        elif effectId == WeaponGlobals.C_MAGIC_SHIELD:
            self._addMagicShieldEffect(attackerId, timeLeft)
        elif base.config.GetBool('want-potion-game', 0) and PotionGlobals.getIsPotionBuff(effectId):
            if not self.potionStatusEffectManager:
                self.enablePotionFx()
            self.potionStatusEffectManager.addStatusEffect(effectId, attackerId, duration, timeLeft, timestamp, buffData)
        elif effectId == WeaponGlobals.C_DARK_CURSE:
            self.setGhostColor(2)
            self.startGhost(1)
        elif effectId == WeaponGlobals.C_GHOST_FORM:
            self.setGhostColor(3)
            self.startGhost(1)
        elif effectId == WeaponGlobals.C_SPAWN:
            self.playSpawnEffect()

    def playSpawnEffect(self):
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow and base.launcher.getPhaseComplete(3):
            self.protectionEffect = ProtectionDome.getEffect()
            if self.protectionEffect:
                self.protectionEffect.reparentTo(self)
                self.protectionEffect.setScale(0.5)
                self.protectionEffect.setZ(1.0)
                self.protectionEffect.startLoop()

    def stopSpawnEffect(self):
        if self.protectionEffect:
            self.protectionEffect.stopLoop()

    def removeStatusEffect(self, effectId, attackerId):
        if effectId == WeaponGlobals.C_ATTUNE:
            self._removeAttuneEffect()
        if self.findAllBuffCopyKeys(effectId):
            return
        if effectId == WeaponGlobals.C_BLIND:
            self._removeBlindEffect()
        elif effectId == WeaponGlobals.C_DIRT:
            self._removeDirtEffect()
        elif effectId == WeaponGlobals.C_POISON:
            self._removePoisonEffect()
        elif effectId == WeaponGlobals.C_ACID:
            self._removeAcidEffect()
        elif effectId == WeaponGlobals.C_WOUND:
            self._removeWoundEffect()
        elif effectId == WeaponGlobals.C_TAUNT:
            self._removeTauntEffect()
        elif effectId == WeaponGlobals.C_ON_FIRE:
            self._removeOnFireEffect()
        elif effectId == WeaponGlobals.C_ON_CURSED_FIRE:
            self._removeOnFireEffect()
        elif effectId == WeaponGlobals.C_SLOW:
            self._removeSlowEffect()
        elif effectId == WeaponGlobals.C_STUN:
            self._removeStunEffect()
        elif effectId == WeaponGlobals.C_HOLD:
            self._removeHoldEffect()
        elif effectId == WeaponGlobals.C_VOODOO_STUN:
            self._removeVoodooStunEffect()
        elif effectId == WeaponGlobals.C_VOODOO_HEX_STUN:
            self._removeVoodooHexStunEffect()
        elif effectId == WeaponGlobals.C_OPENFIRE:
            self._removeOpenFireEffect()
        elif effectId == WeaponGlobals.C_TAKECOVER:
            self._removeTakeCoverEffect()
        elif effectId == WeaponGlobals.C_TOXIN:
            self._removeToxinEffect()
        elif effectId == WeaponGlobals.C_FREEZE:
            self._removeFreezeEffect()
        elif effectId == WeaponGlobals.C_MONKEY_PANIC:
            self._removeMonkeyPanicEffect()
        elif effectId == WeaponGlobals.C_MASTERS_RIPOSTE:
            self._removeMastersRiposteEffect()
        elif effectId == WeaponGlobals.C_QUICKLOAD:
            self._removeQuickloadEffect()
        elif effectId == WeaponGlobals.C_REGEN:
            self._removeRegenEffect()
        elif effectId == WeaponGlobals.C_FURY:
            self._removeFuryEffect()
        elif effectId in [WeaponGlobals.C_MELEE_SHIELD, WeaponGlobals.C_MISSILE_SHIELD, WeaponGlobals.C_MAGIC_SHIELD]:
            self._removeGhostGuardEffect()
        elif base.config.GetBool('want-potion-game', 0) and PotionGlobals.getIsPotionBuff(effectId):
            if not self.potionStatusEffectManager:
                self.enablePotionFx()
            self.potionStatusEffectManager.removeStatusEffect(effectId, attackerId)
        elif effectId == WeaponGlobals.C_DARK_CURSE:
            self.stopGhost(1)
        elif effectId == WeaponGlobals.C_GHOST_FORM:
            self.stopGhost(1)
        elif effectId == WeaponGlobals.C_SPAWN:
            self.stopSpawnEffect()

    def _addBlindEffect(self, attackerId, duration):
        if self.isLocal():
            self.guiMgr.showSmokePanel()

    def _removeBlindEffect(self):
        if self.isLocal():
            self.guiMgr.hideSmokePanel()

    def _addDirtEffect(self, attackerId, duration):
        if self.isLocal():
            self.guiMgr.showDirtPanel()

    def _removeDirtEffect(self):
        if self.isLocal():
            self.guiMgr.hideDirtPanel()

    def _addPoisonEffect(self, attackerId, duration):
        LerpColorScaleInterval(self.getGeomNode(), 1.0, Vec4(0.7, 1, 0.6, 1), startColorScale=Vec4(1, 1, 1, 1)).start()
        if self.poisonEffect:
            return
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            avatarScale = self.getEnemyScale()
            self.poisonEffect = PoisonEffect.getEffect()
            if self.poisonEffect:
                self.poisonEffect.reparentTo(self)
                self.poisonEffect.setPos(0, 0.75, self.height - 1.5)
                self.poisonEffect.effectScale = avatarScale
                self.poisonEffect.startLoop()

    def _removePoisonEffect(self, cleanup=False):
        if not cleanup:
            LerpColorScaleInterval(self.getGeomNode(), 1.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(0.7, 1.0, 0.6, 1)).start()
        if self.poisonEffect:
            self.poisonEffect.stopLoop()
            self.poisonEffect = None
        return

    def _addToxinEffect(self, attackerId, duration):
        LerpColorScaleInterval(self.getGeomNode(), 1.0, Vec4(0.8, 0.85, 1, 1), startColorScale=Vec4(1, 1, 1, 1)).start()
        if self.toxinEffect:
            return
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
            avatarScale = self.getEnemyScale()
            self.toxinEffect = ToxinEffect.getEffect()
            if self.toxinEffect:
                self.toxinEffect.reparentTo(self)
                self.toxinEffect.setPos(0, 0.75, self.height - 1.5)
                self.toxinEffect.effectScale = avatarScale
                self.toxinEffect.startLoop()

    def _removeToxinEffect(self, cleanup=False):
        if not cleanup:
            LerpColorScaleInterval(self.getGeomNode(), 1.0, Vec4(1, 1, 1, 1)).start()
        if self.toxinEffect:
            self.toxinEffect.stopLoop()
            self.toxinEffect = None
        return

    def _addAcidEffect(self, attackerId, duration):
        self.smokeWispEffect = SmokeWisps.getEffect()
        if self.smokeWispEffect:
            self.smokeWispEffect.reparentTo(self)
            self.smokeWispEffect.setPos(0, 0, self.height)
            self.smokeWispEffect.startLoop()

    def _removeAcidEffect(self):
        if self.smokeWispEffect:
            self.smokeWispEffect.stopLoop()
            self.smokeWispEffect = None
        return

    def _addFreezeEffect(self, attackerId, duration):
        self.frozenCopy = self.getParent().attachNewNode('FrozenCopy')
        geom = self.getGeomNode()
        geom.getChild(0).copyTo(self.frozenCopy)
        geom.getParent().hide()
        self.frozenCopy.setPos(self.getPos())
        self.frozenCopy.setHpr(self, 180, 0, 0)
        self.frozenCopy.setColorScale(0.3, 0.4, 1, 1)
        freezeBlast = FreezeBlast.getEffect()
        if freezeBlast:
            freezeBlast.reparentTo(self.frozenCopy)
            freezeBlast.setPos(0, 0, self.getHeight() / 2.0)
            freezeBlast.setScale(1, 1, max(1, self.getHeight() / 3.0))
            freezeBlast.play()

    def _removeFreezeEffect(self):
        self.frozenCopy.removeNode()
        self.getGeomNode().getParent().show()

    def _addWoundEffect(self, attackerId, duration):
        pass

    def _removeWoundEffect(self):
        pass

    def _addTauntEffect(self, attackerId, duration):
        self.getGeomNode().setColorScale(1.0, 0.4, 0.4, 1)

    def _removeTauntEffect(self):
        self.getGeomNode().setColorScale(1, 1, 1, 1)

    def _addOnFireEffect(self, attackerId, duration):
        if self.fireEffect:
            return
        if self.avatarType.isA(AvatarTypes.Ghost):
            return
        avatarScale = self.getEnemyScale()
        self.fireEffect = Flame.getEffect()
        if self.fireEffect:
            if hasattr(self, 'headNode') and self.headNode:
                self.fireEffect.reparentTo(self.headNode)
                self.fireEffect.setPos(self.headNode, -2, 0, 0)
                self.fireEffect.setHpr(0, 0, 80)
            else:
                self.fireEffect.reparentTo(self)
                self.fireEffect.setPos(0, 0, self.height * 0.8)
            self.fireEffect.effectScale = 0.25 * avatarScale
            self.fireEffect.duration = 4.0
            self.fireEffect.startLoop()
        self.smokeWispEffect = SmokeWisps.getEffect()
        if self.smokeWispEffect:
            self.smokeWispEffect.reparentTo(self)
            self.smokeWispEffect.setPos(0, 0, self.height)
            self.smokeWispEffect.startLoop()

    def _removeOnFireEffect(self):
        if self.fireEffect:
            self.fireEffect.stopLoop()
            self.fireEffect = None
        if self.smokeWispEffect:
            self.smokeWispEffect.stopLoop()
            self.smokeWispEffect = None
        return

    def _addSlowEffect(self, attackerId, duration):
        if self.slowEffect:
            return
        self.slowEffect = SlowEffect.getEffect()
        if self.slowEffect:
            self.slowEffect.duration = 1.75
            self.slowEffect.effectScale = 0.85
            if hasattr(self, 'headNode') and self.headNode:
                self.slowEffect.reparentTo(self.headNode)
                self.slowEffect.setHpr(0, 0, 90)
                self.slowEffect.setPos(self.headNode, 1.5, 0, 0)
            else:
                self.slowEffect.reparentTo(self)
                self.slowEffect.setHpr(self, 0, 0, 0)
                self.slowEffect.setPos(self, 0, 0, self.getHeight() + 1.5)
            self.slowEffect.startLoop()
        self.slowEffect2 = SlowEffect.getEffect()
        if self.slowEffect2:
            self.slowEffect2.duration = 1.75
            self.slowEffect2.effectScale = 0.75
            if hasattr(self, 'headNode') and self.headNode:
                self.slowEffect2.reparentTo(self.headNode)
                self.slowEffect2.setHpr(0, 120, 90)
                self.slowEffect2.setPos(self.headNode, 1.75, 0, 0)
            else:
                self.slowEffect2.reparentTo(self)
                self.slowEffect2.setHpr(self, 120, 0, 0)
                self.slowEffect2.setPos(self, 0, 0, self.getHeight() + 1.25)
            self.slowEffect2.startLoop()

    def _removeSlowEffect(self):
        if self.slowEffect:
            self.slowEffect.stopLoop()
            self.slowEffect = None
        if self.slowEffect2:
            self.slowEffect2.stopLoop()
            self.slowEffect2 = None
        return

    def _addStunEffect(self, attackerId, duration):
        if self.stunEffect:
            return
        self.stunEffect = StunEffect.getEffect()
        if self.stunEffect:
            self.stunEffect.duration = 1.0
            self.stunEffect.direction = 1
            self.stunEffect.effectScale = 0.65
            if hasattr(self, 'headNode') and self.headNode:
                self.stunEffect.reparentTo(self.headNode)
                self.stunEffect.setHpr(0, 0, 90)
                self.stunEffect.setPos(self.headNode, 1, 0, 0)
            else:
                self.stunEffect.reparentTo(self)
                self.stunEffect.setHpr(self, 0, 0, 0)
                self.stunEffect.setPos(self, 0, 0, self.getHeight() + 1)
            self.stunEffect.startLoop()
        self.stunEffect2 = StunEffect.getEffect()
        if self.stunEffect2:
            self.stunEffect2.duration = 1.0
            self.stunEffect2.direction = -1
            self.stunEffect2.effectScale = 0.5
            if hasattr(self, 'headNode') and self.headNode:
                self.stunEffect2.reparentTo(self.headNode)
                self.stunEffect2.setHpr(0, 120, 90)
                self.stunEffect2.setPos(self.headNode, 1.25, 0, 0)
            else:
                self.stunEffect2.reparentTo(self)
                self.stunEffect2.setHpr(self, 120, 0, 0)
                self.stunEffect2.setPos(self, 0, 0, self.getHeight() + 0.9)
            self.stunEffect2.startLoop()

    def _removeStunEffect(self):
        if self.stunEffect:
            self.stunEffect.stopLoop()
            self.stunEffect = None
        if self.stunEffect2:
            self.stunEffect2.stopLoop()
            self.stunEffect2 = None
        if self.isLocal():
            messenger.send('skillFinished')
        return

    def _addHoldEffect(self, attackerId, duration):
        if self.shacklesEffect:
            return
        attacker = self.cr.doId2do.get(attackerId)
        avatarScale = self.getEnemyScale()
        isJollyHold = attacker and attacker.avatarType and attacker.avatarType.isA(AvatarTypes.JollyRoger)
        self.shacklesEffect = GraveShackles.getEffect(unlimited=True)
        if self.shacklesEffect:
            self.shacklesEffect.reparentTo(self)
            self.shacklesEffect.setScale(avatarScale * 1.25)
            if isJollyHold:
                self.shacklesEffect.setColor(Vec4(0.8, 1, 0.2, 1))
            else:
                self.shacklesEffect.setColor(Vec4(1, 1, 1, 1))
            self.shacklesEffect.setPos(0, 0, 0)
            self.shacklesEffect.startLoop()
        if not isJollyHold:
            self.voodooSmokeEffect = AttuneSmoke.getEffect()
            if self.voodooSmokeEffect:
                self.voodooSmokeEffect.reparentTo(self)
                self.voodooSmokeEffect.setPos(0, 0, 0.2)
                self.voodooSmokeEffect.startLoop()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            effect = GroundDirt.getEffect()
            if effect:
                effect.effectScale = avatarScale
                effect.setScale(avatarScale)
                effect.reparentTo(self)
                effect.play()
            cameraShakerEffect = CameraShaker()
            cameraShakerEffect.reparentTo(self)
            cameraShakerEffect.setPos(0, 0, 0)
            cameraShakerEffect.shakeSpeed = 0.08
            cameraShakerEffect.shakePower = 1.5
            cameraShakerEffect.numShakes = 2
            cameraShakerEffect.scalePower = 1
            cameraShakerEffect.play(100.0)

    def _removeHoldEffect(self, cleanup=False):
        if not cleanup:
            effect = GroundDirt.getEffect()
            if effect:
                avatarScale = self.getEnemyScale()
                effect.effectScale = avatarScale / 1.5
                effect.setScale(avatarScale)
                effect.reparentTo(self)
                effect.play()
        if self.voodooSmokeEffect:
            self.voodooSmokeEffect.stopLoop()
            self.voodooSmokeEffect = None
        if self.shacklesEffect:
            self.shacklesEffect.stopLoop()
            self.shacklesEffect = None
        return

    def _addAttuneEffect(self, attackerId, duration):
        attacker = self.cr.doId2do.get(attackerId)
        self.checkAttuneBuffEffect()
        if attacker and attacker.isLocal() and not self.isInvisibleGhost():
            attacker.addStickyTarget(self.doId)

    def _removeAttuneEffect(self):
        self.checkAttuneBuffEffect()

    def _addVoodooStunEffect(self, attackerId, duration):
        self.showVoodooDollUnattuned()
        self.showEffectString(PLocalizer.AttackUnattune)

    def _removeVoodooStunEffect(self):
        if self.currentTarget:
            if self.findAllBuffCopyKeys(WeaponGlobals.C_VOODOO_HEX_STUN):
                return
            self.showVoodooDollAttuned()

    def _addVoodooHexStunEffect(self, attackerId, duration):
        self.showVoodooDollUnattuned()

    def _removeVoodooHexStunEffect(self):
        if self.currentTarget:
            if self.findAllBuffCopyKeys(WeaponGlobals.C_VOODOO_STUN):
                return
            self.showVoodooDollAttuned()

    def _addInterruptedEffect(self, attackerId, duration):
        self.showEffectString(PLocalizer.AttackInterrupt)

    def _removeInterruptedEffect(self):
        pass

    def _addOpenFireEffect(self, attackerId, duration):
        if self.doId == localAvatar.doId:
            if self.crewBuffDisplay:
                self.crewBuffDisplay.stop()
                self.crewBuffDisplay.destroy()
            self.crewBuffDisplay = CrewBuffDisplay(skillIcon=loader.loadModel('models/textureCards/skillIcons').find('**/sail_openfire2'), duration=duration, buffName=PLocalizer.CrewBuffOpenFireString, buffDesc=PLocalizer.CrewBuffOpenFire % int((WeaponGlobals.OPEN_FIRE_BONUS - 1) * 100), parent=base.a2dBottomRight)
            self.crewBuffDisplay.reparentTo(base.a2dBottomRight, sort=-1000)
            self.crewBuffDisplay.play()

    def _removeOpenFireEffect(self):
        if self.crewBuffDisplay:
            self.crewBuffDisplay.stop()
            self.crewBuffDisplay.destroy()
            self.crewBuffDisplay = None
        return

    def _addTakeCoverEffect(self, attackerId, duration):
        if self.doId == localAvatar.doId:
            if self.crewBuffDisplay:
                self.crewBuffDisplay.stop()
                self.crewBuffDisplay.destroy()
            self.crewBuffDisplay = CrewBuffDisplay(skillIcon=loader.loadModel('models/textureCards/skillIcons').find('**/sail_take_cover'), duration=duration, buffName=PLocalizer.CrewBuffTakeCoverString, buffDesc=PLocalizer.CrewBuffTakeCover % int((1 - WeaponGlobals.TAKE_COVER_BONUS) * 100), parent=base.a2dBottomRight)
            self.crewBuffDisplay.reparentTo(base.a2dBottomRight, sort=-1000)
            self.crewBuffDisplay.play()

    def _removeTakeCoverEffect(self):
        if self.crewBuffDisplay:
            self.crewBuffDisplay.stop()
            self.crewBuffDisplay.destroy()
            self.crewBuffDisplay = None
        return

    def _addMonkeyPanicEffect(self, attackerId, duration):
        LerpColorScaleInterval(self.getGeomNode(), 1.0, Vec4(1, 0.6, 0.6, 1), startColorScale=Vec4(1, 1, 1, 1)).start()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            self.monkeyPanic = MonkeyPanic.getEffect()
            if self.monkeyPanic:
                if hasattr(self, 'headNode') and self.headNode:
                    self.monkeyPanic.reparentTo(self.headNode)
                    self.monkeyPanic.setPos(-1.0, 0, 0)
                else:
                    self.monkeyPanic.reparentTo(self)
                    self.monkeyPanic.setPos(0, 0, self.height * 0.65)
                self.monkeyPanic.duration = duration
                self.monkeyPanic.usesSound = self.isLocal()
                self.monkeyPanic.startLoop()

    def _removeMonkeyPanicEffect(self, cleanup=False):
        if not cleanup:
            LerpColorScaleInterval(self.getGeomNode(), 1.0, Vec4(1, 1, 1, 1)).start()
        if self.monkeyPanic:
            self.monkeyPanic.stopLoop()
            self.monkeyPanic = None
        return

    def _addMastersRiposteEffect(self, attackerId, duration):
        if self.currentWeapon and hasattr(self.currentWeapon, 'startFrost'):
            self.currentWeapon.startFrost()

    def _removeMastersRiposteEffect(self):
        if self.currentWeapon and hasattr(self.currentWeapon, 'stopFrost'):
            self.currentWeapon.stopFrost()

    def _addQuickloadEffect(self, attackerId, duration):
        if self.currentWeapon and hasattr(self.currentWeapon, 'startPulseGlow'):
            self.currentWeapon.startPulseGlow()

    def _removeQuickloadEffect(self):
        if self.currentWeapon and hasattr(self.currentWeapon, 'stopPulseGlow'):
            self.currentWeapon.stopPulseGlow()

    def _addRegenEffect(self, attackerId, duration):
        unlimited = self.isLocal()
        self.healRaysEffect = HealRays.getEffect(unlimited)
        if self.healRaysEffect:
            self.healRaysEffect.reparentTo(self)
            self.healRaysEffect.setScale(0.75, 0.5, 2.5)
            self.healRaysEffect.setPos(0, 0, 3.5)
            self.healRaysEffect.setEffectColor(Vec4(0.3, 1, 1, 1))
            self.healRaysEffect.startLoop()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            self.healSparksEffect = HealSparks.getEffect(unlimited)
            if self.healSparksEffect:
                self.healSparksEffect.reparentTo(self)
                self.healSparksEffect.setScale(1.25, 1, 3)
                self.healSparksEffect.setPos(0, 0, 3.5)
                self.healSparksEffect.setEffectColor(Vec4(0.3, 1, 1, 0.3))
                self.healSparksEffect.startLoop()

    def _removeRegenEffect(self):
        if self.healRaysEffect:
            self.healRaysEffect.stopLoop()
            self.healRaysEffect = None
        if self.healSparksEffect:
            self.healSparksEffect.stopLoop()
            self.healSparksEffect = None
        return

    def _addFuryEffect(self, attackerId, duration):
        unlimited = self.isLocal()
        if not self.furyEffect:
            pass
        if self.furyEffect:
            self.furyEffect.reparentTo(self)
            self.furyEffect.setScale(0.7)
            self.furyEffect.setEffectColor(Vec4(0.6, 0, 0, 0.5))
            self.furyEffect.startLoop()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            self.pulseEffect = PulseEffect.getEffect(unlimited)
            if self.pulseEffect:
                if hasattr(self, 'headNode') and self.headNode:
                    self.pulseEffect.reparentTo(self.headNode)
                    self.pulseEffect.setPos(-1, 0, 0)
                else:
                    self.pulseEffect.reparentTo(self)
                    self.pulseEffect.setPos(0, 0, self.height * 0.65)
                self.pulseEffect.setEffectScale(0.5)
                self.pulseEffect.startLoop()

    def _removeFuryEffect(self):
        if self.furyEffect:
            self.furyEffect.stopLoop()
            self.furyEffect = None
        if self.pulseEffect:
            self.pulseEffect.stopLoop()
            self.pulseEffect = None
        return

    def _createGhostGuardEffect(self):
        if not self.ghostGuardEffect:
            unlimited = self.isLocal()
            self.ghostGuardEffect = ProtectionSpiral.getEffect(unlimited)
        if self.ghostGuardEffect:
            self.ghostGuardEffect.reparentTo(self)
            self.ghostGuardEffect.setPos(0, 0, 2)
            self.ghostGuardEffect.setScale(0.8, 0.6, 0.9)

    def _removeGhostGuardEffect(self):
        if self.ghostGuardEffect:
            self.ghostGuardEffect.stopLoop()
            self.ghostGuardEffect = None
        return

    def pulseGhostGuardEffect(self, attacker, color, wantBlending=True):
        if self.ghostGuardEffect:
            originalColor = self.ghostGuardEffect.effectColor
            self.ghostGuardPulseIval = Sequence(Func(self.ghostGuardEffect.setEffectColor, color), Wait(0.25), Func(self.ghostGuardEffect.setEffectColor, color))
            self.ghostGuardPulseIval.start()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                auraPulse = HitPulse.getEffect(unlimited=self.isLocal())
                if auraPulse:
                    auraPulse.reparentTo(self)
                    auraPulse.setEffectColor(Vec4(color), wantBlending)
                    auraPulse.effectModel.setPos(0, 2, 4.25)
                    auraPulse.setScale(0.8)
                    auraPulse.lookAt(attacker)
                    auraPulse.play()
                flashEffect = FlashEffect()
                flashEffect.reparentTo(self)
                flashEffect.setScale(10.0)
                flashEffect.setPos(0, 2, 3.5)
                flashEffect.fadeTime = 1.0
                flashEffect.setEffectColor(Vec4(color), wantBlending)
                flashEffect.play()

    def _addMeleeShieldEffect(self, attackerId, duration):
        self._createGhostGuardEffect()
        if self.ghostGuardEffect:
            self.ghostGuardEffect.setEffectColor(Vec4(0, 0, 0, 0.75))
            self.ghostGuardEffect.startLoop()

    def _addMissileShieldEffect(self, attackerId, duration):
        self._createGhostGuardEffect()
        if self.ghostGuardEffect:
            self.ghostGuardEffect.setEffectColor(Vec4(1, 1, 1, 0.75))
            self.ghostGuardEffect.startLoop()

    def _addMagicShieldEffect(self, attackerId, duration):
        self._createGhostGuardEffect()
        if self.ghostGuardEffect:
            self.ghostGuardEffect.setEffectColor(Vec4(0.5, 0.3, 1, 0.75))
            self.ghostGuardEffect.startLoop()

    def checkAttuneBuffEffect(self):
        attuneBuffs = self.findAllBuffCopyKeys(WeaponGlobals.C_ATTUNE)
        if not attuneBuffs or self.isInvisibleGhost():
            if self.voodooAttuneEffect:
                self.voodooAttuneSound.stop()
                self.voodooAttuneSound = None
                self.voodooAttuneEffect.stopLoop()
                self.voodooAttuneEffect = None
            return
        if not self.voodooAttuneEffect:
            self.voodooAttuneEffect = AttuneEffect.getEffect()
            if self.voodooAttuneEffect:
                self.voodooAttuneEffect.reparentTo(self)
                self.voodooAttuneEffect.setPos(0, 0, self.getHeight())
                self.voodooAttuneEffect.startLoop()
        if self.voodooAttuneEffect:
            self.voodooAttuneSound = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_ATTUNE_LOOP)
            base.playSfx(self.voodooAttuneSound, looping=1, node=self, volume=0.25, cutoff=100)
            buffColorType = None
            for buffKeyId in attuneBuffs:
                effectId, attackerId, duration, timeLeft, timestamp, buffData = self.skillEffects[buffKeyId]
                attacker = self.cr.doId2do.get(attackerId)
                if attacker:
                    if not TeamUtils.damageAllowed(attacker, self):
                        if buffColorType != 'hostile':
                            if buffColorType != 'localHostile' and (attackerId == localAvatar.doId or self.doId == localAvatar.doId):
                                buffColorType = 'localFriendly'
                            elif buffColorType != 'localFriendly':
                                buffColorType = 'friendly'
                    elif attackerId == localAvatar.doId or self.doId == localAvatar.doId:
                        buffColorType = 'localHostile'
                    elif buffColorType != 'localHostile' and buffColorType != 'localFriendly':
                        buffColorType = 'hostile'

            if buffColorType == 'localHostile':
                self.voodooAttuneEffect.setEffectColor(Vec4(0.2, 0.1, 0.5, 1))
            elif buffColorType == 'localFriendly':
                self.voodooAttuneEffect.setEffectColor(Vec4(0.2, 0.5, 0.1, 1))
            elif buffColorType == 'hostile':
                self.voodooAttuneEffect.setEffectColor(Vec4(0.0, 0.0, 0.0, 0.5))
            elif buffColorType == 'friendly':
                self.voodooAttuneEffect.setEffectColor(Vec4(0.0, 0.0, 0.0, 0.5))
        return

    def getPVPMoney(self):
        inv = self.getInventory()
        if inv:
            return inv.getStackQuantity(InventoryType.PVPCurrentInfamy)
        else:
            return 0

    def getMaxPVPMoney(self):
        inv = self.getInventory()
        if inv:
            return inv.getStackLimit(InventoryType.PVPCurrentInfamy)
        else:
            return 0

    def setMaxMoney(self, maxMoney):
        self.maxMoney = maxMoney

    def getMaxMoney(self):
        return self.maxMoney

    def setMoney(self, money):
        self.money = money

    def getMoney(self):
        return self.money

    def setMaxBankMoney(self, maxMoney):
        self.maxBankMoney = maxMoney

    def getMaxBankMoney(self):
        return self.maxBankMoney

    def setBankMoney(self, money):
        self.bankMoney = money

    def getBankMoney(self):
        return self.bankMoney

    def getTotalMoney(self):
        return self.getBankMoney() + self.getMoney()

    def updateReputation(self, category, value):
        DistributedReputationAvatar.updateReputation(self, category, value)

    def showHpText(self, number, pos=0, bonus=0, duration=2.0, scale=0.5, basicPenalty=0, crewBonus=0, doubleXPBonus=0, holidayBonus=0, potionBonus=0, itemEffects=[]):
        if self.HpTextEnabled and not self.ghostMode and base.showGui:
            freebooter = not Freebooter.getPaidStatus(base.localAvatar.getDoId())
            if pos != 0 and self.hasNetPythonTag('MonstrousObject'):
                n = NodePath('empty')
                n.reparentTo(self)
                n.setPos(tuple(pos))
                distance = camera.getDistance(n)
                n.detachNode()
                startPos = pos
                scale *= min(max(4.0, distance / 25.0), 20.0)
            else:
                distance = camera.getDistance(self)
                startPos = (0, 0, 5.0)
                scale *= min(max(1.0, distance / 25.0), 20.0)
            if pos == 0:
                startPos = (0, 0, 5.0)
            else:
                startPos = pos
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
            if potionBonus > 0:
                mods[TextEffect.MOD_POTIONBONUS] = potionBonus
            if ItemGlobals.CRITICAL in itemEffects:
                scale *= 1.5
            newEffect = TextEffect.genTextEffect(self, self.HpTextGenerator, number, bonus, self.isNpc, cleanup, startPos, scale=scale, modifiers=mods, effects=itemEffects)
            if newEffect:
                self.textEffects.append(newEffect)
        return

    def hideHpText(self, hpText=None):
        if hpText:
            index = self.hpTextNodes.index(hpText)
            self.hpTextIvals[index].finish()
            self.hpTextIvals[index] = None
            self.hpTextNodes[index].removeNode()
            self.hpTextNodes[index] = None
        return

    def showHpString(self, text, pos=0, duration=2.0, scale=0.5):
        if self.HpTextEnabled and not self.ghostMode and base.showGui:
            if text != '':
                self.HpTextGenerator.setFont(PiratesGlobals.getPirateOutlineFont())
                self.HpTextGenerator.setText(text)
                self.HpTextGenerator.clearShadow()
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                if self.isNpc:
                    r = 0.9
                    g = 0.1
                    b = 0.1
                    a = 1
                else:
                    r = 0.9
                    g = 0.3
                    b = 0.1
                    a = 1
                self.HpTextGenerator.setTextColor(r, g, b, a)
                hpTextNode = self.HpTextGenerator.generate()
                hpTextDummy = self.attachNewNode('hpTextDummy')
                hpText = hpTextDummy.attachNewNode(hpTextNode)
                distance = camera.getDistance(self)
                scale *= min(max(1.0, distance / 25.0), 20.0)
                hpText.setScale(scale)
                hpText.setBillboardPointEye(3.0)
                hpText.setBin('fixed', 100)
                hpText.setDepthWrite(0)
                hpText.setFogOff()
                hpText.setLightOff()
                if pos:
                    hpTextDummy.setPos(self, pos[0], pos[1], pos[2])
                else:
                    hpTextDummy.setPos(self, 0, 0, self.height * 0.666)
                hpTextDummy.setHpr(render, 0, 0, 0)
                numberMoveUp = hpText.posInterval(duration, Point3(0, 0, 8.0), startPos=Point3(0, 0, 2.0))
                fadeOut = hpText.colorScaleInterval(duration * 0.333, Vec4(r, g, b, 0), startColorScale=Vec4(r, g, b, a))
                track = Sequence(Parallel(numberMoveUp, Sequence(Wait(duration * 0.666), fadeOut)), Func(self.hideHpText, hpTextDummy))
                track.start()
                self.hpTextNodes.append(hpTextDummy)
                self.hpTextIvals.append(track)

    def newBackstab(self):
        self.showEffectString(PLocalizer.AttackBackstab, 0, 1.7, 0.46)

    def showEffectString(self, text, pos=0, duration=2.0, scale=0.5):
        if self.HpTextEnabled and not self.ghostMode and base.showGui:
            if text != '':
                self.HpTextGenerator.setFont(PiratesGlobals.getPirateOutlineFont())
                self.HpTextGenerator.setText(text)
                self.HpTextGenerator.clearShadow()
                self.HpTextGenerator.setAlign(TextNode.ACenter)
                r = 0.99
                g = 0.84
                b = 0.01
                a = 1
                self.HpTextGenerator.setTextColor(r, g, b, a)
                hpTextNode = self.HpTextGenerator.generate()
                hpTextDummy = self.attachNewNode('hpTextDummy')
                hpText = hpTextDummy.attachNewNode(hpTextNode)
                distance = camera.getDistance(self)
                scale *= min(max(1.0, distance / 25.0), 20.0)
                hpText.setScale(scale)
                hpText.setBillboardPointEye(3.0)
                hpText.setBin('fixed', 100)
                hpText.setDepthWrite(0)
                hpText.setFogOff()
                hpText.setLightOff()
                if pos:
                    hpTextDummy.setPos(self, pos[0], pos[1], pos[2])
                else:
                    hpTextDummy.setPos(self, 0, 0, self.height * 0.8)
                hpTextDummy.setHpr(render, 0, 0, 0)
                numberScaleUp = hpText.scaleInterval(0.15, scale * 0.7, scale * 1.3)
                numberScaleDown = hpText.scaleInterval(0.15, scale * 1.3, scale)
                fadeOut = hpText.colorScaleInterval(duration * 0.162, Vec4(r, g, b, 0), startColorScale=Vec4(r, g, b, a))
                track = Sequence(numberScaleUp, Parallel(numberScaleDown, Sequence(Wait(duration * 0.333), fadeOut)), Func(self.hideHpText, hpTextDummy))
                track.start()
                self.hpTextNodes.append(hpTextDummy)
                self.hpTextIvals.append(track)

    def showHpMeter(self):
        DistributedReputationAvatar.showHpMeter(self)
        statusTray = localAvatar.guiMgr.targetStatusTray
        statusTray.updateName(self.getShortName(), self.level, self.doId)
        statusTray.updateHp(self.hp, self.maxHp, self.doId)
        statusTray.updateVoodoo(self.mojo, self.maxMojo, self.doId)
        statusTray.updateStatusEffects(self.skillEffects)
        statusTray.updateSkill(self.currentAttack, self.doId)
        statusTray.updateIcon(self.doId)
        sticky = localAvatar.currentTarget == self and localAvatar.hasStickyTargets()
        statusTray.updateSticky(sticky)
        statusTray.show()
        if self.avatarType.isA(AvatarTypes.Pirate) or self.avatarType.isA(AvatarTypes.Muck) or self.avatarType.isA(AvatarTypes.Cadaver) or self.avatarType.isA(AvatarTypes.Splatter) or self.avatarType.isA(AvatarTypes.Drench) or self.avatarType.isA(AvatarTypes.JollyRoger):
            statusTray.voodooMeter.show()
            statusTray.targetFrame2.show()
        else:
            statusTray.voodooMeter.hide()
            statusTray.targetFrame2.hide()

    def hideHpMeter(self, delay=6.0):
        DistributedReputationAvatar.hideHpMeter(self, delay=delay)
        if base.localAvatar.guiMgr.targetStatusTray.doId == self.getDoId():
            if self.getTotalHp() <= 0:
                localAvatar.guiMgr.targetStatusTray.updateHp(0, self.maxHp)

            localAvatar.guiMgr.targetStatusTray.fadeOut(delay=delay)

    def getLandRoamIdleAnimInfo(self):
        return ('idle', 1.0)

    def setEnsnaredTargetId(self, avId):
        self.ensnaredTargetId = avId

    def getEnsnaredTargetId(self):
        return self.ensnaredTargetId

    def getRope(self, thickness=0.125):
        if not self.rope:
            rope = Rope.Rope()
            rope.ropeNode.setRenderMode(RopeNode.RMBillboard)
            rope.ropeNode.setUvMode(RopeNode.UVDistance)
            rope.ropeNode.setUvDirection(1)
            rope.ropeNode.setUvScale(0.5)
            ropeHigh = loader.loadModel('models/char/rope_high')
            ropeTex = ropeHigh.findTexture('rope_single_omit')
            rope.setTexture(ropeTex)
            self.rope = rope
            ropeActor = Actor.Actor()
            ropeActor.loadModel('models/char/rope_high', 'modelRoot')
            ropeActor.loadAnims({'swing_aboard': 'models/char/rope_mtp_swing_aboard'})
            self.ropeActor = ropeActor
        self.rope.ropeNode.setThickness(thickness)
        return (
         self.rope, self.ropeActor)

    def startCompassEffect(self):
        if not self.isDisabled():
            self.stopCompassEffect()
            taskMgr.add(self.compassTask, self.uniqueName('compassTask'), priority=25)

    def stopCompassEffect(self):
        self.compassTask(0)
        taskMgr.remove(self.uniqueName('compassTask'))

    def compassTask(self, task):
        if not self.tracksTerrain and config.GetBool('want-compass-task', 1):
            self.setR(render, 0)
        return Task.cont

    def setHeight(self, height):
        self.height = height
        self.adjustNametag3d()
        if self.collTube:
            self.collTube.setPointB(0, 0, height - self.getRadius())
            if self.collNodePath:
                self.collNodePath.forceRecomputeBounds()
        if self.battleTube:
            self.battleTube.setPointB(0, 0, max(10.0, height) - self.getRadius())
        for tube in self.aimTubeNodePaths:
            tube.node().modifySolid(0).setPointA(0, 0, -max(10.0, height))
            tube.node().modifySolid(0).setPointB(0, 0, max(10.0, height))

    def adjustNametag3d(self):
        defaultZ = 1
        scaleOffset = 0
        newZ = defaultZ
        if self.scale > 1:
            scaleOffset = self.scale - 1
            newZ = 5.4 * scaleOffset + defaultZ
        elif 1 > self.scale:
            scaleOffset = 1 - self.scale
            newZ = 1 - scaleOffset * 5
        self.nametag3d.setPos(0, 0, newZ)

    def drainMojo(self, amt):
        self.sendUpdate('drainMojo', [amt])

    def isAirborne(self):
        return self.motionFSM.isAirborne()

    def printExpText(self, totalExp, colorSetting, basicPenalty, crewBonus, doubleXPBonus, holidayBonus, potionBonus):
        taskMgr.doMethodLater(0.5, self.showHpText, self.taskName('printExp'), [
         totalExp, 0, colorSetting, 5.0, 0.5, basicPenalty, crewBonus, doubleXPBonus, holidayBonus, potionBonus])

    @report(types=['args'], dConfigParam='dteleport')
    def handleArrivedOnShip(self, ship):
        ship.battleAvatarArrived(self)
        self.startCompassEffect()
        self.swapFloorCollideMask(PiratesGlobals.FloorBitmask, PiratesGlobals.ShipFloorBitmask)

    @report(types=['args'], dConfigParam='dteleport')
    def handleLeftShip(self, ship):
        ship.battleAvatarLeft(self)
        self.stopCompassEffect()
        self.swapFloorCollideMask(PiratesGlobals.ShipFloorBitmask, PiratesGlobals.FloorBitmask)

    def swapFloorCollideMask(self, oldMask, newMask):
        pass

    def onShipWithLocalAv(self, sameShip):
        pass

    def setLevel(self, level):
        if level is None:
            if __dev__:
                import pdb
                pdb.set_trace()
            level = 0
        self.level = level
        return

    def getLevel(self):
        return self.level

    def resetAnimProp(self):
        pass

    def motionFSMEnterState(self, anim):
        pass

    def motionFSMExitState(self, anim):
        pass

    def getAdjMaxHp(self):
        if self.isNpc:
            inv = 0
        else:
            inv = self.getInventory()
        if inv:
            if inv.getStackQuantity(InventoryType.Vitae_Level) > 0:
                return int(self.maxHp * 0.75)
            else:
                return self.maxHp
        else:
            return self.maxHp

    def getAdjMaxMojo(self):
        if self.isNpc:
            inv = 0
        else:
            inv = self.getInventory()
        if inv:
            if inv.getStackQuantity(InventoryType.Vitae_Level) > 0:
                return int(self.maxMojo * 0.75)
            else:
                return self.maxMojo
        else:
            return self.maxMojo

    def interrupted(self, effectId):
        pass

    def getSfx(self, name):
        return self.sfx.get(name)

    def getEnemyScale(self):
        return EnemyGlobals.getEnemyScale(self)

    def isBoss(self):
        return self.avatarType.isA(AvatarTypes.BossType)

    def getShortName(self):
        return self.avatarType.getShortName()

    def setInInvasion(self, value):
        self.inInvasion = value

    def isInInvasion(self):
        return self.inInvasion

    def getEfficiency(self):
        return self.efficiency

    def setEfficiency(self, efficiency):
        self.efficiency = efficiency

    def setArmorScale(self, armorScale):
        self.armorScale = armorScale

    def getArmorScale(self):
        return self.armorScale

    def setTrackTerrain(self, value):
        self.tracksTerrain = value

    def trackTerrain(self):
        if self.tracksTerrain == None:
            trackingCreatures = [
             AvatarTypes.Crab, AvatarTypes.RockCrab, AvatarTypes.GiantCrab, AvatarTypes.Pig, AvatarTypes.Dog, AvatarTypes.Scorpion, AvatarTypes.DreadScorpion, AvatarTypes.Alligator, AvatarTypes.BigGator, AvatarTypes.HugeGator]
            if self.avatarType.getNonBossType() in trackingCreatures:
                self.setTrackTerrain(True)
            else:
                self.setTrackTerrain(False)
        if self.tracksTerrain:
            gNode = self.getGeomNode()
            if gNode and not gNode.isEmpty():
                if self.gNodeFwdPt == None:
                    self.gNodeFwdPt = gNode.getRelativePoint(self, Point3(0, 1, 0))
                gNode.headsUp(self.gNodeFwdPt, self.getRelativeVector(self.getParentObj(), self.floorNorm))
        return self.tracksTerrain

    def battleRandomSync(self):
        if hasattr(self, 'battleRandom'):
            self.battleRandom.resync()

    def ramKnockdown(self):
        actorIval = Sequence(self.actorInterval('injured_fall', playRate=1.5, blendOutT=0), self.actorInterval('injured_standup', playRate=1.5, blendInT=0))
        self.ouchAnim = actorIval
        self.ouchAnim.start()

    def regenUpdate(self, hpGained):
        self.showHpText(hpGained)

    def initializeDropShadow(self, hasGeomNode=True):
        DistributedReputationAvatar.initializeDropShadow(self, hasGeomNode=True)
        if self.getShadowJoint():
            self.dropShadow.setPos(0, 0, 0)
            self.compassNode = self.attachNewNode('compassNode')
            self.dropShadow.reparentTo(self.compassNode)
            ce = CompassEffect.make(self.getShadowJoint(), ~CompassEffect.PZ)
            self.compassNode.setEffect(ce)
            if base.options.getCharacterDetailSetting() == PiratesGlobals.CD_LOW and not self.isLocal():
                self.compassNode.stash()

    def considerEnableMovement(self):
        self.motionFSM.on()

    def getMinimapObject(self):
        if not self.minimapObj and not self.isDisabled():
            self.minimapObj = MinimapBattleAvatar(self)
        return self.minimapObj

    def destroyMinimapObject(self):
        if self.minimapObj:
            self.minimapObj.removeFromMap()
            self.minimapObj = None
        return

    def setIsTracked(self, questId):
        self.isTracked = False
        if questId:
            quest = localAvatar.getQuestById(questId)
            if quest and quest.getTasks() and not quest.isTimedOut():
                for currTaskState, currTask in zip(quest.getTaskStates(), quest.getTasks()):
                    if currTask.getGoalUid(currTaskState).compareTo(self) == 0 and not currTaskState.isComplete():
                        self.isTracked = True
                        if localAvatar.questIndicator.indicatorNode:
                            localAvatar.questIndicator.indicatorNode.requestTargetRefresh(0)
                        break

        if self.minimapObj:
            self.minimapObj.setIsTracked(self.isTracked)

    def setVisZone(self, visZone):
        self.visZone = visZone
        self.handleLocalAvatarVisZoneChanged()

    def getVisZone(self):
        return self.visZone

    def d_setVisZone(self, visZone):
        self.sendUpdate('setVisZone', [visZone])

    def b_setVisZone(self, visZone):
        self.setVisZone(visZone)
        self.d_setVisZone(visZone)

    def handleLocalAvatarVisZoneChanged(self):
        if self.trackStats:
            while self.doId in base.visList:
                base.visList.remove(self.doId)

        if hasattr(self.getParentObj(), 'builder'):
            self.getParentObj().builder.handleLighting(self, self.visZone)
            if self.getParentObj().builder.isVisible(self.visZone):
                if self.trackStats:
                    base.visList.append(self.doId)
                self.visShow()
            else:
                self.visHide()
        else:
            self.visShow()
        if self.trackStats:
            base.visCount = len(base.visList)
            onScreenDebug.add('Avatar Vis Count', base.visCount)
            self.pstatsTotal.setLevel(base.npcCount - (base.visCount + 1))
            self.pstatsVisible.setLevel(base.visCount)

    def visHide(self):
        self.hide(invisibleBits=PiratesGlobals.INVIS_VISZONE)

    def visShow(self):
        self.show(invisibleBits=PiratesGlobals.INVIS_VISZONE)

    def getAvatarType(self):
        return self.avatarType

    @report(types=['frameCount', 'args'], dConfigParam='jail')
    def hide(self, drawMask=None, invisibleBits=None):
        if invisibleBits:
            self.invisibleMask |= invisibleBits
        if drawMask:
            DistributedReputationAvatar.hide(self, drawMask)
            if invisibleBits and not invisibleBits.isZero():
                DistributedReputationAvatar.hide(self)
        else:
            DistributedReputationAvatar.hide(self)

    @report(types=['frameCount', 'args'], dConfigParam='jail')
    def show(self, drawMask=None, invisibleBits=None):
        if invisibleBits:
            self.invisibleMask &= ~invisibleBits
        if drawMask:
            DistributedReputationAvatar.show(self, drawMask)
        elif self.invisibleMask.isZero():
            DistributedReputationAvatar.show(self)

    def getSkillRankBonus(self, skillId):
        upgradeAmt = WeaponGlobals.getAttackUpgrade(skillId)
        realSkillId = WeaponGlobals.getLinkedSkillId(skillId)
        if not realSkillId:
            realSkillId = skillId
        rank = self.getSkillRank(realSkillId)
        if WeaponGlobals.getSkillTrack(skillId) != WeaponGlobals.PASSIVE_SKILL_INDEX:
            rank -= 1
        statBonus = 0
        if rank > 5:
            statBonus = 5 * upgradeAmt
            statBonus += (rank - 5) * (upgradeAmt / 2.0)
        else:
            statBonus = rank * upgradeAmt
        return statBonus

    def getSkillRank(self, skillId):
        if self.isNpc:
            return 0
        skillLvl = 0
        inv = self.getInventory()
        if inv:
            skillLvl = max(0, inv.getStackQuantity(skillId) - 1)
            skillLvl += ItemGlobals.getWeaponBoosts(self.currentWeaponId, skillId)
            skillLvl += ItemGlobals.getWeaponBoosts(self.getCurrentCharm(), skillId)
        if self.ship:
            skillLvl += self.ship.getSkillBoost(skillId)
        return skillLvl

    def enablePotionFx(self):
        if base.config.GetBool('want-potion-game', 0):
            self.potionStatusEffectManager = PotionStatusEffectManager(self)

    def disablePotionFx(self):
        if base.config.GetBool('want-potion-game', 0):
            self.potionStatusEffectManager.disable()
            self.potionStatusEffectManager = None
        return

    def switchVisualMode(self, mode):
        pass

    def requestEmote(self, emoteId):
        gamestate = self.getGameState()
        emote = self.getEmote(emoteId)
        if emote:
            emote_gender = EmoteGlobals.getEmoteGender(emoteId)
            if emote_gender and self.style.gender != emote_gender:
                return False
        else:
            return False
        if self.getGameState() in ('Injured', 'Dying', 'Healing'):
            return False
        if self.getGameState() in ('Emote', 'Battle'):
            self.b_setGameState('LandRoam')
        if self.isWeaponDrawn:
            return True
        elif gamestate in ('ShipPilot', 'Cannon', 'WaterRoam', 'WaterTreasureRoam',
                           'ParlorGame', 'NPCInteract', 'DinghyInteract', 'TentacleAlive'):
            return True
        elif localAvatar.controlManager.currentControls.moving:
            return True
        elif EmoteGlobals.getEmoteAnim(emoteId) == None:
            return True
        else:
            self.d_setEmote(emoteId)
            self.b_setGameState('Emote')
            return True
        return

    def playEmote(self, emoteId):
        if self.getGameState() not in ['Emote', 'OOBEmote', 'WeaponReceive', 'NPCInteract']:
            return
        emote = self.getEmote(emoteId)
        if not emote:
            return
        if EmoteGlobals.getEmoteAnim(emoteId) == None:
            return
        self.cleanupEmote()
        self.emoteTrack = Parallel()
        propId = EmoteGlobals.getEmoteProp(emoteId)
        if propId is not None:
            prop = loader.loadModel(propId, okMissing=True)
            if prop:
                if 'grenade' in propId:
                    prop.setScale(0.65)
                motion_blur = prop.find('**/motion_blur')
                if not motion_blur.isEmpty():
                    motion_blur.stash()
                handNode = self.rightHandNode
                if handNode:
                    prop.flattenStrong()
                    prop.reparentTo(handNode)
                    self.emoteProp = prop
                    self.emoteProp.stash()
                propSeq = Sequence()
                waitProp = EmoteGlobals.getWaitProp(emoteId)
                if waitProp:
                    propSeq.append(Wait(waitProp))
                propSeq.append(Func(self.emoteProp.unstash))
                durProp = EmoteGlobals.getDurProp(emoteId)
                if durProp:
                    propSeq.append(Wait(durProp))
                    propSeq.append(Func(self.emoteProp.stash))
                self.emoteTrack.append(propSeq)
            else:
                self.notify.warning('emote %s could not find prop %s, verify it is in the proper phase' % (emoteId, propId))
        looping = EmoteGlobals.getEmoteLoop(emoteId)
        if EmoteGlobals.getEmoteSfx(emoteId):
            sfx = base.loadSfx(EmoteGlobals.getEmoteSfx(emoteId))
            if looping:
                self.emoteTrack.append(SoundInterval(sfx, node=self, loop=True))
            else:
                self.emoteTrack.append(SoundInterval(sfx, node=self))
        self.emoteEffect = EmoteGlobals.getEmoteVfx(emoteId)
        if self.emoteEffect:
            self.emoteEffect.reparentTo(self.rightHandNode)
            if looping:
                self.emoteTrack.append(Func(self.emoteEffect.startLoop))
            else:
                self.emoteTrack.append(Func(self.emoteEffect.play))
        anim = EmoteGlobals.getEmoteAnim(emoteId)
        if looping:
            self.emoteTrack.append(Func(self.loop, anim))
        else:
            self.emoteAnimIval = self.actorInterval(anim)
            tempIval = Sequence(self.emoteAnimIval)
            if self.isLocal():
                if self.getGameState() not in ['NPCInteract', 'OOBEmote']:
                    tempIval.append(Func(self.b_setGameState, 'LandRoam'))
            else:
                tempIval.append(Func(self.setGameState, 'LandRoam'))
            self.emoteTrack.append(tempIval)
        self.emoteTrack.start()
        return

    def cleanupEmote(self):
        if self.emoteTrack:
            self.emoteTrack.pause()
            self.emoteTrack = None
        if self.emoteAnimIval:
            self.emoteAnimIval.finish()
            self.emoteAnimIval = None
        if self.emoteProp:
            self.emoteProp.removeNode()
            self.emoteProp = None
        if self.emoteEffect:
            self.emoteEffect.stopLoop()
            self.emoteEffect = None
        return

    def getEmote(self, emoteId):
        return EmoteGlobals.emotes.get(emoteId)

    def setEmote(self, emoteId):
        self.emoteId = emoteId

    def d_setEmote(self, emoteId):
        self.setEmote(emoteId)
        self.b_setEmote(emoteId)

    def b_setEmote(self, emoteId):
        self.sendUpdate('setEmote', [emoteId])

    def canIdleSplashEver(self):
        return False

    def canIdleSplash(self):
        return self.canIdleSplashEver()

    def getQuestIndicatorOffset(self):
        return base.cr.npcManager.getNpcData(self.uniqueId).get('rolOffset', Point3(0, 0, 0))


class MinimapBattleAvatar(GridMinimapObject):
    ICON = None
    ICON_TRACKED = None
    DEFAULT_COLOR = VBase4(1.0, 0.0, 0.0, 1)

    def __init__(self, avatar):
        if not MinimapBattleAvatar.ICON:
            gui = loader.loadModel('models/gui/compass_main')
            MinimapBattleAvatar.ICON = gui.find('**/icon_sphere')
            MinimapBattleAvatar.ICON.clearTransform()
            MinimapBattleAvatar.ICON.setHpr(90, 90, 0)
            MinimapBattleAvatar.ICON.setScale(200)
            MinimapBattleAvatar.ICON.flattenStrong()
            MinimapBattleAvatar.ICON_TRACKED = gui.find('**/icon_objective_grey')
            MinimapBattleAvatar.ICON_TRACKED.setHpr(90, 90, 0)
            MinimapBattleAvatar.ICON_TRACKED.setScale(200)
            MinimapBattleAvatar.ICON_TRACKED.flattenStrong()
            MinimapBattleAvatar.ICON_TRACKED.setColorScaleOff(1)
            MinimapBattleAvatar.ICON_TRACKED.setColorScale(Vec4(1, 1, 0, 1), 1)
        GridMinimapObject.__init__(self, avatar.getName(), avatar, MinimapBattleAvatar.ICON)
        self.trackedNode = NodePath(avatar.getName())
        self.trackedIcon = MinimapBattleAvatar.ICON_TRACKED.copyTo(self.trackedNode)
        self.trackedIcon.reparentTo(self.mapGeom, sort=-1)
        self.trackedIcon.hide()
        self.isTracked = avatar.isTracked

    def _addedToMap(self, map):
        self.setIconColor()

    def _updateOnMap(self, map):
        GridMinimapObject._updateOnMap(self, map)
        if self.worldNode.isInvisibleGhost() or localAvatar.guiMgr.invasionScoreboard:
            self.mapGeom.hide()
        else:
            self.mapGeom.show()

    def setIsTracked(self, isTracked):
        self.isTracked = isTracked
        if self.isTracked:
            self.trackedIcon.show()
        else:
            self.trackedIcon.hide()
        self.setIconColor()

    def setIconColor(self, color=None):
        self.mapGeom.setColorScale(color or self.DEFAULT_COLOR, 1)
