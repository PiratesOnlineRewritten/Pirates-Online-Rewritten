from pandac.PandaModules import *
from otp.otpbase.OTPGlobals import *
from pirates.uberdog.UberDogGlobals import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.ship import ShipGlobals
from pirates.world.LocationConstants import LocationIds
from pirates.inventory import ItemGlobals
OVERHAUL_COST_PERCENTAGE = 0.4
CAPTAIN_LOOT_MULTIPLIER = 0.25
RESULT_SUCCESS_UPGRADE_ROD = 3
RESULT_SUCCESS_LAUNCH_FISHING_BOAT = 4

def getAvatarHealHpCost(hp):
    return 5


def getAvatarHealMojoCost(mojo):
    return 5


class ItemType():
    MELEE = 1
    SWORD = 2
    PISTOL = 3
    MUSKET = 4
    DAGGER = 5
    GRENADE = 6
    DOLL = 7
    WAND = 8
    KETTLE = 9
    SHIP = 10
    SHIPPART = 11
    CONSUMABLE = 12
    FURNITURE = 13
    INGREDIENT = 14
    COMBAT_WEAPON = 15
    RANGED_WEAPON = 16
    GRENADE_WEAPON = 17
    VOODOO_WEAPON = 18
    CANNON = 19
    WEAPON = 20
    INTERCEPTOR = 21
    MERCHANT = 22
    WARSHIP = 23
    CANNONAMMO = 24
    AMMO = 25
    PISTOLAMMO = 26
    GRENADEAMMO = 27
    DAGGERAMMO = 28
    POTION = 29
    BOTTLE = 30
    BAYONET = 31
    POUCH = 32
    PISTOL_POUCH = 33
    DAGGER_POUCH = 34
    GRENADE_POUCH = 35
    CANNON_POUCH = 36
    FOOD = 37
    FISHING_ROD = 38
    FISHING_LURE = 39
    SHIP_REPAIR_KIT = 40
    FISHING_POUCH = 41
    MATERIAL = 42
    BRIG = 43


class ItemTypeGroup():
    CUTLASS = 1
    DAGGER = 2
    PISTOL = 3
    CANNON = 4
    DOLL = 5
    POTION = 6
    GRENADE = 7
    WAND = 8
    FISHING_GEAR = 9


__itemTypeList = {ItemType.DAGGER: ItemTypeGroup.DAGGER,ItemType.DAGGERAMMO: ItemTypeGroup.DAGGER,ItemType.DAGGER_POUCH: ItemTypeGroup.DAGGER,ItemType.SWORD: ItemTypeGroup.CUTLASS,ItemType.PISTOL: ItemTypeGroup.PISTOL,ItemType.PISTOLAMMO: ItemTypeGroup.PISTOL,ItemType.PISTOL_POUCH: ItemTypeGroup.PISTOL,ItemType.CANNONAMMO: ItemTypeGroup.CANNON,ItemType.CANNON_POUCH: ItemTypeGroup.CANNON,ItemType.DOLL: ItemTypeGroup.DOLL,ItemType.POTION: ItemTypeGroup.POTION,ItemType.GRENADE: ItemTypeGroup.GRENADE,ItemType.GRENADEAMMO: ItemTypeGroup.GRENADE,ItemType.GRENADE_POUCH: ItemTypeGroup.GRENADE,ItemType.WAND: ItemTypeGroup.WAND,ItemType.FISHING_LURE: ItemTypeGroup.FISHING_GEAR,ItemType.FISHING_ROD: ItemTypeGroup.FISHING_GEAR}

class ItemId():
    GOLD = InventoryType.GoldInPocket
    MATERIAL_BASIC = 0
    MATERIAL_UNCOMMON = 1
    MATERIAL_PINE = InventoryType.PineInPocket
    MATERIAL_OAK = InventoryType.OakInPocket
    MATERIAL_IRON = InventoryType.IronInPocket
    MATERIAL_STEEL = InventoryType.SteelInPocket
    MATERIAL_SILK = InventoryType.SilkInPocket
    MATERIAL_CANVAS = InventoryType.CanvasInPocket
    MATERIAL_GROG = InventoryType.GrogInPocket
    COLLECT = InventoryType.Collection_Set1
    CARD = InventoryType.begin_Cards
    CLOTHING = InventoryType.Clothing
    BOUNTY = InventoryType.PVPCurrentInfamy
    MELEE_L1 = InventoryType.MeleeWeaponL1
    MELEE_L2 = InventoryType.MeleeWeaponL2
    MELEE_L3 = InventoryType.MeleeWeaponL3
    MELEE_L4 = InventoryType.MeleeWeaponL4
    MELEE_L5 = InventoryType.MeleeWeaponL5
    MELEE_L6 = InventoryType.MeleeWeaponL6
    CUTLASS_L1 = InventoryType.CutlassWeaponL1
    CUTLASS_L2 = InventoryType.CutlassWeaponL2
    CUTLASS_L3 = InventoryType.CutlassWeaponL3
    CUTLASS_L4 = InventoryType.CutlassWeaponL4
    CUTLASS_L5 = InventoryType.CutlassWeaponL5
    CUTLASS_L6 = InventoryType.CutlassWeaponL6
    PISTOL_L1 = InventoryType.PistolWeaponL1
    PISTOL_L2 = InventoryType.PistolWeaponL2
    PISTOL_L3 = InventoryType.PistolWeaponL3
    PISTOL_L4 = InventoryType.PistolWeaponL4
    PISTOL_L5 = InventoryType.PistolWeaponL5
    PISTOL_L6 = InventoryType.PistolWeaponL6
    MUSKET_L1 = InventoryType.MusketWeaponL1
    MUSKET_L2 = InventoryType.MusketWeaponL2
    MUSKET_L3 = InventoryType.MusketWeaponL3
    DAGGER_L1 = InventoryType.DaggerWeaponL1
    DAGGER_L2 = InventoryType.DaggerWeaponL2
    DAGGER_L3 = InventoryType.DaggerWeaponL3
    DAGGER_L4 = InventoryType.DaggerWeaponL4
    DAGGER_L5 = InventoryType.DaggerWeaponL5
    DAGGER_L6 = InventoryType.DaggerWeaponL6
    GRENADE_L1 = InventoryType.GrenadeWeaponL1
    GRENADE_L2 = InventoryType.GrenadeWeaponL2
    GRENADE_L3 = InventoryType.GrenadeWeaponL3
    GRENADE_L4 = InventoryType.GrenadeWeaponL4
    GRENADE_L5 = InventoryType.GrenadeWeaponL5
    GRENADE_L6 = InventoryType.GrenadeWeaponL6
    WAND_L1 = InventoryType.WandWeaponL1
    WAND_L2 = InventoryType.WandWeaponL2
    WAND_L3 = InventoryType.WandWeaponL3
    WAND_L4 = InventoryType.WandWeaponL4
    WAND_L5 = InventoryType.WandWeaponL5
    WAND_L6 = InventoryType.WandWeaponL6
    DOLL_L1 = InventoryType.DollWeaponL1
    DOLL_L2 = InventoryType.DollWeaponL2
    DOLL_L3 = InventoryType.DollWeaponL3
    DOLL_L4 = InventoryType.DollWeaponL4
    DOLL_L5 = InventoryType.DollWeaponL5
    DOLL_L6 = InventoryType.DollWeaponL6
    KETTLE_L1 = InventoryType.KettleWeaponL1
    KETTLE_L2 = InventoryType.KettleWeaponL2
    KETTLE_L3 = InventoryType.KettleWeaponL3
    CANNON_L1 = InventoryType.CannonL1
    CANNON_L2 = InventoryType.CannonL2
    CANNON_L3 = InventoryType.CannonL3
    BAYONET_L1 = InventoryType.BayonetWeaponL1
    BAYONET_L2 = InventoryType.BayonetWeaponL2
    BAYONET_L3 = InventoryType.BayonetWeaponL3
    ROUNDSHOT = InventoryType.AmmoRoundShot
    CHAIN_SHOT = InventoryType.AmmoChainShot
    GRAPE_SHOT = InventoryType.AmmoGrapeShot
    FIREBRAND = InventoryType.AmmoFirebrand
    THUNDERBOLT = InventoryType.AmmoThunderbolt
    EXPLOSIVE = InventoryType.AmmoExplosive
    FURY = InventoryType.AmmoFury
    GRAPPLE_HOOK = InventoryType.AmmoGrappleHook
    BULLET = InventoryType.AmmoBullet
    GAS_CLOUD = InventoryType.AmmoGasCloud
    SKULL_AMMO = InventoryType.AmmoSkull
    FLAME_CLOUD = InventoryType.AmmoFlameCloud
    FLAMING_SKULL = InventoryType.AmmoFlamingSkull
    BAR_SHOT = InventoryType.AmmoBarShot
    KNIVES = InventoryType.AmmoKnives
    MINE = InventoryType.AmmoMine
    BARNACLES = InventoryType.AmmoBarnacles
    COMET = InventoryType.AmmoComet
    VENOMSHOT = InventoryType.AmmoVenomShot
    IRONSHOT = InventoryType.AmmoBaneShot
    GOLDENSHOT = InventoryType.AmmoHexEaterShot
    SILVERSHOT = InventoryType.AmmoSilverShot
    STEELSHOT = InventoryType.AmmoSteelShot
    ASP_DAGGER = InventoryType.AmmoAsp
    ADDER_DAGGER = InventoryType.AmmoAdder
    SIDEWINDER_DAGGER = InventoryType.AmmoSidewinder
    VIPERNEST_DAGGER = InventoryType.AmmoViperNest
    EXPLOSION_G = InventoryType.AmmoGrenadeExplosion
    SHOCKBOMB_G = InventoryType.AmmoGrenadeShockBomb
    FLAME_G = InventoryType.AmmoGrenadeFlame
    SMOKE_G = InventoryType.AmmoGrenadeSmoke
    SIEGE_G = InventoryType.AmmoGrenadeSiege
    LANDMINE_G = InventoryType.AmmoGrenadeLandMine
    PISTOL_POUCH_L1 = InventoryType.PistolPouchL1
    PISTOL_POUCH_L2 = InventoryType.PistolPouchL2
    PISTOL_POUCH_L3 = InventoryType.PistolPouchL3
    DAGGER_POUCH_L1 = InventoryType.DaggerPouchL1
    DAGGER_POUCH_L2 = InventoryType.DaggerPouchL2
    DAGGER_POUCH_L3 = InventoryType.DaggerPouchL3
    GRENADE_POUCH_L1 = InventoryType.GrenadePouchL1
    GRENADE_POUCH_L2 = InventoryType.GrenadePouchL2
    GRENADE_POUCH_L3 = InventoryType.GrenadePouchL3
    CANNON_POUCH_L1 = InventoryType.CannonPouchL1
    CANNON_POUCH_L2 = InventoryType.CannonPouchL2
    CANNON_POUCH_L3 = InventoryType.CannonPouchL3
    FISHING_POUCH_L1 = -1
    POTION_1 = InventoryType.Potion1
    POTION_2 = InventoryType.Potion2
    POTION_3 = InventoryType.Potion3
    POTION_4 = InventoryType.Potion4
    POTION_5 = InventoryType.Potion5
    REMOVE_GROGGY = InventoryType.RemoveGroggy
    PORK_CHUNK = InventoryType.PorkChunk
    SHIP_REPAIR_KIT = InventoryType.ShipRepairKit
    FISHING_ROD1 = ItemGlobals.FISHING_ROD_1
    FISHING_ROD2 = ItemGlobals.FISHING_ROD_2
    FISHING_ROD3 = ItemGlobals.FISHING_ROD_3
    FISHING_LURE1 = InventoryType.RegularLure
    FISHING_LURE2 = InventoryType.LegendaryLure
    INTERCEPTOR_L1 = ShipGlobals.INTERCEPTORL1
    INTERCEPTOR_L2 = ShipGlobals.INTERCEPTORL2
    INTERCEPTOR_L3 = ShipGlobals.INTERCEPTORL3
    MERCHANT_L1 = ShipGlobals.MERCHANTL1
    MERCHANT_L2 = ShipGlobals.MERCHANTL2
    MERCHANT_L3 = ShipGlobals.MERCHANTL3
    WARSHIP_L1 = ShipGlobals.WARSHIPL1
    WARSHIP_L2 = ShipGlobals.WARSHIPL2
    WARSHIP_L3 = ShipGlobals.WARSHIPL3
    BRIG_L1 = ShipGlobals.BRIGL1
    BRIG_L2 = ShipGlobals.BRIGL2
    BRIG_L3 = ShipGlobals.BRIGL3
    BLACK_PEARL = ShipGlobals.BLACK_PEARL
    GOLIATH = ShipGlobals.GOLIATH
    DAUNTLESS = ShipGlobals.DAUNTLESS
    FLYING_DUTCHMAN = ShipGlobals.FLYING_DUTCHMAN
    JOLLY_ROGER = ShipGlobals.JOLLY_ROGER
    SKEL_WARSHIPL3 = ShipGlobals.SKEL_WARSHIPL3
    SKEL_INTERCEPTORL3 = ShipGlobals.SKEL_INTERCEPTORL3
    QUEEN_ANNES_REVENGE = ShipGlobals.QUEEN_ANNES_REVENGE
    SHIP_OF_THE_LINE = ShipGlobals.SHIP_OF_THE_LINE
    EL_PATRONS_SHIP = ShipGlobals.EL_PATRONS_SHIP
    P_SKEL_PHANTOM = ShipGlobals.P_SKEL_PHANTOM
    P_SKEL_REVENANT = ShipGlobals.P_SKEL_REVENANT
    P_SKEL_CEREBUS = ShipGlobals.P_SKEL_CEREBUS
    P_NAVY_KINGFISHER = ShipGlobals.P_NAVY_KINGFISHER
    P_EITC_WARLORD = ShipGlobals.P_EITC_WARLORD
    HMS_VICTORY = ShipGlobals.HMS_VICTORY
    HMS_NEWCASTLE = ShipGlobals.HMS_NEWCASTLE
    HMS_INVINCIBLE = ShipGlobals.HMS_INVINCIBLE
    EITC_INTREPID = ShipGlobals.EITC_INTREPID
    EITC_CONQUERER = ShipGlobals.EITC_CONQUERER
    EITC_LEVIATHAN = ShipGlobals.EITC_LEVIATHAN
    NAVY_FERRET = ShipGlobals.NAVY_FERRET
    NAVY_BULWARK = ShipGlobals.NAVY_BULWARK
    NAVY_PANTHER = ShipGlobals.NAVY_PANTHER
    NAVY_GREYHOUND = ShipGlobals.NAVY_GREYHOUND
    NAVY_VANGUARD = ShipGlobals.NAVY_VANGUARD
    NAVY_CENTURION = ShipGlobals.NAVY_CENTURION
    NAVY_KINGFISHER = ShipGlobals.NAVY_KINGFISHER
    NAVY_MONARCH = ShipGlobals.NAVY_MONARCH
    NAVY_MAN_O_WAR = ShipGlobals.NAVY_MAN_O_WAR
    NAVY_PREDATOR = ShipGlobals.NAVY_PREDATOR
    NAVY_COLOSSUS = ShipGlobals.NAVY_COLOSSUS
    NAVY_DREADNOUGHT = ShipGlobals.NAVY_DREADNOUGHT
    NAVY_BASTION = ShipGlobals.NAVY_BASTION
    NAVY_ELITE = ShipGlobals.NAVY_ELITE
    EITC_SEA_VIPER = ShipGlobals.EITC_SEA_VIPER
    EITC_SENTINEL = ShipGlobals.EITC_SENTINEL
    EITC_CORVETTE = ShipGlobals.EITC_CORVETTE
    EITC_BLOODHOUND = ShipGlobals.EITC_BLOODHOUND
    EITC_IRONWALL = ShipGlobals.EITC_IRONWALL
    EITC_MARAUDER = ShipGlobals.EITC_MARAUDER
    EITC_BARRACUDA = ShipGlobals.EITC_BARRACUDA
    EITC_OGRE = ShipGlobals.EITC_OGRE
    EITC_WARLORD = ShipGlobals.EITC_WARLORD
    EITC_CORSAIR = ShipGlobals.EITC_CORSAIR
    EITC_BEHEMOTH = ShipGlobals.EITC_BEHEMOTH
    EITC_JUGGERNAUT = ShipGlobals.EITC_JUGGERNAUT
    EITC_TYRANT = ShipGlobals.EITC_TYRANT
    SKEL_PHANTOM = ShipGlobals.SKEL_PHANTOM
    SKEL_REVENANT = ShipGlobals.SKEL_REVENANT
    SKEL_STORM_REAPER = ShipGlobals.SKEL_STORM_REAPER
    SKEL_BLACK_HARBINGER = ShipGlobals.SKEL_BLACK_HARBINGER
    SKEL_DEATH_OMEN = ShipGlobals.SKEL_DEATH_OMEN
    SKEL_SHADOW_CROW_FR = ShipGlobals.SKEL_SHADOW_CROW_FR
    SKEL_HELLHOUND_FR = ShipGlobals.SKEL_HELLHOUND_FR
    SKEL_BLOOD_SCOURGE_FR = ShipGlobals.SKEL_BLOOD_SCOURGE_FR
    SKEL_SHADOW_CROW_SP = ShipGlobals.SKEL_SHADOW_CROW_SP
    SKEL_HELLHOUND_SP = ShipGlobals.SKEL_HELLHOUND_SP
    SKEL_BLOOD_SCOURGE_SP = ShipGlobals.SKEL_BLOOD_SCOURGE_SP
    HUNTER_VENGEANCE = ShipGlobals.HUNTER_VENGEANCE
    HUNTER_CUTTER_SHARK = ShipGlobals.HUNTER_CUTTER_SHARK
    HUNTER_FLYING_STORM = ShipGlobals.HUNTER_FLYING_STORM
    HUNTER_KILLYADED = ShipGlobals.HUNTER_KILLYADED
    HUNTER_RED_DERVISH = ShipGlobals.HUNTER_RED_DERVISH
    HUNTER_CENTURY_HAWK = ShipGlobals.HUNTER_CENTURY_HAWK
    HUNTER_SCORNED_SIREN = ShipGlobals.HUNTER_SCORNED_SIREN
    HUNTER_TALLYHO = ShipGlobals.HUNTER_TALLYHO
    HUNTER_BATTLEROYALE = ShipGlobals.HUNTER_BATTLEROYALE
    HUNTER_EN_GARDE = ShipGlobals.HUNTER_EN_GARDE
    SMALL_BOTTLE = InventoryType.SmallBottle
    MEDIUM_BOTTLE = InventoryType.MediumBottle
    LARGE_BOTTLE = InventoryType.LargeBottle
    CARGO_CRATE = 1
    CARGO_CHEST = 2
    CARGO_SKCHEST = 3
    CARGO_LOOTSAC = 4
    CARGO_LOOTCHEST = 5
    CARGO_LOOTSKCHEST = 6
    CARGO_SHIPUPGRADECHEST = 7
    CARGO_SHIPUPGRADESKCHEST = 8
    WHEAT = 101
    COTTON = 102
    RUM = 103
    SILK = 104
    IVORY = 105
    SPICES = 106
    IRON_ORE = 107
    COPPER_BARS = 151
    SILVER_BARS = 152
    GOLD_BARS = 153
    EMERALDS = 154
    RUBIES = 155
    DIAMONDS = 156
    CURSED_COIN = 201
    ARTIFACT = 202
    RELIC = 203
    RARE_DIAMOND = 204
    CROWN_JEWELS = 205
    RAREITEM6 = 206
    QUEST_DROP_JEWEL = 250
    QUEST_DROP_TATTOO = 251
    QUEST_DROP_WEAPON = 252


__crateCargoList = {ItemId.CARGO_CRATE: 50,ItemId.CARGO_CHEST: 45,ItemId.CARGO_SKCHEST: 5}

def getCargoValue(itemId):
    entry = __crateCargoList.get(itemId)
    if entry:
        return entry[0]
    return None


SHIP_CARGO_PREFERENCE = [
 ItemId.CARGO_CRATE, ItemId.CARGO_CHEST, ItemId.CARGO_LOOTSAC, ItemId.CARGO_LOOTCHEST, ItemId.CARGO_SKCHEST, ItemId.CARGO_SHIPUPGRADECHEST, ItemId.CARGO_SHIPUPGRADESKCHEST, ItemId.CARGO_LOOTSKCHEST]
SHIP_NEVER_DUMP = [
 ItemId.CARGO_LOOTCHEST, ItemId.CARGO_LOOTSKCHEST, ItemId.CARGO_SHIPUPGRADECHEST, ItemId.CARGO_SHIPUPGRADESKCHEST]
SHIP_LOOT_CONTAINERS = [
 ItemId.CARGO_LOOTSAC, ItemId.CARGO_LOOTCHEST, ItemId.CARGO_LOOTSKCHEST, ItemId.CARGO_SHIPUPGRADECHEST, ItemId.CARGO_SHIPUPGRADESKCHEST]
__cargoList = {ItemId.WHEAT: (5, ItemId.CARGO_CRATE, 35),ItemId.COTTON: (7, ItemId.CARGO_CRATE, 25),ItemId.RUM: (9, ItemId.CARGO_CRATE, 20),ItemId.IRON_ORE: (15, ItemId.CARGO_CRATE, 10),ItemId.IVORY: (25, ItemId.CARGO_CRATE, 5),ItemId.SILK: (40, ItemId.CARGO_CRATE, 3),ItemId.SPICES: (90, ItemId.CARGO_CRATE, 2),ItemId.COPPER_BARS: (25, ItemId.CARGO_CHEST, 75),ItemId.SILVER_BARS: (50, ItemId.CARGO_CHEST, 20),ItemId.GOLD_BARS: (120, ItemId.CARGO_CHEST, 5),ItemId.EMERALDS: (90, ItemId.CARGO_SKCHEST, 80),ItemId.RUBIES: (140, ItemId.CARGO_SKCHEST, 15),ItemId.DIAMONDS: (250, ItemId.CARGO_SKCHEST, 5)}

def getCargoValue(itemId):
    entry = __cargoList.get(itemId)
    if entry:
        return entry[0]
    return 0


def getCargoCategory(itemId):
    entry = __cargoList.get(itemId)
    if entry:
        return entry[1]
    return None


def getCargoRarity(itemId):
    entry = __cargoList.get(itemId)
    if entry:
        return entry[2]
    return None


def getAllCargoType(cargoType):
    cargo = []
    for itemId in __cargoList:
        if __cargoList.get(itemId)[1] == cargoType:
            cargo.append(itemId)

    return cargo


def getCargoTotalValue(unpackedCargoList):
    total = 0
    for itemId in unpackedCargoList:
        total += getCargoValue(itemId)

    return total


def getRespecCost(numRespecs):
    if numRespecs <= 0:
        return 250
    elif numRespecs <= 1:
        return 2500
    else:
        return 10000


LAUNCH_FISHING_BOAT_COST = 1000
__itemList = {ItemId.MELEE_L1: (0, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 0, None),ItemId.MELEE_L2: (50, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 5, None),ItemId.MELEE_L3: (500, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 10, None),ItemId.MELEE_L4: (2500, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 15, None),ItemId.MELEE_L5: (10000, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 20, None),ItemId.MELEE_L6: (50000, ItemType.WEAPON, ItemType.MELEE, ItemType.COMBAT_WEAPON, 1, 25, None),ItemId.CUTLASS_L1: (40, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 0, InventoryType.CutlassToken),ItemId.CUTLASS_L2: (200, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 5, InventoryType.CutlassToken),ItemId.CUTLASS_L3: (1000, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 10, InventoryType.CutlassToken),ItemId.CUTLASS_L4: (5000, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 15, InventoryType.CutlassToken),ItemId.CUTLASS_L5: (10000, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 20, InventoryType.CutlassToken),ItemId.CUTLASS_L6: (25000, ItemType.WEAPON, ItemType.SWORD, ItemType.COMBAT_WEAPON, 1, 25, InventoryType.CutlassToken),ItemId.PISTOL_L1: (60, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 0, InventoryType.PistolToken),ItemId.PISTOL_L2: (300, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 5, InventoryType.PistolToken),ItemId.PISTOL_L3: (2000, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 10, InventoryType.PistolToken),ItemId.PISTOL_L4: (7500, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 15, InventoryType.PistolToken),ItemId.PISTOL_L5: (15000, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 20, InventoryType.PistolToken),ItemId.PISTOL_L6: (30000, ItemType.WEAPON, ItemType.PISTOL, ItemType.RANGED_WEAPON, 1, 25, InventoryType.PistolToken),ItemId.MUSKET_L1: (60, ItemType.WEAPON, ItemType.MUSKET, ItemType.RANGED_WEAPON, 1, 0, None),ItemId.MUSKET_L2: (600, ItemType.WEAPON, ItemType.MUSKET, ItemType.RANGED_WEAPON, 1, 5, None),ItemId.MUSKET_L3: (6000, ItemType.WEAPON, ItemType.MUSKET, ItemType.RANGED_WEAPON, 1, 15, None),ItemId.DAGGER_L1: (100, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 0, InventoryType.DaggerToken),ItemId.DAGGER_L2: (250, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 5, InventoryType.DaggerToken),ItemId.DAGGER_L3: (1250, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 10, InventoryType.DaggerToken),ItemId.DAGGER_L4: (7000, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 15, InventoryType.DaggerToken),ItemId.DAGGER_L5: (14000, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 20, InventoryType.DaggerToken),ItemId.DAGGER_L6: (28000, ItemType.WEAPON, ItemType.DAGGER, ItemType.COMBAT_WEAPON, 1, 25, InventoryType.DaggerToken),ItemId.GRENADE_L1: (200, ItemType.WEAPON, ItemType.GRENADE, ItemType.GRENADE_WEAPON, 1, 0, InventoryType.GrenadeToken),ItemId.WAND_L1: (100, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 0, InventoryType.WandToken),ItemId.WAND_L2: (300, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 5, InventoryType.WandToken),ItemId.WAND_L3: (1800, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 10, InventoryType.WandToken),ItemId.WAND_L4: (6000, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 15, InventoryType.WandToken),ItemId.WAND_L5: (12000, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 20, InventoryType.WandToken),ItemId.WAND_L6: (24000, ItemType.WEAPON, ItemType.WAND, ItemType.VOODOO_WEAPON, 1, 25, InventoryType.WandToken),ItemId.DOLL_L1: (80, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 0, InventoryType.DollToken),ItemId.DOLL_L2: (200, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 5, InventoryType.DollToken),ItemId.DOLL_L3: (1200, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 10, InventoryType.DollToken),ItemId.DOLL_L4: (2400, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 15, InventoryType.DollToken),ItemId.DOLL_L5: (4800, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 20, InventoryType.DollToken),ItemId.DOLL_L6: (20000, ItemType.WEAPON, ItemType.DOLL, ItemType.VOODOO_WEAPON, 1, 25, InventoryType.DollToken),ItemId.KETTLE_L1: (300, ItemType.WEAPON, ItemType.KETTLE, ItemType.VOODOO_WEAPON, 1, 0, None),ItemId.KETTLE_L2: (3000, ItemType.WEAPON, ItemType.KETTLE, ItemType.VOODOO_WEAPON, 1, 5, None),ItemId.KETTLE_L3: (30000, ItemType.WEAPON, ItemType.KETTLE, ItemType.VOODOO_WEAPON, 1, 15, None),ItemId.BAYONET_L1: (60, ItemType.WEAPON, ItemType.BAYONET, ItemType.RANGED_WEAPON, 1, 0, None),ItemId.BAYONET_L2: (600, ItemType.WEAPON, ItemType.BAYONET, ItemType.RANGED_WEAPON, 1, 5, None),ItemId.BAYONET_L3: (6000, ItemType.WEAPON, ItemType.BAYONET, ItemType.RANGED_WEAPON, 1, 15, None),ItemId.VENOMSHOT: (0.15, ItemType.AMMO, ItemType.PISTOLAMMO, None, 25, 0, None),ItemId.IRONSHOT: (0.2, ItemType.AMMO, ItemType.PISTOLAMMO, None, 25, 0, None),ItemId.GOLDENSHOT: (0.25, ItemType.AMMO, ItemType.PISTOLAMMO, None, 25, 0, None),ItemId.SILVERSHOT: (0.3, ItemType.AMMO, ItemType.PISTOLAMMO, None, 25, 0, None),ItemId.STEELSHOT: (0.35, ItemType.AMMO, ItemType.PISTOLAMMO, None, 25, 0, None),ItemId.ASP_DAGGER: (0.15, ItemType.AMMO, ItemType.DAGGERAMMO, None, 25, 0, None),ItemId.ADDER_DAGGER: (0.3, ItemType.AMMO, ItemType.DAGGERAMMO, None, 25, 0, None),ItemId.SIDEWINDER_DAGGER: (0.45, ItemType.AMMO, ItemType.DAGGERAMMO, None, 25, 0, None),ItemId.VIPERNEST_DAGGER: (1.5, ItemType.AMMO, ItemType.DAGGERAMMO, None, 5, 0, None),ItemId.EXPLOSION_G: (0.4, ItemType.AMMO, ItemType.GRENADEAMMO, None, 25, 0, None),ItemId.SHOCKBOMB_G: (0.5, ItemType.AMMO, ItemType.GRENADEAMMO, None, 10, 0, None),ItemId.FLAME_G: (0.6, ItemType.AMMO, ItemType.GRENADEAMMO, None, 10, 0, None),ItemId.SMOKE_G: (1.5, ItemType.AMMO, ItemType.GRENADEAMMO, None, 5, 0, None),ItemId.LANDMINE_G: (1.2, ItemType.AMMO, ItemType.GRENADEAMMO, None, 5, 0, None),ItemId.SIEGE_G: (2.0, ItemType.AMMO, ItemType.GRENADEAMMO, None, 5, 0, None),ItemId.POTION_1: (3, ItemType.CONSUMABLE, ItemType.POTION, None, 1, 0, None),ItemId.POTION_2: (6, ItemType.CONSUMABLE, ItemType.POTION, None, 1, 0, None),ItemId.POTION_3: (9, ItemType.CONSUMABLE, ItemType.POTION, None, 1, 0, None),ItemId.POTION_4: (15, ItemType.CONSUMABLE, ItemType.POTION, None, 1, 0, None),ItemId.POTION_5: (30, ItemType.CONSUMABLE, ItemType.POTION, None, 1, 0, None),ItemId.PORK_CHUNK: (0, ItemType.CONSUMABLE, ItemType.FOOD, None, 1, 0, None),ItemId.REMOVE_GROGGY: (0, ItemType.CONSUMABLE, ItemType.POTION, None, 1, 0, None),ItemId.SHIP_REPAIR_KIT: (50, ItemType.CONSUMABLE, ItemType.SHIP_REPAIR_KIT, None, 1, 0, None),ItemId.FISHING_ROD1: (0, ItemType.WEAPON, ItemType.FISHING_ROD, None, 1, 0, None),ItemId.FISHING_ROD2: (200, ItemType.WEAPON, ItemType.FISHING_ROD, None, 1, 5, None),ItemId.FISHING_ROD3: (300, ItemType.WEAPON, ItemType.FISHING_ROD, None, 1, 15, None),ItemId.FISHING_LURE1: (100, ItemType.AMMO, ItemType.FISHING_LURE, None, 1, 0, None),ItemId.FISHING_LURE2: (300, ItemType.AMMO, ItemType.FISHING_LURE, None, 1, 20, None),ItemId.INTERCEPTOR_L1: (100, ItemType.SHIP, ItemType.INTERCEPTOR, None, 1, 0, InventoryType.NewShipToken),ItemId.MERCHANT_L1: (300, ItemType.SHIP, ItemType.MERCHANT, None, 1, 0, InventoryType.NewShipToken),ItemId.WARSHIP_L1: (800, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.BRIG_L1: (900, ItemType.SHIP, ItemType.BRIG, None, 1, 0, InventoryType.NewShipToken),ItemId.INTERCEPTOR_L2: (1000, ItemType.SHIP, ItemType.INTERCEPTOR, None, 1, 5, InventoryType.NewShipToken),ItemId.MERCHANT_L2: (3500, ItemType.SHIP, ItemType.MERCHANT, None, 1, 5, InventoryType.NewShipToken),ItemId.WARSHIP_L2: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 5, InventoryType.NewShipToken),ItemId.BRIG_L2: (7000, ItemType.SHIP, ItemType.BRIG, None, 1, 5, InventoryType.NewShipToken),ItemId.INTERCEPTOR_L3: (20000, ItemType.SHIP, ItemType.INTERCEPTOR, None, 1, 15, InventoryType.NewShipToken),ItemId.MERCHANT_L3: (40000, ItemType.SHIP, ItemType.MERCHANT, None, 1, 15, InventoryType.NewShipToken),ItemId.WARSHIP_L3: (60000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 15, InventoryType.NewShipToken),ItemId.BRIG_L3: (80000, ItemType.SHIP, ItemType.BRIG, None, 1, 15, InventoryType.NewShipToken),ItemId.BLACK_PEARL: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.GOLIATH: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 30, InventoryType.NewShipToken),ItemId.DAUNTLESS: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 30, InventoryType.NewShipToken),ItemId.FLYING_DUTCHMAN: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 40, InventoryType.NewShipToken),ItemId.JOLLY_ROGER: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 40, InventoryType.NewShipToken),ItemId.SKEL_WARSHIPL3: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 30, InventoryType.NewShipToken),ItemId.SKEL_INTERCEPTORL3: (0, ItemType.SHIP, ItemType.INTERCEPTOR, None, 1, 30, InventoryType.NewShipToken),ItemId.SHIP_OF_THE_LINE: (200000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 30, InventoryType.NewShipToken),ItemId.EL_PATRONS_SHIP: (100000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 10, InventoryType.NewShipToken),ItemId.P_SKEL_PHANTOM: (170000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 25, InventoryType.NewShipToken),ItemId.P_SKEL_REVENANT: (190000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 25, InventoryType.NewShipToken),ItemId.P_SKEL_CEREBUS: (140000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 20, InventoryType.NewShipToken),ItemId.P_NAVY_KINGFISHER: (120000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 20, InventoryType.NewShipToken),ItemId.P_EITC_WARLORD: (180000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 20, InventoryType.NewShipToken),ItemId.QUEEN_ANNES_REVENGE: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.HUNTER_VENGEANCE: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.HUNTER_TALLYHO: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_WARSHIPL3: (0, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_INTERCEPTORL3: (0, ItemType.SHIP, ItemType.INTERCEPTOR, None, 1, 0, InventoryType.NewShipToken),ItemId.HMS_VICTORY: (200000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.HMS_NEWCASTLE: (200000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.HMS_INVINCIBLE: (200000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_INTREPID: (200000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_CONQUERER: (200000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_LEVIATHAN: (200000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_FERRET: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_BULWARK: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_PANTHER: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_GREYHOUND: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_VANGUARD: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_CENTURION: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_KINGFISHER: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_MONARCH: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_MAN_O_WAR: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_PREDATOR: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_COLOSSUS: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_DREADNOUGHT: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_BASTION: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.NAVY_ELITE: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_SEA_VIPER: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_SENTINEL: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_CORVETTE: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_BLOODHOUND: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_IRONWALL: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_MARAUDER: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_BARRACUDA: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_OGRE: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_WARLORD: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_CORSAIR: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_BEHEMOTH: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_JUGGERNAUT: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.EITC_TYRANT: (5000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_PHANTOM: (150000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_REVENANT: (160000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_STORM_REAPER: (170000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_BLACK_HARBINGER: (180000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_DEATH_OMEN: (190000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_SHADOW_CROW_FR: (100000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_HELLHOUND_FR: (125000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_BLOOD_SCOURGE_FR: (150000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_SHADOW_CROW_SP: (100000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_HELLHOUND_SP: (125000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.SKEL_BLOOD_SCOURGE_SP: (150000, ItemType.SHIP, ItemType.WARSHIP, None, 1, 0, InventoryType.NewShipToken),ItemId.CANNON_L1: (300, ItemType.SHIPPART, ItemType.CANNON, None, 1, 0, None),ItemId.CANNON_L2: (3000, ItemType.SHIPPART, ItemType.CANNON, None, 1, 0, None),ItemId.CANNON_L3: (30000, ItemType.SHIPPART, ItemType.CANNON, None, 1, 0, None),ItemId.ROUNDSHOT: (0, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.CHAIN_SHOT: (0.15, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.GRAPE_SHOT: (0.2, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.FIREBRAND: (0.5, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.THUNDERBOLT: (0.6, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.EXPLOSIVE: (15, ItemType.AMMO, ItemType.CANNONAMMO, None, 1, 0, None),ItemId.FURY: (0.8, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.GRAPPLE_HOOK: (0.2, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.BULLET: (0.2, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.GAS_CLOUD: (0.2, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.SKULL_AMMO: (0.3, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.FLAME_CLOUD: (0.3, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.FLAMING_SKULL: (0.3, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.BAR_SHOT: (0.4, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.KNIVES: (0.4, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.MINE: (0.5, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.BARNACLES: (0.5, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.COMET: (0.5, ItemType.AMMO, ItemType.CANNONAMMO, None, 25, 0, None),ItemId.MATERIAL_PINE: (0.1, ItemType.CONSUMABLE, ItemType.MATERIAL, None, 1, 0, None),ItemId.MATERIAL_OAK: (0.1, ItemType.CONSUMABLE, ItemType.MATERIAL, None, 1, 0, None),ItemId.MATERIAL_IRON: (0.1, ItemType.CONSUMABLE, ItemType.MATERIAL, None, 1, 0, None),ItemId.MATERIAL_STEEL: (0.1, ItemType.CONSUMABLE, ItemType.MATERIAL, None, 1, 0, None),ItemId.MATERIAL_SILK: (0.1, ItemType.CONSUMABLE, ItemType.MATERIAL, None, 1, 0, None),ItemId.MATERIAL_CANVAS: (0.1, ItemType.CONSUMABLE, ItemType.MATERIAL, None, 1, 0, None),ItemId.MATERIAL_GROG: (0.1, ItemType.CONSUMABLE, ItemType.MATERIAL, None, 1, 0, None),ItemId.SMALL_BOTTLE: (50, ItemType.BOTTLE, ItemType.BOTTLE, None, 1, 0, None),ItemId.MEDIUM_BOTTLE: (500, ItemType.BOTTLE, ItemType.BOTTLE, None, 1, 0, None),ItemId.LARGE_BOTTLE: (5000, ItemType.BOTTLE, ItemType.BOTTLE, None, 1, 0, None),ItemId.PISTOL_POUCH_L1: (300, ItemType.POUCH, ItemType.PISTOL_POUCH, None, 1, 7, InventoryType.PistolToken),ItemId.PISTOL_POUCH_L2: (1200, ItemType.POUCH, ItemType.PISTOL_POUCH, None, 1, 12, InventoryType.PistolToken),ItemId.PISTOL_POUCH_L3: (3600, ItemType.POUCH, ItemType.PISTOL_POUCH, None, 1, 17, InventoryType.PistolToken),ItemId.DAGGER_POUCH_L1: (200, ItemType.POUCH, ItemType.DAGGER_POUCH, None, 1, 7, InventoryType.DaggerToken),ItemId.DAGGER_POUCH_L2: (800, ItemType.POUCH, ItemType.DAGGER_POUCH, None, 1, 12, InventoryType.DaggerToken),ItemId.DAGGER_POUCH_L3: (2400, ItemType.POUCH, ItemType.DAGGER_POUCH, None, 1, 17, InventoryType.DaggerToken),ItemId.GRENADE_POUCH_L1: (1000, ItemType.POUCH, ItemType.GRENADE_POUCH, None, 1, 7, InventoryType.GrenadeToken),ItemId.GRENADE_POUCH_L2: (4000, ItemType.POUCH, ItemType.GRENADE_POUCH, None, 1, 12, InventoryType.GrenadeToken),ItemId.GRENADE_POUCH_L3: (12000, ItemType.POUCH, ItemType.GRENADE_POUCH, None, 1, 17, InventoryType.GrenadeToken),ItemId.CANNON_POUCH_L1: (500, ItemType.POUCH, ItemType.CANNON_POUCH, None, 1, 7, None),ItemId.CANNON_POUCH_L2: (2000, ItemType.POUCH, ItemType.CANNON_POUCH, None, 1, 12, None),ItemId.CANNON_POUCH_L3: (8000, ItemType.POUCH, ItemType.CANNON_POUCH, None, 1, 17, None)}

def getItemCost(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[0]
    else:
        return None
    return None


def getItemCategory(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[1]
    else:
        return None
    return None


__itemTypeNameList = {ItemGlobals.DAGGER: ItemType.DAGGER,ItemGlobals.SWORD: ItemType.SWORD,ItemGlobals.GUN: ItemType.PISTOL,ItemGlobals.DOLL: ItemType.DOLL,ItemGlobals.GRENADE: ItemType.GRENADE,ItemGlobals.STAFF: ItemType.WAND,ItemGlobals.POTION: ItemType.POTION}

def getItemType(itemId):
    typeId = ItemGlobals.getType(itemId)
    if typeId:
        return __itemTypeNameList.get(typeId)
    item = __itemList.get(itemId)
    if item:
        return item[2]
    else:
        return None
    return None


def getItemGroup(itemId):
    return __itemTypeList.get(getItemType(itemId))


def getWeaponClass(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[3]
    else:
        return None
    return None


def getItemQuantity(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[4]
    else:
        return None
    return None


def getItemMinLevel(itemId):
    item = __itemList.get(itemId)
    if item:
        return item[5]
    else:
        return 0


__itemTrainingList = {ItemGlobals.DAGGER: InventoryType.DaggerToken,ItemGlobals.SWORD: InventoryType.CutlassToken,ItemGlobals.GUN: InventoryType.PistolToken,ItemGlobals.DOLL: InventoryType.DollToken,ItemGlobals.GRENADE: InventoryType.GrenadeToken,ItemGlobals.STAFF: InventoryType.WandToken}

def getItemTrainingReq(itemId):
    typeId = ItemGlobals.getType(itemId)
    if typeId:
        return __itemTrainingList.get(typeId)
    item = __itemList.get(itemId)
    if item:
        return item[6]
    else:
        return 0


__itemIcons = {ItemId.CUTLASS_L1: 'pir_t_ico_swd_cutlass_a',ItemId.CUTLASS_L2: 'pir_t_ico_swd_broadsword_b',ItemId.CUTLASS_L3: 'pir_t_ico_swd_cutlass_c',ItemId.CUTLASS_L4: 'pir_t_ico_swd_cutlass_d',ItemId.CUTLASS_L5: 'pir_t_ico_swd_broadsword_c',ItemId.CUTLASS_L6: 'pir_t_ico_swd_cutlass_g',ItemId.PISTOL_L1: 'pir_t_ico_gun_pistol_a',ItemId.PISTOL_L2: 'pir_t_ico_gun_multiBarrel_a',ItemId.PISTOL_L3: 'pir_t_ico_gun_multiBarrel_c',ItemId.PISTOL_L4: 'pir_t_ico_gun_multiBarrel_d',ItemId.PISTOL_L5: 'pir_t_ico_gun_multiBarrel_e',ItemId.PISTOL_L6: 'pir_t_ico_gun_multiBarrel_f',ItemId.BAYONET_L1: 'pir_t_ico_gun_pistol_a',ItemId.BAYONET_L2: 'pir_t_ico_gun_multiBarrel_a',ItemId.BAYONET_L3: 'pir_t_ico_gun_multiBarrel_c',ItemId.DAGGER_L1: 'pir_t_ico_knf_small',ItemId.DAGGER_L2: 'pir_t_ico_knf_battle',ItemId.DAGGER_L3: 'pir_t_ico_knf_dirk_b',ItemId.DAGGER_L4: 'pir_t_ico_knf_hollow_b',ItemId.DAGGER_L5: 'pir_t_ico_knf_dagger_b',ItemId.DAGGER_L6: 'pir_t_ico_knf_dagger_c',ItemId.GRENADE_L1: 'pir_t_ico_bom_grenade',ItemId.GRENADE_L2: 'pir_t_ico_bom_grenade',ItemId.GRENADE_L3: 'pir_t_ico_bom_grenade',ItemId.GRENADE_L4: 'pir_t_ico_bom_grenade',ItemId.GRENADE_L5: 'pir_t_ico_bom_grenade',ItemId.GRENADE_L6: 'pir_t_ico_bom_grenade',ItemId.WAND_L1: 'pir_t_ico_stf_dark_a',ItemId.WAND_L2: 'pir_t_ico_stf_nature_a',ItemId.WAND_L3: 'pir_t_ico_stf_ward_a',ItemId.WAND_L4: 'pir_t_ico_stf_ward_b',ItemId.WAND_L5: 'pir_t_ico_stf_ward_c',ItemId.WAND_L6: 'pir_t_ico_stf_nature_c',ItemId.DOLL_L1: 'pir_t_ico_dol_spirit_a',ItemId.DOLL_L2: 'pir_t_ico_dol_mojo_a',ItemId.DOLL_L3: 'pir_t_ico_dol_mojo_c',ItemId.DOLL_L4: 'pir_t_ico_dol_bane_c',ItemId.DOLL_L5: 'pir_t_ico_dol_mojo_e',ItemId.DOLL_L6: 'pir_t_ico_dol_bane_e',ItemId.CANNON_L1: 'pir_t_ico_can_single',ItemId.CANNON_L2: 'pir_t_ico_can_single',ItemId.CANNON_L3: 'pir_t_ico_can_single',ItemId.POTION_1: 'pit_t_ico_tonic',ItemId.POTION_2: 'pit_t_ico_tonic',ItemId.POTION_3: 'pir_t_ico_pot_holyWater',ItemId.POTION_4: 'pir_t_ico_pot_elixir',ItemId.POTION_5: 'pir_t_ico_pot_miracleWater',ItemId.REMOVE_GROGGY: 'pir_t_ico_pot_miracleWater',ItemId.PORK_CHUNK: 'pir_t_ico_pot_porkTonic',ItemId.SHIP_REPAIR_KIT: 'sail_come_about',ItemId.PISTOL_POUCH_L1: 'pir_t_ico_gun_shotPouch',ItemId.PISTOL_POUCH_L2: 'pir_t_ico_gun_shotPouch',ItemId.PISTOL_POUCH_L3: 'pir_t_ico_gun_shotPouch',ItemId.DAGGER_POUCH_L1: 'pir_t_ico_knf_belt',ItemId.DAGGER_POUCH_L2: 'pir_t_ico_knf_belt',ItemId.DAGGER_POUCH_L3: 'pir_t_ico_knf_belt',ItemId.GRENADE_POUCH_L1: 'pir_t_ico_bom_pouch',ItemId.GRENADE_POUCH_L2: 'pir_t_ico_bom_pouch',ItemId.GRENADE_POUCH_L3: 'pir_t_ico_bom_pouch',ItemId.CANNON_POUCH_L1: 'pir_t_ico_can_ammoBarrel',ItemId.CANNON_POUCH_L2: 'pir_t_ico_can_ammoBarrel',ItemId.CANNON_POUCH_L3: 'pir_t_ico_can_ammoBarrel',ItemId.FISHING_POUCH_L1: 'pir_t_ico_can_ammoBarrel',ItemId.FISHING_ROD1: 'pir_t_gui_fsh_smRodIcon',ItemId.FISHING_ROD2: 'pir_t_gui_fsh_mdRodIcon',ItemId.FISHING_ROD3: 'pir_t_gui_fsh_lgRodIcon',ItemId.FISHING_LURE1: 'pir_t_gui_fsh_lureReg',ItemId.FISHING_LURE2: 'pir_t_gui_fsh_lureLegend',ItemId.MATERIAL_BASIC: 'pir_t_ico_bom_pouch',ItemId.MATERIAL_UNCOMMON: 'pir_t_ico_bom_pouch',ItemId.MATERIAL_PINE: 'pir_t_gui_sc_pine',ItemId.MATERIAL_OAK: 'pir_t_gui_sc_oak',ItemId.MATERIAL_IRON: 'pir_t_gui_sc_iron',ItemId.MATERIAL_STEEL: 'pir_t_gui_sc_steel',ItemId.MATERIAL_SILK: 'pir_t_gui_sc_silk',ItemId.MATERIAL_CANVAS: 'pir_t_gui_sc_canvas',ItemId.MATERIAL_GROG: 'pir_t_gui_sc_grog',ItemGlobals.TONIC: 'pir_t_ico_pot_tonic',ItemGlobals.REMEDY: 'pir_t_ico_pot_tonic',ItemGlobals.HOLY_WATER: 'pir_t_ico_pot_holyWater',ItemGlobals.ELIXIR: 'pir_t_ico_pot_elixir',ItemGlobals.MIRACLE_WATER: 'pir_t_ico_pot_miracleWater',ItemGlobals.ROAST_PORK: 'pir_t_ico_pot_porkTonic'}

def getItemIcons(itemId):
    item = __itemIcons.get(itemId)
    if item:
        return item
    else:
        return None
    return None


__itemTypeIcons = {ItemType.PISTOL_POUCH: 'pir_t_ico_gun_shotPouch',ItemType.DAGGER_POUCH: 'pir_t_ico_knf_belt',ItemType.GRENADE_POUCH: 'pir_t_ico_bom_pouch',ItemType.CANNON_POUCH: 'pir_t_ico_can_ammoBarrel',ItemType.FISHING_POUCH: 'pir_t_gui_fsh_tackleBasket'}

def getItemTypeIcon(ammoTypeId):
    item = __itemTypeIcons.get(ammoTypeId)
    if item:
        return item
    else:
        return None
    return None


MELEE_SHELF_L1 = []
MELEE_SHELF_L2 = [
 ItemId.CUTLASS_L2, ItemId.CUTLASS_L3, ItemId.DAGGER_L2, ItemId.DAGGER_L3]
MELEE_SHELF_L3 = [
 ItemId.CUTLASS_L5, ItemId.CUTLASS_L6, ItemId.DAGGER_L5, ItemId.DAGGER_L6]
MISSILE_SHELF_L1 = []
MISSILE_SHELF_L2 = [
 ItemId.PISTOL_L2, ItemId.PISTOL_L3]
MISSILE_SHELF_L3 = [
 ItemId.PISTOL_L5, ItemId.PISTOL_L6]
DAGGER_AMMO_SHELF_L1 = [
 ItemId.ASP_DAGGER, ItemId.ADDER_DAGGER]
DAGGER_AMMO_SHELF_L2 = [
 ItemId.SIDEWINDER_DAGGER, ItemId.VIPERNEST_DAGGER]
CANNON_AMMO_SHELF_L1 = [
 ItemId.CHAIN_SHOT, ItemId.GRAPE_SHOT]
CANNON_AMMO_SHELF_L2 = [
 ItemId.FIREBRAND, ItemId.THUNDERBOLT, ItemId.EXPLOSIVE, ItemId.FURY]
SIEGE_SHELF = [
 ItemId.SHIP_REPAIR_KIT]
PISTOL_AMMO_SHELF_L1 = [
 ItemId.VENOMSHOT, ItemId.IRONSHOT]
PISTOL_AMMO_SHELF_L2 = [
 ItemId.GOLDENSHOT, ItemId.SILVERSHOT, ItemId.STEELSHOT]
PISTOL_POUCH_SHELF = [
 ItemId.PISTOL_POUCH_L1, ItemId.PISTOL_POUCH_L2, ItemId.PISTOL_POUCH_L3]
DAGGER_POUCH_SHELF = [
 ItemId.DAGGER_POUCH_L1, ItemId.DAGGER_POUCH_L2, ItemId.DAGGER_POUCH_L3]
GRENADE_POUCH_SHELF = [
 ItemId.GRENADE_POUCH_L1, ItemId.GRENADE_POUCH_L2, ItemId.GRENADE_POUCH_L3]
CANNON_POUCH_SHELF = [
 ItemId.CANNON_POUCH_L1, ItemId.CANNON_POUCH_L2, ItemId.CANNON_POUCH_L3]
BOMB_AMMO_SHELF_L1 = [
 ItemId.SHOCKBOMB_G, ItemId.FLAME_G]
BOMB_AMMO_SHELF_L2 = [
 ItemId.SMOKE_G, ItemId.SIEGE_G]
TONIC_SHELF_L1 = [
 ItemId.POTION_1, ItemId.POTION_2, ItemId.POTION_3]
TONIC_SHELF_L2 = [
 ItemId.POTION_4, ItemId.POTION_5]
BOMB_SHELF_L1 = []
BOMB_SHELF_L2 = []
BOMB_SHELF_L3 = []
WEAPON_SHELF_ALL = CANNON_AMMO_SHELF_L1
SHIP_ITEM_SHELF = [
 ItemId.SMALL_BOTTLE, ItemId.MEDIUM_BOTTLE, ItemId.LARGE_BOTTLE]
MUSIC_SHELF = [
 InventoryType.Song_1, InventoryType.Song_2, InventoryType.Song_3, InventoryType.Song_4, InventoryType.Song_5, InventoryType.Song_6, InventoryType.Song_7, InventoryType.Song_8, InventoryType.Song_9, InventoryType.Song_10, InventoryType.Song_11, InventoryType.Song_12, InventoryType.Song_13, InventoryType.Song_14, InventoryType.Song_15, InventoryType.Song_16, InventoryType.Song_17, InventoryType.Song_18, InventoryType.Song_19, InventoryType.Song_20, InventoryType.Song_21, InventoryType.Song_22]
MOJO_SHELF_L1 = []
MOJO_SHELF_L2 = [
 ItemId.WAND_L2, ItemId.WAND_L3, ItemId.DOLL_L2, ItemId.DOLL_L3]
MOJO_SHELF_L3 = [
 ItemId.WAND_L5, ItemId.WAND_L6, ItemId.DOLL_L5, ItemId.DOLL_L6]
MOJO_SHELF_ALL = MOJO_SHELF_L1 + MOJO_SHELF_L2 + MOJO_SHELF_L3
SHIP_SHELF = [
 ItemId.INTERCEPTOR_L1, ItemId.MERCHANT_L1, ItemId.WARSHIP_L1, ItemId.BRIG_L1, ItemId.INTERCEPTOR_L2, ItemId.MERCHANT_L2, ItemId.WARSHIP_L2, ItemId.BRIG_L2, ItemId.INTERCEPTOR_L3, ItemId.MERCHANT_L3, ItemId.WARSHIP_L3, ItemId.BRIG_L3]
STOWAWAY_SHELF = [
 LocationIds.PORT_ROYAL_ISLAND, LocationIds.TORTUGA_ISLAND, LocationIds.CUBA_ISLAND, LocationIds.DEL_FUEGO_ISLAND]
FISHING_ROD_SHELF = [
 ItemId.FISHING_ROD2, ItemId.FISHING_ROD3]
FISHING_LURE_SHELF = [
 ItemId.FISHING_LURE1, ItemId.FISHING_LURE2]
CollectionValues = {0: 10,1: 25,2: 100}
__pouchTypeToAmmo = {ItemType.PISTOL_POUCH: [ItemId.VENOMSHOT, ItemId.IRONSHOT, ItemId.GOLDENSHOT, ItemId.SILVERSHOT, ItemId.STEELSHOT],ItemType.DAGGER_POUCH: [ItemId.ASP_DAGGER, ItemId.ADDER_DAGGER, ItemId.SIDEWINDER_DAGGER, ItemId.VIPERNEST_DAGGER],ItemType.GRENADE_POUCH: [ItemId.SHOCKBOMB_G, ItemId.FLAME_G, ItemId.SMOKE_G, ItemId.SIEGE_G],ItemType.CANNON_POUCH: [ItemId.CHAIN_SHOT, ItemId.GRAPE_SHOT, ItemId.FIREBRAND, ItemId.THUNDERBOLT, ItemId.EXPLOSIVE, ItemId.FURY],ItemType.FISHING_POUCH: [ItemId.FISHING_LURE1, ItemId.FISHING_LURE2]}

def getPouchAmmoList(pouchType):
    ammoList = __pouchTypeToAmmo.get(pouchType)
    if ammoList:
        return ammoList
    else:
        return None
    return None


__ammoTypeToPouchType = {}
for pouchKey in __pouchTypeToAmmo:
    for ammoType in __pouchTypeToAmmo[pouchKey]:
        __ammoTypeToPouchType[ammoType] = pouchKey

__pouchTypeToPouchs = {ItemType.PISTOL_POUCH: [ItemId.PISTOL_POUCH_L1, ItemId.PISTOL_POUCH_L2, ItemId.PISTOL_POUCH_L3],ItemType.DAGGER_POUCH: [ItemId.DAGGER_POUCH_L1, ItemId.DAGGER_POUCH_L2, ItemId.DAGGER_POUCH_L3],ItemType.GRENADE_POUCH: [ItemId.GRENADE_POUCH_L1, ItemId.GRENADE_POUCH_L2, ItemId.GRENADE_POUCH_L3],ItemType.CANNON_POUCH: [ItemId.CANNON_POUCH_L1, ItemId.CANNON_POUCH_L2, ItemId.CANNON_POUCH_L3],ItemType.FISHING_POUCH: [ItemId.FISHING_POUCH_L1]}

def getListOfPouches(pouchType):
    return __pouchTypeToPouchs[pouchType]


def forAmmoIdGetListofPouches(ammoId):
    pouchType = __ammoTypeToPouchType[ammoId]
    return __pouchTypeToPouchs[pouchType]


def forAmmoIdGetPouchType(ammoId):
    return __ammoTypeToPouchType.get(ammoId)


__pouchInventoryBonus = {ItemId.PISTOL_POUCH_L1: [125, 125, 125, 125, 125],ItemId.PISTOL_POUCH_L2: [150, 150, 150, 150, 150],ItemId.PISTOL_POUCH_L3: [175, 175, 175, 175, 175],ItemId.DAGGER_POUCH_L1: [125, 75, 75, 35],ItemId.DAGGER_POUCH_L2: [150, 100, 100, 45],ItemId.DAGGER_POUCH_L3: [175, 125, 125, 60],ItemId.GRENADE_POUCH_L1: [100, 60, 60, 30, 30],ItemId.GRENADE_POUCH_L2: [125, 70, 70, 35, 35],ItemId.GRENADE_POUCH_L3: [150, 80, 80, 40, 40],ItemId.CANNON_POUCH_L1: [125, 125, 75, 75, 6, 75],ItemId.CANNON_POUCH_L2: [150, 150, 100, 100, 9, 100],ItemId.CANNON_POUCH_L3: [175, 175, 125, 125, 12, 125],ItemId.FISHING_POUCH_L1: [10, 10]}

def getInventoryBonus(itemId, index=-1):
    amount = __pouchInventoryBonus.get(itemId)
    if amount:
        if index >= 0:
            return amount[index]
        return amount
    return 0


StowawayCost = {LocationIds.PORT_ROYAL_ISLAND: 25,LocationIds.TORTUGA_ISLAND: 25,LocationIds.CUBA_ISLAND: 50,LocationIds.DEL_FUEGO_ISLAND: 200}