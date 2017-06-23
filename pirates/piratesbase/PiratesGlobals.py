from pandac.PandaModules import *
import PLocalizer
from otp.otpbase.OTPGlobals import *
from direct.gui import DirectFrame
from direct.gui import DirectButton
from pirates.uberdog.UberDogGlobals import *
from pirates.piratesbase import PLocalizer as PL
from otp.otpbase import OTPLocalizer as OL
from pirates.piratesbase import EmoteGlobals
searchPath = DSearchPath()
for i in range(getModelPath().getNumDirectories()):
    searchPath.appendDirectory(getModelPath().getDirectory(i))

ShipsDatabaseChannelId = 4008
AvatarsDatabaseChannelId = 4021
InventoryDatabaseChannelId = 4023
DatabaseIdFromClassName = {'DistributedPlayerPirate': AvatarsDatabaseChannelId,'DistributedInventory': InventoryDatabaseChannelId,'PirateInventory': InventoryDatabaseChannelId,'DistributedGoldReceipt': InventoryDatabaseChannelId,'DistributedFlag': InventoryDatabaseChannelId,'DistributedQuest': InventoryDatabaseChannelId,'DistributedTreasureMap': InventoryDatabaseChannelId,'DistributedPlayerSimpleShip': ShipsDatabaseChannelId}
preLoadSet = [
 'models/char/fp_2000', 'models/char/fp_1000', 'models/char/fp_500', 'models/char/mp_2000', 'models/char/mp_1000', 'models/char/mp_500', 'models/misc/male_clothes.bam', 'models/misc/female_clothes.bam', 'models/misc/male_body.bam', 'models/misc/female_body.bam', 'models/misc/male_face.bam', 'models/misc/female_face.bam', 'models/char/fp_idle', 'models/char/mp_idle', 'models/char/fp_walk', 'models/char/mp_walk', 'models/char/crab_2000', 'models/char/crab_1000', 'models/char/crab_500', 'models/textureCards/shipTextures', 'models/char/fp_tread_water', 'models/char/mp_tread_water', 'models/char/rooster_hi', 'models/char/rooster_med', 'models/char/rooster_low', 'models/char/pig_hi', 'models/char/pig_med', 'models/char/pig_low', 'models/char/dog_hi', 'models/char/seagull_hi', 'models/sea/wake_zero', 'models/effects/compass_rose', 'models/vegetation/bush_a', 'models/vegetation/bush_b', 'models/vegetation/bush_c', 'models/vegetation/bush_d', 'models/vegetation/bush_e', 'models/vegetation/bush_f', 'models/vegetation/gen_tree_a', 'models/vegetation/gen_tree_b', 'models/vegetation/gen_tree_c', 'models/vegetation/gen_tree_d', 'models/vegetation/gen_tree_e']
INVALID_TEAM = -1
PLAYER_TEAM = 0
UNDEAD_TEAM = 1
NAVY_TEAM = 2
TRADING_CO_TEAM = 3
VILLAGER_TEAM = 4
ISLAND_TEAM = 5
TUTORIAL_ENEMY_TEAM = 6
FRENCH_UNDEAD_TEAM = 7
SPANISH_UNDEAD_TEAM = 8
PROP_TEAM = 9
VOODOO_ZOMBIE_TEAM = 10
BOUNTY_HUNTER_TEAM = 11
NeutralTeams = [
 PLAYER_TEAM, VILLAGER_TEAM]
FriendlyTeams = []
NEUTRAL = 0
PVP_ENEMY = 1
PVP_FRIEND = 2
ENEMY = 3
FRIEND = 4
CREW = 5
PLAYER_TEAM_STR = 'Player'
UNDEAD_TEAM_STR = 'Undead'
NAVY_TEAM_STR = 'EvilNavy'
TRADING_CO_TEAM_STR = 'TradingCo'
VILLAGER_TEAM_STR = 'Villager'
ISLAND_TEAM_STR = 'Island'
TUTORIAL_ENEMY_TEAM_STR = 'TutorialEnemy'
FRENCH_UNDEAD_TEAM_STR = 'French Undead'
SPANISH_UNDEAD_TEAM_STR = 'Spanish Undead'
VOODOO_ZOMBIE_TEAM_STR = 'Juju Sailors'
BOUNTY_HUNTER_TEAM_STR = 'Bounty Hunters'
PLAYER_NAMETAG = (1, 0.8, 0.5, 1)
UNDEAD_NAMETAG = (0.6, 0.6, 0.6, 1)
NAVY_NAMETAG = (1, 0.2, 0.2, 1)
FRENCH_NAMETAG = (0.1, 0.1, 0.44, 1.0)
SPANISH_NAMETAG = (0.85, 0.65, 0.13, 1.0)
NAMETAG_WORDWRAP = 100
MAX_COMBAT_DAMAGE = 999
AI_BROADCAST_PERIOD = config.GetDouble('smooth-lag', 0.2) * 0.9
AI_MOVEMENT_PERIOD = AI_BROADCAST_PERIOD * 0.9
AI_EXAMINE_EVERY = config.GetInt('ai-examine-every', 2)
IDLES_DONT_EXAMINE = [
 VILLAGER_TEAM, PLAYER_TEAM]
COLL_MODE_NONE = 0
COLL_MODE_FLOORS_CL = 1
COLL_MODE_INTERACT = 2
COLL_MODE_FLOORS_AI = 4
COLL_MODE_ALL = COLL_MODE_FLOORS_CL | COLL_MODE_INTERACT | COLL_MODE_FLOORS_AI
TestZone = 1000
FakeZoneId = 999999
InstanceUberShard = 200000000
InstanceUberZone = 10
ShardInterestZone = 2
InventoryZone = 2
IslandAvailableZoneStart = 110
IslandAvailableZoneEnd = 499
IslandConnectorZoneStart = 100
IslandConnectorZoneEnd = 200
IslandShipDeployerZone = 102
IslandLocalZone = 101
InteriorDoorZone = 100
TeleportZone = 500
TargetBitmask = BitMask32.bit(5)
GoldBitmask = BitMask32.bit(6)
ShipFloorBitmask = BitMask32.bit(7)
ShipCollideBitmask = BitMask32.bit(8)
ShipDeployBitmask = BitMask32.bit(12)
SelectBitmask = BitMask32.bit(13)
AIInteractBitmask = BitMask32.bit(14)
AIInteractLocBitmask = BitMask32.bit(15)
BattleAimBitmask = BitMask32.bit(16)
RadarAvatarBitmask = BitMask32.bit(17)
RadarShipBitmask = BitMask32.bit(18)
GenericShipBitmask = BitMask32.bit(19)
ZoneLODBitmask = BitMask32.bit(30)
BattleAimOccludeBitmask = BitMask32.bit(23)
ShipAvoidBitmask = BitMask32.bit(25)
WaterBitmask = BitMask32.bit(26)
ShipCameraBarrierBitmask = BitMask32.bit(27)
CollisionZoneBitmask = BitMask32.bit(28)
SilhouetteZoneDist = 5500
DistanceZoneDist = 3000
DetailsZoneDist = 1000
OnDeckZoneDist = 500
ShipZoneSilhouette = InventoryCategory.SHIP_MAINPARTS
ShipZoneDistance = InventoryCategory.SHIP_ACCESSORIES
ShipZoneDetails = 1000
ShipZoneOnDeck = 500
ShipZones = [OnDeckZoneDist, DetailsZoneDist, DistanceZoneDist, SilhouetteZoneDist]
COLL_AV = 1
COLL_SEA = 2
COLL_LAND = 3
COLL_BLDG = 4
COLL_WOOD = 5
COLL_SHIPPART = 9
COLL_DESTRUCTIBLE = 10
COLL_PORT = 11
COLL_EXIT = 12
COLL_MONSTER = 13
COLL_GRAPPLE_TARGET = 14
COLL_SHIP_WRECK = 15
COLL_SHIP = 16
COLL_CANNON = 17
COLL_FORT = 18
COLL_BLOCKER = 19
COLL_NEWSHIP = 20
COLL_DEFENSE_AMMO = 21
COLL_FLAMING_BARREL = 22
COLL_KRAKEN = 23
COLL_MONSTROUS = 24
SURFACE_DEFAULT = 0
SURFACE_GRASS = 1
SURFACE_SAND = 2
SURFACE_ROCK = 3
SURFACE_WOOD = 4
SURFACE_WATER = 5
SURFACE_CAVE = 6
SURFACE_GRAVEL = 7
SURFACE_WATERWALK = 8
OriginalCameraFov = 30.0
DefaultCameraFov = 50.0
CannonCameraFov = 50.0
SteeringCameraFov = 60.0
BattleCameraFov = 50.0
MakeAPirateCameraFov = 27.0
DefaultCameraFar = 50000.0
DefaultCameraNear = 1.0
DisconnectUnknown = 0
DisconnectBookExit = 1
DisconnectCloseWindow = 2
DisconnectPythonError = 3
DisconnectSwitchShards = 4
DisconnectGraphicsError = 5
DatabaseDialogTimeout = 20.0
DatabaseGiveupTimeout = 45.0
FloorOffset = 0.025
InterfaceOutlineFont = None
PirateFont = None
PirateOutlineFont = None
PirateBoldFont = None
PirateBoldOutlineFont = None

def getInterfaceOutlineFont():
    global InterfaceOutlineFont
    if InterfaceOutlineFont == None:
        if InterfaceOutlineFontPath == None:
            InterfaceOutlineFont = TextNode.getDefaultFont()
        else:
            InterfaceOutlineFont = loader.loadFont(InterfaceOutlineFontPath, lineHeight=1.0)
            if not InterfaceOutlineFont.isValid():
                InterfaceOutlineFont = TextNode.getDefaultFont()
    return InterfaceOutlineFont


def setInterfaceOutlineFont(path):
    global InterfaceOutlineFont
    global InterfaceOutlineFontPath
    InterfaceOutlineFontPath = path
    InterfaceOutlineFont = None
    return


def getPirateFont():
    global PirateFont
    if PirateFont == None:
        if PirateFontPath == None:
            PirateFont = TextNode.getDefaultFont()
        else:
            PirateFont = loader.loadFont(PirateFontPath, lineHeight=1.0)
            if not PirateFont.isValid():
                PirateFont = TextNode.getDefaultFont()
    return PirateFont


def setPirateFont(path):
    global PirateFont
    global PirateFontPath
    PirateFontPath = path
    PirateFont = None
    return


def getPirateOutlineFont():
    global PirateOutlineFont
    if PirateOutlineFont == None:
        if PirateOutlineFontPath == None:
            PirateOutlineFont = TextNode.getDefaultFont()
        else:
            PirateOutlineFont = loader.loadFont(PirateOutlineFontPath, lineHeight=1.0)
            if not PirateOutlineFont.isValid():
                PirateOutlineFont = TextNode.getDefaultFont()
    return PirateOutlineFont


def setPirateOutlineFont(path):
    global PirateOutlineFontPath
    global PirateOutlineFont
    PirateOutlineFontPath = path
    PirateOutlineFont = None
    return


def getPirateBoldOutlineFont():
    global PirateBoldOutlineFont
    if PirateBoldOutlineFont == None:
        if PirateBoldOutlineFontPath == None:
            PirateBoldOutlineFont = TextNode.getDefaultFont()
        else:
            PirateBoldOutlineFont = loader.loadFont(PirateBoldOutlineFontPath, lineHeight=1.0)
            if not PirateBoldOutlineFont.isValid():
                PirateBoldOutlineFont = TextNode.getDefaultFont()
    return PirateBoldOutlineFont


def setPirateBoldOutlineFont(path):
    global PirateBoldOutlineFont
    global PirateBoldOutlineFontPath
    PirateBoldOutlineFontPath = path
    PirateBoldOutlineFont = None
    return


setInterfaceFont(PLocalizer.InterfaceFont)
setInterfaceOutlineFont(PLocalizer.InterfaceOutlineFont)
setSignFont(PLocalizer.SignFont)
setPirateFont(PLocalizer.PirateChippedFont)
setPirateOutlineFont(PLocalizer.PirateChippedOutlineFont)
setPirateBoldOutlineFont(PLocalizer.PirateBoldOutlineFont)
from pirates.piratesgui import PDialog
setDialogClasses(PDialog.PDialog, PDialog.PGlobalDialog)
PirateDialog = None
LogoutHotkey = 'shift-f2'
ScreenshotHotkeyList = ['f9', 'control-f9']
ScreenshotViewerHotkey = 'shift-f9'
MarketingHotkeyList = ['.']
SpeedChatHotkey = '`'
SeaChestHotkey = 'uber-tab'
EscapeHotkey = 'uber-escape'
OptionsHotkey = 'f7'
MinimapHotkey = 'f8'
if config.GetBool('want-dev-hotkeys', 0):
    ShipHotkey = 'f11'
    KrakenHotkey = 'f10'
    SynchronizeHotkey = 'f6'
HideGuiHotkey = 'f12'
TreasureHotkey = 'u'
TreasureHotkey2 = 'shift-u'
GlobalDialogColor = (
 1, 1, 0.75, 1)
DefaultBackgroundColor = (
 0.3, 0.3, 0.3, 1)
DynamicZonesBegin = 61000
DynamicZonesEnd = 1 << 20
ToonStandableGround = 0.707
SPEED_NORMAL_INDEX = 0
SPEED_BATTLE_INDEX = 1
SPEED_FAST_INDEX = 2
SPEED_SLOW_INDEX = 3
SPEED_CARRY_INDEX = 4
SPEED_HEAVY_INDEX = 5
SPEED_NOMOVE_INDEX = 6
PirateSpeeds = [
 (
  24.0, 24.0, 8.0, 120.0), (24.0, 24.0, 8.0, 120.0), (24.0, 24.0, 8.0, 120.0), (6.0, 4.0, 2.5, 33.0), (16.0, 8.0, 8.0, 80.0), (12.0, 8.0, 4.0, 80.0), (0.0, 0.0, 0.0, 0.0)]
ToonForwardFastSpeed = 24.0
ToonJumpFastForce = 24.0
ToonReverseFastSpeed = 8.0
ToonRotateFastSpeed = 120.0
ToonForwardSpeed = 24.0
ToonJumpForce = 24.0
ToonReverseSpeed = 8.0
ToonRotateSpeed = 120.0
ToonForwardBattleSpeed = 24.0
ToonJumpBattleForce = 24.0
ToonReverseBattleSpeed = 8.0
ToonRotateBattleSpeed = 120.0
ToonForwardCarrySpeed = 22.0
ToonJumpCarryForce = 12.0
ToonReverseCarrySpeed = 8.0
ToonRotateCarrySpeed = 120.0
ToonForwardSlowSpeed = 6.0
ToonJumpSlowForce = 4.0
ToonReverseSlowSpeed = 2.5
ToonRotateSlowSpeed = 33.0
STAND_INDEX = 0
WALK_INDEX = 1
RUN_INDEX = 2
REVERSE_INDEX = 3
STRAFE_LEFT_INDEX = 4
STRAFE_RIGHT_INDEX = 5
STRAFE_LEFT_DIAG_INDEX = 6
STRAFE_RIGHT_DIAG_INDEX = 7
STRAFE_LEFT_DIAG_REV_INDEX = 8
STRAFE_RIGHT_DIAG_REV_INDEX = 9
OVER_SOLID_INDEX = 10
OVER_WATER_INDEX = 11
SPIN_LEFT_INDEX = 12
SPIN_RIGHT_INDEX = 13
SWIM_WALK_TRANSITION_TIME = 0.5
AnimScaleTable = {'models/char/mp_walk_gp8': 0.35,'models/char/mp_walk_gp4': 0.35,'models/char/mp_walk': 0.1,'models/char/mp_bayonet_walk': 0.2,'models/char/mp_run_gp8': 0.0971,'models/char/mp_run': 0.03,'models/char/mp_bayonet_run_mtm': 0.03,'models/char/mp_bayonet_run': 0.03,'models/char/mp_run_mtm': 0.03,'models/char/mp_run_mtp': 0.03,'models/char/mp_run_mmi': 0.03}

def GetAnimScale(animName):
    return AnimScaleTable.get(animName)


SPHidden = 0
SPRender = 1
SPShip = 2
TOD_OFF = -1
TOD_DAWN = 0
TOD_DAWN2DAY = 1
TOD_DAY = 2
TOD_DAY2DUSK = 3
TOD_DUSK = 4
TOD_DUSK2NIGHT = 5
TOD_NIGHT = 6
TOD_NIGHT2STARS = 7
TOD_STARS = 8
TOD_STARS2DAWN = 9
TOD_DAY2STORM = 10
TOD_SWAMP = 11
TOD_HALLOWEEN = 12
TOD_FULLMOON = 13
TOD_HALFMOON = 14
TOD_HALFMOON2 = 15
TOD_CUSTOM = 16
TOD_JOLLYINVASION = 17
TOD_NORMAL2JOLLY = 18
TOD_JOLLY2NIGHT = 19
TOD_JOLLY2CURSED = 20
TOD_BASE = 21
TOD_ALL = (
 TOD_DAWN, TOD_DAWN2DAY, TOD_DAY, TOD_DAY2DUSK, TOD_DUSK, TOD_DUSK2NIGHT, TOD_NIGHT, TOD_NIGHT2STARS, TOD_STARS, TOD_STARS2DAWN)
TOD_REALSECONDS_PER_GAMEDAY = 3600.0
TOD_GAMEHOURS_IN_GAMEDAY = 24.0
TUT_STARTED = 0
TUT_GOT_SEACHEST = 1
TUT_GOT_CUTLASS = 2
TUT_MET_JOLLY_ROGER = 3
TUT_KILLED_1_SKELETON = 5
TUT_GOT_COMPASS = 6
TUT_GOT_SHIP = 7
TUT_GOT_PISTOL = 8
TUT_CHAPTER3_STARTED = 9
TUT_INTRODUCTION_TO_CHAT = 10
TUT_INTRODUCTION_TO_FRIENDS = 11
TUT_FINISHED = 12
AI_CANNON_HEADING_RANGE = 45
AI_CANNON_DIST_RANGE = 3500
AI_FORT_CANNON_HEADING_RANGE = 75
AI_FORT_CANNON_DIST_RANGE = 7500
CANNON_FIRING_DELAY = 1
CANNON_STATE_NORMAL = 0
CANNON_STATE_DESTRUCT = 1
NPC_DELETE_MSG = 'npcDeleted'
AVATAR_DEATH_MSG = 'death'
AVATAR_KICK_MSG = 'kick'
AVATAR_DEFEAT_MSG = 'defeat'
AVATAR_DOCK_MSG = 'dock'
AVATAR_AREA_LEAVE_MSG = 'gameAreaLeft'
SHIP_SINKING_MSG = 'shipSinking'
SHIP_DOCKED_MSG = 'shipDocked'
SHIP_HIT_MSG = 'shipHit'
SHIP_OFFLINE_MSG = 'shipExited'
SHIP_ONLINE_MSG = 'shipEntered'
NPC_HIT_MSG = 'npcHit'
NPC_DEATH_BY_AVATARS_MSG = 'npcDeathByAvatars'
EVENT_SPHERE_PORT = 'ES_PORT'
EVENT_SPHERE_CAPTURE = 'ES_CAPTURE'
EVENT_SPHERE_SNEAK = 'ES_SNEAK'
EVENT_SPHERE_DOCK = 'ES_DOCK'
LOCATION_SPHERE = 'LOC_SPHERE'
SPHERE_ENTER_SUFFIX = '_ENTER'
SPHERE_EXIT_SUFFIX = '_EXIT'
IslandPos = [
 (
  -750, 0, 0, 90, 0, 0), (750, 0, 0, -90, 0, 0), (0, 750, 0, 0, 0, 0), (0, -750, 0, 180, 0, 0)]
NumIslands = [
 2, 2, 4]
IslandTeams = [[0, -1], [0, 1], [0, 1, 2, 3]]
LOC_PIRATES = '12345'
INSTANCE_NONE = 0
INSTANCE_GENERIC = 1
INSTANCE_MAIN = 2
INSTANCE_MAINSUB = 3
INSTANCE_TM = 4
INSTANCE_PG = 5
INSTANCE_TUTORIAL = 6
INSTANCE_PVP = 7
INSTANCE_LOBBY = 8
INSTANCE_WELCOME = 9
INSTANCE_DEFENDMINIGAME = 10
INSTANCE_SPECIFIC = 11
INSTANCE_SCRIMMAGE = 12
SHARD_MAIN = 1
SHARD_LOW_LATENCY = 2
SHARD_WELCOME = 3
INSTANCE_NO_NEWS_MESSAGES = [
 INSTANCE_TM, INSTANCE_PG, INSTANCE_TUTORIAL, INSTANCE_PVP]
LowLatencyInstanceTypes = (
 INSTANCE_PVP,)
PARLORGAME_VARIATION_NORMAL = 0
PARLORGAME_VARIATION_UNDEAD = 1
PARLORGAME_UNDEAD_HPFACTOR = 1.0
PARLORGAME_UNDEAD_EXIT_LOSS = 500
GAME_TYPE_PRIV = 0
GAME_TYPE_PVP = 1
GAME_TYPE_CREW = 2
GAME_TYPE_QUEST = 3
GAME_TYPE_PG = 4
GAME_TYPE_TM = 5
GAME_TYPE_HSA = 6
GAME_STYLE_ANY = 1
GAME_STYLE_BATTLE = 0
GAME_STYLE_TEAM_BATTLE = 2
GAME_STYLE_SHIP_BATTLE = 3
GAME_STYLE_CTF = 4
GAME_STYLE_CTL = 5
GAME_STYLE_PIRATEER = 6
GAME_STYLE_ARMADA = 7
GAME_STYLE_TKP = 8
GAME_STYLE_BTB = 9
GAME_STYLE_POKER = 10
GAME_STYLE_BLACKJACK = 11
GAME_STYLE_MAX = 12
CREW_STYLE_FIND_A_CREW = 13
CREW_STYLE_RECRUIT_MEMBERS = 15
CREW_STYLE_FIND_A_PVP_CREW = 14
GAME_STYLE_TM_ANY = GAME_STYLE_ANY
GAME_STYLE_TM_BLACK_PEARL = 0
DYNAMIC_GAME_STYLE_PROPS = {GAME_TYPE_TM: {GAME_STYLE_TM_BLACK_PEARL: {'Name': PLocalizer.BlackPearlTMName,'Desc': PLocalizer.BlackPearlTMDesc,'MapName': 'BlackpearlWorld','NumPlayers': [2, 12]},GAME_STYLE_ANY: {'Name': PLocalizer.AnyTMName,'Desc': '','MapName': ''}}}
LOOKOUT_INVITE_NONE = 0
LOOKOUT_INVITE_CREW = 1
LOOKOUT_INVITE_GUILD = 2
LOOKOUT_INVITE_FRIENDS = 3
LOOKOUT_JOIN_TIMEOUT = 30
LOOKOUT_JOIN_TIMEOUT_INVITE = 90
AvatarDetailsEvent = 'avatarDetailsEvent'
PlayerDetailsEvent = 'playerDetailsEvent'
GuildMakeEvent = 'guildMakeEvent'
GuildAddEvent = 'guildAddEvent'
GuildInvitationEvent = 'guildInvitationEvent'
FriendMakeEvent = 'friendMakeEvent'
FriendAddEvent = 'friendAddEvent'
FriendSecretAddEvent = 'friendSecretAddEvent'
FriendRemoveEvent = 'friendRemoveEvent'
FriendOnlineEvent = 'friendOnlineEvent'
FriendOfflineEvent = 'friendOfflineEvent'
FriendRejectInviteEvent = 'friendRejectInviteEvent'
FriendRetractInviteEvent = 'friendRetractInviteEvent'
FriendInvitationEvent = 'friendInvitationEvent'
FriendNewSecretEvent = 'friendNewSecretEvent'
FriendRejectNewSecretEvent = 'friendRejectNewSecretEvent'
FriendToSecretFriendEvent = 'friendToSecretFriendEvent'
FriendRejectUseSecretEvent = 'friendRejectUseSecretEvent'
MaxPirateFriends = 100
PVPAcceptEvent = 'challengeAccept'
PVPRejectEvent = 'challengeReject'
PVPChallengeEvent = 'challengeReceived'
PVPChallengedEvent = 'challengedReceived'
PVPAcceptedEvent = 'challengeAccepted'
MaxCrew = 6
TradeCreatedEvent = 'tradeCreatedEvent'
TradeRequestEvent = 'tradeRequestEvent'
TradeIncomingEvent = 'tradeIncomingEvent'
TradeFinishedEvent = 'tradeFinishedEvent'
TradeChangedEvent = 'tradeChangedEvent'
TradeRejectInviteEvent = 'tradeRejectInviteEvent'
TREASURE_SURFACE = 0
TREASURE_BURIED = 1
TREASURE_BANK = 2
TREASURE_WRECK = 3
WITHDRAW_NONE = 0
WITHDRAW_LUMP_SUM = 1
WITHDRAW_INCREMENTAL = 2
HIGHSEAS_ADV_WAIT = 1
HIGHSEAS_ADV_START = 2
TM_SELECTION_TIMER = 3
SHIP_SELECTION_TIMER = 4
SHIP_BOARD_TIMER = 5
SHIP_STAGING_TIMER = 6
DOOR_CLOSED = 0
DOOR_OPEN = 1
INTERACT_TYPE_FRIENDLY = 0
INTERACT_TYPE_HOSTILE = 1
INTERACT_TYPE_S2SBOARD = 2
S2SBOARD_SUCCESS_MSG = 'S2SBoarding complete-'

def teamStr2TeamId(typeStr, defaultTeam=PLAYER_TEAM):
    team = defaultTeam
    if typeStr == NAVY_TEAM_STR:
        team = NAVY_TEAM
    elif typeStr == UNDEAD_TEAM_STR:
        team = UNDEAD_TEAM
    elif typeStr == PLAYER_TEAM_STR:
        team = PLAYER_TEAM
    elif typeStr == VILLAGER_TEAM_STR:
        team = VILLAGER_TEAM
    elif typeStr == TUTORIAL_ENEMY_TEAM_STR:
        team = TUTORIAL_ENEMY_TEAM
    elif typeStr == SPANISH_UNDEAD_TEAM_STR:
        team = SPANISH_UNDEAD_TEAM_STR
    elif typeStr == FRENCH_UNDEAD_TEAM_STR:
        team = FRENCH_UNDEAD_TEAM_STR
    return team


SearchableCrate = 'Crate'
SearchableBarrel = 'Barrel'
SearchableCabinet = 'Cabinet'
SearchableBookshelf = 'Bookshelf'
SearchableClock = 'Clock'
SearchableDesk = 'Desk'
SearchableHaystack = 'Haystack'
SearchableWellA = 'WellA'
SearchableStove = 'Stove'
SearchableModels = {SearchableCrate: 'models/props/crate_04',SearchableBarrel: 'models/props/barrel',SearchableCabinet: 'models/props/cabinet_fancy_low',SearchableBookshelf: 'models/props/bookshelf_fancy',SearchableClock: 'models/props/clock_fancy_tall',SearchableDesk: 'models/props/desk_gov',SearchableHaystack: 'models/props/haystack',SearchableHaystack: 'models/props/haystack',SearchableWellA: 'models/props/wellA',SearchableStove: 'models/props/stove_potbelly'}
QUEST_PROP_AZT_IDOL_A_DESTR = 'azt_idol_a_destr'
QUEST_PROP_AZT_IDOL_B_DESTR = 'azt_idol_b_destr'
QUEST_PROP_AZT_SKELETON_A_DESTR = 'azt_skeleton_a_destr'
QUEST_PROP_AZT_SKELETON_B_DESTR = 'azt_skeleton_b_destr'
QUEST_PROP_WPN_AMMOPILE = 'wpn_ammopile'
QUEST_PROP_ROK_RUBBLE_DIGSPOT = 'rok_rubble_digspot'
QUEST_PROP_ROK_RUBBLE_TUNNEL = 'rok_rubble_tunnel'
QUEST_PROP_WPN_WEAPONRACK = 'wpn_weaponrack'
QUEST_PROP_LIT_TORCHSTAND = 'lit_torchstand'
QUEST_PROP_CEM_TOMB_INTER = 'cem_tomb_inter'
QUEST_PROP_CAV_WEBWALL = 'cav_webwall'
QUEST_PROP_FRT_TENT_NAVY = 'frt_tent_navy'
QUEST_PROP_BON_SKULL_SHRINE = 'bon_skullShrine'
QUEST_PROP_SET_CHAIR_DESTR = 'set_chair_destr'
QUEST_PROP_ENM_HIVE_SCORPION = 'enm_hive_scorpion'
QUEST_PROP_ENM_HIVE_WASP = 'enm_hive_wasp'
QUEST_PROP_FRM_PEN_LIVESTOCK = 'frm_pen_livestock'
QUEST_PROP_SHP_WRK_GALLEON = 'shp_wrk_galleon'
QUEST_PROP_SHP_WRK_MAST_A = 'shp_wrk_mastA'
QUEST_PROP_SHP_WRK_MAST_B = 'shp_wrk_mastB'
QUEST_PROP_SHP_WRK_MAST_C = 'shp_wrk_mastC'
QUEST_PROP_OCN_ROCK_A = 'ocn_rock_a'
QUEST_PROP_OCN_ROCK_B = 'ocn_rock_b'
QUEST_PROP_OCN_ROCK_C = 'ocn_rock_c'
QUEST_PROP_OCN_ROCK_D = 'ocn_rock_d'
QUEST_PROP_OCN_ROCK_E = 'ocn_rock_e'
QUEST_PROP_OCN_ROCK_F = 'ocn_rock_f'
QUEST_PROP_OCN_FORTISLAND = 'ocn_fortisland'
QUEST_PROP_CAV_FORTDOOR = 'cav_fortdoor'
QUEST_PROP_OCN_WATCHTOWER_EITC = 'ocn_watchtower_eitc'
QUEST_PROP_OCN_WATCHTOWER_NAVY = 'ocn_watchtower_navy'
QUEST_PROP_FRT_CAGE_INTER = 'frt_cage_inter'
QUEST_PROP_CEM_COFFIN_INTER = 'cem_coffin_inter'
QUEST_PROP_TOL_SLEDGE = 'tol_sledge'
QUEST_PROP_VOO_CRYSTALBALL = 'voo_crystalball'
QUEST_PROP_HSW_BOTTLE_DESTR = 'hsw_bottle_destr'
QUEST_PROP_SET_BENCH_DESTR = 'set_bench_destr'
QUEST_PROP_FRM_SUGARCANE = 'frm_sugarcane'
QUEST_PROP_POWDER_KEG = 'powder_keg'
QUEST_PROP_DIG_SPOT = 'dig_spot'
QUEST_PROP_MNG_ELEVATOR_BASKET = 'mng_elevator_basket'
QUEST_PROP_TRS_CHEST_02 = 'trs_chest_02'
QUEST_PROP_CAV_DOOR_EL_PATRON = 'cav_door_elPatron'
QUEST_PROP_SHP_GANGPLANK_RAILS_WEATHERED = 'models/props/pir_m_prp_shp_gangplankRails_weathered'
QUEST_PROP_MODELS = {QUEST_PROP_AZT_IDOL_A_DESTR: 'models/props/pir_r_prp_azt_idol_a_destructible',QUEST_PROP_AZT_IDOL_B_DESTR: 'models/props/pir_r_prp_azt_idol_b_destructible',QUEST_PROP_AZT_SKELETON_A_DESTR: 'models/props/pir_r_prp_azt_skeleton_a_destructible',QUEST_PROP_AZT_SKELETON_B_DESTR: 'models/props/pir_r_prp_azt_skeleton_b_destructible',QUEST_PROP_WPN_AMMOPILE: 'models/props/pir_m_prp_wpn_ammoPile',QUEST_PROP_ROK_RUBBLE_DIGSPOT: 'models/props/pir_m_prp_rok_rubble_digspot',QUEST_PROP_ROK_RUBBLE_TUNNEL: 'models/props/pir_m_prp_rok_rubble_tunnel',QUEST_PROP_WPN_WEAPONRACK: 'models/props/pir_m_prp_wpn_weaponRack',QUEST_PROP_LIT_TORCHSTAND: 'models/props/pir_m_prp_lit_torchStand',QUEST_PROP_CEM_TOMB_INTER: 'models/props/pir_r_prp_cem_tomb_interact',QUEST_PROP_CAV_WEBWALL: 'models/props/pir_m_prp_cav_webWall',QUEST_PROP_FRT_TENT_NAVY: 'models/props/pir_m_prp_frt_tent_navy',QUEST_PROP_BON_SKULL_SHRINE: 'models/props/pir_r_prp_bon_skullShrine_destructible',QUEST_PROP_SET_CHAIR_DESTR: 'models/props/pir_m_prp_set_chair_destructible',QUEST_PROP_ENM_HIVE_SCORPION: 'models/props/pir_m_prp_enm_hive_scorpion',QUEST_PROP_ENM_HIVE_WASP: 'models/props/pir_m_prp_enm_hive_wasp',QUEST_PROP_FRM_PEN_LIVESTOCK: 'models/props/pir_m_prp_frm_pen_livestock',QUEST_PROP_SHP_WRK_GALLEON: 'models/props/pir_m_shp_wrk_galleon',QUEST_PROP_SHP_WRK_MAST_A: 'models/props/pir_m_shp_wrk_mastA',QUEST_PROP_SHP_WRK_MAST_B: 'models/props/pir_m_shp_wrk_mastB',QUEST_PROP_SHP_WRK_MAST_C: 'models/props/pir_m_shp_wrk_mastC',QUEST_PROP_OCN_ROCK_A: 'models/props/pir_m_prp_ocn_rock_a',QUEST_PROP_OCN_ROCK_B: 'models/props/pir_m_prp_ocn_rock_b',QUEST_PROP_OCN_ROCK_C: 'models/props/pir_m_prp_ocn_rock_c',QUEST_PROP_OCN_ROCK_D: 'models/props/pir_m_prp_ocn_rock_d',QUEST_PROP_OCN_ROCK_E: 'models/props/pir_m_prp_ocn_rock_e',QUEST_PROP_OCN_ROCK_F: 'models/props/pir_m_prp_ocn_rock_f',QUEST_PROP_OCN_FORTISLAND: 'models/props/pir_m_prp_ocn_fortIsland',QUEST_PROP_CAV_FORTDOOR: 'models/props/pir_m_prp_cav_fortDoor',QUEST_PROP_OCN_WATCHTOWER_EITC: 'models/props/pir_m_prp_ocn_watchtower_eitc',QUEST_PROP_OCN_WATCHTOWER_NAVY: 'models/props/pir_m_prp_ocn_watchtower_navy',QUEST_PROP_FRT_CAGE_INTER: 'models/props/pir_r_prp_frt_cage_interact',QUEST_PROP_CEM_COFFIN_INTER: 'models/props/pir_r_prp_cem_coffin_interact',QUEST_PROP_TOL_SLEDGE: 'models/props/pir_m_hnd_tol_sledge',QUEST_PROP_VOO_CRYSTALBALL: 'models/props/pir_m_prp_voo_crystalBall',QUEST_PROP_HSW_BOTTLE_DESTR: 'models/props/pir_m_prp_hsw_bottle_destructible',QUEST_PROP_SET_BENCH_DESTR: 'models/props/pir_m_prp_set_bench_destructible',QUEST_PROP_FRM_SUGARCANE: 'models/props/pir_m_prp_frm_sugarCane',QUEST_PROP_POWDER_KEG: 'models/handheld/pir_m_hnd_bom_barrelDynamite',QUEST_PROP_DIG_SPOT: 'models/misc/smiley',QUEST_PROP_MNG_ELEVATOR_BASKET: 'models/props/pir_m_prp_mng_elevator_basket',QUEST_PROP_TRS_CHEST_02: 'models/props/pir_m_prp_trs_chest_02',QUEST_PROP_CAV_DOOR_EL_PATRON: 'models/props/pir_m_prp_cav_door_elPatron',QUEST_PROP_SHP_GANGPLANK_RAILS_WEATHERED: 'models/props/pir_m_prp_shp_gangplankRails_weathered'}
QUEST_PROP_ANIMS = {QUEST_PROP_AZT_IDOL_A_DESTR: {'break': 'models/props/pir_a_prp_azt_idol_a_destructible_break'},QUEST_PROP_AZT_IDOL_B_DESTR: {'break': 'models/props/pir_a_prp_azt_idol_b_destructible_break'},QUEST_PROP_AZT_SKELETON_A_DESTR: {'break': 'models/props/pir_a_prp_azt_skeleton_a_destructible_break'},QUEST_PROP_AZT_SKELETON_B_DESTR: {'break': 'models/props/pir_a_prp_azt_skeleton_b_destructible_break'},QUEST_PROP_CEM_TOMB_INTER: {'open': 'models/props/pir_a_prp_cem_tomb_open'},QUEST_PROP_BON_SKULL_SHRINE: {'break': 'models/props/pir_a_prp_bon_skullShrine_break'}}
TFFlag = 0
TFPlayerConfirm = BitMask32.bit(TFFlag)
TFFlag += 1
TFPhaseIncomplete = BitMask32.bit(TFFlag)
TFFlag += 1
TFVelvetRope = BitMask32.bit(TFFlag)
TFFlag += 1
TFInTutorial = BitMask32.bit(TFFlag)
TFFlag += 1
TFNoCompass = BitMask32.bit(TFFlag)
TFFlag += 1
TFInjured = BitMask32.bit(TFFlag)
TFFlag += 1
TFInJail = BitMask32.bit(TFFlag)
TFFlag += 1
TFNoIslandToken = BitMask32.bit(TFFlag)
TFFlag += 1
TFInPVP = BitMask32.bit(TFFlag)
TFFlag += 1
TFParlorGame = BitMask32.bit(TFFlag)
TFFlag += 1
TFTreasureMap = BitMask32.bit(TFFlag)
TFFlag += 1
TFFlagshipBattle = BitMask32.bit(TFFlag)
TFFlag += 1
TFInBattle = BitMask32.bit(TFFlag)
TFFlag += 1
TFOnShip = BitMask32.bit(TFFlag)
TFFlag += 1
TFNotSameCrew = BitMask32.bit(TFFlag)
TFFlag += 1
TFInWater = BitMask32.bit(TFFlag)
TFFlag += 1
TFInTunnel = BitMask32.bit(TFFlag)
TFFlag += 1
TFLookoutJoined = BitMask32.bit(TFFlag)
TFFlag += 1
TFInInitTeleport = BitMask32.bit(TFFlag)
TFFlag += 1
TFInTeleport = BitMask32.bit(TFFlag)
TFFlag += 1
TFUnavailable = BitMask32.bit(TFFlag)
TFFlag += 1
TFSiegeCaptain = BitMask32.bit(TFFlag)
TFFlag += 1
TFIgnore = BitMask32.bit(TFFlag)
TFFlag += 1
TFInWelcomeWorld = BitMask32.bit(TFFlag)
TFFlag += 1
TFZombie = BitMask32.bit(TFFlag)
TFFlag += 1
TFSameArea = BitMask32.bit(TFFlag)
TFFlag += 1
TFFishing = BitMask32.bit(TFFlag)
TFFlag += 1
TFPotionCrafting = BitMask32.bit(TFFlag)
TFFlag += 1
TFCannonDefense = BitMask32.bit(TFFlag)
TFFlag += 1
TFInScrimmage = BitMask32.bit(TFFlag)
TFFlag += 1
del TFFlag
TFNoTeleport = TFInPVP | TFInTeleport | TFInTunnel | TFInTutorial | TFInJail | TFFlagshipBattle | TFInInitTeleport | TFTreasureMap | TFZombie | TFInScrimmage
TFNoTeleportTo = TFNoTeleport | TFIgnore | TFOnShip | TFNotSameCrew | TFInWelcomeWorld | TFCannonDefense
TFNoTeleportOut = TFNoTeleport | TFNoIslandToken | TFInBattle | TFInWater | TFParlorGame | TFFishing | TFNoCompass | TFPhaseIncomplete | TFLookoutJoined | TFVelvetRope | TFSiegeCaptain | TFSameArea | TFInjured | TFPotionCrafting
TFNoTeleportReasons = {TFOnShip: PLocalizer.NoTeleportOnShip,TFNoIslandToken: PLocalizer.NoTeleportIslandToken,TFInBattle: PLocalizer.NoTeleportInBattle,TFInPVP: PLocalizer.NoTeleportInPVP,TFInTutorial: PLocalizer.NoTeleportInTutorial,TFNoCompass: PLocalizer.NoTeleportCompass,TFInTunnel: PLocalizer.NoTeleportInTunnel,TFInTeleport: PLocalizer.NoTeleportInTeleport,TFInInitTeleport: PLocalizer.NoTeleportInTeleport,TFInjured: PLocalizer.NoTeleportInjured,TFInJail: PLocalizer.NoTeleportInJail,TFInWater: PLocalizer.NoTeleportInWater,TFParlorGame: PLocalizer.NoTeleportParlorGame,TFFlagshipBattle: PLocalizer.NoTeleportFlagshipBattle,TFPhaseIncomplete: PLocalizer.NoTeleportPhaseIncomplete,TFLookoutJoined: PLocalizer.NoTeleportLookoutJoined,TFTreasureMap: PLocalizer.NoTeleportTreasureMap,TFSiegeCaptain: PLocalizer.NoTeleportSiegeCaptain,TFZombie: PLocalizer.NoTeleportZombie,TFSameArea: PLocalizer.NoTeleportSameArea,TFFishing: PLocalizer.NoTeleportFishing,TFPotionCrafting: PLocalizer.NoTeleportPotionCrafting,TFInScrimmage: PLocalizer.NoTeleportInScrimmage}
TFNoTeleportToReasons = {TFUnavailable: PLocalizer.NoTeleportToUnavailable,TFInPVP: PLocalizer.NoTeleportToInPVP,TFInTutorial: PLocalizer.NoTeleportToInTutorial,TFInTunnel: PLocalizer.NoTeleportToInTunnel,TFInTeleport: PLocalizer.NoTeleportToInTeleport,TFInInitTeleport: PLocalizer.NoTeleportToInTeleport,TFInJail: PLocalizer.NoTeleportToInJail,TFFlagshipBattle: PLocalizer.NoTeleportToFlagshipBattle,TFIgnore: PLocalizer.NoTeleportToIgnore,TFNotSameCrew: PLocalizer.NoTeleportToNoPermission,TFOnShip: PLocalizer.NoTeleportToNoSpaceOnShip,TFTreasureMap: PLocalizer.NoTeleportToTreasureMap,TFInWelcomeWorld: PLocalizer.NoTeleportToWelcomeWorld,TFZombie: PLocalizer.NoTeleportToZombie,TFCannonDefense: PLocalizer.NoTeleportCannonDefense,TFInScrimmage: PLocalizer.NoTeleportToInScrimmage}

def encodeTeleportFlag(flag):
    return flag.getHighestOnBit() + 1


def decodeTeleportFlag(available):
    return BitMask32.bit(available - 1)


TAAvailable = 0
TALater = 1
TAIgnore = 2
buf = [
 '        ', '        ']
nicknamesMale = PL.PirateNames_NickNamesGeneric + PL.PirateNames_NickNamesMale
nicknamesFemale = PL.PirateNames_NickNamesGeneric + PL.PirateNames_NickNamesFemale
firstNamesMale = PL.PirateNames_FirstNamesGeneric + PL.PirateNames_FirstNamesMale
firstNamesFemale = PL.PirateNames_FirstNamesGeneric + PL.PirateNames_FirstNamesFemale
lastPrefixesMale = PL.PirateNames_LastNamePrefixesGeneric + PL.PirateNames_LastNamePrefixesCapped + PL.PirateNames_LastNamePrefixesMale
lastPrefixesFemale = PL.PirateNames_LastNamePrefixesGeneric + PL.PirateNames_LastNamePrefixesCapped + PL.PirateNames_LastNamePrefixesFemale
lastSuffixesMale = PL.PirateNames_LastNameSuffixesGeneric + PL.PirateNames_LastNameSuffixesMale
lastSuffixesFemale = PL.PirateNames_LastNameSuffixesGeneric + PL.PirateNames_LastNameSuffixesFemale
nicknamesMale.sort()
nicknamesFemale.sort()
firstNamesMale.sort()
firstNamesFemale.sort()
lastPrefixesMale.sort()
lastPrefixesFemale.sort()
lastSuffixesMale.sort()
lastSuffixesFemale.sort()
nicknamesMale = buf + nicknamesMale + buf
nicknamesFemale = buf + nicknamesFemale + buf
firstNamesMale = buf + firstNamesMale + buf
firstNamesFemale = buf + firstNamesFemale + buf
lastPrefixesMale = buf + lastPrefixesMale + buf
lastPrefixesFemale = buf + lastPrefixesFemale + buf
lastSuffixesMale = buf + lastSuffixesMale + buf
lastSuffixesFemale = buf + lastSuffixesFemale + buf
del buf
maleNames = [[], firstNamesMale[:], lastPrefixesMale[:], lastSuffixesMale[:]]
femaleNames = [[], firstNamesFemale[:], lastPrefixesFemale[:], lastSuffixesFemale[:]]
lastNamePrefixesCapped = PL.PirateNames_LastNamePrefixesCapped[:]
TreasureMapReadyTimeout = 45
DEFAULT_AMBIENT_VOLUME = 1.0
DEFAULT_AMBIENT_VOLUME_FAINT = DEFAULT_AMBIENT_VOLUME * 0.25
DEFAULT_AMBIENT_VOLUME_MIDDLE = DEFAULT_AMBIENT_VOLUME * 0.5
DEFAULT_AMBIENT_VOLUME_NEAR = DEFAULT_AMBIENT_VOLUME * 0.75
treasureCarryTransforms = {'m': [TransformState.makePosHprScale(Vec3(0.05, 0, -1.1), Vec3(0, 0, -90), Vec3(0.5, 0.5, 0.5)), TransformState.makePosHprScale(Vec3(0.05, 0, -0.97), Vec3(0, 0, -90), Vec3(0.47, 0.47, 0.47)), TransformState.makePosHprScale(Vec3(0.05, 0, -1.12), Vec3(0, 0, -90), Vec3(0.53, 0.53, 0.53)), TransformState.makePosHprScale(Vec3(0.05, 0, -1.03), Vec3(0, 0, -90), Vec3(0.48, 0.48, 0.48)), TransformState.makePosHprScale(Vec3(0.05, 0, -1.3), Vec3(0, 0, -90), Vec3(0.63, 0.63, 0.63))],'f': [TransformState.makePosHprScale(Vec3(0.05, 0, -0.97), Vec3(0, 0, -90), Vec3(0.47, 0.47, 0.47)), TransformState.makePosHprScale(Vec3(0.05, 0, -0.97), Vec3(0, 0, -90), Vec3(0.47, 0.47, 0.47)), TransformState.makePosHprScale(Vec3(0.05, 0, -0.97), Vec3(0, 0, -90), Vec3(0.47, 0.47, 0.47)), TransformState.makePosHprScale(Vec3(-0.1, 0, -0.97), Vec3(0, 0, -90), Vec3(0.42, 0.42, 0.42)), TransformState.makePosHprScale(Vec3(0.05, 0, -0.97), Vec3(0, 0, -90), Vec3(0.47, 0.47, 0.47))]}
treasureSwimTransform = TransformState.makePosHprScale(Vec3(0, 0, 5), Vec3(0, 0, 0), Vec3(0.5, 0.5, 0.5))
PORT_ROYAL_DEFAULTS = 100
PORT_ROYAL_ALL = 101
PRIVATEER_TATTOOS = 102
PORT_ROYAL_THRIFT = 102
PRIVATEER_HATS = 103
PRIVATEER_COATS = 104
TORTUGA_DEFAULTS = 200
CUBA_DEFAULTS = 300
DEL_FUEGO_DEFAULTS = 400
SHIP_PVP_HELP_FRENCH_A = 1
SHIP_PVP_HELP_SPAINISH_A = 2
SHIP_PVP_HELP_FRENCH_B = 3
SHIP_PVP_HELP_SPAINISH_B = 4
MaxFriends = 300
ExamineSurroundingsCTravName = 'examineSurroundings'
XP_HOLIDAY_START = 1
XP_HOLIDAY_END = 2
BLACKJACK_FRIDAY_START = 1
BLACKJACK_FRIDAY_END = 2
QRFlag = 0
QRFlagMainStory = BitMask32.bit(QRFlag)
del QRFlag
SkillToQRFlagMapping = {12661: QRFlagMainStory}
WARDROBE_LIMIT_JEWELER = 4
WARDROBE_LIMIT_TAILOR = 4
WARDROBE_LIMIT_TATTOO = 4
STATUS_AFK = 1
STATUS_LFG = 2

def getShardTypeFromInstance(instanceType):
    if instanceType in LowLatencyInstanceTypes:
        return SHARD_LOW_LATENCY
    elif instanceType == INSTANCE_TUTORIAL or instanceType == INSTANCE_WELCOME:
        return SHARD_WELCOME
    else:
        return SHARD_MAIN


ShipPVPFrench = 0
ShipPVPSpanish = 1
ShipPVPSiege = 0
ShipPVPShip = 0
ShipPVPPirate = 1
ShipPVPKillCannon = 0
ShipPVPKillShip = 1
PrivateerBothTeamFull = 0
PrivateerSingleTeamFull = 1
ZombieNoBoats = 2
ShipNeedCompass = 3
TIME_TO_REVIVE = 15.0
REVIVE_TIME_OUT = 60.0
ITEM_SAC = 4
TREASURE_CHEST = 5
RARE_CHEST = 6
UPGRADE_CHEST = 7
RARE_UPGRADE_CHEST = 8
SPT_DEFAULT = -1
SPT_TUTORIAL = 0
SPT_DINGHY = 1
REWARD_GOLD = 0
REWARD_WEAPONS = 1
REWARD_AMMO = 2
REWARD_CLOTHING = 3
TD_LOW = 0
TD_MED = 1
TD_HIGH = 2
CD_LOW = 0
CD_MED = 1
CD_HIGH = 2
INVIS_VISZONE = BitMask32.bit(0)
INVIS_DEATH = BitMask32.bit(1)
INVIS_CAMERA = BitMask32.bit(2)
INVIS_QUEST = BitMask32.bit(3)
INVIS_DIALOG = BitMask32.bit(4)
INVIS_EFFECIENCY = BitMask32.bit(0)
INVIS_BOARDING = BitMask32.bit(1)
CANNON_DEFENSE_SKILLS = []
DAZED_DURATION = 5.0
DAZED_SHAKEOFF_THRESHOLD = 10
DAZED_BUTTON_INCREMENT = 0.4
ANY_LOCATION_SPAWN_INDEX = -1
START_ISLAND_SPAWN_INDEX = 0
SHIP_DOCKING_SPAWN_INDEX = 1
CANNON_DEFENSE_SPAWN_INDEX = 26
RAVENS_COVE_SPAWN_INDEX = 28
SCRIMMAGE_SPAWN_INDEX = 30

def flattenOrdered(root):
    gr = SceneGraphReducer()
    gr.applyAttribs(root.node())
    num_removed = gr.flatten(root.node(), -1)
    gr.makeCompatibleState(root.node())
    gr.collectVertexData(root.node(), ~(SceneGraphReducer.CVDFormat | SceneGraphReducer.CVDName | SceneGraphReducer.CVDAnimationType))
    gr.unify(root.node(), True)
    return num_removed


INTERACT_TYPES_WITHOUT_FORCE_POS = [
 'barrel_hide']
POPULATION_FACTOR = 0.2
