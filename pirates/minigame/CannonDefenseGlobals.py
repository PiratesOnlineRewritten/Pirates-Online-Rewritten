from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals
from pirates.inventory import ItemGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
DAZED_ENABLED = True
PLAYER_AFK_TIMEOUT = 300
GAME_OVER_WAIT = 30
ENEMY_DIFFICULTY_INCREASE = 0.1
ENEMY_LINEAR_HEALTH_DIFFICULTY = 300
MOUSE_SENSITIVITY_H = 0.14
MOUSE_SENSITIVITY_P = 0.08
KEYBOARD_RATE = 250
CANNON_HPR = (
 -120.38, -4.96, 0)
SHIP_FADEIN = 4
SHIP_FADEOUT = 4.0
SHIP_DELAY = 1.0
SHIP_SCALE = 0.4
SHIP_SINK_DURATION_SCALE = 0.5
SHIP_STATE_NONE = 0
SHIP_STATE_STEALING = 1
SHIP_STATE_HASTREASURE = 2
SHIP_STATE_HASBNOTES = 3
FLAMING_BARREL_VELOCITY = 90
MAX_BARREL_FLIGHT_DURATION = 14.0
BARREL_GRAVITY = 0.07
REPEATER_RELOAD_MODIFIER = 0.1
REPEATER_DAMAGE_MODIFIER = 0.1
DAMAGE_TO_GOLD_RATE = 0.002
SHIP_TREASURE_THROTTLE = 0.5
SHIPS_PER_PATH_THRESHOLD = 3
MIN_SHIP_HEALTH_PER_PLAYER = 900
MINE_TREASURE_START = 1000
MINE_TREASURE_AWARD = 0.05
RESULT_SCREEN_DURATION = 15
VICTORY_SCREEN_DURATION = 45
TUTORIAL_DURATION = 20
GAME_FULL_MSG_TIME = 3
INFINITE_WAVE = False
ALLOW_IDLE = True
LIGHTGALLEON = 0
LIGHTSLOOP = 1
LIGHTFRIGATE = 2
STANDARDGALLEON = 3
STANDARDSLOOP = 4
STANDARDFRIGATE = 5
WARSHIPGALLEON = 6
WARSHIPSLOOP = 7
WARSHIPFRIGATE = 8
HEAVYWARSHIPGALLEON = 9
HEAVYWARSHIPSLOOP = 10
HEAVYWARSHIPFRIGATE = 11
SHIP_HEALTH_COLORS = [
 (
  1.0, 0.0, 0.0, 1.0), (1.0, 0.5, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0)]
SHIP_SMOKE_SCREEN_SPEED_PERCENTAGE = 0.25
SHIP_SMOKE_ICE_SHOT_PERCENTAGE = 0.1
NAVY_CANNON_EXP_PER_DAMAGE = 0.05
NAVY_CANNON_EXP_PER_DAMAGE_OTHER = 0.015
CANNON_EXP_PER_DAMAGE = 0.0006
BANKNOTES_PER_DAMAGE = 0.01
FREEBOOTER_MAX_AMMO_SLOTS = 2
FREEBOOTER_LAST_AMMO_AVAILABLE = InventoryType.DefenseCannonMine
waveData = [{'maxShipsOnScreenPerPlayer': [3, 4, 5, 6],'miniWaveData': {0: {'duration': 30,'basicShips': [(LIGHTSLOOP, 1.0)]},1: {'duration': 30,'basicShips': [(LIGHTSLOOP, 0.8), (LIGHTGALLEON, 0.2)]}}}, {'maxShipsOnScreenPerPlayer': [3, 4, 5, 6],'miniWaveData': {0: {'duration': 15,'basicShips': [(LIGHTGALLEON, 0.5), (LIGHTSLOOP, 0.5)]},1: {'duration': 15,'basicShips': [(LIGHTGALLEON, 1.0)]},2: {'duration': 30,'basicShips': [(LIGHTGALLEON, 0.5), (LIGHTSLOOP, 0.5)],'bossShips': [LIGHTFRIGATE, LIGHTFRIGATE, LIGHTFRIGATE]}}}, {'maxShipsOnScreenPerPlayer': [3, 4, 5, 6],'miniWaveData': {0: {'duration': 15,'basicShips': [(LIGHTGALLEON, 0.2), (LIGHTSLOOP, 0.8)]},1: {'duration': 15,'basicShips': [(LIGHTGALLEON, 0.5), (LIGHTFRIGATE, 0.4), (LIGHTSLOOP, 0.1)]},2: {'duration': 15,'basicShips': [(LIGHTFRIGATE, 1.0)]},3: {'duration': 15,'basicShips': [(LIGHTGALLEON, 0.5), (LIGHTFRIGATE, 0.5)],'bossShips': [STANDARDGALLEON]}}}, {'maxShipsOnScreenPerPlayer': [4, 6, 8, 10],'miniWaveData': {0: {'duration': 30,'basicShips': [(LIGHTGALLEON, 1.0)],'bossShips': [STANDARDGALLEON]},1: {'duration': 30,'basicShips': [(LIGHTFRIGATE, 0.8), (LIGHTGALLEON, 0.2)],'bossShips': [STANDARDGALLEON, STANDARDGALLEON, STANDARDGALLEON]}}}, {'maxShipsOnScreenPerPlayer': [4, 6, 8, 10],'miniWaveData': {0: {'duration': 60,'basicShips': [(STANDARDSLOOP, 0.4), (LIGHTSLOOP, 0.2), (LIGHTGALLEON, 0.2), (LIGHTFRIGATE, 0.2)],'bossShips': [STANDARDGALLEON, STANDARDGALLEON, STANDARDGALLEON, STANDARDGALLEON, STANDARDGALLEON, STANDARDGALLEON]}}}, {'maxShipsOnScreenPerPlayer': [4, 6, 8, 10],'miniWaveData': {0: {'duration': 30,'basicShips': [(LIGHTSLOOP, 0.55), (STANDARDSLOOP, 0.45)],'bossShips': [STANDARDGALLEON, STANDARDGALLEON]},1: {'duration': 45,'basicShips': [(LIGHTGALLEON, 0.5), (LIGHTFRIGATE, 0.5)],'bossShips': [STANDARDGALLEON, STANDARDGALLEON, WARSHIPSLOOP]}}}, {'maxShipsOnScreenPerPlayer': [4, 6, 8, 10],'miniWaveData': {0: {'duration': 30,'basicShips': [(LIGHTSLOOP, 1.0)],'bossShips': [STANDARDFRIGATE, STANDARDFRIGATE, STANDARDFRIGATE]},1: {'duration': 30,'basicShips': [(LIGHTGALLEON, 0.5), (LIGHTFRIGATE, 0.5)],'bossShips': [WARSHIPSLOOP, WARSHIPSLOOP]},2: {'duration': 30,'basicShips': [(STANDARDGALLEON, 0.5), (LIGHTSLOOP, 0.5)],'bossShips': [WARSHIPGALLEON]}}}, {'maxShipsOnScreenPerPlayer': [4, 5, 8, 10],'miniWaveData': {0: {'duration': 45,'basicShips': [(STANDARDSLOOP, 0.65), (LIGHTFRIGATE, 0.35)],'bossShips': [WARSHIPGALLEON, WARSHIPGALLEON]},1: {'duration': 45,'basicShips': [(WARSHIPSLOOP, 0.4), (STANDARDFRIGATE, 0.6)],'bossShips': [WARSHIPGALLEON, WARSHIPGALLEON, WARSHIPGALLEON, WARSHIPGALLEON]}}}, {'maxShipsOnScreenPerPlayer': [4, 6, 8, 10],'miniWaveData': {0: {'duration': 15,'basicShips': [(STANDARDSLOOP, 0.7), (LIGHTGALLEON, 0.2), (LIGHTSLOOP, 0.1)],'bossShips': [WARSHIPFRIGATE, WARSHIPFRIGATE]},1: {'duration': 30,'basicShips': [(STANDARDSLOOP, 0.7), (LIGHTGALLEON, 0.2), (LIGHTSLOOP, 0.1)]},2: {'duration': 30,'basicShips': [(LIGHTGALLEON, 0.5), (LIGHTSLOOP, 0.5)],'bossShips': [STANDARDGALLEON, STANDARDGALLEON, STANDARDGALLEON, STANDARDGALLEON, STANDARDGALLEON, STANDARDGALLEON]},3: {'duration': 30,'basicShips': [(STANDARDSLOOP, 0.5), (LIGHTSLOOP, 0.5)],'bosShips': [WARSHIPFRIGATE, WARSHIPSLOOP, WARSHIPGALLEON, WARSHIPFRIGATE]}}}, {'maxShipsOnScreenPerPlayer': [4, 6, 8, 10],'miniWaveData': {0: {'duration': 60,'basicShips': [(STANDARDGALLEON, 0.5), (LIGHTGALLEON, 0.5)],'bossShips': [STANDARDGALLEON, WARSHIPGALLEON]},1: {'duration': 60,'basicShips': [(LIGHTSLOOP, 0.4), (WARSHIPSLOOP, 0.2), (STANDARDSLOOP, 0.4)],'bossShips': [HEAVYWARSHIPSLOOP, HEAVYWARSHIPSLOOP, HEAVYWARSHIPSLOOP, HEAVYWARSHIPSLOOP]}}}, {'maxShipsOnScreenPerPlayer': [5, 7, 9, 11],'miniWaveData': {0: {'duration': 45,'basicShips': [(LIGHTSLOOP, 1.0)],'bossShips': [WARSHIPSLOOP, WARSHIPSLOOP]},1: {'duration': 30,'basicShips': [(STANDARDGALLEON, 0.35), (STANDARDSLOOP, 0.35), (LIGHTFRIGATE, 0.3)],'bossShips': [WARSHIPGALLEON, WARSHIPSLOOP, WARSHIPSLOOP]},2: {'duration': 45,'basicShips': [(STANDARDGALLEON, 0.2), (WARSHIPSLOOP, 0.2), (LIGHTFRIGATE, 0.3), (STANDARDSLOOP, 0.3)],'bossShips': [WARSHIPGALLEON, HEAVYWARSHIPGALLEON]}}}, {'maxShipsOnScreenPerPlayer': [5, 7, 9, 11],'miniWaveData': {0: {'duration': 60,'basicShips': [(STANDARDFRIGATE, 0.4), (LIGHTFRIGATE, 0.6)],'bossShips': [WARSHIPFRIGATE, HEAVYWARSHIPGALLEON]},1: {'duration': 75,'basicShips': [(STANDARDGALLEON, 0.25), (STANDARDSLOOP, 0.75)],'bossShips': [WARSHIPGALLEON, WARSHIPGALLEON, HEAVYWARSHIPFRIGATE]}}}, {'maxShipsOnScreenPerPlayer': [5, 7, 9, 11],'miniWaveData': {0: {'duration': 30,'basicShips': [(STANDARDSLOOP, 0.3), (STANDARDFRIGATE, 0.3), (LIGHTGALLEON, 0.3), (LIGHTSLOOP, 0.1)]},1: {'duration': 45,'basicShips': [(STANDARDGALLEON, 0.35), (LIGHTFRIGATE, 0.25), (STANDARDSLOOP, 0.15)],'bossShips': [WARSHIPSLOOP, WARSHIPSLOOP]},2: {'duration': 60,'basicShips': [(STANDARDGALLEON, 0.5), (STANDARDSLOOP, 0.3), (STANDARDFRIGATE, 0.2)],'bossShips': [WARSHIPSLOOP, HEAVYWARSHIPGALLEON, HEAVYWARSHIPFRIGATE, WARSHIPFRIGATE, HEAVYWARSHIPGALLEON, HEAVYWARSHIPFRIGATE]},3: {'duration': 30,'basicShips': [(WARSHIPFRIGATE, 0.2), (WARSHIPGALLEON, 0.2), (STANDARDGALLEON, 0.2), (LIGHTFRIGATE, 0.2), (LIGHTSLOOP, 0.2)],'bossShips': [HEAVYWARSHIPFRIGATE, HEAVYWARSHIPSLOOP, HEAVYWARSHIPFRIGATE, HEAVYWARSHIPSLOOP, HEAVYWARSHIPSLOOP]}}}]
SHIP_BEHAVIOR_TO_LOGO = {'normal': ShipGlobals.Logos.NoLogo,'barrels': ShipGlobals.Logos.Bandit_Scorpion,'speedIncrease': ShipGlobals.Logos.Bandit_Bull,'variableSpeed': ShipGlobals.Logos.Bandit_Claw,'bloodlust': ShipGlobals.Logos.Bandit_Dagger}
MAX_BARRELS_ALLOWED = 5
BLOOD_LUST_TIME_BETWEEN_BARRELS_RANGE = (
 12, 16)
TIME_BETWEEN_BARREL_ATTACKS_RANGE = (
 14, 20)
TIME_BETWEEN_BARRELS_IN_SAME_ATTACK = 1
shipStats = {LIGHTSLOOP: {'shipHp': 280,'mastHp': [280, 0, 0, 0, 0],'speedRange': [10, 12],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [75, 76],'stealingSpeed': 74,'treasureReturnRate': 0.5,'behavior': 'normal','style': ShipGlobals.Styles.Bandit01,'shipModel': ShipGlobals.NAVY_FERRET,'collisionRadius': 100,'healthBarHeight': 100.0},LIGHTGALLEON: {'shipHp': 600,'mastHp': [800, 800, 0, 800, 0],'speedRange': [7, 8],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [100, 101],'stealingSpeed': 99,'treasureReturnRate': 0.5,'behavior': 'normal','style': ShipGlobals.Styles.Bandit01,'shipModel': ShipGlobals.NAVY_BULWARK,'collisionRadius': 100,'healthBarHeight': 150.0},LIGHTFRIGATE: {'shipHp': 850,'mastHp': [1200, 1200, 0, 1200, 0],'speedRange': [8, 9],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [125, 126],'stealingSpeed': 124,'treasureReturnRate': 0.5,'behavior': 'bloodlust','style': ShipGlobals.Styles.Bandit01,'shipModel': ShipGlobals.NAVY_PANTHER,'collisionRadius': 100,'healthBarHeight': 200.0},STANDARDSLOOP: {'shipHp': 1000,'mastHp': [1280, 0, 0, 0, 0],'speedRange': [7, 8],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [75, 76],'stealingSpeed': 74,'treasureReturnRate': 0.5,'behavior': 'speedIncrease','style': ShipGlobals.Styles.Bandit02,'shipModel': ShipGlobals.NAVY_GREYHOUND,'collisionRadius': 150,'healthBarHeight': 200.0},STANDARDGALLEON: {'shipHp': 1800,'mastHp': [2720, 2720, 2720, 2720, 0],'speedRange': [4.5, 5],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [100, 101],'stealingSpeed': 99,'treasureReturnRate': 0.5,'behavior': 'barrels','style': ShipGlobals.Styles.Bandit02,'shipModel': ShipGlobals.NAVY_VANGUARD,'collisionRadius': 150,'healthBarHeight': 200.0},STANDARDFRIGATE: {'shipHp': 2800,'mastHp': [3400, 3400, 0, 3400, 3400],'speedRange': [5, 6],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [125, 126],'stealingSpeed': 124,'treasureReturnRate': 0.5,'behavior': 'bloodlust','style': ShipGlobals.Styles.Bandit02,'shipModel': ShipGlobals.NAVY_CENTURION,'collisionRadius': 150,'healthBarHeight': 250.0},WARSHIPSLOOP: {'shipHp': 1500,'mastHp': [2080, 0, 0, 0, 2080],'speedRange': [8, 9],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [75, 76],'stealingSpeed': 74,'treasureReturnRate': 0.5,'behavior': 'barrels','style': ShipGlobals.Styles.Bandit03,'shipModel': ShipGlobals.NAVY_KINGFISHER,'collisionRadius': 200,'healthBarHeight': 250.0},WARSHIPGALLEON: {'shipHp': 3000,'mastHp': [4000, 4000, 4000, 4000, 0],'speedRange': [5, 6],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [100, 101],'stealingSpeed': 99,'treasureReturnRate': 0.5,'behavior': 'normal','style': ShipGlobals.Styles.Bandit03,'shipModel': ShipGlobals.NAVY_MONARCH,'collisionRadius': 200,'healthBarHeight': 270.0},WARSHIPFRIGATE: {'shipHp': 3640,'mastHp': [4840, 4840, 0, 4840, 4840],'speedRange': [4, 5],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [125, 126],'stealingSpeed': 124,'treasureReturnRate': 0.5,'behavior': 'variableSpeed','style': ShipGlobals.Styles.Bandit03,'shipModel': ShipGlobals.NAVY_MAN_O_WAR,'collisionRadius': 200,'healthBarHeight': 320.0},HEAVYWARSHIPSLOOP: {'shipHp': 2400,'mastHp': [3200, 0, 0, 0, 3200],'speedRange': [7, 8],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [75, 76],'stealingSpeed': 74,'treasureReturnRate': 0.5,'behavior': 'speedIncrease','style': ShipGlobals.Styles.Bandit04,'shipModel': ShipGlobals.NAVY_PREDATOR,'collisionRadius': 200,'healthBarHeight': 250.0},HEAVYWARSHIPGALLEON: {'shipHp': 5400,'mastHp': [7120, 7120, 7120, 7120, 0],'speedRange': [4.5, 5.5],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [100, 101],'stealingSpeed': 99,'treasureReturnRate': 0.5,'behavior': 'bloodlust','style': ShipGlobals.Styles.Bandit04,'shipModel': ShipGlobals.NAVY_COLOSSUS,'collisionRadius': 200,'healthBarHeight': 300.0},HEAVYWARSHIPFRIGATE: {'shipHp': 6000,'mastHp': [7880, 7880, 0, 7880, 7880],'speedRange': [4, 5],'escapeSpeedMuliplier': 0.35,'stealingLimitRange': [125, 126],'stealingSpeed': 124,'treasureReturnRate': 0.5,'behavior': 'variableSpeed','style': ShipGlobals.Styles.Bandit04,'shipModel': ShipGlobals.NAVY_DREADNOUGHT,'collisionRadius': 200,'healthBarHeight': 300.0}}
levelUpgrades = [
 [
  InventoryType.DefenseCannonRoundShot, 1], [InventoryType.DefenseCannonTargetedShot, 2], [], [InventoryType.DefenseCannonSmokePowder], [InventoryType.DefenseCannonMine], [3], [InventoryType.DefenseCannonHotShot], [InventoryType.DefenseCannonScatterShot], [4], [InventoryType.DefenseCannonPowderKeg], [InventoryType.DefenseCannonBullet], [], [InventoryType.DefenseCannonColdShot], [InventoryType.DefenseCannonBomb], [], [InventoryType.DefenseCannonChumShot], [], [InventoryType.DefenseCannonFireStorm], [], ['upgrade']]

def getLevelUnlockedAt(ammoSkillId):
    for i in range(len(levelUpgrades)):
        array = levelUpgrades[i]
        for j in range(len(array)):
            if array[j] == ammoSkillId:
                return i + 1

    return -1


__defenseCannonAmmoDurrations = {InventoryType.DefenseCannonMine: 60.0,InventoryType.DefenseCannonPowderKeg: 60.0,InventoryType.DefenseCannonColdShot: 12.0,InventoryType.DefenseCannonSmokePowder: 12.0}

def getDefenseCannonAmmoDuration(ammoSkillId):
    return __defenseCannonAmmoDurrations.get(ammoSkillId)


_defenseCannonAmmoCost = {InventoryType.DefenseCannonRoundShot: 0,InventoryType.DefenseCannonTargetedShot: 20,InventoryType.DefenseCannonSmokePowder: 50,InventoryType.DefenseCannonMine: 100,InventoryType.DefenseCannonHotShot: 100,InventoryType.DefenseCannonScatterShot: 125,InventoryType.DefenseCannonPowderKeg: 500,InventoryType.DefenseCannonBullet: 200,InventoryType.DefenseCannonColdShot: 200,InventoryType.DefenseCannonBomb: 250,InventoryType.DefenseCannonChumShot: 1000,InventoryType.DefenseCannonFireStorm: 400}

def getDefenseCannonAmmoCost(ammoSkillId):
    return _defenseCannonAmmoCost[ammoSkillId]


_defenseCannonAmmoAmount = {InventoryType.DefenseCannonRoundShot: -1,InventoryType.DefenseCannonTargetedShot: 100,InventoryType.DefenseCannonMine: 50,InventoryType.DefenseCannonHotShot: 50,InventoryType.DefenseCannonScatterShot: 50,InventoryType.DefenseCannonPowderKeg: 9,InventoryType.DefenseCannonSmokePowder: 50,InventoryType.DefenseCannonBullet: 50,InventoryType.DefenseCannonColdShot: 50,InventoryType.DefenseCannonBomb: 50,InventoryType.DefenseCannonChumShot: 6,InventoryType.DefenseCannonFireStorm: 25}

def getDefenseCannonAmmoAmount(ammoSkillId):
    if _defenseCannonAmmoAmount.has_key(ammoSkillId):
        return _defenseCannonAmmoAmount[ammoSkillId]
    return 1


RewardTable = {(0, 0): [[InventoryType.ItemTypeConsumable, ItemGlobals.TONIC], [InventoryType.ItemTypeConsumable, ItemGlobals.REMEDY], [InventoryType.ItemTypeConsumable, ItemGlobals.HOLY_WATER], [InventoryType.ItemTypeConsumable, ItemGlobals.POTION_CANNON_1]],(0, 5): [[InventoryType.ItemTypeConsumable, ItemGlobals.REMEDY], [InventoryType.ItemTypeCharm, ItemGlobals.OLD_CANNON_RAM], [InventoryType.ItemTypeWeapon, ItemGlobals.RUSTY_BAYONET], [InventoryType.ItemTypeCharm, ItemGlobals.BRONZE_CANNON_RAM]],(0, 12): [[InventoryType.ItemTypeConsumable, ItemGlobals.POTION_CANNON_1], [InventoryType.ItemTypeCharm, ItemGlobals.BRONZE_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.HASTY_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.GUNNERS_CANNON_RAM]],(1, 5): [[InventoryType.ItemTypeConsumable, ItemGlobals.HOLY_WATER], [InventoryType.ItemTypeWeapon, ItemGlobals.NAVY_GUARD_BAYONET], [InventoryType.ItemTypeCharm, ItemGlobals.HASTY_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.IRON_CANNON_RAM]],(1, 12): [[InventoryType.ItemTypeCharm, ItemGlobals.OLD_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.GREYHOUND_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.WOOL_CANNON_RAM]],(2, 5): [[InventoryType.ItemTypeConsumable, ItemGlobals.ELIXIR], [InventoryType.ItemTypeCharm, ItemGlobals.HASTY_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.FIERY_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.STEEL_CANNON_RAM]],(2, 12): [[InventoryType.ItemTypeCharm, ItemGlobals.OLD_CANNON_RAM], [InventoryType.ItemTypeWeapon, ItemGlobals.MILITARY_BAYONET], [InventoryType.ItemTypeCharm, ItemGlobals.MARAUDER_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.SEARING_CANNON_RAM]],(3, 5): [[InventoryType.ItemTypeConsumable, ItemGlobals.POTION_CANNON_2], [InventoryType.ItemTypeCharm, ItemGlobals.COTTON_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.IRON_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.WOOL_CANNON_RAM]],(3, 12): [[InventoryType.ItemTypeCharm, ItemGlobals.OLD_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.GUNNERS_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.BLOODHOUND_CANNON_RAM]]}
EpicTable = [
 [
  InventoryType.ItemTypeCharm, ItemGlobals.GREYHOUND_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.MARAUDER_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.HAUNTED_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.REVENANT_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.PHANTOM_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.MAKESHIFT_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.SEARING_CANNON_RAM], [InventoryType.ItemTypeCharm, ItemGlobals.CAJUN_CANNON_RAM]]