import os
import webbrowser
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import FSM
from otp.otpbase import OTPGlobals
from otp.nametag.Nametag import Nametag
from otp.nametag import NametagGlobals
from otp.nametag.NametagGroup import NametagGroup
from otp.nametag.WhisperPopup import WhisperPopup
from otp.nametag.NametagFloat2d import NametagFloat2d
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.battle import WeaponGlobals
from pirates.reputation import ReputationGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import SkillPage
from pirates.piratesgui import StatusTray
from pirates.piratesgui import ClothingPage
from pirates.piratesgui import TitlesPage
from pirates.piratesgui.GuiButton import GuiButton
from pirates.piratesgui import ChestTray
from pirates.piratesgui import ChestPanel
from pirates.piratesgui import GameGui
from pirates.piratesgui import SocialPanel
from pirates.piratesgui import QuestPage
from pirates.piratesgui import ShipPage
from pirates.piratesgui import WeaponPage
from pirates.piratesgui import CollectionPage
from pirates.piratesgui import CollectionMain
from pirates.piratesgui import MapPage
from pirates.piratesgui import TradeInviter
from pirates.piratesgui import TradePanel
from pirates.piratesgui import JournalButton
from pirates.piratesgui import CombatTray
from pirates.piratesgui import FriendsPage
from pirates.piratesgui import GuildPage
from pirates.piratesgui import CrewHUD
from pirates.piratesgui import CrewPage
from pirates.piratesgui import CrewInviter
from pirates.piratesgui import CrewInvitee
from pirates.piratesgui import CrewRejoin
from pirates.piratesgui import CrewBoot
from pirates.piratesgui import LeaveCrewWarning
from pirates.piratesgui import RadarGui
from pirates.piratesgui import ComboMeter
from pirates.piratesgui.Subtitler import Subtitler
from pirates.piratesgui.TextPrinter import TextPrinter
from pirates.friends import RelationshipChooser
from pirates.friends import FriendInviter
from pirates.friends import IgnoreConfirm
from pirates.friends import GuildInviter
from pirates.friends import FriendInvitee
from pirates.friends import GuildInvitee
from pirates.friends import GuildMember
from pirates.piratesgui import InventoryBagPage
from pirates.pvp import PVPInviter
from pirates.pvp import PVPInvitee
from pirates.pvp import PVPGlobals
from pirates.piratesgui import PirateProfilePage
from pirates.piratesgui.ObjectivesPanel import ObjectivesPanel
from pirates.piratesgui.TreasureMapCompletePanel import TreasureMapCompletePanel
from pirates.piratesgui.PVPCompletePanel import PVPCompletePanel
from pirates.pvp.PVPRulesPanel import PVPRulesPanel
from pirates.piratesgui import BarSelectionMenu
from pirates.piratesgui.AttuneMenu import AttuneMenu
from pirates.piratesgui import PVPPanel
from pirates.piratesgui import SheetFrame
from pirates.piratesgui import HighSeasScoreboard
from pirates.piratesgui import InvasionScoreboard
from pirates.piratesgui import HpMeter
from pirates.piratesgui import PiratesTimer
from pirates.piratesgui import PiratesTimerHourglass
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.piratesgui import MessageStackPanel
from pirates.piratesgui import TrialNonPayerPanel
from pirates.piratesgui import StayTunedPanel
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.uberdog import DistributedInventoryBase
from pirates.economy.EconomyGlobals import *
from pirates.economy import EconomyGlobals
from pirates.piratesgui import LookoutRequestLVL1
from pirates.npc.Townfolk import *
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.reputation import ReputationGlobals
from pirates.reputation import RepChart
from pirates.piratesgui.MainMenu import MainMenu
from pirates.piratesgui.DownloadBlockerPanel import DownloadBlockerPanel
from pirates.piratesgui.TeleportBlockerPanel import TeleportBlockerPanel
from pirates.piratesgui import WorkMeter
from pirates.piratesbase import Freebooter
from pirates.band import BandConstance
from pirates.quest import QuestConstants
from pirates.quest.QuestTaskDNA import MaroonNPCTaskDNA, DowsingRodTaskDNA
from pirates.quest import ClubheartsPortrait
from pirates.friends import ReportAPlayer
from pirates.piratesgui import FeedbackPanel
from pirates.piratesgui.SiegeBoard import SiegeBoard
from pirates.piratesgui.PVPBoard import PVPBoard
from pirates.inventory import InventoryUIManager
from pirates.piratesgui import ContextualTutorialPanel
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.piratesgui.ShipUpgradeInterface import ShipUpgradeInterface
from direct.showutil import BuildGeometry
from pirates.pirate import BodyDefs
from direct.distributed.ClockDelta import globalClockDelta
from pirates.piratesgui import MessageGlobals
from pirates.speedchat.PSCDecoders import *
from pirates.piratesbase import UserFunnel
import math
CHEST_FILM_OFFSET_MULT = -0.05
CHEST_FILM_OFFSET_CONST = 0.36
CHEST_FILM_Y = -0.05
FILM_NEUTRAL_OFFSET = 0.0

class GuiManager(FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('GuiManager')
    WantClothingPage = base.config.GetBool('want-clothing-page', 0)
    WantTitlesPage = base.config.GetBool('want-land-infamy', 0) or base.config.GetBool('want-sea-infamy', 0)
    tpMgr = TextPropertiesManager.getGlobalPtr()
    GMgrey = tpMgr.getProperties('grey')
    GMgrey.setGlyphShift(-0.05)
    GMgrey.setGlyphScale(0.9)
    tpMgr.setProperties('GMgrey', GMgrey)
    del tpMgr

    def __init__(self, av):
        FSM.FSM.__init__(self, 'GuiManager')
        self.av = av
        self.isTutEnabled = True
        self.ignoreAllKeys = False
        self.ignoreMainMenuHotKey = False
        self.ignoreEscapeHotKey = False
        self.ignoreAllButSkillHotKey = False
        self.ignoreAllButLookoutHotKey = False
        self.disableMainMenu = base.config.GetBool('location-kiosk', 0)
        self.levelUpIval = None
        self.deathIval = None
        self.oceanIval = None
        self.tmObjectiveList = None
        self.tmCompleteUI = None
        self.showTMCompleteLerp = None
        self.showPVPCompleteLerp = None
        self.gameRulesPanel = None
        self.timer = None
        self.timerHourglass = None
        self.scoreboard = None
        self.invasionScoreboard = None
        self.relationshipChooser = None
        self.friendInviter = None
        self.friendInvitee = None
        self.guildInviter = None
        self.guildInvitee = None
        self.guildMember = None
        self.crewInviter = None
        self.crewInvitee = None
        self.crewRejoin = None
        self.crewBoot = None
        self.leaveCrewWarning = None
        self.tradeInviter = None
        self.tradePanel = None
        self.pvpInviter = None
        self.pvpInvitee = None
        self.ignoreConfirm = None
        self.contextTutPanel = None
        self.bodySelectButton = None
        self.bodyChanger = None
        self.acceptOnce('localPirate-created', self.handleBodySelect)
        self.chatWarningBox = None
        self.accept('system message aknowledge', self.systemWarning)
        self.journalButton = None
        self.smokeFader = None
        self.dirtFader = None
        self.smokePanel = None
        self.dirtPanel = None
        self.nonPayerPanel = None
        self.stayTunedPanel = None
        self.workMeter = WorkMeter.WorkMeter()
        self.workMeter.hide()
        self.progressText = None
        self._putBackSocialPanel = 0
        self.mainMenu = None
        self.questPage = None
        self.tmButtonQuick = None
        self.tmButtonSearch = None
        self.dowsingButton = None
        self.checkPortraitButton = None
        self.clubheartsPortrait = None
        self.chatAllowed = True
        self.chestLock = 0
        self.seaChestAllowed = True
        self.socialPanelAllowed = True
        self.seaChestActive = False
        self.ignoreGuildInvites = 0
        self.ignoreInvitesAvatarList = []
        self.ignoreInvitesPlayerList = []
        self.levelUpBufferDict = {}
        self.forceLookout = base.config.GetBool('force-lookout', 0)
        self.hotkeyButtons = {}
        self.setChatAllowed(True)
        self.setSeaChestAllowed(True)
        self.warningMsg = TextPrinter()
        self.warningMsg.text.setScale(1)
        self.warningMsg.text.setPos(0, 0, -0.485)
        self.warningMsg.text['sortOrder'] = 200
        self.warningMsg.text.setBin('gui-popup', 0)
        self.warningMsg.text.setDepthTest(0)
        self.warningMsg.text.setDepthWrite(0)
        self.socialPanelReturn = False
        self.feedbackFormActive = False
        self.crewHUDTurnedOff = True
        self.gameGui = GameGui.GameGui(parent=NodePath(), state=DGG.NORMAL, relief=None, pos=(-0.2, 0, -0.27), scale=0.75, command=self.gameGuiPressed, frameSize=(0.0, 1.2, -0.03, 0.35))
        self.codeShown = 0
        self.messageStackParent = DirectFrame(parent=base.a2dBottomLeft, relief=None)
        self.messageStack = MessageStackPanel.MessageStackPanel(self.messageStackParent, relief=None, pos=(0.01,
                                                                                                           0,
                                                                                                           0.6))
        self.messageStack.setBin('gui-fixed', 2)
        self.__repValues = {}
        self.repHandlers = []
        self.chestTray = ChestTray.ChestTray(parent=NodePath(), parentMgr=self, pos=(-0.131, 0, 0.02), sortOrder=1)
        self.profilePage = PirateProfilePage.PirateProfilePage()
        self.chestPanel = ChestPanel.ChestPanel(parent=self.chestTray)
        scale = 1.0
        if base.options:
            scale = base.options.getGUIScale()
        if self.WantClothingPage:
            self.clothingPage = ClothingPage.ClothingPage()
            self.chestPanel.addPage(self.clothingPage)
        self.mapPage = MapPage.MapPage()
        self.chestPanel.addPage(self.mapPage)
        self.titlesPage = None
        if self.WantTitlesPage:
            self.titlesPage = TitlesPage.TitlesPage()
            self.chestPanel.addPage(self.titlesPage)
        self.weaponPage = WeaponPage.WeaponPage()
        self.chestPanel.addPage(self.weaponPage)
        self.shipPage = ShipPage.ShipPage()
        self.chestPanel.addPage(self.shipPage)
        self.collectionPage = CollectionPage.CollectionPage()
        self.chestPanel.addPage(self.collectionPage)
        self.collectionMain = CollectionMain.CollectionMain()
        self.chestPanel.addPage(self.collectionMain)
        self.skillPage = SkillPage.SkillPage()
        self.chestPanel.addPage(self.skillPage)
        gui = loader.loadModel('models/gui/toplevel_gui')
        self.combatTray = CombatTray.CombatTray(parent=base.a2dBottomRight)
        self.barSelection = BarSelectionMenu.BarSelectionMenu([], self.combatTray.toggleWeapon)
        self.barSelection.setPos(-0.41, 0, 0.22)
        self.barSelection.setBin('gui-popup', 0)
        self.attuneSelection = AttuneMenu()
        self.attuneSelection.setPos(-0.5, 0, -0.08)
        goldCoin = gui.find('**/treasure_w_coin*')
        self.moneyDisplay = DirectLabel(parent=NodePath(), relief=0, pos=(-0.32, 0, -0.07), scale=2, geom=goldCoin, geom_scale=0.18, geom_pos=(0.06,
                                                                                                                                               0,
                                                                                                                                               0.087), text='', text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_scale=0.02, text_pos=(0.06,
                                                                                                                                                                                                                                                                             0.045), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1)
        self.moneyDisplay.setName(self.moneyDisplay.uniqueName('moneyDisplay'))
        self.moneyDisplay.flattenStrong()
        self.moneyDisplay.hide()
        if self.av.getInventory():
            skills = self.av.getInventory().getSkills(self.av.currentWeaponId)
        self.combatTray.hideSkills()
        self.accept('localAvatarQuestComplete', self.showQuestCompleteText, extraArgs=[PLocalizer.ChatPanelQuestCompletedMsg])
        self.accept('localAvatarQuestUpdate', self.showQuestNotifyText, extraArgs=[PLocalizer.ChatPanelQuestUpdatedMsg])
        self.accept('localAvatarQuestItemUpdate', self.showQuestItemNotifyText)
        self.accept('localAvatarActiveQuestId', self.updateQuestStatusText)
        self.injuredGui = None
        self.accept('show_injured_gui', self.showInjuredGui)
        self.accept('local_pirate_exiting_injured_state', self.hideInjuredGui)
        self.bossMeter = HpMeter.HpMeter(width=1.2, height=0.02)
        self.bossMeter.setPos(-0.9, 0, -0.15)
        self.bossMeter.setScale(1.5)
        self.bossMeter.hide()
        self.targetStatusTray = StatusTray.StatusTray(parent=NodePath(), pos=(-0.225, 0, -0.25), showSkills=1)
        self.targetStatusTray.hpMeter.setPos(0.04, 0, 0.058)
        self.targetStatusTray.voodooMeter.setPos(0.043, 0, 0.045)
        self.targetStatusTray.voodooMeter.setScale(0.925, 1, 0.325)
        self.targetStatusTray.meterChangeOffset = (-0.3875, 0, -0.192)
        self.shipIcons = loader.loadModel('models/gui/ship_battle')
        self.targetStatusTray.targetFrame2 = DirectFrame(relief=None, parent=self.targetStatusTray.hpMeter, image=self.shipIcons.find('**/ship_battle_speed_bar*'), image_scale=(0.4,
                                                                                                                                                                                 1.0,
                                                                                                                                                                                 0.7), pos=(0.244,
                                                                                                                                                                                            0.0,
                                                                                                                                                                                            0.002), scale=(0.925,
                                                                                                                                                                                                           1.0,
                                                                                                                                                                                                           0.325))
        self.targetStatusTray.targetFrame = DirectFrame(relief=None, parent=self.targetStatusTray.hpMeter, image=self.shipIcons.find('**/ship_battle_speed_bar*'), image_scale=(0.43,
                                                                                                                                                                                1.0,
                                                                                                                                                                                0.7), pos=(0.244,
                                                                                                                                                                                           0.0,
                                                                                                                                                                                           0.016))
        self.targetStatusTray.hideValues = 1
        self.targetStatusTray.hpLabel.hide()
        self.targetStatusTray.voodooLabel.hide()
        self.targetStatusTray.flattenStrong()
        self.targetStatusTray.statusEffectsPanel.setScale(0.8)
        self.targetStatusTray.statusEffectsPanel.setPos(-0.15, 0, -0.0525)
        self.targetStatusTray.hide()
        self.targetStatusTray.enemyFrame = DirectFrame(relief=None, parent=self.targetStatusTray, image=self.shipIcons.find('**/ship_battle_dish02*'), image_scale=(0.35,
                                                                                                                                                                    0.35,
                                                                                                                                                                    0.35), pos=(-0.25, 0.0, -0.1725))
        self.shipTargetPanel = None
        self.socialPanel = SocialPanel.SocialPanel()
        self.socialPanel.setPos(-0.57, 0.0, 0.17)
        self.socialPanel.hide()
        self.inventoryUIManager = InventoryUIManager.InventoryUIManager()
        self.inventoryBagPage = InventoryBagPage.InventoryBagPage(self.inventoryUIManager)
        self.chestPanel.addPage(self.inventoryBagPage)
        self.chatPanel = base.chatPanel
        self.friendsPage = FriendsPage.FriendsPage(showAvatar=1, showPlayer=0, showPlayerFriendAvatars=1)
        self.socialPanel.addPage(self.friendsPage)
        self.playerFriendsPage = FriendsPage.FriendsPage(showAvatar=0, showPlayer=1)
        self.socialPanel.addPage(self.playerFriendsPage)
        self.guildPage = GuildPage.GuildPage()
        self.socialPanel.addPage(self.guildPage)
        self.crewHUD = CrewHUD.CrewHUD()
        self.crewPage = CrewPage.CrewPage(self.crewHUD)
        self.socialPanel.addPage(self.crewPage)
        self.socialPanel.setPage(self.friendsPage)
        NametagGlobals.setMasterNametagsActive(1)
        self.accept('gotoAvatar', self.handleGotoAvatar)
        self.accept(PiratesGlobals.AvatarDetailsEvent, self.handleAvatarDetails)
        self.accept(PiratesGlobals.PlayerDetailsEvent, self.handlePlayerDetails)
        self.accept('clickedNametag', self.handleClickedNametag)
        self.accept(BandConstance.BandMakeEvent, self.handleCrewInvite)
        self.accept(BandConstance.BandInvitationEvent, self.handleCrewInvitation)
        self.accept(BandConstance.BandRejoinEvent, self.handleCrewRejoin)
        self.accept(PiratesGlobals.GuildMakeEvent, self.handleGuildInvite)
        self.accept(PiratesGlobals.GuildInvitationEvent, self.handleGuildInvitation)
        self.accept(PiratesGlobals.FriendMakeEvent, self.handleAvatarFriendInvite)
        self.accept(OTPGlobals.AvatarFriendInvitationEvent, self.handleAvatarFriendInvitation)
        self.accept(OTPGlobals.PlayerFriendInvitationEvent, self.handlePlayerFriendInvitation)
        self.accept(PiratesGlobals.TradeRequestEvent, self.handleTradeInvite)
        self.accept(PiratesGlobals.TradeIncomingEvent, self.handleTradeInvitation)
        self.accept(PiratesGlobals.PVPChallengedEvent, self.handlePVPInvitation)
        self.accept(PiratesGlobals.PVPAcceptedEvent, self.handlePVPAccepted)
        self.accept(OTPGlobals.WhisperIncomingEvent, self.handleWhisperIncoming)
        self.soundWhisper = loadSfx(SoundGlobals.SFX_GUI_WHISPER)
        self.radarGui = RadarGui.RadarGui(NodePath(), self.av, sortOrder=1)
        self.radarGui.setPos(-self.radarGui.width, 0, -self.radarGui.height)
        self.minimap = None
        self.minimapRoot = aspect2d.attachNewNode('minimaps')
        self.accept(PiratesGlobals.MinimapHotkey, self.handleMinimapKeyDown)
        self.accept(PiratesGlobals.MinimapHotkey + '-up', self.handleMinimapKeyUp)
        gui = loader.loadModel('models/gui/compass_main')
        self.trackedQuestLabel = DirectLabel(parent=base.a2dTopRight, relief=None, image=gui.find('**/icon_objective_grey'), image_color=Vec4(1, 1, 0, 1), image_scale=0.14, image_pos=(-0.03, 0, 0.012), text='', text_fg=PiratesGuiGlobals.TextFG2, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=12, pos=(-0.9, 0, -0.05))
        if base.downloadWatcher:
            self.trackedQuestLabel.setPos(-0.9, 0, -0.2)
        self.trackedQuestLabel.hide()
        self.questStatusText = ''
        self.questHintText = ''
        self.questTimerText = ''
        self.lookoutPopup2DNode = None
        self.lookoutPage = LookoutRequestLVL1.LookoutRequestLVL1(PLocalizer.LookoutPanelTitle, base.cr.matchMaker, self)
        self.chestPanel.addPage(self.lookoutPage)
        self.createLookoutPopup()
        self.contextTutPanel = ContextualTutorialPanel.ContextualTutorialPanel()
        self.accept('highSeasScoreBoardClose', self.removeScoreboard)
        self.accept('invasionScoreBoardClose', self.removeInvasionScoreboard)
        self.accept('guiMgrToggleBossMeter', self.toggleBossMeter)
        self.accept('guiMgrToggleInventory', self.showInventoryBagPanel)
        self.accept('guiMgrToggleSocial', self.toggleSocialPanel)
        self.accept('guiMgrToggleRadar', self.handleRadarToggle)
        self.accept('guiMgrToggleMap', self.showMapPage)
        self.accept('guiMgrToggleWeapons', self.showWeaponPanel)
        if self.WantClothingPage:
            self.accept('guiMgrToggleClothing', self.showClothingPanel)
        if self.WantTitlesPage:
            self.accept('guiMgrToggleTitles', self.showTitlesPanel)
        self.accept('guiMgrToggleShips', self.showShipPanel)
        self.accept('guiMgrToggleTreasures', self.showTreasurePanel)
        self.accept(PiratesGlobals.TreasureHotkey, self.showTreasurePanel)
        self.accept(PiratesGlobals.TreasureHotkey2, self.showTreasurePanel)
        self.accept('guiMgrToggleLevels', self.showSkillPage)
        self.accept('guiMgrToggleQuest', self.showQuestPanel)
        self.accept('guiMgrToggleLookout', self.showLookoutPanel)
        self.accept('guiMgrToggleMainMenu', self.toggleMainMenu)
        self.oceanMsg = DirectFrame(parent=self.gameGui, relief=None, text='Ocean Zone', text_fg=PiratesGuiGlobals.TextFG2, text_scale=0.4, text_font=PiratesGlobals.getPirateOutlineFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_align=TextNode.ACenter, frameSize=(-1, 1, -0.5, 0.5), frameColor=(0.5,
                                                                                                                                                                                                                                                                                                              0.5,
                                                                                                                                                                                                                                                                                                              0.5,
                                                                                                                                                                                                                                                                                                              1.0), pos=(2.0, 0, -0.3))
        self.oceanMsg.setScale(0.1)
        self.oceanMsg.hide()
        self.pvpPanel = None
        self.pvpStatus = None
        self.siegeStatus = None
        self.pvpCompleteUI = None
        self.titler = TextPrinter()
        self.titler.text.setPos(0, 0, 0)
        self.titler.text['text_scale'] = PiratesGuiGlobals.TextScaleTitleJumbo
        self.titler.text.setScale(1)
        self.secondarytitler = TextPrinter()
        self.secondarytitler.text.setPos(0, 0, -0.1)
        self.secondarytitler.text['text_scale'] = PiratesGuiGlobals.TextScaleTitleMed
        self.secondarytitler.text.setScale(1)
        self.subtitler = Subtitler()
        self.subtitler.text['text_wordwrap'] = 28
        self.dialogSubtitler = Subtitler()
        self.dialogSubtitler.text['text_wordwrap'] = 28
        self.dialogSubtitler.text.wrtReparentTo(aspect2d)
        self.dialogSubtitler.text.setPos(-0.49, 0, -0.55)
        self.dialogSubtitler.text.setBin('gui-fixed', 1)
        self.dialogSubtitler.confirmButton.reparentTo(aspect2d)
        self.dialogSubtitler.specialButtonImage = GuiButton.redGenericButton
        self.dialogSubtitler.confirmButton['image'] = GuiButton.redGenericButton
        self.dialogSubtitler.confirmButton['image_scale'] = (0.6, 0.6, 0.6)
        self.dialogSubtitler.confirmButton.setPos(0.2, 0, -0.71)
        self.dialogSubtitler.confirmButton.setBin('gui-fixed', 1)
        self.interactionalSubtitler = Subtitler()
        self.progressMsg = TextPrinter()
        self.progressMsg.text.setPos(0, 0, 0.3)
        self.interactionalFrame = None
        self.bg = None
        self.comboMeter = ComboMeter.ComboMeter()
        self.offscreenHitEffects = None
        self.offscreenHitIvals = None
        self.injuredEffects = None
        self.injuredBlackoutGeom = None
        self.injuredTrack = None
        self.stickySeaChestIcons = []
        self.effectIvals = []
        self.pirateCode = None
        self.mouseX, self.mouseY = (0, 0)
        self.reportAPlayer = None
        self.prevTag = None
        self.createPreviewTag()
        self.bossMeter.reparentTo(base.a2dTopCenter)
        self.targetStatusTray.reparentTo(base.a2dTopCenter)
        self.barSelection.reparentTo(base.a2dBottomCenter)
        self.gameGui.reparentTo(base.a2dTopLeft)
        self.moneyDisplay.reparentTo(base.a2dBottomRight)
        self.socialPanel.reparentTo(base.a2dBottomRight)
        self.chestTray.reparentTo(base.a2dBottomRight)
        self.radarGui.reparentTo(base.a2dTopRight)
        self.warningMsg.text.reparentTo(aspect2d)
        self.titler.text.reparentTo(aspect2d)
        self.secondarytitler.text.reparentTo(aspect2d)
        self.setUIScale(base.options.gui_scale * 0.6 + 0.7)
        self.filmOffsetLerp = None
        self.filmShouldOffset = 0
        self.chestPanel.makeCurPage(self.inventoryBagPage)
        self.instructionMessageText = None
        self.instructionMessageBoxText = None
        self.instructionMessageQueue = []
        self.instructionMessageActive = 0
        self.instructionMessageLockObj = None
        self.currentInstructionMessage = None
        self.instructionMessageSoundIval = None
        self.currentInstructionTime = None
        self.lastlockingInstructionMessageCat = None
        self.lastlockingInstructionMessageTime = None
        self.iMBsizeX = 0.96
        self.iMBsizeZ = 0.17
        iMBmodelName = 'pir_m_gui_frm_subframe'
        iMBimageColorScale = VBase4(0.75, 0.75, 0.9, 1.0)
        self.iMBtextScale = 0.045
        iMBframeSize = (-0.0 * self.iMBsizeX, 1.0 * self.iMBsizeX, -0.0 * self.iMBsizeZ, 1.0 * self.iMBsizeZ)
        self.instructionMessageBoxText = BorderFrame(parent=base.a2dBottomCenter, frameSize=iMBframeSize, modelName=iMBmodelName, imageColorScale=iMBimageColorScale, pos=(self.iMBsizeX * -0.5, 0, 0.3), textMayChange=1, text='', text_scale=self.iMBtextScale, text_align=TextNode.ACenter, text_pos=(self.iMBsizeX * 0.5, 0.09), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                                                                                     1), text_wordwrap=self.iMBsizeX * 0.9 / self.iMBtextScale, text_font=PiratesGlobals.getInterfaceFont())
        self.instructionMessageBoxText.hide()
        self.instructionMessageBoxText.setBin('gui-popup', 1)
        self.instructionMessageText = DirectLabel(parent=base.a2dBottomCenter, pos=(self.iMBsizeX * -0.5, 0, 0.3), textMayChange=1, text='', text_scale=self.iMBtextScale, text_align=TextNode.ACenter, text_pos=(self.iMBsizeX * 0.5, 0.09), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=(0,
                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                              0,
                                                                                                                                                                                                                                                                                              1), text_wordwrap=self.iMBsizeX * 0.9 / self.iMBtextScale, text_font=PiratesGlobals.getInterfaceFont())
        self.instructionMessageText.setBin('gui-popup', 1)
        self.instructionMessageText.hide()
        self.instructionMessageIcon = DirectLabel(parent=self.instructionMessageText)
        base.ibt = self.instructionMessageBoxText
        self.shipUpgradeInterface = None
        return

    def getTutorialStatus(self):
        if self.av.style:
            return self.av.style.getTutorial()
        else:
            return 0

    def handleRadarToggle(self, message=None):
        if self.getTutorialStatus() >= PiratesGlobals.TUT_GOT_COMPASS:
            self.radarGui.toggle()

    def delete(self):
        if self.mainMenu:
            self.mainMenu.destroy()
        self.trackedQuestLabel.destroy()
        self.hidePVPInstructions()
        self.removePVPStatus()
        self.removePVPUI()
        self.removePVPCompleteUI()
        self.moneyDisplay.destroy()
        self._showMouse()
        self.setChatAllowed(False)
        self.setSeaChestAllowed(False)
        self.ignoreAll()
        if self.pirateCode:
            self.pirateCode.destroy()
        self.chestPanel.destroy()
        self.gameGui.destroy()
        self.radarGui.destroy()
        self.combatTray.destroy()
        self.chestTray.destroy()
        self.barSelection.destroy()
        self.attuneSelection.destroy()
        self.comboMeter.destroy()
        self.socialPanel.destroy()
        self.inventoryUIManager.destroy()
        self.removeScoreboard()
        self.removeInvasionScoreboard()
        if self.filmOffsetLerp:
            self.filmOffsetLerp.pause()
            self.filmOffsetLerp = None
        if self.nonPayerPanel:
            self.nonPayerPanel.destroy()
            self.nonPayerPanel = None
        if self.stayTunedPanel:
            self.stayTunedPanel.destroy()
            self.stayTunedPanel = None
        self.chatPanel = None
        if self.lookoutPage:
            self.lookoutPage.ignore(self.lookoutPopup.getUniqueId())
            self.lookoutPage.destroy()
            self.lookoutPage = None
        self.titler.destroy()
        self.secondarytitler.destroy()
        self.subtitler.destroy()
        self.dialogSubtitler.destroy()
        self.interactionalSubtitler.destroy()
        if self.interactionalFrame:
            self.interactionalFrame.destroy()
        self.bossMeter.destroy()
        self.warningMsg.destroy()
        self.progressMsg.destroy()
        self.removeNewQuestIndicator()
        self.targetStatusTray.targetFrame.destroy()
        self.targetStatusTray.enemyFrame.destroy()
        self.targetStatusTray.destroy()
        self.deleteLevelUpText()
        taskMgr.remove('processLevelUpBuffer')
        taskMgr.remove('hidePirateCode')
        taskMgr.remove('clearTopTen')
        taskMgr.remove('clearWarning')
        taskMgr.remove('clearTitle')
        taskMgr.remove('clearSubtitle')
        taskMgr.remove('clearProgress')
        taskMgr.remove('titles-refresh')
        taskMgr.remove('guiMgrChangeQuestStatus')
        if self.oceanIval:
            del self.oceanIval
        if self.timer:
            self.timer.destroy()
            self.timer = None
        if self.timerHourglass:
            self.timerHourglass.destroy()
            self.timerHourglass = None
        if hasattr(self, '_dlBlocker'):
            self._dlBlocker.destroy()
            del self._dlBlocker
        if self.tradeInviter:
            self.tradeInviter.destroy()
            del self.tradeInviter
        if self.tradePanel:
            self.tradePanel.destroy()
            del self.tradePanel
        if self.guildInviter:
            self.guildInviter.destroy()
            del self.guildInviter
        if self.guildMember:
            self.guildMember.destroy()
            del self.guildMember
        if self.guildInvitee:
            self.guildInvitee.destroy()
            del self.guildInvitee
        if self.friendInviter:
            self.friendInviter.destroy()
            del self.friendInviter
        if self.friendInvitee:
            self.friendInvitee.destroy()
            del self.friendInvitee
        if self.pvpInviter:
            self.pvpInviter.destroy()
            del self.pvpInviter
        if self.pvpInvitee:
            self.pvpInvitee.destroy()
            del self.pvpInvitee
        if self.crewInviter:
            self.crewInviter.destroy()
            del self.crewInviter
        if self.crewInvitee:
            self.crewInvitee.destroy()
            del self.crewInvitee
        if self.crewRejoin:
            self.crewRejoin.destroy()
            del self.crewRejoin
        if self.crewBoot:
            self.crewBoot.destroy()
            del self.crewBoot
        if self.leaveCrewWarning:
            self.leaveCrewWarning.destroy()
            del self.leaveCrewWarning
        if self.ignoreConfirm:
            self.ignoreConfirm.destroy()
            del self.ignoreConfirm
        if self.reportAPlayer:
            self.reportAPlayer.destroy()
            del self.reportAPlayer
        if self.workMeter:
            self.workMeter.destroy()
            del self.workMeter
        if self.crewHUD:
            self.crewHUD.destroy()
            del self.crewHUD
        if self.profilePage:
            self.profilePage.destroy()
            del self.profilePage
        if self.contextTutPanel:
            self.contextTutPanel.destroy()
            del self.contextTutPanel
        if self.minimap:
            del self.minimap
        if self.bodySelectButton:
            self.bodySelectButton.destroy()
        self.killInstructionMessageQueue()
        if self.instructionMessageText:
            self.instructionMessageText.destroy()
            self.instructionMessageText = None
        if self.instructionMessageBoxText:
            self.instructionMessageBoxText.destroy()
            self.instructionMessageBoxText = None
        NametagGlobals.setMasterNametagsActive(0)
        if self.offscreenHitEffects:
            for effect in self.offscreenHitEffects:
                effect.removeNode()

        del self.offscreenHitEffects
        if self.offscreenHitIvals:
            for ival in self.offscreenHitIvals:
                ival.pause()

        del self.offscreenHitIvals
        del self.av
        if self.injuredTrack:
            self.injuredTrack.pause()
            self.injuredTrack = None
        if self.injuredEffects:
            for effect in self.injuredEffects:
                effect.removeNode()

            self.injuredBlackoutGeom.removeNode()
        self.deleteLookoutPopup()
        for currEffectIval in self.effectIvals:
            currEffectIval.pause()

        self.effectIvals = []
        if self.instructionMessageSoundIval:
            self.instructionMessageSoundIval.finish()
            self.instructionMessageSoundIval = None
        if self.progressText:
            self.showProgressIval.pause()
            self.showProgressIval = None
            self.progressText.destroy()
            self.progressText = None
        if self.messageStack:
            self.messageStack.destroy()
            self.messageStack = None
            self.messageStackParent.destroy()
            self.messageStackParent = None
        if self.tmButtonQuick:
            self.tmButtonQuick.destroy()
            self.tmButtonQuick = None
        if self.tmButtonSearch:
            self.tmButtonSearch.destroy()
            self.tmButtonSearch = None
        if self.dowsingButton:
            self.dowsingButton.destroy()
            self.dowsingButton = None
        if self.checkPortraitButton:
            self.checkPortraitButton.destroy()
            self.checkPortraitButton = None
        if self.clubheartsPortrait:
            self.clubheartsPortrait.destroy()
            self.clubheartsPortrait = None
        if self.shipUpgradeInterface:
            self.shipUpgradeInterface.destroy()
        return

    def toggleShipUpgrades(self):
        if self.shipUpgradeInterface.isHidden():
            self.shipUpgradeInterface.show()
            self.shipUpgradeInterface.onOpen()
        else:
            self.shipUpgradeInterface.hide()
            self.shipUpgradeInterface.onClose()

    def openShipUpgrades(self, shipId, callback=None):
        if self.shipUpgradeInterface == None:
            self.shipUpgradeInterface = ShipUpgradeInterface(base.a2dTopCenter)
        self.shipUpgradeInterface.setPos(-0.3, 0.0, -0.9)
        self.shipUpgradeInterface.show()
        self.shipUpgradeInterface.onOpen(shipId, callback)
        return

    def closeShipUpgrades(self):
        if self.shipUpgradeInterface:
            self.shipUpgradeInterface.destroy()
        self.shipUpgradeInterface = None
        return

    def queueInstructionMessage(self, messageText, messageSoundList=[], messageGraphic=None, graphicScale=1.0, messageCategory=MessageGlobals.MSG_CAT_DEFAULT):
        lastMessage = None
        if self.instructionMessageQueue:
            lastMessage = self.instructionMessageQueue[len(self.instructionMessageQueue) - 1]
        if messageCategory and self.currentInstructionMessage and messageCategory == self.currentInstructionMessage[4]:
            return
        if messageCategory and lastMessage and messageCategory == lastMessage[4]:
            return
        message = (messageText, messageSoundList, messageGraphic, graphicScale, messageCategory)
        if self.instructionMessageLockObj:
            return
        self.instructionMessageQueue.append(message)
        if self.instructionMessageActive:
            pass
        else:
            self.doInstructionMessageQueue()
        return

    def queueInstructionMessageFront(self, messageText, messageSoundList=[], messageGraphic=None, graphicScale=1.0, messageCategory=MessageGlobals.MSG_CAT_DEFAULT):
        message = (
         messageText, messageSoundList, messageGraphic, graphicScale, messageCategory)
        if self.instructionMessageLockObj:
            return
        self.instructionMessageQueue.insert(0, message)
        if self.currentInstructionMessage:
            if self.currentInstructionTime and message[4] and message[4] == self.currentInstructionMessage[4]:
                self.currentInstructionMessage = None
                self.currentInstructionTime = None
            elif self.currentInstructionTime and globalClockDelta.localElapsedTime(self.currentInstructionTime) < 2.5:
                self.instructionMessageQueue.insert(1, self.currentInstructionMessage)
            else:
                self.currentInstructionMessage = None
                self.currentInstructionTime = None
        taskMgr.remove('doInstructionMessageQueue')
        self.doInstructionMessageQueue()
        return

    def doInstructionMessageQueue(self, task=None):
        if self.instructionMessageActive:
            pass
        else:
            taskMgr.remove('hideLockedMessage')
            self.instructionMessageActive = 1
            self.instructionMessageText.show()
            if localAvatar.getGameState() in ['Cannon']:
                self.instructionMessageBoxText.setPos(self.iMBsizeX * -0.5, 0, 0.5)
                self.instructionMessageText.setPos(self.iMBsizeX * -0.5, 0, 0.5)
            else:
                self.instructionMessageBoxText.setPos(self.iMBsizeX * -0.5, 0, 0.37)
                self.instructionMessageText.setPos(self.iMBsizeX * -0.5, 0, 0.37)
            if len(self.instructionMessageQueue) > 0:
                newMessage = self.instructionMessageQueue.pop(0)
                messageCategory = newMessage[4]
                msgCatInfo = MessageGlobals.MessageOptions[messageCategory]
                self.currentInstructionMessage = newMessage
                self.currentInstructionTime = globalClockDelta.getFrameNetworkTime()
                self.instructionMessageText['text'] = msgCatInfo['messagePrefix'] + newMessage[0]
                taskMgr.doMethodLater(msgCatInfo['messageTime'], self.doInstructionMessageQueue, 'doInstructionMessageQueue')
                if not base.firstMateVoiceOn and messageCategory in [MessageGlobals.MSG_CAT_THREAT_LEVEL, MessageGlobals.MSG_CAT_NO_PORT, MessageGlobals.MSG_CAT_TELL_PORT, MessageGlobals.MSG_CAT_ANNOUNCE_ATTACK, MessageGlobals.MSG_CAT_SUNK_SHIP]:
                    pass
                else:
                    messageSoundList = newMessage[1]
                    if self.instructionMessageSoundIval:
                        self.instructionMessageSoundIval.finish()
                    self.instructionMessageSoundIval = Sequence()
                    for sound in messageSoundList:
                        self.instructionMessageSoundIval.append(SoundInterval(loadSfx(sound), seamlessLoop=False))

                    self.instructionMessageSoundIval.start()
                messageImage = newMessage[2]
                messageImageScale = newMessage[3]
                if msgCatInfo['showBorder?']:
                    self.instructionMessageBoxText.show()
                else:
                    self.instructionMessageBoxText.hide()
                self.instructionMessageText['text_fg'] = msgCatInfo['text_fg']
                self.instructionMessageText['text_shadow'] = msgCatInfo['text_shadow']
                self.instructionMessageText['text_font'] = msgCatInfo['text_font']
                self.instructionMessageText['text_scale'] = msgCatInfo['text_scale']
                self.instructionMessageBoxText.setColorScale(msgCatInfo['text_fg'])
                self.instructionMessageText['text_wordwrap'] = self.iMBsizeX * 0.9 / msgCatInfo['text_scale']
                if messageImage:
                    self.instructionMessageIcon['image'] = messageImage
                    self.instructionMessageIcon['image_scale'] = messageImageScale * 0.15
                    self.instructionMessageIcon['image_pos'] = (0.08, 0.0, self.iMBsizeZ * 0.5)
                    self.instructionMessageIcon.show()
                    self.instructionMessageText['text_pos'] = (self.iMBsizeX * 0.57, 0.12)
                    self.instructionMessageText['text_wordwrap'] = self.iMBsizeX * 0.8 / msgCatInfo['text_scale']
                else:
                    self.instructionMessageIcon['image'] = None
                    self.instructionMessageIcon.hide()
                    self.instructionMessageText['text_pos'] = (self.iMBsizeX * 0.5, 0.12)
                    self.instructionMessageText['text_wordwrap'] = self.iMBsizeX * 0.9 / msgCatInfo['text_scale']
            else:
                self.instructionMessageText['text'] = ''
                self.currentInstructionMessage = None
                self.currentInstructionTime = None
                self.instructionMessageText.hide()
                self.instructionMessageBoxText.hide()
                self.instructionMessageQueue = []
                self.instructionMessageActive = 0
                self.instructionMessageText['image'] = None
                taskMgr.remove('doInstructionMessageQueue')
                taskMgr.remove('hideLockedMessage')
            if task:
                return task.done
        return

    def lockInstructionMessage(self, lockingObj, messageText, messageSoundList=[], messageGraphic=None, graphicScale=1.0, messageCategory=MessageGlobals.MSG_CAT_DEFAULT):
        newMessage = (
         messageText, messageSoundList, messageGraphic, graphicScale, messageCategory)
        if lockingObj and self.instructionMessageLockObj == None:
            self.instructionMessageLockObj = lockingObj
        else:
            return False
        self.killInstructionMessageQueue()
        msgCatInfo = MessageGlobals.MessageOptions[messageCategory]
        self.instructionMessageText['text'] = newMessage[0]
        self.instructionMessageText.show()
        if msgCatInfo['showBorder?']:
            self.instructionMessageBoxText.show()
        else:
            self.instructionMessageBoxText.hide()
        if localAvatar.getGameState() in ['Cannon']:
            self.instructionMessageBoxText.setPos(self.iMBsizeX * -0.5, 0, 0.5)
            self.instructionMessageText.setPos(self.iMBsizeX * -0.5, 0, 0.5)
        else:
            self.instructionMessageBoxText.setPos(self.iMBsizeX * -0.5, 0, 0.37)
            self.instructionMessageText.setPos(self.iMBsizeX * -0.5, 0, 0.37)
        self.instructionMessageText['text_fg'] = msgCatInfo['text_fg']
        self.instructionMessageText['text_shadow'] = msgCatInfo['text_shadow']
        self.instructionMessageText['text_font'] = msgCatInfo['text_font']
        self.instructionMessageText['text_scale'] = msgCatInfo['text_scale']
        self.instructionMessageBoxText.setColorScale(msgCatInfo['text_fg'])
        self.instructionMessageText['text_wordwrap'] = self.iMBsizeX * 0.9 / msgCatInfo['text_scale']
        if messageGraphic:
            self.instructionMessageIcon['image'] = messageImage
            self.instructionMessageIcon['image_scale'] = messageImageScale * 0.15
            self.instructionMessageIcon['image_pos'] = (0.08, 0.0, self.iMBsizeZ * 0.5)
            self.instructionMessageIcon.show()
            self.instructionMessageText['text_pos'] = (self.iMBsizeX * 0.57, 0.12)
            self.instructionMessageText['text_wordwrap'] = self.iMBsizeX * 0.8 / msgCatInfo['text_scale']
        else:
            self.instructionMessageIcon['image'] = None
            self.instructionMessageIcon.hide()
            self.instructionMessageText['text_pos'] = (self.iMBsizeX * 0.5, 0.12)
            self.instructionMessageText['text_wordwrap'] = self.iMBsizeX * 0.9 / msgCatInfo['text_scale']
        if self.lastlockingInstructionMessageTime and globalClockDelta.localElapsedTime(self.lastlockingInstructionMessageTime) < 4.0 and messageCategory == self.lastlockingInstructionMessageCat:
            pass
        else:
            messageSoundList = newMessage[1]
            if self.instructionMessageSoundIval:
                self.instructionMessageSoundIval.finish()
            self.instructionMessageSoundIval = Sequence()
            for sound in messageSoundList:
                self.instructionMessageSoundIval.append(SoundInterval(loadSfx(sound), seamlessLoop=False))

            self.instructionMessageSoundIval.start()
            self.lastlockingInstructionMessageTime = globalClockDelta.getFrameNetworkTime()
        self.lastlockingInstructionMessageCat = messageCategory
        return True

    def unlockInstructionMessage(self, lockingObj):
        if lockingObj and self.instructionMessageLockObj == lockingObj:
            self.instructionMessageLockObj = None
            msgCatInfo = MessageGlobals.MessageOptions[self.lastlockingInstructionMessageCat]
            residualTime = msgCatInfo['messageTime']
            if residualTime:
                taskMgr.doMethodLater(residualTime, self.hideLockedMessage, 'hideLockedMessage')
            else:
                self.hideLockedMessage()
        return

    def forceUnlockInstructionMessage(self):
        self.instructionMessageLockObj = None
        msgCatInfo = MessageGlobals.MessageOptions[self.lastlockingInstructionMessageCat]
        residualTime = msgCatInfo['messageTime']
        if residualTime:
            taskMgr.doMethodLater(residualTime, self.hideLockedMessage, 'hideLockedMessage')
        else:
            self.hideLockedMessage()
        return

    def hideLockedMessage(self, task=None):
        self.instructionMessageBoxText.hide()
        self.instructionMessageText.hide()

    def killInstructionMessageQueue(self, task=None):
        taskMgr.remove('doInstructionMessageQueue')
        taskMgr.remove('hideLockedMessage')
        self.instructionMessageQueue = []
        self.instructionMessageActive = 0
        self.currentInstructionMessage = None
        self.currentInstructionTime = None
        self.instructionMessageText.hide()
        self.instructionMessageBoxText.hide()
        if task:
            return task.done
        return

    def handleBodySelect(self):
        if not base.config.GetBool('want-body-prompt', 0):
            return
        gender = localAvatar.getStyle().gender
        oldShape = localAvatar.getStyle().getBodyShape()
        if not base.config.GetBool('want-body-prompt-all', 0):
            if gender == 'f':
                if oldShape in BodyDefs.BodyChoicesFemale:
                    return
            elif gender == 'm':
                if oldShape in BodyDefs.BodyChoicesMale:
                    return
        if self.bodySelectButton:
            return
        topGui = loader.loadModel('models/gui/toplevel_gui')
        gui2 = loader.loadModel('models/textureCards/basic_unlimited')
        norm_geom = gui2.find('**/but_nav')
        over_geom = gui2.find('**/but_nav_over')
        down_geom = gui2.find('**/but_nav_down')
        dsbl_geom = gui2.find('**/but_nav_disabled')
        self.bodySelectGui = DirectFrame(parent=base.a2dTopRight, relief=None, pos=(-0.2, 0, -0.45))
        self.bodySelectButton = DirectButton(parent=self.bodySelectGui, relief=None, geom=(norm_geom, down_geom, over_geom), pos=(0.0, 0, -0.08), scale=0.65, command=self.askForBodySelect, text=PLocalizer.BodyChangeButton, text_fg=PiratesGuiGlobals.TextFG2, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_scale=0.07, text_wordwrap=9, text_pos=(0, -0.02))
        return

    def askForBodySelect(self):
        if localAvatar.getGameState() not in ('LandRoam', 'Battle'):
            return
        from pirates.makeapirate import BodyShapeChanger
        if not self.bodyChanger:
            self.bodyChanger = BodyShapeChanger.BodyShapeChanger()
        if self.bodyChanger:
            self.bodyChanger.show()

    def showInjuredGui(self):
        self.chestTray.hide()
        if self.filmOffsetLerp:
            self.filmOffsetLerp.pause()
            self.filmOffsetLerp = None
        self.setFilmOffsetX(0.0)
        self.setFilmOffsetY(0.0)
        self.combatTray.hide()
        if self.injuredGui:
            self.injuredGui.show()
        else:
            topGui = loader.loadModel('models/gui/toplevel_gui')
            gui2 = loader.loadModel('models/textureCards/basic_unlimited')
            norm_geom = gui2.find('**/but_nav')
            over_geom = gui2.find('**/but_nav_over')
            down_geom = gui2.find('**/but_nav_down')
            dsbl_geom = gui2.find('**/but_nav_disabled')
            self.injuredGui = DirectFrame(parent=base.a2dBottomRight, relief=None, pos=(-0.4, 0, 0.3))
            self.gotoJailText = DirectLabel(parent=self.injuredGui, relief=None, frameSize=(-0.25, 0.25, -0.25, 0.25), image=topGui.find('**/pir_t_gui_gen_parchment'), image_scale=(0.345,
                                                                                                                                                                                     0,
                                                                                                                                                                                     0.465), scale=1.0, text=PLocalizer.InjuredOrHelp, text_fg=PiratesGuiGlobals.TextFG0, text_font=PiratesGlobals.getPirateFont(), text_scale=0.04, text_wordwrap=13, text_pos=(0,
                                                                                                                                                                                                                                                                                                                                                                 0.07))
            defeatedText = DirectLabel(parent=self.gotoJailText, relief=None, scale=1.0, text=PLocalizer.InjuredDefeated, text_fg=PiratesGuiGlobals.TextFG23, text_font=PiratesGlobals.getPirateFont(), text_scale=0.05, text_wordwrap=12, text_pos=(0,
                                                                                                                                                                                                                                                     0.12))
            self.gotoJailButton = DirectButton(parent=self.injuredGui, relief=None, geom=(norm_geom, down_geom, over_geom), pos=(0.0, 0, -0.08), scale=0.65, command=self.askForJail, text=PLocalizer.InjuredGotoJail, text_fg=PiratesGuiGlobals.TextFG2, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_scale=0.07, text_wordwrap=9, text_pos=(0, -0.02))
            self.injuredHeartbeat = loader.loadSfx('audio/sfx_heartbeat_slow.wav')
            self.injuredHeartbeat.setLoop(True)
        self.injuredHeartbeat.setVolume(0.5)
        self.injuredHeartbeat.setPlayRate(0.75)
        self.injuredHeartbeat.play()
        self.startInjuredEffect()
        return

    def askForJail(self):
        messenger.send('asked_for_jail', [])

    def hideInjuredGui(self):
        self.chestTray.show()
        self.combatTray.show()
        if self.injuredGui:
            self.injuredGui.hide()
        self.finishInjuredEffect()
        self.injuredHeartbeat.stop()

    def toggleBossMeter(self):
        if self.bossMeter.isHidden():
            self.bossMeter.show()
        else:
            self.bossMeter.hide()

    def updateBossMeter(self, hp, maxHp):
        self.bossMeter.update(hp, maxHp)

    def showBossMeter(self):
        if self.bossMeter:
            self.bossMeter.show()

    def hideBossMeter(self):
        if self.bossMeter:
            self.bossMeter.hide()

    def initQuestPage(self):

        def inventoryReceived(inventory):
            if inventory:
                self.questPage = QuestPage.QuestPage()
                self.questPage.updateQuestTitles(findNewTrackable=False)
                self.questPage.hide()
                self.chestPanel.addPage(self.questPage, index=6)
                self.showBlackPearlButtonsForTest()
                if localAvatar.activeQuestId:
                    quest = localAvatar.getQuestById(localAvatar.activeQuestId)
                    if quest:
                        timeLimit = quest.questDNA.getTimeLimit()
                        if quest.isCompleteWithBonus() or timeLimit and not quest.getTimeRemaining():
                            statusText = quest.getReturnText()
                        else:
                            statusText = quest.getStatusText()
                        self.setQuestStatusText(statusText)

        if not self.questPage:
            DistributedInventoryBase.DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), inventoryReceived)

    def toggleShipPageVis(self):
        self.shipPage.toggleVis()

    def updateUnspent(self, category, value):
        if self.skillPage:
            self.skillPage.updateUnspent(category, value)
        if localAvatar.isWeaponDrawn:
            self.combatTray.initCombatTray(WeaponGlobals.getRepId(localAvatar.currentWeaponId))

    def updateSkillUnlock(self, skillId, amt):
        if self.skillPage:
            self.skillPage.updateSkillUnlock(skillId)
        if localAvatar.isWeaponDrawn:
            self.combatTray.initCombatTray(WeaponGlobals.getRepId(localAvatar.currentWeaponId))

    def updateTonic(self, tonicId):
        self.combatTray.updateBestTonic()

    def updateShipRepairKit(self, kitId):
        self.combatTray.updateShipRepairKits()

    def registerReputationHandler(self, handler):
        self.repHandlers.append(handler)

    def unregisterReputationHandler(self, handler):
        self.repHandlers.remove(handler)

    def updateReputation(self, category, value):
        totalReputation = 0
        inv = self.av.getInventory()
        if inv:
            totalReputation = inv.getReputation(InventoryType.OverallRep)
        else:
            self.notify.warning('updateReputation: inventory not created')
        self.gameGui.repMeter.update(totalReputation, updateLocal=1)
        if self.skillPage.getRep() == category:
            self.skillPage.repMeter.update(value)
        weaponPanel = self.weaponPage.weaponPanels.get(category)
        if weaponPanel and weaponPanel.repMeter:
            weaponPanel.repMeter.update(value)
        if category == InventoryType.FishingRep and self.weaponPage.fishingRepMeter:
            self.weaponPage.fishingRepMeter.update(value)
        if category == InventoryType.PotionsRep and self.weaponPage.potionRepMeter:
            self.weaponPage.potionRepMeter.update(value)
        self.combatTray.updateWeaponRep(category, value)
        self.barSelection.updateRep(category, value)
        oldValue = self.__repValues.get(category, None)
        self.__repValues[category] = value
        if inv:
            vtLevel = inv.getStackQuantity(InventoryType.Vitae_Level)
            vtCost = inv.getStackQuantity(InventoryType.Vitae_Cost)
            vtLeft = inv.getStackQuantity(InventoryType.Vitae_Left)
            self.gameGui.updateVitae(vtLevel, vtCost, vtLeft)
        for handler in self.repHandlers:
            handler(category, value)

        return

    def setEquippedWeapons(self, equippedWeapons):
        if equippedWeapons:
            if self.combatTray:
                self.combatTray.setEquippedWeapons(equippedWeapons)

    def cleanupEquippedWeapons(self):
        if self.combatTray:
            self.combatTray.cleanupEquippedWeapons()

    def setCurrentWeapon(self, currentWeapon, isWeaponDrawn, slotId):
        if self.combatTray:
            self.combatTray.setCurrentWeapon(currentWeapon, isWeaponDrawn, slotId)
        if self.skillPage and not self.skillPage.isHidden():
            self.skillPage.update()

    def refreshInventoryWeapons(self, newWeaponId=None):
        equipped = []
        if self.combatTray.slotDisplay:
            for i in range(0, len(self.combatTray.slotDisplay.cellList)):
                if localAvatar.guiMgr.combatTray.slotDisplay.cellList[i].hotlink:
                    equipped.append([localAvatar.guiMgr.combatTray.slotDisplay.cellList[i].hotlink.getId(), localAvatar.guiMgr.combatTray.slotDisplay.slotList[i]])

        self.barSelection.update(equipped)
        currentWeapon = localAvatar.guiMgr.combatTray.weaponId
        if currentWeapon and currentWeapon not in equipped:
            skillCategory = getSkillCategory(currentWeapon)
        self.weaponPage.refreshList()

    def listenMoney(self, coins):
        self.setMoney(coins)

    def deleteLevelUpText(self):
        if not self.levelUpIval:
            return
        if self.levelUpIval:
            self.levelUpIval.pause()
            self.levelUpIval = None
        self.levelUpLabel.destroy()
        self.levelUpCategoryLabel.destroy()
        self.levelUpText.removeNode()
        del self.levelUpSfx
        return

    def createLevelUpText(self):
        if self.levelUpIval:
            return
        self.levelUpSfx = loadSfx(SoundGlobals.SFX_GUI_LEVELUP)
        self.levelUpSfx.setVolume(0.5)
        self.levelUpText = NodePath('levelUpText')
        self.levelUpLabel = DirectLabel(parent=self.levelUpText, relief=None, text='', text_font=PiratesGlobals.getPirateOutlineFont(), text_fg=(0.1,
                                                                                                                                                 0.7,
                                                                                                                                                 0.1,
                                                                                                                                                 1), scale=0.25)
        self.levelUpCategoryLabel = DirectLabel(parent=self.levelUpText, relief=None, text='', text_font=PiratesGlobals.getPirateOutlineFont(), text_fg=(0.1,
                                                                                                                                                         0.7,
                                                                                                                                                         0.1,
                                                                                                                                                         1), scale=0.125, pos=(0, 0, -0.125))
        self.levelUpIval = Sequence(Func(self.levelUpSfx.play), Func(self.levelUpText.reparentTo, aspect2d), Parallel(LerpPosInterval(self.levelUpText, 5, pos=Point3(0, 0, 0.3), startPos=Point3(0, 0, -0.3)), Sequence(LerpColorScaleInterval(self.levelUpText, 0.5, colorScale=VBase4(1, 1, 1, 1), startColorScale=VBase4(1, 1, 1, 0)), Wait(4), LerpColorScaleInterval(self.levelUpText, 0.5, colorScale=VBase4(1, 1, 1, 0), startColorScale=VBase4(1, 1, 1, 1)))), Func(self.levelUpText.detachNode))
        return

    def bufferLevelUpText(self, category, level):
        catLevel = self.levelUpBufferDict.get(category)
        if level > catLevel:
            self.levelUpBufferDict[category] = level
        taskMgr.doMethodLater(0.1, self.processLevelUpBuffer, 'processLevelUpBuffer')

    def processLevelUpBuffer(self, task=None):
        for categoryKey in self.levelUpBufferDict:
            level = self.levelUpBufferDict[categoryKey]
            self.showLevelUpText(categoryKey, level)

        self.levelUpBufferDict = {}
        if task:
            return task.done

    def showLevelUpText(self, category, level):
        if self.pageOpen(self.skillPage):
            self.togglePage(self.skillPage)
        self.skillPage.update(category)
        self.createLevelUpText()
        self.levelUpLabel['text'] = PLocalizer.LevelUp
        categoryName = PLocalizer.InventoryTypeNames[category]
        if category == InventoryType.OverallRep:
            self.levelUpCategoryLabel['text_fg'] = (1.0, 1.0, 0.2, 1)
            self.levelUpLabel['text_fg'] = (1.0, 1.0, 0.1, 1)
        else:
            if category == InventoryType.PVPTotalInfamyLand or category == InventoryType.PVPTotalInfamySea:
                self.levelUpCategoryLabel['text_fg'] = (1.0, 0.2, 0.2, 1)
                self.levelUpLabel['text_fg'] = (1.0, 0.1, 0.1, 1)
            else:
                if category == InventoryType.DefenseCannonRep:
                    tpMgr = TextPropertiesManager.getGlobalPtr()
                    self.levelUpCategoryLabel['text_fg'] = tpMgr.getProperties('CPLtBlueOVER').getTextColor()
                    self.levelUpLabel['text_fg'] = tpMgr.getProperties('CPLtBlueOVER').getTextColor()
                    del tpMgr
                else:
                    self.levelUpCategoryLabel['text_fg'] = (0.1, 0.7, 0.2, 1)
                    self.levelUpLabel['text_fg'] = (0.1, 0.7, 0.1, 1)
                self.levelUpCategoryLabel['text'] = '%s Level %s' % (categoryName, level)
                self.levelUpIval.pause()
                self.levelUpIval.start()
                msg = PLocalizer.ChatPanelLevelUpMsg % (categoryName, level)
                base.talkAssistant.receiveGameMessage(msg)
                levelUpReward = ''
                stats = RepChart.getLevelUpStats(category)
                if stats[0] > 0:
                    levelUpReward += PLocalizer.LevelUpHPIncrease % stats[0]
                if stats[1] > 0:
                    levelUpReward += PLocalizer.LevelUpVoodooIncrease % stats[1]
                skills = RepChart.getLevelUpSkills(category, level)
                for skillId in skills[0]:
                    pointName = PLocalizer.getInventoryTypeName(skillId)
                    levelUpReward += PLocalizer.LevelUpSkillPoint % pointName

                for skillId in skills[1]:
                    skillName = PLocalizer.getInventoryTypeName(skillId)
                    levelUpReward += PLocalizer.LevelUpSkillUnlock % skillName

                if levelUpReward:
                    levelUpReward = PLocalizer.ChatPanelLevelUpMsg % (categoryName, level) + '\n' + levelUpReward
                    self.messageStack.addTextMessage(levelUpReward, icon=('reputation', category))
            if self.skillPage.tabBar:
                self.skillPage.tabBar.stash()

    def showQuestItemNotifyText(self, quest, item, note):
        if self.getTutorialStatus() < PiratesGlobals.TUT_GOT_SEACHEST:
            return
        msg = PLocalizer.QuestItemNotifications[note]
        msg, color = quest.getProgressMsg()
        if msg:
            self.createProgressMsg(msg, color)

    def showQuestAddedText(self, quest):
        self.av.queueStoryQuest(quest)
        if self.getTutorialStatus() < PiratesGlobals.TUT_GOT_SEACHEST:
            return
        inv = self.av.getInventory()
        UserFunnel.logSubmit(0, 'quest_assigned_%s' % quest.questId)
        UserFunnel.logSubmit(1, 'quest_assigned_%s' % quest.questId)

    def showQuestNotifyText(self, message, quest):
        if self.getTutorialStatus() < PiratesGlobals.TUT_GOT_SEACHEST:
            return
        msg, color = quest.getProgressMsg()
        if msg:
            self.createProgressMsg(msg, color)

    def showQuestCompleteText(self, message, quest):
        if self.getTutorialStatus() < PiratesGlobals.TUT_GOT_SEACHEST:
            return
        duration = 5.0
        if isinstance(quest.getTasks()[0], MaroonNPCTaskDNA):
            duration = 12.0
        msg, color = quest.getProgressMsg()
        if msg:
            self.createProgressMsg(msg, color, duration)

    def handleTopTen(self, stuff):
        self.topTen = DirectFrame(parent=aspect2d, relief=DGG.FLAT, frameSize=(-0.8, 0.8, -0.7, 0.6), frameColor=PiratesGuiGlobals.FrameColor, pos=(0,
                                                                                                                                                    0,
                                                                                                                                                    0), text='Reputation Top Ten', text_align=TextNode.ACenter, text_scale=0.04, text_fg=(0.9,
                                                                                                                                                                                                                                          1,
                                                                                                                                                                                                                                          0.9,
                                                                                                                                                                                                                                          1), text_pos=(0,
                                                                                                                                                                                                                                                        0.5,
                                                                                                                                                                                                                                                        0))
        count = len(stuff)
        for person in stuff:
            slot = DirectFrame(parent=self.topTen, relief=DGG.FLAT, frameSize=(-0.5, 0.5, -0.035, 0.045), frameColor=(1,
                                                                                                                      1,
                                                                                                                      1,
                                                                                                                      1), pos=(0, 0, 0.5 + -0.1 * count), text='%10d    %s' % (person[2], person[1]), text_scale=0.04)
            count -= 1

        taskMgr.doMethodLater(15.0, self.dismissTopTen, 'clearTopTen')

    def dismissTopTen(self, task):
        self.topTen.hide()
        self.topTen.destroy()

    def handleClickedNametag(self, avatar):
        if avatar.isGhost >= 3:
            return
        if avatar.isConfused:
            self.handleContextTutorial(InventoryType.ChatPreferences, 0, 0, avatar.wlEnabled)
        else:
            return self.handleAvatarDetails(avatar.getDoId())

    def handleIgnoreGuildInvites(self):
        self.ignoreGuildInvites = 1

    def ignoreInvitesPlayer(self, pId):
        if pId not in self.ignoreInvitesPlayerList:
            self.ignoreInvitesPlayerList.append(pId)

    def ignoreInvitesAvatar(self, avId):
        if avId not in self.ignoreInvitesAvatarList:
            self.ignoreInvitesAvatarList.append(avId)

    def handleAvatarDetails(self, avId, avName=None):
        messenger.send('avatarDetailsOpened')
        self.profilePage.showProfile(avId, avName)
        if hasattr(base, 'localAvatar'):
            base.localAvatar.removeContext(InventoryType.PlayerProfiles)
            base.localAvatar.removeContext(InventoryType.PlayerInvites)
            base.localAvatar.removeContext(InventoryType.DockCrewCommands)
            base.localAvatar.removeContext(InventoryType.TeleportToFriends)

    def hideAvatarDetails(self):
        self.profilePage.hide()

    def handlePlayerDetails(self, playerId, playerName=None):
        self.profilePage.showPlayerProfile(playerId, playerName)

    def hidePlayerDetails(self):
        self.profilePage.hide()

    def handleGotoAvatar(self, avId, avName=None):
        if not launcher.canLeaveFirstIsland():
            base.cr.centralLogger.writeClientEvent('Player encountered phase 4 blocker trying to teleport to another pirate')
            self.showDownloadBlocker(DownloadBlockerPanel.Reasons.TELEPORT)
            return
        base.cr.teleportMgr.queryAvatarForTeleport(avId)

    def handleRelationships(self, avId, avName, playerId=None):
        if self.relationshipChooser:
            self.relationshipChooser.destroy()
        self.relationshipChooser = RelationshipChooser.RelationshipChooser(avId, avName, playerId)
        self.relationshipChooser.setPos(-0.75, 0, -0.295)

    def handleAvatarFriendInvite(self, avId, avName):
        if self.friendInviter:
            self.friendInviter.destroy()
        av = base.cr.doId2do.get(avId)
        if av:
            avName = av.getName()
        self.friendInviter = FriendInviter.FriendInviter(avId, avName, False, False)

    def handlePlayerFriendInvite(self, avId, avName, pId=None):
        pInfo = base.cr.playerFriendsManager.findPlayerInfoFromAvId(avId)
        if pInfo:
            avName = pInfo.playerName
        if self.friendInviter:
            self.friendInviter.destroy()
        self.friendInviter = FriendInviter.FriendInviter(avId, avName, True, False, pId)

    def handleAvatarFriendInvitation(self, avId, avName='Unknown'):
        if self.friendInvitee:
            self.friendInvitee.destroy()
        self.friendInvitee = FriendInvitee.FriendInvitee(avId, avName, False)

    def handlePlayerFriendInvitation(self, avId, avName='Unknown'):
        if self.friendInvitee:
            self.friendInvitee.destroy()
        self.friendInvitee = FriendInvitee.FriendInvitee(avId, avName, True)

    def handleGuildInviteAccept(self, avid):
        if not self.guildInviter:
            return
        self.guildInviter.guildAcceptInvite(avid)

    def handleGuildInviteReject(self, avid, reason):
        if not self.guildInviter:
            return
        self.guildInviter.guildRejectInvite(avid, reason)

    def handleGuildInvite(self, avId, avName):
        if self.guildInviter:
            self.guildInviter.destroy()
        self.guildInviter = GuildInviter.GuildInviter(avId, avName)

    def handleGuildMember(self, avId, avName, guildId, canpromote, candemote, cankick):
        if self.guildMember:
            self.guildMember.destroy()
        self.guildMember = GuildMember.GuildMember(avId, avName, guildId, canpromote, candemote, cankick)

    def handleGuildInvitation(self, avId, avName, guildId, guildName):
        if self.guildInvitee:
            self.guildInvitee.destroy()
        self.guildInvitee = GuildInvitee.GuildInvitee(avId, avName, guildId, guildName)

    def handleCrewInvite(self, avId, avName):
        if self.crewInviter:
            self.crewInviter.destroy()
        self.crewInviter = CrewInviter.CrewInviter()
        self.crewInviter.inviteAvatar(avId, avName)

    def handleCrewLeave(self):
        if self.crewInviter:
            self.crewInviter.destroy()
        self.crewInviter = CrewInviter.CrewInviter(self.av.doId, self.av.getName())

    def handleCrewInvitation(self, avId, avName='Unknown'):
        if self.crewInvitee:
            self.crewInvitee.destroy()
        self.crewInvitee = CrewInvitee.CrewInvitee(avId, avName)

    def handleCrewRejoin(self, avId, isManager=0, isPvp=0):
        if self.crewRejoin:
            self.crewRejoin.destroy()
        self.crewRejoin = CrewRejoin.CrewRejoin(avId, isManager, isPvp)

    def handleCrewBoot(self, avId, avName='Unknown'):
        if self.crewBoot:
            self.crewBoot.destroy()
        self.crewBoot = CrewBoot.CrewBoot(avId, avName)

    def handleLeaveCrewWarning(self, shardId):
        if self.leaveCrewWarning:
            self.leaveCrewWarning.destroy()
        self.leaveCrewWarning = LeaveCrewWarning.LeaveCrewWarning(shardId)

    def handleTradeInvite(self, avId, avName):
        if self.tradeInviter:
            self.tradeInviter.destroy()
        self.tradeInviter = TradeInviter.TradeInviter(avId, avName)

    def handleTradeInvitation(self, trade):
        if self.tradePanel:
            self.tradePanel.destroy()
        self.tradePanel = TradePanel.TradePanel(trade)
        self.tradePanel.setPos(base.a2dLeft, 0, -0.15)

    def handlePVPInvite(self, avId, avName):
        if self.pvpInviter:
            self.pvpInviter.destroy()
        self.pvpInviter = PVPInviter.PVPInviter(avId, avName)

    def handlePVPInvitation(self, avId, avName='Unknown'):
        if self.pvpInvitee:
            self.pvpInvitee.destroy()
        self.pvpInvitee = PVPInvitee.PVPInvitee(avId, avName)

    def handlePVPAccepted(self, avId, avName='Unknown'):
        if self.pvpInvitee:
            self.pvpInvitee.destroy()
            self.pvpInvitee = None
        elif self.pvpInviter:
            self.pvpInviter.destroy()
            self.pvpInviter = None
        return

    def handleIgnore(self, avId, avName):
        if self.ignoreConfirm:
            self.ignoreConfirm.destroy()
        self.ignoreConfirm = IgnoreConfirm.IgnoreConfirm(avId, avName)

    def handleReport(self, playerId, avId, avName):
        if self.reportAPlayer:
            self.reportAPlayer.destroy()
        self.reportAPlayer = ReportAPlayer.ReportAPlayer(playerId, avId, avName)

    def handleWhisperIncoming(self, senderId, msgText):
        if base.cr.avatarFriendsManager.checkIgnored(senderId):
            return
        sender = base.cr.identifyAvatar(senderId)
        if sender:
            senderName = sender.getName()
        else:
            self.notify.warning('handleWhisperIncoming: senderId: %s not found' % senderId)
            senderName = 'Unknown'
        whisperType = WhisperPopup.WTNormal
        base.talkAssistant.receiveAvatarWhisperTypedChat(msgText, senderId)
        if self.soundWhisper:
            base.playSfx(self.soundWhisper)

    def handleContextTutorial(self, contextId, number, type, part):
        if self.isTutEnabled == False:
            return
        result = self.contextTutPanel.setPanel(contextId, number, type, part)
        if result and self.seaChestAllowed:
            self.contextTutPanel.show()

    def showTMUI(self, tm):
        if self.tmObjectiveList == None:
            self.createObjectiveList(tm)
        self.tmObjectiveList.show()
        if self.crewPage:
            self.crewPage.determineOptionsButtonsState()
        return

    def hideTMUI(self):
        if self.tmObjectiveList:
            self.tmObjectiveList.cleanup()
            self.tmObjectiveList.hide()
            del self.tmObjectiveList
            self.tmObjectiveList = None
        if self.crewPage:
            self.crewPage.determineOptionsButtonsState()
        return

    def createObjectiveList(self, tm):
        self.tmObjectiveList = ObjectivesPanel('Treasure Map Objectives', tm)
        self.tmObjectiveList.setPos(base.a2dLeft, 0, 0.45)

    def showTMCompleteUI(self, tm, results):
        return
        if self.tmCompleteUI == None:
            self.createTMCompleteUI(tm, results)
        self.tmCompleteUI.setAlphaScale(0)
        self.tmCompleteUI.show()
        if self.showTMCompleteLerp:
            self.showTMCompleteLerp.pause()
        self.showTMCompleteLerp = LerpColorScaleInterval(self.tmCompleteUI, 1, Vec4(1, 1, 1, 1))
        self.showTMCompleteLerp.start()
        return

    def hideTMCompleteUI(self):
        if self.showTMCompleteLerp:
            self.showTMCompleteLerp.pause()
            self.showTMCompleteLerp = None
        if self.tmCompleteUI:
            self.tmCompleteUI.hide()
        return

    def createTMCompleteUI(self, tm, results):
        self.tmCompleteUI = TreasureMapCompletePanel('Treasure Map Complete', tm, results)
        self.tmCompleteUI.setPos(-1.25, 0, -0.82)

    def showPVPInstructions(self, title, instructions):
        if not self.gameRulesPanel:
            self.gameRulesPanel = PVPRulesPanel('PVPRulesPanel', title, instructions)

    def hidePVPInstructions(self):
        if self.gameRulesPanel:
            self.gameRulesPanel.destroy()
            self.gameRulesPanel = None
        return

    def createPVPStatus(self, holder):
        if self.pvpStatus is None:
            self.pvpStatus = PVPBoard(holder)
            self.pvpStatus.hide()
        return

    def showPVPStatus(self):
        if self.pvpStatus != None:
            self.pvpStatus.show()
        return

    def hidePVPStatus(self):
        if self.pvpStatus:
            self.pvpStatus.hide()

    def removePVPStatus(self):
        if self.pvpStatus:
            self.pvpStatus.destroy()
            self.pvpStatus = None
        return

    def removeScoreboard(self):
        if self.scoreboard:
            self.scoreboard.hide()
            self.scoreboard.destroy()
            self.scoreboard = None
        return

    def removeInvasionScoreboard(self):
        if self.invasionScoreboard:
            self.invasionScoreboard.hide()
            self.invasionScoreboard.destroy()
            self.invasionScoreboard = None
        return

    def createSiegeStatus(self, holder):
        if self.siegeStatus is None:
            self.siegeStatus = SiegeBoard(holder)
        return

    def showSiegeStatus(self):
        if self.siegeStatus != None:
            self.siegeStatus.show()
        return

    def hideSiegeStatus(self):
        if self.siegeStatus:
            self.siegeStatus.hide()

    def removeSiegeStatus(self):
        if self.siegeStatus:
            self.siegeStatus.destroy()
            self.siegeStatus = None
        return

    def showPVPTimer(self, pvpInstance):
        if pvpInstance.hasTimeLimit():
            timeRemaining = pvpInstance.getTimeLimit() - (globalClock.getRealTime() - pvpInstance.gameStartTime)
            self.setTimer(timeRemaining, alarmTime=10)
            self._oldTimerPos = self.timer.getPos()
            self.timer.setPos(0.435, 0, 1.4)

    def createPVPUI(self, holder):
        if self.pvpPanel is None:
            self.pvpPanel = PVPPanel.PVPPanel(PLocalizer.PVPPanelTitle, holder)
            self.pvpPanel.reparentTo(base.a2dLeftCenter)
            self.pvpPanel.setPos(0.05, 0, 0.25)
            self.pvpPanel.hide()
        return

    def showPVPUI(self, team):
        if self.pvpPanel != None:
            self.pvpPanel.show(team)
        return

    def hidePVPUI(self):
        if self.pvpPanel != None:
            self.pvpPanel.hide()
        return

    def removePVPUI(self):
        if self.pvpPanel:
            if self.timer:
                self.timer.setPos(self._oldTimerPos)
            self.timerExpired()
            self.pvpPanel.cleanup()
            self.pvpPanel.destroy()
            self.pvpPanel = None
        return

    def createPVPCompleteUI(self, pvpInstance):
        if self.pvpCompleteUI is None:
            self.pvpCompleteUI = PVPCompletePanel(PLocalizer.PVPCompleteTitle, pvpInstance)
            self.pvpCompleteUI.setPos(-1.25, 0, -0.82)
        return

    def showPVPCompleteUI(self):
        self.pvpCompleteUI.setAlphaScale(0)
        self.pvpCompleteUI.show()
        if self.showPVPCompleteLerp:
            self.showPVPCompleteLerp.pause()
        self.showPVPCompleteLerp = LerpColorScaleInterval(self.pvpCompleteUI, 1, Vec4(1, 1, 1, 1))
        self.showPVPCompleteLerp.start()

    def setPVPResult(self, type, rank, teams, tie):
        if teams == 2:
            if tie:
                self.pvpCompleteUI.setOutcome(PLocalizer.PVPTied)
            elif type == 'player':
                if rank == 1:
                    self.pvpCompleteUI.setOutcome(PLocalizer.PVPPlayerWon)
                else:
                    self.pvpCompleteUI.setOutcome(PLocalizer.PVPPlayerLost)
            elif type == 'team':
                if rank == 1:
                    self.pvpCompleteUI.setOutcome(PLocalizer.PVPTeamWon % localAvatar.getPVPTeam())
                else:
                    self.pvpCompleteUI.setOutcome(PLocalizer.PVPTeamWon % (3 - localAvatar.getPVPTeam()))
        elif type == 'player':
            self.pvpCompleteUI.setOutcome('%s%s' % (PLocalizer.PVPYourRank, rank))
        elif type == 'team':
            self.pvpCompleteUI.setOutcome('%s%s' % (PLocalizer.PVPYourTeamRank, rank))

    def hidePVPCompleteUI(self):
        if self.showPVPCompleteLerp:
            self.showPVPCompleteLerp.pause()
            self.showPVPCompleteLerp = None
        if self.pvpCompleteUI:
            self.pvpCompleteUI.hide()
        return

    def removePVPCompleteUI(self):
        if self.pvpCompleteUI:
            self.pvpCompleteUI.hide()
            self.pvpCompleteUI.destroy()
            self.pvpCompleteUI = None
        return

    def hideTrays(self):
        self.removeInvasionScoreboard()
        self.combatTray.hide()
        self.gameGui.hide()
        self.chestTray.hide()
        if self.filmOffsetLerp:
            self.filmOffsetLerp.pause()
            self.filmOffsetLerp = None
        self.setFilmOffsetX(0.0)
        self.setFilmOffsetY(0.0)
        if self.mainMenu:
            self.mainMenu.abruptHide()
        self.setSeaChestAllowed(False, close=True)
        self.radarGui.hide()
        self.targetStatusTray.hide()
        if not self.socialPanel.isHidden():
            self.socialPanel.hide()
            self._putBackSocialPanel = 1
        self.socialPanel.hide()
        self.chatPanel.hide()
        self.av.chatMgr.stop()
        self.av.stopChat()
        self.setChatAllowed(False, close=True)
        self.moneyDisplay.hide()
        self.contextTutPanel.hide()
        if self.av.getCrewShip():
            self.av.getCrewShip().hideStatusDisplay()
            self.av.getCrewShip().hideTargets()
        if self.prevTag:
            self.prevTag.hide()
        if self.tmButtonQuick:
            self.tmButtonQuick.hide()
        if self.tmButtonSearch:
            self.tmButtonSearch.hide()
        self.hideTrackedQuestInfo()
        if self.crewHUD.hudOn:
            self.crewHUD.setHUDOff()
            self.crewHUDTurnedOff = True
        self.hideMinimap()
        self.profilePage.hide()
        return

    def showTrays(self):
        if self.filmOffsetLerp:
            self.filmOffsetLerp.pause()
            self.filmOffsetLerp = None
        self.setFilmOffsetX(0.0)
        self.setFilmOffsetY(0.0)
        self.setIgnoreMainMenuHotKey(False)
        self.setIgnoreAllButSkillHotKey(False)
        self.setIgnoreAllButLookoutHotKey(False)
        if self.mainMenu:
            self.mainMenu.abruptHide()
        if self.getTutorialStatus() >= PiratesGlobals.TUT_GOT_SEACHEST:
            self.chestTray.show()
            self.setSeaChestAllowed(True)
            self.combatTray.show()
            self.gameGui.show()
            self.chatPanel.show()
            self.av.chatMgr.start()
            self.av.startChat()
            if self.contextTutPanel.isFilled() and self.isTutEnabled:
                self.contextTutPanel.show()
            self.setChatAllowed(True)
            if self._putBackSocialPanel:
                if hasattr(base, 'localAvatar') and not base.localAvatar.inPvp:
                    self.socialPanel.show()
                self._putBackSocialPanel = 0
            if self.av.getCrewShip() and self.av.getCrewShip() == self.av.getShip():
                self.av.getCrewShip().showStatusDisplay()
                self.av.getCrewShip().showTargets()
            if self.prevTag and not Freebooter.AllAccessHoliday:
                self.prevTag.show()
        if self.getTutorialStatus() >= PiratesGlobals.TUT_GOT_COMPASS:
            self.radarGui.show()
            if self.tmButtonQuick and base.cr.teleportMgr and base.cr.teleportMgr.inInstanceType != PiratesGlobals.INSTANCE_TM:
                self.tmButtonQuick.show()
            if self.tmButtonSearch and base.cr.teleportMgr and base.cr.teleportMgr.inInstanceType != PiratesGlobals.INSTANCE_TM:
                self.tmButtonSearch.show()
            if len(self.trackedQuestLabel['text'] and self.av.activeQuestId):
                self.showTrackedQuestInfo()
        if self.crewHUDTurnedOff and (self.getTutorialStatus() >= PiratesGlobals.TUT_MET_JOLLY_ROGER or self.forceLookout or self.crewHUD.crew):
            self.crewHUD.setHUDOn()
            self.crewHUDTurnedOff = False
        return

    def getTray(self, gearId):
        categoryType = InventoryId.getCategory(gearId)
        gearRepId = WeaponGlobals.getRepId(gearId)
        if categoryType == ReputationGlobals.WEAPON_CATEGORY:
            if gearRepId == InventoryType.CannonRep:
                pass
        return None

    def setTimer(self, time, showMinutes=1, mode=None, titleText='', titleFg=None, infoText='', cancelText='', cancelCallback=None, timerExpiredCallback=None, alarmTime=5):
        self.timerExpired()
        self.timer = PiratesTimer.PiratesTimer(showMinutes=showMinutes, mode=mode, titleText=titleText, titleFg=titleFg, infoText=infoText, cancelText=cancelText, cancelCallback=cancelCallback, alarmTime=alarmTime)
        self.timer.reparentTo(base.a2dBottomLeft)
        self.timer.setPos(0.32, 0, 1.2)
        self.timer.show()
        if timerExpiredCallback:
            self.timer.countdown(time, timerExpiredCallback)
        else:
            self.timer.countdown(time, self.timerExpired)

    def timerExpired(self):
        if self.timer:
            self.timer.destroy()
            self.timer = None
        return

    def cancelTimer(self, mode):
        if self.timer and self.timer.mode == mode:
            self.timerExpired()

    def setHourglassTimer(self, time, showMinutes=1, mode=None, titleText='', titleFg=None, infoText='', cancelText='', cancelCallback=None, timerExpiredCallback=None):
        self.hourglassTimerExpired()
        timer = PiratesTimerHourglass.PiratesTimerHourglass(showMinutes=showMinutes, mode=mode, titleText=titleText, titleFg=titleFg, infoText=infoText, cancelText=cancelText, cancelCallback=cancelCallback)
        self.timerHourglass = timer
        timer.reparentTo(base.a2dBottomLeft)
        timer.setPos(0.13, 0, 1.2)
        timer.setScale(0.2)
        timer.show()
        if timerExpiredCallback:
            timer.countdown(time, timerExpiredCallback)
        else:
            timer.countdown(time, self.hourglassTimerExpired)

    def hourglassTimerExpired(self):
        if self.timerHourglass:
            self.timerHourglass.destroy()
            self.timerHourglass = None
        return

    def cancelHourglassTimer(self, mode):
        if self.timerHourglass and self.timerHourglass.mode == mode:
            self.hourglassTimerExpired()

    def createSubtitle(self, text, color=None):
        self.subtitler.showText(text, color)
        taskMgr.remove('clearSubtitle')

        def clearSubtitle(event):
            self.subtitler.clearText()

        taskMgr.doMethodLater(2.0, clearSubtitle, 'clearSubtitle')

    def createTitle(self, text, color=None):
        self.titler.fadeInText(text, color)
        taskMgr.remove('clearTitle')
        self.titler.text['text_scale'] = PiratesGuiGlobals.TextScaleTitleJumbo
        self.titler.text['text_font'] = PiratesGlobals.getPirateOutlineFont()
        self.titler.text['text_shadow'] = PiratesGuiGlobals.TextShadow
        position = Vec3(0.0, 0.0, 0.0)
        self.titler.text.setPos(position)

        def clearTitle(event):
            self.titler.fadeOutText()

        taskMgr.doMethodLater(3.0, clearTitle, 'clearTitle')

    def createSecondaryTitle(self, text, color=None):
        self.secondarytitler.fadeInText(text, color)
        taskMgr.remove('clearSecondaryTitle')
        self.secondarytitler.text['text_scale'] = PiratesGuiGlobals.TextScaleTitleMed
        self.secondarytitler.text['text_font'] = PiratesGlobals.getPirateOutlineFont()
        self.secondarytitler.text['text_shadow'] = PiratesGuiGlobals.TextShadow
        position = Vec3(0.0, 0.0, -0.1)
        self.secondarytitler.text.setPos(position)

        def clearSecondaryTitle(event):
            self.secondarytitler.fadeOutText()

        taskMgr.doMethodLater(3.0, clearSecondaryTitle, 'clearSecondaryTitle')

    def createWarning(self, text, color=PiratesGuiGlobals.TextFG6, duration=2.0):
        self.warningMsg.showText(text, color)
        taskMgr.remove('clearWarning')

        def clearWarningMsg(event):
            self.warningMsg.clearText()

        taskMgr.doMethodLater(duration, clearWarningMsg, 'clearWarning')

    def createProgressMsg(self, text, color=None, duration=5.0):
        self.progressMsg.text.setPos(0, 0, PiratesGuiGlobals.ProgressMsgOffset)
        self.progressMsg.showText(text, color)
        taskMgr.remove('clearProgress')

        def clearProgressMsg(event):
            self.progressMsg.clearText()

        taskMgr.doMethodLater(duration, clearProgressMsg, 'clearProgress')

    def createInteractionalSubtitle(self, text, avatar, audio=None, color=None):
        if self.interactionalFrame == None:
            self.interactionalFrame = DirectFrame(parent=aspect2d, relief=DGG.FLAT, state=DGG.DISABLED, frameSize=(-0.8, 0.8, -0.1, 0.1), frameColor=(0,
                                                                                                                                                      0,
                                                                                                                                                      0,
                                                                                                                                                      0), pos=(0.125,
                                                                                                                                                               0,
                                                                                                                                                               0.79))
        else:
            self.interactionalFrame.show()
        if self.bg == None:
            self.bg = loader.loadModel('models/misc/square_drop_shadow')
            self.bg.reparentTo(self.interactionalFrame)
            self.bg.setTransparency(1)
            self.bg.setColorScale(1, 1, 1, 0.85)
            self.bg.setScale(0.32, 0.032, 0.2)
            self.bg.setHpr(0, 90, 0)
            self.interactionalSubtitler.text.reparentTo(self.interactionalFrame)
            self.interactionalSubtitler.text.setScale(1)
            self.interactionalSubtitler.text['text_wordwrap'] = 28
        self.interactionalSubtitler.showText(text, color)
        textBounds = self.interactionalSubtitler.text.component('text0').textNode.getFrameActual()
        self.interactionalSubtitler.text.setPos(0, 0, -(textBounds[3] + textBounds[2]) / 2 * self.interactionalSubtitler.text['text_scale'][1])
        avatar.playCurrentDialogue(audio, 0)
        return

    def clearInteractionalSubtitle(self):
        self.interactionalSubtitler.showText('')
        if self.interactionalFrame:
            self.interactionalFrame.hide()

    def createNewQuestIndicator(self, quest):
        if self.getTutorialStatus() < PiratesGlobals.TUT_GOT_SEACHEST:
            return
        if self.journalButton:
            self.journalButton.addNewQuest()
            self.journalButton['extraArgs'] = [quest]
            return
        self.journalButton = JournalButton.JournalButton(parent=base.a2dBottomRight, command=self.viewJournal, pos=(-0.12, 0, 0.27), scale=0.9, extraArgs=[quest])
        self.journalButton.addNewQuest()

    def viewJournal(self, quest):
        self.showQuestPanel()
        self.questPage.titleList.select(quest.getQuestId())

    def removeNewQuestIndicator(self):
        if self.journalButton:
            self.journalButton.removeNewQuest()
            if self.journalButton.questCounter <= 0:
                self.journalButton.destroy()
                self.journalButton = None
        return

    def createHighSeasScoreboard(self, portName, missionData, playerData, ship):
        if self.scoreboard:
            self.removeScoreboard()
        self.scoreboard = HighSeasScoreboard.HighSeasScoreboard(portName, missionData, playerData, ship)
        self.scoreboard.setPos(-self.scoreboard.width / 2.0, 0, -0.95)

    def createInvasionScoreboard(self, holidayId, wonInvasion, repEarned, enemiesKilled, barricadesSaved, wavesCleared):
        if self.invasionScoreboard:
            self.removeInvasionScoreboard()
        self.invasionScoreboard = InvasionScoreboard.InvasionScoreboard(holidayId, wonInvasion, repEarned, enemiesKilled, barricadesSaved, wavesCleared)
        self.invasionScoreboard.setPos(-self.invasionScoreboard.width / 2.0 - 0.2, 0, self.invasionScoreboard.height / 2.0 + 0.1)

    def loadOffscreenHitEffects(self):
        if self.offscreenHitEffects:
            return
        onColor = Vec4(1, 0, 0, 0.7)
        offColor = Vec4(1, 0, 0, 0)
        left = loader.loadModel('models/textureCards/offscreenFlash')
        left.setColor(onColor)
        left.setScale(4, 0, 9)
        left.setPosHpr(0.2, 0, 0, 0, 0, 0)
        left.hide()
        left.flattenStrong()
        left.setName('leftHitFlash')
        left.reparentTo(base.a2dLeftCenter, -1)
        right = loader.loadModel('models/textureCards/offscreenFlash')
        right.setColor(onColor)
        right.setScale(4, 0, 9)
        right.setPosHpr(-0.2, 0, 0, 0, 0, 180)
        right.hide()
        right.flattenStrong()
        right.setName('rightHitFlash')
        right.reparentTo(base.a2dRightCenter, -1)
        bottom = loader.loadModel('models/textureCards/offscreenFlash')
        bottom.setColor(onColor)
        bottom.setScale(4, 0, 10)
        bottom.setPosHpr(0, 0, 0.25, 0, 0, -90)
        bottom.hide()
        bottom.flattenStrong()
        bottom.setName('bottomHitFlash')
        bottom.reparentTo(base.a2dBottomCenter, -1)
        top = loader.loadModel('models/textureCards/offscreenFlash')
        top.setColor(onColor)
        top.setScale(4, 0, 10)
        top.setPosHpr(0, 0, -0.25, 0, 0, 90)
        top.hide()
        top.flattenStrong()
        top.setName('topHitFlash')
        top.reparentTo(base.a2dTopCenter, -1)
        self.offscreenHitEffects = [
         left, bottom, right, top]
        flashLeft = Sequence(Func(left.show), LerpColorInterval(left, 0.2, onColor, offColor), LerpColorInterval(left, 0.4, offColor, onColor), Func(left.hide))
        flashRight = Sequence(Func(right.show), LerpColorInterval(right, 0.2, onColor, offColor), LerpColorInterval(right, 0.4, offColor, onColor), Func(right.hide))
        flashBottom = Sequence(Func(bottom.show), LerpColorInterval(bottom, 0.2, onColor, offColor), LerpColorInterval(bottom, 0.4, offColor, onColor), Func(bottom.hide))
        flashTop = Sequence(Func(top.show), LerpColorInterval(top, 0.2, onColor, offColor), LerpColorInterval(top, 0.4, offColor, onColor), Func(top.hide))
        self.offscreenHitIvals = [
         flashLeft, flashBottom, flashRight, flashTop]

    def setupInjuredEffect(self):
        if self.injuredEffects:
            return
        onColor = Vec4(0, 0, 0, 0.7)
        offColor = Vec4(0, 0, 0, 0)
        left = loader.loadModel('models/textureCards/offscreenFlash')
        left.setColor(onColor)
        left.setScale(4, 0, 9)
        left.setPosHpr(0.25, 0, 0, 0, 0, 0)
        left.hide()
        left.setName('leftDaze')
        left.reparentTo(base.a2dLeftCenter, -1)
        right = loader.loadModel('models/textureCards/offscreenFlash')
        right.setColor(onColor)
        right.setScale(4, 0, 9)
        right.setPosHpr(-0.25, 0, 0, 0, 0, 180)
        right.hide()
        right.setName('rightDaze')
        right.reparentTo(base.a2dRightCenter, -1)
        bottom = loader.loadModel('models/textureCards/offscreenFlash')
        bottom.setColor(onColor)
        bottom.setScale(4, 0, 12)
        bottom.setPosHpr(0, 0, 0.25, 0, 0, -90)
        bottom.hide()
        bottom.setName('bottomDaze')
        bottom.reparentTo(base.a2dBottomCenter, -1)
        top = loader.loadModel('models/textureCards/offscreenFlash')
        top.setColor(onColor)
        top.setScale(4, 0, 12)
        top.setPosHpr(0, 0, -0.25, 0, 0, 90)
        top.hide()
        top.setName('topDaze')
        top.reparentTo(base.a2dTopCenter, -1)
        self.injuredEffects = [
         left, bottom, right, top]
        screenSizeX = base.a2dLeft - base.a2dRight
        screenSizeZ = base.a2dBottom - base.a2dTop
        self.injuredBlackoutGeom = BuildGeometry.addCircleGeom(base.aspect2d, 8, 0.75, color=Vec4(1.0, 1.0, 1.0, 1.0), centerColor=Vec4(1.0, 1.0, 1.0, 0.5))[0]
        self.injuredBlackoutGeom.setHpr(0, 90, 0)
        self.injuredBlackoutGeom.hide()
        self.injuredBlackoutGeom.setTransparency(TransparencyAttrib.MAlpha)
        self.injuredBlackoutGeom.setScale(screenSizeX, screenSizeZ, 1.0)

    def regenInjuredTrack(self, timeStart):
        blackoutTime = PiratesGlobals.REVIVE_TIME_OUT
        blackoutPropStart = timeStart / blackoutTime
        timeCycle = 2.0 - 1.5 * blackoutPropStart
        self.injuredHeartbeat.setPlayRate(0.75 + 1.0 * blackoutPropStart)
        self.injuredHeartbeat.setVolume(0.5 + 0.5 * blackoutPropStart)
        blackoutPropEnd = (timeStart + timeCycle) / blackoutTime
        barWidth = 4.0 + float(blackoutPropEnd) * 4.0
        hScale = Vec3(4, 0, 12)
        vScale = Vec3(4, 0, 9)
        newHScale = Vec3(barWidth, 0, 12)
        newVScale = Vec3(barWidth, 0, 9)
        blackColor = 0.5 * blackoutPropEnd
        darkColor = 0.5 + blackColor
        if darkColor > 1.0:
            darkColor = 1.0
        alteredProp = blackoutPropEnd - 0.0
        if alteredProp < 0.0:
            alteredProp = 0.0
        darkMildColor = (darkColor + blackColor) * 0.5
        blackMildColor = darkMildColor * alteredProp + blackColor * (1 - alteredProp)
        onColor = Vec4(0, 0, 0, darkColor)
        offColor = Vec4(0, 0, 0, 0.0 + blackColor)
        darkOutColor = Vec4(darkMildColor * 0.0, 0, 0, darkMildColor)
        blackOutColor = Vec4(blackMildColor * 0.0, 0, 0, blackMildColor)
        import random
        halfCycle = timeCycle * 0.5
        quarterCycle = timeCycle * 0.25
        time1 = halfCycle * random.random() + quarterCycle
        time1I = timeCycle - time1
        time2 = halfCycle * random.random() + quarterCycle
        time2I = timeCycle - time2
        time3 = halfCycle * random.random() + quarterCycle
        time3I = timeCycle - time3
        time4 = halfCycle * random.random() + quarterCycle
        time4I = timeCycle - time4
        newTime = timeStart + timeCycle * 2.0
        self.injuredTrack = Parallel(Sequence(LerpColorScaleInterval(self.injuredBlackoutGeom, timeCycle * 0.5, darkOutColor), LerpColorScaleInterval(self.injuredBlackoutGeom, timeCycle * 0.5, blackOutColor)), Sequence(LerpColorInterval(self.injuredEffects[0], time1I, onColor), LerpColorInterval(self.injuredEffects[0], time1, offColor), LerpColorInterval(self.injuredEffects[0], time2, onColor), LerpColorInterval(self.injuredEffects[0], time2I, offColor)), Sequence(LerpColorInterval(self.injuredEffects[2], time3, onColor), LerpColorInterval(self.injuredEffects[2], time3I, offColor), LerpColorInterval(self.injuredEffects[2], time4I, onColor), LerpColorInterval(self.injuredEffects[2], time4, offColor)), Sequence(LerpColorInterval(self.injuredEffects[1], time2I, onColor), LerpColorInterval(self.injuredEffects[1], time2, offColor), LerpColorInterval(self.injuredEffects[1], time1, onColor), LerpColorInterval(self.injuredEffects[1], time1I, offColor)), Sequence(LerpColorInterval(self.injuredEffects[3], time4, onColor), LerpColorInterval(self.injuredEffects[3], time4I, offColor), LerpColorInterval(self.injuredEffects[3], time3I, onColor), LerpColorInterval(self.injuredEffects[3], time3, offColor), Func(self.playInjuredEffect, newTime)))

    def finishInjuredEffect(self):
        finishColor = Vec4(0, 0, 0, 0)
        finishTime = 1.0
        hScale = Vec3(4, 0, 12)
        vScale = Vec3(4, 0, 9)
        if self.injuredTrack:
            self.injuredTrack.pause()
            self.injuredTrack = Parallel(LerpColorScaleInterval(self.injuredBlackoutGeom, finishTime, finishColor), LerpScaleInterval(self.injuredEffects[0], duration=finishTime, scale=vScale), LerpScaleInterval(self.injuredEffects[2], duration=finishTime, scale=vScale), LerpScaleInterval(self.injuredEffects[1], duration=finishTime, scale=hScale), LerpScaleInterval(self.injuredEffects[3], duration=finishTime, scale=hScale), Sequence(LerpColorInterval(self.injuredEffects[0], finishTime, finishColor)), Sequence(LerpColorInterval(self.injuredEffects[2], finishTime, finishColor)), Sequence(LerpColorInterval(self.injuredEffects[1], finishTime, finishColor)), Sequence(LerpColorInterval(self.injuredEffects[3], finishTime, finishColor), Func(self.stopInjuredEffect)))
            self.injuredTrack.start()

    def startInjuredEffect(self):
        self.setupInjuredEffect()
        for effect in self.injuredEffects:
            effect.show()

        self.injuredBlackoutGeom.setColorScale(Vec4(0.0, 0.0, 0.0, 0.0))
        self.injuredBlackoutGeom.show()
        self.playInjuredEffect()

    def playInjuredEffect(self, time=0):
        screenSizeX = base.a2dLeft - base.a2dRight
        screenSizeZ = base.a2dBottom - base.a2dTop
        self.injuredBlackoutGeom.setScale(screenSizeX, screenSizeZ, 1.0)
        self.regenInjuredTrack(time)
        self.injuredTrack.start()

    def stopInjuredEffect(self):
        self.injuredTrack.pause()
        for effect in self.injuredEffects:
            effect.setColor(0, 0, 0)
            effect.hide()

        self.injuredEffects[0].setScale(4, 0, 9)
        self.injuredEffects[2].setScale(4, 0, 9)
        self.injuredEffects[1].setScale(4, 0, 12)
        self.injuredEffects[3].setScale(4, 0, 12)
        self.injuredBlackoutGeom.hide()
        self.injuredTrack = None
        return

    def hitFromOffscreen(self, attacker):
        self.loadOffscreenHitEffects()
        pos = attacker.getPos(self.av)
        distance = attacker.getDistance(self.av)
        angle = rad2Deg(math.atan2(pos[0], pos[1]))
        if distance > 6.0 or hasattr(self.av, 'gameFSM') and self.av.gameFSM.state == 'Cannon' or self.av.gameFSM.state == 'ShipPilot':
            if angle < -135 or angle > 135:
                self.offscreenHitIvals[1].start()
            elif angle < -45:
                self.offscreenHitIvals[0].start()
            elif angle > 45:
                self.offscreenHitIvals[2].start()
            elif self.av.gameFSM.state == 'Cannon' or self.av.gameFSM.state == 'ShipPilot':
                self.offscreenHitIvals[3].start()

    def createLookoutPopup(self):
        self.lookoutPopup = NametagGroup()
        self.lookoutPopup.setColorCode(NametagGroup.CCToonBuilding)
        self.lookoutPopup.setAvatar(base.a2dBottomRight)
        self.lookoutPopup2D = NametagFloat2d()
        self.lookoutPopup2D.setContents(Nametag.CSpeech | Nametag.CThought)
        self.lookoutPopup2D.setActive(True)
        self.lookoutPopup.addNametag(self.lookoutPopup2D)
        self.lookoutPopup2DNode = base.a2dBottomRight.attachNewNode(self.lookoutPopup2D)
        self.lookoutPopup2DNode.setPosHprScale(-0.6, 0, 0.18, 0, 0, 0, 0.04, 0.04, 0.04)
        self.lookoutPopup2DNode.setColorScale(0.92, 0.82, 0.65, 1.0)
        self.lookoutPopup.setFont(PiratesGlobals.getInterfaceFont())
        self.lookoutPopup.manage(base.marginManager)
        self.lookoutPopup.setActive(True)
        self.lookoutPage.accept(self.lookoutPopup.getUniqueId(), self.lookoutPage.msgClick)

    def deleteLookoutPopup(self):
        self.lookoutPopup.unmanage(base.marginManager)
        self.lookoutPopup.removeNametag(self.lookoutPopup2D)
        del self.lookoutPopup
        del self.lookoutPopup2D
        del self.lookoutPopup2DNode

    def moveLookoutPopup(self, chestOpen=True):
        if self.lookoutPopup2DNode:
            if chestOpen:
                self.lookoutPopup2DNode.setPos(-1.7, 0, 0.18)
            else:
                self.lookoutPopup2DNode.setPos(-0.6, 0, 0.18)

    def loadPirateCode(self):
        if self.pirateCode:
            return
        self.pirateCode = BorderFrame(parent=base.a2dLeftCenter, frameSize=(0, 1.0,
                                                                            0, 0.3), pos=(0.25,
                                                                                          0,
                                                                                          0), scale=0.75)
        self.pirateCode.setName(self.pirateCode.uniqueName('PirateCodeBorderFrame'))
        codeMessage1 = DirectLabel(parent=self.pirateCode, relief=None, text=PLocalizer.PirateCodeWarning1, text_fg=(1,
                                                                                                                     1,
                                                                                                                     1,
                                                                                                                     1), text_shadow=(0,
                                                                                                                                      0,
                                                                                                                                      0,
                                                                                                                                      1), pos=(0.5,
                                                                                                                                               0,
                                                                                                                                               0.18), text_scale=0.08)
        codeMessage2 = DirectLabel(parent=self.pirateCode, relief=None, text=PLocalizer.PirateCodeWarning2, text_fg=(1,
                                                                                                                     1,
                                                                                                                     1,
                                                                                                                     1), text_shadow=(0,
                                                                                                                                      0,
                                                                                                                                      0,
                                                                                                                                      1), pos=(0.49,
                                                                                                                                               0,
                                                                                                                                               0.09), text_scale=0.08)
        self.pirateCode.hide()
        self.pirateCodeDialog = loadSfx(SoundGlobals.WTD_CODE)
        return

    def showPirateCode(self):
        if not self.pirateCode:
            self.loadPirateCode()
        if not self.codeShown:
            self.codeShown = 1
            self.pirateCode.show()
            base.playSfx(self.pirateCodeDialog)
            taskMgr.remove('hidePirateCode')
            taskMgr.doMethodLater(5.0, self.hidePirateCode, 'hidePirateCode')

    def hidePirateCode(self, task=None):
        if not self.pirateCode:
            return
        self.pirateCode.hide()
        self.pirateCodeDialog.stop()

    def toggleSocialPanel(self, args=None):
        if self.ignoreAllKeys or not self.seaChestAllowed or not self.getSocialPanelAllowed():
            return
        if self.socialPanel.isHidden():
            self.socialPanel.show()
            if self.seaChestActive:
                localAvatar.guiMgr.hideSeaChest()
            if hasattr(base, 'localAvatar'):
                base.localAvatar.removeContext(InventoryType.NewFriend)
                base.localAvatar.removeContext(InventoryType.NewGuild)
        else:
            self.socialPanel.hide()

    def showInventoryBagPanel(self, args=None):
        self.togglePage(self.inventoryBagPage, args)

    def showTreasurePanel(self, args=None):
        if self.togglePage(self.inventoryBagPage, args):
            self.inventoryBagPage.openTreasures()

    def showWeaponPanel(self, args=None):
        self.chestPanel.beenOpen = 1
        self.chestPanel.setTitleName(PLocalizer.SeaChestTitleWeapons)
        self.togglePage(self.weaponPage, args)

    def showSubCollection(self, args=None, setKey=None):
        self.collectionMain.hide(False)
        self.collectionPage.refreshList(setKey)
        self.collectionPage.show()

    def showCollectionMain(self, args=None):
        self.collectionPage.hide()
        self.collectionMain.show()

    def showCollectionPanel(self, args=None):
        self.togglePage(self.collectionPage, args)

    def showClothingPanel(self, args=None):
        self.togglePage(self.clothingPage, args)

    def showTitlesPanel(self, args=None):
        self.chestPanel.beenOpen = 1
        self.chestPanel.setTitleName(PLocalizer.SeaChestTitleBadges)
        if self.titlesPage:
            self.titlesPage.refresh()
        self.togglePage(self.titlesPage, args)

    def showShipPanel(self, args=None):
        self.chestPanel.beenOpen = 1
        self.chestPanel.setTitleName(PLocalizer.SeaChestTitleShips)
        self.togglePage(self.shipPage, args)

    def showQuestPanel(self, args=None):
        self.chestPanel.beenOpen = 1
        self.chestPanel.setTitleName(PLocalizer.SeaChestTitleQuests)
        self.initQuestPage()
        if self.questPage:
            if self.togglePage(self.questPage, args):
                messenger.send('questPageOpened')
            else:
                messenger.send('questPageClosed')
        self.removeNewQuestIndicator()
        if hasattr(base, 'localAvatar'):
            base.localAvatar.removeContext(InventoryType.QuestJournal)
            base.localAvatar.removeContext(InventoryType.ChangeQuestTracking)

    def showLookoutPanel(self, args=None):
        if not launcher.canLeaveFirstIsland():
            base.cr.centralLogger.writeClientEvent('Player encountered phase 4 blocker using the lookout system')
            self.showDownloadBlocker(DownloadBlockerPanel.Reasons.LOOKOUT)
        else:
            self.chestPanel.beenOpen = 1
            self.chestPanel.setTitleName(PLocalizer.SeaChestTitleLookout)
            if self.pageOpen(self.lookoutPage):
                messenger.send('lookoutClosed')
            else:
                messenger.send('lookoutOpened')
            self.lookoutPage.toggleVis(False)
            self.togglePage(self.lookoutPage, args)
            if hasattr(base, 'localAvatar'):
                base.localAvatar.removeContext(InventoryType.DockCommands)

    def disableLookoutPanel(self, disable):
        if disable:
            if self.pageOpen(self.lookoutPage):
                self.showLookoutPanel()
            self.chestTray.lookoutButton['state'] = DGG.DISABLED
            self.chestTray.lookoutButton.ignoreHotkeys()
            self.chestPanel.setPage(self.mapPage)
            self.chestTray.lookoutButton['image3_color'] = VBase4(0.4, 0.4, 0.4, 1)
            self.chestTray.lookoutButtonImage.setColorScale(1, 1, 1, 0.25)
        else:
            self.chestTray.lookoutButton['state'] = DGG.NORMAL
            self.chestTray.lookoutButton.acceptHotkeys()
            self.chestTray.lookoutButton['image3_color'] = VBase4(0.6, 0.6, 0.6, 1)
            self.chestTray.lookoutButtonImage.setColorScale(1, 1, 1, 1)

    def showDownloadBlocker(self, reason=None):
        if hasattr(self, '_dlBlocker'):
            self._dlBlocker.destroy()
        self._dlBlocker = DownloadBlockerPanel(reason)
        self._dlBlocker.setPos(0.1, 0, -0.4)
        self._dlBlocker.show()

    def showTeleportBlocker(self):
        if hasattr(self, '_tpBlocker'):
            self._tpBlocker.destroy()
        self._tpBlocker = TeleportBlockerPanel()
        self._tpBlocker.setPos(0.1, 0, -0.4)
        self._tpBlocker.show()

    def showMapPage(self, args=None):
        self.chestPanel.beenOpen = 1
        self.chestPanel.setTitleName(PLocalizer.SeaChestTitleMap)
        self.togglePage(self.mapPage, args)
        if hasattr(base, 'localAvatar'):
            base.localAvatar.removeContext(InventoryType.IslandTeleport)

    def showSkillPage(self, args=None):
        self.chestPanel.beenOpen = 1
        self.chestPanel.setTitleName(PLocalizer.SeaChestTitleSkills)
        result = self.togglePage(self.skillPage, args)
        if result:
            messenger.send('skillPanelOpened')
            if hasattr(base, 'localAvatar'):
                base.localAvatar.removeContext(InventoryType.NewSkillPoint)
        else:
            messenger.send('skillPanelClosed')

    def toggleSkillPageDemo(self, value):
        self.chestPanel.setTitleName(PLocalizer.SeaChestTitleSkills)
        if value:
            self.togglePage(self.skillPage, None)
            self.skillPage.showDemo()
        else:
            self.hideSeaChest()
            self.skillPage.removeDemo()
        return

    def togglePage(self, page, args=None):
        if self.ignoreAllKeys:
            return False
        if self.getTutorialStatus() < PiratesGlobals.TUT_MET_JOLLY_ROGER and page == self.lookoutPage:
            return False
        if self.ignoreAllButSkillHotKey and page != self.skillPage:
            return False
        if self.ignoreAllButLookoutHotKey and page != self.lookoutPage:
            return False
        self.hideMinimap()
        if self.pageOpen(page):
            self.hideSeaChest()
            return False
        elif self.seaChestAllowed:
            self.showSeaChest(page)
            if hasattr(base, 'localAvatar') and page == self.collectionMain:
                base.localAvatar.removeContext(InventoryType.QuestJournal)
            return True
        else:
            return False

    def pageOpen(self, page):
        if self.chestPanel.getCurPage() == page and self.chestPanel.isActive():
            return 1
        else:
            return 0

    def setMoney(self, money):
        self.moneyDisplay['text'] = '\x01white\x01%s\x02' % money

    def setUIScale(self, scale):
        base.a2dTopCenter.setScale(scale)
        base.a2dBottomCenter.setScale(scale)
        base.a2dLeftCenter.setScale(scale)
        base.a2dRightCenter.setScale(scale)
        base.a2dTopLeft.setScale(scale)
        base.a2dTopRight.setScale(scale)
        base.a2dBottomLeft.setScale(scale)
        base.a2dBottomRight.setScale(scale)

    def setChatAllowed(self, allowed, close=False):
        self.chatAllowed = allowed

    def setSeaChestAllowed(self, allowed, close=False, priority=0, reset=False):
        if priority >= self.chestLock:
            self.chestLock = priority
            self.seaChestAllowed = allowed
            if self.seaChestAllowed:
                self.accept(PiratesGlobals.SeaChestHotkey, self.toggleSeaChest)
            else:
                self.ignore(PiratesGlobals.SeaChestHotkey)
                if close:
                    self.hideSeaChest()
        if reset:
            self.chestLock = 0

    def isSeaChestAllowed(self):
        if self.mainMenu and not self.mainMenu.isHidden():
            return False
        return self.seaChestAllowed

    def _showCursor(self):
        wp = WindowProperties()
        wp.setCursorHidden(0)
        base.win.requestProperties(wp)
        base.graphicsEngine.openWindows()

    def _showMouse(self):
        localAvatar.cameraFSM.disableMouseControl()
        self.combatTray.disableMouseDrawsWeapon()
        self._showCursor()
        base.win.movePointer(0, self.mouseX, self.mouseY)

    def _hideCursor(self):
        wp = WindowProperties()
        wp.setCursorHidden(1)
        base.win.requestProperties(wp)
        base.graphicsEngine.openWindows()

    def _hideMouse(self, moveToCenter=True):
        localAvatar.cameraFSM.enableMouseControl()
        self.combatTray.enableMouseDrawsWeapon()
        self._hideCursor()
        if moveToCenter and base.mouseWatcherNode.hasMouse():
            self.mouseX = base.win.getPointer(0).getX()
            self.mouseY = base.win.getPointer(0).getY()
            base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)

    def showSeaChest(self, page=None):
        if page:
            self.chestPanel.setPage(page)
        if not self.seaChestActive:
            self.seaChestActive = True
            self.chestPanel.slideOpen()
            self.chestTray.slideOpen()
            hSize = base.a2dLeft - base.a2dRight
            hOffSet = abs(hSize) * CHEST_FILM_OFFSET_MULT + CHEST_FILM_OFFSET_CONST
            self.filmOffsetLerp = Parallel(LerpFunctionInterval(self.setFilmOffsetX, fromData=FILM_NEUTRAL_OFFSET, toData=hOffSet, duration=0.25, blendType='noBlend', name='film Offset'), LerpFunctionInterval(self.setFilmOffsetY, fromData=0.0, toData=CHEST_FILM_Y, duration=0.25, blendType='noBlend', name='film OffsetY'))
            if not self.chestTray.isHidden() and localAvatar.getGameState() != 'ParlorGame':
                self.filmOffsetLerp.start()
            self.filmShouldOffset = 1
            self.hideStickySeaChestIcons()
            messenger.send('seachestOpened')
            self.removeNewQuestIndicator()
            self.hidePrevPanel()
        if not self.socialPanel.isHidden():
            self.socialPanel.hide()
            self.socialPanelReturn = True

    def setFilmOffsetX(self, offX):
        offY = base.camLens.getFilmOffset()[1]
        base.camLens.setFilmOffset(offX, offY)
        messenger.send('FilmOffset_Change')

    def setFilmOffsetY(self, offY):
        offX = base.camLens.getFilmOffset()[0]
        base.camLens.setFilmOffset(offX, offY)
        messenger.send('FilmOffset_Change')

    def hideSeaChest(self):
        if self.seaChestActive:
            self.seaChestActive = False
            self.chestPanel.slideClose()
            self.chestTray.slideClose()
            hSize = base.a2dLeft - base.a2dRight
            hOffSet = abs(hSize) * CHEST_FILM_OFFSET_MULT + CHEST_FILM_OFFSET_CONST
            self.filmOffsetLerp = Parallel(LerpFunctionInterval(self.setFilmOffsetX, fromData=hOffSet, toData=FILM_NEUTRAL_OFFSET, duration=0.25, blendType='noBlend', name='film Offset'), LerpFunctionInterval(self.setFilmOffsetY, fromData=CHEST_FILM_Y, toData=0.0, duration=0.25, blendType='noBlend', name='film OffsetY'))
            if not self.chestTray.isHidden() and localAvatar.getGameState() != 'ParlorGame':
                self.filmOffsetLerp.start()
            self.filmShouldOffset = 0
            self.showStickySeaChestIcons()
            self.showPrevPanel()
            messenger.send('seachestClosed')
        if self.socialPanelReturn:
            self.socialPanel.show()
            self.socialPanelReturn = False

    def enterWorldMode(self):
        self.enterMouseLook()

    def enterMouseLook(self):
        if self.getTutorialStatus() >= PiratesGlobals.TUT_GOT_COMPASS:
            self.setChatAllowed(True)
        if self.getTutorialStatus() >= PiratesGlobals.TUT_GOT_SEACHEST:
            self.setSeaChestAllowed(True)
        messenger.send('GuiManagerWorldMode')
        if self.mainMenu:
            self.mainMenu.abruptHide()
            self.profilePage.createBuffer()
        self.hideMinimap()

    def filterWorldMode(self, request, args):
        return self.filterMouseLook(request, args)

    def filterMouseLook(self, request, args):
        return self.defaultFilter(request, args)

    def exitWorldMode(self):
        self.exitMouseLook()

    def exitMouseLook(self):
        pass

    def enterPopup(self):
        self.setChatAllowed(False)
        self.setSeaChestAllowed(False)

    def filterPopup(self, request, args):
        return self.defaultFilter(request, args)

    def exitPopup(self):
        pass

    def enterInterface(self, extraArgs=[
 True, True]):
        allowChat = extraArgs[0]
        allowSeaChest = extraArgs[1] & (localAvatar.style.getTutorial() >= PiratesGlobals.TUT_GOT_SEACHEST)
        self.setChatAllowed(allowChat, close=not allowChat)
        self.setSeaChestAllowed(allowSeaChest, close=not allowChat)

    def filterInterface(self, request, args):
        return self.defaultFilter(request, args)

    def exitInterface(self):
        pass

    def enterInteraction(self, extraArgs=[
 True, True]):
        allowChat = extraArgs[0]
        allowSeaChest = extraArgs[1] & (localAvatar.style.getTutorial() >= PiratesGlobals.TUT_GOT_SEACHEST)
        self.setChatAllowed(allowChat, close=not allowChat)
        self.setSeaChestAllowed(allowSeaChest, close=not allowChat)
        self.combatTray.hide()
        self.chestTray.hide()
        if self.filmOffsetLerp:
            self.filmOffsetLerp.pause()
            self.filmOffsetLerp = None
        self.setFilmOffsetX(0.0)
        self.setFilmOffsetY(0.0)
        return

    def filterInteraction(self, request, args):
        return self.defaultFilter(request, args)

    def exitInteraction(self):
        self.combatTray.show()
        self.chestTray.show()

    def enterCutscene(self):
        self.hideTrays()
        self.setIgnoreEscapeHotKey(True)

    def filterCutscene(self, request, args):
        return self.defaultFilter(request, args)

    def exitCutscene(self):
        self.showTrays()
        self.setIgnoreEscapeHotKey(False)

    def toggleSeaChest(self):
        self.hideMinimap()
        if self.seaChestActive:
            self.hideSeaChest()
        elif self.isSeaChestAllowed():
            self.showSeaChest()

    def hideStickySeaChestIcons(self):
        for currIcon in self.stickySeaChestIcons:
            currIcon.hide()

    def showStickySeaChestIcons(self):
        for currIcon in self.stickySeaChestIcons:
            currIcon.show()

    def addStickySeaChestIcon(self, iconType):
        pass

    def createReceiveEffect(self, uiItem, explain=False):
        displayIval = Sequence()
        if explain:
            uiItem.setScale(0, 0, 0)
            uiItem.setPos(-2, 0, -1.2)
            uiItem.setColorScale(1, 1, 1, 0)
            startPos = uiItem.getPos()
            finalPos = Point3(-0.8, 0, -1.0)
            startScale = uiItem.getScale()
            finalScale = Point3(2, 2, 2)
            displayIval.append(Func(uiItem.hideMinimapObjects))
        else:
            startPos = uiItem.getPos()
            finalPos = Point3(-0.4, 0, -0.4)
            startScale = uiItem.getScale()
            finalScale = Point3(1.0, 1.0, 1.0)
        receiveDelay = 0.35
        placeDelay = 0.7
        displayIval.append(Sequence(Parallel(LerpScaleInterval(uiItem, duration=receiveDelay, scale=startScale, blendType='easeOut'), LerpColorScaleInterval(uiItem, receiveDelay, Vec4(1, 1, 1, 1), blendType='easeIn')), Wait(0.5), Parallel(LerpPosInterval(uiItem, duration=placeDelay, pos=finalPos, blendType='easeIn'), LerpScaleInterval(uiItem, duration=placeDelay, scale=finalScale, blendType='easeIn'))))
        if not explain:
            pass
        displayIval.start()
        self.addEffectIval(displayIval)

    def addEffectIval(self, ival):
        self.effectIvals.append(ival)

    def clearIvals(self):
        for currEffectIval in self.effectIvals:
            currEffectIval.finish()

        self.effectIvals = []

    def toggleMainMenu(self, args=None):
        if self.disableMainMenu:
            return
        if self.ignoreMainMenuHotKey:
            return
        if args and (args == 'escape' or args == 'Esc') and (self.ignoreEscapeHotKey or self.av.gameFSM.state in ('Battle',
                                                                                                                  'Cutscene',
                                                                                                                  'Cannon',
                                                                                                                  'Dialog',
                                                                                                                  'NPCInteract',
                                                                                                                  'ShipPilot',
                                                                                                                  'DinghyInteract',
                                                                                                                  'MakeAPirate',
                                                                                                                  'Fishing')):
            return
        if self.av.gameFSM.state in ('TeleportIn', 'TeleportOut', 'EnterTunnel', 'Digging',
                                     'Searching', 'ShipRepair', 'BenchRepair', 'DoorKicking'):
            return
        if self.mainMenu and self.mainMenu.gameOptions and not self.mainMenu.gameOptions.isHidden():
            return
        if self.mainMenu and self.mainMenu.popupDialog:
            return
        self.hideSeaChest()
        if not self.mainMenu:
            if base.config.GetBool('want-custom-keys', 0):
                width = 1.8
            else:
                width = 1.6
            height = 1.6
            x = -width / 2
            y = -height / 2
            self.mainMenu = MainMenu('Main Menu', x, y, width, height)
            self.mainMenu.hide()
        if self.mainMenu.isHidden():
            self.socialPanel.hide()
            self.chatPanel.hide()
            self.av.chatMgr.stop()
            self.av.stopChat()
            self.av.stopAutoRun()
            #self.av.motionFSM.moveLockIfOn()
            self.setChatAllowed(False, close=True)
            self.setSeaChestAllowed(False)
            self.mainMenu.showMenu()
        else:
            if self.av.getGameState() not in ('Cutscene', 'Dialog', 'NPCInteract',
                                              'DinghyInteract', 'MakeAPirate'):
                self.chatPanel.show()
                self.av.chatMgr.start()
                self.av.startChat()
                self.setSeaChestAllowed(True)
                #self.av.motionFSM.onIfMoveLock()
            self.mainMenu.hideMenu()
            self.profilePage.createBuffer()

    def addMinimap(self, minimap):
        minimap.getScreenNode().reparentTo(self.minimapRoot)

    def removeMinimap(self, minimap):
        if minimap:
            self.clearMinimap(minimap)
            minimap.getScreenNode().detachNode()

    def setMinimap(self, minimap):
        self.hideMinimap()
        if self.minimap is not minimap:
            self.oldMap = self.minimap
            self.newMap = minimap
            messenger.send('transferMinimapObjects', [self])
            self.oldMap = None
            self.newMap = None
            self.minimap = minimap
            self.hideMinimap()
            self.radarGui.setMinimap(minimap)
        return

    def transferMinimapObject(self, obj):
        if self.oldMap:
            self.oldMap.removeObject(obj)
        if self.newMap:
            self.newMap.addObject(obj)

    def getMinimap(self):
        return self.minimap

    def clearMinimap(self, minimap):
        if self.minimap is minimap:
            self.setMinimap(None)
        return

    def hideMinimap(self):
        if self.minimap:
            self.minimap.request('Off')

    def nextMinimap(self):
        if self.minimap:
            self.minimap.request('next')
            if hasattr(base, 'localAvatar'):
                base.localAvatar.removeContext(InventoryType.IslandMap)
        else:
            self.createWarning(PLocalizer.MinimapNotAvailable, duration=3)

    def handleMinimapKeyDown(self):
        if base.config.GetBool('want-momentary-minimap', 1):
            if self.minimap and self.minimap.allowOnScreen():
                self.minimap.request('Opaque')
            else:
                self.createWarning(PLocalizer.MinimapNotAvailable, duration=3)
        else:
            self.nextMinimap()

    def handleMinimapKeyUp(self):
        if base.config.GetBool('want-momentary-minimap', 1):
            if self.minimap:
                self.minimap.request('Off')

    def showDirtPanel(self):
        if not self.dirtPanel:
            self.createDirtPanel()
        if self.dirtFader:
            self.dirtFader.pause()
            self.dirtFader = None
        self.dirtPanel.setAlphaScale(1.0)
        self.dirtPanel.show()
        return

    def hideDirtPanel(self):
        if self.dirtPanel is None:
            return
        fadeOut = LerpFunctionInterval(self.dirtPanel.setAlphaScale, fromData=self.dirtPanel.getColorScale()[3], toData=0, duration=0.3)
        self.dirtFader = Sequence(fadeOut, Func(self.dirtPanel.hide))
        self.dirtFader.start()
        return

    def createSmokePanel(self):
        card = loader.loadModel('models/effects/blinders')
        smokeTex = card.find('**/effectSmokeBlind')
        card.removeNode()
        del card
        self.smokePanel = DirectFrame(parent=aspect2d, relief=None, frameSize=(-4,
                                                                               4,
                                                                               -4.0,
                                                                               4.0), frameColor=(0.5,
                                                                                                 0.5,
                                                                                                 0.5,
                                                                                                 0.85), sortOrder=25, pos=(0,
                                                                                                                           0,
                                                                                                                           0.25), image=smokeTex, image_scale=4.0, suppressMouse=0, suppressKeys=0)
        self.smokePanel.hide()
        return

    def createDirtPanel(self):
        card = loader.loadModel('models/effects/blinders')
        dirtTex = card.find('**/effectDirtBlind')
        card.removeNode()
        del card
        self.dirtPanel = DirectFrame(parent=aspect2d, relief=None, frameSize=(-4, 4,
                                                                              -4.0,
                                                                              4.0), frameColor=(0.5,
                                                                                                0.5,
                                                                                                0.5,
                                                                                                0.85), sortOrder=25, pos=(0,
                                                                                                                          0,
                                                                                                                          0.25), image=dirtTex, image_scale=4.0, suppressMouse=0, suppressKeys=0)
        self.dirtPanel.hide()
        return

    def showSmokePanel(self):
        if not self.smokePanel:
            self.createSmokePanel()
        if self.smokeFader:
            self.smokeFader.pause()
            self.smokeFader = None
        self.smokePanel.setAlphaScale(1.0)
        self.smokePanel.show()
        return

    def hideSmokePanel(self):
        if self.smokePanel is None:
            return
        fadeOut = LerpFunctionInterval(self.smokePanel.setAlphaScale, fromData=self.smokePanel.getColorScale()[3], toData=0, duration=0.3)
        self.smokeFader = Sequence(fadeOut, Func(self.smokePanel.hide))
        self.smokeFader.start()
        return

    def showQuestProgress(self, questProgress):
        if not self.progressText:
            self.progressText = DirectLabel(parent=base.a2dBottomCenter, relief=None, text='', text_pos=(0,
                                                                                                         0.06), text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0,
                                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                                             0.1))
            self.showProgressIval = Sequence(Func(self.progressText.clearColorScale), Func(self.progressText.show), Wait(4.0), LerpColorScaleInterval(self.progressText, 1.0, colorScale=Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1)), Func(self.progressText.hide))
        if not questProgress:
            progressText = PLocalizer.DidNotFindQuestItem
            self.progressText['text'] = progressText
            self.showProgressIval.start()
        return

    def toggleGuiForNpcInteraction(self, state):
        if state == 0:
            self.hideSeaChest()
            self.gameGui.hide()
            self.chatPanel.hide()
            self.radarGui.hide()
            self.combatTray.hide()
            self.moneyDisplay.hide()
            self.chestTray.hideChestButton()
            self.contextTutPanel.hide()
            if not self.socialPanel.isHidden():
                self.socialPanel.hide()
                self._putBackSocialPanel = 1

            if self.tmButtonQuick:
                self.tmButtonQuick.hide()

            if self.tmButtonSearch:
                self.tmButtonSearch.hide()

            if self.questPage:
                self.hideTrackedQuestInfo()

            if self.crewHUD.hudOn:
                self.crewHUD.setHUDOff()
                self.crewHUDTurnedOff = True

            self.hideMinimap()
            self.profilePage.hide()
        else:
            self.hideSeaChest()
            self.gameGui.show()
            self.chatPanel.show()
            self.combatTray.show()
            self.chestTray.showChestButton()
            if self.contextTutPanel.isFilled():
                self.contextTutPanel.show()

            if self._putBackSocialPanel:
                self.socialPanel.show()
                self._putBackSocialPanel = 0

        if self.getTutorialStatus() >= PiratesGlobals.TUT_GOT_COMPASS:
            self.radarGui.show()
            if self.tmButtonQuick:
                self.tmButtonQuick.show()

            if self.tmButtonSearch:
                self.tmButtonSearch.show()

            if self.trackedQuestLabel['text']:
                pass

            if len(self.av.activeQuestId):
                self.showTrackedQuestInfo()

        if self.crewHUDTurnedOff:
            if self.getTutorialStatus() >= PiratesGlobals.TUT_MET_JOLLY_ROGER and self.forceLookout or self.crewHUD.crew:
                self.crewHUD.setHUDOn()
                self.crewHUDTurnedOff = False

    def showStayTuned(self, quest=None, focus=None):
        if not self.stayTunedPanel:
            self.stayTunedPanel = StayTunedPanel.StayTunedPanel()
        if focus is not None:
            self.stayTunedPanel.setPicFocus(focus)
        if quest is not None:
            self.stayTunedPanel.show(quest)
        else:
            self.stayTunedPanel.show()
        return

    def showNonPayer(self, quest=None, focus=None):
        if not __dev__ and localAvatar.isPaid:
            return
        if not self.nonPayerPanel:
            self.nonPayerPanel = TrialNonPayerPanel.TrialNonPayerPanel(trial=False)
        if quest is not None:
            self.nonPayerPanel.show(quest)
        else:
            self.nonPayerPanel.show()
        return

    def flashOceanMsg(self, oceanZoneName):
        self.oceanMsg.show()
        self.oceanMsg['text'] = PLocalizer.EnterOceanZone % oceanZoneName
        self.oceanMsg.setScale(0.1, 0.1, 0.1)
        self.oceanIval = Sequence(LerpScaleInterval(self.oceanMsg, duration=2.0, scale=Point3(0.45, 0.45, 0.45), blendType='easeOut'), LerpScaleInterval(self.oceanMsg, duration=3.0, scale=Point3(0.1, 0.1, 0.1), blendType='easeOut'), Func(self.oceanMsg.hide))
        self.oceanIval.start()

    def createPreviewTag(self):
        return
        if Freebooter.AllAccessHoliday:
            return
        if launcher.getValue('GAME_SHOW_ADDS') == 'NO':
            return
        self.prevTag = DirectFrame(parent=base.a2dTopRight, relief=None, pos=(-0.25,
                                                                              0,
                                                                              -0.63), scale=0.8, sortOrder=0)
        gui2 = loader.loadModel('models/textureCards/basic_unlimited')
        self.imageOne = DirectFrame(parent=self.prevTag, relief=None, image=gui2.find('**/but_message_panel_border'), image_scale=(1,
                                                                                                                                   1,
                                                                                                                                   0.95), scale=0.4)
        self.titleText1 = DirectLabel(parent=self.prevTag, relief=None, text=PLocalizer.PreviewTitle1, text_align=TextNode.ACenter, text_scale=0.09, text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getPirateFont(), text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.0,
                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                 0.08))
        self.titleText2 = DirectLabel(parent=self.prevTag, relief=None, text=PLocalizer.PreviewTitle2, text_align=TextNode.ACenter, text_scale=0.07, text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getPirateFont(), text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.0, 0, -0.01))
        norm_geom = gui2.find('**/but_nav')
        over_geom = gui2.find('**/but_nav_over')
        down_geom = gui2.find('**/but_nav_down')
        dsbl_geom = gui2.find('**/but_nav_disabled')
        self.upgradeButton = DirectButton(parent=self.prevTag, relief=None, geom=(norm_geom, down_geom, over_geom), pos=(0.0, 0, -0.11), scale=0.8, command=base.popupBrowser, extraArgs=[launcher.getValue('GAME_INGAME_UPGRADE'), True], text=PLocalizer.FirstAddUpgrade, text_fg=PiratesGuiGlobals.TextFG1, text_font=PiratesGlobals.getInterfaceFont(), text_shadow=PiratesGuiGlobals.TextShadow, text_scale=0.05, text_wordwrap=9, text_pos=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                  0.01))
        return

    def showPrevPanel(self):
        if self.prevTag and not Freebooter.AllAccessHoliday:
            self.prevTag.show()

    def hidePrevPanel(self):
        if self.prevTag:
            self.prevTag.hide()

    def stashPrevPanel(self):
        if self.prevTag:
            self.prevTag.stash()

    def showBlackPearlButtonsForTest(self):

        def inventoryReceived(inventory):
            if inventory:
                self.invRequest = None
                tms = inventory.getTreasureMapsList()
                for currTm in tms:
                    if currTm.mapId == PiratesGlobals.GAME_STYLE_TM_BLACK_PEARL:
                        currTm.sendUpdate('requestIsEnabled')
                        self.addTreasureMapButtons(currTm)
                        break

            return

        DistributedInventoryBase.DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), inventoryReceived)

    def addTreasureMapButtons(self, tm):
        if launcher.getValue('GAME_ENVIRONMENT', 'LIVE') in ['QA', 'DEV']:
            helpPos = (
             -0.26, 0, 0.095)
            self.tmButtonQuick = GuiButton(parent=base.a2dTopRight, text=PLocalizer.PlayTMNow, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0, -0.01), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=40, image_scale=(0.45,
                                                                                                                                                                                                                                                                                                            1,
                                                                                                                                                                                                                                                                                                            0.25), command=self.questPage.startTreasureMap, extraArgs=[tm], pos=(-0.65,
                                                                                                                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                                                                                                                 -0.23), helpText=PLocalizer.PlayTMNowHelp, helpPos=helpPos)
            self.tmButtonSearch = GuiButton(parent=base.a2dTopRight, text=PLocalizer.PlayTMLookout, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0, -0.01), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=40, image_scale=(0.45,
                                                                                                                                                                                                                                                                                                                 1,
                                                                                                                                                                                                                                                                                                                 0.25), command=self.questPage.startTreasureMap, extraArgs=[tm, False], pos=(-0.65,
                                                                                                                                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                                                                                                                                             -0.33), helpText=PLocalizer.PlayTMLookoutHelp, helpPos=helpPos)
            self.tmButtonQuick.setColorScale(1, 1, 1, 0.75)
            self.tmButtonSearch.setColorScale(1, 1, 1, 0.75)

    def addDowsingButton(self):
        if not self.dowsingButton:
            self.dowsingButton = GuiButton(parent=base.a2dTopRight, text=PLocalizer.Dowse, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0, -0.01), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=40, image_scale=(0.45,
                                                                                                                                                                                                                                                                                                        1,
                                                                                                                                                                                                                                                                                                        0.25), command=localAvatar.d_useDowsingRod, pos=(-0.65,
                                                                                                                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                                                                                                                         -0.23))

    def removeDowsingButton(self):
        if self.dowsingButton:
            self.dowsingButton.destroy()
            self.dowsingButton = None
        return

    def addCheckPortraitButton(self):
        if not self.checkPortraitButton:
            self.checkPortraitButton = GuiButton(parent=base.a2dTopRight, text=PLocalizer.CheckPortrait, text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_pos=(0.0, -0.01), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=40, textMayChange=1, image_scale=(0.45,
                                                                                                                                                                                                                                                                                                                                       1,
                                                                                                                                                                                                                                                                                                                                       0.25), command=self.checkPortrait, pos=(-0.65,
                                                                                                                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                                                                                                                               -0.23))

    def removeCheckPortraitButton(self):
        if self.checkPortraitButton:
            self.checkPortraitButton.destroy()
            self.checkPortraitButton = None
        if self.clubheartsPortrait:
            self.clubheartsPortrait.destroy()
            self.clubheartsPortrait = None
        return

    def checkPortrait(self):
        if self.clubheartsPortrait:
            self.clubheartsPortrait.destroy()
            self.clubheartsPortrait = None
            if self.checkPortraitButton:
                self.checkPortraitButton['text'] = PLocalizer.CheckPortrait
        else:
            self.clubheartsPortrait = ClubheartsPortrait.ClubheartsPortrait()
            if self.checkPortraitButton:
                self.checkPortraitButton['text'] = PLocalizer.RemovePortrait
        return

    def setSocialPanelAllowed(self, value):
        self.socialPanelAllowed = value

    def getSocialPanelAllowed(self):
        return self.getTutorialStatus() >= PiratesGlobals.TUT_MET_JOLLY_ROGER and self.socialPanelAllowed

    def setIgnoreAllKeys(self, ignore):
        self.ignoreAllKeys = ignore

    def setIgnoreAllButSkillHotKey(self, ignore):
        self.ignoreAllButSkillHotKey = ignore

    def setIgnoreAllButLookoutHotKey(self, ignore):
        self.ignoreAllButLookoutHotKey = ignore

    def setIgnoreMainMenuHotKey(self, ignore):
        if ignore:
            taskMgr.remove('removeIgnoreMainMenu')
            self.ignoreMainMenuHotKey = ignore
        else:
            taskMgr.doMethodLater(2, self.delayedSetIgnoreMainMenuHotKey, 'removeIgnoreMainMenu', [ignore])

    def delayedSetIgnoreMainMenuHotKey(self, ignore):
        self.ignoreMainMenuHotKey = ignore

    def setIgnoreEscapeHotKey(self, ignore):
        if ignore:
            taskMgr.remove('removeIgnoreEscape')
            self.ignoreEscapeHotKey = ignore
        else:
            taskMgr.doMethodLater(2, self.delayedSetIgnoreEscapeHotKey, 'removeIgnoreEscape', [ignore])

    def delayedSetIgnoreEscapeHotKey(self, ignore):
        self.ignoreEscapeHotKey = ignore

    def isSkillPanelOpen(self):
        if self.chestPanel.getCurPage() == self.skillPage:
            return True
        return False

    def hideChestTray(self):
        self.chestTray.hide()
        if self.filmOffsetLerp:
            self.filmOffsetLerp.pause()
            self.filmOffsetLerp = None
        self.setFilmOffsetX(0.0)
        self.setFilmOffsetY(0.0)
        return

    def showChestTray(self):
        self.chestTray.show()
        if self.filmShouldOffset:
            self.setFilmOffsetX(0.15)
            self.setFilmOffsetY(-0.05)

    def allowSkillPageOnly(self):
        self.setSeaChestAllowed(True)
        self.setIgnoreAllButSkillHotKey(True)
        self.chestPanel.setCurPage(0)

    def allowLookoutPageOnly(self):
        self.setSeaChestAllowed(True)
        self.setSocialPanelAllowed(False)
        self.setIgnoreAllButLookoutHotKey(True)
        self.chestPanel.setCurPage(0)

    def updateTrackedQuestLabel(self):
        text = self.questStatusText + self.questHintText
        self.removeDowsingButton()
        self.removeCheckPortraitButton()
        if localAvatar.activeQuestId:
            quest = localAvatar.getQuestById(localAvatar.activeQuestId)
            if quest:
                if quest.questDNA.getTimeLimit():
                    if not self.questTimerText:
                        self.questTimerText = quest.getTimerText()
                    text = text + '\n' + self.questTimerText
                questTasks = quest.questDNA.getTasks()
                for currQuestTask in questTasks:
                    if isinstance(currQuestTask, DowsingRodTaskDNA) and not quest.isComplete():
                        self.addDowsingButton()
                        break

                if quest.getQuestId() == 'rc.ghosts.clubhearts.disguise' and not quest.isComplete():
                    self.addCheckPortraitButton()
        if text and not self.gameGui.isHidden():
            self.showTrackedQuestInfo()
        elif not text:
            self.hideTrackedQuestInfo()
        self.trackedQuestLabel['text'] = text

    def hideTrackedQuestInfo(self):
        self.trackedQuestLabel.hide()
        if self.dowsingButton:
            self.dowsingButton.hide()
        if self.checkPortraitButton:
            self.checkPortraitButton.hide()
            if self.clubheartsPortrait:
                self.clubheartsPortrait.destroy()
                self.checkPortraitButton['text'] = PLocalizer.CheckPortrait

    def showTrackedQuestInfo(self):
        self.trackedQuestLabel.show()
        if self.dowsingButton:
            self.dowsingButton.show()
        if self.checkPortraitButton:
            self.checkPortraitButton.show()

    def updateQuestStatusText(self, questId):

        def changeQuestStatus(task):
            quest = localAvatar.getQuestById(questId)
            if quest:
                timeLimit = quest.questDNA.getTimeLimit()
                if quest.isCompleteWithBonus() or timeLimit and not quest.getTimeRemaining():
                    statusText = quest.getReturnText()
                else:
                    statusText = quest.getStatusText()
                self.setQuestStatusText(statusText)
                return task.done
            else:
                task.setDelay(1)
                return task.again

        taskMgr.remove('guiMgrChangeQuestStatus')
        taskMgr.doMethodLater(0, changeQuestStatus, 'guiMgrChangeQuestStatus')

    def setQuestStatusText(self, text=''):
        self.questStatusText = text
        self.updateTrackedQuestLabel()

    def setQuestHintText(self, text=''):
        self.questHintText = text
        self.updateTrackedQuestLabel()

    def setQuestTimerText(self, text=''):
        self.questTimerText = text
        self.updateTrackedQuestLabel()

    def systemWarning(self, warningText='Bad things'):
        from pirates.chat import ChatWarningBox
        self.chatWarningBox = ChatWarningBox.ChatWarningBox(warningText)
        self.chatWarningBox.reparentTo(aspect2d)
        self.chatWarningBox.setZ(0.25)

    def closeSystemWarning(self):
        if self.chatWarningBox:
            self.chatWarningBox.close()
        self.chatWarningBox = None
        return

    def gameGuiPressed(self):
        self.handleAvatarDetails(localAvatar.getDoId())
