from pirates.ship import ShipGlobals
from pirates.pirate import AvatarTypes
from pirates.piratesbase import PiratesGlobals
from pandac.PandaModules import Point3, Vec4
from pirates.quest.QuestConstants import NPCIds
from pirates.ai import HolidayGlobals
from pirates.world.LocationConstants import LocationIds
from pirates.uberdog.UberDogGlobals import InventoryType
JOLLY_ROGER_INVASION_SHIP = ShipGlobals.JOLLY_ROGER
JOLLY_UNIQUE_ID = '1248740229.97robrusso'
JOLLY_DISENGAGE_LIMIT = 1
JOLLY_DISENGAGE_TIME = 5.0
JOLLY_ATTACK_TIME = 2.0
BOSS_WAIT_TIME = 120
INVASION_PORT_ROYAL = HolidayGlobals.INVASIONPORTROYAL
INVASION_TORTUGA = HolidayGlobals.INVASIONTORTUGA
INVASION_DEL_FUEGO = HolidayGlobals.INVASIONDELFUEGO
INVASION_IDS = [
 HolidayGlobals.getHolidayName(INVASION_PORT_ROYAL), HolidayGlobals.getHolidayName(INVASION_TORTUGA), HolidayGlobals.getHolidayName(INVASION_DEL_FUEGO)]
INVASION_NUMBERS = [
 INVASION_PORT_ROYAL, INVASION_TORTUGA, INVASION_DEL_FUEGO]
ISLAND_IDS = {INVASION_PORT_ROYAL: LocationIds.PORT_ROYAL_ISLAND,INVASION_TORTUGA: LocationIds.TORTUGA_ISLAND,INVASION_DEL_FUEGO: LocationIds.DEL_FUEGO_ISLAND,HolidayGlobals.WRECKEDGOVERNORSMANSION: LocationIds.PORT_ROYAL_ISLAND,HolidayGlobals.WRECKEDFAITHFULBRIDE: LocationIds.TORTUGA_ISLAND,HolidayGlobals.WRECKEDDELFUEGOTOWN: LocationIds.DEL_FUEGO_ISLAND}

def getIslandId(holiday):
    return ISLAND_IDS[holiday]


REMOVABLE_SPAWN_PTS = {INVASION_PORT_ROYAL: ['1158366723.53dparis', '1158366673.28dparis', '1158366574.17dparis', '1178667776.0dxschafe0', '1178667776.0dxschafe1', '1184632064.0dxschafe', '1178667904.0dxschafe', '1178668288.0dxschafe0', '1178667776.0dxschafe'],INVASION_TORTUGA: [],INVASION_DEL_FUEGO: []}

def getRemovableSpawnPts(holiday):
    return REMOVABLE_SPAWN_PTS[holiday]


LOSS_HOLIDAYS = {INVASION_PORT_ROYAL: HolidayGlobals.WRECKEDGOVERNORSMANSION,INVASION_TORTUGA: HolidayGlobals.WRECKEDFAITHFULBRIDE,INVASION_DEL_FUEGO: HolidayGlobals.WRECKEDDELFUEGOTOWN}

def getLossHoliday(holiday):
    return LOSS_HOLIDAYS[holiday]


SCREEN_INFO = {INVASION_PORT_ROYAL: [(0.75, 0, -0.65), 0.00055],INVASION_TORTUGA: [(0.75, 0, -0.65), 0.0008],INVASION_DEL_FUEGO: [(0.75, 0, -0.68), 0.00045]}

def getScreenInfo(holiday):
    return SCREEN_INFO[holiday]


LOSS_FIRES = {INVASION_PORT_ROYAL: [[(0.82, 0, -0.292), (-0.45, 0.45, 0.45)], [(0.84, 0, -0.295), 0.6], [(0.865, 0, -0.29), 0.45]],INVASION_TORTUGA: [[(0.84, 0, -0.48), 0.6]],INVASION_DEL_FUEGO: [[(0.96, 0, -0.7), 0.7], [(0.91, 0, -0.68), (-0.6, 0.6, 0.6)], [(0.93, 0, -0.72), 0.6]]}

def getLossFires(holiday):
    return LOSS_FIRES[holiday]


TOWNFOLK_IDS = {INVASION_PORT_ROYAL: [NPCIds.EDWARD_STORMHAWK, NPCIds.SAM_SEABONES, NPCIds.FLECTHER_BEAKMAN, NPCIds.DARBY_DRYDOCK, NPCIds.LUCINDA, NPCIds.CASSANDRA, NPCIds.EMMA, NPCIds.JAMES_MACDOUGAL, NPCIds.EDWARD_SHACKLEBY, NPCIds.CLAYTON_COLLARD, NPCIds.ENSIGN_GRIMM, NPCIds.ANGEL_OBONNEY, NPCIds.ROSE_SEAFELLOW],INVASION_TORTUGA: [NPCIds.ORINDA, NPCIds.HORATIO_FOWLER, NPCIds.O_MALLEY, NPCIds.FABIOLA, NPCIds.SCARLET, NPCIds.HENDRY_CUTTS, NPCIds.BUTCHER_BROWN, NPCIds.BIG_PHIL],INVASION_DEL_FUEGO: [NPCIds.ROMANY_BEV, NPCIds.SHOCHETT_PRYMME, NPCIds.VALENTINA, NPCIds.ROLAND_RAGGART, NPCIds.OLIVIER, NPCIds.HENRY_LOWMAN, NPCIds.BALTHASAR, NPCIds.PELAGIA, NPCIds.HEARTLESS_ROSALINE, NPCIds.CLEMENCE_BASILSHOT]}

def getTownfolkIds(holiday):
    return TOWNFOLK_IDS[holiday]


START_MESSAGE_RANGE = {INVASION_PORT_ROYAL: 1,INVASION_TORTUGA: 1,INVASION_DEL_FUEGO: 1}

def getStartMessageRange(holiday):
    return range(0, START_MESSAGE_RANGE[holiday])


SECOND_WAVE_MESSAGE_RANGE = {INVASION_PORT_ROYAL: 1,INVASION_TORTUGA: 1,INVASION_DEL_FUEGO: 1}

def getSecondWaveMessageRange(holiday):
    return range(0, SECOND_WAVE_MESSAGE_RANGE[holiday])


LAST_WAVE_MESSAGE_RANGE = {INVASION_PORT_ROYAL: 1,INVASION_TORTUGA: 1,INVASION_DEL_FUEGO: 1}

def getLastWaveMessageRange(holiday):
    return range(0, LAST_WAVE_MESSAGE_RANGE[holiday])


PHASE_MESSAGE_RANGE = {INVASION_PORT_ROYAL: 25,INVASION_TORTUGA: 24,INVASION_DEL_FUEGO: 23}

def getPhaseMessageRange(holiday):
    return range(0, PHASE_MESSAGE_RANGE[holiday])


GOOD_BOSS_MESSAGE_RANGE = {INVASION_PORT_ROYAL: 4,INVASION_TORTUGA: 4,INVASION_DEL_FUEGO: 4}

def getGoodBossMessageRange(holiday):
    return range(0, GOOD_BOSS_MESSAGE_RANGE[holiday])


BAD_BOSS_MESSAGE_RANGE = {INVASION_PORT_ROYAL: 1,INVASION_TORTUGA: 1,INVASION_DEL_FUEGO: 1}

def getBadBossMessageRange(holiday):
    return range(0, BAD_BOSS_MESSAGE_RANGE[holiday])


LOW_HEALTH_MESSAGE_RANGE = {INVASION_PORT_ROYAL: 2,INVASION_TORTUGA: 2,INVASION_DEL_FUEGO: 2}

def getLowHealthMessageRange(holiday):
    return range(0, LOW_HEALTH_MESSAGE_RANGE[holiday])


WIN_MESSAGE_RANGE = {INVASION_PORT_ROYAL: 1,INVASION_TORTUGA: 1,INVASION_DEL_FUEGO: 1}

def getWinMessageRange(holiday):
    return range(0, WIN_MESSAGE_RANGE[holiday])


LOSE_MESSAGE_RANGE = {INVASION_PORT_ROYAL: 3,INVASION_TORTUGA: 1,INVASION_DEL_FUEGO: 3}

def getLoseMessageRange(holiday):
    return range(0, LOSE_MESSAGE_RANGE[holiday])


TOTAL_SPAWN_ZONE_LIST = {INVASION_PORT_ROYAL: 8,INVASION_TORTUGA: 7,INVASION_DEL_FUEGO: 8}

def getTotalSpawnZones(holiday):
    return TOTAL_SPAWN_ZONE_LIST[holiday]


SPAWN_ZONE_LIST = {INVASION_PORT_ROYAL: ([1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 5, 6], [1, 3, 5, 6, 7], [1, 3, 5, 6, 7, 8]),INVASION_TORTUGA: ([1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 3, 5, 6], [1, 2, 3, 5, 6, 7]),INVASION_DEL_FUEGO: ([1, 2, 3, 4], [1, 3, 4, 5], [1, 3, 4, 5, 7], [1, 3, 4, 5, 6, 7], [1, 3, 5, 6, 7, 8])}

def getSpawnZones(holiday, numPlayers):
    if holiday == INVASION_PORT_ROYAL or holiday == INVASION_DEL_FUEGO:
        if numPlayers < 41:
            return SPAWN_ZONE_LIST[holiday][0]
        elif numPlayers < 71:
            return SPAWN_ZONE_LIST[holiday][1]
        elif numPlayers < 101:
            return SPAWN_ZONE_LIST[holiday][2]
        elif numPlayers < 131:
            return SPAWN_ZONE_LIST[holiday][3]
        else:
            return SPAWN_ZONE_LIST[holiday][4]
    elif holiday == INVASION_TORTUGA:
        if numPlayers < 21:
            return SPAWN_ZONE_LIST[holiday][0]
        elif numPlayers < 41:
            return SPAWN_ZONE_LIST[holiday][1]
        elif numPlayers < 81:
            return SPAWN_ZONE_LIST[holiday][2]
        else:
            return SPAWN_ZONE_LIST[holiday][3]


TOTAL_PHASE_LIST = {INVASION_PORT_ROYAL: 7,INVASION_TORTUGA: 7,INVASION_DEL_FUEGO: 7}

def getTotalPhases(holiday):
    return TOTAL_PHASE_LIST[holiday]


PHASE_1_ENEMIES = [
 AvatarTypes.Mire, AvatarTypes.Mire, AvatarTypes.Mire, AvatarTypes.Mire, AvatarTypes.Mire, AvatarTypes.Mire, AvatarTypes.Mire, AvatarTypes.Muck, AvatarTypes.Muck]
PHASE_2_ENEMIES = [
 AvatarTypes.MuckCutlass, AvatarTypes.MuckCutlass, AvatarTypes.MuckCutlass, AvatarTypes.MuckCutlass, AvatarTypes.MuckCutlass, AvatarTypes.MuckCutlass, AvatarTypes.Muck, AvatarTypes.Muck, AvatarTypes.Muck]
PHASE_3_ENEMIES = [
 AvatarTypes.Muck, AvatarTypes.Muck, AvatarTypes.Muck, AvatarTypes.Muck, AvatarTypes.SpanishUndeadA, AvatarTypes.SpanishUndeadA, AvatarTypes.SpanishUndeadA, AvatarTypes.SpanishUndeadB, AvatarTypes.SpanishUndeadB]
PHASE_4_ENEMIES = [
 AvatarTypes.FrenchUndeadA, AvatarTypes.FrenchUndeadA, AvatarTypes.FrenchUndeadB, AvatarTypes.FrenchUndeadB, AvatarTypes.FrenchUndeadC, AvatarTypes.Muck, AvatarTypes.Muck, AvatarTypes.Muck, AvatarTypes.Cadaver]
PHASE_5_ENEMIES = [
 AvatarTypes.Muck, AvatarTypes.Muck, AvatarTypes.CorpseCutlass, AvatarTypes.CorpseCutlass, AvatarTypes.CorpseCutlass, AvatarTypes.SpanishUndeadC, AvatarTypes.SpanishUndeadC, AvatarTypes.Cadaver, AvatarTypes.Cadaver]
PHASE_6_ENEMIES = [
 AvatarTypes.Cadaver, AvatarTypes.Cadaver, AvatarTypes.Cadaver, AvatarTypes.Muck, AvatarTypes.CadaverCutlass, AvatarTypes.CadaverCutlass, AvatarTypes.CadaverCutlass, AvatarTypes.FrenchUndeadD, AvatarTypes.SpanishUndeadD]
PHASE_7_ENEMIES = [
 AvatarTypes.CadaverCutlass, AvatarTypes.CadaverCutlass, AvatarTypes.CaptMudmoss, AvatarTypes.CaptMudmoss, AvatarTypes.Cadaver, AvatarTypes.Cadaver, AvatarTypes.Cadaver, AvatarTypes.Stump, AvatarTypes.Stump]
PHASE_ENEMY_SETS = {INVASION_PORT_ROYAL: {1: PHASE_1_ENEMIES,2: PHASE_2_ENEMIES,3: PHASE_3_ENEMIES,4: PHASE_4_ENEMIES,5: PHASE_5_ENEMIES,6: PHASE_6_ENEMIES,7: PHASE_7_ENEMIES},INVASION_TORTUGA: {1: PHASE_1_ENEMIES,2: PHASE_2_ENEMIES,3: PHASE_3_ENEMIES,4: PHASE_4_ENEMIES,5: PHASE_5_ENEMIES,6: PHASE_6_ENEMIES,7: PHASE_7_ENEMIES},INVASION_DEL_FUEGO: {1: PHASE_1_ENEMIES,2: PHASE_2_ENEMIES,3: PHASE_3_ENEMIES,4: PHASE_4_ENEMIES,5: PHASE_5_ENEMIES,6: PHASE_6_ENEMIES,7: PHASE_7_ENEMIES}}

def getPhaseEnemySets(holiday):
    return PHASE_ENEMY_SETS[holiday]


ENEMY_SPEEDS = {INVASION_PORT_ROYAL: 1.0,INVASION_TORTUGA: 1.0,INVASION_DEL_FUEGO: 1.25}

def getEnemySpeed(holiday):
    return ENEMY_SPEEDS[holiday]


ENEMY_DURATION_MODIFIER = {INVASION_PORT_ROYAL: {1: 1.0,2: 1.0,3: 1.0,4: 1.0,5: 1.0,6: 1.0,7: 1.0},INVASION_TORTUGA: {1: 1.5,2: 1.5,3: 1.5,4: 1.5,5: 1.5,6: 1.5,7: 1.5},INVASION_DEL_FUEGO: {1: 1.0,2: 1.0,3: 1.0,4: 1.0,5: 1.0,6: 1.0,7: 1.0}}

def getEnemyDurationModifier(holiday, phase):
    return ENEMY_DURATION_MODIFIER[holiday][phase]


BOMBER_ZOMBIE_PROBABILITY = {INVASION_PORT_ROYAL: {1: 0.0,2: 0.6,3: 0.2,4: 0.6,5: 0.2,6: 0.6,7: 0.6},INVASION_TORTUGA: {1: 0.0,2: 0.6,3: 0.6,4: 0.2,5: 0.6,6: 0.2,7: 0.6},INVASION_DEL_FUEGO: {1: 0.6,2: 0.2,3: 0.6,4: 0.2,5: 0.2,6: 0.6,7: 0.6}}

def getBomberZombieProbability(holiday, phase):
    return BOMBER_ZOMBIE_PROBABILITY[holiday][phase]


BOMBER_ZOMBIE_PERCENT = {INVASION_PORT_ROYAL: {1: 0.0,2: 0.05,3: 0.4,4: 0.05,5: 0.4,6: 0.1,7: 0.1},INVASION_TORTUGA: {1: 0.0,2: 0.05,3: 0.05,4: 0.4,5: 0.1,6: 0.4,7: 0.1},INVASION_DEL_FUEGO: {1: 0.05,2: 0.4,3: 0.1,4: 0.4,5: 0.4,6: 0.1,7: 0.1}}

def getBomberZombiePercent(holiday, phase):
    return BOMBER_ZOMBIE_PERCENT[holiday][phase]


ENEMY_START_PATH_POS_LIST = {INVASION_PORT_ROYAL: {1: (-61.0232, -192.343, 11.1546),2: (534.141, -379.633, 4.22788),3: (339.465, -461.702, 6.63037),4: (13.4009, -284.659, 4.03184),5: (226.343, -315.485, 13.9557),6: None,7: None,8: None,10: (-61.0232, -192.343, 11.1546),11: (339.465, -461.702, 6.63037)},INVASION_TORTUGA: {1: (77.7542, -392.561, 1.39463),2: (107.408, -401.547, 0.175161),3: (316.505, -256.694, 0.729866),4: (337.154, -174.624, 0.432898),5: None,6: None,7: None,10: (77.7542, -392.561, 1.39463),11: (316.505, -256.694, 0.729866)},INVASION_DEL_FUEGO: {1: (-1300.7, -493.171, 0.849964),2: (-1292.32, -551.34, 3.20932),3: (-1489.03, 362.417, 5.01261),4: (-1277.69, 554.611, 1.51438),5: (-1089.08, -190.335, 0.694368),6: None,7: (-1177.85, 18.5966, 0.722509),8: None,10: (-1300.7, -493.171, 0.849964),11: (-1489.03, 362.417, 5.01261),12: (-1277.69, 554.611, 1.51438)}}

def getEnemyStartPathPos(holiday, zone):
    return ENEMY_START_PATH_POS_LIST[holiday][zone]


TOTAL_CAPTURE_POINT_LIST = {INVASION_PORT_ROYAL: 7,INVASION_TORTUGA: 7,INVASION_DEL_FUEGO: 7,HolidayGlobals.getHolidayName(INVASION_PORT_ROYAL): 7,HolidayGlobals.getHolidayName(INVASION_TORTUGA): 7,HolidayGlobals.getHolidayName(INVASION_DEL_FUEGO): 7}

def getTotalCapturePoints(holiday):
    return TOTAL_CAPTURE_POINT_LIST[holiday]


CAPTURE_POINT_TARGET_LIST = {INVASION_PORT_ROYAL: {1: [1, 5, 7],2: [2, 4, 6, 7],3: [2, 3, 4, 6, 7],4: [1, 5, 7],5: [3, 4, 6, 7],6: [6, 7],7: [5, 7],8: [7],10: [1, 5, 7],11: [2, 4, 6, 7]},INVASION_TORTUGA: {1: [1, 3, 5, 7],2: [1, 3, 5, 7],3: [2, 4, 6, 7],4: [2, 4, 6, 7],5: [5, 7],6: [6, 7],7: [7],10: [1, 3, 5, 7],11: [2, 4, 6, 7]},INVASION_DEL_FUEGO: {1: [1, 4, 7],2: [1, 4, 7],3: [2, 5, 7],4: [3, 6, 7],5: [4, 7],6: [6, 7],7: [5, 7],8: [7],10: [1, 4, 7],11: [2, 5, 7],12: [3, 6, 7]}}

def getCapturePointTargetList(holiday):
    return CAPTURE_POINT_TARGET_LIST[holiday]


CAPTURE_POINT_HP_LIST = {INVASION_PORT_ROYAL: {1: 5000,2: 5000,3: 5000,4: 5000,5: 14000,6: 14000,7: 40000},INVASION_TORTUGA: {1: 5000,2: 5000,3: 5000,4: 5000,5: 12000,6: 12000,7: 40000},INVASION_DEL_FUEGO: {1: 5000,2: 5000,3: 5000,4: 14000,5: 14000,6: 14000,7: 40000}}

def getCapturePointHp(holiday, zone):
    return CAPTURE_POINT_HP_LIST[holiday][zone]


CAPTURE_POINT_PATH_POS_LIST = {INVASION_PORT_ROYAL: {1: Point3(-59.1151, -187.478, 12.366),2: Point3(372.508, -466.794, 3.98782),3: Point3(130.951, -261.169, 38.2806),4: Point3(391.335, -247.478, 13.9557),5: Point3(-126.583, 64.0033, 35.8098),6: Point3(221.399, 80.8056, 35.6117),7: Point3(47.3903, 350.277, 85.5975)},INVASION_TORTUGA: {1: Point3(57.6055, -346.396, 5.64634),2: Point3(222.423, -169.901, 6.71903),3: Point3(43.6479, -120.363, 16.7635),4: Point3(281.659, 1.409, 8.39594),5: Point3(-28.37, 58.491, 30.5733),6: Point3(318.294, 126.935, 12.182),7: None},INVASION_DEL_FUEGO: {1: Point3(-1244.69, -547.2, 11.288),2: Point3(-1336.16, 268.509, 10.6513),3: Point3(-1260.94, 471.589, 5.94097),4: None,5: Point3(-1199.04, 55.6291, 2.19007),6: Point3(-918.66, 400.498, 15.0496),7: None}}

def getCapturePointPathPos(holiday, zone):
    return CAPTURE_POINT_PATH_POS_LIST[holiday][zone]


CAPTURE_POINT_LOW_HP_PERCENT_LIST = {INVASION_PORT_ROYAL: 0.25,INVASION_TORTUGA: 0.25,INVASION_DEL_FUEGO: 0.25}

def getCapturePointLowHpPercent(holiday):
    return CAPTURE_POINT_LOW_HP_PERCENT_LIST[holiday]


CAPTURE_POINT_TARGETS = {INVASION_DEL_FUEGO: {4: {1: [1, 2],2: [1, 2],5: [0, 3]}}}

def getCapturePointTargets(holiday, zone, spawnZone):
    if CAPTURE_POINT_TARGETS.get(holiday) and CAPTURE_POINT_TARGETS.get(holiday).get(zone):
        return CAPTURE_POINT_TARGETS.get(holiday).get(zone).get(spawnZone)
    return None


MAIN_CAPTURE_POINT_TARGETS = {INVASION_TORTUGA: {1: [1, 2],2: [1, 2],3: [0, 3],4: [0, 3],5: [1, 2],6: [0, 3],7: [1, 2],10: [1, 2],11: [0, 3]},INVASION_DEL_FUEGO: {1: [0, 3],2: [0, 3],3: [1, 4, 5, 7, 8],4: [2],5: [0, 3],6: [2],7: [1, 4, 5, 7, 8],8: [6, 9],10: [1, 4, 5, 7, 8],11: [1, 4, 5, 7, 8],12: [1, 4, 5, 7, 8]}}

def getMainCapturePointTargets(holiday, spawnZone):
    if MAIN_CAPTURE_POINT_TARGETS.get(holiday):
        return MAIN_CAPTURE_POINT_TARGETS.get(holiday).get(spawnZone)
    return None


MAIN_CAPTURE_POINT_HP_POS = {HolidayGlobals.getHolidayName(INVASION_PORT_ROYAL): Point3(290, 620, 0),HolidayGlobals.getHolidayName(INVASION_TORTUGA): Point3(130, 230, 0),HolidayGlobals.getHolidayName(INVASION_DEL_FUEGO): Point3(600, -100, 0)}

def getMainCapturePointHpPos(holiday):
    return MAIN_CAPTURE_POINT_HP_POS[holiday]


BOSS_ENEMY_LIST = {INVASION_PORT_ROYAL: AvatarTypes.JollyRoger,INVASION_TORTUGA: AvatarTypes.JollyRoger,INVASION_DEL_FUEGO: AvatarTypes.JollyRoger}

def getBossEnemy(holiday):
    return BOSS_ENEMY_LIST[holiday]


BOSS_ID_LIST = {INVASION_PORT_ROYAL: '1248740229.97robrusso',INVASION_TORTUGA: '1248740229.97robrusso',INVASION_DEL_FUEGO: '1248740229.97robrusso'}

def getBossId(holiday):
    return BOSS_ID_LIST[holiday]


BOSS_TRIGGER_LIST = {INVASION_PORT_ROYAL: [(1, 5), (2, 4, 6)],INVASION_TORTUGA: [(1, 3, 5), (2, 4, 6)],INVASION_DEL_FUEGO: [(1, 4), (2, 5), (3, 6)]}

def getBossTriggers(holiday):
    return BOSS_TRIGGER_LIST[holiday]


BOSS_NPC_LIST = {INVASION_PORT_ROYAL: ([1.0, 1.0, 1.0, 0.5, 0.11], [1.0, 1.25, 2.0, 0.6, 0.1], [1.0, 1.5, 3.0, 0.7, 0.09], [1.0, 1.75, 4.0, 0.8, 0.08], [1.0, 2.0, 5.0, 0.9, 0.07], [1.0, 2.25, 6.0, 1.0, 0.06], [1.0, 2.5, 7.0, 1.1, 0.05], [1.0, 2.75, 8.0, 1.2, 0.04], [1.0, 3.0, 9.0, 1.3, 0.03], [1.0, 3.25, 10.0, 1.4, 0.02], [1.0, 3.5, 11.0, 1.5, 0.01], [1.0, 3.75, 12.0, 1.6, 0.008], [1.0, 4.0, 13.0, 1.7, 0.006], [1.0, 4.25, 14.0, 1.8, 0.004], [1.0, 4.5, 15.0, 1.9, 0.002], [1.0, 4.75, 16.0, 2.0, 0.001], [1.0, 5.0, 17.0, 2.1, 0.001], [1.0, 5.25, 18.0, 2.2, 0.001]),INVASION_TORTUGA: ([1.0, 1.0, 1.0, 0.5, 0.11], [1.0, 1.25, 2.0, 0.6, 0.1], [1.0, 1.5, 3.0, 0.7, 0.09], [1.0, 1.75, 4.0, 0.8, 0.08], [1.0, 2.0, 5.0, 0.9, 0.07], [1.0, 2.25, 6.0, 1.0, 0.06], [1.0, 2.5, 7.0, 1.1, 0.05], [1.0, 2.75, 8.0, 1.2, 0.04], [1.0, 3.0, 9.0, 1.3, 0.03], [1.0, 3.25, 10.0, 1.4, 0.02], [1.0, 3.5, 11.0, 1.5, 0.01], [1.0, 3.75, 12.0, 1.6, 0.008], [1.0, 4.0, 13.0, 1.7, 0.006], [1.0, 4.25, 14.0, 1.8, 0.004], [1.0, 4.5, 15.0, 1.9, 0.002], [1.0, 4.75, 16.0, 2.0, 0.001], [1.0, 5.0, 17.0, 2.1, 0.001], [1.0, 5.25, 18.0, 2.2, 0.001]),INVASION_DEL_FUEGO: ([1.0, 1.0, 1.0, 0.5, 0.11], [1.0, 1.25, 2.0, 0.6, 0.1], [1.0, 1.5, 3.0, 0.7, 0.09], [1.0, 1.75, 4.0, 0.8, 0.08], [1.0, 2.0, 5.0, 0.9, 0.07], [1.0, 2.25, 6.0, 1.0, 0.06], [1.0, 2.5, 7.0, 1.1, 0.05], [1.0, 2.75, 8.0, 1.2, 0.04], [1.0, 3.0, 9.0, 1.3, 0.03], [1.0, 3.25, 10.0, 1.4, 0.02], [1.0, 3.5, 11.0, 1.5, 0.01], [1.0, 3.75, 12.0, 1.6, 0.008], [1.0, 4.0, 13.0, 1.7, 0.006], [1.0, 4.25, 14.0, 1.8, 0.004], [1.0, 4.5, 15.0, 1.9, 0.002], [1.0, 4.75, 16.0, 2.0, 0.001], [1.0, 5.0, 17.0, 2.1, 0.001], [1.0, 5.25, 18.0, 2.2, 0.001])}

def getBossSkills(holiday, numPlayers):
    if numPlayers < 6:
        return BOSS_NPC_LIST[holiday][0]
    elif numPlayers < 11:
        return BOSS_NPC_LIST[holiday][1]
    elif numPlayers < 16:
        return BOSS_NPC_LIST[holiday][2]
    elif numPlayers < 21:
        return BOSS_NPC_LIST[holiday][3]
    elif numPlayers < 26:
        return BOSS_NPC_LIST[holiday][4]
    elif numPlayers < 31:
        return BOSS_NPC_LIST[holiday][5]
    elif numPlayers < 36:
        return BOSS_NPC_LIST[holiday][6]
    elif numPlayers < 41:
        return BOSS_NPC_LIST[holiday][7]
    elif numPlayers < 46:
        return BOSS_NPC_LIST[holiday][8]
    elif numPlayers < 51:
        return BOSS_NPC_LIST[holiday][9]
    elif numPlayers < 56:
        return BOSS_NPC_LIST[holiday][10]
    elif numPlayers < 61:
        return BOSS_NPC_LIST[holiday][11]
    elif numPlayers < 66:
        return BOSS_NPC_LIST[holiday][12]
    elif numPlayers < 71:
        return BOSS_NPC_LIST[holiday][13]
    elif numPlayers < 76:
        return BOSS_NPC_LIST[holiday][14]
    elif numPlayers < 81:
        return BOSS_NPC_LIST[holiday][15]
    elif numPlayers < 86:
        return BOSS_NPC_LIST[holiday][16]
    else:
        return BOSS_NPC_LIST[holiday][17]


BOSS_SPAWN_LIST = {INVASION_PORT_ROYAL: {0: 10,1: 10,2: 11,3: 11,4: 11,5: 10,6: 11},INVASION_TORTUGA: {0: 10,1: 10,2: 11,3: 10,4: 11,5: 10,6: 11},INVASION_DEL_FUEGO: {0: 10,1: 10,2: 11,3: 12,4: 10,5: 11,6: 12}}

def getBossSpawnZone(holiday, zone):
    return BOSS_SPAWN_LIST[holiday][zone]


WARNING_TIME = {INVASION_PORT_ROYAL: 1800,INVASION_TORTUGA: 1800,INVASION_DEL_FUEGO: 1800}

def getExtraBossStats(numPlayers):
    if numPlayers < 3:
        return (0.0, 0)
    elif numPlayers < 5:
        return (0.05, 1)
    elif numPlayers < 7:
        return (0.1, 1)
    elif numPlayers < 9:
        return (0.15, 2)
    elif numPlayers < 11:
        return (0.2, 2)
    elif numPlayers < 13:
        return (0.25, 2)
    elif numPlayers < 15:
        return (0.3, 3)
    elif numPlayers < 17:
        return (0.35, 3)
    elif numPlayers < 19:
        return (0.4, 4)
    elif numPlayers < 21:
        return (0.45, 4)
    elif numPlayers < 25:
        return (0.5, 5)
    elif numPlayers < 29:
        return (0.55, 5)
    elif numPlayers < 33:
        return (0.6, 5)
    elif numPlayers < 37:
        return (0.65, 6)
    elif numPlayers < 41:
        return (0.7, 6)
    else:
        return (0.75, 6)


def getEnemyStats(numPlayers):
    if numPlayers < 21:
        return (1.25, 0.8)
    elif numPlayers < 26:
        return (1.3, 0.8)
    elif numPlayers < 31:
        return (1.35, 0.75)
    elif numPlayers < 36:
        return (1.4, 0.7)
    elif numPlayers < 41:
        return (1.5, 0.65)
    elif numPlayers < 46:
        return (1.6, 0.6)
    elif numPlayers < 51:
        return (1.7, 0.55)
    elif numPlayers < 56:
        return (1.8, 0.5)
    elif numPlayers < 61:
        return (1.9, 0.45)
    elif numPlayers < 66:
        return (2.0, 0.4)
    elif numPlayers < 71:
        return (2.1, 0.35)
    elif numPlayers < 76:
        return (2.2, 0.3)
    elif numPlayers < 81:
        return (2.25, 0.25)
    elif numPlayers < 86:
        return (2.3, 0.2)
    elif numPlayers < 91:
        return (2.35, 0.15)
    elif numPlayers < 96:
        return (2.4, 0.1)
    elif numPlayers < 101:
        return (2.45, 0.1)
    elif numPlayers < 106:
        return (2.5, 0.1)
    elif numPlayers < 111:
        return (2.55, 0.1)
    else:
        return (2.6, 0.1)


def getWarningTime(holiday):
    return WARNING_TIME[holiday]


DELAYED_START_LIST = {INVASION_PORT_ROYAL: 28.0,INVASION_TORTUGA: 28.0,INVASION_DEL_FUEGO: 28.0}

def getDelayedStart(holiday):
    return DELAYED_START_LIST[holiday]


DELAYED_END_LIST = {INVASION_PORT_ROYAL: 16.0,INVASION_TORTUGA: 24.0,INVASION_DEL_FUEGO: 24.0}

def getDelayedEnd(holiday):
    return DELAYED_END_LIST[holiday]


SEA_ZONE_LIST = {INVASION_PORT_ROYAL: {1: 10,2: 11,3: 11,4: 10,5: 11,6: 11,7: 10,8: 10},INVASION_TORTUGA: {1: 10,2: 10,3: 11,4: 11,5: 10,6: 11,7: 10},INVASION_DEL_FUEGO: {1: 10,2: 10,3: 11,4: 12,5: 10,6: 11,7: 12,8: 10}}

def getSeaZone(holiday, zone):
    return SEA_ZONE_LIST[holiday][zone]


SPAWN_STAGGER = 2.0

def getExtraWaveSpawnStagger(numPlayers):
    if numPlayers < 3:
        return 5.0
    elif numPlayers < 5:
        return 4.5
    elif numPlayers < 7:
        return 4.0
    elif numPlayers < 9:
        return 3.5
    elif numPlayers < 11:
        return 3.0
    elif numPlayers < 13:
        return 2.5
    elif numPlayers < 15:
        return 2.0
    elif numPlayers < 17:
        return 1.5
    elif numPlayers < 19:
        return 1.0
    elif numPlayers < 21:
        return 0.5
    else:
        return 0.0


CAPTURE_POINT_UPDATE_WAIT = 1.0
CAPTURE_POINT_HP_SPHERE_SIZES = {INVASION_PORT_ROYAL: 70,INVASION_TORTUGA: 50,INVASION_DEL_FUEGO: 60}

def getCapturePointHpSphereSize(holiday):
    return CAPTURE_POINT_HP_SPHERE_SIZES[holiday]


FOG_COLORS = {INVASION_PORT_ROYAL: Vec4(0.1, 0.12, 0.03, 1),INVASION_TORTUGA: Vec4(0.1, 0.12, 0.03, 1),INVASION_DEL_FUEGO: Vec4(0.1, 0.12, 0.03, 1)}

def getFogColor(holiday):
    return FOG_COLORS[holiday]


FOG_RANGES = {INVASION_PORT_ROYAL: (0.0, 150.0),INVASION_TORTUGA: (0.0, 150.0),INVASION_DEL_FUEGO: (0.0, 150.0)}

def getFogRange(holiday):
    return FOG_RANGES[holiday]


FAR_FOG_RANGES = {INVASION_PORT_ROYAL: (350.0, 2000.0),INVASION_TORTUGA: (350.0, 2000.0),INVASION_DEL_FUEGO: (350.0, 2000.0)}

def getFarFogRange(holiday):
    return FAR_FOG_RANGES[holiday]


INVASION_LIKELIHOOD = {INVASION_PORT_ROYAL: 40,INVASION_TORTUGA: 30,INVASION_DEL_FUEGO: 30}

def getInvasionLikelihood(holiday):
    return INVASION_LIKELIHOOD[holiday]


PERCENT_REMAINING_FOR_NEW_WAVE = 0.1

def getPercentRemainingForExtraWave(holiday, numPlayers):
    if holiday == INVASION_DEL_FUEGO:
        if numPlayers < 36:
            return 0.5
        elif numPlayers < 41:
            return 0.6
        else:
            return 0.7
    elif numPlayers < 11:
        return 0.0
    elif numPlayers < 16:
        return 0.1
    elif numPlayers < 21:
        return 0.2
    elif numPlayers < 26:
        return 0.3
    elif numPlayers < 31:
        return 0.4
    elif numPlayers < 36:
        return 0.5
    elif numPlayers < 41:
        return 0.6
    else:
        return 0.7


MAIN_ZONE_BONUS = 0.4
ENEMY_BONUS = 0.5
BARRICADE_BONUS = 0.15
WAVE_BONUS = 0.2
MAX_REP_EARNED = 800
POST_INVASION_DURATION = 3 * 24 * 60 * 60
POST_INVASION_FIRE_DURATION = 3600
JR_PATHS = {INVASION_PORT_ROYAL: {(0, 1): [Point3(-43.8825, -239.528, 3.03623), Point3(-62.3444, -166.508, 17.9701)],(1, 5): [Point3(-89.7967, -82.5102, 34.9792), Point3(-125.313, 18.7841, 35.2021), Point3(-119.152, 65.9646, 36.4963)],(5, 7): [Point3(-91.2655, 97.4878, 39.968), Point3(-74.2463, 103.105, 42.419), Point3(-26.6557, 176.269, 58.5433), Point3(-11.1696, 257.124, 78.2706), Point3(-5.13773, 281.093, 84.1871), Point3(26.7467, 335.128, 84.2789)],(0, 2): [Point3(399.478, -452.454, 3.10073), Point3(336.32, -460.439, 6.96459)],(2, 4): [Point3(297.142, -401.346, 13.9557), Point3(369.162, -330.924, 13.9557), Point3(401.266, -253.636, 13.9557)],(4, 6): [Point3(374.898, -201.071, 13.9557), Point3(358.458, -119.725, 14.7235), Point3(408.256, -97.515, 27.8583), Point3(418.754, -74.8395, 32.1563), Point3(413.975, -52.8406, 32.5726), Point3(383.277, -41.3519, 32.8422), Point3(376.512, -16.9647, 40.2479), Point3(355.754, 25.1279, 41.2657), Point3(328.945, 57.7713, 41.2657), Point3(283.197, 76.1017, 41.2657), Point3(227.305, 82.0586, 35.673)],(6, 7): [Point3(200.214, 109.271, 36.33), Point3(195.359, 119.363, 37.4573), Point3(191.927, 147.958, 38.7167), Point3(177.632, 201.103, 45.168), Point3(157.167, 211.012, 52.6092), Point3(113.697, 223.263, 65.7057), Point3(97.7321, 255.417, 77.6612), Point3(92.3337, 277.835, 83.735), Point3(72.4895, 334.517, 84.2789)]},INVASION_TORTUGA: {(0, 1): [Point3(67.0641, -386.78, 1.77451), Point3(47.4459, -360.073, 4.26133)],(1, 3): [Point3(20.8564, -302.938, 6.96829), Point3(2.31014, -265.455, 7.93029), Point3(10.7063, -202.721, 9.40618), Point3(54.9207, -127.113, 15.4122)],(3, 5): [Point3(42.5136, -70.0453, 26.8595), Point3(23.0176, -46.1746, 29.1847), Point3(19.765, -40.8399, 29.5809), Point3(-4.84028, -27.9147, 30.6739), Point3(-32.9961, 7.57262, 29.534), Point3(-36.8601, 14.503, 29.4988), Point3(-33.6866, 33.086, 30.1041), Point3(-32.0029, 75.2962, 30.3034)],(5, 7): [Point3(-10.7064, 110.148, 30.7391), Point3(11.5704, 113.84, 31.1967), Point3(53.3613, 111.254, 31.2772)],(0, 2): [Point3(293.969, -245.331, 2.31207), Point3(258.291, -172.621, 5.27697)],(2, 4): [Point3(223.905, -63.0303, 8.73826), Point3(241.803, -27.9764, 8.91244), Point3(280.385, -2.24409, 8.3111)],(4, 6): [Point3(295.033, 6.26949, 8.06414), Point3(322.144, 21.6205, 7.78477), Point3(341.453, 55.5907, 7.24173), Point3(321.157, 127.525, 11.6012)],(6, 7): [Point3(280.984, 151.618, 24.6632), Point3(264.343, 163.028, 29.5431), Point3(226.525, 186.121, 31.015), Point3(168.767, 176.928, 31.2232), Point3(121.853, 118.714, 30.2191), Point3(116.232, 112.712, 30.1649), Point3(106.008, 84.7669, 29.7169), Point3(96.0121, 71.9735, 29.7394)]},INVASION_DEL_FUEGO: {(0, 1): [Point3(-1265.08, -527.948, 7.72675)],(1, 4): [Point3(-1246.63, -473.303, 4.10242), Point3(-1214.06, -423.89, 35.6783), Point3(-1167.41, -345.169, 35.6835), Point3(-1137.54, -294.761, 2.01549), Point3(-1096.93, -261.442, 1.23705)],(4, 7): [Point3(-1029.58, -199.25, 1.99986), Point3(-998.646, -154.637, 2.1946)],(0, 2): [Point3(-1489.56, 363.81, 5.01256), Point3(-1362.69, 254.972, 9.26481)],(2, 5): [Point3(-1324.21, 200.345, 11.9518), Point3(-1237.56, 177.173, 9.89098), Point3(-1201.42, 58.2305, 2.27976)],(5, 7): [Point3(-1116.76, 46.3089, 4.93439), Point3(-1060.53, -25.0102, 1.86531), Point3(-1006.15, -84.6436, 2.19162)],(0, 3): [Point3(-1264.8, 531.995, 2.73673), Point3(-1257.18, 497.701, 4.56281)],(3, 6): [Point3(-1184.4, 469.418, 12.3011), Point3(-1141.76, 430.489, 16.1967), Point3(-1100.93, 420.015, 19.1489), Point3(-983.191, 443.208, 16.1529), Point3(-924.758, 407.871, 15.0837), Point3(-912.644, 339.663, 16.3741), Point3(-920.645, 312.75, 17.7257)],(6, 7): [Point3(-971.018, 213.917, 27.0729), Point3(-963.09, 176.192, 29.7741), Point3(-910.649, 133.697, 27.1761), Point3(-910.866, 56.3491, 13.2449), Point3(-991.102, 11.8028, 3.52431), Point3(-1015.01, -64.5912, 2.18138), Point3(-993.32, -92.5042, 2.29201)]}}
JR_POINTS = {INVASION_PORT_ROYAL: {10: [0, 1, 5, 7],11: [0, 2, 4, 6, 7]},INVASION_TORTUGA: {10: [0, 1, 3, 5, 7],11: [0, 2, 4, 6, 7]},INVASION_DEL_FUEGO: {10: [0, 1, 4, 7],11: [0, 2, 5, 7],12: [0, 3, 6, 7]}}

def getJollyPath(holidayId, startPos, endPos, spawnZone):
    points = JR_POINTS[holidayId][spawnZone]
    startIndex = points.index(startPos)
    endIndex = points.index(endPos)
    path = []
    for i in range(startIndex, endIndex):
        path.extend(JR_PATHS[holidayId][points[i], points[i + 1]])

    return path