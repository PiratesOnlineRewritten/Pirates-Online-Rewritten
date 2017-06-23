import random
import copy
from pandac.PandaModules import *
from pirates.battle import WeaponGlobals
from pirates.battle.EnemySkills import *
from pirates.pirate import AvatarTypes
from pirates.pirate.AvatarType import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.inventory import ItemGlobals
SpawnPositions = [
 Vec3(295, -250, 3), Vec3(299, -245, 3), Vec3(303, -250, 3), Vec3(291, -245, 3), Vec3(287, -250, 3), Vec3(307, -255, 3), Vec3(311, -260, 3)]
CANNON_DAMAGE_MODIFIER_PER_LEVEL = 0.025
CANNON_BASE_DAMAGE_MODIFIER = 1.0
MAX_COMPARATIVE_SHIP_LEVEL_DAMAGE_MOD = 0.1
USE_DEFAULT_AGGRO = -1
INSTANT_AGGRO_RADIUS_DEFAULT_MODEL0 = 20
INSTANT_AGGRO_RADIUS_DEFAULT_MODEL1 = 40
ENEMY_LEVEL_THRESHOLD_MODEL0 = 3
ENEMY_LEVEL_THRESHOLD_MODEL1 = 5
SELF_HEAL_AMOUNT_MODEL0 = 1.0
SELF_HEAL_AMOUNT_MODEL1 = 2.0
ATTACK_DAMAGE_THRESHOLD_MODEL0 = 3.0
ATTACK_DAMAGE_THRESHOLD_MODEL1 = 5.0
ATTACK_ACCURACY_THRESHOLD_MODEL0 = 4.0
ATTACK_ACCURACY_THRESHOLD_MODEL1 = 5.0
AGGRO_RADIUS_LEVEL_BUFFER = 1
ENEMY_GANGUP_LEVEL_OFFSET = 5.0
SINGLE_ENEMY_THREAT_BONUS = 7.0
THREAT_LEEWAY = 5.0
MAX_ATTACKERS = 4.0
ENEMY_THREAT_AMOUNT = 0.1
THREAT_BASE_CAPCITY = 2.0
CALL_FOR_HELP_DISTANCE = 80
MINIMUM_THREAT = 0.5

def listThreats():
    for level in range(1, 51):
        threatThreshold = float(level - ENEMY_GANGUP_LEVEL_OFFSET)
        threatCapcity = max(1, level * ENEMY_THREAT_AMOUNT + THREAT_BASE_CAPCITY)
        print 'Level: %s Threat Threshold %s Capcity %s' % (level, threatThreshold, threatCapcity)
        lowerBound = 1
        upperBound = 55
        for monsterLevel in range(lowerBound, upperBound):
            maxMobs = threatCapcity
            enemyThreat = max(MINIMUM_THREAT, monsterLevel - threatThreshold)
            attackers = 0
            for i in range(0, MAX_ATTACKERS):
                currentThreat = attackers * enemyThreat
                if currentThreat < threatCapcity:
                    if attackers == 0 and currentThreat + enemyThreat < threatCapcity + SINGLE_ENEMY_THREAT_BONUS:
                        attackers += 1
                    elif currentThreat + enemyThreat < threatCapcity + THREAT_LEEWAY:
                        attackers += 1

            if attackers < MAX_ATTACKERS and attackers > 0:
                print '    Max Level %s mobs against player: %s' % (monsterLevel, attackers)


BASE_GANGUP_CHANCE = 25
TEAM_AGGRO_RADIUS = 7
AGGRO_RADIUS_FALLOFF_RATE = 1.5
NEWBIE_AGGRO_LEVEL = 0
NEWBIE_GANGUP_HELP_LEVEL = 10
LOW_LEVEL_GANGUP_HELP_LEVEL = 20
GANGUP_LIMIT = 3
WEAK_ENEMY_AGGRO_DEACTIVATION = 10
AGGRO_RADIUS_TOLERANCE = 150
RED = 1.5
YELLOW = 1.0
GREEN = 0.7
GREY = 0.4
ENEMY_DAMAGE_NERF = 0.425
ENEMY_DAMAGE_NERF_MODEL0 = 0.425
ENEMY_DAMAGE_NERF_MODEL1 = 0.64
ENEMY_HP_NERF_MODEL0 = 1.0
ENEMY_HP_NERF_MODEL1 = 0.67
INTERIOR_MAX_SEARCH_RADIUS = 25
MAX_SEARCH_RADIUS = 40
MIN_SEARCH_RADIUS = 0
AGGRO_MODE_DEFAULT = 0
AGGRO_MODE_CUSTOM = 1
AGGRO_MODE_FORCED = 2
AGGRO_MODE_NEVER = 3
AGGRO_NAME_DICT = {AGGRO_MODE_DEFAULT: 'AGGRO_MODE_DEFAULT',AGGRO_MODE_CUSTOM: 'AGGRO_MODE_CUSTOM',AGGRO_MODE_FORCED: 'AGGRO_MODE_FORCED',AGGRO_MODE_NEVER: 'AGGRO_MODE_NEVER'}
TARGET_SWITCH_TYPE_RANDOM = BitMask32.bit(0)
TARGET_SWITCH_TYPE_DAMAGE = BitMask32.bit(1)
TARGET_SWITCH_TYPE_LOW_LVL = BitMask32.bit(2)
TARGET_SWITCH_TYPE_HIGH_LVL = BitMask32.bit(3)
SHIP_SEARCH_RADIUS = 4000
SHIP_MIN_SEARCH_RADIUS = 1000
SHIP_INSTANT_AGGRO_RADIUS = 1000
SHIP_AGGRO_RADIUS_FALLOFF_RATE = 0.1
SHIP_AGGRO_RADIUS_LEVEL_BUFFER = 5
SHIP_INSTANT_HIGH_AGGRO_RADIUS = 2000
SHIP_MAX_HELP_DISTANCE = 10000.0
SHIP_HUNTER_LOST_DISTANCE = 10000.0
SHIP_MIN_THREAT_CARGO_LEVEL = 6.0
SHIP_MIN_THREAT_CARGO_PROP = 0.66
SHIP_THREAT_NONE = 0
SHIP_THREAT_ATTACK_BACK = 1
SHIP_THREAT_CALL_FOR_HELP = 2
SHIP_THREAT_BOUNTY_HUNTERS = 3
SHIP_THREAT_NAVY_HUNTERS = 4
SHIP_THREAT_SCENARIO_START = 5
SHIP_THREAT_SCENARIO_END = 6
THREAT_ICON_DICT = {SHIP_THREAT_NONE: None,SHIP_THREAT_ATTACK_BACK: 'threat_L_One',SHIP_THREAT_CALL_FOR_HELP: 'threat_L_Two',SHIP_THREAT_BOUNTY_HUNTERS: 'threat_L_Three',SHIP_THREAT_NAVY_HUNTERS: 'threat_L_Four',SHIP_THREAT_SCENARIO_START: 'threat_L_Five',SHIP_THREAT_SCENARIO_END: 'threat_L_Six'}
THREAT_SCORE_VALUE_HUNTERS = 1
THREAT_SCORE_VALUE_NAVY_HUNTERS = 2
THREAT_SCORE_NAVY_HUNTERS = 5
THREAT_SCORE_SCENARIO = 10
BOARDING_DIFFICULTY_REGULAR = 0
BOARDING_DIFFICULTY_RAISE_TO_LEVEL = 1
OPEN_PORT_ALL = 0
OPEN_PORT_NONE = 1
OPEN_PORT_CUBA = 2
OPEN_PORT_TORTUGA = 3
OPEN_PORT_RAVEN_COVE = 4
OPEN_PORT_DEVILS_ANVIL = 5
OPEN_PORT_DICT = {OPEN_PORT_ALL: '',OPEN_PORT_NONE: '',OPEN_PORT_CUBA: '1160614528.73sdnaik',OPEN_PORT_TORTUGA: '1156207188.95dzlu',OPEN_PORT_RAVEN_COVE: '1271348547.01akelts',OPEN_PORT_DEVILS_ANVIL: '1164135492.81dzlu'}
OPEN_PORT_REVERSER = {'1160614528.73sdnaik': OPEN_PORT_CUBA,'1156207188.95dzlu': OPEN_PORT_TORTUGA,'1271348547.01akelts': OPEN_PORT_RAVEN_COVE,'1164135492.81dzlu': OPEN_PORT_DEVILS_ANVIL}
NON_WILD_ISLANDS = [
 '1160614528.73sdnaik', '1156207188.95dzlu', '1271348547.01akelts', '1164135492.81dzlu', '1150922126.8dzlu', '1233100928.0akelts']
ALWAYS_HAVE = 100.0
MOSTLY_HAVE = 80.0
USUALLY_HAVE = 60.0
HALF_HAVE = 50.0
UNLIKELY_HAVE = 25.0
NEVER_HAVE = 0.0
SKELETON = 1
MONSTER = 2
HUMAN = 3
SKELETON_TALK_PROB = 40
NAVY_TALK_PROB = 70
EITC_TALK_PROB = 50
GHOST_TALK_PROB = 50
TEAMTALK_PROB = 4
MELEE = 0
CUTLASS = 1
DAGGER = 2
PISTOL = 3
MUSKET = 4
GRENADE = 5
WAND = 6
DOLL = 7
KETTLE = 8
MONSTER = 9
BAYONET = 10
HEAVY = 11
DUALCUTLASS = 12
FOIL = 13
BROADSWORD = 14
__HP_CHART = (
 1, 50, 75, 125, 175, 250, 350, 450, 550, 650, 750, 850, 950, 1050, 1150, 1250, 1350, 1450, 1550, 1650, 1750, 1850, 1950, 2050, 2150, 2250, 2350, 2450, 2550, 2650, 2750, 2850, 2950, 3050, 3150, 3250, 3350, 3450, 3550, 3650, 3750, 3850, 3950, 4050, 4150, 4250, 4350, 4450, 4550, 4650, 4750, 4850, 4950, 5050, 5150, 5250, 5350, 5450, 5550, 5650, 5750, 5850, 5950, 6050, 6150, 6250, 6350, 6450, 6550, 6650, 6750, 6850, 6950, 7050, 7150, 7250, 7350, 7450, 7550, 7650, 7750, 7850, 7950, 8050, 8150, 8250, 8350, 8450, 8550, 8650, 8750, 8850, 8950, 9050, 9150, 9250, 9350, 9450, 9550, 9650, 9750)
__MP_CHART = (
 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990)
__DMG_CHART = (
 10, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910, 920, 930, 940, 950, 960, 970, 980, 990, 1000)
__weaponTable = {MELEE: [InventoryType.MeleeWeaponL1, InventoryType.MeleeWeaponL2, InventoryType.MeleeWeaponL3],CUTLASS: [InventoryType.CutlassWeaponL1, InventoryType.CutlassWeaponL2, InventoryType.CutlassWeaponL3],DAGGER: [InventoryType.DaggerWeaponL1, InventoryType.DaggerWeaponL2, InventoryType.DaggerWeaponL3],PISTOL: [InventoryType.PistolWeaponL1, InventoryType.PistolWeaponL2, InventoryType.PistolWeaponL3],MUSKET: [InventoryType.MusketWeaponL1, InventoryType.MusketWeaponL2, InventoryType.MusketWeaponL3],GRENADE: [InventoryType.GrenadeWeaponL1, InventoryType.GrenadeWeaponL2, InventoryType.GrenadeWeaponL3],WAND: [InventoryType.WandWeaponL1, InventoryType.WandWeaponL2, InventoryType.WandWeaponL3],DOLL: [InventoryType.DollWeaponL1, InventoryType.DollWeaponL2, InventoryType.DollWeaponL3],KETTLE: [InventoryType.KettleWeaponL1, InventoryType.KettleWeaponL2, InventoryType.KettleWeaponL3],BAYONET: [InventoryType.BayonetWeaponL1, InventoryType.BayonetWeaponL2, InventoryType.BayonetWeaponL3],HEAVY: [],MONSTER: [InventoryType.MonsterWeaponL1, InventoryType.MonsterWeaponL2, InventoryType.MonsterWeaponL3, InventoryType.MonsterWeaponL4, InventoryType.MonsterWeaponL5],DUALCUTLASS: [InventoryType.DualCutlassL1],FOIL: [InventoryType.FoilL1]}
__enemyWeaponTable = {MELEE: [InventoryType.MeleeWeaponL1, InventoryType.MeleeWeaponL2, InventoryType.MeleeWeaponL3],CUTLASS: [ItemGlobals.RUSTY_CUTLASS, ItemGlobals.IRON_CUTLASS, ItemGlobals.STEEL_CUTLASS],DAGGER: [ItemGlobals.BASIC_DAGGER, ItemGlobals.BATTLE_DIRK, ItemGlobals.MAIN_GAUCHE],PISTOL: [ItemGlobals.FLINTLOCK_PISTOL, ItemGlobals.DOUBLE_BARREL, ItemGlobals.TRI_BARREL],MUSKET: [ItemGlobals.OLD_MUSKET, ItemGlobals.FLINTLOCK_MUSKET, ItemGlobals.WHEELLOCK_MUSKET],GRENADE: [ItemGlobals.GRENADE_POUCH],WAND: [ItemGlobals.CURSED_STAFF, ItemGlobals.WARPED_STAFF, ItemGlobals.REND_STAFF],DOLL: [ItemGlobals.VOODOO_DOLL, ItemGlobals.CLOTH_DOLL, ItemGlobals.WITCH_DOLL],KETTLE: [InventoryType.KettleWeaponL1, InventoryType.KettleWeaponL2, InventoryType.KettleWeaponL3],BAYONET: [ItemGlobals.RUSTY_BAYONET, ItemGlobals.FLINTLOCK_BAYONET, ItemGlobals.WHEELLOCK_BAYONET],HEAVY: [],MONSTER: [ItemGlobals.MONSTER_WEAPON],DUALCUTLASS: [ItemGlobals.DUAL_RUSTY_CUTLASS],FOIL: [ItemGlobals.EPEE_1],BROADSWORD: [ItemGlobals.WORN_BROADSWORD]}
MIN_LEVEL = 0
MAX_LEVEL = 1
SCALE_INDEX = 2
HEIGHT_INDEX = 3
BATTLE_TUBE_RADIUS_INDEX = 4
MONSTER_CLASS_INDEX = 5
ENABLED_INDEX = 6
__baseAvatarStats = {AvatarTypes.Undead: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Clod: [1, 3, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.Sludge: [2, 5, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.Mire: [4, 7, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.MireKnife: [4, 7, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.Muck: [6, 10, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.MuckCutlass: [6, 10, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.Corpse: [9, 14, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.CorpseCutlass: [13, 19, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.Carrion: [18, 25, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.CarrionKnife: [18, 25, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.Cadaver: [23, 30, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.CadaverCutlass: [23, 30, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.Zombie: [28, 35, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.CaptMudmoss: [32, 38, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Mossman: [19, 25, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Whiff: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Reek: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Billow: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Stench: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Shade: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Specter: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Phantom: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Wraith: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.CaptZephyr: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Squall: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Glint: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Flicker: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Smolder: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Spark: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Imp: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Brand: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Lumen: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Fiend: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.CaptCinderbones: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Torch: [1, 1, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.Drip: [23, 30, 1.0, 5.0, 2.0, MONSTER, 1],AvatarTypes.Damp: [28, 35, 1.0, 5.0, 2.0, MONSTER, 1],AvatarTypes.Drizzle: [28, 35, 1.0, 5.0, 2.0, MONSTER, 1],AvatarTypes.Spray: [33, 40, 1.0, 5.0, 2.0, MONSTER, 1],AvatarTypes.Splatter: [33, 40, 1.0, 5.0, 2.0, MONSTER, 1],AvatarTypes.Drool: [38, 45, 1.0, 5.0, 2.0, MONSTER, 1],AvatarTypes.Drench: [38, 45, 1.0, 5.0, 2.0, MONSTER, 1],AvatarTypes.Douse: [43, 50, 1.0, 5.0, 2.0, MONSTER, 1],AvatarTypes.CaptBriney: [43, 50, 1.0, 5.0, 2.0, MONSTER, 1],AvatarTypes.Spout: [40, 40, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.FrenchUndeadA: [10, 15, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.FrenchUndeadB: [15, 20, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.FrenchUndeadC: [20, 25, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.FrenchUndeadD: [25, 30, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.FrenchBossA: [28, 35, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.SpanishUndeadA: [10, 15, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.SpanishUndeadB: [15, 20, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.SpanishUndeadC: [20, 25, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.SpanishUndeadD: [25, 30, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.SpanishBossA: [28, 35, 1.0, 5.0, 2.0, SKELETON, 0],AvatarTypes.JollyRoger: [80, 80, 1.0, 5.0, 2.0, SKELETON, 1],AvatarTypes.BomberZombie: [15, 20, 1.55, 5.0, 2.0, SKELETON, 1],AvatarTypes.Revenant: [23, 30, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.RageGhost: [44, 52, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.MutineerGhost: [33, 40, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.DeviousGhost: [33, 40, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.TraitorGhost: [38, 46, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.CrewGhost: [33, 40, 1.1, 5.0, 2.0, MONSTER, 0],AvatarTypes.LeaderGhost: [33, 40, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.PressGangVoodooZombie: [9, 14, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.CookVoodooZombie: [13, 19, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.SwabbieVoodooZombie: [18, 25, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.LookoutVoodooZombie: [23, 30, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.AngryVoodooZombie: [28, 35, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.OfficerVoodooZombie: [33, 40, 1.1, 5.0, 2.0, MONSTER, 0],AvatarTypes.SlaveDriverVoodooZombie: [38, 46, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.VoodooZombieBoss: [38, 46, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.PettyHunter: [13, 19, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.BailHunter: [18, 25, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.ScallyWagHunter: [23, 30, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.BanditHunter: [28, 35, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.PirateHunter: [33, 40, 1.1, 5.0, 2.0, MONSTER, 0],AvatarTypes.WitchHunter: [38, 46, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.MasterHunter: [44, 52, 1.0, 5.0, 2.0, MONSTER, 0],AvatarTypes.Navy: [1, 1, 1.0, 5.0, 2.0, HUMAN, 0],AvatarTypes.Cadet: [2, 4, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.Guard: [4, 7, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.Marine: [6, 10, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.Sergeant: [9, 14, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.Veteran: [13, 19, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.Officer: [18, 25, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.Dragoon: [23, 30, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.TradingCo: [1, 1, 1.0, 5.0, 2.0, HUMAN, 0],AvatarTypes.Thug: [9, 14, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.Grunt: [13, 19, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.Hiredgun: [18, 25, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.Mercenary: [23, 30, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.Assassin: [28, 35, 1.0, 5.0, 2.0, HUMAN, 1],AvatarTypes.Creature: [1, 1, 1.0, 4.0, 2.0, MONSTER, 0],AvatarTypes.Monkey: [1, 1, 1.0, 2.0, 2.0, MONSTER, 0],AvatarTypes.Crab: [1, 3, 2.0, 1.0, 1.0, MONSTER, 1],AvatarTypes.StoneCrab: [2, 5, 2.0, 1.0, 1.0, MONSTER, 1],AvatarTypes.RockCrab: [6, 10, 3.5, 2.0, 1.0, MONSTER, 1],AvatarTypes.GiantCrab: [13, 19, 5.0, 3.0, 2.0, MONSTER, 1],AvatarTypes.CrusherCrab: [18, 25, 5.0, 3.0, 2.0, MONSTER, 1],AvatarTypes.Stump: [28, 35, 1.15, 8.0, 2.5, MONSTER, 1],AvatarTypes.TwistedStump: [33, 40, 1.15, 8.0, 2.5, MONSTER, 1],AvatarTypes.FlyTrap: [6, 10, 1.0, 20.0, 2.5, MONSTER, 1],AvatarTypes.RancidFlyTrap: [13, 19, 1.0, 20.0, 2.5, MONSTER, 1],AvatarTypes.AncientFlyTrap: [28, 35, 1.0, 20.0, 2.5, MONSTER, 1],AvatarTypes.Seagull: [1, 1, 1.0, 3.0, 2.0, MONSTER, 0],AvatarTypes.Raven: [1, 1, 1.0, 3.0, 2.0, MONSTER, 0],AvatarTypes.Scorpion: [2, 5, 0.35, 2.0, 2.0, MONSTER, 1],AvatarTypes.DireScorpion: [6, 10, 0.35, 2.0, 2.0, MONSTER, 1],AvatarTypes.DreadScorpion: [13, 19, 0.5, 2.0, 2.0, MONSTER, 1],AvatarTypes.Alligator: [2, 5, 1.0, 2.0, 2.0, MONSTER, 1],AvatarTypes.BayouGator: [4, 7, 1.0, 2.0, 2.0, MONSTER, 1],AvatarTypes.BigGator: [9, 14, 1.5, 2.0, 2.0, MONSTER, 1],AvatarTypes.HugeGator: [13, 19, 2.0, 2.0, 2.0, MONSTER, 1],AvatarTypes.Bat: [2, 5, 1.0, 6.0, 2.0, MONSTER, 1],AvatarTypes.RabidBat: [4, 7, 1.0, 6.0, 2.0, MONSTER, 1],AvatarTypes.VampireBat: [9, 14, 1.5, 6.0, 2.0, MONSTER, 1],AvatarTypes.FireBat: [28, 35, 1.5, 6.0, 2.0, MONSTER, 0],AvatarTypes.Wasp: [6, 10, 0.5, 4.0, 2.0, MONSTER, 1],AvatarTypes.KillerWasp: [9, 14, 0.5, 4.0, 2.0, MONSTER, 1],AvatarTypes.AngryWasp: [13, 19, 0.7, 4.0, 2.0, MONSTER, 1],AvatarTypes.SoldierWasp: [18, 25, 0.7, 4.0, 2.0, MONSTER, 1],AvatarTypes.SeaSerpent: [30, 30, 2.0, 60.0, 280.0, MONSTER, 0],AvatarTypes.Townfolk: [1, 1, 1.0, 5.0, 2.0, HUMAN, 0],AvatarTypes.Pirate: [1, 1, 1.0, 5.0, 2.0, HUMAN, 0],AvatarTypes.Landlubber: [1, 4, 1.0, 5.0, 2.0, HUMAN, 0],AvatarTypes.Scallywag: [2, 8, 1.0, 5.0, 2.0, HUMAN, 0],AvatarTypes.Buccaneer: [4, 12, 1.0, 5.0, 2.0, HUMAN, 0],AvatarTypes.Swashbuckler: [8, 16, 1.0, 5.0, 2.0, HUMAN, 0],AvatarTypes.Warmonger: [16, 20, 1.0, 5.0, 2.0, HUMAN, 0]}

def getBaseStats(avatarType):
    if type(avatarType) == type(''):
        if __dev__:
            import pdb
            pdb.set_trace()
        self.notify.warning('AvatarType is a string %s' % avatarType)
    baseStats = __baseAvatarStats.get(avatarType.getNonBossType())
    if not baseStats:
        fact = avatarType.getFaction()
        track = avatarType.getTrack()
        avatarType = AvatarType(faction=fact, track=track)
        baseStats = __baseAvatarStats.get(avatarType)
    if not baseStats:
        fact = avatarType.getFaction()
        avatarType = AvatarType(faction=fact)
        baseStats = __baseAvatarStats.get(avatarType)
    if baseStats:
        return baseStats[:]
    return


def getHeight(avatarType):
    baseStats = getBaseStats(avatarType.getNonBossType())
    if baseStats:
        return baseStats[HEIGHT_INDEX]
    else:
        return None
    return None


def getBattleTubeRadius(avatarType):
    baseStats = getBaseStats(avatarType.getNonBossType())
    if baseStats:
        return baseStats[BATTLE_TUBE_RADIUS_INDEX]
    else:
        return None
    return None


def getMonsterClass(avatarType):
    baseStats = getBaseStats(avatarType.getNonBossType())
    if baseStats:
        return baseStats[MONSTER_CLASS_INDEX]
    else:
        return None
    return None


HP_MOD = 0
WEAPON_MOD = 1
SKILL_MOD = 2
SCALE_MOD = 3
__baseLevelStatMultiplier = {0: (1.0, 1, 1, 0.925),1: (1.2, 1, 1, 0.95),2: (1.4, 1, 2, 0.975),3: (1.6, 2, 2, 1.0),4: (1.8, 2, 3, 1.025),5: (2.0, 2, 3, 1.05),6: (2.2, 3, 4, 1.075),7: (2.4, 3, 4, 1.1),8: (2.6, 3, 5, 1.125),9: (2.8, 4, 5, 1.15),10: (3.0, 4, 6, 1.175),11: (3.2, 4, 6, 1.2),12: (3.4, 5, 7, 1.225),13: (3.6, 5, 7, 1.25),14: (3.8, 5, 8, 1.275),15: (4.0, 6, 8, 1.3),16: (4.2, 6, 9, 1.325),17: (4.4, 6, 9, 1.35),18: (4.6, 7, 10, 1.375),19: (4.8, 7, 10, 1.4),20: (5.0, 7, 11, 1.425),21: (5.2, 8, 11, 1.45),22: (5.4, 8, 12, 1.475),23: (5.6, 8, 12, 1.5),24: (5.8, 9, 13, 1.525),25: (6.0, 9, 13, 1.55),26: (6.2, 9, 14, 1.575),27: (6.4, 10, 14, 1.6),28: (6.6, 10, 15, 1.625),29: (6.8, 10, 15, 1.65),30: (7.0, 11, 16, 1.675),31: (7.2, 11, 16, 1.705),32: (7.4, 11, 17, 1.725),33: (7.6, 12, 17, 1.75),34: (7.8, 12, 18, 1.775),35: (8.0, 12, 18, 1.8),36: (8.2, 13, 19, 1.825),37: (8.4, 13, 19, 1.85),38: (8.6, 13, 20, 1.875),39: (8.8, 14, 20, 1.9),40: (9.0, 14, 21, 1.925),41: (9.2, 14, 21, 1.95),42: (9.4, 15, 22, 1.975),43: (9.6, 15, 22, 2.0),44: (9.8, 15, 23, 2.025),45: (10.0, 16, 23, 2.05),46: (10.2, 16, 24, 2.075),47: (10.4, 16, 24, 2.1),48: (10.6, 17, 25, 2.125),49: (10.8, 17, 25, 2.15),50: (11.0, 17, 26, 2.175),51: (11.2, 18, 26, 2.2),52: (11.4, 18, 27, 2.225),53: (11.6, 18, 27, 2.25),54: (11.8, 19, 28, 2.275),55: (12.0, 19, 28, 2.3),56: (12.2, 19, 29, 2.325),57: (12.4, 20, 29, 2.35),58: (12.6, 20, 30, 2.375),59: (12.8, 20, 30, 2.4),60: (13.0, 21, 31, 2.425),61: (13.2, 21, 31, 2.45),62: (13.4, 21, 32, 2.475),63: (13.6, 22, 32, 2.5),64: (13.8, 22, 33, 2.525),65: (14.0, 22, 33, 2.55),66: (14.2, 23, 34, 2.575),67: (14.4, 23, 34, 2.6),68: (14.6, 23, 35, 2.625),69: (14.8, 24, 35, 2.65),70: (15.0, 24, 36, 2.675),71: (15.2, 24, 36, 2.7),72: (15.4, 25, 37, 2.725),73: (15.6, 25, 37, 2.75),74: (15.8, 25, 38, 2.775),75: (16.0, 26, 38, 2.8),76: (16.2, 26, 39, 2.825),77: (16.4, 26, 39, 2.85),78: (16.6, 27, 40, 2.875),79: (16.8, 27, 40, 2.9),80: (17.0, 27, 41, 2.925),81: (17.2, 28, 41, 2.95),82: (17.4, 28, 42, 2.975),83: (17.6, 28, 42, 3.0),84: (17.8, 29, 43, 3.025),85: (18.0, 29, 43, 3.05),86: (18.2, 29, 44, 3.075),87: (18.4, 30, 44, 3.1),88: (18.6, 30, 45, 3.125),89: (18.8, 30, 45, 3.15),90: (19.0, 31, 46, 3.175),91: (19.2, 31, 46, 3.2),92: (19.4, 31, 47, 3.225),93: (19.6, 32, 47, 3.25),94: (19.8, 32, 48, 3.275),95: (20.0, 32, 48, 3.3),96: (20.2, 33, 49, 3.325),97: (20.4, 33, 49, 3.35),98: (20.6, 33, 50, 3.375),99: (20.8, 34, 50, 3.4),100: (21.0, 34, 51, 3.425)}
WEAPON_INDEX = 0
SKILL_INDEX = 1
__baseAvatarSkills = {AvatarTypes.Undead: ([CUTLASS], [InventoryType.CutlassHack]),AvatarTypes.Clod: ([DAGGER], [InventoryType.DaggerCut, EnemySkills.DAGGER_THROW_KNIFE, InventoryType.DaggerSwipe]),AvatarTypes.Sludge: ([CUTLASS], [InventoryType.CutlassHack, InventoryType.CutlassSlash, InventoryType.CutlassCleave, EnemySkills.CUTLASS_CHOP, EnemySkills.CUTLASS_STAB]),AvatarTypes.Mire: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassSweep, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_DOUBLESLASH, EnemySkills.CUTLASS_WILDSLASH]),AvatarTypes.MireKnife: ([DAGGER], [InventoryType.DaggerCut, EnemySkills.DAGGER_THROW_KNIFE, InventoryType.DaggerSwipe]),AvatarTypes.Muck: ([DOLL], [EnemySkills.DOLL_POKE2, InventoryType.DollSwarm, InventoryType.DollCurse]),AvatarTypes.MuckCutlass: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassSweep, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_DOUBLESLASH, EnemySkills.CUTLASS_WILDSLASH]),AvatarTypes.Corpse: ([DAGGER], [InventoryType.DaggerCut, InventoryType.DaggerSwipe, EnemySkills.DAGGER_THROW_VENOMBLADE, InventoryType.DaggerGouge, EnemySkills.DAGGER_THROW_INTERRUPT, InventoryType.DaggerEviscerate, EnemySkills.DAGGER_THROW_KNIFE]),AvatarTypes.CorpseCutlass: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassSweep, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_DOUBLESLASH, EnemySkills.CUTLASS_WILDSLASH]),AvatarTypes.Carrion: ([GRENADE], [InventoryType.GrenadeExplosion, InventoryType.GrenadeShockBomb]),AvatarTypes.CarrionKnife: ([DAGGER], [InventoryType.DaggerCut, InventoryType.DaggerSwipe, EnemySkills.DAGGER_THROW_VENOMBLADE, InventoryType.DaggerGouge, EnemySkills.DAGGER_THROW_INTERRUPT, InventoryType.DaggerEviscerate, EnemySkills.DAGGER_THROW_KNIFE]),AvatarTypes.Cadaver: ([DOLL], [EnemySkills.DOLL_POKE2, InventoryType.DollSwarm, InventoryType.DollCurse, InventoryType.DollBurn, InventoryType.DollShackles, InventoryType.DollLifeDrain]),AvatarTypes.CadaverCutlass: ([CUTLASS], [EnemySkills.CUTLASS_CHOP, EnemySkills.CUTLASS_DOUBLESLASH, InventoryType.CutlassBrawl, EnemySkills.CUTLASS_FLURRY, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassSweep, InventoryType.CutlassTaunt]),AvatarTypes.Zombie: ([CUTLASS, DAGGER], [EnemySkills.CUTLASS_CHOP, EnemySkills.CUTLASS_DOUBLESLASH, InventoryType.CutlassBrawl, EnemySkills.CUTLASS_FLURRY, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassSweep, InventoryType.CutlassTaunt, InventoryType.DaggerSidewinder, InventoryType.DaggerEviscerate, EnemySkills.DAGGER_THROW_KNIFE]),AvatarTypes.CaptMudmoss: ([CUTLASS, DAGGER], [EnemySkills.CUTLASS_FLURRY, EnemySkills.CUTLASS_COMBOA, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassBrawl, InventoryType.DaggerSidewinder, EnemySkills.CUTLASS_LUNGE, InventoryType.CutlassStab, InventoryType.CutlassBladestorm, InventoryType.DaggerEviscerate, InventoryType.CutlassSweep, InventoryType.DaggerViperNest, EnemySkills.DAGGER_THROW_INTERRUPT, EnemySkills.DAGGER_THROW_KNIFE]),AvatarTypes.Mossman: ([MONSTER], []),AvatarTypes.Whiff: ([DAGGER], [InventoryType.DaggerAsp, InventoryType.DaggerAdder]),AvatarTypes.Reek: ([CUTLASS], [InventoryType.CutlassSlash]),AvatarTypes.Billow: ([DAGGER], [InventoryType.DaggerSwipe]),AvatarTypes.Stench: ([DAGGER, CUTLASS], [InventoryType.DaggerAsp, InventoryType.CutlassSlash]),AvatarTypes.Shade: ([GRENADE], [InventoryType.GrenadeExplosion]),AvatarTypes.Specter: ([CUTLASS], [InventoryType.CutlassSlash]),AvatarTypes.Phantom: ([DOLL], [InventoryType.DollShackles]),AvatarTypes.Wraith: ([GRENADE], [InventoryType.GrenadeExplosion]),AvatarTypes.CaptZephyr: ([CUTLASS], [InventoryType.CutlassSlash]),AvatarTypes.Squall: ([MONSTER], []),AvatarTypes.Glint: ([DAGGER], [InventoryType.DaggerAsp]),AvatarTypes.Flicker: ([CUTLASS], [InventoryType.CutlassSlash]),AvatarTypes.Smolder: ([GRENADE], [InventoryType.GrenadeExplosion]),AvatarTypes.Spark: ([DAGGER, CUTLASS], [InventoryType.DaggerAsp, InventoryType.CutlassSlash]),AvatarTypes.Imp: ([GRENADE, DOLL], [InventoryType.GrenadeExplosion, InventoryType.DollBurn]),AvatarTypes.Brand: ([CUTLASS], [InventoryType.CutlassSlash]),AvatarTypes.Lumen: ([DOLL], [InventoryType.DollCurse]),AvatarTypes.Fiend: ([GRENADE], [InventoryType.GrenadeExplosion]),AvatarTypes.CaptCinderbones: ([CUTLASS], [InventoryType.CutlassSlash]),AvatarTypes.Torch: ([MONSTER], []),AvatarTypes.Drip: ([DAGGER], [InventoryType.DaggerCut, EnemySkills.DAGGER_THROW_INTERRUPT, InventoryType.DaggerSwipe, InventoryType.DaggerGouge, EnemySkills.DAGGER_THROW_VENOMBLADE, EnemySkills.DAGGER_THROW_KNIFE, InventoryType.DaggerEviscerate, EnemySkills.DAGGER_THROW_BARBED]),AvatarTypes.Damp: ([CUTLASS], [InventoryType.CutlassBrawl, InventoryType.CutlassSlash, InventoryType.CutlassSweep, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassFlourish, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_STAB, EnemySkills.CUTLASS_FLURRY, InventoryType.CutlassStab]),AvatarTypes.Drizzle: ([GRENADE], [InventoryType.GrenadeExplosion, InventoryType.GrenadeShockBomb, InventoryType.GrenadeFireBomb]),AvatarTypes.Spray: ([DAGGER, CUTLASS], [InventoryType.DaggerAdder, InventoryType.CutlassSweep, InventoryType.DaggerGouge, InventoryType.CutlassFlourish, InventoryType.DaggerSidewinder, EnemySkills.CUTLASS_RIPOSTE, InventoryType.DaggerEviscerate, InventoryType.CutlassStab, InventoryType.DaggerViperNest, EnemySkills.DAGGER_THROW_KNIFE]),AvatarTypes.Splatter: ([DOLL], [EnemySkills.DOLL_POKE2, InventoryType.DollSwarm, InventoryType.DollCurse, InventoryType.DollBurn, InventoryType.DollShackles, InventoryType.DollLifeDrain]),AvatarTypes.Drool: ([CUTLASS], [InventoryType.CutlassBrawl, InventoryType.CutlassCleave, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_FLURRY, InventoryType.CutlassSweep, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassStab, InventoryType.CutlassTaunt, InventoryType.CutlassFlourish, InventoryType.CutlassBladestorm]),AvatarTypes.Drench: ([DOLL], [EnemySkills.DOLL_POKE2, InventoryType.DollSwarm, InventoryType.DollCurse, InventoryType.DollBurn, InventoryType.DollShackles, InventoryType.DollLifeDrain]),AvatarTypes.Douse: ([GRENADE], [InventoryType.GrenadeExplosion, InventoryType.GrenadeShockBomb, InventoryType.GrenadeSiege]),AvatarTypes.CaptBriney: ([CUTLASS], [InventoryType.CutlassBrawl, InventoryType.CutlassCleave, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_FLURRY, InventoryType.CutlassSweep, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassStab, InventoryType.CutlassTaunt, InventoryType.CutlassFlourish, InventoryType.CutlassBladestorm, EnemySkills.CUTLASS_RIPOSTE]),AvatarTypes.Spout: ([MONSTER], []),AvatarTypes.Revenant: ([MONSTER], [EnemySkills.GHOST_PHANTOM_TOUCH]),AvatarTypes.RageGhost: ([MONSTER], [EnemySkills.GHOST_KILL_TOUCH]),AvatarTypes.MutineerGhost: ([CUTLASS], [InventoryType.CutlassBrawl, InventoryType.CutlassCleave, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_FLURRY, InventoryType.CutlassSweep, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassStab, InventoryType.CutlassTaunt, InventoryType.CutlassFlourish, InventoryType.CutlassBladestorm]),AvatarTypes.DeviousGhost: ([DAGGER], [InventoryType.DaggerCut, EnemySkills.DAGGER_THROW_INTERRUPT, InventoryType.DaggerSwipe, InventoryType.DaggerGouge, EnemySkills.DAGGER_THROW_VENOMBLADE, EnemySkills.DAGGER_THROW_KNIFE, InventoryType.DaggerEviscerate, EnemySkills.DAGGER_THROW_BARBED]),AvatarTypes.TraitorGhost: ([CUTLASS], [InventoryType.CutlassBrawl, InventoryType.CutlassCleave, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_FLURRY, InventoryType.CutlassSweep, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassStab, InventoryType.CutlassTaunt, InventoryType.CutlassFlourish, InventoryType.CutlassBladestorm]),AvatarTypes.Ghost: ([CUTLASS], [InventoryType.CutlassBrawl, InventoryType.CutlassCleave, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_FLURRY, InventoryType.CutlassSweep, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassStab, InventoryType.CutlassTaunt, InventoryType.CutlassFlourish, InventoryType.CutlassBladestorm]),AvatarTypes.CrewGhost: ([CUTLASS], [InventoryType.CutlassBrawl, InventoryType.CutlassCleave, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_FLURRY, InventoryType.CutlassSweep, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassStab, InventoryType.CutlassTaunt, InventoryType.CutlassFlourish, InventoryType.CutlassBladestorm]),AvatarTypes.LeaderGhost: ([BROADSWORD], [EnemySkills.GHOST_SUMMON_HELP, EnemySkills.BROADSWORD_CLEAVE, EnemySkills.BROADSWORD_FLOURISH, EnemySkills.BROADSWORD_STAB, InventoryType.CutlassBrawl, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_FLURRY, InventoryType.CutlassSweep, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassTaunt, InventoryType.CutlassBladestorm]),AvatarTypes.JollyRoger: ([MONSTER], [EnemySkills.JR_GRAVEBIND, EnemySkills.JR_SOUL_HARVEST, EnemySkills.JR_CORRUPTION, EnemySkills.JR_THUNDER]),AvatarTypes.BomberZombie: ([MONSTER], [EnemySkills.BZ_EXPLODE, EnemySkills.BZ_EXPLODE_DEATH]),AvatarTypes.PressGangVoodooZombie: ([CUTLASS], [EnemySkills.CUTLASS_DOUBLESLASH, EnemySkills.CUTLASS_WILDSLASH]),AvatarTypes.CookVoodooZombie: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassSweep, EnemySkills.CUTLASS_DOUBLESLASH, EnemySkills.CUTLASS_WILDSLASH]),AvatarTypes.SwabbieVoodooZombie: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassSweep, EnemySkills.CUTLASS_DOUBLESLASH, EnemySkills.CUTLASS_WILDSLASH]),AvatarTypes.LookoutVoodooZombie: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassSweep, EnemySkills.CUTLASS_DOUBLESLASH, EnemySkills.CUTLASS_WILDSLASH]),AvatarTypes.AngryVoodooZombie: ([CUTLASS], [EnemySkills.CUTLASS_CHOP, EnemySkills.CUTLASS_DOUBLESLASH, InventoryType.CutlassBrawl, EnemySkills.CUTLASS_FLURRY, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassSweep, InventoryType.CutlassTaunt]),AvatarTypes.OfficerVoodooZombie: ([CUTLASS], [EnemySkills.CUTLASS_CHOP, EnemySkills.CUTLASS_DOUBLESLASH, InventoryType.CutlassBrawl, EnemySkills.CUTLASS_FLURRY, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassSweep, InventoryType.CutlassTaunt]),AvatarTypes.SlaveDriverVoodooZombie: ([CUTLASS], [EnemySkills.CUTLASS_CHOP, EnemySkills.CUTLASS_DOUBLESLASH, InventoryType.CutlassBrawl, EnemySkills.CUTLASS_FLURRY, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassSweep, InventoryType.CutlassTaunt]),AvatarTypes.VoodooZombieBoss: ([CUTLASS], [EnemySkills.CUTLASS_CHOP, EnemySkills.CUTLASS_DOUBLESLASH, InventoryType.CutlassBrawl, EnemySkills.CUTLASS_FLURRY, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassSweep, InventoryType.CutlassTaunt]),AvatarTypes.PettyHunter: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassSweep, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_DOUBLESLASH, EnemySkills.CUTLASS_WILDSLASH]),AvatarTypes.BailHunter: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassSweep, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_DOUBLESLASH, EnemySkills.CUTLASS_WILDSLASH]),AvatarTypes.ScallyWagHunter: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassSweep, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_DOUBLESLASH, EnemySkills.CUTLASS_WILDSLASH]),AvatarTypes.BanditHunter: ([CUTLASS], [EnemySkills.CUTLASS_CHOP, EnemySkills.CUTLASS_DOUBLESLASH, InventoryType.CutlassBrawl, EnemySkills.CUTLASS_FLURRY, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassSweep, InventoryType.CutlassTaunt]),AvatarTypes.PirateHunter: ([FOIL], [EnemySkills.FOIL_FLECHE, EnemySkills.FOIL_REPRISE, EnemySkills.FOIL_SWIPE, EnemySkills.FOIL_IMPALE, EnemySkills.FOIL_REMISE, EnemySkills.FOIL_BALESTRAKICK, EnemySkills.FOIL_CADENCE]),AvatarTypes.WitchHunter: ([DUALCUTLASS], [EnemySkills.DUALCUTLASS_COMBINATION, EnemySkills.DUALCUTLASS_SPIN, EnemySkills.DUALCUTLASS_BARRAGE, EnemySkills.DUALCUTLASS_XSLASH, EnemySkills.DUALCUTLASS_GORE]),AvatarTypes.MasterHunter: ([BROADSWORD], [EnemySkills.BROADSWORD_CLEAVE, EnemySkills.BROADSWORD_FLOURISH, EnemySkills.BROADSWORD_STAB, InventoryType.CutlassBrawl, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_FLURRY, InventoryType.CutlassSweep, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassTaunt, InventoryType.CutlassBladestorm]),AvatarTypes.FrenchUndeadA: ([FOIL], [EnemySkills.FOIL_FLECHE, EnemySkills.FOIL_REPRISE, EnemySkills.FOIL_SWIPE, EnemySkills.FOIL_IMPALE, EnemySkills.FOIL_REMISE, EnemySkills.FOIL_BALESTRAKICK, EnemySkills.FOIL_CADENCE]),AvatarTypes.FrenchUndeadB: ([FOIL], [EnemySkills.FOIL_FLECHE, EnemySkills.FOIL_REPRISE, EnemySkills.FOIL_SWIPE, EnemySkills.FOIL_IMPALE, EnemySkills.FOIL_REMISE, EnemySkills.FOIL_BALESTRAKICK, EnemySkills.FOIL_CADENCE]),AvatarTypes.FrenchUndeadC: ([FOIL], [EnemySkills.FOIL_FLECHE, EnemySkills.FOIL_REPRISE, EnemySkills.FOIL_SWIPE, EnemySkills.FOIL_IMPALE, EnemySkills.FOIL_REMISE, EnemySkills.FOIL_BALESTRAKICK, EnemySkills.FOIL_CADENCE]),AvatarTypes.FrenchUndeadD: ([FOIL], [EnemySkills.FOIL_FLECHE, EnemySkills.FOIL_REPRISE, EnemySkills.FOIL_SWIPE, EnemySkills.FOIL_IMPALE, EnemySkills.FOIL_REMISE, EnemySkills.FOIL_BALESTRAKICK, EnemySkills.FOIL_CADENCE]),AvatarTypes.FrenchBossA: ([FOIL], [EnemySkills.FOIL_FLECHE, EnemySkills.FOIL_REPRISE, EnemySkills.FOIL_SWIPE, EnemySkills.FOIL_IMPALE, EnemySkills.FOIL_REMISE, EnemySkills.FOIL_BALESTRAKICK, EnemySkills.FOIL_CADENCE]),AvatarTypes.SpanishUndeadA: ([DUALCUTLASS], [EnemySkills.DUALCUTLASS_COMBINATION, EnemySkills.DUALCUTLASS_SPIN, EnemySkills.DUALCUTLASS_BARRAGE, EnemySkills.DUALCUTLASS_XSLASH, EnemySkills.DUALCUTLASS_GORE]),AvatarTypes.SpanishUndeadB: ([DUALCUTLASS], [EnemySkills.DUALCUTLASS_COMBINATION, EnemySkills.DUALCUTLASS_SPIN, EnemySkills.DUALCUTLASS_BARRAGE, EnemySkills.DUALCUTLASS_XSLASH, EnemySkills.DUALCUTLASS_GORE]),AvatarTypes.SpanishUndeadC: ([DUALCUTLASS], [EnemySkills.DUALCUTLASS_COMBINATION, EnemySkills.DUALCUTLASS_SPIN, EnemySkills.DUALCUTLASS_BARRAGE, EnemySkills.DUALCUTLASS_XSLASH, EnemySkills.DUALCUTLASS_GORE]),AvatarTypes.SpanishUndeadD: ([DUALCUTLASS], [EnemySkills.DUALCUTLASS_COMBINATION, EnemySkills.DUALCUTLASS_SPIN, EnemySkills.DUALCUTLASS_BARRAGE, EnemySkills.DUALCUTLASS_XSLASH, EnemySkills.DUALCUTLASS_GORE]),AvatarTypes.SpanishBossA: ([DUALCUTLASS], [EnemySkills.DUALCUTLASS_COMBINATION, EnemySkills.DUALCUTLASS_SPIN, EnemySkills.DUALCUTLASS_BARRAGE, EnemySkills.DUALCUTLASS_XSLASH, EnemySkills.DUALCUTLASS_GORE]),AvatarTypes.Navy: ([BAYONET], [EnemySkills.BAYONET_STAB, EnemySkills.BAYONET_BASH]),AvatarTypes.Cadet: ([BAYONET], [EnemySkills.BAYONET_STAB, EnemySkills.BAYONET_BASH]),AvatarTypes.Guard: ([BAYONET], [EnemySkills.BAYONET_STAB, EnemySkills.BAYONET_BASH, EnemySkills.BAYONET_RUSH]),AvatarTypes.Marine: ([CUTLASS], [EnemySkills.CUTLASS_STAB, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_RIPOSTE, EnemySkills.CUTLASS_DOUBLESLASH, InventoryType.CutlassFlourish]),AvatarTypes.Sergeant: ([CUTLASS], [EnemySkills.CUTLASS_STAB, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_RIPOSTE, EnemySkills.CUTLASS_DOUBLESLASH, InventoryType.CutlassFlourish]),AvatarTypes.Veteran: ([BAYONET], [EnemySkills.BAYONET_STAB, EnemySkills.BAYONET_BASH, EnemySkills.BAYONET_RUSH]),AvatarTypes.Officer: ([CUTLASS], [EnemySkills.CUTLASS_STAB, InventoryType.CutlassSweep, EnemySkills.CUTLASS_DOUBLESLASH, EnemySkills.CUTLASS_COMBOA, EnemySkills.CUTLASS_FLURRY, InventoryType.CutlassFlourish, EnemySkills.CUTLASS_RIPOSTE, EnemySkills.CUTLASS_LUNGE, InventoryType.CutlassStab]),AvatarTypes.Dragoon: ([BAYONET], [EnemySkills.BAYONET_STAB, EnemySkills.BAYONET_BASH, EnemySkills.BAYONET_RUSH]),AvatarTypes.TradingCo: ([DAGGER], [InventoryType.DaggerSwipe, EnemySkills.DAGGER_THROW_VENOMBLADE, InventoryType.DaggerGouge]),AvatarTypes.Thug: ([DAGGER], [InventoryType.DaggerSwipe, EnemySkills.DAGGER_THROW_VENOMBLADE, EnemySkills.DAGGER_THROW_KNIFE, InventoryType.DaggerGouge]),AvatarTypes.Grunt: ([CUTLASS], [InventoryType.CutlassSlash, EnemySkills.CUTLASS_CHOP, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassCleave, EnemySkills.CUTLASS_DOUBLESLASH]),AvatarTypes.Hiredgun: ([DAGGER], [EnemySkills.DAGGER_THROW_INTERRUPT, InventoryType.DaggerAdder, InventoryType.DaggerSwipe, InventoryType.DaggerSidewinder, InventoryType.DaggerGouge, InventoryType.DaggerEviscerate, EnemySkills.DAGGER_THROW_BARBED, EnemySkills.DAGGER_THROW_KNIFE]),AvatarTypes.Mercenary: ([CUTLASS], [InventoryType.CutlassBrawl, InventoryType.CutlassCleave, EnemySkills.CUTLASS_LUNGE, EnemySkills.CUTLASS_FLURRY, InventoryType.CutlassSweep, EnemySkills.CUTLASS_WILDSLASH, InventoryType.CutlassStab, InventoryType.CutlassTaunt, InventoryType.CutlassFlourish, InventoryType.CutlassBladestorm]),AvatarTypes.Assassin: ([DAGGER], [InventoryType.DaggerSwipe, InventoryType.DaggerAdder, InventoryType.DaggerGouge, InventoryType.DaggerSidewinder, InventoryType.DaggerEviscerate, InventoryType.DaggerViperNest, InventoryType.DaggerAsp, EnemySkills.DAGGER_THROW_BARBED, EnemySkills.DAGGER_THROW_INTERRUPT, EnemySkills.DAGGER_THROW_KNIFE]),AvatarTypes.Creature: ([MONSTER], []),AvatarTypes.Crab: ([MONSTER], [EnemySkills.CLAW_RAKE, EnemySkills.CLAW_STRIKE, EnemySkills.DUAL_CLAW]),AvatarTypes.StoneCrab: ([MONSTER], [EnemySkills.CLAW_RAKE, EnemySkills.CLAW_STRIKE, EnemySkills.DUAL_CLAW]),AvatarTypes.RockCrab: ([MONSTER], [EnemySkills.CLAW_RAKE, EnemySkills.CLAW_STRIKE, EnemySkills.DUAL_CLAW]),AvatarTypes.GiantCrab: ([MONSTER], [EnemySkills.CLAW_RAKE, EnemySkills.CLAW_STRIKE, EnemySkills.DUAL_CLAW]),AvatarTypes.CrusherCrab: ([MONSTER], [EnemySkills.CLAW_RAKE, EnemySkills.CLAW_STRIKE, EnemySkills.DUAL_CLAW]),AvatarTypes.Stump: ([MONSTER], [EnemySkills.STUMP_SLAP_LEFT, EnemySkills.STUMP_SLAP_RIGHT, EnemySkills.STUMP_SWAT_LEFT, EnemySkills.STUMP_SWAT_RIGHT, EnemySkills.STUMP_STOMP]),AvatarTypes.TwistedStump: ([MONSTER], [EnemySkills.STUMP_SLAP_LEFT, EnemySkills.STUMP_SLAP_RIGHT, EnemySkills.STUMP_SWAT_LEFT, EnemySkills.STUMP_SWAT_RIGHT, EnemySkills.STUMP_STOMP]),AvatarTypes.FlyTrap: ([MONSTER], [EnemySkills.FLYTRAP_WEAK_SPIT, EnemySkills.FLYTRAP_ATTACK_A, EnemySkills.FLYTRAP_ATTACK_JAB]),AvatarTypes.RancidFlyTrap: ([MONSTER], [EnemySkills.FLYTRAP_SPIT, EnemySkills.FLYTRAP_ATTACK_A, EnemySkills.FLYTRAP_ATTACK_JAB]),AvatarTypes.AncientFlyTrap: ([MONSTER], [EnemySkills.FLYTRAP_SPIT, EnemySkills.FLYTRAP_ATTACK_A, EnemySkills.FLYTRAP_ATTACK_JAB]),AvatarTypes.Scorpion: ([MONSTER], [EnemySkills.SCORPION_ATTACK_LEFT, EnemySkills.SCORPION_ATTACK_RIGHT, EnemySkills.SCORPION_ATTACK_BOTH, EnemySkills.SCORPION_ATTACK_TAIL_STING, EnemySkills.SCORPION_PICK_UP_HUMAN, EnemySkills.SCORPION_REAR_UP]),AvatarTypes.DireScorpion: ([MONSTER], [EnemySkills.SCORPION_ATTACK_LEFT, EnemySkills.SCORPION_ATTACK_RIGHT, EnemySkills.SCORPION_ATTACK_BOTH, EnemySkills.SCORPION_ATTACK_TAIL_STING, EnemySkills.SCORPION_PICK_UP_HUMAN, EnemySkills.SCORPION_REAR_UP]),AvatarTypes.DreadScorpion: ([MONSTER], [EnemySkills.SCORPION_ATTACK_LEFT, EnemySkills.SCORPION_ATTACK_RIGHT, EnemySkills.SCORPION_ATTACK_BOTH, EnemySkills.SCORPION_ATTACK_TAIL_STING, EnemySkills.SCORPION_PICK_UP_HUMAN, EnemySkills.SCORPION_REAR_UP]),AvatarTypes.Alligator: ([MONSTER], [EnemySkills.ALLIGATOR_ATTACK_LEFT, EnemySkills.ALLIGATOR_ATTACK_RIGHT, EnemySkills.ALLIGATOR_ATTACK_STRAIGHT, EnemySkills.ALLIGATOR_CRUSH, EnemySkills.ALLIGATOR_MAIM]),AvatarTypes.BayouGator: ([MONSTER], [EnemySkills.ALLIGATOR_ATTACK_LEFT, EnemySkills.ALLIGATOR_ATTACK_RIGHT, EnemySkills.ALLIGATOR_ATTACK_STRAIGHT, EnemySkills.ALLIGATOR_CRUSH, EnemySkills.ALLIGATOR_MAIM]),AvatarTypes.BigGator: ([MONSTER], [EnemySkills.ALLIGATOR_ATTACK_LEFT, EnemySkills.ALLIGATOR_ATTACK_RIGHT, EnemySkills.ALLIGATOR_ATTACK_STRAIGHT, EnemySkills.ALLIGATOR_CRUSH, EnemySkills.ALLIGATOR_MAIM]),AvatarTypes.HugeGator: ([MONSTER], [EnemySkills.ALLIGATOR_ATTACK_LEFT, EnemySkills.ALLIGATOR_ATTACK_RIGHT, EnemySkills.ALLIGATOR_ATTACK_STRAIGHT, EnemySkills.ALLIGATOR_CRUSH, EnemySkills.ALLIGATOR_MAIM]),AvatarTypes.Bat: ([MONSTER], [EnemySkills.BAT_ATTACK_LEFT, EnemySkills.BAT_ATTACK_RIGHT, EnemySkills.BAT_SHRIEK, EnemySkills.BAT_FLURRY]),AvatarTypes.RabidBat: ([MONSTER], [EnemySkills.BAT_ATTACK_LEFT, EnemySkills.BAT_ATTACK_RIGHT, EnemySkills.BAT_SHRIEK, EnemySkills.BAT_FLURRY]),AvatarTypes.VampireBat: ([MONSTER], [EnemySkills.BAT_ATTACK_LEFT, EnemySkills.BAT_ATTACK_RIGHT, EnemySkills.BAT_SHRIEK, EnemySkills.BAT_FLURRY]),AvatarTypes.FireBat: ([MONSTER], [EnemySkills.BAT_ATTACK_LEFT, EnemySkills.BAT_ATTACK_RIGHT, EnemySkills.BAT_SHRIEK, EnemySkills.BAT_FLURRY]),AvatarTypes.Wasp: ([MONSTER], [EnemySkills.WASP_ATTACK, EnemySkills.WASP_ATTACK_LEAP, EnemySkills.WASP_POISON_STING, EnemySkills.WASP_PAIN_BITE]),AvatarTypes.KillerWasp: ([MONSTER], [EnemySkills.WASP_ATTACK, EnemySkills.WASP_ATTACK_LEAP, EnemySkills.WASP_POISON_STING, EnemySkills.WASP_PAIN_BITE]),AvatarTypes.AngryWasp: ([MONSTER], [EnemySkills.WASP_ATTACK, EnemySkills.WASP_ATTACK_LEAP, EnemySkills.WASP_POISON_STING, EnemySkills.WASP_PAIN_BITE]),AvatarTypes.SoldierWasp: ([MONSTER], [EnemySkills.WASP_ATTACK, EnemySkills.WASP_ATTACK_LEAP, EnemySkills.WASP_POISON_STING, EnemySkills.WASP_PAIN_BITE]),AvatarTypes.Townfolk: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassStab, InventoryType.CutlassSlash, InventoryType.CutlassBrawl, InventoryType.CutlassFlourish]),AvatarTypes.Pirate: ([MELEE], [InventoryType.MeleePunch]),AvatarTypes.Landlubber: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassStab, InventoryType.CutlassSlash, InventoryType.CutlassBrawl, InventoryType.CutlassFlourish]),AvatarTypes.Scallywag: ([CUTLASS, DAGGER], [InventoryType.CutlassSlash, InventoryType.DaggerAsp, InventoryType.CutlassStab, InventoryType.DaggerAdder]),AvatarTypes.Buccaneer: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassStab]),AvatarTypes.Swashbuckler: ([CUTLASS], [InventoryType.CutlassSlash, InventoryType.CutlassBrawl, InventoryType.CutlassStab]),AvatarTypes.Warmonger: ([CUTLASS, GRENADE], [InventoryType.CutlassSlash, InventoryType.GrenadeExplosion, InventoryType.CutlassStab, InventoryType.GrenadeShockBomb, InventoryType.CutlassStab, InventoryType.CutlassFlourish])}
__enemyAttackDelay = {InventoryType.GrenadeThrow: [6, 6]}

def getAttackDelay(skillId, default=None):
    delayInfo = __enemyAttackDelay.get(skillId, None)
    if delayInfo == None:
        if default:
            delayInfo = default
        else:
            return [2, 2]
    delay = delayInfo[0] + delayInfo[1] * random.random()
    return delay


def getBaseSkills(avatarType):
    baseSkills = __baseAvatarSkills.get(avatarType.getNonBossType())
    if not baseSkills:
        fact = avatarType.getFaction()
        track = avatarType.getTrack()
        avatarType = AvatarType(faction=fact, track=track)
        baseSkills = __baseAvatarSkills.get(avatarType)
    if not baseSkills:
        fact = avatarType.getFaction()
        avatarType = AvatarType(faction=fact)
        baseSkills = __baseAvatarSkills.get(avatarType)
    return (baseSkills[WEAPON_INDEX][:], baseSkills[SKILL_INDEX][:])


def getEnemyStats(avatarType, level, hpMultiplier=1, mpMultiplier=1):
    if avatarType.isA(AvatarTypes.SeaSerpent):
        monsterHP = 10000
    else:
        monsterHP = getMonsterHp(level)
    monsterMP = getMonsterMp(level)
    return (
     monsterHP * hpMultiplier, monsterMP * mpMultiplier)


def getMonsterHp(level):
    if simbase.config.GetBool('demo-hacks', 0) == 1 and level > 5:
        return 700
    else:
        return __HP_CHART[level]


def getMonsterMp(level):
    if simbase.config.GetBool('demo-hacks', 0) == 1 and level > 5:
        return 50
    else:
        return __MP_CHART[level]


def getMonsterDmg(level, damageMultiplier=1):
    amt = __DMG_CHART[level]
    amt = int(amt * damageMultiplier)
    return amt


def getEnemyScale(npc, scaleMultiplier=1):
    avatarType = npc.avatarType
    lvl = npc.getLevel()
    return getEnemyScaleByType(avatarType, lvl, scaleMultiplier)


def getEnemyScaleByType(avatarType, level, scaleMultiplier=1):
    baseStats = getBaseStats(avatarType.getNonBossType())
    avgLvl = baseStats[MIN_LEVEL] + baseStats[MAX_LEVEL]
    avgLvl /= 2
    if level is None:
        if __dev__:
            import pdb
            pdb.set_trace()
        level = avgLvl
    modifier = 1.0 + 0.03 * (level - avgLvl)
    humanScale = 1.0 * scaleMultiplier
    if avatarType.isA(AvatarTypes.Navy):
        return humanScale
    elif avatarType.isA(AvatarTypes.Townfolk):
        return humanScale
    elif avatarType.isA(AvatarTypes.Pirate):
        return humanScale
    elif avatarType.isA(AvatarTypes.TradingCo):
        return humanScale
    elif avatarType.isA(AvatarTypes.Ghost):
        return humanScale
    else:
        return float(baseStats[SCALE_INDEX] * (modifier + (scaleMultiplier - 1)))
    return


def getRandomEncounter(level):
    level = min(level, 50)
    encounterArray = []
    for critter in __baseAvatarStats:
        avgLvl = __baseAvatarStats[critter][MIN_LEVEL] + __baseAvatarStats[critter][MAX_LEVEL]
        avgLvl /= 2
        if avgLvl < level + 6 and avgLvl > level - 6:
            if __baseAvatarStats[critter][ENABLED_INDEX]:
                encounterArray.append(critter)

    if len(encounterArray):
        encounterType = random.choice(encounterArray)
        avgLvl = __baseAvatarStats[encounterType][MIN_LEVEL] + __baseAvatarStats[encounterType][MAX_LEVEL]
        avgLvl /= 2
        amount = 10 + (avgLvl - level)
        return (
         encounterType, amount)
    else:
        encounterType = None
        while not encounterType:
            enemyType = random.choice(__baseAvatarStats.keys())
            if __baseAvatarStats[enemyType][ENABLED_INDEX]:
                encounterType = enemyType

        return (
         encounterType, 10)
    return


def getEnemyWeapons(avatarType, level, weaponlist=[], weaponlevel=0):
    invWeapons = {}
    baseStats = getBaseSkills(avatarType.getNonBossType())
    levelModifier = __baseLevelStatMultiplier.get(level)
    weaponlist = weaponlist or baseStats[WEAPON_INDEX]
    weaponlevel = weaponlevel or levelModifier[WEAPON_MOD]
    baselevel = int(weaponlevel / 2)
    remainder = weaponlevel % 2
    for weapon in weaponlist:
        weaponset = __enemyWeaponTable.get(weapon)
        level = baselevel + remainder
        if len(weaponset) > level:
            weaponId = weaponset[level - 1]
        else:
            weaponId = weaponset[0]
        remainder = 0
        invWeapons[weaponId] = 1

    return invWeapons


def getEnemySkills(avatarType, level, skillList=[], skillLevel=0):
    weaponSkills = {}
    baseSkills = getBaseSkills(avatarType.getNonBossType())
    levelModifier = __baseLevelStatMultiplier.get(level)
    skillList = skillList or baseSkills[SKILL_INDEX]
    skillLevel = skillLevel or levelModifier[SKILL_MOD]
    if not simbase.config.GetBool('npcs-all-skills', 0):
        skillLevel = 15
    skillIds = skillList[0:skillLevel]
    for skillId in skillIds:
        weaponSkills[skillId] = WeaponGlobals.getSkillMaxQuantity(skillId)

    return weaponSkills


def getRandomEnemyLevel(avatarType):
    baseStats = getBaseStats(avatarType.getNonBossType())
    if not baseStats:
        return 1
    return random.randint(baseStats[MIN_LEVEL], baseStats[MAX_LEVEL])


def getMaxEnemyLevel(avatarType):
    baseStats = getBaseStats(avatarType.getNonBossType())
    if not baseStats:
        return 1
    return baseStats[MAX_LEVEL]


def getMinEnemyLevel(avatarType):
    baseStats = getBaseStats(avatarType.getNonBossType())
    if not baseStats:
        return 1
    return baseStats[MIN_LEVEL]


__goldAmountByLevel = {0: (0, 0),1: (1, 3),2: (1, 4),3: (1, 5),4: (2, 6),5: (2, 7),6: (2, 8),7: (3, 9),8: (3, 10),9: (3, 11),10: (4, 12),11: (4, 13),12: (4, 14),13: (5, 15),14: (5, 16),15: (5, 17),16: (6, 18),17: (6, 19),18: (6, 20),19: (7, 21),20: (7, 22),21: (7, 23),22: (8, 24),23: (8, 25),24: (8, 26),25: (9, 27),26: (9, 28),27: (9, 29),28: (10, 30),29: (10, 31),30: (10, 32),31: (11, 33),32: (11, 34),33: (11, 35),34: (12, 36),35: (12, 37),36: (12, 38),37: (13, 39),38: (13, 40),39: (13, 41),40: (14, 42),41: (14, 43),42: (14, 44),43: (15, 45),44: (15, 46),45: (15, 47),46: (16, 48),47: (16, 49),48: (16, 50),49: (17, 51),50: (17, 52),51: (17, 53),52: (18, 54),53: (18, 55),54: (18, 56),55: (19, 57),56: (19, 58),57: (19, 59),58: (20, 60),59: (20, 61),60: (20, 62),61: (21, 63),62: (21, 64),63: (21, 65),64: (22, 66),65: (22, 67),66: (22, 68),67: (23, 69),68: (23, 70),69: (23, 71),70: (24, 72),71: (24, 73),72: (24, 74),73: (25, 75),74: (25, 76),75: (25, 77),76: (26, 78),77: (26, 79),78: (26, 80),79: (27, 81),80: (27, 82),81: (27, 83),82: (28, 84),83: (28, 85),84: (28, 86),85: (29, 87),86: (29, 88),87: (29, 89),88: (30, 90),89: (30, 91),90: (31, 92),91: (31, 93),92: (32, 94),93: (32, 95),94: (32, 96),95: (33, 97),96: (33, 98),97: (33, 99),98: (34, 100),99: (34, 101),100: (35, 102)}

def randomize(amt):
    return int(amt * random.random())


def getGoldDrop(avatarType, level, dropMultiplier=1):
    if not 1 <= level <= 60:
        return 0
    goldMin, goldMax = __goldAmountByLevel.get(level)
    amount = random.randint(goldMin, goldMax)
    if avatarType:
        if avatarType.isA(AvatarTypes.Navy):
            amount *= 1.1
        elif avatarType.isA(AvatarTypes.TradingCo):
            amount *= 1.2
        elif avatarType.isA(AvatarTypes.Undead):
            pass
        else:
            amount = 0
    return int(amount * dropMultiplier)


def getMaxGoldDrop(avatarType, level, dropMultiplier=1):
    if not 1 <= level <= 60:
        return 0
    goldMin, goldMax = __goldAmountByLevel.get(level)
    amount = goldMax
    if avatarType:
        if avatarType.isA(AvatarTypes.Navy):
            amount *= 1.1
        elif avatarType.isA(AvatarTypes.TradingCo):
            amount *= 1.2
        elif avatarType.isA(AvatarTypes.Undead):
            pass
        else:
            amount = 0
    return int(amount * dropMultiplier)


def getNametagColor(avatarType):
    if avatarType.isA(AvatarTypes.Townfolk):
        return Vec4(0.5, 1, 0.5, 1)
    elif avatarType.isA(AvatarTypes.Pirate):
        return Vec4(1.0, 0.9, 0.6, 1)
    else:
        return Vec4(0.8, 0.7, 0.6, 1)


def getShipNametagColor(team):
    if team == PiratesGlobals.UNDEAD_TEAM:
        return Vec4(0.8, 0.7, 0.5, 1)
    elif team == PiratesGlobals.NAVY_TEAM:
        return Vec4(1, 0, 0, 1)
    elif team == PiratesGlobals.TRADING_CO_TEAM:
        return Vec4(0.5, 0.5, 0.5, 1)
    elif team == PiratesGlobals.VILLAGER_TEAM:
        return Vec4(0.5, 1, 0.5, 1)
    elif team == PiratesGlobals.PLAYER_TEAM:
        return Vec4(0.8, 0.7, 0.5, 1)
    elif team == PiratesGlobals.FRENCH_UNDEAD_TEAM:
        return Vec4(0.8, 0.7, 0.5, 1)
    elif team == PiratesGlobals.SPANISH_UNDEAD_TEAM:
        return Vec4(0.8, 0.7, 0.5, 1)
    elif team == PiratesGlobals.VOODOO_ZOMBIE_TEAM:
        return Vec4(0.8, 0.7, 0.5, 1)
    elif team == PiratesGlobals.BOUNTY_HUNTER_TEAM:
        return Vec4(0.8, 0.7, 0.5, 1)


def getTeamIconModelPath(team):
    if team == PiratesGlobals.UNDEAD_TEAM:
        return '**/flag_undead'
    elif team == PiratesGlobals.NAVY_TEAM:
        return '**/flag_navy'
    elif team == PiratesGlobals.TRADING_CO_TEAM:
        return '**/flag_eitc'
    elif team == PiratesGlobals.FRENCH_UNDEAD_TEAM:
        return '**/flag_undead'
    elif team == PiratesGlobals.SPANISH_UNDEAD_TEAM:
        return '**/flag_undead'
    elif team == PiratesGlobals.VOODOO_ZOMBIE_TEAM:
        return '**/flag_undead'
    elif team == PiratesGlobals.BOUNTY_HUNTER_TEAM:
        return '**/flag_undead'
    else:
        return None
    return None


def getFlagshipIconModelPath(team):
    if team == PiratesGlobals.UNDEAD_TEAM:
        return 'models/gui/flagship_undead'
    elif team == PiratesGlobals.NAVY_TEAM:
        return 'models/gui/flagship_navy'
    elif team == PiratesGlobals.TRADING_CO_TEAM:
        return 'models/gui/flagship_eitc'
    elif team == PiratesGlobals.FRENCH_UNDEAD_TEAM:
        return 'models/gui/flagship_undead'
    elif team == PiratesGlobals.SPANISH_UNDEAD_TEAM:
        return 'models/gui/flagship_undead'
    elif team == PiratesGlobals.VOODOO_ZOMBIE_TEAM:
        return 'models/gui/flagship_undead'
    elif team == PiratesGlobals.BOUNTY_HUNTER_TEAM:
        return 'models/gui/flagship_undead'
    else:
        return None
    return None


def getNPCsByTeam(team, level):
    if team == PiratesGlobals.NAVY_TEAM:
        if level < 4:
            return [AvatarTypes.Cadet]
        elif level < 6:
            return [AvatarTypes.Cadet, AvatarTypes.Guard]
        elif level < 8:
            return [AvatarTypes.Guard]
        elif level < 10:
            return [AvatarTypes.Sergeant, AvatarTypes.Guard]
        elif level < 13:
            return [AvatarTypes.Sergeant]
        elif level < 16:
            return [AvatarTypes.Sergeant, AvatarTypes.Veteran]
        elif level < 19:
            return [AvatarTypes.Veteran]
        elif level < 22:
            return [AvatarTypes.Officer, AvatarTypes.Veteran]
        else:
            return [
             AvatarTypes.Officer]
    elif team == PiratesGlobals.TRADING_CO_TEAM:
        if level < 12:
            return [AvatarTypes.Thug]
        elif level < 15:
            return [AvatarTypes.Thug, AvatarTypes.Grunt]
        elif level < 18:
            return [AvatarTypes.Grunt]
        elif level < 20:
            return [AvatarTypes.Thug, AvatarTypes.Hiredgun]
        elif level < 24:
            return [AvatarTypes.Hiredgun]
        elif level < 27:
            return [AvatarTypes.Mercenary, AvatarTypes.Hiredgun]
        elif level < 30:
            return [AvatarTypes.Mercenary]
        elif level < 32:
            return [AvatarTypes.Mercenary, AvatarTypes.Assassin]
        else:
            return [
             AvatarTypes.Assassin]
    elif team == PiratesGlobals.FRENCH_UNDEAD_TEAM:
        if level < 15:
            return [AvatarTypes.FrenchUndeadA]
        elif level < 20:
            return [AvatarTypes.FrenchUndeadB]
        elif level < 25:
            return [AvatarTypes.FrenchUndeadC]
        else:
            return [
             AvatarTypes.FrenchUndeadD]
    elif team == PiratesGlobals.SPANISH_UNDEAD_TEAM:
        if level < 15:
            return [AvatarTypes.SpanishUndeadA]
        elif level < 20:
            return [AvatarTypes.SpanishUndeadB]
        elif level < 25:
            return [AvatarTypes.SpanishUndeadC]
        else:
            return [
             AvatarTypes.SpanishUndeadD]
    elif team == PiratesGlobals.BOUNTY_HUNTER_TEAM:
        if level < 15:
            return [AvatarTypes.PettyHunter, AvatarTypes.BailHunter, AvatarTypes.ScallyWagHunter, AvatarTypes.BanditHunter]
        elif level < 20:
            return [AvatarTypes.BailHunter, AvatarTypes.ScallyWagHunter, AvatarTypes.BanditHunter, AvatarTypes.PirateHunte]
        elif level < 25:
            return [AvatarTypes.ScallyWagHunter, AvatarTypes.BanditHunter, AvatarTypes.PirateHunter, AvatarTypes.WitchHunter]
        else:
            return [
             AvatarTypes.BanditHunter, AvatarTypes.PirateHunter, AvatarTypes.WitchHunter, AvatarTypes.MasterHunter]
    elif team == PiratesGlobals.VOODOO_ZOMBIE_TEAM:
        if level < 15:
            return [AvatarTypes.PressGangVoodooZombie, AvatarTypes.CookVoodooZombie, AvatarTypes.SwabbieVoodooZombie, AvatarTypes.LookoutVoodooZombie, AvatarTypes.AngryVoodooZombie, AvatarTypes.OfficerVoodooZombie, AvatarTypes.SlaveDriverVoodooZombie]
        elif level < 20:
            return [AvatarTypes.PressGangVoodooZombie, AvatarTypes.CookVoodooZombie, AvatarTypes.SwabbieVoodooZombie, AvatarTypes.LookoutVoodooZombie, AvatarTypes.AngryVoodooZombie, AvatarTypes.OfficerVoodooZombie, AvatarTypes.SlaveDriverVoodooZombie]
        elif level < 25:
            return [AvatarTypes.PressGangVoodooZombie, AvatarTypes.CookVoodooZombie, AvatarTypes.SwabbieVoodooZombie, AvatarTypes.LookoutVoodooZombie, AvatarTypes.AngryVoodooZombie, AvatarTypes.OfficerVoodooZombie, AvatarTypes.SlaveDriverVoodooZombie]
        else:
            return [
             AvatarTypes.PressGangVoodooZombie, AvatarTypes.CookVoodooZombie, AvatarTypes.SwabbieVoodooZombie, AvatarTypes.LookoutVoodooZombie, AvatarTypes.AngryVoodooZombie, AvatarTypes.OfficerVoodooZombie, AvatarTypes.SlaveDriverVoodooZombie]
    elif level < 3:
        return [AvatarTypes.Clod]
    elif level < 5:
        return [AvatarTypes.Clod, AvatarTypes.Sludge]
    elif level < 7:
        return [AvatarTypes.Mire, AvatarTypes.Sludge]
    elif level < 9:
        return [AvatarTypes.Muck, AvatarTypes.Sludge]
    elif level < 11:
        return [AvatarTypes.Muck]
    elif level < 13:
        return [AvatarTypes.Muck, AvatarTypes.Corpse]
    elif level < 16:
        return [AvatarTypes.Corpse]
    elif level < 19:
        return [AvatarTypes.Carrion, AvatarTypes.Corpse]
    elif level < 22:
        return [AvatarTypes.Carrion]
    elif level < 25:
        return [AvatarTypes.Carrion, AvatarTypes.Cadaver]
    elif level < 27:
        return [AvatarTypes.Cadaver]
    elif level < 30:
        return [AvatarTypes.Cadaver, AvatarTypes.Zombie]
    else:
        return [
         AvatarTypes.Zombie]


def determineAggroInfo(aggroRadius):
    aggroInfo = [
     AGGRO_MODE_NEVER, USE_DEFAULT_AGGRO]
    if aggroRadius != None:
        aggroInfo[1] = int(float(aggroRadius))
        if aggroInfo[1] == 0:
            aggroInfo[0] = AGGRO_MODE_FORCED
        else:
            aggroInfo[0] = AGGRO_MODE_CUSTOM
    else:
        aggroInfo[1] = USE_DEFAULT_AGGRO
        aggroInfo[0] = AGGRO_MODE_DEFAULT
    return aggroInfo


def getEffectScale(npc):
    effectScale = getEnemyScale(npc)
    npcName = npc.avatarType.getName()
    if npcName in ['Crab', 'Sand Crab', 'Rock Crab']:
        effectScale *= 0.5
    elif npcName in ['Giant Crab']:
        effectScale *= 0.3
    elif 'Scorpion' in npcName:
        effectScale *= 3.0
    elif npc.avatarType.isA(AvatarTypes.FlyTrap):
        effectScale *= 2.0
    elif npc.avatarType.isA(AvatarTypes.Wasp):
        effectScale *= 2.0
    return effectScale


def getEffectOffset(npc):
    if npc.avatarType.isA(AvatarTypes.FlyTrap):
        return VBase3(8, 0, 0)
    elif npc.avatarType.isA(AvatarTypes.Undead):
        return VBase3(-1.25, 0, 0)
    return VBase3(0, 0, 0)


def getBreakAttackRechargeRate(levelGrade):
    if levelGrade in (RED, YELLOW):
        amount = 1.0
    elif levelGrade == GREEN:
        amount = 0.5
    else:
        amount = 0.25
    return amount