from pirates.piratesbase import PLocalizer
from pirates.audio import SoundGlobals
from pirates.battle import EnemyGlobals
import random
HUNTER_LEVEL_NAME_DICT = {EnemyGlobals.SHIP_THREAT_BOUNTY_HUNTERS: PLocalizer.Nametag_BountyHunter,EnemyGlobals.SHIP_THREAT_NAVY_HUNTERS: PLocalizer.Nametag_Warship}
VO_SALTY = 0
VO_CHOICE = VO_SALTY
VO_DICT = {VO_SALTY: {'ThreatLevelDescriptions': {EnemyGlobals.SHIP_THREAT_NONE: {0: None},EnemyGlobals.SHIP_THREAT_ATTACK_BACK: {0: [(PLocalizer.ThreatLevel_1_text_a, [SoundGlobals.VO_THREAT_L1_ANNOUNCE_A]), (PLocalizer.ThreatLevel_1_text_b, [SoundGlobals.VO_THREAT_L1_ANNOUNCE_B])]},EnemyGlobals.SHIP_THREAT_CALL_FOR_HELP: {0: [(PLocalizer.ThreatLevel_2_text_a, [SoundGlobals.VO_THREAT_L2_ANNOUNCE_A]), (PLocalizer.ThreatLevel_2_text_b, [SoundGlobals.VO_THREAT_L2_ANNOUNCE_B])]},EnemyGlobals.SHIP_THREAT_BOUNTY_HUNTERS: {0: [(PLocalizer.ThreatLevel_3_text_a, [SoundGlobals.VO_THREAT_L3_ANNOUNCE_A]), (PLocalizer.ThreatLevel_3_text_b, [SoundGlobals.VO_THREAT_L3_ANNOUNCE_B])]},EnemyGlobals.SHIP_THREAT_NAVY_HUNTERS: {0: [(PLocalizer.ThreatLevel_4_text_a, [SoundGlobals.VO_THREAT_L4_ANNOUNCE_A])]},EnemyGlobals.SHIP_THREAT_SCENARIO_START: {0: [(PLocalizer.ThreatLevel_5_Scenerio_DJ_text_a, [SoundGlobals.JSD_ANYTIME_01, SoundGlobals.JSD_HAT_01])]},EnemyGlobals.SHIP_THREAT_SCENARIO_END: {0: [(PLocalizer.ThreatLevel_6_Scenerio_DJ_text_b,)]}},'PortClosedMessages': {'1160614528.73sdnaik': [(PLocalizer.PortClosed_Cuba, SoundGlobals.VO_THREAT_PORT_CLOSE_CUBA)],'1156207188.95dzlu': [(PLocalizer.PortClosed_Tortuga, SoundGlobals.VO_THREAT_PORT_CLOSE_TORTUGA)],'1271348547.01akelts': [(PLocalizer.PortClosed_RavensCove, SoundGlobals.VO_THREAT_PORT_CLOSE_RAVENSCOVE)],'1164135492.81dzlu': [(PLocalizer.PortClosed_DevilsAnvil, SoundGlobals.VO_THREAT_PORT_CLOSE_DEVILSANVIL)]},'PortOpenMessages': {'1160614528.73sdnaik': [(PLocalizer.PortOpen_Cuba, SoundGlobals.VO_THREAT_PORT_BUT_OPEN_CUBA)],'1156207188.95dzlu': [(PLocalizer.PortOpen_Tortuga, SoundGlobals.VO_THREAT_PORT_BUT_OPEN_TORTUGA)],'1271348547.01akelts': [(PLocalizer.PortOpen_RavensCove, SoundGlobals.VO_THREAT_PORT_BUT_OPEN_RAVENSCOVE)],'1164135492.81dzlu': [(PLocalizer.PortOpen_DevilsAnvil, SoundGlobals.VO_THREAT_PORT_BUT_OPEN_DEVILSANVIL)]},'PortIntial': [(PLocalizer.PortClosed_Initial, SoundGlobals.VO_THREAT_PORT_CLOSE_ALL)],'WildIslandMessage': [(PLocalizer.NoPortWild, SoundGlobals.VO_THREAT_CANT_PORT_WILD_A)],'WrongIslandMessage': [(PLocalizer.CantPortNavy_a, SoundGlobals.VO_THREAT_CANT_PORT_NAVY_A), (PLocalizer.CantPortNavy_b, SoundGlobals.VO_THREAT_CANT_PORT_NAVY_B)],'ShipInboundSimple': [(PLocalizer.ShipInboundSimple_a, [SoundGlobals.VO_THREAT_INBOUND_SIMPLE_A]), (PLocalizer.ShipInboundSimple_b, [SoundGlobals.VO_THREAT_INBOUND_SIMPLE_B]), (PLocalizer.ShipInboundSimple_c, [SoundGlobals.VO_THREAT_INBOUND_SIMPLE_C])],'ShipInboundHelp': [(PLocalizer.ShipInboundHelp_a, [SoundGlobals.VO_THREAT_INBOUND_HELP_A]), (PLocalizer.ShipInboundHelp_b, [SoundGlobals.VO_THREAT_INBOUND_HELP_B])],'ShipInboundHunter': [(PLocalizer.ShipInboundHunter_a, [SoundGlobals.VO_THREAT_INBOUND_BOUNTYHUNTER_A]), (PLocalizer.ShipInboundHunter_b, [SoundGlobals.VO_THREAT_INBOUND_BOUNTYHUNTER_B]), (PLocalizer.ShipInboundHunter_c, [SoundGlobals.VO_THREAT_INBOUND_BOUNTYHUNTER_C])],'ShipSunkMessage': [(PLocalizer.ShipSunkMessage_a, [SoundGlobals.VO_THREAT_SHIPSUNK_A]), (PLocalizer.ShipSunkMessage_b, [SoundGlobals.VO_THREAT_SHIPSUNK_B]), (PLocalizer.ShipSunkMessage_c, [SoundGlobals.VO_THREAT_SHIPSUNK_C]), (PLocalizer.ShipSunkMessage_d, [SoundGlobals.VO_THREAT_SHIPSUNK_D]), (PLocalizer.ShipSunkMessage_e, [SoundGlobals.VO_THREAT_SHIPSUNK_E]), (PLocalizer.ShipSunkMessage_f, [SoundGlobals.VO_THREAT_SHIPSUNK_F])]}}
LAST_CLOSED = None

def getPortClosedMessage(portUId):
    global VO_CHOICE
    global LAST_CLOSED
    choiceList = VO_DICT[VO_CHOICE]['PortClosedMessages'].get(portUId)
    if choiceList == None:
        return
    messageChoice = random.choice(choiceList)
    while messageChoice == LAST_CLOSED and len(choiceList) > 1:
        messageChoice = random.choice(choiceList)

    LAST_CLOSED = messageChoice
    return messageChoice


LAST_OPEN = None

def getPortOpenMessage(portUId):
    global LAST_OPEN
    choiceList = VO_DICT[VO_CHOICE]['PortOpenMessages'].get(portUId)
    if choiceList == None:
        return
    messageChoice = random.choice(choiceList)
    while messageChoice == LAST_OPEN and len(choiceList) > 1:
        messageChoice = random.choice(choiceList)

    LAST_OPEN = messageChoice
    return messageChoice


LAST_PORT_INIT = None

def getInitPortMessage():
    global LAST_PORT_INIT
    choiceList = VO_DICT[VO_CHOICE]['PortIntial']
    messageChoice = random.choice(choiceList)
    while messageChoice == LAST_PORT_INIT and len(choiceList) > 1:
        messageChoice = random.choice(choiceList)

    LAST_PORT_INIT = messageChoice
    return messageChoice


LAST_WILD_ISLAND = None

def getWildIslandMessage():
    global LAST_WILD_ISLAND
    choiceList = VO_DICT[VO_CHOICE]['WildIslandMessage']
    messageChoice = random.choice(choiceList)
    while messageChoice == LAST_WILD_ISLAND and len(choiceList) > 1:
        messageChoice = random.choice(choiceList)

    LAST_WILD_ISLAND = messageChoice
    return messageChoice


LAST_WRONG_ISLAND = None

def getWrongIslandMessage():
    global LAST_WRONG_ISLAND
    choiceList = VO_DICT[VO_CHOICE]['WrongIslandMessage']
    messageChoice = random.choice(choiceList)
    while messageChoice == LAST_WRONG_ISLAND and len(choiceList) > 1:
        messageChoice = random.choice(choiceList)

    LAST_WRONG_ISLAND = messageChoice
    return messageChoice


LAST_INBOUD_SIMPLE = None

def getInboundMessage():
    global LAST_INBOUD_SIMPLE
    choiceList = VO_DICT[VO_CHOICE]['ShipInboundSimple']
    messageChoice = random.choice(choiceList)
    while messageChoice == LAST_INBOUD_SIMPLE and len(choiceList) > 1:
        messageChoice = random.choice(choiceList)

    LAST_INBOUD_SIMPLE = messageChoice
    return messageChoice


LAST_INBOUND_HELP = None

def getInboundHelpMessage():
    global LAST_INBOUND_HELP
    choiceList = VO_DICT[VO_CHOICE]['ShipInboundHelp']
    messageChoice = random.choice(choiceList)
    while messageChoice == LAST_INBOUND_HELP and len(choiceList) > 1:
        messageChoice = random.choice(choiceList)

    LAST_INBOUND_HELP = messageChoice
    return messageChoice


LAST_INBOUND_HUNTER = None

def getInboundHunterMessage():
    global LAST_INBOUND_HUNTER
    choiceList = VO_DICT[VO_CHOICE]['ShipInboundHunter']
    messageChoice = random.choice(choiceList)
    while messageChoice == LAST_INBOUND_HUNTER and len(choiceList) > 1:
        messageChoice = random.choice(choiceList)

    LAST_INBOUND_HUNTER = messageChoice
    return messageChoice


LAST_SUNK = []

def getShipSunkMessage():
    global LAST_SUNK
    choiceList = VO_DICT[VO_CHOICE]['ShipSunkMessage']
    messageChoice = random.choice(choiceList)
    while messageChoice in LAST_SUNK and len(choiceList) > 1:
        messageChoice = random.choice(choiceList)

    LAST_SUNK.append(messageChoice)
    LAST_SUNK = LAST_SUNK[-2:]
    return messageChoice


LAST_THREAT = None

def getThreatLevelDescription(threatLevel, scenarioIndex):
    global LAST_THREAT
    threatLevelDict = VO_DICT[VO_CHOICE]['ThreatLevelDescriptions'].get(threatLevel, None)
    if threatLevelDict == None:
        return
    scenarioList = threatLevelDict.get(scenarioIndex, None)
    if scenarioList == None:
        threatLevelDict.get(0, None)
    if scenarioList == None:
        return
    messageChoice = random.choice(scenarioList)
    while messageChoice == LAST_THREAT and len(scenarioList) > 1:
        messageChoice = random.choice(scenarioList)

    LAST_THREAT = messageChoice
    return messageChoice