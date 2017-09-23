import random
import copy
import time
from math import sin
from math import cos
from math import pi
from panda3d.core import *
from direct.showbase.PythonUtil import Functor
from direct.showbase.PythonUtil import report
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.DirectObject import *
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.distributed.MsgTypes import *
from direct.distributed import DistributedNode
from direct.task import Task
from direct.gui import DirectLabel
from direct.actor import Actor
from direct.distributed import PyDatagram
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectWaitBar, DGG
from direct.gui.DirectGui import *
from direct.fsm.StatePush import FunctionCall, StateVar
from otp.nametag.NametagGroup import NametagGroup
from otp.nametag.NametagGlobals import CFSpeech, CFQuicktalker, CFTimeout
from otp.avatar.DistributedPlayer import DistributedPlayer
from otp.otpbase import OTPLocalizer
from otp.otpbase import OTPGlobals
from otp.chat import ChatGlobals
from otp.otpgui import OTPDialog
from otp.avatar.Avatar import Avatar
from pirates.piratesbase import UserFunnel
from pirates.effects.LevelUpEffect import LevelUpEffect
from pirates.battle.DistributedBattleAvatar import DistributedBattleAvatar, MinimapBattleAvatar
from pirates.battle import WeaponGlobals
from pirates.battle.EnemySkills import *
from pirates.pirate.DistributedPirateBase import DistributedPirateBase
from pirates.pirate import Biped
from pirates.pirate.PAvatarHandle import PAvatarHandle
from pirates.demo import DemoGlobals
from pirates.quest.DistributedQuestAvatar import DistributedQuestAvatar
from pirates.world.LocationConstants import LocationIds
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals, NamePanelGui, PDialog
from pirates.piratesbase import TeamUtils
from pirates.minigame import Fish, FishingGlobals
from pirates.npc import Skeleton
from pirates.pirate import AvatarTypes
from pirates.effects.VoodooAura import VoodooAura
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.reputation import ReputationGlobals
import PlayerPirateGameFSM
from pirates.band import BandConstance
from pirates.band import DistributedBandMember
from pirates.world.DistributedGameArea import DistributedGameArea
from pirates.world.DistributedIsland import DistributedIsland
from pirates.speedchat import PSCDecoders
from pirates.battle import Consumable
from pirates.piratesbase import Freebooter
from pirates.uberdog.UberDogGlobals import *
from pirates.minigame import PotionGlobals
from pirates.battle import EnemyGlobals
from pirates.inventory import ItemGlobals
from pirates.pirate import AvatarTypes
from pirates.creature.Alligator import Alligator
from pirates.creature.Scorpion import Scorpion
from pirates.creature.Crab import Crab
from pirates.creature import DistributedCreature
from pirates.movement.MotionFSM import MotionFSM
from pirates.effects.WaterRipple import WaterRipple
from pirates.effects.WaterRippleWake import WaterRippleWake
from pirates.effects.WaterRippleSplash import WaterRippleSplash
from pirates.effects.HealSparks import HealSparks
from pirates.effects.HealRays import HealRays
from pirates.piratesgui import CrewIconSelector
from pirates.coderedemption import CodeRedemption
from pirates.pvp import PVPGlobals
from pirates.pirate import TitleGlobals
from pirates.effects.InjuredEffect import InjuredEffect
from otp.otpbase import OTPRender
from pirates.audio.SoundGlobals import loadSfx
from pirates.audio import SoundGlobals
from pirates.makeapirate import ClothingGlobals
from pirates.pirate import PlayerStateGlobals
from pirates.economy.StowawayGUI import StowawayGUI
from pirates.ai import HolidayGlobals
from pirates.piratesgui.DialMeter import DialMeter
from pirates.quest import QuestDB
from pirates.piratesbase import Freebooter
from pirates.inventory import ItemConstants

class DistributedPlayerPirate(DistributedPirateBase, DistributedPlayer, DistributedBattleAvatar, DistributedQuestAvatar, PAvatarHandle):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPirate')
    wantBattle = base.config.GetBool('want-battle', 1)
    deferrable = True
    GoldFounderIcon = None
    SilverFounderIcon = None
    crewIconId = None
    tempDoubleXPStatus = None
    badgeIconDict = None
    gmNameTag = None
    confusedIcon = None

    def __init__(self, cr):
        try:
            self.DistributedPirate_initialized
            return
        except:
            self.DistributedPirate_initialized = 1

        self.onWelcomeWorld = False
        if not self.GoldFounderIcon:
            gui = loader.loadModel('models/gui/toplevel_gui')
            self.GoldFounderIcon = gui.find('**/founders_coin').copyTo(NodePath('coinTop'))
            self.GoldFounderIcon.setScale(2.8)
            self.SilverFounderIcon = gui.find('**/founders_silver_coin').copyTo(NodePath('coinTop'))
            self.SilverFounderIcon.setScale(2.8)
            tpMgr = TextPropertiesManager.getGlobalPtr()
            tpMgr.setGraphic('goldFounderIcon', self.GoldFounderIcon)
            tpMgr.setGraphic('silverFounderIcon', self.SilverFounderIcon)
            gold = TextProperties()
            gold.setTextColor(1, 0.8, 0.4, 1)
            tpMgr.setProperties('goldFounder', gold)
            silver = TextProperties()
            silver.setTextColor(0.75, 0.75, 0.75, 1)
            tpMgr.setProperties('silverFounder', silver)
            crewPurpleColor = TextProperties()
            crewPurpleColor.setTextColor(0.9, 0.5, 1.0, 1)
            tpMgr.setProperties('crewPurple', crewPurpleColor)
            afkGrayColor = TextProperties()
            afkGrayColor.setTextColor(0.5, 0.5, 0.5, 1)
            tpMgr.setProperties('afkGray', afkGrayColor)
            injuredRedColor = TextProperties()
            injuredRedColor.setTextColor(1.0, 0.0, 0.0, 1)
            tpMgr.setProperties('injuredRed', injuredRedColor)
            ignoredPinkColor = TextProperties()
            ignoredPinkColor.setTextColor(1.0, 0.0, 1.0, 1)
            tpMgr.setProperties('ignoredPink', ignoredPinkColor)
            injuredRedTimerColor = TextProperties()
            injuredRedTimerColor.setTextColor(1.0, 0.0, 0.0, 1)
            injuredRedTimerColor.setTextScale(2.0)
            tpMgr.setProperties('injuredRedTimer', injuredRedTimerColor)

        if not self.tempDoubleXPStatus:
            x2XPGui = loader.loadModel('models/gui/toplevel_gui')
            self.x2XPIcon = gui.find('**/2xp')
            self.x2XPIcon.setScale(4.5)
            tpMgr.setGraphic('x2XPAwardIcon', self.x2XPIcon)

        if not self.crewIconId:
            self.crewIconId = True
            crewIconGui = loader.loadModel(CrewIconSelector.CREW_ICON_BAM)
            self.crewIconDict = {}
            for k, v in CrewIconSelector.CREW_ICONS.iteritems():
                np = crewIconGui.find('**/%s' % v)
                self.crewIconDict[k] = np.copyTo(NodePath())
                self.crewIconDict[k].setScale(8.8)
                if k == 1:
                    np = crewIconGui.find('**/icon_glow')
                    self.myCrewColorGlow = np.copyTo(self.crewIconDict[k])
                    self.myCrewColorGlow.setScale(1.25)
                    self.myCrewColorGlow.setColor(0, 1, 0, 1)
                elif k == 2:
                    np = crewIconGui.find('**/icon_glow')
                    self.otherCrewColorGlow = np.copyTo(self.crewIconDict[k])
                    self.otherCrewColorGlow.setScale(1.25)
                    self.otherCrewColorGlow.setColor(1, 0, 0, 1)

                tpMgr.setGraphic('crewIcon%s' % k, self.crewIconDict[k])

        if not self.badgeIconDict:
            self.badgeIconDict = {}
            for titleId in TitleGlobals.TitlesDict.keys():
                titleModel = loader.loadModel(TitleGlobals.getModelPath(titleId))
                for rank in range(TitleGlobals.getMaxRank(titleId) + 1):
                    icName = TitleGlobals.getIconName(titleId, rank)
                    if not icName:
                        continue

                    icon = titleModel.find('**/' + icName)
                    if not icon or icon.isEmpty():
                        continue

                    imgScale = TitleGlobals.getScale(titleId)
                    icon.setScale(0.71 * imgScale)
                    iconKey = 'badge-%s-%s' % (titleId, rank)
                    self.badgeIconDict[iconKey] = icon
                    tg = TextGraphic(icon, -0.25, 0.75, -0.31, 0.69)
                    tpMgr.setGraphic(iconKey, tg)

        if not self.gmNameTag:
            self.gmNameTagIcon = loader.loadModel('models/gui/gmLogo_tflip')
            self.gmNameTagIcon.setScale(2.5)
            tpMgr.setGraphic('gmNameTagLogo', self.gmNameTagIcon)
            gmGoldColor = TextProperties()
            gmGoldColor.setTextColor(1, 0.9, 0.7, 1)
            tpMgr.setProperties('goldGM', gmGoldColor)
            gmRedColor = TextProperties()
            gmRedColor.setTextColor(1.0, 0.1, 0.1, 1)
            tpMgr.setProperties('redGM', gmRedColor)
            gmGreenColor = TextProperties()
            gmGreenColor.setTextColor(0.3, 0.7, 0.25, 1)
            tpMgr.setProperties('greenGM', gmGreenColor)
            gmBlueColor = TextProperties()
            gmBlueColor.setTextColor(0.35, 0.7, 1, 1)
            tpMgr.setProperties('blueGM', gmBlueColor)
            gmWhiteColor = TextProperties()
            gmWhiteColor.setTextColor(1, 1, 1, 1)
            tpMgr.setProperties('whiteGM', gmWhiteColor)

        if not self.confusedIcon:
            self.confusedIcon = gui.find('**/pir_t_gui_but_chatIncomplete').copyTo(NodePath('confusedTop'))
            self.confusedIcon.setScale(10.0)
            tpMgr.setGraphic('confusedIcon', self.confusedIcon)

        self.title = ''
        self.lastLoop = None
        DistributedPirateBase.__init__(self, cr)
        DistributedBattleAvatar.__init__(self, cr)
        DistributedPlayer.__init__(self, cr)
        DistributedQuestAvatar.__init__(self)
        self.name = ''
        self.inPvp = False
        self._inPvpSV = StateVar(self.inPvp)
        self.inParlorGame = False
        self._zombieSV = StateVar(self.zombie)
        self.setPickable(1)
        self.interactioneer = None
        self.crewShip = None
        self.crewShipId = 0
        self.pendingSetCrewShip = None
        self.activeShipId = 0
        self.pendingTeleportMgr = None
        self.crewInterest = None
        self.captainId = 0
        self.chestIcon = None
        self.lootCarried = 0
        self.inventoryId = 0
        self.undead = 0
        self.undeadStyle = ''
        self.skeleton = None
        self.stickyTargets = []
        self.attuneEffect = None
        self.avatarFriendsList = set()
        self.playerFriendsList = set()
        self.guildName = PLocalizer.GuildNoGuild
        self.guildId = -1
        self.guildRank = -1
        self.defaultShard = 0
        self.returnLocation = ''
        self.currentIsland = ''
        self.jailCellIndex = 0
        self.beacon = None
        self.teleportFriendDoId = 0
        self._beaconVisibleSV = StateVar(False)
        self._pvpTeamSV = StateVar(0)
        self.teleportFlags = PiratesGlobals.TFInInitTeleport
        self.teleportConfirmCallbacks = {}
        self.questRewardFlags = 0
        self.bandMember = None
        self.gameAccess = OTPGlobals.AccessUnknown
        self.founder = False
        self.port = 0
        self.waterRipple = None
        self.waterWake = None
        self.waterSplash = None
        self.founderIcon = None
        self.badge = None
        self.shipBadge = None
        self.lastPVPSinkTime = 0
        self.lastShipPVPDecayTime = 0
        self.infamySea = 0
        self.lastPVPDefeatTime = 0
        self.lastLandPVPDecayTime = 0
        self.infamyLand = 0
        self.isLookingForCrew = 0
        self.tutorialState = 0
        self.hasCrewIcon = 0
        self.isAFK = False
        self.status = 0
        self.isPaid = False
        self.populated = 0
        self.updatePaidStatus()
        self.tempDoubleXPStatus = 0
        self.tempDoubleXPStatusMessaged = False
        self.gmNameTagEnabled = 0
        self.gmNameTagColor = 'whiteGM'
        self.gmNameTagString = ''
        self.BandId = None
        self.cursed = False
        self.injuredSetup = 0
        self.injuredTimeLeft = 0
        self.layingOnGround = 0
        self.dizzyEffect = None
        self.dizzyEffect2 = None
        self.beingHealed = False
        self.healEffects = []
        self.healEffectIval = None
        self.isPlundering = 0
        self.isConfused = False
        self.wlEnabled = False
        self.initDazed()
        self.creatureId = -1
        self.creature = None
        self.transformationEffect = None
        self.transformationIval = None
        self.gTransNodeFwdPt = None
        self.cRay = None
        self.cRayNode = None
        self.lifter = None
        self.alligatorSound = loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_ALLIGATOR)
        self.crabSound = loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_CRAB)
        self.scorpionSound = loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_SCORPION)
        self.genericTransformation = loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_TRANFORMATION)
        self.scaleChangeEffect = None
        self.scaleChangeIval = None
        self.isGiant = False
        self.isTiny = False
        self.growSound = loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_GROW)
        self.shrinkSound = loadSfx(SoundGlobals.SFX_MINIGAME_POTION_FX_SHRINK)
        self.crazySkinColorEffect = None
        self.crazySkinColorIval = None
        self.transformSeqEffect = None
        self.injuredFrame = None
        self.ghostEffect = None
        self.isGhost = 0
        self.needRegenFlag = 0
        self.bloodFireTime = 0.0
        self.auraActivated = 0
        self.auraIval = None
        self.fishSwivel = NodePath('fishSwivel')
        self.shownFish = None
        self.shownFishSeq = None
        self.popupDialog = None
        self.injuredTrack = None
        self.__surpressedRepFlags = []
        self.__tutorialEnabled = True
        self.swingTrack = None

    def disable(self):
        DistributedPirateBase.disable(self)
        DistributedPlayer.disable(self)
        DistributedBattleAvatar.disable(self)
        self.exitDialogMode()
        self.ignore('localAvatarEntersDialog')
        self.ignore('localAvatarExitsDialog')
        self.ignore('Local_Efficiency_Set')
        self.stopBlink()
        self.ignoreAll()
        self._showBeaconFC.destroy()
        self._decideBeaconFC.destroy()
        self.hideBeacon()
        self.show(invisibleBits=PiratesGlobals.INVIS_DEATH)
        self.stopDizzyEffect()
        if self.injuredFrame:
            self.injuredFrame.destroy()
        if self.auraIval:
            self.auraIval.pause()
            self.auraIval = None
        if not self.isLocal():
            if hasattr(base, 'localAvatar'):
                base.localAvatar.playersNearby.pop(self.getDoId())
        DistributedPlayerPirate._setCreatureTransformation(self, False, 0)
        if self.transformationEffect:
            self.transformationEffect.detachNode()
            self.transformationEffect = None
        if self.transformationIval:
            self.transformationIval.clearToInitial()
            self.transformationIval = None
        self.isGiant = False
        self.isTiny = False
        if self.scaleChangeIval:
            self.scaleChangeIval.clearToInitial()
            self.scaleChangeIval = None
        self.crazyColorSkin = False
        if self.crazySkinColorIval:
            self.crazySkinColorIval.clearToInitial()
            self.crazySkinColorIval = None
        if self.transformSeqEffect:
            self.transformSeqEffect.detachNode()
            self.transformSeqEffect = None
        if self.consumable:
            self.consumable.delete()
            self.consumable = None
        self.crewShip = None
        if self.pendingSetCrewShip:
            self.cr.relatedObjectMgr.abortRequest(self.pendingSetCrewShip)
            self.pendingSetCrewShip = None
        if self.attuneEffect:
            self.attuneEffect.stopLoop()
            self.attuneEffect = None
        if self.waterRipple:
            self.waterRipple.stopLoop()
            self.waterRipple = None
        if self.waterWake:
            self.waterWake.stopLoop()
            self.waterWake = None
        if self.waterSplash:
            self.waterSplash.stopLoop()
            self.waterSplash = None
        if self.healEffectIval:
            self.healEffectIval.pause()
            self.healEffectIval = None
        for effect in self.healEffects:
            effect.stopLoop()

        self.healEffects = []
        if self.pendingTeleportMgr:
            base.cr.relatedObjectMgr.abortRequest(self.pendingTeleportMgr)
            self.pendingTeleportMgr = None
        taskMgr.remove(self.uniqueName('injuryDial'))
        taskMgr.remove(self.uniqueName('createInvasionScoreboard'))
        taskMgr.remove(self.uniqueName('bloodFireCharging'))
        taskMgr.remove(self.uniqueName('decayInfamySea'))
        taskMgr.remove(self.uniqueName('decayInfamyLand'))
        self.port = 0
        return

    def delete(self):
        try:
            self.DistributedPlayerPirate_deleted
            return
        except:
            self.DistributedPlayerPirate_deleted = 1

        DistributedPirateBase.delete(self)
        DistributedPlayer.delete(self)
        DistributedBattleAvatar.delete(self)
        DistributedQuestAvatar.delete(self)
        if self.skeleton:
            self.skeleton.delete()
            self.skeleton = None

        if self.shownFish:
            self.shownFish.destroy()
            self.shownFish = None

        if self.shownFishSeq:
            self.shownFishSeq.pause()
            self.shownFishSeq = None

    def generate(self):
        DistributedPirateBase.generate(self)
        DistributedPlayer.generate(self)
        DistributedBattleAvatar.generate(self)
        self.setDefaultDNA()
        self._decideBeaconFC = FunctionCall(self._decideShowBeacon, self._zombieSV, self._inPvpSV, self._pvpTeamSV)
        self._decideBeaconFC.pushCurrentState()
        self._showBeaconFC = FunctionCall(self._handleShowBeacon, self._beaconVisibleSV, self._pvpTeamSV)
        self._showBeaconFC.pushCurrentState()
        self.useStandardInteract()
        self.setPlayerType(NametagGroup.CCNormal)

    def sendAILog(self, errorString):
        self.sendUpdate('submitErrorLog', [errorString])

    def useStandardInteract(self):
        if self.isLocal() or self.getTeam() == localAvatar.getTeam():
            allowInteract = False
        else:
            allowInteract = True
        self.setInteractOptions(proximityText='', mouseOver=0, mouseClick=0, isTarget=1, allowInteract=allowInteract)
        if hasattr(base, 'localAvatar'):
            base.localAvatar.playersNearby[self.getDoId()] = (
             self.commonChatFlags, self.whitelistChatFlags)
            if len(localAvatar.playersNearby) > 3:
                level = base.localAvatar.getLevel()
                if level >= 3:
                    inv = base.localAvatar.getInventory()
                    if inv:
                        inv.getStackQuantity(InventoryType.PlayerChat) or base.localAvatar.sendRequestContext(InventoryType.PlayerChat)
                    elif level >= 5 and not inv.getStackQuantity(InventoryType.PlayerProfiles):
                        base.localAvatar.sendRequestContext(InventoryType.PlayerProfiles)
                    elif level >= 6 and not inv.getStackQuantity(InventoryType.PlayerInvites):
                        base.localAvatar.sendRequestContext(InventoryType.PlayerInvites)
                    elif level >= 7:
                        if not inv.getStackQuantity(InventoryType.TeleportToFriends):
                            base.localAvatar.sendRequestContext(InventoryType.TeleportToFriends)
                        elif level >= 8:
                            if not inv.getStackQuantity(InventoryType.UseEmotes):
                                base.localAvatar.sendRequestContext(InventoryType.UseEmotes)

    def setupInjured(self, timeStamp=None, MessageData=None):
        if timeStamp == None:
            timeStamp = globalClock.getFrameTime()
        else:
            self.injuredTimeStamp = globalClock.getFrameTime() - timeStamp
            self.injuredTimeLeft = int(PiratesGlobals.REVIVE_TIME_OUT - self.injuredTimeStamp)
        if not self.isLocal():
            if not localAvatar.isUndead():
                self.acceptOnce('LocalAvatarIsZombie', self.setupInjured, [None])
                sphereScale = 5.0
                if localAvatar.guiMgr.combatTray.tonicButton.getBestTonic(allowNone=1):
                    self.setInteractOptions(proximityText=PLocalizer.InjuredHasTonic, sphereScale=sphereScale, diskRadius=7, resetState=0, offset=Point3(0, -1.5, 0))
                else:
                    self.setInteractOptions(proximityText=PLocalizer.InjuredNeedTonic, sphereScale=sphereScale, diskRadius=7, resetState=0, offset=Point3(0, -1.5, 0))
                avSphereRad = 1.4
                if hasattr(localAvatar.controlManager.currentControls, 'cWallSphereNodePath'):
                    avSphereRad = localAvatar.controlManager.currentControls.cWallSphereNodePath.getBounds().getRadius() + 0.05
                if self.getDistance(localAvatar) <= sphereScale + avSphereRad and self != localAvatar:
                    self.request('Proximity')
            for index in range(InventoryType.begin_Consumables, InventoryType.end_Consumables):
                inv = localAvatar.getInventory()
                if inv:
                    messageName = 'inventoryQuantity-%s-%s' % (inv.doId, index)
                    self.ignore(messageName)
                    self.acceptOnce(messageName, self.setupInjured, [None])

            self.injuredSetup = 1
            taskMgr.add(self.resizeInjuryFrame, self.uniqueName('injuryDial'))
            topGui = self.injuredFrame or loader.loadModel('models/gui/toplevel_gui')
            injuredIcon = topGui.find('**/pir_t_gui_gen_medical')
            circleBase = topGui.find('**/pir_t_gui_frm_base_circle')
            self.injuredFrame = DirectFrame(parent=NodePath(), relief=None, pos=(0.0,
                                                                                 0,
                                                                                 0.0), image=circleBase, image_scale=2.4)
            self.injuredDial = DialMeter(parent=self.injuredFrame, meterColor=VBase4(1.0, 0.0, 0.0, 1), baseColor=VBase4(0.1, 0.1, 0.1, 1), wantCover=0, pos=(0.0, -0.01, 0.0), sortOrder=1, scale=0.9)
            left, right, bottom, top = self.injuredDial.getBounds()
            tpMgr = TextPropertiesManager.getGlobalPtr()
            self.injuredFrame.reparentTo(self.nametag3d)
            self.injuredFrame.setZ(5.5)
            self.injuredFrame.setBillboardPointEye(1)
            self.injuredFrame.setLightOff()
            innerFrame = DirectFrame(parent=self.injuredFrame, relief=None, pos=(0.0, -0.03, 0.0), image=circleBase, image_scale=1.8, sortOrder=2)
            icon = DirectFrame(parent=self.injuredFrame, relief=None, pos=(0.0, -0.04, 0.0), image=injuredIcon, image_scale=2.7, sortOrder=3)
            knockoutLabel = DirectLabel(parent=self.injuredDial, relief=None, state=DGG.DISABLED, text='\x01injuredRed\x01\n%s\x02\n' % PLocalizer.InjuredFlag, text_scale=PiratesGuiGlobals.TextScaleLarge * 5, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateBoldOutlineFont(), pos=(0.0, 0, -0.4), sortOrder=4)
        self.injuredDial.update(self.injuredTimeLeft, PiratesGlobals.REVIVE_TIME_OUT)
        self.injuredFrame.show()
        self.injuredFrame.setBin('fixed', 0)
        self.refreshName()
        return

    def resizeInjuryFrame(self, task):
        self.injuredFrame.setScale(1.0 + 0.03 * camera.getDistance(self))
        self.injuryCountDownTask()
        return task.cont

    def injuryCountDownTask(self, task=None):
        localTime = globalClock.getFrameTime()
        self.injuredTimeLeft = PiratesGlobals.REVIVE_TIME_OUT - (localTime - self.injuredTimeStamp)
        if self.injuredTimeLeft < 0.0:
            self.injuredTimeLeft = 0.0
        self.injuredDial.update(self.injuredTimeLeft, PiratesGlobals.REVIVE_TIME_OUT)

    def cleanupInjured(self, revived=0):
        self.useStandardInteract()
        taskMgr.remove(self.uniqueName('injuryDial'))
        if localAvatar.getInventory():
            for index in range(InventoryType.begin_Consumables, InventoryType.end_Consumables):
                messageName = 'inventoryQuantity-%s-%s' % (localAvatar.getInventory().doId, index)
                self.ignore(messageName)

        self.injuredSetup = 0
        self.injuredFrame.hide()
        self.refreshName()

    def startHeadShakeIval(self):
        self.startDizzyEffect()
        self.headShakeIval = None
        self.playHeadShake()
        return

    def startHeadShakeMixer(self):
        self.startDizzyEffect()
        self.headShakeIval = None
        timeTillShake = 3.0 + random.random() * 6.0
        taskMgr.doMethodLater(timeTillShake, self.doHeadShake, 'shake_head_while_injured_Task')
        return

    def playHeadShake(self):
        if self.headShakeIval:
            self.headShakeIval.pause()
            self.headShakeIval = None
        playAnim = random.choice(['injured_idle_shakehead', 'injured_idle', 'injured_idle', 'injured_idle'])
        self.headShakeIval = Sequence(self.actorInterval(playAnim, blendInT=0.0, blendOutT=0.0), Func(self.playHeadShake))
        self.headShakeIval.start()
        return

    def doHeadShake(self, task):
        self.play('injured_idle_shakehead')
        timeTillShake = 3.0 + random.random() * 10.0
        taskMgr.remove('shake_head_while_injured_Task')
        taskMgr.doMethodLater(timeTillShake, self.doHeadShake, 'shake_head_while_injured_Task')
        return task.done

    def stopHeadShake(self):
        if self.headShakeIval:
            self.headShakeIval.pause()
            self.headShakeIval = None
        self.stopDizzyEffect()
        taskMgr.remove('shake_head_while_injured_Task')

    def startDizzyEffect(self):
        if self.dizzyEffect:
            return
        self.dizzyEffect = InjuredEffect.getEffect()
        if self.dizzyEffect:
            self.dizzyEffect.duration = 2.0
            self.dizzyEffect.direction = 1
            self.dizzyEffect.effectScale = 0.65
            if hasattr(self, 'headNode') and self.headNode:
                self.dizzyEffect.reparentTo(self.headNode)
                self.dizzyEffect.setHpr(0, 0, 90)
                self.dizzyEffect.setPos(self.headNode, 0.6, 0, 0)
            else:
                self.dizzyEffect.reparentTo(self)
                self.dizzyEffect.setHpr(self, 0, 0, 0)
                self.dizzyEffect.setPos(self, 0, 0, self.getHeight() + 0.5)
            self.dizzyEffect.hide(OTPRender.ShadowCameraBitmask)
            self.dizzyEffect.startLoop()
        self.dizzyEffect2 = InjuredEffect.getEffect()
        if self.dizzyEffect2:
            self.dizzyEffect2.duration = 2.0
            self.dizzyEffect2.direction = -1
            self.dizzyEffect2.effectScale = 0.5
            if hasattr(self, 'headNode') and self.headNode:
                self.dizzyEffect2.reparentTo(self.headNode)
                self.dizzyEffect2.setHpr(0, 120, 90)
                self.dizzyEffect2.setPos(self.headNode, 0.85, 0, 0)
            else:
                self.dizzyEffect2.reparentTo(self)
                self.dizzyEffect2.setHpr(self, 120, 0, 0)
                self.dizzyEffect2.setPos(self, 0, 0, self.getHeight() + 0.25)
            self.dizzyEffect2.hide(OTPRender.ShadowCameraBitmask)
            self.dizzyEffect2.startLoop()

    def stopDizzyEffect(self):
        if self.dizzyEffect:
            self.dizzyEffect.stopLoop()
            self.dizzyEffect = None
        if self.dizzyEffect2:
            self.dizzyEffect2.stopLoop()
            self.dizzyEffect2 = None
        return

    def initDazed(self):
        self.isDazed = False
        self.dazedButtonBoolean = False
        shipGui = loader.loadModel('models/gui/ship_battle')
        self.dazedBar = DirectWaitBar(parent=base.a2dBottomCenter, frameSize=(-0.7, 0.7, -0.02, 0.02), relief=DGG.FLAT, image=shipGui.find('**/ship_battle_speed_bar*'), image_pos=(0.0,
                                                                                                                                                                                    0,
                                                                                                                                                                                    0.0), image_scale=(1.0,
                                                                                                                                                                                                       1.0,
                                                                                                                                                                                                       1.0), borderWidth=(0,
                                                                                                                                                                                                                          0), pos=(0.0,
                                                                                                                                                                                                                                   0.0,
                                                                                                                                                                                                                                   0.6), frameColor=(1.0,
                                                                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                                                                     1.0), barColor=(0.0,
                                                                                                                                                                                                                                                                     1.0,
                                                                                                                                                                                                                                                                     0.0,
                                                                                                                                                                                                                                                                     1.0))
        self.dazedBar['value'] = 0
        self.dazedBar.hide()
        self.dazedTextNode = TextNode('DazedTextNode')
        self.dazedTextNodePath = NodePath(self.dazedTextNode)
        self.dazedTextNodePath.setPos(0.0, 0.0, 0.8)
        self.dazedTextNodePath.setScale(0.12)
        self.dazedTextNode.setText(PLocalizer.DazedHelpText)
        self.dazedTextNode.setTextColor(1.0, 1.0, 1.0, 1.0)
        self.dazedTextNode.setAlign(TextNode.ACenter)
        self.dazedTextNode.setFont(PiratesGlobals.getPirateFont())
        self.dazedTextNodePath.reparentTo(base.a2dBottomCenter)
        self.dazedTextNodePath.hide()

    def setPirateDazed(self, isDazedBool):
        if isDazedBool:
            if not self.isDazed:
                if self.gameFSM is None:
                    return
                self.isDazed = True
                if self.isLocal():
                    self.accept('arrow_left', self.dazedButtonPressed, [False])
                    self.accept('a', self.dazedButtonPressed, [False])
                    self.accept('q', self.dazedButtonPressed, [False])
                    self.accept('arrow_right', self.dazedButtonPressed, [True])
                    self.accept('d', self.dazedButtonPressed, [True])
                    self.accept('e', self.dazedButtonPressed, [True])
                    if self.cameraFSM:
                        currentCamera = self.cameraFSM.getCurrentCamera()
                        if currentCamera:
                            currentCamera.disableInput()
                    self.dazedBar.show()
                    self.dazedTextNodePath.show()
                    if self.gameFSM.getCurrentOrNextState() == 'Cannon':
                        self.cannon.cgui.hideCannonControls()
                    taskMgr.add(self.shakeOffDazed, self.uniqueName('ShakeOffDazed'))
                    if base.mouseWatcherNode.hasMouse():
                        self.lastMousePos = Point2(base.mouseWatcherNode.getMouseX(), base.mouseWatcherNode.getMouseY())
                    else:
                        self.lastMousePos = Point2(0.0, 0.0)
                    self.shakeOffDazedCount = 0.0
                    self.dazedBar['value'] = 0
                self.injuredTrack = self.getInjuredTrack()
                self.injuredTrack.start()
                self.startDizzyEffect()
                taskMgr.doMethodLater(PiratesGlobals.DAZED_DURATION, self.setPirateDazed, self.uniqueName('EndDazed'), extraArgs=[False])
        else:
            self.isDazed = False
            if self.isLocal():
                self.ignore('arrow_left')
                self.ignore('a')
                self.ignore('q')
                self.ignore('arrow_right')
                self.ignore('d')
                self.ignore('e')
                if self.cameraFSM:
                    currentCamera = self.cameraFSM.getCurrentCamera()
                    if currentCamera:
                        currentCamera.enableInput()
                self.dazedTextNodePath.hide()
                self.dazedBar.hide()
            if self.gameFSM is None:
                return
            if self.gameFSM.getCurrentOrNextState() == 'Cannon':
                self.loop('kneel')
                if self.cannon is not None and self.cannon.cgui is not None:
                    self.cannon.cgui.showCannonControls()
            if self.injuredTrack:
                self.injuredTrack.finish()
                self.injuredTrack = None
            self.stopDizzyEffect()
            taskMgr.remove(self.uniqueName('EndDazed'))
            taskMgr.remove(self.uniqueName('ShakeOffDazed'))
        return

    def dazedButtonPressed(self, bool):
        if not self.isDazed:
            return
        if bool == self.dazedButtonBoolean:
            self.dazedButtonBoolean = not self.dazedButtonBoolean
            self.shakeOffDazedCount += PiratesGlobals.DAZED_BUTTON_INCREMENT

    def shakeOffDazed(self, task):
        if not self.isDazed:
            return
        if base.mouseWatcherNode.hasMouse():
            currentMousePos = Point2(base.mouseWatcherNode.getMouseX(), base.mouseWatcherNode.getMouseY())
            self.shakeOffDazedCount += (self.lastMousePos - currentMousePos).length()
            self.dazedBar['value'] = int(100.0 * self.shakeOffDazedCount / PiratesGlobals.DAZED_SHAKEOFF_THRESHOLD)
            if self.shakeOffDazedCount > PiratesGlobals.DAZED_SHAKEOFF_THRESHOLD:
                self.setPirateDazed(False)
            self.lastMousePos = currentMousePos
        return Task.again

    def getGetupTrack(self, timeStamp=0.0):
        av = self

        def loopIdle():
            av.loop('idle', blendDelay=0.15)

        getupTrack = Parallel(Sequence(Wait(0.5), Func(loopIdle)), av.actorInterval('injured_standup', blendInT=0.15, blendOutT=0.15))
        return getupTrack

    def getInjuredTrack(self, timeStamp=0.0):
        av = self

        def loopIdle():
            av.loop('injured_idle', blendDelay=0.15)

        def startSFX():
            sfx = self.getSfx('death')
            if sfx:
                base.playSfx(sfx, node=self, cutoff=100)

        injuredTrack = Sequence(Parallel(Sequence(Wait(0.5), Func(loopIdle)), Func(startSFX), av.actorInterval('injured_fall', blendInT=0.15, blendOutT=0.15)))
        return injuredTrack

    def getDyingTrack(self, timeStamp):
        av = self
        animName = 'injured_idle_shakehead'

        def stopSmooth():
            if self.smoothStarted:
                taskName = self.taskName('smooth')
                taskMgr.remove(taskName)
                self.smoothStarted = 0

        def gotoRoam():
            if av.getGameState() == 'Dying':
                if av == localAvatar:
                    av.b_setGameState('LandRoam')

        diedSound = loader.loadSfx('audio/sfx_doll_unattune.mp3')
        diedSoundInterval = SoundInterval(diedSound, node=self)
        duration = 1.0
        deathIval = Parallel(diedSoundInterval, Func(self.setTransparency, 1), self.actorInterval(animName, blendInT=0.15, blendOutT=0.15), Sequence(LerpColorScaleInterval(self, duration, Vec4(1, 1, 1, 0), startColorScale=Vec4(1)), Func(self.hide, None, PiratesGlobals.INVIS_DEATH), Func(self.clearColorScale), Func(self.clearTransparency), Func(gotoRoam)))
        return deathIval

    def reportRevive(self, healerId):
        healer = base.cr.doId2do.get(healerId)
        if healer:
            message = PLocalizer.InjuredHelped % (self.getName(), healer.getName())
            base.talkAssistant.receiveGameMessage(message)

    def faceDO(self, doId2Face):
        do2face = base.cr.doId2do.get(doId2Face)
        if do2face:
            self.headsUp(do2face)

    def startHealing(self, healTime):
        self.acceptInteraction()
        localAvatar.guiMgr.workMeter.updateText(PLocalizer.InjuredReviving)
        localAvatar.guiMgr.workMeter.startTimer(healTime)
        localAvatar.b_setGameState('Healing')
        pos = localAvatar.getPos(self.headNode)
        arm = self.headNode.attachNewNode('arm')
        arm.lookAt(localAvatar)
        oldParent = localAvatar.getParent()
        localAvatar.wrtReparentTo(arm)
        localAvatar.setH(localAvatar, 0)
        radius = 3.5
        aAngle = arm.getH()
        if aAngle > 85.0 and aAngle < 140:
            arm.setH(140)
        elif aAngle <= 85.0 and aAngle > 30:
            arm.setH(30)
        localAvatar.setX(0)
        localAvatar.setY(radius)
        localAvatar.wrtReparentTo(oldParent)
        localAvatar.setScale(1.0)
        localAvatar.setShear(VBase3(0, 0, 0))
        arm.removeNode()
        localAvatar.setZ(self, 0)
        localAvatar.headsUp(self.headNode)
        localAvatar.sendCurrentPosition()

    def stopHealing(self):
        localAvatar.guiMgr.workMeter.stopTimer()
        if localAvatar.getGameState() == 'Healing':
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)

    def setBeingHealed(self, beingHealed):
        self.beingHealed = beingHealed

        def startHealEffects():
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                healSparks = HealSparks.getEffect()
                if healSparks:
                    healSparks.reparentTo(self)
                    healSparks.setPos(self, 0, -1, 0)
                    healSparks.setHpr(self, 0, 90, 0)
                    healSparks.setScale(1.5, 1.5, 2)
                    healSparks.setEffectColor(Vec4(0.3, 1, 1, 0.3))
                    healSparks.startLoop()
                    self.healEffects.append(healSparks)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                healRays = HealRays.getEffect()
                if healRays:
                    healRays.reparentTo(self)
                    healRays.setPos(self, 0, -1, 0)
                    healRays.setHpr(self, 0, 90, 0)
                    healRays.setScale(0.75, 0.75, 2)
                    healRays.setEffectColor(Vec4(0.3, 1, 1, 1))
                    healRays.startLoop()
                    self.healEffects.append(healRays)

        if beingHealed:
            self.healEffectIval = Sequence(Wait(3.0), Func(startHealEffects))
            self.healEffectIval.start()
        else:
            if self.healEffectIval:
                self.healEffectIval.pause()
                self.healEffectIval = None
            for effect in self.healEffects:
                effect.stopLoop()

            self.healEffects = []
        return

    def getBeingHealed(self):
        return self.beingHealed

    def requestExit(self):
        DistributedBattleAvatar.requestExit(self)
        self.stopHealing()

    def _handleShowBeacon(self, showBeacon, pvpTeam):
        if not self.isLocal():
            if showBeacon:
                self.showBeacon(pvpTeam)
            else:
                self.hideBeacon()

    def _decideShowBeacon(self, isZombie, inPvp, pvpTeam):
        self._beaconVisibleSV.set(isZombie and inPvp and pvpTeam)

    def setTeam(self, team):
        DistributedBattleAvatar.setTeam(self, team)
        if not self.isLocal():
            if self.getTeam() == localAvatar.getTeam():
                self.setAllowInteract(False)
            else:
                self.setAllowInteract(True)

    def setPVPTeam(self, team):
        if team and self.isLocal():
            self.guiMgr.crewHUD.setHUDOff()
            self.guiMgr.crewHUDTurnedOff = True
        DistributedBattleAvatar.setPVPTeam(self, team)
        self._pvpTeamSV.set(team)

    def createGameFSM(self):
        self.gameFSM = PlayerPirateGameFSM.PlayerPirateGameFSM(self)

    def announceGenerate(self):
        DistributedPirateBase.announceGenerate(self)
        DistributedPlayer.announceGenerate(self)
        DistributedBattleAvatar.announceGenerate(self)
        self.accept('localAvatarEntersDialog', self.enterDialogMode)
        self.accept('localAvatarExitsDialog', self.exitDialogMode)
        self.accept('Local_Efficiency_Set', self.setEfficiency)
        if localAvatar.duringDialog:
            self.enterDialogMode()
        self.setName(self.name)
        if base.config.GetBool('disable-player-collisions', 1):
            if self.battleTubeNodePaths:
                for np in self.battleTubeNodePaths:
                    np.node().setIntoCollideMask(np.node().getIntoCollideMask() & ~PiratesGlobals.WallBitmask)

            if not self.isLocal():
                self.collNode.setIntoCollideMask(np.node().getIntoCollideMask() & ~PiratesGlobals.WallBitmask)
        self.checkAttuneEffect()
        if base.launcher.getPhaseComplete(4):
            self.createConsumable()
        else:
            self.consumable = None
            self.accept('phaseComplete-4', self.handlePhaseComplete, extraArgs=[4])
        self.initVisibleToCamera()
        yieldThread('current Item')
        self.setEfficiency(localAvatar.getEfficiency())
        return

    def handlePhaseComplete(self, phase):
        if phase == 4:
            self.createConsumable()

    def createConsumable(self):
        self.consumable = Consumable.Consumable(ItemGlobals.TONIC)

    def setLocation(self, parentId, zoneId):
        DistributedBattleAvatar.setLocation(self, parentId, zoneId)

    def wrtReparentTo(self, parent):
        DistributedBattleAvatar.wrtReparentTo(self, parent)

    def setName(self, name):
        DistributedBattleAvatar.setName(self, name)
        self.refreshName()

    def setCrewIcon(self, iconId):
        self.sendUpdate('setCrewIconIndicator', [iconId])
        self.hasCrewIcon = iconId
        self.setCrewIconIndicator(iconId)

    def getCrewIcon(self):
        return self.hasCrewIcon

    def setCrewIconIndicator(self, iconId):
        if self.getDoId() != localAvatar.getDoId() and iconId != 0:
            if self.getDoId() not in localAvatar.guiMgr.crewHUD.crew:
                iconId = 2
        if iconId not in range(0, 3):
            return
        self.hasCrewIcon = iconId
        self.refreshName()
        minimapObj = self.getMinimapObject()
        if minimapObj:
            minimapObj

    def setBadgeIcon(self, titleId, rank):
        self.badge = (
         titleId, rank)
        if titleId < 0 or rank < 0:
            self.badge = None
        self.refreshName()
        return

    def setShipBadgeIcon(self, titleId, rank):
        self.shipBadge = (
         titleId, rank)
        if titleId < 0 or rank < 0:
            self.shipBadge = None
        return

    def sendRequestSetBadgeIcon(self, titleId, rank):
        self.sendUpdate('requestBadgeIcon', [titleId, rank])

    def sendRequestSetShipBadgeIcon(self, titleId, rank):
        self.sendUpdate('requestShipBadgeIcon', [titleId, rank])

    def setLastPVPSinkTime(self, timestamp):
        self.lastPVPSinkTime = timestamp

    def setLastShipPVPDecayTime(self, timestamp):
        self.lastShipPVPDecayTime = timestamp

    def setInfamySea(self, infamySea):
        messenger.send('infamySeaUpdated', [infamySea - self.infamySea])
        self.infamySea = infamySea
        self.setupInfamySeaDecay()

    def getInfamySea(self):
        return self.infamySea

    def setupInfamySeaDecay(self):
        timeNow = time.time()
        taskMgr.remove(self.uniqueName('decayInfamySea'))
        if not self.infamySea:
            return
        if timeNow - self.lastPVPSinkTime < PVPGlobals.SHIP_PVP_SINK_TIME_MAX:
            taskMgr.doMethodLater(PVPGlobals.SHIP_PVP_SINK_TIME_MAX - (timeNow - self.lastPVPSinkTime), self.decayInfamySea, self.uniqueName('decayInfamySea'))
        else:
            taskMgr.doMethodLater(PVPGlobals.SHIP_PVP_SINK_TIME_NEXT, self.decayInfamySea, self.uniqueName('decayInfamySea'))

    def decayInfamySea(self, task=None):
        infamyToRemove = self.infamySea * PVPGlobals.SHIP_PVP_INFAMY_DEC_PERCENT + PVPGlobals.SHIP_PVP_INFAMY_DEC_FLAT
        infamyToRemove = int(min(self.infamySea, infamyToRemove))
        messenger.send('infamySeaUpdated', [-infamyToRemove])
        self.infamySea -= infamyToRemove
        if self.infamySea:
            taskMgr.doMethodLater(PVPGlobals.SHIP_PVP_SINK_TIME_NEXT, self.decayInfamySea, self.uniqueName('decayInfamySea'))
        return Task.done

    def setLastPVPDefeatTime(self, timestamp):
        self.lastPVPDefeatTime = timestamp

    def setLastLandPVPDecayTime(self, timestamp):
        self.lastLandPVPDecayTime = timestamp

    def setInfamyLand(self, infamyLand):
        messenger.send('infamyLandUpdated', [infamyLand - self.infamyLand])
        self.infamyLand = infamyLand
        self.setupInfamyLandDecay()

    def getInfamyLand(self):
        return self.infamyLand

    def setupInfamyLandDecay(self):
        timeNow = time.time()
        taskMgr.remove(self.uniqueName('decayInfamyLand'))
        if not self.infamyLand:
            return
        if timeNow - self.lastPVPDefeatTime < PVPGlobals.LAND_PVP_DEFEAT_TIME_MAX:
            taskMgr.doMethodLater(PVPGlobals.LAND_PVP_DEFEAT_TIME_MAX - (timeNow - self.lastPVPDefeatTime), self.decayInfamyLand, self.uniqueName('decayInfamyLand'))
        else:
            taskMgr.doMethodLater(PVPGlobals.LAND_PVP_DEFEAT_TIME_NEXT, self.decayInfamyLand, self.uniqueName('decayInfamyLand'))

    def decayInfamyLand(self, task=None):
        infamyToRemove = self.infamyLand * PVPGlobals.LAND_PVP_INFAMY_DEC_PERCENT + PVPGlobals.LAND_PVP_INFAMY_DEC_FLAT
        infamyToRemove = int(min(self.infamyLand, infamyToRemove))
        messenger.send('infamyLandUpdated', [-infamyToRemove])
        self.infamyLand -= infamyToRemove
        if self.infamyLand:
            taskMgr.doMethodLater(PVPGlobals.LAND_PVP_DEFEAT_TIME_NEXT, self.decayInfamyLand, self.uniqueName('decayInfamyLand'))
        return Task.done

    def infamyRankSeaDecreaseMessage(self, oldRank, newRank):
        oldRankName = PLocalizer.PVPTitleSeaRanks[oldRank]
        newRankName = PLocalizer.PVPTitleSeaRanks[newRank]
        message = PLocalizer.PVPSeaRankDecreaseMessage % (oldRankName, newRankName)
        base.talkAssistant.receiveSystemMessage(message)

    def infamyRankLandDecreaseMessage(self, oldRank, newRank):
        oldRankName = PLocalizer.PVPTitleLandRanks[oldRank]
        newRankName = PLocalizer.PVPTitleLandRanks[newRank]
        message = PLocalizer.PVPLandRankDecreaseMessage % (oldRankName, newRankName)
        base.talkAssistant.receiveSystemMessage(message)

    def setStatus(self, status):
        self.isLookingForCrew = status & PiratesGlobals.STATUS_LFG
        self.isAFK = status & PiratesGlobals.STATUS_AFK
        self.refreshName()

    def d_refreshStatus(self):
        status = 0
        if self.isAFK:
            status += PiratesGlobals.STATUS_AFK
        if self.isLookingForCrew:
            status += PiratesGlobals.STATUS_LFG
        self.sendUpdate('setStatus', [status])

    def toggleLookingForCrewSign(self):
        try:
            localAvatar.guiMgr.crewHUD.toggleLookingForCrew()
        except:
            pass

    def setLookingForCrew(self, state):
        self.isLookingForCrew = state
        self.refreshName()
        self.d_refreshStatus()

    def getLookingForCrew(self):
        return self.isLookingForCrew

    def b_setAFK(self, isAFK):
        self.isAFK = isAFK
        self.d_setAFK(isAFK)
        self.refreshName()
        self.d_refreshStatus()

    def d_setAFK(self, isAFK):
        self.sendUpdate('setAFK', [isAFK])

    def refreshName(self):
        if not hasattr(base, 'localAvatar') or localAvatar.isDeleted():
            return None

        self.refreshStatusTray()
        if hasattr(self, 'nametag'):
            self.nametag.setName(self.getName())
            self.nametag.setDisplayName('        ')

        if self.guildName == '0' or self.guildName == '':
            guildName = PLocalizer.GuildDefaultName % self.guildId
        else:
            guildName = self.guildName
        nameText = self.getNameText()
        if nameText:
            level = self.getLevel()
            if self.inPvp and self != localAvatar:
                levelColor = self.cr.battleMgr.getExperienceColor(
                    base.localAvatar, self)
            else:
                levelColor = '\x01white\x01'
            x2XPTempAwardIndicator = ''
            if self.tempDoubleXPStatus:
                x2XPTempAwardIndicator = '\x05x2XPAwardIcon\x05'

            if self.guildName == PLocalizer.GuildNoGuild:
                text = '%s%s  \x01smallCaps\x01%s%s%s%s\x02\x02' % (
                    self.title, self.name, levelColor, PLocalizer.Lv, level, x2XPTempAwardIndicator)
            else:
                text = '%s%s  \x01smallCaps\x01%s%s%s%s\x02\x02\n\x01guildName\x01%s\x02' % (
                    self.title, self.name, levelColor, PLocalizer.Lv, level, x2XPTempAwardIndicator, guildName)
            nameText['text'] = text
            if Freebooter.getPaidStatus(self.doId):
                if self.getFounder():
                    nameText['fg'] = (1, 1, 1, 1)
                    nameText['font'] = PiratesGlobals.getPirateOutlineFont()
                    if not base.config.GetBool(
                            'want-land-infamy', 0) or base.config.GetBool('want-sea-infamy', 0):
                        nameText['text'] = '\x05goldFounderIcon\x05 \x01goldFounder\x01%s\x02' % text
                    else:
                        nameText['text'] = '\x01goldFounder\x01%s\x02' % text
                else:
                    nameText['fg'] = (
                        0.40000000000000002,
                        0.29999999999999999,
                        0.94999999999999996,
                        1)
                    nameText['font'] = PiratesGlobals.getPirateOutlineFont()
            else:
                nameText['fg'] = (0.5, 0.5, 0.5, 1)
            prefix = ''
            if self.injuredSetup and 0:
                if self.injuredTimeLeft:
                    prefix = '\x01injuredRedTimer\x01%s\x02\x01injuredRed\x01\n%s\x02\n' % PLocalizer.InjuredFlag
                else:
                    prefix = '\x01injuredRed\x01%s\x02\n' % PLocalizer.InjuredFlag
            elif base.cr.avatarFriendsManager.checkIgnored(self.doId):
                prefix = '\x01ignoredPink\x01%s\x02\n' % PLocalizer.IngoredFlag
            elif self.isAFK:
                prefix = '\x01afkGray\x01%s\x02\n' % PLocalizer.AFKFlag
            elif self.getLookingForCrew():
                prefix = '\x01crewPurple\x01%s\x02\n' % PLocalizer.CrewLookingForAd

            badges = ''
            if self.isConfused:
                prefix = '\x05confusedIcon\x05\n'
            elif self.badge and Freebooter.getPaidStatus(self.doId):
                if base.config.GetBool(
                        'want-land-infamy', 0) or base.config.GetBool('want-sea-infamy', 0):
                    if self.badge[0]:
                        textProp = TitleGlobals.Title2nametagTextProp[self.badge[0]]
                        if textProp == 'goldFounder':
                            if not Freebooter.getFounderStatus(self.doId):
                                pass
                            else:
                                badges += '\x01white\x01\x05badge-%s-%s\x05\x02 ' % (
                                    self.badge[0], 1)
                                nameText['text'] = '\x01%s\x01%s\x02' % (
                                    textProp, nameText['text'])
                        elif textProp:
                            badges += '\x01white\x01\x05badge-%s-%s\x05\x02 ' % (
                                self.badge[0], self.badge[1])
                            nameText['text'] = '\x01%s\x01%s\x02' % (
                                textProp, nameText['text'])
                        else:
                            badges += '\x01white\x01\x05badge-%s-%s\x05\x02 ' % (
                                self.badge[0], self.badge[1])

            nameText['text'] = prefix + badges + nameText['text']
            if self.isInvisibleGhost() or self.isInvisible():
                nameText['text'] = ''
                if not self.isLocal():
                    return None

            if self.getCrewIcon() and not (self.gmNameTagEnabled):
                if self.getCrewIcon() != 2:
                    oldLabelText = nameText['text']
                    nameText['text'] = '\x01white\x01\x05crewIcon%s\x05\x02\n%s' % (
                        self.hasCrewIcon, oldLabelText)

            if self.gmNameTagEnabled and self.isGM():
                if self.getCrewIcon():
                    nameText['text'] = '\x05gmNameTagLogo\x05\x01white\x01\x05crewIcon%s\x05\x02\n\x01%s\x01%s\x02\n%s' % (
                        self.hasCrewIcon, self.getGMNameTagColor(), self.gmNameTagString, nameText['text'])
                else:
                    nameText['text'] = '\x05gmNameTagLogo\x05\n\x01%s\x01%s\x02\n%s' % (
                        self.getGMNameTagColor(), self.gmNameTagString, nameText['text'])

    def setTutorialAck(self, tutorialAck):
        self.tutorialAck = tutorialAck

    def setEfficiency(self, efficiency):
        if self.efficiency != efficiency:
            self.efficiency = efficiency
            if self.efficiency:
                self.enableReducedMixing()
            else:
                self.enableMixing()
                if self.getGameState() == 'Injured':
                    self.loop('injured_idle', blendDelay=0.15)

    def b_setInInvasion(self, inInvasion):
        self.d_setInInvasion(inInvasion)
        self.setInInvasion(inInvasion)

    def d_setInInvasion(self, inInvasion):
        self.sendUpdate('setInInvasion', [inInvasion])

    def setInInvasion(self, inInvasion):
        self.inInvasion = inInvasion
        if inInvasion:
            if not base.config.GetBool('disable-player-collisions', 1):
                if self.battleTubeNodePaths:
                    for np in self.battleTubeNodePaths:
                        np.node().setIntoCollideMask(np.node().getIntoCollideMask() & ~PiratesGlobals.WallBitmask)

                if not self.isLocal():
                    self.collNode.setIntoCollideMask(np.node().getIntoCollideMask() & ~PiratesGlobals.WallBitmask)
            if not self.isLocal():
                self.enableReducedMixing()
        else:
            if not base.config.GetBool('disable-player-collisions', 1):
                if self.battleTubeNodePaths:
                    for np in self.battleTubeNodePaths:
                        np.node().setIntoCollideMask(np.node().getIntoCollideMask() | PiratesGlobals.WallBitmask)

                if not self.isLocal():
                    self.collNode.setIntoCollideMask(np.node().getIntoCollideMask() | PiratesGlobals.WallBitmask)
            if not self.isLocal():
                self.enableMixing()
                if self.getGameState() == 'Injured':
                    self.loop('injured_idle', blendDelay=0.15)

    def getInventoryId(self):
        return self.inventoryId

    def setInventoryId(self, inventoryId):
        self.inventoryId = inventoryId

    def getInventory(self):
        if not self:
            return None

        if not self.cr:
            return None

        inventory = self.cr.doId2do.get(self.inventoryId)
        if inventory:
            return inventory
        else:
            return None

        return None

    def getFriendsListId(self):
        pass

    def setFriendsListId(self, friendsListId):
        pass

    def getFriendsList(self):
        return self.avatarFriendsList

    def getAvatarFriendsList(self):
        return self.avatarFriendsList

    def getPlayerFriendsList(self):
        return self.playerFriendsList

    def getName(self):
        return self.title + self.name

    def setGuildName(self, newname):
        if not newname:
            self.guildName = PLocalizer.GuildNoGuild
        else:
            self.guildName = newname

        self.refreshName()

    def getGuildName(self):
        return self.guildName

    def setGuildRank(self, rank):
        self.guildRank = rank

    def getGuildRank(self):
        return self.guildRank

    def getGuildId(self):
        return self.guildId

    def setGuildId(self, guildId):
        self.guildId = guildId

    def getCrewMemberId(self):
        return self.crewMemberId

    def setCrewMemberId(self, crewMemberId):
        self.crewMemberId = crewMemberId

    def getDinghyId(self):
        return self.dinghyId

    def setDinghyId(self, dinghyId):
        self.dinghyId = dinghyId

    def getDinghy(self):
        return self.cr.doId2do.get(self.dinghyId)

    def setDNAString(self, dnaString):
        DistributedPirateBase.setDNAString(self, dnaString)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='shipboard')
    def b_setActiveShipId(self, shipId):
        self.d_setActiveShipId(shipId)
        self.setActiveShipId(shipId)

    @report(types=['frameCount', 'deltaStamp', 'args'], dConfigParam='shipboard')
    def d_setActiveShipId(self, shipId):
        self.sendUpdate('setActiveShipId', [shipId])

    @report(types=['deltaStamp', 'module', 'args'], dConfigParam='shipboard')
    def setActiveShipId(self, shipId):
        if shipId and localAvatar.getDoId() == self.getDoId():
            messenger.send('localAvatarToSea')
        elif not shipId and localAvatar.getDoId() == self.getDoId():
            messenger.send('localAvatarToLand')
        self.activeShipId = shipId

    def getActiveShip(self):
        return self.cr.doId2do.get(self.activeShipId)

    def getActiveShipId(self):
        return self.activeShipId

    @report(types=['deltaStamp', 'module', 'args'], dConfigParam='shipboard')
    def setCrewShipId(self, shipId):
        if self.pendingSetCrewShip:
            self.cr.relatedObjectMgr.abortRequest(self.pendingSetCrewShip)
            self.pendingSetCrewShip = None
        self.crewShipId = shipId
        if shipId:
            self.pendingSetCrewShip = self.cr.relatedObjectMgr.requestObjects([shipId], eachCallback=self._setCrewShip)
            messenger.send('localAvatarToSea')
        else:
            self._setCrewShip(None)
            messenger.send('localAvatarToLand')
        return

    def getCrewShipId(self):
        return self.crewShipId

    @report(types=['deltaStamp', 'module', 'args'], dConfigParam='shipboard')
    def _setCrewShip(self, ship):
        self.crewShip = ship

    def getCrewShip(self):
        return self.crewShip

    def printShips(self):
        print 'activeShip:\t', self.getActiveShipId(), self.getActiveShip()
        print 'crewShip:\t', self.getCrewShipId(), self.getCrewShip()
        print 'ship:\t\t', self.getShip(), self.getShip()

    def getShipString(self):
        return 'A: %s, C: %s, S: %s' % (self.getActiveShipId(), self.getCrewShipId(), self.getShipId())

    def hpChange(self, quietly=0):
        DistributedBattleAvatar.hpChange(self, quietly)

    def updateReputation(self, category, value):
        DistributedBattleAvatar.updateReputation(self, category, value)

    def useTargetedSkill(self, skillId, ammoSkillId, actualResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, itemEffects, timestamp, pos, charge=0, localSignal=0):
        targetEffects = list(targetEffects)
        attackerEffects = list(attackerEffects)
        DistributedBattleAvatar.useTargetedSkill(self, skillId, ammoSkillId, actualResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, itemEffects, timestamp, pos, charge, localSignal)

    def playSkillMovie(self, skillId, ammoSkillId, skillResult, charge=0, targetId=0, areaIdList=[]):
        DistributedBattleAvatar.playSkillMovie(self, skillId, ammoSkillId, skillResult, charge, targetId, areaIdList)

    @report(types=['deltaStamp', 'module', 'args'], dConfigParam='teleport')
    def forceTeleportStart(self, instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone):

        def effectDoneCallback():
            self.cr.teleportMgr.forceTeleportStart(instanceName, tzDoId, thDoId, worldGridDoId, tzParent, tzZone)

        self.acceptOnce('avatarTeleportEffect-done', effectDoneCallback)
        if self.cr.teleportMgr.stowawayEffect:
            self.setGameState('TeleportOut', timestamp=None, localArgs=['someBogusEventName', False])
            self.controlManager.collisionsOff()
            par = self.getParentObj()
            uid = par.getUniqueId()
            if uid == LocationIds.PORT_ROYAL_ISLAND:
                self.setPos(par, -93.5896, -362.238, 11.5197)
                self.setHpr(par, -118.823, 0, 0)
            elif uid == LocationIds.TORTUGA_ISLAND:
                self.setPos(par, 19.7727, -460.671, 4.24051)
                self.setHpr(par, -92.8273, 0, 0)
            elif uid == LocationIds.CUBA_ISLAND:
                self.setPos(par, -194.761, -764.573, 4.00303)
                self.setHpr(par, -172.742, 0, 0)
            elif uid == LocationIds.DEL_FUEGO_ISLAND:
                self.setPos(par, -1464.62, 385.615, 5.00972)
                self.setHpr(par, -22.449, 0, 0)

            def spiffyPlay():
                self.play('stowaway_get_in_crate', blendOutT=0.0)

            teleportTrack = Parallel(Func(spiffyPlay), Sequence(Wait(0.6), Func(base.transitions.fadeOut), Parallel(Sequence(Wait(0.5), SoundInterval(StowawayGUI.CrateShutSound, loop=0)), Sequence(Wait(3.0), Func(base.cr.loadingScreen.show, waitForLocation=True, disableSfx=False)))))
            teleportTrack.setDoneEvent('avatarTeleportEffect-done')
            teleportTrack.start()
        else:
            doEffect = self.cr.teleportMgr.doEffect and not self.testTeleportFlag(PiratesGlobals.TFInInitTeleport) and not self.testTeleportFlag(PiratesGlobals.TFInWater)
            if self.gameFSM.getCurrentOrNextState() != 'TeleportOut':
                self.b_setGameState('TeleportOut', ['avatarTeleportEffect-done', doEffect])
            else:
                messenger.send('avatarTeleportEffect-done')
        self.cr.teleportMgr.doEffect = True
        return

    @report(types=['deltaStamp', 'module', 'args'], dConfigParam='teleport')
    def relayTeleportLoc(self, shardId, zoneId, teleportMgrDoId):
        self.b_setDefaultShard(shardId)
        self.cr.playingGameLocReceived(shardId, self.doId)
        if self.pendingTeleportMgr:
            base.cr.relatedObjectMgr.abortRequest(self.pendingTeleportMgr)
            self.pendingTeleportMgr = None

        self.pendingTeleportMgr = base.cr.relatedObjectMgr.requestObjects([teleportMgrDoId], eachCallback=self.readyToTeleport)

    @report(types=['deltaStamp', 'module'], dConfigParam='teleport')
    def readyToTeleport(self, teleportMgr):
        teleportMgr.initiateTeleport(0, '', shardId=self.getDefaultShard(), locationUid=self.returnLocation)

    def requestActivityAccepted(self):
        self.guiMgr.lookoutPage.requestActivityAccepted()

    def lookoutMatchFound(self, timeToJoin, matchId):
        self.guiMgr.lookoutPage.matchFound(matchId, timeToJoin)

    def lookoutMatchFailed(self, restartRequest):
        self.guiMgr.lookoutPage.matchFailed(restartRequest)

    def lookoutFeedback(self, matchChance):
        self.guiMgr.lookoutPage.matchChance(matchChance)

    def beginningTeleport(self, instanceType, fromInstanceType, instanceName, gameType):
        base.cr.loadingScreen.showTarget()
        self.cr.teleportMgr.teleportHasBegun(instanceType, fromInstanceType, instanceName, gameType)
        self.guiMgr.lookoutPage.matchTeleport()

    def showContextTutPanel(self, contextId, number, type, part):
        if self.__tutorialEnabled == False:
            return
        if self.isLocal() and self.isInInvasion():
            return
        self.guiMgr.handleContextTutorial(contextId, number, type, part)

    def enableTutorial(self):
        self.__tutorialEnabled = True
        self.guiMgr.isTutEnabled = True

    def disableTutorial(self):
        self.__tutorialEnabled = False
        self.guiMgr.isTutEnabled = False
        if self.guiMgr.contextTutPanel.isHidden() == False:
            self.guiMgr.contextTutPanel.hide()

    def informMissedLoot(self, lootType, reason):
        pass

    def setLootCarried(self, amt, maxCarry):
        self.lootCarried = amt

    def startTimer(self, time, timestamp, mode=None):
        if config.GetBool('hide-gui', 0):
            return
        if self == localAvatar:
            self.timerTimestamp = timestamp
            if time:
                ts = globalClockDelta.localElapsedTime(timestamp)
                newTime = time - ts
                if newTime > 0:
                    if mode == PiratesGlobals.HIGHSEAS_ADV_START:
                        pass
                    elif mode in [PiratesGlobals.SHIP_SELECTION_TIMER, PiratesGlobals.SHIP_BOARD_TIMER, PiratesGlobals.SHIP_DOCK_TIMER]:
                        self.guiMgr.setTimer(newTime, mode=mode)
                    else:
                        self.guiMgr.setTimer(newTime)
                else:
                    self.guiMgr.timerExpired()
            else:
                self.guiMgr.timerExpired()

    def cancelTimer(self, mode):
        self.guiMgr.cancelTimer(mode)

    def endMissionPanel(self, missionData, playerData):
        if config.GetBool('hide-gui', 0):
            return
        portName = ''
        if base.localAvatar.ship and not base.localAvatar.ship.getSiegeTeam():
            self.guiMgr.createHighSeasScoreboard(portName, missionData, playerData, base.localAvatar.ship)

    def endInvasionPanel(self, holidayId, wonInvasion, repEarned, enemiesKilled, barricadesSaved, wavesCleared):
        if config.GetBool('hide-gui', 0):
            return
        taskMgr.doMethodLater(8.0, self.guiMgr.createInvasionScoreboard, self.uniqueName('createInvasionScoreboard'), [
         holidayId, wonInvasion, repEarned, enemiesKilled, barricadesSaved, wavesCleared])

    def createTitle(self, textIndex):
        base.localAvatar.guiMgr.createTitle(textIndex)

    def sendCancelMission(self):
        self.sendUpdate('cancelMission')

    def loop(self, *args, **kwArgs):
        if self.creature and len(args) > 1:
            if args[0] in ['spin_left', 'spin_right', 'run', 'strafe_left', 'strafe_right']:
                args = (
                 'walk', args[1])
            self.creature.loop(*args, **kwArgs)
        else:
            Biped.Biped.loop(self, *args, **kwArgs)

    def play(self, *args, **kwArgs):
        Biped.Biped.play(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        Biped.Biped.pingpong(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        Biped.Biped.pose(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        Biped.Biped.stop(self, *args, **kwArgs)

    def putAwayCurrentWeapon(self, blendInT=0.1, blendOutT=0.1):
        self.setStickyTargets([])
        return DistributedBattleAvatar.putAwayCurrentWeapon(self, blendInT, blendOutT)

    def setStickyTargets(self, avList):
        self.stickyTargets = avList
        self.checkAttuneEffect()
        localAvatar.guiMgr.attuneSelection.update()

    def checkAttuneEffect(self):
        if not self.isGenerated():
            return
        if self.stickyTargets:
            if not self.attuneEffect:
                self.attuneEffect = VoodooAura.getEffect()
            if self.attuneEffect:
                self.attuneEffect.reparentTo(self.rightHandNode)
                self.attuneEffect.setPos(0, 0, 0)
                self.attuneEffect.particleDummy.reparentTo(self.rightHandNode)
                self.attuneEffect.startLoop()
                hasFriendly = 0
                hasEnemies = 0
                for targetId in self.stickyTargets:
                    target = self.cr.doId2do.get(targetId)
                    if target:
                        if TeamUtils.damageAllowed(self, target):
                            hasEnemies = 1
                        else:
                            hasFriendly = 1

                if hasFriendly and not hasEnemies:
                    self.attuneEffect.setEffectColor(Vec4(0.2, 0.5, 0.1, 1))
                elif hasEnemies and not hasFriendly:
                    self.attuneEffect.setEffectColor(Vec4(0.2, 0.1, 0.5, 1))
                elif hasEnemies and hasFriendly:
                    self.attuneEffect.setEffectColor(Vec4(0, 0.15, 0.15, 1))
        elif self.attuneEffect:
            self.attuneEffect.stopLoop()
            self.attuneEffect = None
        return

    def getStickyTargets(self):
        return self.stickyTargets

    def addStickyTarget(self, avId):
        if avId not in self.stickyTargets:
            self.stickyTargets.append(avId)
            self.setStickyTargets(self.stickyTargets)
            localAvatar.guiMgr.attuneSelection.update()

    def sendRequestRemoveStickyTargets(self, doIdList):
        self.sendUpdate('requestRemoveEffects', [doIdList])

    def sendRequestRemoveEffects(self, doIdList):
        self.sendUpdate('requestRemoveEffects', [doIdList])

    def hasStickyTargets(self):
        return self.stickyTargets

    def getFriendlyStickyTargets(self):
        avIdList = []
        for avId in self.stickyTargets:
            av = self.cr.doId2do.get(avId)
            if av:
                if not TeamUtils.damageAllowed(av, self):
                    avIdList.append(avId)

        return avIdList

    def getHostileStickyTargets(self):
        avIdList = []
        for avId in self.stickyTargets:
            av = self.cr.doId2do.get(avId)
            if av:
                if TeamUtils.damageAllowed(self, av):
                    avIdList.append(avId)

        return avIdList

    def sendRequestAuraDetection(self, doIdList):
        self.sendUpdate('requestAuraDetection', [doIdList])

    def sendRequestRemoveAuraDetection(self):
        self.sendUpdate('requestRemoveAuraDetection')

    def sendClothingMessage(self, clothingId, colorId):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=0, card=0, cloth=clothingId, color=colorId)

    def sendLootMessage(self, lootId):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=lootId)

    def sendCardMessage(self, cardId):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=0, card=cardId)

    def sendWeaponMessage(self, weapon):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=0, weapon=weapon)

    def sendJewelryMessage(self, jewelryUID):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=0, jewel=jewelryUID)

    def sendTattooMessage(self, tattooUID):
        localAvatar.guiMgr.messageStack.showLoot([], gold=0, collect=0, tattoo=tattooUID)

    def sendReputationMessage(self, targetId, categories, reputationList, basicPenalty, crewBonus, doubleXPBonus, holidayBonus, potionBonus):
        target = base.cr.doId2do.get(targetId)
        if target:
            totalWeaponRep = 0
            for i in range(len(categories)):
                if categories[i] != InventoryType.OverallRep:
                    totalWeaponRep += reputationList[i]

            overallRep = 0
            if categories.count(InventoryType.OverallRep):
                overallRepIndex = categories.index(InventoryType.OverallRep)
                overallRep = reputationList[overallRepIndex]
            totalRep = max(totalWeaponRep, overallRep)
            colorSetting = 4
            if InventoryType.GeneralRep in categories:
                colorSetting = 5
            target.printExpText(totalRep, colorSetting, basicPenalty, crewBonus, doubleXPBonus, holidayBonus, potionBonus)

    def sendRenownMessage(self, targetId, landRenown, seaRenown, killStreakLevel, killStreakBonus):
        target = base.cr.doId2do.get(targetId)
        renown = max(landRenown, seaRenown)
        if target:
            colorSetting = 7
            if landRenown:
                colorSetting = 8
            if hasattr(target, 'printExpText'):
                target.printExpText(renown, colorSetting, 0, 0, 0, 0, 0)
        if self.getShip() and self.getShip().renownDisplay:
            prevRank = TitleGlobals.getRank(TitleGlobals.ShipPVPTitle, self.getInfamySea())
            newRank = TitleGlobals.getRank(TitleGlobals.ShipPVPTitle, self.getInfamySea() + renown)
            if prevRank < newRank:
                self.levelUpMsg(InventoryType.PVPTotalInfamySea, newRank, 0)
            if killStreakLevel:
                textTitle = PLocalizer.PVPSinkStreak1
                if killStreakLevel == 1:
                    textTitle = PLocalizer.PVPSinkStreak1
                elif killStreakLevel == 2:
                    textTitle = PLocalizer.PVPSinkStreak2
                elif killStreakLevel == 3:
                    textTitle = PLocalizer.PVPSinkStreak3
                textSecondarytitle = '+%d ' % (killStreakBonus,) + PLocalizer.PVPInfamySea
                base.localAvatar.guiMgr.createTitle(textTitle)
                base.localAvatar.guiMgr.createSecondaryTitle(textSecondarytitle)
        elif self.isLocal() and self.guiMgr and self.guiMgr.pvpPanel and hasattr(self.guiMgr.pvpPanel, 'renownDisplay') and self.guiMgr.pvpPanel.renownDisplay:
            prevRank = TitleGlobals.getRank(TitleGlobals.LandPVPTitle, self.getInfamyLand())
            newRank = TitleGlobals.getRank(TitleGlobals.LandPVPTitle, self.getInfamyLand() + renown)
            if prevRank < newRank:
                self.levelUpMsg(InventoryType.PVPTotalInfamyLand, newRank, 0)
            if killStreakLevel:
                textTitle = PLocalizer.PVPSinkStreak1
                textSecondarytitle = '+%d ' % (killStreakBonus,) + PLocalizer.PVPInfamySea
                base.localAvatar.guiMgr.createTitle(textTitle)
                base.localAvatar.guiMgr.createSecondaryTitle(textSecondarytitle)
        if localAvatar.guiMgr and hasattr(localAvatar.guiMgr, 'titlesPage') and localAvatar.guiMgr.titlesPage:
            taskMgr.doMethodLater(1.4, localAvatar.guiMgr.titlesPage.refresh, 'titles-refresh', [])
        self.refreshName()

    def sendSalvageMessage(self, targetId, amount):
        target = base.cr.doId2do.get(targetId)
        if target:
            colorSetting = 9
            if hasattr(target, 'printExpText'):
                target.printExpText(amount, colorSetting, 0, 0, 0, 0, 0)
        self.refreshName()

    def __cleanupPopupDialog(self, value=None):
        if self.popupDialog:
            self.popupDialog.destroy()
            self.popupDialog = None
        return

    def sendFreeInventoryMessage(self, type):
        if not self.popupDialog:
            if type == InventoryType.ItemTypeWeapon or type == InventoryType.ItemTypeCharm:
                text = PLocalizer.FreeWeaponInventoryMessage
            elif type == InventoryType.ItemTypeClothing:
                text = PLocalizer.FreeClothingInventoryMessage
            elif type == InventoryType.ItemTypeJewelry:
                text = PLocalizer.FreeJewelryInventoryMessage
            elif type == InventoryType.ItemTypeTattoo:
                text = PLocalizer.FreeTattooInventoryMessage
            self.popupDialog = PDialog.PDialog(text=text, style=OTPDialog.Acknowledge, command=self.__cleanupPopupDialog)

    def sendFailedLootTradeMessage(self, tellAgain):
        if tellAgain:
            text = PLocalizer.FailedLootTradeTryAgainMessage
        else:
            text = PLocalizer.FailedLootTradeMessage
        self.guiMgr.createWarning(text, PiratesGuiGlobals.TextFG6, duration=10)

    def setLevel(self, level):
        DistributedBattleAvatar.setLevel(self, level)
        self.refreshName()

    def getLevel(self):
        return self.level

    def levelUpMsg(self, category, level, messageId):
        isSupressed = category in self.__surpressedRepFlags
        if self.isLocal():
            if isSupressed == False:
                self.guiMgr.bufferLevelUpText(category, level)
                messenger.send('weaponChange')
                if self.isLocal():
                    messenger.send('localLevelUp')
                if category == InventoryType.DefenseCannonRep:
                    messenger.send('defenseCannonLevelUp', [level])
        if isSupressed == False:
            self.playLevelUpEffect()

    def surpressRepFlag(self, flag):
        self.__surpressedRepFlags.append(flag)

    def clearRepFlags(self):
        self.__surpressedRepFlags = []

    def playLevelUpEffect(self):
        effect = LevelUpEffect.getEffect()
        if effect:
            effect.reparentTo(self)
            effect.particleDummy.reparentTo(self)
            effect.setPos(0, 0, 0)
            effect.play()

    @report(types=['frameCount', 'args'], dConfigParam='login')
    def b_setDefaultShard(self, defaultShard):
        if self.defaultShard != defaultShard:
            self.d_setDefaultShard(defaultShard)
            self.setDefaultShard(defaultShard)

    @report(types=['frameCount', 'args'], dConfigParam='login')
    def d_setDefaultShard(self, defaultShard):
        self.sendUpdate('setDefaultShard', [defaultShard])

    @report(types=['frameCount', 'args'], dConfigParam='login')
    def setDefaultShard(self, defaultShard):
        self.defaultShard = defaultShard

    @report(types=['frameCount'], dConfigParam='login')
    def getDefaultShard(self):
        return self.defaultShard

    def setDefaultZone(self, zone):
        self.defaultZone = zone

    @report(types=['frameCount', 'args'], dConfigParam='jail')
    def d_requestReturnLocation(self, locationDoId):
        self.sendUpdate('requestReturnLocation', [locationDoId])

    @report(types=['frameCount', 'args'], dConfigParam='jail')
    def setReturnLocation(self, returnLocation):
        if __dev__ and not getBase().config.GetBool('login-location-used-setRetLoc', False):
            ConfigVariableBool('login-location-used-setRetLoc').setValue(True)
            config_location = getBase().config.GetString('login-location', '').lower()
            config_location_uid = PLocalizer.LocationUids.get(config_location)
            if config_location and config_location_uid:
                returnLocation = config_location_uid

        if returnLocation == '1142018473.22dxschafe':
            returnLocation = LocationIds.DEL_FUEGO_ISLAND

        self.returnLocation = returnLocation

    @report(types=['frameCount'], dConfigParam='jail')
    def getReturnLocation(self):
        return self.returnLocation

    @report(types=['frameCount', 'args'], dConfigParam='map')
    def d_requestCurrentIsland(self, locationDoId):
        self.sendUpdate('requestCurrentIsland', [locationDoId])

    @report(types=['frameCount', 'args'], dConfigParam='map')
    def setCurrentIsland(self, islandUid):
        self.currentIsland = islandUid

    @report(types=['frameCount'], dConfigParam='jail')
    def getCurrentIsland(self):
        return self.currentIsland

    @report(types=['frameCount', 'args'], dConfigParam='jail')
    def setJailCellIndex(self, index):
        self.jailCellIndex = index
        if self.belongsInJail():
            self.b_setTeleportFlag(PiratesGlobals.TFInJail)
        else:
            self.b_clearTeleportFlag(PiratesGlobals.TFInJail)

    @report(types=['frameCount'], dConfigParam='jail')
    def getJailCellIndex(self):
        return self.jailCellIndex

    def belongsInJail(self):
        return bool(self.jailCellIndex)

    def addTransformationCollisions(self):
        if self.cRay == None:
            self.cRay = CollisionRay(0.0, 0.0, 4000.0, 0.0, 0.0, -1.0)
            self.cRayNode = CollisionNode(self.taskName('cRay'))
            self.cRayNode.addSolid(self.cRay)
            self.cRayNode.setFromCollideMask(PiratesGlobals.FloorBitmask | PiratesGlobals.ShipFloorBitmask)
            self.cRayNode.setIntoCollideMask(BitMask32.allOff())
            self.cRayNode.setBounds(BoundingSphere())
            self.cRayNode.setFinal(1)
            self.cRayNodePath = self.attachNewNode(self.cRayNode)
            self.creatureQueue = CollisionHandlerQueue()
            base.cTrav.addCollider(self.cRayNodePath, self.creatureQueue)
        return

    def removeTransformationCollisions(self):
        if self.cRayNodePath:
            base.cTrav.removeCollider(self.cRayNodePath)
            self.cRayNodePath.removeNode()
            self.cRayNodePath = None
        if self.cRayNode:
            self.cRayNode = None
        if self.cRay:
            self.cRay = None
        if self.creatureQueue:
            self.creatureQueue = None
        return

    def transformationTrackTerrain(self, task):
        if self.creatureTransformation:
            base.cTrav.traverse(render)
            if self.creatureQueue.getNumEntries() > 0:
                self.creatureQueue.sortEntries()
                collEntry = self.creatureQueue.getEntry(0)
                self.floorNorm = collEntry.getInto().getNormal()
            gNode = self.creature
            if gNode and not gNode.isEmpty():
                if self.gTransNodeFwdPt == None:
                    self.gTransNodeFwdPt = gNode.getRelativePoint(self, Point3(0, 1, 0))
                gNode.headsUp(self.gTransNodeFwdPt, self.getRelativeVector(self.getParentObj(), self.floorNorm))
        return Task.cont

    def getCreatureTransformation(self):
        return (
         self.creatureTransformation, self.creatureId)

    def setupCreature(self, avatarType):
        if not self.creature:
            self.creature = DistributedCreature.CreatureTypes[avatarType.getNonBossType()]()
            self.creature.setAvatarType(avatarType)
            self.creature.getGeomNode().setH(-180)
            parent = self.find('**/actorGeom')
            self.creature.reparentTo(parent)
            self.creature.loop('idle')
            maxLevel = EnemyGlobals.getMinEnemyLevel(avatarType)
            enemyScale = EnemyGlobals.getEnemyScaleByType(avatarType, maxLevel)
            self.creature.setAvatarScale(self.creature.scale * enemyScale)
            if base.options.getCharacterDetailSetting() == 0:
                self.creature.getLODNode().forceSwitch(2)

    def deleteCreature(self):
        if self.creature:
            self.creature.detachNode()
            self.creature.delete()
            self.creature = None
        return

    def _setCreatureTransformation(self, value, effectId):
        if self.creatureTransformation == value:
            return
        self.creatureTransformation = value
        self.creatureId = effectId
        geom = self.getGeomNode()
        if value:
            self.addTransformationCollisions()
            taskMgr.add(self.transformationTrackTerrain, self.uniqueName('transformationTrackTerrain'))
            if effectId == PotionGlobals.C_CRAB_TRANSFORM:
                self.setupCreature(AvatarTypes.RockCrab)
            elif effectId == PotionGlobals.C_ALLIGATOR_TRANSFORM:
                self.setupCreature(AvatarTypes.Alligator)
            elif effectId == PotionGlobals.C_SCORPION_TRANSFORM:
                self.setupCreature(AvatarTypes.Scorpion)
            self.deleteDropShadow()
            geom.stash()
        else:
            self.removeTransformationCollisions()
            taskMgr.remove(self.uniqueName('transformationTrackTerrain'))
            geom.setHpr(Vec3(180, 0, 0))
            self.initializeDropShadow()
            self.deleteCreature()
            geom.unstash()

    def playTransformationToCreature(self, effectId):
        from pirates.effects.JRSpawn import JRSpawn
        if self.transformationEffect:
            self.transformationEffect.detachNode()
            self.transformationEffect = None
        if self.transformationIval:
            self.transformationIval.clearToInitial()
            self.transformationIval = None
        self.transformationEffect = JRSpawn.getEffect()
        if self.transformationEffect:
            self.transformationEffect.reparentTo(self)
            self.transformationEffect.setPos(0, 1, 0)
            self.transformationIval = Sequence(Func(self.motionFSM.off), Func(self.transformationEffect.play), Func(self.play, 'death3'), Wait(1.7), Func(self._setCreatureTransformation, True, effectId), Func(self.motionFSM.on))
            self.transformationIval.start()
        return

    def playTransformationToPirate(self, effectId):
        from pirates.effects.JRSpawn import JRSpawn
        if self.transformationEffect:
            self.transformationEffect.detachNode()
            self.transformationEffect = None
        if self.transformationIval:
            self.transformationIval.clearToInitial()
            self.transformationIval = None
        self.transformationEffect = JRSpawn.getEffect()
        if self.transformationEffect:
            self.transformationEffect.reparentTo(self)
            self.transformationEffect.setPos(0, 1, 0)
            self.transformationIval = Sequence(name='transformationIval')
            if self.doLongHumanTransform():
                self.transformationIval.append(Func(self.motionFSM.off))
            self.transformationIval.append(Func(self.transformationEffect.play))
            self.transformationIval.append(Func(self._setCreatureTransformation, False, effectId))
            if self.doLongHumanTransform():
                self.transformationIval.append(Func(self.play, 'jail_standup', fromFrame=65))
                self.transformationIval.append(Wait(1.7))
                self.transformationIval.append(Func(self.motionFSM.on))
            self.transformationIval.start()
        return

    def doLongHumanTransform(self):
        state = self.gameFSM.getCurrentOrNextState()
        if state in ('WaterRoam', 'WaterTreasureRoam', 'TeleportOut', 'ShipBoarding',
                     'EnterTunnel'):
            return False
        else:
            return True

    def setCreatureTransformation(self, value, effectId):
        if self.creatureTransformation == value:
            return
        if value:
            self.playTransformationToCreature(effectId)
        else:
            self.playTransformationToPirate(effectId)

    def addTransformationCollisions(self):
        if self.cRay == None:
            self.cRay = CollisionRay(0.0, 0.0, 4000.0, 0.0, 0.0, -1.0)
            self.cRayNode = CollisionNode(self.taskName('cRay'))
            self.cRayNode.addSolid(self.cRay)
            self.cRayNode.setFromCollideMask(PiratesGlobals.FloorBitmask | PiratesGlobals.ShipFloorBitmask)
            self.cRayNode.setIntoCollideMask(BitMask32.allOff())
            self.cRayNode.setBounds(BoundingSphere())
            self.cRayNode.setFinal(1)
            self.cRayNodePath = self.attachNewNode(self.cRayNode)
            self.creatureQueue = CollisionHandlerQueue()
            base.cTrav.addCollider(self.cRayNodePath, self.creatureQueue)
        return

    def removeTransformationCollisions(self):
        if self.cRayNodePath:
            base.cTrav.removeCollider(self.cRayNodePath)
            self.cRayNodePath.removeNode()
            self.cRayNodePath = None
        if self.cRayNode:
            self.cRayNode = None
        if self.cRay:
            self.cRay = None
        if self.creatureQueue:
            self.creatureQueue = None
        return

    def transformationTrackTerrain(self, task):
        if self.gameFSM.state == 'WaterRoam':
            self.creature.setP(0)
            self.creature.setR(0)
            return Task.cont
        if not isinstance(self.getParentObj(), NodePath):
            return Task.cont
        if self.creatureTransformation:
            base.cTrav.traverse(render)
            if self.creatureQueue.getNumEntries() > 0:
                self.creatureQueue.sortEntries()
                collEntry = self.creatureQueue.getEntry(0)
                self.floorNorm = collEntry.getInto().getNormal()
            gNode = self.creature
            if gNode and not gNode.isEmpty():
                if self.gTransNodeFwdPt == None:
                    self.gTransNodeFwdPt = gNode.getRelativePoint(self, Point3(0, 1, 0))
                gNode.headsUp(self.gTransNodeFwdPt, self.getRelativeVector(self.getParentObj(), self.floorNorm))
        return Task.cont

    def getCreatureTransformation(self):
        return (
         self.creatureTransformation, self.creatureId)

    def setupCreature(self, avatarType):
        if not self.creature:
            self.creature = DistributedCreature.CreatureTypes[avatarType.getNonBossType()]()
            self.creature.setAvatarType(avatarType)
            self.creature.getGeomNode().setH(-180)
            parent = self.find('**/actorGeom')
            self.creature.reparentTo(parent)
            self.creature.loop('idle')
            maxLevel = EnemyGlobals.getMinEnemyLevel(avatarType)
            enemyScale = EnemyGlobals.getEnemyScaleByType(avatarType, maxLevel)
            self.creature.setAvatarScale(self.creature.scale * enemyScale)
            if base.options.getCharacterDetailSetting() == 0:
                self.creature.getLODNode().forceSwitch(2)
                self.creature.shadowPlacer.on()

    def deleteCreature(self):
        if self.creature:
            self.creature.detachNode()
            self.creature.delete()
            self.creature = None
        return

    def _setCreatureTransformation(self, value, effectId):
        if self.creatureTransformation == value:
            return
        self.creatureTransformation = value
        self.creatureId = effectId
        geom = self.getGeomNode()
        if value:
            self.addTransformationCollisions()
            taskMgr.add(self.transformationTrackTerrain, self.uniqueName('transformationTrackTerrain'))
            if effectId == PotionGlobals.C_CRAB_TRANSFORM:
                self.setupCreature(AvatarTypes.RockCrab)
            elif effectId == PotionGlobals.C_ALLIGATOR_TRANSFORM:
                self.setupCreature(AvatarTypes.BayouGator)
                self.creature.setToNormal()
            elif effectId == PotionGlobals.C_SCORPION_TRANSFORM:
                self.setupCreature(AvatarTypes.Scorpion)
            self.deleteDropShadow()
            geom.stash()
            self.motionFSM.avHeight = 1
        else:
            self.removeTransformationCollisions()
            taskMgr.remove(self.uniqueName('transformationTrackTerrain'))
            geom.setHpr(Vec3(180, 0, 0))
            self.initializeDropShadow()
            self.deleteCreature()
            geom.unstash()
            self.motionFSM.avHeight = 5

    def playTransformationToCreature(self, effectId, timeSince=0):
        from pirates.effects.JRSpawn import JRSpawn
        if self.transformationEffect:
            self.transformationEffect.detachNode()
            self.transformationEffect = None
        if self.transformationIval:
            self.transformationIval.clearToInitial()
            self.transformationIval = None

        def startSFX(effectId):
            sfx = None
            if effectId == PotionGlobals.C_CRAB_TRANSFORM:
                sfx = self.crabSound
            else:
                if effectId == PotionGlobals.C_ALLIGATOR_TRANSFORM:
                    sfx = self.alligatorSound
                elif effectId == PotionGlobals.C_SCORPION_TRANSFORM:
                    sfx = self.scorpionSound
                if sfx:
                    base.playSfx(sfx, node=self, cutoff=100)
            return

        if timeSince > 1.5 or self.gameFSM.state not in ['LandRoam', 'Battle']:
            self.transformationIval = Func(self._setCreatureTransformation, True, effectId)
        else:
            self.transformationEffect = JRSpawn.getEffect()
            if self.transformationEffect:
                self.transformationEffect.reparentTo(self)
                self.transformationEffect.setPos(0, 1, 0)
                self.transformationIval = Sequence(Func(self.motionFSM.off, lock=True), Func(startSFX, effectId), Func(self.transformationEffect.play), Func(self.play, 'death3'), Wait(1.7), Func(self._setCreatureTransformation, True, effectId), Func(self.motionFSM.on, unlock=True))
        self.transformationIval.start()
        return

    def playTransformationToPirate(self, effectId):
        from pirates.effects.JRSpawn import JRSpawn

        def startSFX():
            sfx = self.genericTransformation
            if sfx:
                base.playSfx(sfx, node=self, cutoff=100)

        if self.transformationEffect:
            self.transformationEffect.detachNode()
            self.transformationEffect = None
        if self.transformationIval:
            self.transformationIval.clearToInitial()
            self.transformationIval = None
        if self.gameFSM.state not in ['LandRoam', 'Battle']:
            self.transformationIval = Func(self._setCreatureTransformation, False, effectId)
        else:
            self.transformationEffect = JRSpawn.getEffect()
            if self.transformationEffect:
                self.transformationEffect.reparentTo(self)
                self.transformationEffect.setPos(0, 1, 0)
                self.transformationIval = Sequence(name='transformationIval')
                if self.doLongHumanTransform():
                    self.transformationIval.append(Func(self.motionFSM.off))
                self.transformationIval.append(Func(startSFX))
                self.transformationIval.append(Func(self.transformationEffect.play))
                self.transformationIval.append(Func(self._setCreatureTransformation, False, effectId))
                if self.doLongHumanTransform():
                    self.transformationIval.append(Func(self.play, 'jail_standup', fromFrame=65))
                    self.transformationIval.append(Wait(1.7))
                    self.transformationIval.append(Func(self.motionFSM.on))
        self.transformationIval.start()
        return

    def doLongHumanTransform(self):
        state = self.gameFSM.getCurrentOrNextState()
        if state in ('WaterRoam', 'WaterTreasureRoam', 'TeleportOut', 'ShipBoarding',
                     'EnterTunnel'):
            return False
        else:
            return True

    def setCreatureTransformation(self, value, effectId, timeSince=0):
        if self.creatureTransformation == value:
            return
        if value:
            self.playTransformationToCreature(effectId, timeSince)
        else:
            self.playTransformationToPirate(effectId)

    def addTransformationCollisions(self):
        if self.cRay == None:
            self.cRay = CollisionRay(0.0, 0.0, 4000.0, 0.0, 0.0, -1.0)
            self.cRayNode = CollisionNode(self.taskName('cRay'))
            self.cRayNode.addSolid(self.cRay)
            self.cRayNode.setFromCollideMask(PiratesGlobals.FloorBitmask | PiratesGlobals.ShipFloorBitmask)
            self.cRayNode.setIntoCollideMask(BitMask32.allOff())
            self.cRayNode.setBounds(BoundingSphere())
            self.cRayNode.setFinal(1)
            self.cRayNodePath = self.attachNewNode(self.cRayNode)
            self.creatureQueue = CollisionHandlerQueue()
            base.cTrav.addCollider(self.cRayNodePath, self.creatureQueue)
        return

    def removeTransformationCollisions(self):
        if self.cRayNodePath:
            base.cTrav.removeCollider(self.cRayNodePath)
            self.cRayNodePath.removeNode()
            self.cRayNodePath = None
        if self.cRayNode:
            self.cRayNode = None
        if self.cRay:
            self.cRay = None
        if self.creatureQueue:
            self.creatureQueue = None
        return

    def transformationTrackTerrain(self, task):
        if self.gameFSM.state == 'WaterRoam':
            self.creature.setP(0)
            self.creature.setR(0)
            return Task.cont
        if not isinstance(self.getParentObj(), NodePath):
            return Task.cont
        if self.creatureTransformation:
            base.cTrav.traverse(render)
            if self.creatureQueue.getNumEntries() > 0:
                self.creatureQueue.sortEntries()
                collEntry = self.creatureQueue.getEntry(0)
                self.floorNorm = collEntry.getInto().getNormal()
            gNode = self.creature
            if gNode and not gNode.isEmpty():
                if self.gTransNodeFwdPt == None:
                    self.gTransNodeFwdPt = gNode.getRelativePoint(self, Point3(0, 1, 0))
                gNode.headsUp(self.gTransNodeFwdPt, self.getRelativeVector(self.getParentObj(), self.floorNorm))
        return Task.cont

    def getCreatureTransformation(self):
        return (
         self.creatureTransformation, self.creatureId)

    def setupCreature(self, avatarType):
        if not self.creature:
            self.creature = DistributedCreature.CreatureTypes[avatarType.getNonBossType()]()
            self.creature.setAvatarType(avatarType)
            self.creature.getGeomNode().setH(-180)
            parent = self.find('**/actorGeom')
            self.creature.reparentTo(parent)
            self.creature.loop('idle')
            maxLevel = EnemyGlobals.getMinEnemyLevel(avatarType)
            enemyScale = EnemyGlobals.getEnemyScaleByType(avatarType, maxLevel)
            self.creature.setAvatarScale(self.creature.scale * enemyScale)
            if base.options.getCharacterDetailSetting() == 0:
                self.creature.getLODNode().forceSwitch(2)
                self.creature.shadowPlacer.on()

    def deleteCreature(self):
        if self.creature:
            self.creature.detachNode()
            self.creature.delete()
            self.creature = None
        return

    def _setCreatureTransformation(self, value, effectId):
        if self.creatureTransformation == value:
            return
        self.creatureTransformation = value
        self.creatureId = effectId
        geom = self.getGeomNode()
        if value:
            self.addTransformationCollisions()
            taskMgr.add(self.transformationTrackTerrain, self.uniqueName('transformationTrackTerrain'))
            if effectId == PotionGlobals.C_CRAB_TRANSFORM:
                self.setupCreature(AvatarTypes.RockCrab)
            elif effectId == PotionGlobals.C_ALLIGATOR_TRANSFORM:
                self.setupCreature(AvatarTypes.BayouGator)
                self.creature.setToNormal()
            elif effectId == PotionGlobals.C_SCORPION_TRANSFORM:
                self.setupCreature(AvatarTypes.Scorpion)
            self.deleteDropShadow()
            geom.stash()
            self.motionFSM.avHeight = 1
        else:
            self.removeTransformationCollisions()
            taskMgr.remove(self.uniqueName('transformationTrackTerrain'))
            geom.setHpr(Vec3(180, 0, 0))
            self.initializeDropShadow()
            self.deleteCreature()
            geom.unstash()
            self.motionFSM.avHeight = 5

    def playTransformationToCreature(self, effectId, timeSince=0):
        from pirates.effects.JRSpawn import JRSpawn
        if self.transformationEffect:
            self.transformationEffect.detachNode()
            self.transformationEffect = None
        if self.transformationIval:
            self.transformationIval.clearToInitial()
            self.transformationIval = None

        def startSFX(effectId):
            sfx = None
            if effectId == PotionGlobals.C_CRAB_TRANSFORM:
                sfx = self.crabSound
            else:
                if effectId == PotionGlobals.C_ALLIGATOR_TRANSFORM:
                    sfx = self.alligatorSound
                elif effectId == PotionGlobals.C_SCORPION_TRANSFORM:
                    sfx = self.scorpionSound
                if sfx:
                    base.playSfx(sfx, node=self, cutoff=100)
            return

        if timeSince > 1.5 or self.gameFSM.state not in ['LandRoam', 'Battle']:
            self.transformationIval = Func(self._setCreatureTransformation, True, effectId)
        else:
            self.transformationEffect = JRSpawn.getEffect()
            if self.transformationEffect:
                self.transformationEffect.reparentTo(self)
                self.transformationEffect.setPos(0, 1, 0)
                self.transformationIval = Sequence(Func(self.motionFSM.off, lock=True), Func(startSFX, effectId), Func(self.transformationEffect.play), Func(self.play, 'death3'), Wait(1.7), Func(self._setCreatureTransformation, True, effectId), Func(self.motionFSM.on, unlock=True))
        self.transformationIval.start()
        return

    def playTransformationToPirate(self, effectId):
        from pirates.effects.JRSpawn import JRSpawn

        def startSFX():
            sfx = self.genericTransformation
            if sfx:
                base.playSfx(sfx, node=self, cutoff=100)

        if self.transformationEffect:
            self.transformationEffect.detachNode()
            self.transformationEffect = None
        if self.transformationIval:
            self.transformationIval.clearToInitial()
            self.transformationIval = None
        if self.gameFSM.state not in ['LandRoam', 'Battle']:
            self.transformationIval = Func(self._setCreatureTransformation, False, effectId)
        else:
            self.transformationEffect = JRSpawn.getEffect()
            if self.transformationEffect:
                self.transformationEffect.reparentTo(self)
                self.transformationEffect.setPos(0, 1, 0)
                self.transformationIval = Sequence(name='transformationIval')
                if self.doLongHumanTransform():
                    self.transformationIval.append(Func(self.motionFSM.off))
                self.transformationIval.append(Func(startSFX))
                self.transformationIval.append(Func(self.transformationEffect.play))
                self.transformationIval.append(Func(self._setCreatureTransformation, False, effectId))
                if self.doLongHumanTransform():
                    self.transformationIval.append(Func(self.play, 'jail_standup', fromFrame=65))
                    self.transformationIval.append(Wait(1.7))
                    self.transformationIval.append(Func(self.motionFSM.on))
        self.transformationIval.start()
        return

    def doLongHumanTransform(self):
        state = self.gameFSM.getCurrentOrNextState()
        if state in ('WaterRoam', 'WaterTreasureRoam', 'TeleportOut', 'ShipBoarding',
                     'EnterTunnel'):
            return False
        else:
            return True

    def setCreatureTransformation(self, value, effectId, timeSince=0):
        if self.creatureTransformation == value:
            return
        if value:
            self.playTransformationToCreature(effectId, timeSince)
        else:
            self.playTransformationToPirate(effectId)

    def changeBodyType(self):
        self.generateHuman(self.style.gender, self.masterHuman)
        if self.motionFSM.state != 'Off':
            self.motionFSM.off()
            self.motionFSM.on()

    def generateHuman(self, *args, **kwargs):
        if base.cr.newsManager and base.cr.newsManager.getHoliday(HolidayGlobals.APRILFOOLS) == 1:
            self.setJewelryZone5(10)
        DistributedPirateBase.generateHuman(self, *args, **kwargs)
        self.getGeomNode().setScale(self.scale)
        self.setHeight(self.height)
        self.maintainEffects()
        if self.potionStatusEffectManager:
            self.potionStatusEffectManager.maintainEffects()

    def maintainEffects(self):
        if self.isInvisible():
            self.activateInvisibleEffect()
        if self.creatureTransformation:
            self.getGeomNode().stash()

    def setAvatarSkinCrazy(self, value, colorIndex=0, timeSince=0):
        if self.crazyColorSkin == value:
            return
        self.crazyColorSkin = value
        self.crazySkinColorEffect = colorIndex
        if self.crazyColorSkin == True:
            self.setCrazyColorSkinIndex(colorIndex)
        if self.crazySkinColorIval:
            self.crazySkinColorIval.clearToInitial()
            self.crazySkinColorIval = None
        self.crazySkinColorIval = self.getTransformSequence(None, self.changeBodyType, [], timeSince)
        self.crazySkinColorIval.start()
        return

    def setAvatarScale(self, scale):
        if self.dropShadow:
            self.dropShadow.setScale(scale)
        Avatar.setAvatarScale(self, scale)

    def playScaleChangeAnimation(self, scale, timeSince=0):
        if self.scaleChangeIval:
            self.scaleChangeIval.clearToInitial()
            self.scaleChangeIval = None
        if scale < 1.0:
            soundEffect = self.shrinkSound
        elif scale > 1.0:
            soundEffect = self.growSound
        else:
            soundEffect = self.genericTransformation
        self.scaleChangeIval = self.getTransformSequence(soundEffect, self.setAvatarScale, [scale], timeSince)
        self.scaleChangeIval.start()
        return

    def getTransformSequence(self, sfx, func=None, args=[], timeSince=0):
        from pirates.effects.JRSpawn import JRSpawn
        if timeSince > 1.5 or self.gameFSM.state not in ['LandRoam', 'Battle']:
            return Func(func, *args)
        seq = Sequence(name=self.uniqueName('transformationIval'))
        if sfx == None:
            sfx = self.genericTransformation

        def startSFX(sfx):
            if sfx:
                base.playSfx(sfx, node=self, cutoff=100)

        self.transformSeqEffect = JRSpawn.getEffect()
        if self.transformSeqEffect:
            self.transformSeqEffect.reparentTo(self)
            self.transformSeqEffect.setPos(0, 1, 0)
            seq.append(Func(self.motionFSM.off, lock=True))
            seq.append(Func(startSFX, sfx))
            seq.append(Func(self.transformSeqEffect.play))
            seq.append(Func(self.play, 'death3'))
            seq.append(Wait(1.7))
            if func is not None:
                seq.append(Func(func, *args))
            seq.append(Func(self.play, 'jail_standup', fromFrame=65))
            seq.append(Wait(2.25))
            seq.append(Func(self.motionFSM.on, unlock=True))
        return seq

    def stopTransformAnims(self):
        self.isGiant = False
        self.isTiny = False
        if self.scaleChangeIval:
            self.scaleChangeIval.clearToInitial()
            self.scaleChangeIval = None
        self.crazyColorSkin = False
        if self.crazySkinColorIval:
            self.crazySkinColorIval.clearToInitial()
            self.crazySkinColorIval = None
        if self.transformSeqEffect:
            self.transformSeqEffect.detachNode()
            self.transformSeqEffect = None
        self.setCrazyColorSkinIndex(0)
        self.setAvatarScale(1.0)
        self.changeBodyType()
        if self.potionStatusEffectManager:
            self.potionStatusEffectManager.stopTransformAnims()
        if self.motionFSM.isLocked():
            self.motionFSM.unlock()
        return

    def setZombie(self, value, cursed=False):
        hiddenNode = self.getHiddenAncestor()
        needToHide = hiddenNode and hiddenNode.compareTo(self) == 0
        if self.zombie == value:
            return
        self.zombie = value
        self.cursed = cursed
        self.changeBodyType()
        self._zombieSV.set(self.zombie)
        if needToHide:
            self.hide()

    def isUndead(self):
        return self.zombie

    def respawn(self):
        self.motionFSM.on()
        self.unstashBattleCollisions()
        self.startCompassEffect()
        self.show(invisibleBits=PiratesGlobals.INVIS_DEATH)

    def setWishName(self):
        self.cr.sendWishName(self.doId, self.style.name)

    def canTeleport(self):
        return config.GetBool('ignore-teleport-requirements', (self.teleportFlags & PiratesGlobals.TFNoTeleportOut).isZero())

    def canTeleportTo(self):
        return config.GetBool('ignore-teleport-requirements', (self.teleportFlags & PiratesGlobals.TFNoTeleportTo).isZero())

    def testTeleportFlag(self, flag):
        return not (self.teleportFlags & flag).isZero()

    def getNextTeleportConfirmFlag(self, currentFlag=None, flags=None):
        currentFlag = currentFlag or BitMask32()
        flags = flags or BitMask32(self.teleportFlags)
        flags &= PiratesGlobals.TFNoTeleportOut
        return flags.keepNextHighestBit(currentFlag)

    def getNextTeleportToConfirmFlag(self, currentFlag=None, flags=None):
        currentFlag = currentFlag or BitMask32()
        flags = flags or BitMask32(self.teleportFlags)
        flags &= PiratesGlobals.TFNoTeleportTo
        return flags.keepNextHighestBit(currentFlag)

    def getNoTeleportString(self, flag=None):
        flag = flag or self.teleportFlags.keepNextHighestBit()
        if not flag.isZero():
            return PiratesGlobals.TFNoTeleportReasons.get(flag, '')
        return ''

    def getNoTeleportToString(self, flag=None):
        flag = flag or self.teleportFlags.keepNextHighestBit()
        if not flag.isZero():
            return PiratesGlobals.TFNoTeleportToReasons.get(flag, '')
        return ''

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def confirmTeleport(self, callback, feedback=False):
        if not self.canTeleport():
            flag = self.getNextTeleportConfirmFlag()
            while not flag.isZero():
                confirmFunc, confirmArgs = self.teleportConfirmCallbacks.get(flag, (None, []))
                if confirmFunc and confirmFunc('from', 0, 0, 0, 0, *confirmArgs):
                    flag = self.getNextTeleportConfirmFlag(flag)
                else:
                    if feedback:
                        if self.guiMgr.mapPage:
                            self.guiMgr.mapPage.shardPanel.refreshCurrentShard()
                        self.guiMgr.createWarning(self.getNoTeleportString(flag), PiratesGuiGlobals.TextFG6, duration=10)
                    callback(False)
                    return

        callback(True)
        return

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def confirmTeleportTo(self, callback, avId, avName, bandMgrId, bandId, guildId):
        flag = self.getNextTeleportToConfirmFlag()
        while not flag.isZero():
            confirmFunc, confirmArgs = self.teleportConfirmCallbacks.get(flag, (None, []))
            if confirmFunc and confirmFunc('to', avId, bandMgrId, bandId, guildId, *confirmArgs):
                flag = self.getNextTeleportToConfirmFlag(flag)
            else:
                callback(False, avId, flag)
                return

        callback(True, avId, flag)
        return

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def b_setTeleportFlag(self, flag, confirmCallback=None, confirmArgs=[]):
        self.b_setTeleportFlags(self.teleportFlags | flag, {flag: (confirmCallback, confirmArgs)})

    def setTeleportFlag(self, flag, confirmCallback=None, confirmArgs=[]):
        self.setTeleportFlags(self.teleportFlags | flag, {flag: (confirmCallback, confirmArgs)})

    def b_clearTeleportFlag(self, flag):
        self.b_setTeleportFlags(self.teleportFlags & ~flag, {flag: (None, [])})
        return

    def clearTeleportFlag(self, flag):
        self.setTeleportFlags(self.teleportFlags & ~flag, {flag: (None, [])})
        return

    def b_setTeleportFlags(self, flags, confirmDict):
        if self.teleportFlags != flags:
            self.d_setTeleportFlags(flags)
            self.setTeleportFlags(flags, confirmDict)

    def d_setTeleportFlags(self, flags):
        self.sendUpdate('setTeleportFlags', [flags.getWord()])

    def setTeleportFlags(self, flags, confirmDict={}):
        self.teleportFlags = BitMask32(flags)
        b = BitMask32.bit(31)
        while not b.isZero():
            if (b & self.teleportFlags).isZero():
                self.teleportConfirmCallbacks.pop(b, None)
            elif b in confirmDict:
                self.teleportConfirmCallbacks[b] = confirmDict[b]
            b = b >> 1

        return

    def getTeleportFlags(self):
        return self.teleportFlags

    def decipherTeleportFlags(self):
        iter = BitMask32(1)
        print self.teleportFlags, '-' * 80
        while iter.getWord():
            if (iter & self.teleportFlags).getWord():
                print '%-4s' % iter.getHighestOnBit(), self.getNoTeleportString(iter) or self.getNoTeleportToString(iter)
            iter <<= 1

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportQuery(self, sendToId, localBandMgrId, localBandId, localGuildId, localShardId):
        self.d_teleportQuery(localAvatar.doId, localBandMgrId, localBandId, localGuildId, localShardId, sendToId)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def d_teleportQuery(self, localAvId, localBandMgrId, localBandId, localGuildId, localShardId, sendToId):
        self.sendUpdate('teleportQuery', [localAvId, localBandMgrId, localBandId, localGuildId, localShardId], sendToId=sendToId)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def teleportQuery(self, requesterId, requesterBandMgrId, requesterBandId, requesterGuildId, requesterShardId):
        pass

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def sendTeleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        self.d_teleportResponse(available, shardId, instanceDoId, areaDoId, sendToId)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def d_teleportResponse(self, available, shardId, instanceDoId, areaDoId, sendToId=None):
        self.sendUpdate('teleportResponse', [localAvatar.doId, available, shardId, instanceDoId, areaDoId], sendToId)

    @report(types=['deltaStamp', 'args'], dConfigParam='teleport')
    def teleportResponse(self, avId, available, shardId, instanceDoId, areaDoId):
        pass

    def teleportTokenCheck(self, token):
        inv = self.getInventory()
        return bool(inv) and inv.getStackQuantity(token)

    def hasIslandTeleportToken(self, islandUid):
        token = InventoryType.getIslandTeleportToken(islandUid)
        return self.teleportTokenCheck(token)

    def confirmIslandTokenTeleport(self, toFrom, incomingAvid=0, bandMgrId=0, bandId=0, guildId=0, islandUid=''):
        if toFrom == 'from':
            return self.hasIslandTeleportToken(islandUid) or self.returnLocation == islandUid or self.currentIsland == islandUid or self.cr.distributedDistrict.worldCreator.isPvpIslandByUid(islandUid) or base.config.GetBool('teleport-all', 0) or islandUid == LocationIds.PORT_ROYAL_ISLAND and self.getInventory() and not self.getInventory().getShipDoIdList()
        else:
            return True

    def confirmNotSameAreaTeleport(self, toFrom, incomingAvid=0, bandMgrId=0, bandId=0, guildId=0, islandUid=''):
        if toFrom == 'from':
            try:
                if self.getParentObj().getUniqueId() == islandUid:
                    return False
            except AttributeError:
                pass

            return True
        else:
            return True

    def confirmNotSameAreaTeleportToPlayer(self, toFrom, incomingAvid=0, bandMgrId=0, bandId=0, guildId=0, areaDoId=0):
        if toFrom == 'from':
            try:
                if self.getParentObj().doId == areaDoId:
                    return False
            except AttributeError:
                pass

            return True
        else:
            return True

    def confirmSwimmingTeleport(self, toFrom, incomingAvid=0, bandMgrId=0, bandId=0, guildId=0):
        if toFrom == 'from':
            return True
        else:
            return True

    def setBandId(self, bandmanager, bandId):
        if bandId:
            self.BandId = (
             bandmanager, bandId)
        else:
            self.BandId = None
        return

    def getBandId(self):
        return self.BandId

    def isOnline(self):
        return True

    def isUnderstandable(self):
        return True

    def setPvp(self, value):
        self.inPvp = value
        self._inPvpSV.set(value)

    def setParlorGame(self, value):
        self.inParlorGame = value
        if self.inParlorGame and self.isLocal():
            self.guiMgr.crewHUD.setHUDOff()
            self.guiMgr.crewHUDTurnedOff = True

    def d_setBandPvp(self, value):
        self.sendUpdate('setBandPvp', [value])

    def d_setBandParlor(self, value):
        self.sendUpdate('setBandParlor', [value])

    def d_setBandDisconnect(self, value):
        self.sendUpdate('setBandDisconnect', [value])

    def checkQuestRewardFlag(self, flag):
        return not (self.questRewardFlags & flag).isZero()

    def setQuestRewardFlags(self, flags):
        self.questRewardFlags = BitMask32(flags)

    def getQuestRewardFlags(self):
        return self.questRewardFlags

    def spentSkillPoint(self, category):
        self.guiMgr.combatTray.skillTray.rebuildSkillTray()
        self.guiMgr.combatTray.initCombatTray()

    def resetSkillPoints(self, skillId):
        self.guiMgr.combatTray.skillTray.rebuildSkillTray()
        self.guiMgr.combatTray.initCombatTray()

    def requestLookoutInvite(self, inviterId, inviterName, activityCategory, activityType, options):
        if self.isLocal() and inviterId != localAvatar.doId:
            self.guiMgr.lookoutPage.requestInvite(inviterName, activityCategory, activityType, options)

    def unlimitedInviteNotice(self, activityCategory):
        self.guiMgr.lookoutPage.unlimitedInviteNotice(activityCategory)

    def scrubTalk(self, message, mods):
        scrubbed = 0
        text = copy.copy(message)
        for mod in mods:
            index = mod[0]
            length = mod[1] - mod[0] + 1
            newText = text[0:index] + length * '\x07' + text[index + length:]
            text = newText

        words = text.split(' ')
        newwords = []
        spaceCount = 0
        for word in words:
            if word == '':
                spaceCount += 1
            else:
                spaceCount = 0
            if word == '' and spaceCount > 10:
                pass
            elif word == '':
                newwords.append(word)
            elif word[0] == '\x07':
                newwords.append('\x01WLDisplay\x01' + random.choice(PLocalizer.WhitelistScrubList) + '\x02')
                scrubbed = 1
            elif base.whiteList.isWord(word):
                newwords.append(word)
            else:
                newwords.append('\x01WLDisplay\x01' + word + '\x02')
                scrubbed = 1

        newText = ' '.join(newwords)
        return (
         newText, scrubbed)

    def b_setSCEmote(self, emoteId):
        self.setSCEmote(emoteId)
        self.d_setSCEmote(emoteId)

    def d_setSCEmote(self, emoteId):
        self.sendUpdate('setSCEmote', [
         emoteId])

    def setSCEmote(self, emoteId):
        if self.doId in base.localAvatar.ignoreList:
            return
        base.talkAssistant.receiveOpenSpeedChat(ChatGlobals.SPEEDCHAT_EMOTE, emoteId, self.doId)

    def b_setSpeedChatQuest(self, questInt, msgType, taskNum):
        qId = QuestDB.getQuestIdFromQuestInt(questInt)
        quest = self.getQuestById(qId)
        if quest:
            taskState = quest.getTaskStates()[taskNum]
            self.setSpeedChatQuest(questInt, msgType, taskNum, taskState)
            self.d_setSpeedChatQuest(questInt, msgType, taskNum, taskState)
        return None

    def d_setSpeedChatQuest(self, questInt, msgType, taskNum, taskState):
        self.sendUpdate('setSpeedChatQuest', [
         questInt, msgType, taskNum, taskState])
        return None

    def setSpeedChatQuest(self, questInt, msgType, taskNum, taskState):
        if self.doId in base.localAvatar.ignoreList:
            return
        chatString = PSCDecoders.decodeSCQuestMsgInt(questInt, msgType, taskNum, taskState)
        if chatString:
            self.setChatAbsolute(chatString, CFSpeech | CFQuicktalker | CFTimeout)
        base.talkAssistant.receiveOpenTalk(self.doId, self.getName(), None, None, chatString)
        return

    def whisperSCQuestTo(self, questInt, msgType, taskNum, sendToId):
        messenger.send('wakeup')
        self.sendUpdate('setWhisperSCQuest', [self.doId, questInt, msgType, taskNum], sendToId)

    def setWhisperSCQuest(self, fromId, questInt, msgType, taskNum):
        if fromId in base.localAvatar.ignoreList:
            return
        fromHandle = base.cr.identifyAvatar(fromId)
        if fromHandle:
            fromName = fromHandle.getName()
        else:
            return
        chatString = PSCDecoders.decodeSCQuestMsgInt(questInt, msgType, taskNum)
        base.talkAssistant.receiveWhisperTalk(fromId, fromName, None, None, self.doId, self.getName(), chatString)
        return

    def getAccess(self):
        if Freebooter.AllAccessHoliday:
            return 2
        else:
            return self.getGameAccess()

    def setAccess(self, access):
        self.setGameAccess(access)

    def setGameAccess(self, access):
        self.gameAccess = access
        self.refreshName()

    def getGameAccess(self):
        return self.gameAccess

    def setFounder(self, founder):
        self.founder = founder
        self.refreshName()

    def getFounder(self):
        return self.founder

    def useBestTonic(self):
        self.sendUpdate('useBestTonic', [])

    def useTonic(self, tonicId):
        self.sendUpdate('useTonic', [tonicId])

    @report(types=['frameCount', 'args'], dConfigParam='port')
    def setPort(self, islandId):
        self.port = islandId
        if self.ship:
            self.ship.checkAbleDropAnchor()

    @report(types=['frameCount', 'args'], dConfigParam='port')
    def clearPort(self, islandId):
        if islandId == self.port:
            self.port = 0
            if self.ship:
                self.ship.checkAbleDropAnchor()

    def getPort(self):
        return self.port

    def enableWaterEffect(self):
        if base.options.getSpecialEffectsSetting() < base.options.SpecialEffectsMedium:
            return
        if not self.waterRipple:
            self.waterRipple = WaterRipple.getEffect()
            if self.waterRipple:
                self.waterRipple.reparentTo(self)
                self.waterRipple.startLoop()
        if not self.waterWake:
            self.waterWake = WaterRippleWake.getEffect()
            if self.waterWake:
                self.waterWake.reparentTo(self)
                self.waterWake.startLoop()
        if not self.waterSplash:
            self.waterSplash = WaterRippleSplash.getEffect()
            if self.waterSplash:
                self.waterSplash.reparentTo(self)
                self.waterSplash.startLoop()

    def disableWaterEffect(self):
        if base.options.getSpecialEffectsSetting() < base.options.SpecialEffectsMedium:
            return
        if self.waterRipple:
            self.waterRipple.stopLoop()
            self.waterRipple = None
        if self.waterWake:
            self.waterWake.stopLoop()
            self.waterWake = None
        if self.waterSplash:
            self.waterSplash.stopLoop()
            self.waterSplash = None
        return

    def adjustWaterEffect(self, offset, forwardSpeed=0.0, rotateSpeed=0.0, slideSpeed=0.0):
        if base.options.getSpecialEffectsSetting() < base.options.SpecialEffectsMedium:
            return
        if forwardSpeed == 0.0 and slideSpeed == 0.0:
            if not self.waterRipple:
                self.waterRipple = WaterRipple.getEffect()
                if self.waterRipple:
                    self.waterRipple.reparentTo(self)
                    self.waterRipple.startLoop()
            if self.waterWake:
                self.waterWake.stopLoop()
                self.waterWake = None
            if self.waterSplash:
                self.waterSplash.stopLoop()
                self.waterSplash = None
        else:
            if not self.waterWake:
                self.waterWake = WaterRippleWake.getEffect()
                if self.waterWake:
                    self.waterWake.reparentTo(self)
                    self.waterWake.startLoop()
            if not self.waterSplash:
                self.waterSplash = WaterRippleSplash.getEffect()
                if self.waterSplash:
                    self.waterSplash.reparentTo(self)
                    self.waterSplash.startLoop()
            if self.waterRipple:
                self.waterRipple.stopLoop()
                self.waterRipple = None
        if rotateSpeed != 0.0 and self.waterRipple:
            self.waterRipple.disturbRipple()
        if self.waterRipple:
            self.waterRipple.setZ(offset)
        if self.waterWake:
            self.waterWake.setY(forwardSpeed / 9.5)
            self.waterWake.setX(slideSpeed / 9.0)
            self.waterWake.setZ(offset)
        if self.waterSplash:
            self.waterSplash.setX(slideSpeed / 20.0)
            self.waterSplash.setZ(offset - 0.75)
        return

    def setCompositeDNA(self, *dna):
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('setCompositeDNA').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

    def announceClothingChange(self, *dna):
        if self.isLocal():
            return
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('announceClothingChange').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

        self.generateHuman(self.style.getGender(), self.masterHuman)
        self.motionFSM.off()
        self.motionFSM.on()

    def tryOnTattoo(self, tattooItem, location):
        flipIt = 0
        if location == 0:
            equipFunction = self.setTattooChest
        else:
            if location == 1:
                equipFunction = self.setTattooZone2
            elif location == 2:
                equipFunction = self.setTattooZone3
                flipIt = 1
            elif location == 3:
                equipFunction = self.setTattooZone4
            elif location == 4:
                equipFunction = self.setTattooZone5
            elif location == 5:
                equipFunction = self.setTattooZone6
            elif location == 6:
                equipFunction = self.setTattooZone7
            elif location == 7:
                equipFunction = self.setTattooZone8
            if tattooItem:
                gender = self.style.getGender()
                itemId = tattooItem.getId()
                rarity = ItemGlobals.getRarity(itemId)
                if rarity != ItemConstants.CRUDE and not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                    equipFunction(0, 0, 0, 0, 0, 0)
                else:
                    if gender == 'm':
                        tattooId = ItemGlobals.getMaleModelId(itemId)
                        if flipIt:
                            tattooOrientation = ItemGlobals.getOrientation(ItemGlobals.getMaleOrientation2(itemId))
                        else:
                            tattooOrientation = ItemGlobals.getOrientation(ItemGlobals.getMaleOrientation(itemId))
                    else:
                        tattooId = ItemGlobals.getFemaleModelId(itemId)
                        if flipIt:
                            tattooOrientation = ItemGlobals.getOrientation(ItemGlobals.getFemaleOrientation2(itemId))
                        else:
                            tattooOrientation = ItemGlobals.getOrientation(ItemGlobals.getFemaleOrientation(itemId))
                    offsetx = tattooOrientation[0]
                    offsety = tattooOrientation[1]
                    scale = tattooOrientation[2]
                    rotate = tattooOrientation[3]
                    S = Vec2(1 / float(scale), 1 / float(scale))
                    Iv = Vec2(offsetx, offsety)
                    Vm = Vec2(sin(rotate * pi / 180.0), cos(rotate * pi / 180.0))
                    Vms = Vec2(Vm[0] * S[0], Vm[1] * S[1])
                    Vn = Vec2(Vm[1], -Vm[0])
                    Vns = Vec2(Vn[0] * S[0], Vn[1] * S[1])
                    F = Vec2(-Vns.dot(Iv) + 0.5, -Vms.dot(Iv) + 0.5)
                    color = 0
                    equipFunction(tattooId, F[0], F[1], S[0], rotate, color)
            equipFunction(0, 0, 0, 0, 0, 0)
        self.doRegeneration()

    def tryOnJewelry(self, jewelryItem, location):
        equipFunction = None
        if location == 0:
            equipFunction = self.setJewelryZone3
        else:
            if location == 1:
                equipFunction = self.setJewelryZone4
            elif location == 2:
                equipFunction = self.setJewelryZone1
            elif location == 3:
                equipFunction = self.setJewelryZone2
            elif location == 4:
                equipFunction = self.setJewelryZone5
            elif location == 5:
                equipFunction = self.setJewelryZone6
            elif location == 6:
                equipFunction = self.setJewelryZone7
            elif location == 7:
                equipFunction = self.setJewelryZone8
            if equipFunction:
                if jewelryItem != None:
                    gender = self.style.getGender()
                    itemId = jewelryItem.getId()
                    rarity = ItemGlobals.getRarity(itemId)
                    if rarity != ItemConstants.CRUDE and not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                        equipFunction(0, 0, 0)
                    else:
                        if gender == 'f':
                            modelIndex = ItemGlobals.getFemaleModelId(itemId)
                        else:
                            modelIndex = ItemGlobals.getMaleModelId(itemId)
                        equipFunction(modelIndex, ItemGlobals.getPrimaryColor(itemId), ItemGlobals.getSecondaryColor(itemId))
                else:
                    equipFunction(0, 0, 0)
        self.doRegeneration()
        return

    def requestClothesList(self):
        self.sendUpdate('requestClothesList', [])

    def receiveClothesList(self, clothesList):
        messenger.send('received_clothes_list', [clothesList])

    def removeClothes(self, clothingType):
        gender = self.style.getGender()
        underwearTable = ClothingGlobals.UNDERWEAR.get(gender)
        if underwearTable:
            underwearTuple = underwearTable.get(clothingType, (0, 0, 0))
        self.wearClothing(clothingType, underwearTuple[0], underwearTuple[1], underwearTuple[2])

    def tryOnClothes(self, location, itemTuple):
        gender = self.style.getGender()
        rarity = ItemGlobals.getRarity(itemTuple[1])
        if gender == 'f':
            modelIndex = ItemGlobals.getFemaleModelId(itemTuple[1])
            textureIndex = ItemGlobals.getFemaleTextureId(itemTuple[1])
        else:
            modelIndex = ItemGlobals.getMaleModelId(itemTuple[1])
            textureIndex = ItemGlobals.getMaleTextureId(itemTuple[1])
        colorIndex = itemTuple[3]
        if modelIndex == -1 or rarity != ItemConstants.CRUDE and not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
            underwearTable = ClothingGlobals.UNDERWEAR.get(gender)
            if underwearTable:
                underwearTuple = underwearTable.get(location, (0, 0, 0))
                modelIndex = underwearTuple[0]
                textureIndex = underwearTuple[1]
                colorIndex = underwearTuple[2]
            else:
                modelId = 0
                texId = 0
                colorId = 0
        self.wearClothing(location, modelIndex, textureIndex, colorIndex)

    def wearClothing(self, location, modelId, texId, colorId):
        takenOff = 0
        topColors = self.getStyle().getClothesTopColor()
        botColors = self.getStyle().getClothesBotColor()
        colorHat = self.getStyle().getHatColor()
        colorShirt = topColors[0]
        colorVest = topColors[1]
        colorCoat = topColors[2]
        colorPant = botColors[0]
        colorSash = botColors[1]
        colorShoe = botColors[2]
        if location == ClothingGlobals.HAT:
            self.getStyle().setClothesHat(modelId, texId)
            colorHat = colorId
        else:
            if location == ClothingGlobals.SHIRT:
                self.getStyle().setClothesShirt(modelId, texId)
                colorShirt = colorId
            elif location == ClothingGlobals.VEST:
                self.getStyle().setClothesVest(modelId, texId)
                colorVest = colorId
            elif location == ClothingGlobals.COAT:
                self.getStyle().setClothesCoat(modelId, texId)
                colorCoat = colorId
            elif location == ClothingGlobals.PANT:
                self.getStyle().setClothesPant(modelId, texId)
                colorPant = colorId
            elif location == ClothingGlobals.BELT:
                self.getStyle().setClothesBelt(modelId, texId)
                colorSash = colorId
            elif location == ClothingGlobals.SOCK:
                self.getStyle().setClothesSock(modelId, texId)
            elif location == ClothingGlobals.SHOE:
                self.getStyle().setClothesShoe(modelId, texId)
                colorShoe = colorId
            if modelId == -1:
                underwearTable = ClothingGlobals.UNDERWEAR.get(gender)
                if underwearTable:
                    underwearTuple = underwearTable.get(location, (0, 0, 0))
                    modelId = underwearTuple[0]
                    texId = underwearTuple[1]
                    colorId = underwearTuple[2]
        self.getStyle().setHatColor(colorHat)
        self.getStyle().setClothesTopColor(colorShirt, colorVest, colorCoat)
        self.getStyle().setClothesBotColor(colorPant, colorSash, colorShoe)
        self.setClothesFromList(self.getClothesComposite())
        self.doRegeneration()

    def getClothesComposite(self):
        clothesComposite = [
         self.getStyle().getHatIdx(), self.getStyle().getHatTexture(), self.getStyle().getHatColor()] + self.getStyle().getClothesShirt() + self.getStyle().getClothesVest() + self.getStyle().getClothesCoat() + self.getStyle().getClothesBelt() + self.getStyle().getClothesPant() + self.getStyle().getClothesShoe() + self.getStyle().getClothesTopColor() + self.getStyle().getClothesBotColor()
        return tuple(clothesComposite)

    def setClothesFromList(self, dna):
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('setClothes').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

        messenger.send(self.uniqueName('accessoriesUpdate'))

    def cueRegenerate(self, force=0):
        if self.gameFSM.state in ['LandRoam', 'Battle', 'WaterRoam', 'Off']:
            self.doRegeneration()
        else:
            self.needRegenFlag = 1

    def askRegen(self):
        if self.needRegenFlag:
            self.doRegeneration()

    def doRegeneration(self):
        self.needRegenFlag = 0
        if self.isLocal():
            cameraPos = camera.getPos()
            camOff = localAvatar.cameraFSM.getFPSCamera().camOffset
            localAvatar.guiMgr.combatTray.endButtonCharge()
        self.generateHuman(self.style.getGender(), self.masterHuman)
        self.motionFSM.off()
        self.motionFSM.on()
        messenger.send(self.uniqueName('accessoriesUpdate'))
        if self.isLocal():
            camera.setPos(cameraPos)
            localAvatar.cameraFSM.getFPSCamera().camOffset = camOff

    def setClothes2(self, *dna):
        if hasattr(self, 'clothingEquipBufferDict') and len(self.clothingEquipBufferDict.keys()) > 0:
            return
        elif dna == self.getClothesComposite():
            pass
        else:
            self.setClothesFromList(dna)

    def setClothes(self, *dna):
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('setClothes').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

        messenger.send(self.uniqueName('accessoriesUpdate'))

    def setHair(self, *dna):
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('setHair').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

        self.generateHuman(self.style.getGender(), self.masterHuman)
        self.motionFSM.off()
        self.motionFSM.on()

    def setJewelry(self, *dna):
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('setJewelry').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

        messenger.send(self.uniqueName('jewelryUpdate'))

    def setTattoos(self, *dna):
        counter = 0
        dclass = base.cr.dclassesByName['DistributedPlayerPirate']
        field = dclass.getFieldByName('setTattoos').asMolecularField()
        for i in xrange(field.getNumAtomics()):
            subField = field.getAtomic(i)
            args = dna[counter:counter + subField.getNumElements()]
            counter += subField.getNumElements()
            getattr(self.style, subField.getName())(*args)

        messenger.send(self.uniqueName('tattooUpdate'))

    def requestActivity(self, gameType, gameCategory, options, shipIds):
        self.sendUpdate('requestActivity', [gameType, gameCategory, options, shipIds])

    def requestInvitesResp(self, invitees, numFailed):
        if len(invitees) > 0:
            self.guiMgr.lookoutPage.requestInvitesResponse(invitees)
        else:
            if self.guiMgr.lookoutPage.currentInviteRequiresInvitees():
                self.guiMgr.lookoutPage.restoreOrCancelSearch()
                if numFailed == 0:
                    if DistributedBandMember.DistributedBandMember.getBandMember(localAvatar.doId):
                        self.guiMgr.messageStack.addTextMessage(PLocalizer.LookoutInviteIgnore, icon=('lookout',
                                                                                                      None))
                    else:
                        self.guiMgr.messageStack.addTextMessage(PLocalizer.LookoutInviteNeedCrew, icon=('lookout',
                                                                                                        None))
            else:
                self.guiMgr.lookoutPage.requestInvitesResponse([])
            if numFailed > 0:
                self.guiMgr.messageStack.addTextMessage(PLocalizer.LookoutInviteFail % numFailed, icon=('lookout',
                                                                                                        None))
        return None

    def getTutorialState(self):
        if config.GetBool('force-tutorial-complete', False):
            return PiratesGlobals.TUT_MET_JOLLY_ROGER
        return self.tutorialState

    def updateClientTutorialStatus(self, val):
        self.tutorialState = val

    def getIsPaid(self):
        self.updatePaidStatus()
        return self.isPaid

    def updatePaidStatus(self):
        pStatus = self.getGameAccess()
        if pStatus == 2 or pStatus == 0:
            self.isPaid = True
        else:
            self.isPaid = False

    def initVisibleToCamera(self):
        if self is not localAvatar and localAvatar.getSoloInteraction():
            self.hideFromCamera()
        else:
            self.showToCamera()

    def hideFromCamera(self):
        self.accept('showOtherAvatars', self.showToCamera)
        self.node().adjustDrawMask(BitMask32.allOff(), base.cam.node().getCameraMask(), BitMask32.allOff())

    def showToCamera(self):
        self.accept('hideOtherAvatars', self.hideFromCamera)
        self.node().adjustDrawMask(base.cam.node().getCameraMask(), BitMask32.allOff(), BitMask32.allOff())

    def submitCodeToServer(self, code):
        if code:
            base.cr.codeRedemption.redeemCode(code)

    def getNameText(self):
        return DistributedPirateBase.getNameText(self)

    def setOnWelcomeWorld(self, value):
        self.onWelcomeWorld = value

    def setTempDoubleXPReward(self, value):
        if not self.tempDoubleXPStatusMessaged:
            self.tempDoubleXPStatusMessaged = True
            if self.getDoId() == localAvatar.getDoId() and value != 0:
                h, m = self.getHoursAndMinutes(value)
                base.localAvatar.guiMgr.messageStack.addModalTextMessage(PLocalizer.TEMP_DOUBLE_REP % (h, m), seconds=45, priority=0, color=PiratesGuiGlobals.TextFG14)
        elif value > self.tempDoubleXPStatus:
            h, m = self.getHoursAndMinutes(value)
            base.localAvatar.guiMgr.messageStack.addModalTextMessage(PLocalizer.TEMP_DOUBLE_REP % (h, m), seconds=45, priority=0, color=PiratesGuiGlobals.TextFG14)
        self.tempDoubleXPStatus = value
        self.x2XPIcon.setPos(0.3, 0, -0.15)
        self.refreshName()

    def getTempDoubleXPReward(self):
        return self.tempDoubleXPStatus

    def setLastAttackTime(self, timestamp):
        self.lastAttackTime = globalClockDelta.localElapsedTime(timestamp)

    def getHoursAndMinutes(self, seconds):
        t = int(seconds)
        minutes, seconds = divmod(t, 60)
        hours, minutes = divmod(minutes, 60)
        return [
         hours, minutes]

    def setGMNameTagState(self, state):
        self.gmNameTagEnabled = state

    def setGMNameTagString(self, nameTagString):
        self.gmNameTagString = nameTagString

    def getGMNameTagString(self):
        return self.gmNameTagString

    def setGMNameTagColor(self, color):
        self.gmNameTagColor = color

    def getGMNameTagColor(self):
        return self.gmNameTagColor

    def updateGMNameTag(self, state, color, tagString):
        if color == 'gold':
            color = 'goldGM'
        elif color == 'red':
            color = 'redGM'
        elif color == 'green':
            color = 'greenGM'
        elif color == 'blue':
            color = 'blueGM'
        else:
            color = 'whiteGM'
        self.setGMNameTagState(state)
        self.setGMNameTagColor(color)
        self.setGMNameTagString(tagString)
        self.refreshName()

    def nameTag3dInitialized(self):
        DistributedPirateBase.nameTag3dInitialized(self)
        self.refreshName()

    def b_updateGMNameTag(self, state, color, tagString):
        self.d_updateGMNameTag(state, color, tagString)
        self.updateGMNameTag(state, color, tagString)

    def d_updateGMNameTag(self, state, color, tagString):
        self.sendUpdate('updateGMNameTag', [state, color, tagString])

    def getShortName(self):
        return self.getName()

    def setTalk(self, fromAV, fromAC, avatarName, chat, mods, flags):
        if not hasattr(self, 'isGM') or not self.isGM():
            if not self.isConfused:
                DistributedPlayer.setTalk(self, fromAV, fromAC, avatarName, chat, mods, flags)
            else:
                newText, scrubbed = self.scrubTalk(chat, mods)
                if base.talkAssistant.isThought(newText):
                    base.talkAssistant.receiveThought(fromAV, avatarName, fromAC, None, newText, scrubbed)
                else:
                    base.talkAssistant.receiveOpenTalk(fromAV, avatarName, fromAC, None, newText, scrubbed)
        else:
            base.talkAssistant.receiveGMTalk(fromAV, avatarName, fromAC, None, chat, 0)
        return

    def getBroadcastPeriod(self):
        period = localAvatar.getPosHprBroadcastPeriod()
        if period == None:
            return PiratesGlobals.AI_MOVEMENT_PERIOD
        else:
            return period
        return

    def setPlundering(self, plunderingId):
        self.isPlundering = plunderingId

    def getPlundering(self):
        return self.isPlundering

    def setPopulated(self, state):
        self.populated = state

    def isPopulated(self):
        return self.populated

    def sendRequestContext(self, context, part=0):
        self.sendUpdate('requestContext', [context, part])

    def sendRequestSeenContext(self, context):
        self.sendUpdate('requestSeenContext', [context])

    def sendRequestChangeTutType(self, type, off):
        self.sendUpdate('requestChangeTutType', [type, off])

    def removeContext(self, context, number=0):
        if self.guiMgr:
            contextTutPanel = self.guiMgr.contextTutPanel
            if number:
                if contextTutPanel.isFilled() and self.guiMgr.contextTutPanel.getContext() == context and self.guiMgr.contextTutPanel.getNumber() == number:
                    contextTutPanel.closePanel()
            elif contextTutPanel.isFilled() and self.guiMgr.contextTutPanel.getContext() == context:
                contextTutPanel.closePanel()

    def setCommonChatFlags(self, commonChatFlags):
        DistributedPlayer.setCommonChatFlags(self, commonChatFlags)
        if hasattr(base, 'localAvatar') and base.localAvatar.playersNearby.has_key(self.getDoId()):
            base.localAvatar.playersNearby[self.getDoId()] = (
             commonChatFlags, base.localAvatar.playersNearby[self.getDoId()][1])

    def setWhitelistChatFlags(self, whitelistChatFlags):
        DistributedPlayer.setWhitelistChatFlags(self, whitelistChatFlags)
        if hasattr(base, 'localAvatar') and base.localAvatar.playersNearby.has_key(self.getDoId()):
            base.localAvatar.playersNearby[self.getDoId()] = (
             base.localAvatar.playersNearby[self.getDoId()][0], whitelistChatFlags)

    def requestConfusedText(self, wlEnabled):
        self.isConfused = True
        self.wlEnabled = wlEnabled
        self.clearChat()
        self.refreshName()
        taskMgr.doMethodLater(5.0, self.removeConfusedText, self.uniqueName('removeConfusedText'))

    def removeConfusedText(self, task):
        self.isConfused = False
        self.refreshName()

    @report(types=['args'], dConfigParam='dteleport')
    def handleArrivedOnShip(self, ship):
        DistributedBattleAvatar.handleArrivedOnShip(self, ship)
        ship.playerPirateArrived(self)

    @report(types=['args'], dConfigParam='dteleport')
    def handleLeftShip(self, ship):
        DistributedBattleAvatar.handleLeftShip(self, ship)
        ship.playerPirateLeft(self)

    @report(types=['args'], dConfigParam='dteleport')
    def d_boardShip(self, ship, boardingSpot):
        self.sendUpdate('boardShip', [ship, boardingSpot])

    @report(types=['args'], dConfigParam='dteleport')
    def boardShip(self, ship, boardingSpot):
        pass

    @report(types=['args'], dConfigParam='dteleport')
    def d_swingToShip(self, fromShip, toShip, boardingSpot, timestamp):
        self.sendUpdate('swingToShip', [fromShip, toShip, boardingSpot, timestamp])

    @report(types=['args'], dConfigParam='dteleport')
    def swingToShip(self, fromShip, toShip, boardingSpot, timestamp, playRate=0.6):
        fromShip = self.cr.getDo(fromShip)
        ship = self.cr.getDo(toShip)
        if fromShip == None or ship == None:
            return
        if self.swingTrack:
            self.swingTrack.pause()
            self.swingTrack = None
        self.swingTrack = self.createSwingTrack(fromShip, ship, boardingSpot)
        elapsed = globalClockDelta.localElapsedTime(timestamp)
        self.swingTrack.start(elapsed, playRate=playRate)
        return

    @report(types=['args'], dConfigParam='dteleport')
    def createSwingTrack(self, fromShip, ship, boardingSpot):
        boardingNode = ship.getBoardingLocator(boardingSpot)
        topNode = ship.model.modelRoot.attachNewNode(self.uniqueName('rope-top'))
        topNode.setZ(200)
        avStartPos = self.getPos(ship.model.modelRoot)
        avEndPos = boardingNode.getPos(ship.model.modelRoot)
        midNode = ship.model.modelRoot.attachNewNode(self.uniqueName('rope-mid'))
        midNodeStartPos = ((topNode.getPos() + avStartPos) * 0.5 + (topNode.getPos() + avEndPos) * 0.5) * 0.5
        midNodeEndPos = (topNode.getPos() + avEndPos) * 0.5
        midNode.setPos(midNodeStartPos)
        rope, ropeActor = self.getRope()
        rope.setup(3, ((None, Point3(0)), (midNode, Point3(0)), (topNode, Point3(0))))
        rope.reparentTo(self.rightHandNode)
        rope.hide()
        ropeActor.reparentTo(self.rightHandNode)
        ropeActor.hide()
        swingDuration = self.getDuration('swing_aboard', fromFrame=45, toFrame=75)
        cameraDuration = self.getDuration('swing_aboard', fromFrame=27, toFrame=45)
        swingTrack = Sequence(Func(self.wrtReparentTo, fromShip.model.modelRoot), Func(self.lookAt, ship), Func(self.setP, 0), Func(self.setR, 0), Parallel(self.actorInterval('swing_aboard', startFrame=27, endFrame=45, blendOutT=0), self.getSwingCameraOut(cameraDuration)), Func(self.wrtReparentTo, ship.model.modelRoot), Func(self.setP, 0), Func(self.setR, 0), Func(rope.show), Func(ropeActor.show), Parallel(self.actorInterval('swing_aboard', startFrame=45, endFrame=75, blendInT=0, blendOutT=0), ropeActor.actorInterval('swing_aboard', startFrame=0, endFrame=30), ProjectileInterval(self, endPos=avEndPos, duration=swingDuration, gravityMult=6), LerpPosInterval(midNode, pos=midNodeEndPos, duration=swingDuration), self.getSwingCameraIn(swingDuration)), Func(ropeActor.detachNode), Func(topNode.detachNode), Func(midNode.detachNode), Func(rope.detachNode))
        return swingTrack

    def getSwingCameraOut(self, duration):
        return Wait(duration)

    def getSwingCameraIn(self, duration):
        return Wait(duration)

    def bloodFireChange(self, increase):
        if increase:
            if self.bloodFireTime <= 0.0:
                startTimer = True
                self.taskTime = 0
                if self.isLocal():
                    self.guiMgr.combatTray.showBloodFire()
            else:
                startTimer = False
            maxBloodFire = ItemGlobals.BLOOD_FIRE_MAX * ItemGlobals.BLOOD_FIRE_TIMER
            if self.bloodFireTime + ItemGlobals.BLOOD_FIRE_TIMER < maxBloodFire:
                self.bloodFireTime += ItemGlobals.BLOOD_FIRE_TIMER
            if startTimer:
                taskMgr.add(self.bloodFireCharging, self.uniqueName('bloodFireCharging'), priority=40)

    def bloodFireCharging(self, task):
        if not self.currentWeapon or ItemGlobals.getType(self.currentWeaponId) != ItemGlobals.SWORD:
            return Task.done
        self.bloodFireTime -= task.time - self.taskTime
        if self.isLocal():
            self.guiMgr.combatTray.updateBloodFire(self.bloodFireTime)
            self.currentWeapon.setFlameIntensity(self.bloodFireTime / (ItemGlobals.BLOOD_FIRE_TIMER * ItemGlobals.BLOOD_FIRE_MAX))
        if self.bloodFireTime <= 0.0:
            self.bloodFireTime = 0.0
            if self.isLocal():
                self.guiMgr.combatTray.hideBloodFire()
            return Task.done
        self.taskTime = task.time
        return Task.cont

    def clearBloodFire(self):
        taskMgr.remove(self.uniqueName('bloodFireCharging'))
        self.bloodFireTime = 0.0
        if self.isLocal():
            self.guiMgr.combatTray.clearBloodFire()

    def setAuraActivated(self, auraActivated):
        if not self.currentWeapon or ItemGlobals.getType(self.currentWeaponId) != ItemGlobals.STAFF:
            self.auraActivated = False
            return
        if auraActivated == EnemySkills.STAFF_TOGGLE_AURA_WARDING:
            self.auraIval = self.currentWeapon.getWardingAura(self)
        else:
            if auraActivated == EnemySkills.STAFF_TOGGLE_AURA_NATURE:
                self.auraIval = self.currentWeapon.getNatureAura(self)
            elif auraActivated == EnemySkills.STAFF_TOGGLE_AURA_DARK:
                self.auraIval = self.currentWeapon.getDarkAura(self)
            else:
                if self.auraIval:
                    self.auraIval.pause()
                    self.auraIval = None
                self.currentWeapon.stopAuraEffects()
            if self.auraIval:
                self.auraIval.start()
        self.auraActivated = auraActivated
        return

    def getAuraActivated(self):
        return self.auraActivated

    def considerEnableMovement(self):
        if self.getGameState() in ('PVPComplete', 'Off'):
            return
        else:
            return DistributedBattleAvatar.considerEnableMovement(self)

    def getMinimapObject(self):
        if not self.minimapObj and not self.isDisabled():
            self.minimapObj = MinimapPlayerPirate(self)
        if self.minimapObj:
            if DistributedBandMember.DistributedBandMember.areSameCrew(self.doId, localAvatar.doId):
                self.minimapObj.joinedCrew()
            else:
                self.minimapObj.leftCrew()
        return self.minimapObj

    def setIsTracked(self, questId):
        self.isTracked = False
        if self.minimapObj:
            self.minimapObj.setIsTracked(self.isTracked)

    def d_requestShowOffFish(self, collectionId):
        if config.GetBool('want-show-off-fish', 0):
            self.sendUpdate('requestShowOffFish', [collectionId])

    def showOffFish(self, collectionId, weight):
        fishData = FishingGlobals.CollectionToData[collectionId]
        if self.shownFish:
            self.shownFish.destroy()
        self.shownFish = Fish.Fish(None, fishData, 0, trophy=weight)
        self.fishSwivel.reparentTo(self.leftHandNode)
        self.shownFish.reparentTo(self.fishSwivel)
        mouthTrans = self.shownFish.mouthJoint.getTransform(self.shownFish).getInverse()
        self.shownFish.setTransform(mouthTrans)
        self.fishSwivel.setHpr(180, 0, -90)
        return

    def setEmote(self, emoteId):
        DistributedBattleAvatar.setEmote(self, emoteId)

    def playEmote(self, emoteId):
        if base.cr.avatarFriendsManager.checkIgnored(self.doId):
            return
        else:
            DistributedBattleAvatar.playEmote(self, emoteId)

    def canIdleSplashEver(self):
        return True

    def canIdleSplash(self):
        return self.getCurrentAnim() == 'idle'

    def enterDialogMode(self):
        self.hide(invisibleBits=PiratesGlobals.INVIS_DIALOG)

    def exitDialogMode(self):
        self.show(invisibleBits=PiratesGlobals.INVIS_DIALOG)

    def rewardNotify(self, rewardCat, rewardId):
        if base.config.GetBool('black-pearl-repeat-reward', 1) == 1:

            def showRewardPanel(task=None):
                rewardSkillId = ItemGlobals.getUseSkill(rewardId)
                rewardName = PLocalizer.getInventoryTypeName(rewardSkillId)
                if rewardCat and rewardId:
                    rewardText = PLocalizer.BlackPearlRewardSuccess % rewardName
                else:
                    rewardText = PLocalizer.BlackPearlRewardFailure % rewardName
                localAvatar.guiMgr.messageStack.addTextMessage(rewardText, seconds=30, icon=('friends',
                                                                                             None))
                return None

            self.acceptOnce('highSeasScoreBoardClose', showRewardPanel)
        return


class MinimapPlayerPirate(MinimapBattleAvatar):
    DEFAULT_COLOR = VBase4(0.1, 0.5, 1.0, 0.7)

    def __init__(self, avatar):
        MinimapBattleAvatar.__init__(self, avatar)
        self.inCrew = False

    def _addedToMap(self, map):
        self.accept(BandConstance.BandMembershipChange, self.bandUpdated)

    def _removedFromMap(self, map):
        self.ignore(BandConstance.BandMembershipChange)

    def bandUpdated(self, member, removed):
        if member.avatarId == self.worldNode.getDoId():
            if removed:
                self.leftCrew()
            else:
                self.joinedCrew()

    def joinedCrew(self):
        self.inCrew = True
        self.setIconColor()

    def leftCrew(self):
        self.inCrew = False
        self.setIconColor()

    def setIconColor(self, color=None):
        if self.inCrew:
            MinimapBattleAvatar.setIconColor(self, color or VBase4(0.9, 0.5, 0.95, 1))
        else:
            MinimapBattleAvatar.setIconColor(self, color or VBase4(0.1, 0.5, 1.0, 0.7))
