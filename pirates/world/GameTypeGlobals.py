from pandac.PandaModules import *
import types
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pandac.PandaModules import ConfigVariable
from pirates.uberdog import DistributedInventoryBase
from otp.otpbase import OTPGlobals
GAME_DURATION_SHORT = 0
GAME_DURATION_MED = 1
GAME_DURATION_LONG = 2
GAME_OPTION_DURATION = 0
GAME_OPTION_MATCH_COUNT = 1
GAME_OPTION_PASSWORD = 2
GAME_OPTION_NPC_PLAYERS = 3
GAME_OPTION_LOCATION = 4
GAME_OPTION_USE_CURR_CREW = 5
GAME_OPTION_MIN_BET = 6
GAME_OPTION_MIN_PLAYERS = 7
GAME_OPTION_DESIRED_PLAYERS = 8
GAME_OPTION_MAX_PLAYERS = 9
GAME_OPTION_MAX_CREW_SIZE = 10
GAME_OPTION_MAX_CREW_SHIP = 11
GAME_OPTION_VIP_PASS = 12
GAME_OPTION_CREW_INFO = 13
GAME_OPTION_TM_ID = 14
GAME_OPTION_SOLO_PLAY = 15
MATCH_CHANCE_LOW = 1
MATCH_CHANCE_MODERATE = 25
MATCH_CHANCE_HIGH = 75
GAME_TYPE_2_INSTANCE_TYPE = {PiratesGlobals.GAME_TYPE_PG: PiratesGlobals.INSTANCE_PG,PiratesGlobals.GAME_TYPE_PVP: PiratesGlobals.INSTANCE_PVP,PiratesGlobals.GAME_TYPE_HSA: PiratesGlobals.INSTANCE_MAIN,PiratesGlobals.GAME_TYPE_TM: PiratesGlobals.INSTANCE_TM,PiratesGlobals.GAME_TYPE_CREW: PiratesGlobals.INSTANCE_MAIN,PiratesGlobals.GAME_TYPE_PRIV: PiratesGlobals.INSTANCE_MAIN,PiratesGlobals.GAME_TYPE_QUEST: PiratesGlobals.INSTANCE_MAIN}

def gameType2InstanceType(gameType):
    instanceType = GAME_TYPE_2_INSTANCE_TYPE.get(gameType)
    return instanceType


GameTypeRanking = {PiratesGlobals.GAME_STYLE_CTF: InventoryType.CTFGame,PiratesGlobals.GAME_STYLE_CTL: InventoryType.CTLGame,PiratesGlobals.GAME_STYLE_PIRATEER: InventoryType.PTRGame,PiratesGlobals.GAME_STYLE_BATTLE: InventoryType.BTLGame,PiratesGlobals.GAME_STYLE_TEAM_BATTLE: InventoryType.TBTGame,PiratesGlobals.GAME_STYLE_SHIP_BATTLE: InventoryType.SBTGame,PiratesGlobals.GAME_STYLE_ARMADA: InventoryType.ARMGame,PiratesGlobals.GAME_STYLE_TKP: InventoryType.TKPGame,PiratesGlobals.GAME_STYLE_BTB: InventoryType.BTBGame,PiratesGlobals.GAME_STYLE_BLACKJACK: InventoryType.BlackjackGame,PiratesGlobals.GAME_STYLE_POKER: InventoryType.PokerGame}
GameTypeStrings = {'type': {PiratesGlobals.GAME_TYPE_PVP: PLocalizer.PVPGame,PiratesGlobals.GAME_TYPE_PG: PLocalizer.ParlorGame,PiratesGlobals.GAME_TYPE_HSA: PLocalizer.HSAGame,PiratesGlobals.GAME_TYPE_TM: PLocalizer.TMGame,PiratesGlobals.GAME_TYPE_CREW: PLocalizer.CrewGame,PiratesGlobals.GAME_TYPE_PRIV: PLocalizer.PrivGame,PiratesGlobals.GAME_TYPE_QUEST: PLocalizer.QuestGame},'typeBrief': {PiratesGlobals.GAME_TYPE_PVP: PLocalizer.PVPGameBrief,PiratesGlobals.GAME_TYPE_PG: PLocalizer.ParlorGameBrief,PiratesGlobals.GAME_TYPE_HSA: PLocalizer.HSAGameBrief,PiratesGlobals.GAME_TYPE_TM: PLocalizer.TMGameBrief,PiratesGlobals.GAME_TYPE_CREW: PLocalizer.CrewGameBrief,PiratesGlobals.GAME_TYPE_PRIV: PLocalizer.PrivGameBrief,PiratesGlobals.GAME_TYPE_QUEST: PLocalizer.QuestGameBrief},'description': {PiratesGlobals.GAME_TYPE_PVP: PLocalizer.PVPGameDesc,PiratesGlobals.GAME_TYPE_PG: PLocalizer.ParlorGameDesc,PiratesGlobals.GAME_TYPE_HSA: PLocalizer.HSAGameDesc,PiratesGlobals.GAME_TYPE_TM: PLocalizer.TMGameDesc,PiratesGlobals.GAME_TYPE_CREW: PLocalizer.CrewGameDesc,PiratesGlobals.GAME_TYPE_PRIV: PLocalizer.PrivGameDesc,PiratesGlobals.GAME_TYPE_QUEST: PLocalizer.QuestGameDesc},'descriptionStyle': {PiratesGlobals.GAME_STYLE_BATTLE: PLocalizer.GameStyleBattleDesc,PiratesGlobals.GAME_STYLE_TEAM_BATTLE: PLocalizer.GameStyleTeamBattleDesc,PiratesGlobals.GAME_STYLE_SHIP_BATTLE: PLocalizer.GameStyleShipBattleDesc,PiratesGlobals.GAME_STYLE_CTF: PLocalizer.GameStyleCTFDesc,PiratesGlobals.GAME_STYLE_CTL: PLocalizer.GameStyleCTLDesc,PiratesGlobals.GAME_STYLE_PIRATEER: PLocalizer.GameStylePirateer,PiratesGlobals.GAME_STYLE_POKER: PLocalizer.GameStylePoker,PiratesGlobals.GAME_STYLE_BLACKJACK: PLocalizer.GameStyleBlackjack,PiratesGlobals.CREW_STYLE_FIND_A_CREW: PLocalizer.CrewStyleFindACrewDesc,PiratesGlobals.CREW_STYLE_FIND_A_PVP_CREW: PLocalizer.CrewStyleFindAPVPCrewDesc,PiratesGlobals.CREW_STYLE_RECRUIT_MEMBERS: PLocalizer.CrewStyleRecruitMembersDesc},'icon': {PiratesGlobals.GAME_TYPE_PVP: 'lookout_win_pvp_game_icon',PiratesGlobals.GAME_TYPE_PG: 'lookout_win_parlor_game_icon',PiratesGlobals.GAME_TYPE_HSA: None,PiratesGlobals.GAME_TYPE_TM: 'lookout_win_treasuremap_icon',PiratesGlobals.GAME_TYPE_CREW: 'friend_button',PiratesGlobals.GAME_TYPE_PRIV: 'pir_t_gui_lok_shipPvp',PiratesGlobals.GAME_TYPE_QUEST: None},'iconStyle': {PiratesGlobals.GAME_STYLE_BATTLE: None,PiratesGlobals.GAME_STYLE_TEAM_BATTLE: None,PiratesGlobals.GAME_STYLE_SHIP_BATTLE: None,PiratesGlobals.GAME_STYLE_CTF: None,PiratesGlobals.GAME_STYLE_CTL: None,PiratesGlobals.GAME_STYLE_PIRATEER: None,PiratesGlobals.GAME_STYLE_POKER: None,PiratesGlobals.GAME_STYLE_BLACKJACK: None},'style': {PiratesGlobals.GAME_STYLE_ANY: PLocalizer.AnyGame,PiratesGlobals.GAME_STYLE_CTF: PLocalizer.CTFGame,PiratesGlobals.GAME_STYLE_CTL: PLocalizer.CTLGame,PiratesGlobals.GAME_STYLE_PIRATEER: PLocalizer.PTRGame,PiratesGlobals.GAME_STYLE_BATTLE: PLocalizer.BTLGame,PiratesGlobals.GAME_STYLE_TEAM_BATTLE: PLocalizer.TBTGame,PiratesGlobals.GAME_STYLE_SHIP_BATTLE: PLocalizer.SBTGame,PiratesGlobals.GAME_STYLE_ARMADA: PLocalizer.ARMGame,PiratesGlobals.GAME_STYLE_TKP: PLocalizer.TKPGame,PiratesGlobals.GAME_STYLE_BTB: PLocalizer.BTBGame,PiratesGlobals.GAME_STYLE_BLACKJACK: PLocalizer.BlackjackGame,PiratesGlobals.GAME_STYLE_POKER: PLocalizer.PokerGame,PiratesGlobals.CREW_STYLE_FIND_A_CREW: PLocalizer.FindACrew,PiratesGlobals.CREW_STYLE_FIND_A_PVP_CREW: PLocalizer.FindAPVPCrew,PiratesGlobals.CREW_STYLE_RECRUIT_MEMBERS: PLocalizer.RecruitCrewMembers},'option': {GAME_OPTION_DURATION: PLocalizer.GameDuration,GAME_OPTION_MATCH_COUNT: PLocalizer.GameMatchCount,GAME_OPTION_PASSWORD: PLocalizer.GamePassword,GAME_OPTION_MIN_BET: PLocalizer.GameMinBet,GAME_OPTION_NPC_PLAYERS: PLocalizer.GameNPCPlayers,GAME_OPTION_LOCATION: PLocalizer.GameLocation,GAME_OPTION_USE_CURR_CREW: PLocalizer.GameUseCrew,GAME_OPTION_MIN_PLAYERS: PLocalizer.GameMinPlayers,GAME_OPTION_DESIRED_PLAYERS: PLocalizer.GameDesPlayers,GAME_OPTION_MAX_PLAYERS: PLocalizer.GameMaxPlayers,GAME_OPTION_MAX_CREW_SIZE: PLocalizer.GameMaxCrew,GAME_OPTION_MAX_CREW_SHIP: PLocalizer.GameMaxShip,GAME_OPTION_VIP_PASS: PLocalizer.GameVIPPass,GAME_OPTION_SOLO_PLAY: PLocalizer.GameSoloPlay},'optionVal': {GAME_DURATION_SHORT: PLocalizer.GameDurationShort,GAME_DURATION_MED: PLocalizer.GameDurationMed,GAME_DURATION_LONG: PLocalizer.GameDurationLong}}

def gatherGameStyleInfo(gameType, gameStyle, callback):
    requestId = None
    options = {}
    if gameType == PiratesGlobals.GAME_TYPE_TM:

        def gatherTMInfo(inventory):
            if inventory:
                treasureMaps = inventory.getTreasureMapsList()
            else:
                treasureMaps = []
            tmsOwned = {}
            for currTM in treasureMaps:
                tmsOwned[currTM.mapId] = currTM.getOptions()

            callback(tmsOwned)

        if callback:
            if game.process == 'client':
                requestId = DistributedInventoryBase.DistributedInventoryBase.getInventory(localAvatar.inventoryId, gatherTMInfo)
            else:
                tmsAvailable = {}
                if gameStyle != None:
                    numPlayers = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[PiratesGlobals.GAME_TYPE_TM][gameStyle].get('NumPlayers')
                    if numPlayers and len(numPlayers) > 1:
                        options = {GAME_OPTION_MAX_PLAYERS: numPlayers}
                        tmsAvailable[gameStyle] = options
                        styleInfo = {'options': options}
                callback(tmsAvailable)
    return (
     requestId, options)


GameTypes = {PiratesGlobals.GAME_TYPE_PRIV: {'options': {'execute': 'findPvp'}},PiratesGlobals.GAME_TYPE_PVP: {'style': {PiratesGlobals.GAME_STYLE_CTL: {'options': {GAME_OPTION_MIN_PLAYERS: [PiratesGuiGlobals.UIItemType_ListItem, ['2', '3', '4', '5', '6']]}},PiratesGlobals.GAME_STYLE_PIRATEER: {'options': {GAME_OPTION_MIN_PLAYERS: [PiratesGuiGlobals.UIItemType_ListItem, ['2', '3', '4', '5', '6']]}},PiratesGlobals.GAME_STYLE_TEAM_BATTLE: {'options': {GAME_OPTION_MIN_PLAYERS: [PiratesGuiGlobals.UIItemType_ListItem, ['4', '6']],GAME_OPTION_MAX_PLAYERS: [PiratesGuiGlobals.UIItemType_Hidden, '8']}},PiratesGlobals.GAME_STYLE_BATTLE: {'options': {GAME_OPTION_MIN_PLAYERS: [PiratesGuiGlobals.UIItemType_ListItem, ['2', '3', '4', '5', '6']],GAME_OPTION_MAX_PLAYERS: [PiratesGuiGlobals.UIItemType_Hidden, '8']}},PiratesGlobals.GAME_STYLE_SHIP_BATTLE: {'options': {GAME_OPTION_MAX_CREW_SIZE: [PiratesGuiGlobals.UIItemType_Hidden],GAME_OPTION_MAX_CREW_SHIP: [PiratesGuiGlobals.UIItemType_Hidden]}}}},PiratesGlobals.GAME_TYPE_CREW: {'options': {'execute': 'find'}},PiratesGlobals.GAME_TYPE_PG: {'style': {PiratesGlobals.GAME_STYLE_BLACKJACK: {'options': {GAME_OPTION_MAX_PLAYERS: [PiratesGuiGlobals.UIItemType_Hidden, '6']}},PiratesGlobals.GAME_STYLE_POKER: {'options': {GAME_OPTION_MAX_PLAYERS: [PiratesGuiGlobals.UIItemType_Hidden, '6']}}}},PiratesGlobals.GAME_TYPE_TM: {'style': gatherGameStyleInfo,'hidden': True}}
pvpMode = ConfigVariableBool('pvp-testing-level', 0).getIntWord(0)
if pvpMode < 1:
    del GameTypes[PiratesGlobals.GAME_TYPE_PVP]['style'][PiratesGlobals.GAME_STYLE_CTL]
if pvpMode < 2:
    del GameTypes[PiratesGlobals.GAME_TYPE_PVP]['style'][PiratesGlobals.GAME_STYLE_PIRATEER]
if pvpMode < 3:
    del GameTypes[PiratesGlobals.GAME_TYPE_PVP]['style'][PiratesGlobals.GAME_STYLE_SHIP_BATTLE]

def getGameTypes():
    print GameTypes
    return GameTypes.keys()


def getGameStyles(gameType, gameStyle=None, callback=None):
    if GameTypes.has_key(gameType) and GameTypes[gameType].has_key('style'):
        styleInfo = GameTypes[gameType]['style']
        if _styleInfoIsDynamic(styleInfo):
            return styleInfo(gameType, gameStyle, callback)
        callback(styleInfo.keys())
        return (
         None, styleInfo.keys())
    return None


def styleInfoIsDynamic(gameType):
    styleInfo = GameTypes[gameType]['style']
    return _styleInfoIsDynamic(styleInfo)


def _styleInfoIsDynamic(styleInfo):
    return type(styleInfo) == types.MethodType or type(styleInfo) == types.FunctionType


def getGameOptions(gameType, gameStyle=None, callback=None):
    requestId = None
    gameOptions = {}
    if GameTypes.has_key(gameType):
        if GameTypes[gameType].has_key('options'):
            return GameTypes[gameType]['options']
        elif gameStyle != None and GameTypes[gameType].has_key('style'):
            styleInfo = GameTypes[gameType]['style']
            if _styleInfoIsDynamic(styleInfo):

                def extractOptions(tmsOwned):
                    if callback:
                        foundOptions = {}
                        if tmsOwned:
                            foundOptions = tmsOwned[gameStyle].get('options', {})
                        callback(foundOptions)

                requestId, gameOptions = styleInfo(gameType, gameStyle, extractOptions)
            elif styleInfo.has_key(gameStyle):
                gameOptions = styleInfo[gameStyle]['options']
                if callback:
                    callback(gameOptions)
    return (
     requestId, gameOptions)


def getGameTypeString(value, type, category=None):
    if category != None and PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS.has_key(category):
        typeInfo = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[category].get(value)
        if typeInfo:
            if type == 'style':
                return typeInfo.get('Name')
            elif type == 'descriptionStyle':
                return typeInfo.get('Desc')
    values = GameTypeStrings.get(type)
    foundStr = None
    if values:
        foundStr = values.get(value)
    return foundStr


def getGameTypeRanking(value):
    foundIt = GameTypeRanking.get(value)
    return foundIt


def gameTypeAccessable(gameCat, gameType, paidStatus):
    if paidStatus:
        return True
    elif gameCat == PiratesGlobals.GAME_TYPE_PVP and (gameType == PiratesGlobals.GAME_STYLE_BATTLE or gameType == PiratesGlobals.GAME_STYLE_TEAM_BATTLE) or gameCat == PiratesGlobals.GAME_TYPE_PG and gameType == PiratesGlobals.GAME_STYLE_BLACKJACK:
        return True
    return False