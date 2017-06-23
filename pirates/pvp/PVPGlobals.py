from pandac.PandaModules import Vec4
from otp.web.Setting import StateVarSetting
from direct.fsm.StatePush import FunctionCall
from pirates.piratesbase import PLocalizer
from pirates.ship import ShipGlobals
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
RulesDuration = 12.0
ReadyTimeout = 120.0
ReadyBarrierTimeout = RulesDuration + ReadyTimeout
RenownBreakpointsSea = [
 0, 25, 200, 1000, 2500, 4500, 6500, 9000]
RenownBreakpointsLand = [0, 25, 200, 1000, 2500, 4500, 6500, 9000]
MainWorldAvRespawnDelay = 3.0
MainWorldInvulnerabilityDuration = StateVarSetting('pvp.invulnerability.duration', 180.0)
MainWorldInvulnerabilityWantCutoff = StateVarSetting('pvp.invulnerability.wantCutoff', 1)
MainWorldInvulnerabilityCutoffRadiusScale = StateVarSetting('pvp.invulnerability.cutoffSphereRadiusScale', 1.1)
WantIslandRegen = StateVarSetting('pvp.shipHeal.WantIslandRegen', getBase().config.GetBool('want-pvp-island-regeneration', 0))
WantShipRepairSpots = StateVarSetting('pvp.shipHeal.WantShipRepairSpots', getBase().config.GetBool('want-ship-repair-spots', 1))
WantShipRepairKit = StateVarSetting('pvp.shipHeal.WantShipRepairKit', getBase().config.GetBool('want-ship-repair-kit', 0))
ShipRegenRadiusScale = StateVarSetting('pvp.shipHeal.island.sphereRadiusScale', 1.0)
ShipRegenHps = StateVarSetting('pvp.shipHeal.island.healPerSecHP', 50)
ShipRegenSps = StateVarSetting('pvp.shipHeal.island.healPerSecSP', 50)
ShipRegenPeriod = StateVarSetting('pvp.shipHeal.island.healPeriodSecs', 2)
RepairRate = StateVarSetting('pvp.shipHeal.repairSpots.repairRate', 10.0)
RepairRateMultipliers = StateVarSetting('pvp.shipHeal.repairSpots.repairRateMultipliers', [
 1.0, 2.0, 3.0, 4.0])
RepairAcceleration = StateVarSetting('pvp.shipHeal.repairSpots.repairAcceleration', 2)
RepairAccelerationMultipliers = StateVarSetting('pvp.shipHeal.repairSpots.repairAccelerationMultipliers', [
 1.0, 1.0, 1.0, 1.0])
RepairKitHp = StateVarSetting('pvp.shipHeal.repairKit.HP', WeaponGlobals.getAttackHullHP(InventoryType.ShipRepairKit))
RepairKitSp = StateVarSetting('pvp.shipHeal.repairKit.SP', WeaponGlobals.getAttackSailHP(InventoryType.ShipRepairKit))
SinkHpBonusPercent = StateVarSetting('pvp.sinkBonus.hp.percent', 0.8)
SinkStreakPeriod = StateVarSetting('pvp.announcements.sinkStreakPeriod', 5)

def updateRepairKitHp(hp):
    WeaponGlobals.__skillInfo[InventoryType.ShipRepairKit][WeaponGlobals.HULL_HP_INDEX] = hp


def updateRepairKitSp(sp):
    WeaponGlobals.__skillInfo[InventoryType.ShipRepairKit][WeaponGlobals.SAIL_HP_INDEX] = sp


UpdateRepairKitHp = FunctionCall(updateRepairKitHp, RepairKitHp)
UpdateRepairKitHp.pushCurrentState()
UpdateRepairKitSp = FunctionCall(updateRepairKitSp, RepairKitSp)
UpdateRepairKitSp.pushCurrentState()
RepairSpotLocatorNames = [
 'repair_spot_0', 'repair_spot_1', 'repair_spot_2', 'repair_spot_3']
repairSpotNamePrefix = 'pvp.shipHeal.repairSpots.spots.'
ShipClass2repairLocators = {ShipGlobals.INTERCEPTORL1: StateVarSetting(repairSpotNamePrefix + 'interceptorL1', [0, 1, 2, 3]),ShipGlobals.INTERCEPTORL2: StateVarSetting(repairSpotNamePrefix + 'interceptorL2', [0, 1, 2, 3]),ShipGlobals.INTERCEPTORL3: StateVarSetting(repairSpotNamePrefix + 'interceptorL3', [0, 1, 2, 3]),ShipGlobals.MERCHANTL1: StateVarSetting(repairSpotNamePrefix + 'merchantL1', [0, 1, 2, 3]),ShipGlobals.MERCHANTL2: StateVarSetting(repairSpotNamePrefix + 'merchantL2', [0, 1, 2, 3]),ShipGlobals.MERCHANTL3: StateVarSetting(repairSpotNamePrefix + 'merchantL3', [0, 1, 2, 3]),ShipGlobals.WARSHIPL1: StateVarSetting(repairSpotNamePrefix + 'warshipL1', [0, 1, 2, 3]),ShipGlobals.WARSHIPL2: StateVarSetting(repairSpotNamePrefix + 'warshipL2', [0, 1, 2, 3]),ShipGlobals.WARSHIPL3: StateVarSetting(repairSpotNamePrefix + 'warshipL3', [0, 1, 2, 3]),ShipGlobals.BRIGL1: StateVarSetting(repairSpotNamePrefix + 'brigL1', [0, 1, 2, 3]),ShipGlobals.BRIGL2: StateVarSetting(repairSpotNamePrefix + 'brigL2', [0, 1, 2, 3]),ShipGlobals.BRIGL3: StateVarSetting(repairSpotNamePrefix + 'brigL3', [0, 1, 2, 3]),ShipGlobals.SHIP_OF_THE_LINE: StateVarSetting(repairSpotNamePrefix + 'shipOfTheLine', []),ShipGlobals.HMS_VICTORY: StateVarSetting(repairSpotNamePrefix + 'hmsVictory', []),ShipGlobals.HMS_NEWCASTLE: StateVarSetting(repairSpotNamePrefix + 'hmsNewCastle', []),ShipGlobals.HMS_INVINCIBLE: StateVarSetting(repairSpotNamePrefix + 'hmsInvincible', []),ShipGlobals.EITC_INTREPID: StateVarSetting(repairSpotNamePrefix + 'eitcIntrepid', []),ShipGlobals.EITC_CONQUERER: StateVarSetting(repairSpotNamePrefix + 'eitcConquerer', []),ShipGlobals.EITC_LEVIATHAN: StateVarSetting(repairSpotNamePrefix + 'eitcLeviathan', []),ShipGlobals.BLACK_PEARL: StateVarSetting(repairSpotNamePrefix + 'blackpearl', []),ShipGlobals.GOLIATH: StateVarSetting(repairSpotNamePrefix + 'goliath', []),ShipGlobals.FLYING_DUTCHMAN: StateVarSetting(repairSpotNamePrefix + 'flyingdutchman', []),ShipGlobals.DAUNTLESS: StateVarSetting(repairSpotNamePrefix + 'dauntless', []),ShipGlobals.JOLLY_ROGER: StateVarSetting(repairSpotNamePrefix + 'jollyroger', []),ShipGlobals.SKEL_WARSHIPL3: StateVarSetting(repairSpotNamePrefix + 'skel_warshipL3', []),ShipGlobals.SKEL_INTERCEPTORL3: StateVarSetting(repairSpotNamePrefix + 'skel_interceptorL3', []),ShipGlobals.EL_PATRONS_SHIP: StateVarSetting(repairSpotNamePrefix + 'el_patrons_ship', [0, 1, 2, 3]),ShipGlobals.P_NAVY_KINGFISHER: StateVarSetting(repairSpotNamePrefix + 'p_navy_kingfisher', [0, 1, 2, 3]),ShipGlobals.P_EITC_WARLORD: StateVarSetting(repairSpotNamePrefix + 'p_eitc_warlord', [0, 1, 2, 3]),ShipGlobals.P_SKEL_PHANTOM: StateVarSetting(repairSpotNamePrefix + 'p_skel_phantom', []),ShipGlobals.P_SKEL_REVENANT: StateVarSetting(repairSpotNamePrefix + 'p_skel_revenant', []),ShipGlobals.P_SKEL_CEREBUS: StateVarSetting(repairSpotNamePrefix + 'p_skel_cerebus', []),ShipGlobals.QUEEN_ANNES_REVENGE: StateVarSetting(repairSpotNamePrefix + 'queenAnnesRevenge', []),ShipGlobals.HUNTER_VENGEANCE: StateVarSetting(repairSpotNamePrefix + 'hunterVengeance', []),ShipGlobals.HUNTER_TALLYHO: StateVarSetting(repairSpotNamePrefix + 'hunterTallyho', [])}
del repairSpotNamePrefix
INSTANCE_PVP_CTL = 0
INSTANCE_PVP_STB = 1
WIN_COND_SCORE = 1
WIN_COND_TIME = 2
WIN_COND_CAPTURE = 3
ID = 0
NAME = 1
SCORE = 2
KILLS = 3
DEATHS = 4
RANK = 5
TEAM = 6
BOUNTY = 7
TOO_LOW_LEVEL = 12
GOOD_MATCH = 2
PLAYER_SCORE = 0
SHIP_SCORE = 1
TEAM_SCORE = 2
FrenchTeam = 1
SpanishTeam = 2
siegeTeamNames = {FrenchTeam: PLocalizer.ShipPVPQuestFrench,SpanishTeam: PLocalizer.ShipPVPQuestSpanish}
MaxPrivateerShipsPerTeam = StateVarSetting('pvp.maxShipsPerTeam', getBase().config.GetInt('max-ships-per-privateer-team', 10))
statText = {SCORE: PLocalizer.PVPScore,KILLS: PLocalizer.PVPEnemiesDefeated,DEATHS: PLocalizer.PVPTimesDefeated,BOUNTY: PLocalizer.PVPBounty}
TEAM_COLOR = [
 Vec4(1.0, 0.4, 0.4, 1.0), Vec4(0.4, 0.4, 1.0, 1.0), Vec4(0.4, 1.0, 0.4, 1.0), Vec4(0.4, 1.0, 1.0, 1.0), Vec4(1.0, 0.4, 1.0, 1.0), Vec4(1.0, 1.0, 0.4, 1.0), Vec4(0.0, 0.0, 0.0, 1.0), Vec4(0.5, 0.5, 0.5, 1.0), Vec4(1.0, 1.0, 1.0, 1.0), Vec4(0.2, 0.4, 0.4, 1.0), Vec4(0.4, 0.2, 0.4, 1.0), Vec4(0.4, 0.4, 0.2, 1.0)]

def getTeamColor(team, TEAM_COLOR=TEAM_COLOR):
    return TEAM_COLOR[(team - 1) % len(TEAM_COLOR)]


SIEGE_TEAM_COLOR = [
 Vec4(0.08, 0.28, 0.67, 1.0), Vec4(1.0, 0.8, 0.0, 1.0)]

def getSiegeColor(team, SIEGE_TEAM_COLOR=SIEGE_TEAM_COLOR):
    return SIEGE_TEAM_COLOR[(team - 1) % len(SIEGE_TEAM_COLOR)]


EventDefeat = 0
TeamBalanceValues = ScratchPad()
TeamBalanceValues.Player = 2
TeamBalanceValues.Ships = {ShipGlobals.INTERCEPTORL1: 5,ShipGlobals.INTERCEPTORL2: 8,ShipGlobals.INTERCEPTORL3: 12,ShipGlobals.MERCHANTL1: 13,ShipGlobals.MERCHANTL2: 18,ShipGlobals.MERCHANTL3: 22,ShipGlobals.WARSHIPL1: 12,ShipGlobals.WARSHIPL2: 15,ShipGlobals.WARSHIPL3: 20,ShipGlobals.BRIGL1: 14,ShipGlobals.BRIGL2: 16,ShipGlobals.BRIGL3: 23,ShipGlobals.SHIP_OF_THE_LINE: 25,ShipGlobals.EL_PATRONS_SHIP: 20,ShipGlobals.QUEEN_ANNES_REVENGE: 20,ShipGlobals.P_NAVY_KINGFISHER: 8,ShipGlobals.P_EITC_WARLORD: 20,ShipGlobals.P_SKEL_PHANTOM: 22,ShipGlobals.P_SKEL_REVENANT: 22,ShipGlobals.SKEL_STORM_REAPER: 22,ShipGlobals.SKEL_BLACK_HARBINGER: 22,ShipGlobals.SKEL_DEATH_OMEN: 22,ShipGlobals.P_SKEL_CEREBUS: 12}
RenownWorthValues = {ShipGlobals.INTERCEPTORL1: 2,ShipGlobals.INTERCEPTORL2: 4,ShipGlobals.INTERCEPTORL3: 6,ShipGlobals.MERCHANTL1: 4,ShipGlobals.MERCHANTL2: 7,ShipGlobals.MERCHANTL3: 10,ShipGlobals.WARSHIPL1: 5,ShipGlobals.WARSHIPL2: 8,ShipGlobals.WARSHIPL3: 10,ShipGlobals.BRIGL1: 5,ShipGlobals.BRIGL2: 8,ShipGlobals.BRIGL3: 10,ShipGlobals.SHIP_OF_THE_LINE: 13,ShipGlobals.EL_PATRONS_SHIP: 10,ShipGlobals.QUEEN_ANNES_REVENGE: 11,ShipGlobals.P_NAVY_KINGFISHER: 4,ShipGlobals.P_EITC_WARLORD: 10,ShipGlobals.P_SKEL_PHANTOM: 11,ShipGlobals.P_SKEL_REVENANT: 11,ShipGlobals.SKEL_STORM_REAPER: 11,ShipGlobals.SKEL_BLACK_HARBINGER: 11,ShipGlobals.SKEL_DEATH_OMEN: 11,ShipGlobals.P_SKEL_CEREBUS: 6}

class ShipDescription():

    def __init__(self, shipClass):
        self.shipClass = shipClass


def getTeamBalanceValue(obj):
    if hasattr(obj, 'shipClass'):
        return TeamBalanceValues.Ships[obj.shipClass]
    else:
        return TeamBalanceValues.Player


def getRankLand(expPoints):
    high = 0
    for testValue in RenownBreakpointsLand:
        if testValue > expPoints:
            return high - 1
        high += 1

    return high - 1


def getRankSea(expPoints):
    high = 0
    for testValue in RenownBreakpointsSea:
        if testValue > expPoints:
            return high - 1
        high += 1

    return high - 1


def getMaxRankLand():
    return len(RenownBreakpointsLand) - 1


def getMaxRankSea():
    return len(RenownBreakpointsSea) - 1


def getShipInfamyWorth(shipClass):
    if shipClass:
        if shipClass in RenownWorthValues:
            return RenownWorthValues.get(shipClass)
        else:
            return 1
    else:
        return 0


BountyRanks = [
 50, 100, 250, 500, 1000]
BountyRankLevels = len(BountyRanks)
SHIP_PVP_SINK_TIME_MAX = 60 * 60 * 24
SHIP_PVP_SINK_TIME_NEXT = 60 * 60 * 24
SHIP_PVP_INFAMY_DEC_PERCENT = 0.0
SHIP_PVP_INFAMY_DEC_FLAT = 1
LAND_PVP_DEFEAT_TIME_MAX = 60 * 60 * 24
LAND_PVP_DEFEAT_TIME_NEXT = 60 * 60 * 24
LAND_PVP_INFAMY_DEC_PERCENT = 0.0
LAND_PVP_INFAMY_DEC_FLAT = 1