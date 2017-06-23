import cPickle
from libpandaexpress import ConfigVariableBool
from pandac.PandaModules import *
from direct.showbase.PythonUtil import *
from direct.showbase import AppRunnerGlobal
from pirates.pirate import AvatarTypes
from pirates.battle import EnemyGlobals
from pirates.ship import ShipGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.battle import EnemyGlobals
import string
import random
import os
vfs = VirtualFileSystem.getGlobalPtr()
filename = Filename('DropGlobals.pkl')
searchPath = DSearchPath()
if AppRunnerGlobal.appRunner:
    searchPath.appendDirectory(Filename.expandFrom('$POTCO_2_ROOT/etc'))
else:
    searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$PIRATES/src/inventory')))
    searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/src/inventory')))
    searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/inventory')))
    searchPath.appendDirectory(Filename('.'))
    searchPath.appendDirectory(Filename('etc'))
found = vfs.resolveFilename(filename, searchPath)
if not found:
    print 'DropGlobals.pkl file not found: %s' % filename.cStr()
data = vfs.readFile(filename, 1)
__dropInfo = cPickle.loads(data)
__lootDropCache = {}
__lootStoreCache = {}
__lootShipCache = {}
__columnHeadings = __dropInfo.pop('columnHeadings')
filenameDrops = Filename('CommonDrops.pkl')
searchPathDrops = DSearchPath()
foundDrops = vfs.resolveFilename(filenameDrops, searchPath)
if not foundDrops:
    print 'CommonDrops.pkl file not found: %s' % filenameDrops.cStr()
commonDropData = vfs.readFile(filenameDrops, 1)
__commonDropInfo = cPickle.loads(commonDropData)
__staticIdTypeList = {}
for heading, value in __columnHeadings.items():
    try:
        newHeading = string.replace(heading, '\r', '')
        exec '%s = %s' % (newHeading, value) in globals()
    except:
        newHeading = string.replace(heading, '\r', '')
        exec "__staticIdTypeList['%s'] = %s" % (newHeading, value) in globals()

__staticCommonDropList = {}
__typeCommonDropList = {}
for heading, value in __commonDropInfo.items():
    if value == 'x':
        value = 1
    else:
        value = 0
    try:
        newHeading = string.replace(heading, '\r', '')
        id = None
        exec 'id = (AvatarTypes.%s.getFaction(), AvatarTypes.%s.getTrack(), AvatarTypes.%s.getId())' % (heading, heading, heading)
        exec '__typeCommonDropList[id] = %s' % value in globals()
    except:
        newHeading = string.replace(heading, '\r', '')
        exec "__staticCommonDropList['%s'] = %s" % (newHeading, value) in globals()

filenameShipMaterialDrops = Filename('ShipMaterialDrops.pkl')
searchPathDrops = DSearchPath()
foundShipMaterialDrops = vfs.resolveFilename(filenameShipMaterialDrops, searchPath)
if not foundShipMaterialDrops:
    print 'ShipMaterialDrops.pkl file not found: %s' % filenameDrops.cStr()
shipMaterialDropData = vfs.readFile(filenameShipMaterialDrops, 1)
__shipMaterialDropInfo = cPickle.loads(shipMaterialDropData)
__shipMaterialDropList = {}
for heading, value in __shipMaterialDropInfo.items():
    entryValue = 0
    if value == 2:
        entryValue = 2
    else:
        if value == 1:
            entryValue = 1
        else:
            entryValue = 0
        if hasattr(ShipGlobals, heading):
            newHeading = string.replace(heading, '\r', '')
            exec '__shipMaterialDropList[ShipGlobals.%s] = %s' % (newHeading, entryValue) in globals()

del searchPath
del __columnHeadings
del data

def isLive(item):
    if ConfigVariableBool('force-all-items-live', False):
        return True
    isLive = item[IS_LIVE]
    return item[IS_LIVE]


__containerDropRate = {EnemyGlobals.RED: 45.0,EnemyGlobals.YELLOW: 45.0,EnemyGlobals.GREEN: 20.0,EnemyGlobals.GREY: 8.0}

def getContainerDropRate(enemyGrade):
    dropRate = __containerDropRate.get(enemyGrade)
    if dropRate:
        return dropRate
    else:
        return 0


__containerTypeRate = {1: (100, 0, 0),2: (99, 1, 0),3: (98, 2, 0),4: (97, 3, 0),5: (96, 4, 0),6: (95, 5, 0),7: (94, 6, 0),8: (93, 7, 0),9: (92, 8, 0),10: (91, 8, 1),11: (90, 9, 1),12: (89, 10, 1),13: (88, 11, 1),14: (87, 12, 1),15: (86, 12, 2),16: (85, 13, 2),17: (84, 14, 2),18: (83, 15, 2),19: (82, 16, 2),20: (81, 16, 3),21: (80, 17, 3),22: (79, 18, 3),23: (78, 19, 3),24: (77, 20, 3),25: (76, 20, 4),26: (76, 20, 4),27: (76, 20, 4),28: (76, 20, 4),29: (76, 20, 4),30: (75, 20, 5),31: (75, 20, 5),32: (75, 20, 5),33: (75, 20, 5),34: (75, 20, 5),35: (75, 20, 5),36: (75, 20, 5),37: (75, 20, 5),38: (75, 20, 5),39: (75, 20, 5),40: (75, 20, 5),41: (75, 20, 5),42: (75, 20, 5),43: (75, 20, 5),44: (75, 20, 5),45: (75, 20, 5),46: (75, 20, 5),47: (75, 20, 5),48: (75, 20, 5),49: (75, 20, 5),50: (75, 20, 5),51: (75, 20, 5),52: (75, 20, 5),53: (75, 20, 5),54: (75, 20, 5),55: (75, 20, 5),56: (75, 20, 5),57: (75, 20, 5),58: (75, 20, 5),59: (75, 20, 5),60: (75, 20, 5),61: (75, 20, 5),62: (75, 20, 5),63: (75, 20, 5),64: (75, 20, 5),65: (75, 20, 5),66: (75, 20, 5),67: (75, 20, 5),68: (75, 20, 5),69: (75, 20, 5),70: (75, 20, 5),71: (75, 20, 5),72: (75, 20, 5),73: (75, 20, 5),74: (75, 20, 5),75: (75, 20, 5),76: (75, 20, 5),77: (75, 20, 5),78: (75, 20, 5),79: (75, 20, 5),80: (75, 20, 5)}

def getContainerTypeRate(enemyLevel):
    typeRate = __containerTypeRate.get(enemyLevel)
    if typeRate:
        return typeRate
    else:
        return (0, 0, 0)


__numItemsRate = {PiratesGlobals.ITEM_SAC: (40, 35, 20, 5, 0, 0),PiratesGlobals.TREASURE_CHEST: (0, 25, 40, 25, 10, 0),PiratesGlobals.RARE_CHEST: (0, 10, 25, 30, 25, 10)}

def getNumItemsRate(containerType):
    numItemsRate = __numItemsRate.get(containerType)
    if numItemsRate:
        return numItemsRate
    else:
        return (0, 0, 0, 0, 0, 0)


__itemTypeRate = {PiratesGlobals.ITEM_SAC: (0.3, 0.2, 0.15, 0.1, 0.05, 0.08, 0.12),PiratesGlobals.TREASURE_CHEST: (0.3, 0.25, 0.15, 0.1, 0.1, 0.1, 0.0),PiratesGlobals.RARE_CHEST: (0.3, 0.2, 0.15, 0.1, 0.1, 0.15, 0.0)}

def getItemTypeRate(containerType):
    itemTypeRate = __itemTypeRate.get(containerType)
    if itemTypeRate:
        return itemTypeRate
    else:
        return (1.0, 0, 0, 0, 0, 0, 0)


__itemRarityRate = {PiratesGlobals.ITEM_SAC: (0.7549, 0.2, 0.045, 0.0001, 0.0),PiratesGlobals.TREASURE_CHEST: (0.41979, 0.48, 0.1, 0.0002, 1e-05),PiratesGlobals.RARE_CHEST: (0.0, 0.72415, 0.25, 0.025, 0.00085)}

def getItemRarityRate(containerType):
    itemRarityRate = __itemRarityRate.get(containerType)
    if itemRarityRate:
        return itemRarityRate
    else:
        return (1.0, 0, 0, 0, 0, 0, 0)


def getAllItemIds():
    return __dropInfo.keys()


__shipTypeList = {ShipGlobals.NAVY_FERRET: NAVY_FERRET,ShipGlobals.NAVY_BULWARK: NAVY_BULWARK,ShipGlobals.NAVY_PANTHER: NAVY_PANTHER,ShipGlobals.NAVY_GREYHOUND: NAVY_GREYHOUND,ShipGlobals.NAVY_VANGUARD: NAVY_VANGUARD,ShipGlobals.NAVY_CENTURION: NAVY_CENTURION,ShipGlobals.NAVY_KINGFISHER: NAVY_KINGFISHER,ShipGlobals.NAVY_MONARCH: NAVY_MONARCH,ShipGlobals.NAVY_MAN_O_WAR: NAVY_MAN_O_WAR,ShipGlobals.NAVY_PREDATOR: NAVY_PREDATOR,ShipGlobals.NAVY_COLOSSUS: NAVY_COLOSSUS,ShipGlobals.NAVY_DREADNOUGHT: NAVY_DREADNOUGHT,ShipGlobals.EITC_SEA_VIPER: EITC_SEA_VIPER,ShipGlobals.EITC_SENTINEL: EITC_SENTINEL,ShipGlobals.EITC_CORVETTE: EITC_CORVETTE,ShipGlobals.EITC_BLOODHOUND: EITC_BLOODHOUND,ShipGlobals.EITC_IRONWALL: EITC_IRONWALL,ShipGlobals.EITC_MARAUDER: EITC_MARAUDER,ShipGlobals.EITC_BARRACUDA: EITC_BARRACUDA,ShipGlobals.EITC_OGRE: EITC_OGRE,ShipGlobals.EITC_WARLORD: EITC_WARLORD,ShipGlobals.EITC_CORSAIR: EITC_CORSAIR,ShipGlobals.EITC_BEHEMOTH: EITC_BEHEMOTH,ShipGlobals.SKEL_PHANTOM: SKEL_PHANTOM,ShipGlobals.SKEL_REVENANT: SKEL_REVENANT,ShipGlobals.SKEL_STORM_REAPER: SKEL_STORM_REAPER,ShipGlobals.SKEL_BLACK_HARBINGER: SKEL_BLACK_HARBINGER,ShipGlobals.SKEL_DEATH_OMEN: SKEL_DEATH_OMEN,ShipGlobals.SKEL_SHADOW_CROW_SP: SKEL_SHADOW_CROW_SP,ShipGlobals.SKEL_HELLHOUND_SP: SKEL_HELLHOUND_SP,ShipGlobals.SKEL_BLOOD_SCOURGE_SP: SKEL_BLOOD_SCOURGE_SP,ShipGlobals.SKEL_SHADOW_CROW_FR: SKEL_SHADOW_CROW_FR,ShipGlobals.SKEL_HELLHOUND_FR: SKEL_HELLHOUND_FR,ShipGlobals.SKEL_BLOOD_SCOURGE_FR: SKEL_BLOOD_SCOURGE_FR,ShipGlobals.GOLIATH: GOLIATH,ShipGlobals.FLYING_DUTCHMAN: FLYING_DUTCHMAN,ShipGlobals.JOLLY_ROGER: JOLLY_ROGER,ShipGlobals.HUNTER_VENGEANCE: HUNTER_VENGEANCE,ShipGlobals.HUNTER_CUTTER_SHARK: HUNTER_CUTTER_SHARK,ShipGlobals.HUNTER_FLYING_STORM: HUNTER_FLYING_STORM,ShipGlobals.HUNTER_KILLYADED: HUNTER_KILLYADED,ShipGlobals.HUNTER_RED_DERVISH: HUNTER_RED_DERVISH,ShipGlobals.HUNTER_CENTURY_HAWK: HUNTER_CENTURY_HAWK,ShipGlobals.HUNTER_SCORNED_SIREN: HUNTER_SCORNED_SIREN,ShipGlobals.HUNTER_TALLYHO: HUNTER_TALLYHO,ShipGlobals.HUNTER_BATTLEROYALE: HUNTER_BATTLEROYALE,ShipGlobals.HUNTER_EN_GARDE: HUNTER_EN_GARDE}

def getShipMaterialDropByClass(shipClass):
    materialDropType = __shipMaterialDropList.get(shipClass, 0)
    return materialDropType


getShipMaterialDropByClass(ShipGlobals.HUNTER_VENGEANCE)

def getShipDropItemsByClass(shipClass):
    dropItems = []
    shipType = __shipTypeList.get(shipClass)
    if __lootShipCache.has_key(shipClass):
        return __lootShipCache[shipClass]
    for itemId in __dropInfo:
        item = __dropInfo[itemId]
        if not isLive(item):
            continue
        if item[DROPS_FROM_ALL_SHIPS]:
            dropItems.append(itemId)
        if shipType and shipType < len(item):
            if item[shipType]:
                dropItems.append(itemId)

    __lootShipCache[shipClass] = dropItems
    return dropItems


__enemyTypeList = {AvatarTypes.Cadet: Cadet,AvatarTypes.Guard: Guard,AvatarTypes.Marine: Marine,AvatarTypes.Sergeant: Sergeant,AvatarTypes.Veteran: Veteran,AvatarTypes.Officer: Officer,AvatarTypes.Dragoon: Dragoon,AvatarTypes.Thug: Thug,AvatarTypes.Grunt: Grunt,AvatarTypes.Hiredgun: Hiredgun,AvatarTypes.Mercenary: Mercenary,AvatarTypes.Assassin: Assassin,AvatarTypes.Clod: Clod,AvatarTypes.Sludge: Sludge,AvatarTypes.Mire: Mire,AvatarTypes.MireKnife: MireKnife,AvatarTypes.Muck: Muck,AvatarTypes.MuckCutlass: MuckCutlass,AvatarTypes.Corpse: Corpse,AvatarTypes.CorpseCutlass: CorpseCutlass,AvatarTypes.Carrion: Carrion,AvatarTypes.CarrionKnife: CarrionKnife,AvatarTypes.Cadaver: Cadaver,AvatarTypes.CadaverCutlass: CadaverCutlass,AvatarTypes.Zombie: Zombie,AvatarTypes.CaptMudmoss: CaptMudmoss,AvatarTypes.Revenant: Revenant,AvatarTypes.RageGhost: RageGhost,AvatarTypes.MutineerGhost: MutineerGhost,AvatarTypes.DeviousGhost: DeviousGhost,AvatarTypes.TraitorGhost: TraitorGhost,AvatarTypes.PressGangVoodooZombie: PressGangVoodooZombie,AvatarTypes.CookVoodooZombie: CookVoodooZombie,AvatarTypes.SwabbieVoodooZombie: SwabbieVoodooZombie,AvatarTypes.LookoutVoodooZombie: LookoutVoodooZombie,AvatarTypes.AngryVoodooZombie: AngryVoodooZombie,AvatarTypes.OfficerVoodooZombie: OfficerVoodooZombie,AvatarTypes.SlaveDriverVoodooZombie: SlaveDriverVoodooZombie,AvatarTypes.PettyHunter: PressGangVoodooZombie,AvatarTypes.BailHunter: CookVoodooZombie,AvatarTypes.ScallyWagHunter: SwabbieVoodooZombie,AvatarTypes.BanditHunter: LookoutVoodooZombie,AvatarTypes.PirateHunter: AngryVoodooZombie,AvatarTypes.WitchHunter: OfficerVoodooZombie,AvatarTypes.MasterHunter: SlaveDriverVoodooZombie,AvatarTypes.SpanishUndeadA: SpanishUndeadA,AvatarTypes.SpanishUndeadB: SpanishUndeadB,AvatarTypes.SpanishUndeadC: SpanishUndeadC,AvatarTypes.SpanishUndeadD: SpanishUndeadD,AvatarTypes.SpanishBossA: SpanishUndeadD,AvatarTypes.FrenchUndeadA: FrenchUndeadA,AvatarTypes.FrenchUndeadB: FrenchUndeadB,AvatarTypes.FrenchUndeadC: FrenchUndeadC,AvatarTypes.FrenchUndeadD: FrenchUndeadD,AvatarTypes.FrenchBossA: FrenchUndeadD,AvatarTypes.Drip: Drip,AvatarTypes.Damp: Damp,AvatarTypes.Drizzle: Drizzle,AvatarTypes.Spray: Spray,AvatarTypes.Splatter: Splatter,AvatarTypes.Drool: Drool,AvatarTypes.Drench: Drench,AvatarTypes.Douse: Douse,AvatarTypes.CaptBriney: CaptBriney,AvatarTypes.Crab: Crab,AvatarTypes.StoneCrab: StoneCrab,AvatarTypes.RockCrab: RockCrab,AvatarTypes.GiantCrab: GiantCrab,AvatarTypes.CrusherCrab: CrusherCrab,AvatarTypes.Scorpion: Scorpion,AvatarTypes.DireScorpion: DireScorpion,AvatarTypes.DreadScorpion: DreadScorpion,AvatarTypes.Alligator: Alligator,AvatarTypes.BayouGator: BayouGator,AvatarTypes.BigGator: BigGator,AvatarTypes.HugeGator: HugeGator,AvatarTypes.FlyTrap: Flytrap,AvatarTypes.RancidFlyTrap: RancidFlytrap,AvatarTypes.AncientFlyTrap: AncientFlytrap,AvatarTypes.Stump: Stump,AvatarTypes.TwistedStump: TwistedStump,AvatarTypes.Wasp: Wasp,AvatarTypes.KillerWasp: KillerWasp,AvatarTypes.AngryWasp: AngryWasp,AvatarTypes.SoldierWasp: SoldierWasp,AvatarTypes.Bat: Bat,AvatarTypes.RabidBat: RabidBat,AvatarTypes.VampireBat: VampireBat,AvatarTypes.FireBat: FireBat,AvatarTypes.WillBurybones: WillBurybones,AvatarTypes.FoulCrenshaw: FoulCrenshaw,AvatarTypes.EvanTheDigger: EvanTheDigger,AvatarTypes.ThadIllFortune: ThadIllFortune,AvatarTypes.SimonButcher: SimonButcher,AvatarTypes.ThaddeusWoodworm: ThaddeusWoodworm,AvatarTypes.Bonebreaker: Bonebreaker,AvatarTypes.GideonGrog: GideonGrog,AvatarTypes.WhitWidowmaker: WhitWidowmaker,AvatarTypes.Blackheart: Blackheart,AvatarTypes.FrancisFaust: FrancisFaust,AvatarTypes.JeremyColdhand: JeremyColdhand,AvatarTypes.Stench: Stench,AvatarTypes.GeoffreyPain: GeoffreyPain,AvatarTypes.HughBrandish: HughBrandish,AvatarTypes.NathanielGrimm: NathanielGrimm,AvatarTypes.SidShiver: SidShiver,AvatarTypes.IanRamjaw: IanRamjaw,AvatarTypes.SandStalker: SandStalker,AvatarTypes.ManRipper: ManRipper,AvatarTypes.ClawChief: ClawChief,AvatarTypes.Bowbreaker: Bowbreaker,AvatarTypes.SnapDragon: SnapDragon,AvatarTypes.RipTail: RipTail,AvatarTypes.SilentStinger: SilentStinger,AvatarTypes.Bonecracker: Bonecracker,AvatarTypes.Trapjaw: Trapjaw,AvatarTypes.SwampTerror: SwampTerror,AvatarTypes.Frightfang: Frightfang,AvatarTypes.Bloodleach: Bloodleach,AvatarTypes.Firesting: Firesting,AvatarTypes.Devilwing: Devilwing,AvatarTypes.CarlosCudgel: CarlosCudgel,AvatarTypes.ZachariahSharp: ZachariahSharp,AvatarTypes.HenryFlint: HenryFlint,AvatarTypes.PhineasFowl: PhineasFowl,AvatarTypes.EdwardLohand: EdwardLohand}
__ignoreEnemyTypeList = [
 AvatarTypes.Pirate, AvatarTypes.Flicker, AvatarTypes.Spark, AvatarTypes.TradingCo, AvatarTypes.CaptZephyr, AvatarTypes.Fiend, AvatarTypes.Scallywag, AvatarTypes.Swashbuckler, AvatarTypes.Whiff, AvatarTypes.Billow, AvatarTypes.Shade, AvatarTypes.Spout, AvatarTypes.Creature, AvatarTypes.Phantom, AvatarTypes.CaptCinderbones, AvatarTypes.Townfolk, AvatarTypes.Mossman, AvatarTypes.SeaSerpent, AvatarTypes.Undead, AvatarTypes.Glint, AvatarTypes.Smolder, AvatarTypes.Warmonger, AvatarTypes.Imp, AvatarTypes.Brand, AvatarTypes.Squall, AvatarTypes.Lumen, AvatarTypes.Landlubber, AvatarTypes.Buccaneer, AvatarTypes.Reek, AvatarTypes.Navy, AvatarTypes.Specter, AvatarTypes.Wraith, AvatarTypes.Torch, AvatarTypes.Seagull, AvatarTypes.Raven, AvatarTypes.Monkey, AvatarTypes.BomberZombie, AvatarTypes.JollyRoger, AvatarTypes.CrewGhost, AvatarTypes.LeaderGhost, AvatarTypes.VoodooZombieBoss]
for baseStat in EnemyGlobals.__baseAvatarStats:
    pass

def isValidEnemy(type, uniqueId):
    return __staticIdTypeList.get(uniqueId) or __enemyTypeList.get(type)


def getEnemyDropItemsByType(type, uniqueId):
    shouldUseCommonDrop = 1
    isStatic = 0
    dropKey = None
    if __staticCommonDropList.has_key(uniqueId):
        shouldUseCommonDrop = __staticCommonDropList[uniqueId]
        isStatic = 1
        dropKey = uniqueId
    else:
        typeKey = (
         type.getFaction(), type.getTrack(), type.getId())
        if __typeCommonDropList.has_key(typeKey):
            shouldUseCommonDrop = __typeCommonDropList[typeKey]
            dropKey = typeKey
    dropItems = []
    enemyType = __staticIdTypeList.get(uniqueId)
    isBoss = 1
    if not enemyType:
        enemyType = __enemyTypeList.get(type)
    if dropKey and __lootDropCache.has_key(dropKey):
        return __lootDropCache[dropKey]
    for itemId in __dropInfo:
        item = __dropInfo[itemId]
        if not isLive(item):
            continue
        if shouldUseCommonDrop and item[DROPS_FROM_ALL_ENEMIES]:
            dropItems.append(itemId)
        if enemyType and enemyType < len(item):
            if item[enemyType]:
                dropItems.append(itemId)

    if dropKey:
        __lootDropCache[dropKey] = dropItems
    return dropItems
    if dropKey:
        __lootDropCache[dropKey] = dropItems
    return dropItems


def getStoreItems(uniqueId):
    storeItems = []
    shopKeeper = __staticIdTypeList.get(uniqueId)
    if shopKeeper:
        if __lootStoreCache.has_key(uniqueId):
            return __lootStoreCache[uniqueId]
        for itemId in __dropInfo:
            item = __dropInfo[itemId]
            if not isLive(item):
                continue
            if item[shopKeeper]:
                storeItems.append(itemId)

    __lootStoreCache[uniqueId] = storeItems
    return storeItems


def getMakeAPirateClothing():
    mapClothing = []
    for itemId in __dropInfo:
        item = __dropInfo[itemId]
        if not isLive(item):
            continue
        if item[MakeAPirate]:
            mapClothing.append(itemId)

    return mapClothing


def getQuestPropItems():
    qpItems = []
    for itemId in __dropInfo:
        item = __dropInfo[itemId]
        if not isLive(item):
            continue
        if item[QuestProp]:
            qpItems.append(itemId)

    return qpItems


__fishTables = []
for index in [FishSmall, FishMed, FishLarge, FishLegendary]:
    dropTable = []
    for itemId, item in __dropInfo.iteritems():
        if not isLive(item):
            continue
        if index < len(item):
            if item[index]:
                dropTable.append(itemId)

    __fishTables.append(dropTable)

def getFishDrops(size):
    return __fishTables[size]


def createZippedDist(unsummedDist, outcomes):
    hundredSum = abs(sum(unsummedDist) - 100) < 0.1
    if hundredSum:
        return zip([ sum(unsummedDist[:x]) for x in range(len(unsummedDist)) ], outcomes)
    else:
        return zip([ sum(unsummedDist[:x]) * 100 for x in range(len(unsummedDist)) ], outcomes)


def rollDistribution(zippedDist):
    roll = random.uniform(0, 100)
    return [ x for x in zippedDist if x[0] <= roll ][-1][1]