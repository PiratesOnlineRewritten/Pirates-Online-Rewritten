import copy
import math
import cPickle
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import *
from direct.showbase import AppRunnerGlobal
from pirates.battle.EnemySkills import *
from pirates.battle import CannonGlobals
from pirates.piratesbase import PLocalizer
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.economy import EconomyGlobals
from pirates.reputation import RepChart
from pirates.inventory import ItemGlobals
import random
import os
import copy
import Pistol
import Sword
import Doll
import Melee
import Dagger
import Grenade
import Wand
import Bayonet
import MonsterMelee
import Consumable
import Weapon
import DualCutlass
import Foil
import FishingRod
import Gun
import Torch
import PowderKeg
from WeaponConstants import *
__defensiveBuffs = [
 C_TAKECOVER, C_OPENFIRE, C_ATTUNE, C_HASTEN, C_REGEN, C_CANNON_DAMAGE_LVL1, C_CANNON_DAMAGE_LVL2, C_CANNON_DAMAGE_LVL3, C_PISTOL_DAMAGE_LVL1, C_PISTOL_DAMAGE_LVL2, C_PISTOL_DAMAGE_LVL3, C_CUTLASS_DAMAGE_LVL1, C_CUTLASS_DAMAGE_LVL2, C_CUTLASS_DAMAGE_LVL3, C_DOLL_DAMAGE_LVL1, C_DOLL_DAMAGE_LVL2, C_DOLL_DAMAGE_LVL3, C_REP_BONUS_LVL1, C_REP_BONUS_LVL2, C_REP_BONUS_LVL3, C_GOLD_BONUS_LVL1, C_GOLD_BONUS_LVL2, C_BURP, C_FART, C_FART_LVL2, C_VOMIT, C_HASTEN_LVL1, C_HASTEN_LVL2, C_HASTEN_LVL3, C_ACCURACY_BONUS_LVL1, C_ACCURACY_BONUS_LVL2, C_ACCURACY_BONUS_LVL3, C_REGEN_LVL1, C_REGEN_LVL2, C_REGEN_LVL3, C_REGEN_LVL4, C_HEAD_FIRE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2, C_WRECKHULL, C_WRECKMASTS, C_SINKHER, C_INCOMING, C_SPIRIT, C_QUICKLOAD, C_DARK_CURSE, C_MASTERS_RIPOSTE, C_MONKEY_PANIC, C_VOODOO_REFLECT, C_RED_FURY, C_GHOST_FORM, C_HEAD_GROW, C_CRAZY_SKIN_COLOR, C_SIZE_REDUCE, C_SIZE_INCREASE, C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_SUMMON_CHICKEN, C_REP_BONUS_LVLCOMP, C_SUMMON_MONKEY, C_SUMMON_WASP, C_SUMMON_DOG]
_compEffects = [
 C_REP_BONUS_LVLCOMP]

def getIsDefensiveBuff(effectId):
    return __defensiveBuffs.count(effectId)


def getIsCompEffect(effectId):
    return _compEffects.count(effectId)


__transformationBuffs = [
 C_HEAD_FIRE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2, C_HEAD_GROW, C_CRAZY_SKIN_COLOR, C_SIZE_REDUCE, C_SIZE_INCREASE, C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM]

def getIsTransformationBuff(effectId):
    return __transformationBuffs.count(effectId)


BD_NULL = 0
BD_1INT = 1
BD_2INT = 2
BD_MULTIPLIER = 3
BD_1FLOAT = 4
vfs = VirtualFileSystem.getGlobalPtr()
filename = Filename('WeaponGlobals.pkl')
searchPath = DSearchPath()
if AppRunnerGlobal.appRunner:
    searchPath.appendDirectory(Filename.expandFrom('$POTCO_2_ROOT/etc'))
else:
    searchPath.appendDirectory(Filename.expandFrom('$PIRATES/src/battle'))
    searchPath.appendDirectory(Filename.expandFrom('pirates/src/battle'))
    searchPath.appendDirectory(Filename.expandFrom('pirates/battle'))
    searchPath.appendDirectory(Filename('.'))
    searchPath.appendDirectory(Filename('etc'))
found = vfs.resolveFilename(filename, searchPath)
if not found:
    message = 'WeaponGlobals.pkl file not found on %s' % searchPath
    raise IOError, message
data = vfs.readFile(filename, 1)
__skillInfo = cPickle.loads(data)
__attackEffectsSkillInfo = {}
__columnHeadings = __skillInfo.pop('columnHeadings')
for heading, value in __columnHeadings.items():
    exec '%s = %s' % (heading, value) in globals()

del searchPath
del __columnHeadings
del data
NA = -1
TARGET_SELECT_BUTTON = 'mouse1'
TEAM_COMBO_WINDOW = 2.0
NUM_PLAYER_WEAPONS = 6
COMBAT = 1
FIREARM = 2
GRENADE = 3
VOODOO = 4
STAFF = 5
MELEE = 6
THROWING = 7
CONSUMABLE = 7
SAILING = 8
CANNON = 9
FISHING = 10
DEFENSE_CANNON = 11
__humanWeapons = {InventoryType.MeleeWeaponL1: MELEE,InventoryType.MeleeWeaponL2: MELEE,InventoryType.MeleeWeaponL3: MELEE,InventoryType.MeleeWeaponL4: MELEE,InventoryType.MeleeWeaponL5: MELEE,InventoryType.MeleeWeaponL6: MELEE,InventoryType.CutlassWeaponL1: COMBAT,InventoryType.CutlassWeaponL2: COMBAT,InventoryType.CutlassWeaponL3: COMBAT,InventoryType.CutlassWeaponL4: COMBAT,InventoryType.CutlassWeaponL5: COMBAT,InventoryType.CutlassWeaponL6: COMBAT,InventoryType.PistolWeaponL1: FIREARM,InventoryType.PistolWeaponL2: FIREARM,InventoryType.PistolWeaponL3: FIREARM,InventoryType.PistolWeaponL4: FIREARM,InventoryType.PistolWeaponL5: FIREARM,InventoryType.PistolWeaponL6: FIREARM,InventoryType.MusketWeaponL1: FIREARM,InventoryType.MusketWeaponL2: FIREARM,InventoryType.MusketWeaponL3: FIREARM,InventoryType.BayonetWeaponL1: FIREARM,InventoryType.BayonetWeaponL2: FIREARM,InventoryType.BayonetWeaponL3: FIREARM,InventoryType.DaggerWeaponL1: THROWING,InventoryType.DaggerWeaponL2: THROWING,InventoryType.DaggerWeaponL3: THROWING,InventoryType.DaggerWeaponL4: THROWING,InventoryType.DaggerWeaponL5: THROWING,InventoryType.DaggerWeaponL6: THROWING,InventoryType.GrenadeWeaponL1: GRENADE,InventoryType.GrenadeWeaponL2: GRENADE,InventoryType.GrenadeWeaponL3: GRENADE,InventoryType.GrenadeWeaponL4: GRENADE,InventoryType.GrenadeWeaponL5: GRENADE,InventoryType.GrenadeWeaponL6: GRENADE,InventoryType.WandWeaponL1: STAFF,InventoryType.WandWeaponL2: STAFF,InventoryType.WandWeaponL3: STAFF,InventoryType.WandWeaponL4: STAFF,InventoryType.WandWeaponL5: STAFF,InventoryType.WandWeaponL6: STAFF,InventoryType.DollWeaponL1: VOODOO,InventoryType.DollWeaponL2: VOODOO,InventoryType.DollWeaponL3: VOODOO,InventoryType.DollWeaponL4: VOODOO,InventoryType.DollWeaponL5: VOODOO,InventoryType.DollWeaponL6: VOODOO,InventoryType.KettleWeaponL1: VOODOO,InventoryType.KettleWeaponL2: VOODOO,InventoryType.KettleWeaponL3: VOODOO,InventoryType.Potion1: CONSUMABLE,InventoryType.Potion2: CONSUMABLE,InventoryType.Potion3: CONSUMABLE,InventoryType.Potion4: CONSUMABLE,InventoryType.Potion5: CONSUMABLE,InventoryType.CannonDamageLvl1: CONSUMABLE,InventoryType.CannonDamageLvl2: CONSUMABLE,InventoryType.CannonDamageLvl3: CONSUMABLE,InventoryType.PistolDamageLvl1: CONSUMABLE,InventoryType.PistolDamageLvl2: CONSUMABLE,InventoryType.PistolDamageLvl3: CONSUMABLE,InventoryType.CutlassDamageLvl1: CONSUMABLE,InventoryType.CutlassDamageLvl2: CONSUMABLE,InventoryType.CutlassDamageLvl3: CONSUMABLE,InventoryType.DollDamageLvl1: CONSUMABLE,InventoryType.DollDamageLvl2: CONSUMABLE,InventoryType.DollDamageLvl3: CONSUMABLE,InventoryType.HastenLvl1: CONSUMABLE,InventoryType.HastenLvl2: CONSUMABLE,InventoryType.HastenLvl3: CONSUMABLE,InventoryType.RepBonusLvl1: CONSUMABLE,InventoryType.RepBonusLvl2: CONSUMABLE,InventoryType.RepBonusLvl3: CONSUMABLE,InventoryType.RepBonusLvlComp: CONSUMABLE,InventoryType.GoldBonusLvl1: CONSUMABLE,InventoryType.GoldBonusLvl2: CONSUMABLE,InventoryType.InvisibilityLvl1: CONSUMABLE,InventoryType.InvisibilityLvl2: CONSUMABLE,InventoryType.RegenLvl1: CONSUMABLE,InventoryType.RegenLvl2: CONSUMABLE,InventoryType.RegenLvl3: CONSUMABLE,InventoryType.RegenLvl4: CONSUMABLE,InventoryType.Burp: CONSUMABLE,InventoryType.Fart: CONSUMABLE,InventoryType.FartLvl2: CONSUMABLE,InventoryType.Vomit: CONSUMABLE,InventoryType.HeadGrow: CONSUMABLE,InventoryType.FaceColor: CONSUMABLE,InventoryType.SizeReduce: CONSUMABLE,InventoryType.SizeIncrease: CONSUMABLE,InventoryType.HeadFire: CONSUMABLE,InventoryType.ScorpionTransform: CONSUMABLE,InventoryType.AlligatorTransform: CONSUMABLE,InventoryType.CrabTransform: CONSUMABLE,InventoryType.AccuracyBonusLvl1: CONSUMABLE,InventoryType.AccuracyBonusLvl2: CONSUMABLE,InventoryType.AccuracyBonusLvl3: CONSUMABLE,InventoryType.RemoveGroggy: CONSUMABLE,InventoryType.ShipRepairKit: CONSUMABLE,InventoryType.PorkChunk: CONSUMABLE}
__enemyWeapons = {InventoryType.MonsterWeaponL1: COMBAT,InventoryType.MonsterWeaponL2: COMBAT,InventoryType.MonsterWeaponL3: COMBAT,InventoryType.MonsterWeaponL4: COMBAT,InventoryType.MonsterWeaponL5: COMBAT,InventoryType.DualCutlassL1: COMBAT,InventoryType.FoilL1: COMBAT}
__typeWeapons = {ItemGlobals.SWORD: COMBAT,ItemGlobals.GUN: FIREARM,ItemGlobals.DOLL: VOODOO,ItemGlobals.DAGGER: THROWING,ItemGlobals.GRENADE: GRENADE,ItemGlobals.STAFF: STAFF,ItemGlobals.AXE: COMBAT,ItemGlobals.FENCING: COMBAT,ItemGlobals.POTION: CONSUMABLE,ItemGlobals.QUEST_PROP: COMBAT}

def getWeaponTypes():
    return __humanWeapons.keys() + __enemyWeapons.keys()


def getHumanWeaponTypes():
    return ItemGlobals.getHumanWeaponTypes()


def getWeaponCategory(weaponId):
    weaponDict = __typeWeapons.copy()
    weaponDict.update(__humanWeapons.copy())
    weaponDict.update(__enemyWeapons.copy())
    typeId = ItemGlobals.getType(weaponId)
    if typeId:
        return weaponDict.get(typeId)
    else:
        return weaponDict.get(weaponId)


__dcFieldNames = {InventoryType.MeleeRep: 'Melee',InventoryType.CutlassRep: 'Cutlass',InventoryType.PistolRep: 'Pistol',InventoryType.MusketRep: 'Musket',InventoryType.DaggerRep: 'Dagger',InventoryType.GrenadeRep: 'Grenade',InventoryType.DollRep: 'Doll',InventoryType.WandRep: 'Wand',InventoryType.KettleRep: 'Kettle',InventoryType.CannonRep: 'Cannon',InventoryType.FishingRep: 'Fishing'}
__weaponId2Class = {InventoryType.MeleeWeaponL1: Melee.Melee,InventoryType.MeleeWeaponL2: Melee.Melee,InventoryType.MeleeWeaponL3: Melee.Melee,InventoryType.MeleeWeaponL4: Melee.Melee,InventoryType.MeleeWeaponL5: Melee.Melee,InventoryType.MeleeWeaponL6: Melee.Melee,InventoryType.CutlassWeaponL1: Sword.Sword,InventoryType.CutlassWeaponL2: Sword.Sword,InventoryType.CutlassWeaponL3: Sword.Sword,InventoryType.CutlassWeaponL4: Sword.Sword,InventoryType.CutlassWeaponL5: Sword.Sword,InventoryType.CutlassWeaponL6: Sword.Sword,InventoryType.PistolWeaponL1: Pistol.Pistol,InventoryType.PistolWeaponL2: Gun.Gun,InventoryType.PistolWeaponL3: Gun.Gun,InventoryType.PistolWeaponL4: Pistol.Pistol,InventoryType.PistolWeaponL5: Pistol.Pistol,InventoryType.PistolWeaponL6: Pistol.Pistol,InventoryType.MusketWeaponL1: Gun.Gun,InventoryType.MusketWeaponL2: Gun.Gun,InventoryType.MusketWeaponL3: Gun.Gun,InventoryType.BayonetWeaponL1: Bayonet.Bayonet,InventoryType.BayonetWeaponL2: Bayonet.Bayonet,InventoryType.BayonetWeaponL3: Bayonet.Bayonet,InventoryType.DaggerWeaponL1: Dagger.Dagger,InventoryType.DaggerWeaponL2: Dagger.Dagger,InventoryType.DaggerWeaponL3: Dagger.Dagger,InventoryType.DaggerWeaponL4: Dagger.Dagger,InventoryType.DaggerWeaponL5: Dagger.Dagger,InventoryType.DaggerWeaponL6: Dagger.Dagger,InventoryType.GrenadeWeaponL1: Grenade.Grenade,InventoryType.GrenadeWeaponL2: Grenade.Grenade,InventoryType.GrenadeWeaponL3: Grenade.Grenade,InventoryType.GrenadeWeaponL4: Grenade.Grenade,InventoryType.GrenadeWeaponL5: Grenade.Grenade,InventoryType.GrenadeWeaponL6: Grenade.Grenade,InventoryType.WandWeaponL1: Wand.Wand,InventoryType.WandWeaponL2: Wand.Wand,InventoryType.WandWeaponL3: Wand.Wand,InventoryType.WandWeaponL4: Wand.Wand,InventoryType.WandWeaponL5: Wand.Wand,InventoryType.WandWeaponL6: Wand.Wand,InventoryType.DollWeaponL1: Doll.Doll,InventoryType.DollWeaponL2: Doll.Doll,InventoryType.DollWeaponL3: Doll.Doll,InventoryType.DollWeaponL4: Doll.Doll,InventoryType.DollWeaponL5: Doll.Doll,InventoryType.DollWeaponL6: Doll.Doll,InventoryType.Potion1: Consumable.Consumable,InventoryType.Potion2: Consumable.Consumable,InventoryType.Potion3: Consumable.Consumable,InventoryType.Potion4: Consumable.Consumable,InventoryType.Potion5: Consumable.Consumable,InventoryType.CannonDamageLvl1: Consumable.Consumable,InventoryType.CannonDamageLvl2: Consumable.Consumable,InventoryType.CannonDamageLvl3: Consumable.Consumable,InventoryType.PistolDamageLvl1: Consumable.Consumable,InventoryType.PistolDamageLvl2: Consumable.Consumable,InventoryType.PistolDamageLvl3: Consumable.Consumable,InventoryType.CutlassDamageLvl1: Consumable.Consumable,InventoryType.CutlassDamageLvl2: Consumable.Consumable,InventoryType.CutlassDamageLvl3: Consumable.Consumable,InventoryType.DollDamageLvl1: Consumable.Consumable,InventoryType.DollDamageLvl2: Consumable.Consumable,InventoryType.DollDamageLvl3: Consumable.Consumable,InventoryType.HastenLvl1: Consumable.Consumable,InventoryType.HastenLvl2: Consumable.Consumable,InventoryType.HastenLvl3: Consumable.Consumable,InventoryType.RepBonusLvl1: Consumable.Consumable,InventoryType.RepBonusLvl2: Consumable.Consumable,InventoryType.RepBonusLvl3: Consumable.Consumable,InventoryType.RepBonusLvlComp: Consumable.Consumable,InventoryType.GoldBonusLvl1: Consumable.Consumable,InventoryType.GoldBonusLvl2: Consumable.Consumable,InventoryType.InvisibilityLvl1: Consumable.Consumable,InventoryType.InvisibilityLvl2: Consumable.Consumable,InventoryType.RegenLvl1: Consumable.Consumable,InventoryType.RegenLvl2: Consumable.Consumable,InventoryType.RegenLvl3: Consumable.Consumable,InventoryType.RegenLvl4: Consumable.Consumable,InventoryType.Burp: Consumable.Consumable,InventoryType.Fart: Consumable.Consumable,InventoryType.FartLvl2: Consumable.Consumable,InventoryType.Vomit: Consumable.Consumable,InventoryType.HeadGrow: Consumable.Consumable,InventoryType.FaceColor: Consumable.Consumable,InventoryType.SizeReduce: Consumable.Consumable,InventoryType.SizeIncrease: Consumable.Consumable,InventoryType.HeadFire: Consumable.Consumable,InventoryType.ScorpionTransform: Consumable.Consumable,InventoryType.AlligatorTransform: Consumable.Consumable,InventoryType.CrabTransform: Consumable.Consumable,InventoryType.AccuracyBonusLvl1: Consumable.Consumable,InventoryType.AccuracyBonusLvl2: Consumable.Consumable,InventoryType.AccuracyBonusLvl3: Consumable.Consumable,InventoryType.RemoveGroggy: Consumable.Consumable,InventoryType.RemoveGroggy: Consumable.Consumable,InventoryType.ShipRepairKit: Consumable.Consumable,InventoryType.PorkChunk: Consumable.Consumable,InventoryType.MonsterWeaponL1: MonsterMelee.MonsterMelee,InventoryType.MonsterWeaponL2: MonsterMelee.MonsterMelee,InventoryType.MonsterWeaponL3: MonsterMelee.MonsterMelee,InventoryType.MonsterWeaponL4: MonsterMelee.MonsterMelee,InventoryType.MonsterWeaponL5: MonsterMelee.MonsterMelee,InventoryType.DualCutlassL1: DualCutlass.DualCutlass,InventoryType.FoilL1: Foil.Foil}
__typeId2Class = {ItemGlobals.SWORD: Sword.Sword,ItemGlobals.DOLL: Doll.Doll,ItemGlobals.DAGGER: Dagger.Dagger,ItemGlobals.GRENADE: Grenade.Grenade,ItemGlobals.STAFF: Wand.Wand,ItemGlobals.AXE: Sword.Sword,ItemGlobals.FENCING: Sword.Sword,ItemGlobals.POTION: Consumable.Consumable,ItemGlobals.FISHING: FishingRod.FishingRod,ItemGlobals.MONSTER: MonsterMelee.MonsterMelee}
__subtypeId2Class = {ItemGlobals.PISTOL: Pistol.Pistol,ItemGlobals.REPEATER: Pistol.Pistol,ItemGlobals.BLUNDERBUSS: Gun.Gun,ItemGlobals.MUSKET: Gun.Gun,ItemGlobals.BAYONET: Bayonet.Bayonet,ItemGlobals.DUAL_CUTLASS: DualCutlass.DualCutlass,ItemGlobals.EPEE: Foil.Foil,ItemGlobals.RAPIER: Foil.Foil,ItemGlobals.QUEST_PROP_TORCH: Torch.Torch,ItemGlobals.QUEST_PROP_POWDER_KEG: PowderKeg.PowderKeg}
__weaponClass2Key = {Sword.Sword: 1,Gun.Gun: 2,Doll.Doll: 3,Dagger.Dagger: 4,Grenade.Grenade: 5,Wand.Wand: 6}

def getWeaponName(weaponId):
    return PLocalizer.InventoryTypeNames.get(weaponId, 'Unknown')


def getDCFieldName(weaponId):
    return __dcFieldNames[weaponId]


def getWeaponClass(weaponId):
    typeId = ItemGlobals.getType(weaponId)
    subtypeId = ItemGlobals.getSubtype(weaponId)
    weaponClass = __subtypeId2Class.get(subtypeId)
    if not weaponClass:
        weaponClass = __typeId2Class.get(typeId)
    if not weaponClass:
        weaponClass = __weaponId2Class.get(weaponId)
    return weaponClass


def getWeaponKey(weaponId):
    return __weaponClass2Key.get(__weaponId2Class.get(weaponId))


WEAPON_MOVIE_CLEAR = 0
WEAPON_MOVIE_START = 1
WEAPON_MOVIE_STOP = 2
WEAPON_MOVIE_DEFEAT = 3
LocalAvatarUsingSkill = 'localAvatarUsingSkill'
LocalAvatarUseProjectileSkill = 'localAvatarUseProjectileSkill'
LocalAvatarUseTargetedSkill = 'localAvatarUseTargetedSkill'
LocalAvatarUseShipSkill = 'localAvatarUseShipSkill'
LocalAvatarUseItem = 'localAvatarUseItem'
LocalAvatarSwitchingWeapons = 'localAvatarSwitchingWeapons'
__weaponStatList = {InventoryType.MeleeWeaponL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.MeleeWeaponL2: ([0, 0, 0, 0, 0], [-2, 0, 0, 0, 0]),InventoryType.MeleeWeaponL3: ([0, 0, 0, 0, 0], [-4, 0, 0, 0, 0]),InventoryType.MeleeWeaponL4: ([0, 0, 0, 0, 0], [-6, 0, 0, 0, 0]),InventoryType.MeleeWeaponL5: ([0, 0, 0, 0, 0], [-8, 0, 0, 0, 0]),InventoryType.MeleeWeaponL6: ([0, 0, 0, 0, 0], [-10, 0, 0, 0, 0]),InventoryType.CutlassWeaponL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.CutlassWeaponL2: ([0, 0, 0, 0, 0], [-2, 0, 0, 0, 0]),InventoryType.CutlassWeaponL3: ([0, 0, 0, 0, 0], [-4, 0, 0, 0, 0]),InventoryType.CutlassWeaponL4: ([0, 0, 0, 0, 0], [-6, 0, 0, 0, 0]),InventoryType.CutlassWeaponL5: ([0, 0, 0, 0, 0], [-8, 0, 0, 0, 0]),InventoryType.CutlassWeaponL6: ([0, 0, 0, 0, 0], [-10, 0, 0, 0, 0]),InventoryType.PistolWeaponL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.PistolWeaponL2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.PistolWeaponL3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.PistolWeaponL4: ([0, 0, 0, 0, 0], [-1, 0, 0, 0, 0]),InventoryType.PistolWeaponL5: ([0, 0, 0, 0, 0], [-2, 0, 0, 0, 0]),InventoryType.PistolWeaponL6: ([0, 0, 0, 0, 0], [-3, 0, 0, 0, 0]),InventoryType.MusketWeaponL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.MusketWeaponL2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.MusketWeaponL3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.BayonetWeaponL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.BayonetWeaponL2: ([0, 0, 0, 0, 0], [-2, 0, 0, 0, 0]),InventoryType.BayonetWeaponL3: ([0, 0, 0, 0, 0], [-4, 0, 0, 0, 0]),InventoryType.DaggerWeaponL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.DaggerWeaponL2: ([0, 0, 0, 0, 0], [-2, 0, 0, 0, 0]),InventoryType.DaggerWeaponL3: ([0, 0, 0, 0, 0], [-4, 0, 0, 0, 0]),InventoryType.DaggerWeaponL4: ([0, 0, 0, 0, 0], [-6, 0, 0, 0, 0]),InventoryType.DaggerWeaponL5: ([0, 0, 0, 0, 0], [-8, 0, 0, 0, 0]),InventoryType.DaggerWeaponL6: ([0, 0, 0, 0, 0], [-10, 0, 0, 0, 0]),InventoryType.GrenadeWeaponL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.GrenadeWeaponL2: ([0, 0, 0, 0, 0], [-2, 0, 0, 0, 0]),InventoryType.GrenadeWeaponL3: ([0, 0, 0, 0, 0], [-4, 0, 0, 0, 0]),InventoryType.GrenadeWeaponL4: ([0, 0, 0, 0, 0], [-6, 0, 0, 0, 0]),InventoryType.GrenadeWeaponL5: ([0, 0, 0, 0, 0], [-8, 0, 0, 0, 0]),InventoryType.GrenadeWeaponL6: ([0, 0, 0, 0, 0], [-10, 0, 0, 0, 0]),InventoryType.WandWeaponL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.WandWeaponL2: ([0, 0, 0, 0, 0], [-2, 0, 0, 0, 0]),InventoryType.WandWeaponL3: ([0, 0, 0, 0, 0], [-4, 0, 0, 0, 0]),InventoryType.WandWeaponL4: ([0, 0, 0, 0, 0], [-6, 0, 0, 0, 0]),InventoryType.WandWeaponL5: ([0, 0, 0, 0, 0], [-8, 0, 0, 0, 0]),InventoryType.WandWeaponL6: ([0, 0, 0, 0, 0], [-10, 0, 0, 0, 0]),InventoryType.DollWeaponL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.DollWeaponL2: ([0, 0, 0, 0, 0], [-2, 0, 0, 0, 0]),InventoryType.DollWeaponL3: ([0, 0, 0, 0, 0], [-4, 0, 0, 0, 0]),InventoryType.DollWeaponL4: ([0, 0, 0, 0, 0], [-6, 0, 0, 0, 0]),InventoryType.DollWeaponL5: ([0, 0, 0, 0, 0], [-8, 0, 0, 0, 0]),InventoryType.DollWeaponL6: ([0, 0, 0, 0, 0], [-10, 0, 0, 0, 0]),InventoryType.KettleWeaponL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.KettleWeaponL2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.KettleWeaponL3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.DualCutlassL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.FoilL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.Potion1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.Potion2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.Potion3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.Potion4: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.Potion5: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.CannonDamageLvl1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.CannonDamageLvl2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.CannonDamageLvl3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.PistolDamageLvl1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.PistolDamageLvl2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.PistolDamageLvl3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.CutlassDamageLvl1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.CutlassDamageLvl2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.CutlassDamageLvl3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.DollDamageLvl1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.DollDamageLvl2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.DollDamageLvl3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.HastenLvl1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.HastenLvl2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.HastenLvl3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.RepBonusLvl1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.RepBonusLvl2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.RepBonusLvl3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.RepBonusLvlComp: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.GoldBonusLvl1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.GoldBonusLvl2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.InvisibilityLvl1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.InvisibilityLvl2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.RegenLvl1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.RegenLvl2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.RegenLvl3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.RegenLvl4: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.Burp: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.Fart: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.FartLvl2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.Vomit: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.HeadGrow: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.FaceColor: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.SizeReduce: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.SizeIncrease: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.HeadFire: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.ScorpionTransform: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.AlligatorTransform: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.CrabTransform: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.AccuracyBonusLvl1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.AccuracyBonusLvl2: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.AccuracyBonusLvl3: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.RemoveGroggy: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.ShipRepairKit: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.PorkChunk: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.MonsterWeaponL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.MonsterWeaponL2: ([0, 0, 0, 0, 0], [-2, 0, 0, 0, 0]),InventoryType.MonsterWeaponL3: ([0, 0, 0, 0, 0], [-4, 0, 0, 0, 0]),InventoryType.MonsterWeaponL4: ([0, 0, 0, 0, 0], [-6, 0, 0, 0, 0]),InventoryType.MonsterWeaponL5: ([0, 0, 0, 0, 0], [-8, 0, 0, 0, 0]),InventoryType.CannonL1: ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]),InventoryType.CannonL2: ([0, 0, 0, 0, 0], [-5, 0, 0, 0, 0]),InventoryType.CannonL3: ([0, 0, 0, 0, 0], [-10, 0, 0, 0, 0])}

def getWeaponStats(attacker, itemId):
    if itemId <= ItemGlobals.WEAPON_RANGE:
        return ([0, 0, 0, 0, 0], [ItemGlobals.getWeaponAttributes(itemId, ItemGlobals.POWERFUL) * -1, 0, 0, 0, 0])
    entry = __weaponStatList.get(itemId)
    if entry:
        return entry
    else:
        return (None, None)
    return None


cutlassScalePVP = 1.6
pistolScalePVP = 0.8
dollScalePVP = 1.25
daggerScalePVP = 1.6
grenadeScalePVP = 0.8
wandScalePVP = 1.6
__weaponDamageScaleList = {InventoryType.MeleeWeaponL1: (1.0, 1.0, 2.0),InventoryType.MeleeWeaponL2: (1.0, 1.0, 2.0),InventoryType.MeleeWeaponL3: (1.0, 1.0, 2.0),InventoryType.MeleeWeaponL4: (1.0, 1.0, 2.0),InventoryType.MeleeWeaponL5: (1.0, 1.0, 2.0),InventoryType.MeleeWeaponL6: (1.0, 1.0, 2.0),InventoryType.CutlassWeaponL1: (1.0, 1.0, cutlassScalePVP),InventoryType.CutlassWeaponL2: (1.0, 1.0, cutlassScalePVP),InventoryType.CutlassWeaponL3: (1.0, 1.0, cutlassScalePVP),InventoryType.CutlassWeaponL4: (1.0, 1.0, cutlassScalePVP),InventoryType.CutlassWeaponL5: (1.0, 1.0, cutlassScalePVP),InventoryType.CutlassWeaponL6: (1.0, 1.0, cutlassScalePVP),ItemGlobals.SWORD: (1.0, 1.0, cutlassScalePVP),ItemGlobals.DOLL: (1.0, 1.0, dollScalePVP),ItemGlobals.DAGGER: (1.0, 1.0, daggerScalePVP),ItemGlobals.GRENADE: (1.0, 1.0, grenadeScalePVP),ItemGlobals.STAFF: (1.0, 1.0, wandScalePVP),InventoryType.PistolWeaponL1: (1.0, 1.0, pistolScalePVP),InventoryType.PistolWeaponL2: (0.8, 0.7566, pistolScalePVP),InventoryType.PistolWeaponL3: (0.7, 0.64, pistolScalePVP),InventoryType.PistolWeaponL4: (0.7, 0.64, pistolScalePVP),InventoryType.PistolWeaponL5: (0.7, 0.64, pistolScalePVP),InventoryType.PistolWeaponL6: (0.7, 0.64, pistolScalePVP),InventoryType.MusketWeaponL1: (1.0, 1.0, 1.2),InventoryType.MusketWeaponL2: (1.0, 1.0, 1.2),InventoryType.MusketWeaponL3: (1.0, 1.0, 1.2),InventoryType.BayonetWeaponL1: (1.0, 1.0, 1.4),InventoryType.BayonetWeaponL2: (1.0, 1.0, 1.4),InventoryType.BayonetWeaponL3: (1.0, 1.0, 1.4),InventoryType.DaggerWeaponL1: (1.0, 1.0, daggerScalePVP),InventoryType.DaggerWeaponL2: (1.0, 1.0, daggerScalePVP),InventoryType.DaggerWeaponL3: (1.0, 1.0, daggerScalePVP),InventoryType.DaggerWeaponL4: (1.0, 1.0, daggerScalePVP),InventoryType.DaggerWeaponL5: (1.0, 1.0, daggerScalePVP),InventoryType.DaggerWeaponL6: (1.0, 1.0, daggerScalePVP),InventoryType.GrenadeWeaponL1: (1.0, 1.0, grenadeScalePVP),InventoryType.GrenadeWeaponL2: (1.0, 1.0, grenadeScalePVP),InventoryType.GrenadeWeaponL3: (1.0, 1.0, grenadeScalePVP),InventoryType.GrenadeWeaponL4: (1.0, 1.0, grenadeScalePVP),InventoryType.GrenadeWeaponL5: (1.0, 1.0, grenadeScalePVP),InventoryType.GrenadeWeaponL6: (1.0, 1.0, grenadeScalePVP),InventoryType.WandWeaponL1: (1.0, 1.0, wandScalePVP),InventoryType.WandWeaponL2: (1.0, 1.0, wandScalePVP),InventoryType.WandWeaponL3: (1.0, 1.0, wandScalePVP),InventoryType.WandWeaponL4: (1.0, 1.0, wandScalePVP),InventoryType.WandWeaponL5: (1.0, 1.0, wandScalePVP),InventoryType.WandWeaponL6: (1.0, 1.0, wandScalePVP),InventoryType.DollWeaponL1: (1.0, 1.0, dollScalePVP),InventoryType.DollWeaponL2: (1.0, 1.0, dollScalePVP),InventoryType.DollWeaponL3: (1.0, 1.0, dollScalePVP),InventoryType.DollWeaponL4: (1.0, 1.0, dollScalePVP),InventoryType.DollWeaponL5: (1.0, 1.0, dollScalePVP),InventoryType.DollWeaponL6: (1.0, 1.0, dollScalePVP),InventoryType.DualCutlassL1: (1.0, 1.0, 1.0),InventoryType.FoilL1: (1.0, 1.0, 1.0),InventoryType.CannonL1: (1.0, 1.0, 1.0),InventoryType.CannonL2: (1.0, 1.0, 1.0),InventoryType.CannonL3: (1.0, 1.0, 1.0)}
__ammoNPCDamageScaleList = {InventoryType.PistolLeadShot: 1.0,InventoryType.PistolVenomShot: 1.0,InventoryType.PistolBaneShot: 1.0,InventoryType.PistolHexEaterShot: 1.0,InventoryType.PistolSilverShot: 1.0,InventoryType.PistolSteelShot: 1.0,InventoryType.GrenadeExplosion: 1.0,InventoryType.GrenadeShockBomb: 1.0,InventoryType.GrenadeFireBomb: 1.0,InventoryType.GrenadeSmokeCloud: 1.0,InventoryType.GrenadeSiege: 1.0,InventoryType.CannonRoundShot: 1.0,InventoryType.CannonChainShot: 1.0,InventoryType.CannonGrapeShot: 1.0,InventoryType.CannonFirebrand: 0.6,InventoryType.CannonThunderbolt: 0.4,InventoryType.CannonExplosive: 0.25,InventoryType.CannonFury: 0.5,InventoryType.CannonGrappleHook: 1.0,InventoryType.DaggerAsp: 1.0,InventoryType.DaggerAdder: 1.0,InventoryType.DaggerSidewinder: 1.0,InventoryType.DaggerViperNest: 1.0,InventoryType.MusketCrackShot: 1.0,InventoryType.MusketMarksman: 1.0,InventoryType.MusketLeadShot: 1.0,InventoryType.MusketScatterShot: 1.0,InventoryType.MusketCursedShot: 1.0,InventoryType.MusketCoalfireShot: 1.0,InventoryType.MusketHeavySlug: 1.0,InventoryType.MusketExploderShot: 1.0}

def getWeaponDamageScale(itemId):
    type = ItemGlobals.getType(itemId)
    entry = __weaponDamageScaleList.get(type)
    if not entry:
        entry = __weaponDamageScaleList.get(itemId)
    if entry:
        return entry[0]
    else:
        return 1.0


def getAmmoNPCDamageScale(ammoId):
    entry = __ammoNPCDamageScaleList.get(ammoId)
    if entry:
        return entry
    else:
        return 1.0


def getWeaponExperienceScale(itemId):
    type = ItemGlobals.getType(itemId)
    entry = __weaponDamageScaleList.get(type)
    if not entry:
        entry = __weaponDamageScaleList.get(itemId)
    if entry:
        return entry[1]
    else:
        return 1.0


def getWeaponPvpDamageScale(itemId):
    type = ItemGlobals.getType(itemId)
    entry = __weaponDamageScaleList.get(type)
    if not entry:
        entry = __weaponDamageScaleList.get(itemId)
    if entry:
        return entry[2]
    else:
        return 1.0


__invId2RepId = {InventoryType.MeleeWeaponL1: InventoryType.MeleeRep,InventoryType.MeleeWeaponL2: InventoryType.MeleeRep,InventoryType.MeleeWeaponL3: InventoryType.MeleeRep,InventoryType.MeleeWeaponL4: InventoryType.MeleeRep,InventoryType.MeleeWeaponL5: InventoryType.MeleeRep,InventoryType.MeleeWeaponL6: InventoryType.MeleeRep,InventoryType.CutlassWeaponL1: InventoryType.CutlassRep,InventoryType.CutlassWeaponL2: InventoryType.CutlassRep,InventoryType.CutlassWeaponL3: InventoryType.CutlassRep,InventoryType.CutlassWeaponL4: InventoryType.CutlassRep,InventoryType.CutlassWeaponL5: InventoryType.CutlassRep,InventoryType.CutlassWeaponL6: InventoryType.CutlassRep,InventoryType.DualCutlassL1: InventoryType.CutlassRep,InventoryType.FoilL1: InventoryType.CutlassRep,InventoryType.PistolWeaponL1: InventoryType.PistolRep,InventoryType.PistolWeaponL2: InventoryType.PistolRep,InventoryType.PistolWeaponL3: InventoryType.PistolRep,InventoryType.PistolWeaponL4: InventoryType.PistolRep,InventoryType.PistolWeaponL5: InventoryType.PistolRep,InventoryType.PistolWeaponL6: InventoryType.PistolRep,InventoryType.MusketWeaponL1: InventoryType.PistolRep,InventoryType.MusketWeaponL2: InventoryType.PistolRep,InventoryType.MusketWeaponL3: InventoryType.PistolRep,InventoryType.BayonetWeaponL1: InventoryType.PistolRep,InventoryType.BayonetWeaponL2: InventoryType.PistolRep,InventoryType.BayonetWeaponL3: InventoryType.PistolRep,InventoryType.DaggerWeaponL1: InventoryType.DaggerRep,InventoryType.DaggerWeaponL2: InventoryType.DaggerRep,InventoryType.DaggerWeaponL3: InventoryType.DaggerRep,InventoryType.DaggerWeaponL4: InventoryType.DaggerRep,InventoryType.DaggerWeaponL5: InventoryType.DaggerRep,InventoryType.DaggerWeaponL6: InventoryType.DaggerRep,InventoryType.GrenadeWeaponL1: InventoryType.GrenadeRep,InventoryType.GrenadeWeaponL2: InventoryType.GrenadeRep,InventoryType.GrenadeWeaponL3: InventoryType.GrenadeRep,InventoryType.GrenadeWeaponL4: InventoryType.GrenadeRep,InventoryType.GrenadeWeaponL5: InventoryType.GrenadeRep,InventoryType.GrenadeWeaponL6: InventoryType.GrenadeRep,InventoryType.WandWeaponL1: InventoryType.WandRep,InventoryType.WandWeaponL2: InventoryType.WandRep,InventoryType.WandWeaponL3: InventoryType.WandRep,InventoryType.WandWeaponL4: InventoryType.WandRep,InventoryType.WandWeaponL5: InventoryType.WandRep,InventoryType.WandWeaponL6: InventoryType.WandRep,InventoryType.DollWeaponL1: InventoryType.DollRep,InventoryType.DollWeaponL2: InventoryType.DollRep,InventoryType.DollWeaponL3: InventoryType.DollRep,InventoryType.DollWeaponL4: InventoryType.DollRep,InventoryType.DollWeaponL5: InventoryType.DollRep,InventoryType.DollWeaponL6: InventoryType.DollRep,InventoryType.KettleWeaponL1: InventoryType.KettleRep,InventoryType.KettleWeaponL2: InventoryType.KettleRep,InventoryType.KettleWeaponL3: InventoryType.KettleRep,InventoryType.MonsterWeaponL1: InventoryType.MonsterRep,InventoryType.MonsterWeaponL2: InventoryType.MonsterRep,InventoryType.MonsterWeaponL3: InventoryType.MonsterRep,InventoryType.MonsterWeaponL4: InventoryType.MonsterRep,InventoryType.MonsterWeaponL5: InventoryType.MonsterRep,InventoryType.PistolPouchL1: InventoryType.PistolRep,InventoryType.PistolPouchL2: InventoryType.PistolRep,InventoryType.PistolPouchL3: InventoryType.PistolRep,InventoryType.DaggerPouchL1: InventoryType.DaggerRep,InventoryType.DaggerPouchL2: InventoryType.DaggerRep,InventoryType.DaggerPouchL3: InventoryType.DaggerRep,InventoryType.GrenadePouchL1: InventoryType.GrenadeRep,InventoryType.GrenadePouchL2: InventoryType.GrenadeRep,InventoryType.GrenadePouchL3: InventoryType.GrenadeRep,InventoryType.CannonPouchL1: InventoryType.CannonRep,InventoryType.CannonPouchL2: InventoryType.CannonRep,InventoryType.CannonPouchL3: InventoryType.CannonRep,InventoryType.RegularLure: InventoryType.FishingRep,InventoryType.LegendaryLure: InventoryType.FishingRep}
__typeId2RepId = {ItemGlobals.SWORD: InventoryType.CutlassRep,ItemGlobals.GUN: InventoryType.PistolRep,ItemGlobals.DOLL: InventoryType.DollRep,ItemGlobals.DAGGER: InventoryType.DaggerRep,ItemGlobals.GRENADE: InventoryType.GrenadeRep,ItemGlobals.STAFF: InventoryType.WandRep,ItemGlobals.AXE: InventoryType.CutlassRep,ItemGlobals.FENCING: InventoryType.CutlassRep,ItemGlobals.CANNON: InventoryType.CannonRep,ItemGlobals.SAILING: InventoryType.SailingRep,ItemGlobals.MONSTER: InventoryType.MonsterRep,ItemGlobals.FISHING: InventoryType.FishingRep,ItemGlobals.QUEST_PROP: InventoryType.MeleeRep}

def getRepId(inventoryId):
    if inventoryId <= ItemGlobals.CHARM_RANGE and inventoryId not in range(InventoryType.begin_FishingLures, InventoryType.end_FishingLures):
        typeId = ItemGlobals.getType(inventoryId)
        return __typeId2RepId.get(typeId, 0)
    else:
        return __invId2RepId.get(inventoryId, 0)


PERFECT_ACC = 100.0
HIGH_ACC = 80.0
MED_ACC = 60.0
LOW_ACC = 40.0
INSTANT_RECHARGE = 0.0
XFAST_RECHARGE = 1.0
FAST_RECHARGE = 2.0
MED_RECHARGE = 5.0
SLOW_RECHARGE = 10.0
XSLOW_RECHARGE = 20.0
CLOSE_RANGE = 10.0
SHORT_RANGE = 30.0
MED_RANGE = 60.0
LONG_RANGE = 100.0
FAR_RANGE = 150.0
DISTANT_RANGE = 200.0
INF_RANGE = NA
Ranges = (
 CLOSE_RANGE, SHORT_RANGE, MED_RANGE, LONG_RANGE, FAR_RANGE, DISTANT_RANGE)
MaxAimDistance = DISTANT_RANGE
AI_RANGE_TOLERANCE = 5.0
AI_AOE_RANGE_TOLERANCE = 10.0
AI_ENEMY_TOLERANCE = 0.0
NO_DELAY = 0.0
SHORT_DELAY = 2.5
MED_DELAY = 5.0
LONG_DELAY = 10.0
PERM_DUR = -1
INSTANT_DUR = 0.0
VERYSHORT_DUR = 8.0
SHORT_DUR = 15.0
MED_DUR = 30.0
MED2_DUR = 45.0
LONG_DUR = 60.0
NO_RECUR = 0.0
FAST_RECUR = 3.0
MED_RECUR = 5.0
SLOW_RECUR = 15.0
HIGH_QUANT = 100
MED_QUANT = 50
LOW_QUANT = 10
INF_QUANT = -1
STAFF_QUANT = -2
NO_AREA = 0
SMALL_AREA = 10.0
MED_AREA = 25.0
LARGE_AREA = 50.0
MAX_AREA_TARGETS = 10
BOSS_AREA_TARGETS = 50
SWIFT_NORM = 0
SWIFT_INC = 1
SWIFT_DEC = -1
SWIFT_MOD = [
 -1.0, -0.5, 0.0, 0.5]
SWIFT_NORM_INDEX = 2
SWIFT_MIN_INDEX = 0
SWIFT_MAX_INDEX = 3
COMBO_SKILL_INDEX = 1
RADIAL_SKILL_INDEX = 2
PASSIVE_SKILL_INDEX = 3
TONIC_SKILL_INDEX = 4
BREAK_ATTACK_SKILL_INDEX = 5
DEFENSE_SKILL_INDEX = 6
BACKSTAB_BONUS = 1.3
BACKSTAB_ANGLE = 60
CHARGEABLE_WEAPONS = [
 InventoryType.PistolRep, InventoryType.GrenadeRep, InventoryType.WandRep]
__skills = {}
for skillId, skillData in __skillInfo.items():
    repCat = skillData[REPUTATION_CATEGORY_INDEX]
    __skills.setdefault(repCat, []).append(skillId)

def getAllSkillIds():
    return __skillInfo.keys()


def getSkills(weaponRepId):
    return __skills.get(weaponRepId, [])


def getPlayerSkills(weaponRepId):
    skills = __skills.get(weaponRepId, [])
    skillSet = []
    for skillId in skills:
        if skillId >= 10000:
            skillSet.append(skillId)

    return skillSet


def getSkillName(skillId):
    return PLocalizer.InventoryTypeNames.get(skillId, 'Unknown')


def getSkillReputationCategoryId(skillId):
    cat = __skillInfo.get(skillId)
    if cat:
        return cat[REPUTATION_CATEGORY_INDEX]
    else:
        return 0


def canFreeUse(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[FREE_INDEX]
    return 0


def canPVPUse(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[PVP_INDEX]
    return 0


def isProjectileSkill(skillId, ammoSkillId):
    value = 0
    if skillId:
        value += __skillInfo[skillId][IS_PROJECTILE_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][IS_PROJECTILE_INDEX]
    if skillId and ammoSkillId:
        if value == 2:
            return 1
        else:
            return 0
    else:
        return value


def isFirearm(weaponId):
    return ItemGlobals.getType(weaponId) == ItemGlobals.GUN


def isBayonet(weaponId):
    return ItemGlobals.getSubtype(weaponId) == ItemGlobals.BAYONET


def isBladedWeapon(weaponId):
    return ItemGlobals.getType(weaponId) in [ItemGlobals.CUTLASS, ItemGlobals.DAGGER, ItemGlobals.AXE, ItemGlobals.FENCING]


def isFriendlyFireWeapon(weaponId):
    return ItemGlobals.getType(weaponId) == ItemGlobals.DOLL


def isVoodooWeapon(weaponId):
    return ItemGlobals.getType(weaponId) in [ItemGlobals.DOLL, ItemGlobals.STAFF]


def getLinkedSkillId(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[LINKED_SKILL]
    return None


def getSkillInterrupt(skillId):
    if skillId:
        value = __skillInfo[skillId][INTERRUPT_INDEX]
        return value
    return 0


def getSkillUnattune(skillId):
    if skillId:
        value = __skillInfo[skillId][UNATTUNE_INDEX]
        return value
    return 0


def isHealingSkill(skillId):
    return skillId in (InventoryType.DollHeal, InventoryType.DollCure, EnemySkills.DOLL_SPIRIT_MEND)


def isFriendlyFire(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][FRIENDLY_FIRE_INDEX]
    if ammoSkillId:
        value |= __skillInfo[ammoSkillId][FRIENDLY_FIRE_INDEX]
    return value


def getSkillAmmoInventoryId(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[AMMO_INVENTORY_TYPE]
    return None


def getAllAmmoSkills():
    skillIds = []
    for skillId in __skillInfo.keys():
        if getSkillAmmoInventoryId(skillId):
            skillIds.append(skillId)

    return skillIds


def getSkillIdForAmmoSkillId(ammoSkillId):
    skillIds = getAllAmmoSkills()
    for skillId in skillIds:
        if ammoSkillId == getSkillAmmoInventoryId(skillId):
            return skillId

    return None


def getSkillMaxQuantity(skillId):
    return __skillInfo[skillId][MAX_QUANTITY_INDEX]


def isInfiniteAmmo(skillId):
    quant = __skillInfo[skillId][MAX_QUANTITY_INDEX]
    return quant == INF_QUANT or quant == STAFF_QUANT


def getAttackMaxCharge(skillId, ammoSkillId=0):
    value = 0
    if skillId:
        value += __skillInfo[skillId][MAX_CHARGE_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][MAX_CHARGE_INDEX]
    return value


def getSkillType(skillId):
    return __skillInfo[skillId][SKILL_TYPE]


def getSkillTrack(skillId):
    track = __skillInfo[skillId][SKILL_TRACK_INDEX]
    if track:
        return track
    else:
        return -1


def getSkillIcon(skillId):
    if not __skillInfo.has_key(skillId):
        return 'base'
    icon = __skillInfo[skillId][SKILL_ICON_INDEX]
    if icon:
        return str(icon)
    else:
        return 'base'


def getMojoCost(skillId):
    mojoCost = __skillInfo[skillId][SELF_MOJO_INDEX]
    if mojoCost:
        return mojoCost
    else:
        return 0


def getHitEffect(skillId):
    skill = __skillInfo[skillId]
    if skill:
        return skill[HIT_VFX]
    return 0


def getCenterEffect(skillId, ammoSkillId=0):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[CENTER_VFX]
    ammoSkill = __skillInfo.get(ammoSkillId)
    if ammoSkill:
        return ammoSkill[CENTER_VFX]


def getUsableInAir(skillId, ammoSkillId=0):
    val = 0
    skill = __skillInfo.get(skillId)
    if skill:
        val += skill[USABLE_IN_AIR]
    ammoSkill = __skillInfo.get(ammoSkillId)
    if ammoSkill:
        val += ammoSkill[USABLE_IN_AIR]
    return val


def getNPCModifier(skillId):
    damageMult = 1.0
    skill = __skillInfo[skillId]
    if skill:
        damageMult = skill[NPC_MODIFIER]
    return damageMult


def isValidSkill(skillId, weaponId, repId):
    skillInfo = __skillInfo.get(skillId)
    if skillInfo:
        if skillInfo[REPUTATION_CATEGORY_INDEX] == repId:
            return 1
    return 0


def isValidAttack(skillId, ammoSkillId, weaponId, repId):
    skillRep = getSkillReputationCategoryId(skillId)
    if not skillRep:
        return 1
    valid = skillRep == repId or skillRep == InventoryType.SailingRep
    if ammoSkillId:
        valid = valid and getSkillReputationCategoryId(ammoSkillId) == repId
    return valid


def getAttackReputation(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][REPUTATION_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][REPUTATION_INDEX]
    return value


def getAttackEffects(skillId, ammoSkillId=None):
    data = __attackEffectsSkillInfo.get((skillId, ammoSkillId))
    if data:
        return data
    skill = __skillInfo.get(skillId)
    if skill:
        selfHP = skill[SELF_HP_INDEX]
        targetHP = skill[TARGET_HP_INDEX]
        selfPower = 0
        targetPower = 0
        selfLuck = 0
        targetEffect = skill[EFFECT_FLAG_INDEX]
        selfMojo = skill[SELF_MOJO_INDEX]
        targetMojo = skill[TARGET_MOJO_INDEX]
        selfSwiftness = 0
        targetSwiftness = 0
        if ammoSkillId:
            skill = __skillInfo.get(ammoSkillId)
            if skill:
                selfHP += skill[SELF_HP_INDEX]
                targetHP += skill[TARGET_HP_INDEX]
                selfPower += 0
                targetPower += 0
                selfLuck += 0
                targetEffect = skill[EFFECT_FLAG_INDEX]
                selfMojo += skill[SELF_MOJO_INDEX]
                targetMojo += skill[TARGET_MOJO_INDEX]
                selfSwiftness = 0
                targetSwiftness += 0
        finalData = (
         [
          selfHP, selfPower, selfLuck, selfMojo, selfSwiftness], [targetHP, targetPower, targetEffect, targetMojo, targetSwiftness])
        __attackEffectsSkillInfo[skillId, ammoSkillId] = finalData
        return finalData
    return None


def getAttackTargetHP(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][TARGET_HP_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][TARGET_HP_INDEX]
    return value


def getAttackSelfHP(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][SELF_HP_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][SELF_HP_INDEX]
    return value


def getAttackTargetMojo(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][TARGET_MOJO_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][TARGET_MOJO_INDEX]
    return value


def getAttackSelfMojo(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][SELF_MOJO_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][SELF_MOJO_INDEX]
    if config.GetBool('mana-free-skills', 0):
        if value < 0:
            value = 0
    return value


def getAttackHullHP(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][HULL_HP_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][HULL_HP_INDEX]
    return value


def getAttackSailHP(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][SAIL_HP_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][SAIL_HP_INDEX]
    return value


def getAttackAccuracy(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][ACCURACY_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][ACCURACY_INDEX]
        value /= 2
    value = max(0, min(100, value))
    return value


def getAttackUpgrade(skillId):
    value = __skillInfo[skillId][UPGRADE_INDEX]
    return value


def getAttackRechargeTime(skillId, ammoSkillId=None):
    value = 0.0
    if skillId:
        value += __skillInfo[skillId][RECHARGE_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][RECHARGE_INDEX]
    return value


def getAttackRange(skillId, ammoSkillId=None):
    range = 0.0
    skillValue = __skillInfo[skillId][RANGE_INDEX]
    if ammoSkillId:
        ammoValue = __skillInfo[ammoSkillId][RANGE_INDEX]
        if skillValue == INF_RANGE:
            if ammoValue == INF_RANGE:
                range = INF_RANGE
                return range
            else:
                range = ammoValue
        elif ammoValue == INF_RANGE:
            range = skillValue
        else:
            range = max(skillValue, ammoValue)
    elif skillValue == INF_RANGE:
        return range
    else:
        range = skillValue
    return range


def getAttackDelay(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][DELAY_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][DELAY_INDEX]
    return value


def getAttackDuration(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][DURATION_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][DURATION_INDEX]
    return value


def getAttackRecur(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][RECUR_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][RECUR_INDEX]
    return value


def getAttackAreaRadius(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][AREA_EFFECT_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][AREA_EFFECT_INDEX]
    value = max(0, value)
    return value


def isAttackAreaSelfDamaging(skillId, ammoSkillId=None):
    value = 0
    if skillId:
        value |= __skillInfo[skillId][AREA_EFFECT_SELF_DAMAGE_INDEX]
    if ammoSkillId:
        value |= __skillInfo[ammoSkillId][AREA_EFFECT_SELF_DAMAGE_INDEX]
    return value


def isSelfUseSkill(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SELF_USE_INDEX]
    return 0


def getAttackVolley(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][VOLLEY_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][VOLLEY_INDEX]
    return float(value)


def getAttackProjectilePower(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][PROJECTILE_POWER_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][PROJECTILE_POWER_INDEX]
    return value


def getAttackReactionDelay(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][REACTION_DELAY_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][REACTION_DELAY_INDEX]
    return value


def getNumHits(skillId, ammoSkillId=None):
    value = __skillInfo[skillId][NUM_HIT_INDEX]
    if ammoSkillId:
        value += __skillInfo[ammoSkillId][NUM_HIT_INDEX]
    return value


def getIsInstantSkill(skillId, ammoSkillId=None):
    skillValue = __skillInfo[skillId][INSTANT_INDEX]
    ammoValue = 1
    if ammoSkillId:
        ammoValue = __skillInfo[ammoSkillId][INSTANT_INDEX]
    if skillValue and ammoValue:
        return 1
    else:
        return 0


def getIsHostileBuff(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[HOSTILE_BUFF]
    return 0


def getNeedTarget(skillId, ammoSkillId=None):
    skill = __skillInfo.get(skillId)
    if skill:
        skillNeedsTarget = skill[NEED_TARGET_INDEX]
        if ammoSkillId:
            ammoSkill = __skillInfo.get(ammoSkillId)
            ammoNeedsTarget = ammoSkill[NEED_TARGET_INDEX]
            return skillNeedsTarget or ammoNeedsTarget
        else:
            return skillNeedsTarget
    return 0


def getSplitTarget(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SPLIT_TARGET_INDEX]
    return 0


def getNeedSight(skillId, ammoSkillId=None):
    skill = __skillInfo.get(skillId)
    if skill:
        skillNeedsSight = skill[NEED_SIGHT]
        if ammoSkillId:
            ammoSkill = __skillInfo.get(ammoSkillId)
            ammoNeedsSight = ammoSkill[NEED_SIGHT]
            return skillNeedsSight or ammoNeedsSight
        else:
            return skillNeedsSight
    return 0


def getShipAcceleration(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_ACCEL_INDEX]
    return 0


def getShipMaxSpeed(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_MAXSPEED_INDEX]
    return 0


def getShipRevAcceleration(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_REVACCEL_INDEX]
    return 0


def getShipRevMaxSpeed(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_REVMAXSPEED_INDEX]
    return 0


def getShipTurnRate(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_TURNRATE_INDEX]
    return 0


def getShipMaxTurn(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHIP_MAXTURN_INDEX]
    return 0


def getIsShout(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[SHOUT_INDEX]
    return 0


def getShipEffects(skillId, ammoSkillId=0):
    skill = __skillInfo.get(skillId)
    if ammoSkillId:
        skill = __skillInfo.get(ammoSkillId)
    if skill:
        return [skill[SHIP_ACCEL_INDEX], skill[SHIP_MAXSPEED_INDEX], skill[SHIP_REVACCEL_INDEX], skill[SHIP_REVMAXSPEED_INDEX], skill[SHIP_TURNRATE_INDEX], skill[SHIP_MAXTURN_INDEX]]
    return [0, 0, 0, 0, 0, 0]


def getIsShipSkill(skillId):
    return getSkillReputationCategoryId(skillId) == InventoryType.SailingRep


def getIsCannonSkill(skillId):
    return getSkillReputationCategoryId(skillId) == InventoryType.CannonRep


def getIsDollAttackSkill(skillId):
    return getSkillReputationCategoryId(skillId) == InventoryType.DollRep and skillId != InventoryType.DollAttune and skillId != EnemySkills.DOLL_UNATTUNE and skillId != EnemySkills.DOLL_EVIL_EYE and skillId != EnemySkills.MISC_CLEANSE


def getIsStaffAttackSkill(skillId):
    return getSkillReputationCategoryId(skillId) == InventoryType.WandRep


def getIsStaffChargeSkill(skillId):
    return skillId >= EnemySkills.STAFF_FIZZLE and skillId <= EnemySkills.STAFF_DESOLATION_CHARGE


def getIsGrappleSkill(skillId, ammoSkillId):
    if ammoSkillId == InventoryType.CannonGrappleHook:
        return 1
    else:
        return 0


def getAnimTime(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[ANIM_TIME_INDEX]
    return 0


def getIsAreaAnimSkill(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[NEED_AREA_ANIM_INDEX]
    return 0


EFFECT_FLAME = 2

def getSkillEffectFlag(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[EFFECT_FLAG_INDEX]
    return 0


def getAttackClass(skillId):
    skill = __skillInfo.get(skillId)
    if skill:
        return skill[ATTACK_CLASS_INDEX]
    return 0


def getAttackAreaShape(skillId, ammoSkillId):
    if ammoSkillId:
        ammoShape = __skillInfo[ammoSkillId][AREA_SHAPE_INDEX]
        if ammoShape:
            return ammoShape
    skillShape = __skillInfo[skillId][AREA_SHAPE_INDEX]
    if skillShape:
        return skillShape
    return AREA_OFF


PLAYABLE_INDEX = 0
HIT_SFX_INDEX = 1
MISS_SFX_INDEX = 2
OUCH_SFX_INDEX = 3
MISTIMEDHIT_SFX_INDEX = 4
ANIM_TYPE = 0
FUNC_TYPE = 1
INTERVAL_TYPE = 2
NONE_TYPE = 3
__skillAnim = {InventoryType.FishingRodStall: ('getStall', Sword.getHitSfx, Sword.getMissSfx),InventoryType.FishingRodPull: ('getPull', Sword.getHitSfx, Sword.getMissSfx),InventoryType.FishingRodHeal: ('getHeal', Sword.getHitSfx, Sword.getMissSfx),InventoryType.FishingRodTug: ('getTug', Sword.getHitSfx, Sword.getMissSfx),InventoryType.FishingRodSink: ('getSink', Sword.getHitSfx, Sword.getMissSfx),InventoryType.FishingRodOceanEye: ('getOceanEye', Sword.getHitSfx, Sword.getMissSfx),InventoryType.MeleePunch: ('getBoxingPunch', Melee.getHitSfx, Melee.getMissSfx, 0, Melee.getMistimedHitSfx),InventoryType.MeleeJab: ('getBoxingPunch', Melee.getHitSfx, Melee.getMissSfx, 0, Melee.getMistimedHitSfx),InventoryType.MeleeKick: ('getKick', Melee.getHitSfx, Melee.getMissSfx, 0, Melee.getMistimedHitSfx),InventoryType.MeleeRoundhouse: ('getKick', Melee.getHitSfx, Melee.getMissSfx, 0, Melee.getMistimedHitSfx),InventoryType.MeleeHeadbutt: ('getKrazyPunch', Melee.getHitSfx, Melee.getMissSfx, 0, Melee.getMistimedHitSfx),InventoryType.MeleeHaymaker: ('getBoxingPunch', Melee.getHitSfx, Melee.getMissSfx, 0, Melee.getMistimedHitSfx),InventoryType.MeleeThrowDirt: ('getKrazyPunch', Melee.getHitSfx, Melee.getMissSfx, 0, Melee.getMistimedHitSfx),InventoryType.CutlassHack: ('getHack', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),InventoryType.CutlassSlash: ('getSlash', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),InventoryType.CutlassStab: ('getThrust', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),InventoryType.CutlassFlourish: ('getFlourish', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),InventoryType.CutlassCleave: ('getCleave', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),InventoryType.CutlassTaunt: ('getTaunt', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),InventoryType.CutlassBrawl: ('getBrawl', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),InventoryType.CutlassSweep: ('getSweep', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),InventoryType.CutlassBladestorm: ('getBladestorm', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_MIGHTYSLASH: ('getWildSlash', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_SKEWER: ('getStab', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_OVERHEAD: ('getWildSlash', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_ROLLTHRUST: ('getRollThrust', Sword.getHitSfx, Sword.getMissSfx, 0, 0),EnemySkills.CUTLASS_CURSED_FIRE: ('getHack', Sword.getFireHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_CURSED_ICE: ('getHack', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_CURSED_THUNDER: ('getHack', Sword.getThunderHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_BLOWBACK: ('getBlowbackSweep', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_CAPTAINS_FURY: ('getFurySweep', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_MASTERS_RIPOSTE: ('getCure', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_POWER_ATTACK: ('getChop', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_FIRE_BREAK: ('getFireSweep', Sword.getFireHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_ICE_BREAK: ('getIceSweep', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.CUTLASS_THUNDER_BREAK: ('getThunderSweep', Sword.getThunderHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.BROADSWORD_HACK: ('getBroadswordHack', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.BROADSWORD_SLASH: ('getBroadswordSlash', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.BROADSWORD_STAB: ('getBroadswordThrust', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.BROADSWORD_FLOURISH: ('getBroadswordFlourish', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.BROADSWORD_CLEAVE: ('getBroadswordCleave', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.SABRE_HACK: ('getSabreHack', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.SABRE_SLASH: ('getSabreSlash', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.SABRE_STAB: ('getSabreThrust', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.SABRE_FLOURISH: ('getSabreFlourish', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.SABRE_CLEAVE: ('getSabreCleave', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),InventoryType.PistolShoot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),InventoryType.PistolTakeAim: ('getPistolTakeAimAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),EnemySkills.PISTOL_CHARGE: ('getPistolChargingAnim', Pistol.getAimSfx, Pistol.getAimSfx, 0, Pistol.getMistimedHitSfx),EnemySkills.PISTOL_RELOAD: ('getPistolReloadAnim', None, None, 0, None),InventoryType.PistolLeadShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),InventoryType.PistolBaneShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),InventoryType.PistolSilverShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),InventoryType.PistolHexEaterShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),InventoryType.PistolSteelShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),InventoryType.PistolVenomShot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),EnemySkills.PISTOL_SCATTERSHOT: ('getPistolScattershotAnim', Gun.getShootSfx, Gun.getShootSfx, 0, Gun.getMistimedHitSfx),EnemySkills.PISTOL_SCATTERSHOT_AIM: ('getPistolTakeAimAnim', Gun.getShootSfx, Gun.getShootSfx, 0, Gun.getMistimedHitSfx),EnemySkills.PISTOL_DEADEYE: ('getPistolFireAnim', Gun.getShootSfx, Gun.getShootSfx, 0, Gun.getMistimedHitSfx),EnemySkills.PISTOL_RAPIDFIRE: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),EnemySkills.PISTOL_QUICKLOAD: ('getPistolReloadAnim', None, None, 0, None),EnemySkills.PISTOL_STUNSHOT: ('getPistolScattershotAnim', Gun.getShootSfx, Gun.getShootSfx, 0, Gun.getMistimedHitSfx),EnemySkills.PISTOL_BREAKSHOT: ('getPistolScattershotAnim', Gun.getShootSfx, Gun.getShootSfx, 0, Gun.getMistimedHitSfx),EnemySkills.PISTOL_POINT_BLANK: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),EnemySkills.PISTOL_HOTSHOT: ('getPistolFireAnim', Doll.getScorchSfx, Doll.getScorchSfx, 0, Doll.getScorchSfx),InventoryType.MusketShoot: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),InventoryType.MusketTakeAim: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),InventoryType.MusketDeadeye: ('getPistolFireAnim', Pistol.getHitSfx, Pistol.getMissSfx, 0, Pistol.getMistimedHitSfx),InventoryType.BayonetShoot: ('getBayonetFireAnim', Bayonet.getShootSfx, Bayonet.getShootSfx, 0, Bayonet.getMistimedHitSfx),InventoryType.BayonetStab: ('getBayonetStab', Bayonet.getHitSfx, Bayonet.getMissSfx, 0, Bayonet.getMistimedHitSfx),InventoryType.BayonetRush: ('getBayonetRush', Bayonet.getHitSfx, Bayonet.getMissSfx, 0, Bayonet.getMistimedHitSfx),InventoryType.BayonetBash: ('getBayonetBash', Bayonet.getHitSfx, Bayonet.getMissSfx, 0, Bayonet.getMistimedHitSfx),EnemySkills.BAYONET_SHOOT: ('getBayonetFireAnim', Bayonet.getShootSfx, Bayonet.getShootSfx, 0, Bayonet.getMistimedHitSfx),EnemySkills.BAYONET_STAB: ('getBayonetStab', Bayonet.getHitSfx, Bayonet.getMissSfx, 0, Bayonet.getMistimedHitSfx),EnemySkills.BAYONET_RUSH: ('getBayonetRush', Bayonet.getHitSfx, Bayonet.getMissSfx, 0, Bayonet.getMistimedHitSfx),EnemySkills.BAYONET_BASH: ('getBayonetBash', Bayonet.getHitSfx, Bayonet.getMissSfx, 0, Bayonet.getMistimedHitSfx),EnemySkills.BAYONET_PLAYER_STAB: ('getPlayerBayonetStab', Bayonet.getHitSfx, Bayonet.getMissSfx, 0, Bayonet.getMistimedHitSfx),EnemySkills.BAYONET_PLAYER_RUSH: ('getPlayerBayonetRush', Bayonet.getHitSfx, Bayonet.getMissSfx, 0, Bayonet.getMistimedHitSfx),EnemySkills.BAYONET_PLAYER_BASH: ('getBayonetBash', Bayonet.getHitSfx, Bayonet.getMissSfx, 0, Bayonet.getMistimedHitSfx),EnemySkills.BAYONET_DISABLE: ('getBayonetBash', Bayonet.getHitSfx, Bayonet.getMissSfx, 0, Bayonet.getMistimedHitSfx),InventoryType.DaggerCut: ('getCut', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),InventoryType.DaggerSwipe: ('getSwipe', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),InventoryType.DaggerGouge: ('getGouge', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),InventoryType.DaggerEviscerate: ('getEviscerate', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),InventoryType.DaggerAsp: ('getDaggerAspInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),InventoryType.DaggerAdder: ('getDaggerAdderInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),InventoryType.DaggerThrowDirt: ('getDaggerThrowDirtInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),InventoryType.DaggerSidewinder: ('getDaggerSidewinderInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),InventoryType.DaggerViperNest: ('getDaggerViperNestInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_THROW_KNIFE: ('getDaggerAspInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_THROW_VENOMBLADE: ('getDaggerAdderInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_THROW_BARBED: ('getDaggerSidewinderInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_THROW_INTERRUPT: ('getDaggerAspInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_BACKSTAB: ('getBackstab', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_COUP: ('getCoup', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_DAGGERRAIN: ('getDaggerRainInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_THROW_COMBO_1: ('getDaggerThrowCombo1Interval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_THROW_COMBO_2: ('getDaggerThrowCombo2Interval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_THROW_COMBO_3: ('getDaggerThrowCombo3Interval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_THROW_COMBO_4: ('getDaggerThrowCombo4Interval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_BARRAGE: ('getDaggerBarrageInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_ICEBARRAGE: ('getDaggerBarrageInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_VENOMSTAB: ('getSlash', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),EnemySkills.DAGGER_ACIDDAGGER: ('getDaggerAcidDaggerInterval', Dagger.getHitSfx, Dagger.getMissSfx, 0, Dagger.getMistimedHitSfx),InventoryType.GrenadeThrow: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx, 0, Grenade.getMistimedHitSfx),InventoryType.GrenadeLongVolley: ('getGrenadeLongVolley', Grenade.getHitSfx, Grenade.getMissSfx, 0, Grenade.getMistimedHitSfx),EnemySkills.GRENADE_CHARGE: ('getGrenadeChargingAnim', Grenade.getAimSfx, Grenade.getAimSfx, 0, Grenade.getMistimedHitSfx),EnemySkills.GRENADE_RELOAD: ('getGrenadeReloadAnim', Grenade.getReloadSfx, Grenade.getReloadSfx, 0, Grenade.getMistimedHitSfx),InventoryType.GrenadeExplosion: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx, 0, Grenade.getMistimedHitSfx),InventoryType.GrenadeShockBomb: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx, 0, Grenade.getMistimedHitSfx),InventoryType.GrenadeFireBomb: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx, 0, Grenade.getMistimedHitSfx),InventoryType.GrenadeSmokeCloud: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx, 0, Grenade.getMistimedHitSfx),InventoryType.GrenadeSiege: ('getGrenadeThrow', Grenade.getHitSfx, Grenade.getMissSfx, 0, Grenade.getMistimedHitSfx),InventoryType.DollAttune: ('getAttune', Doll.getAttuneSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.DOLL_UNATTUNE: ('getUnattune', Doll.getUnattuneSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.DOLL_POKE2: ('getPoke', Doll.getPokeSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),InventoryType.DollPoke: ('getPoke', Doll.getPokeSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),InventoryType.DollSwarm: ('getSwarm', Doll.getSwarmSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),InventoryType.DollHeal: ('getHeal', Doll.getHealSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),InventoryType.DollBurn: ('getBurn', Doll.getScorchSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),InventoryType.DollShackles: ('getShackles', Doll.getShacklesSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),InventoryType.DollCure: ('getCure', Doll.getCureSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),InventoryType.DollCurse: ('getCurse', Doll.getCurseSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),InventoryType.DollLifeDrain: ('getLifeDrain', Doll.getLifedrainSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.DOLL_SPIRIT_MEND: ('getHeal', Doll.getHealSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.DOLL_WIND_GUARD: ('getHeal', Doll.getHealSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.DOLL_RED_FURY: ('getHeal', Doll.getHealSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.DOLL_SPIRIT_GUARD: ('getHeal', Doll.getHealSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.DOLL_HEX_GUARD: ('getHeal', Doll.getHealSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.DOLL_REGENERATION: ('getHeal', Doll.getHealSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.DOLL_EVIL_EYE: ('getEvilEye', Doll.getEvileyeSfx, Doll.getEvileyeSfx, 0, Doll.getEvileyeSfx),EnemySkills.STAFF_WITHER_CHARGE: ('getChargeWitherAnim', Wand.getWitherChargeSfx, Wand.getWitherHoldSfx, 0, None),EnemySkills.STAFF_SOULFLAY_CHARGE: ('getChargeSoulflayAnim', Wand.getSoulflayChargeSfx, Wand.getSoulflayHoldSfx, 0, None),EnemySkills.STAFF_PESTILENCE_CHARGE: ('getChargePestilenceAnim', Wand.getPestilenceChargeSfx, Wand.getPestilenceHoldSfx, 0, None),EnemySkills.STAFF_HELLFIRE_CHARGE: ('getChargeHellfireAnim', Wand.getHellfireChargeSfx, Wand.getHellfireHoldSfx, 0, None),EnemySkills.STAFF_BANISH_CHARGE: ('getChargeBanishAnim', Wand.getBanishChargeSfx, Wand.getBanishHoldSfx, 0, None),EnemySkills.STAFF_DESOLATION_CHARGE: ('getChargeDesolationAnim', Wand.getDesolationChargeSfx, Wand.getDesolationHoldSfx, 0, None),EnemySkills.STAFF_FIZZLE: ('getFizzleAnim', Wand.getChargeSfx, Wand.getChargeLoopSfx, 0, None),InventoryType.StaffBlast: ('getCastFireAnim', Wand.getBlastFireSfx, Wand.getBlastFireSfx, Wand.getBlastHitSfx, 0, None),InventoryType.StaffSoulFlay: ('getCastSoulFlayAnim', Wand.getSoulflayFireSfx, Wand.getSoulflayFireSfx, Wand.getSoulflayHitSfx, 0, None),InventoryType.StaffPestilence: ('getCastPestilenceAnim', Wand.getPestilenceFireSfx, Wand.getPestilenceFireSfx, Wand.getPestilenceHitSfx, 0, None),InventoryType.StaffWither: ('getCastWitherAnim', Wand.getWitherFireSfx, Wand.getWitherFireSfx, Wand.getWitherHitSfx, 0, None),InventoryType.StaffHellfire: ('getCastHellfireAnim', Wand.getHellfireFireSfx, Wand.getHellfireFireSfx, Wand.getHellfireHitSfx, 0, None),InventoryType.StaffBanish: ('getCastBanishAnim', Wand.getBanishFireSfx, Wand.getBanishFireSfx, Wand.getBanishHitSfx, 0, None),InventoryType.StaffDesolation: ('getCastDesolationAnim', Wand.getDesolationFireSfx, Wand.getDesolationFireSfx, Wand.getDesolationHitSfx, 0, None),EnemySkills.STAFF_TOGGLE_AURA_WARDING: ('getToggleAuraOnAnim', Wand.getAuraCastSfx, Wand.getAuraLoopSfx, 0, None),EnemySkills.STAFF_TOGGLE_AURA_NATURE: ('getToggleAuraOnAnim', Wand.getAuraCastSfx, Wand.getAuraLoopSfx, 0, None),EnemySkills.STAFF_TOGGLE_AURA_DARK: ('getToggleAuraOnAnim', Wand.getAuraCastSfx, Wand.getAuraLoopSfx, 0, None),EnemySkills.STAFF_TOGGLE_AURA_OFF: ('getToggleAuraOffAnim', Wand.getAuraOffSfx, Wand.getAuraLoopSfx, 0, None),InventoryType.UseItem: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.UsePotion: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.Potion1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.Potion2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.Potion3: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.Potion4: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.Potion5: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.CannonDamageLvl1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.CannonDamageLvl2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.CannonDamageLvl3: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.PistolDamageLvl1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.PistolDamageLvl2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.PistolDamageLvl3: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.CutlassDamageLvl1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.CutlassDamageLvl2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.CutlassDamageLvl3: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.DollDamageLvl1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.DollDamageLvl2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.DollDamageLvl3: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.HastenLvl1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.HastenLvl2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.HastenLvl3: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.RepBonusLvl1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.RepBonusLvl2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.RepBonusLvl3: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.RepBonusLvlComp: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.GoldBonusLvl1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.GoldBonusLvl2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.InvisibilityLvl1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.InvisibilityLvl2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.RegenLvl1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.RegenLvl2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.RegenLvl3: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.RegenLvl4: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.Burp: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.Fart: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.FartLvl2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.Vomit: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.HeadGrow: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.FaceColor: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.SizeReduce: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.SizeIncrease: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.HeadFire: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.ScorpionTransform: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.AlligatorTransform: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.CrabTransform: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.AccuracyBonusLvl1: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.AccuracyBonusLvl2: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.AccuracyBonusLvl3: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.RemoveGroggy: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.RemoveGroggy: ('getDrink', Consumable.getDrinkSfx, Consumable.getMissSfx, 0, None),InventoryType.ShipRepairKit: ('getShipRepair', Consumable.getShipRepairSfx, Consumable.getMissSfx, 0, None),InventoryType.PorkChunk: ('getDrink', Consumable.getEatSfx, Consumable.getMissSfx, 0, None),InventoryType.SailBroadsideLeft: ('getBroadsideLeft', None, None, 0, None),InventoryType.SailBroadsideRight: ('getBroadsideRight', None, None, 0, None),InventoryType.SailFullSail: ('getFullSail', None, None, 0, None),InventoryType.SailComeAbout: ('getComeAbout', None, None, 0, None),InventoryType.SailOpenFire: ('getOpenFire', None, None, 0, None),InventoryType.SailRammingSpeed: ('getRammingSpeed', None, None, 0, None),InventoryType.SailTakeCover: ('getTakeCover', None, None, 0, None),InventoryType.SailPowerRecharge: ('getPowerRecharge', None, None, 0, None),EnemySkills.SAIL_WRECK_HULL: ('getWreckHull', None, None, 0, None),EnemySkills.SAIL_WRECK_MASTS: ('getWreckMasts', None, None, 0, None),EnemySkills.SAIL_SINK_HER: ('getSinkHer', None, None, 0, None),EnemySkills.SAIL_INCOMING: ('getIncoming', None, None, 0, None),EnemySkills.SAIL_FIX_IT_NOW: ('getFixItNow', None, None, 0, None),EnemySkills.CLAW_RAKE: ('getCrabAttackRight', MonsterMelee.getCrabAttackLeftSfx, MonsterMelee.getCrabAttackLeftSfx, 0, 0),EnemySkills.CLAW_STRIKE: ('getCrabAttackLeft', MonsterMelee.getCrabAttackLeftSfx, MonsterMelee.getCrabAttackLeftSfx, 0, 0),EnemySkills.DUAL_CLAW: ('getCrabAttackBoth', MonsterMelee.getCrabAttackBothSfx, MonsterMelee.getCrabAttackBothSfx, 0, 0),EnemySkills.STUMP_KICK: ('getStumpKick', MonsterMelee.getMossmanAttackKickSfx, MonsterMelee.getMossmanAttackKickSfx, 0, 0),EnemySkills.STUMP_KICK_RIGHT: ('getStumpKickRight', MonsterMelee.getMossmanAttackKickSfx, MonsterMelee.getMossmanAttackKickSfx, 0, 0),EnemySkills.STUMP_SLAP_LEFT: ('getStumpSlapLeft', MonsterMelee.getMossmanAttackSlapSfx, MonsterMelee.getMossmanAttackSlapSfx, 0, 0),EnemySkills.STUMP_SLAP_RIGHT: ('getStumpSlapRight', MonsterMelee.getMossmanAttackSlapSfx, MonsterMelee.getMossmanAttackSlapSfx, 0, 0),EnemySkills.STUMP_SWAT_LEFT: ('getStumpSwatLeft', MonsterMelee.getMossmanAttackSwatSfx, MonsterMelee.getMossmanAttackSwatSfx, 0, 0),EnemySkills.STUMP_SWAT_RIGHT: ('getStumpSwatRight', MonsterMelee.getMossmanAttackSwatSfx, MonsterMelee.getMossmanAttackSwatSfx, 0, 0),EnemySkills.STUMP_STOMP: ('getStumpStomp', MonsterMelee.getMossmanAttackJumpSfx, MonsterMelee.getMossmanAttackJumpSfx, 0, 0),EnemySkills.FLYTRAP_ATTACK_A: ('getFlyTrapAttackA', MonsterMelee.getFlytrapAttackASfx, MonsterMelee.getFlytrapAttackASfx, 0, 0),EnemySkills.FLYTRAP_ATTACK_JAB: ('getFlyTrapAttackJab', MonsterMelee.getFlytrapAttackJabSfx, MonsterMelee.getFlytrapAttackJabSfx, 0, 0),EnemySkills.FLYTRAP_LEFT_FAKE: ('getFlyTrapLeftFake', MonsterMelee.getFlytrapAttackFakeSfx, MonsterMelee.getFlytrapAttackFakeSfx, 0, 0),EnemySkills.FLYTRAP_RIGHT_FAKE: ('getFlyTrapRightFake', MonsterMelee.getFlytrapAttackFakeSfx, MonsterMelee.getFlytrapAttackFakeSfx, 0, 0),EnemySkills.FLYTRAP_SPIT: ('getFlyTrapSpit', MonsterMelee.getFlytrapAttackSpitSfx, MonsterMelee.getFlytrapAttackSpitSfx, 0, 0),EnemySkills.FLYTRAP_WEAK_SPIT: ('getFlyTrapSpit', MonsterMelee.getFlytrapAttackSpitSfx, MonsterMelee.getFlytrapAttackSpitSfx, 0, 0),EnemySkills.POISON_VOMIT: ('getKrakenVomit', MonsterMelee.getEnsnareSfx, MonsterMelee.getMissSfx, 0, 0),EnemySkills.GROUND_SLAP: ('getTentacleSlap', MonsterMelee.getSmashSfx, MonsterMelee.getMissSfx, 0, 0),EnemySkills.ENSNARE: ('getTentacleEnsnare', MonsterMelee.getEnsnareSfx, MonsterMelee.getMissSfx, 0, 0),EnemySkills.CONSTRICT: ('getTentacleConstrict', MonsterMelee.getHitSfx, MonsterMelee.getMissSfx, 0, 0),EnemySkills.PILEDRIVER: ('getTentaclePiledriver', MonsterMelee.getSmashSfx, MonsterMelee.getMissSfx, 0, 0),EnemySkills.POUND: ('getTentaclePound', MonsterMelee.getHitSfx, MonsterMelee.getMissSfx, 0, 0),EnemySkills.SCORPION_ATTACK_LEFT: ('getScorpionAttackLeft', MonsterMelee.getScorpionAttackLeftSfx, MonsterMelee.getScorpionAttackLeftSfx, 0, 0),EnemySkills.SCORPION_ATTACK_RIGHT: ('getScorpionAttackRight', MonsterMelee.getScorpionAttackLeftSfx, MonsterMelee.getScorpionAttackLeftSfx, 0, 0),EnemySkills.SCORPION_ATTACK_BOTH: ('getScorpionAttackBoth', MonsterMelee.getScorpionAttackBothSfx, MonsterMelee.getScorpionAttackBothSfx, 0, 0),EnemySkills.SCORPION_ATTACK_TAIL_STING: ('getScorpionAttackTailSting', MonsterMelee.getScorpionAttackTailStingSfx, MonsterMelee.getScorpionAttackTailStingSfx, 0, 0),EnemySkills.SCORPION_PICK_UP_HUMAN: ('getScorpionPickUpHuman', MonsterMelee.getScorpionPickUpHumanSfx, MonsterMelee.getScorpionPickUpHumanSfx, 0, 0),EnemySkills.SCORPION_REAR_UP: ('getScorpionRearUp', MonsterMelee.getScorpionRearUpSfx, MonsterMelee.getScorpionRearUpSfx, 0, 0),EnemySkills.ALLIGATOR_ATTACK_LEFT: ('getAlligatorAttackLeft', MonsterMelee.getAlligatorAttackLeftSfx, MonsterMelee.getAlligatorAttackLeftSfx, 0, 0),EnemySkills.ALLIGATOR_ATTACK_RIGHT: ('getAlligatorAttackRight', MonsterMelee.getAlligatorAttackLeftSfx, MonsterMelee.getAlligatorAttackLeftSfx, 0, 0),EnemySkills.ALLIGATOR_ATTACK_STRAIGHT: ('getAlligatorAttackStraight', MonsterMelee.getAlligatorAttackStraightSfx, MonsterMelee.getAlligatorAttackStraightSfx, 0, 0),EnemySkills.ALLIGATOR_CRUSH: ('getAlligatorAttackStraight', MonsterMelee.getAlligatorAttackStraightSfx, MonsterMelee.getAlligatorAttackStraightSfx, 0, 0),EnemySkills.ALLIGATOR_MAIM: ('getAlligatorAttackRight', MonsterMelee.getAlligatorAttackLeftSfx, MonsterMelee.getAlligatorAttackLeftSfx, 0, 0),EnemySkills.BAT_ATTACK_LEFT: ('getBatAttackLeft', MonsterMelee.getBatAttackSfx, MonsterMelee.getBatAttackSfx, 0, 0),EnemySkills.BAT_ATTACK_RIGHT: ('getBatAttackRight', MonsterMelee.getBatAttackSfx, MonsterMelee.getBatAttackSfx, 0, 0),EnemySkills.BAT_SHRIEK: ('getBatShriek', MonsterMelee.getBatAttackSfx, MonsterMelee.getBatAttackSfx, 0, 0),EnemySkills.BAT_FLURRY: ('getBatFlurry', MonsterMelee.getBatAttackSfx, MonsterMelee.getBatAttackSfx, 0, 0),EnemySkills.WASP_ATTACK: ('getWaspAttack', MonsterMelee.getWaspStingSfx, MonsterMelee.getWaspStingSfx, 0, 0),EnemySkills.WASP_ATTACK_LEAP: ('getWaspAttackLeap', MonsterMelee.getWaspLeapStingSfx, MonsterMelee.getWaspLeapStingSfx, 0, 0),EnemySkills.WASP_POISON_STING: ('getWaspAttackSting', MonsterMelee.getWaspStingSfx, MonsterMelee.getWaspStingSfx, 0, 0),EnemySkills.WASP_PAIN_BITE: ('getWaspAttack', MonsterMelee.getWaspStingSfx, MonsterMelee.getWaspStingSfx, 0, 0),EnemySkills.SERPENT_VENOM: ('getWaspAttack', MonsterMelee.getWaspStingSfx, MonsterMelee.getWaspStingSfx, 0, 0),EnemySkills.CUTLASS_CHOP: ('getChop', Sword.getHitSfx, Sword.getMissSfx, 0, 0),EnemySkills.CUTLASS_DOUBLESLASH: ('getDoubleSlash', Sword.getHitSfx, Sword.getMissSfx, 0, 0),EnemySkills.CUTLASS_LUNGE: ('getLunge', Sword.getHitSfx, Sword.getMissSfx, 0, 0),EnemySkills.CUTLASS_STAB: ('getStab', Sword.getHitSfx, Sword.getMissSfx, 0, 0),EnemySkills.CUTLASS_COMBOA: ('getComboA', Sword.getHitSfx, Sword.getMissSfx, 0, 0),EnemySkills.CUTLASS_WILDSLASH: ('getWildSlash', Sword.getHitSfx, Sword.getMissSfx, 0, 0),EnemySkills.CUTLASS_FLURRY: ('getFlurry', Sword.getHitSfx, Sword.getMissSfx, 0, 0),EnemySkills.CUTLASS_RIPOSTE: ('getRiposte', Sword.getHitSfx, Sword.getMissSfx, 0, 0),EnemySkills.FOIL_FLECHE: ('getFoilFleche', Foil.getHitSfx, Foil.getMissSfx, 0, 0),EnemySkills.FOIL_REPRISE: ('getFoilReprise', Foil.getHitSfx, Foil.getMissSfx, 0, 0),EnemySkills.FOIL_SWIPE: ('getFoilSwipe', Foil.getHitSfx, Foil.getMissSfx, 0, 0),EnemySkills.FOIL_IMPALE: ('getFoilImpale', Foil.getHitSfx, Foil.getMissSfx, 0, 0),EnemySkills.FOIL_REMISE: ('getFoilRemise', Foil.getHitSfx, Foil.getMissSfx, 0, 0),EnemySkills.FOIL_BALESTRAKICK: ('getFoilBalestraKick', Foil.getHitSfx, Foil.getMissSfx, 0, 0),EnemySkills.FOIL_CADENCE: ('getFoilCadence', Foil.getHitSfx, Foil.getMissSfx, 0, 0),EnemySkills.DUALCUTLASS_COMBINATION: ('getDualCutlassCombination', DualCutlass.getHitSfx, DualCutlass.getMissSfx, 0, 0),EnemySkills.DUALCUTLASS_SPIN: ('getDualCutlassSpin', DualCutlass.getHitSfx, DualCutlass.getMissSfx, 0, 0),EnemySkills.DUALCUTLASS_BARRAGE: ('getDualCutlassBarrage', DualCutlass.getHitSfx, DualCutlass.getMissSfx, 0, 0),EnemySkills.DUALCUTLASS_XSLASH: ('getDualCutlassXSlash', DualCutlass.getHitSfx, DualCutlass.getMissSfx, 0, 0),EnemySkills.DUALCUTLASS_GORE: ('getDualCutlassGore', DualCutlass.getHitSfx, DualCutlass.getMissSfx, 0, 0),EnemySkills.AXE_CHOP: ('getChop', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.JR_DEATH_SLASH: ('getCleave', Sword.getHitSfx, Sword.getMissSfx, 0),EnemySkills.JR_VOODOO_SHOT: ('getCastFireAnim', Wand.getBlastFireSfx, Wand.getBlastFireSfx, Wand.getBlastHitSfx, 0),EnemySkills.JR_GRAVEBIND: ('getGraveBlindAnim', Wand.getWitherFireSfx, Wand.getWitherFireSfx, Wand.getWitherHitSfx, 0),EnemySkills.JR_SOUL_HARVEST: ('getSoulHarvestAnim', Wand.getDesolationFireSfx, Wand.getDesolationFireSfx, Wand.getDesolationHitSfx, 0),EnemySkills.JR_ANIMATE_DEAD: ('getGraveBindAnim', Wand.getWitherFireSfx, Wand.getWitherFireSfx, Wand.getWitherHitSfx, 0),EnemySkills.JR_PULVERIZER: ('getCastFireAnim', Wand.getBlastFireSfx, Wand.getBlastFireSfx, Wand.getBlastHitSfx, 0),EnemySkills.JR_CORRUPTION: ('getCorruptionAnim', Wand.getWitherFireSfx, Wand.getWitherFireSfx, Wand.getWitherHitSfx, 0),EnemySkills.JR_EXECUTE: ('getCleave', Sword.getHitSfx, Sword.getMissSfx, 0),EnemySkills.JR_THUNDER: ('getCastDarkThunderAnim', Wand.getBanishFireSfx, Wand.getBanishFireSfx, Wand.getBanishHitSfx, 0),EnemySkills.GHOST_PHANTOM_TOUCH: ('getCleave', Sword.getHitSfx, Sword.getMissSfx, 0),EnemySkills.GHOST_KILL_TOUCH: ('getCleave', Sword.getHitSfx, Sword.getMissSfx, 0),EnemySkills.GHOST_SUMMON_HELP: ('getSummonHelp', Doll.getCureSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.MISC_CLEANSE: ('getCure', Doll.getCleanseSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.MISC_DARK_CURSE: ('getCure', Doll.getCureSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.MISC_GHOST_FORM: ('getCure', Doll.getCureSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.MISC_FEINT: ('getCure', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx),EnemySkills.MISC_HEX_WARD: ('getHexWard', Doll.getHexWardSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.MISC_CAPTAINS_RESOLVE: ('getCaptainsResolve', None, None, 0, None),EnemySkills.MISC_NOT_IN_FACE: ('getCower', None, None, 0, None),EnemySkills.MISC_ACTIVATE_VOODOO_REFLECT: ('getCure', Doll.getAttuneSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.MISC_VOODOO_REFLECT: ('getReflect', None, None, 0, None),EnemySkills.MISC_MONKEY_PANIC: ('getMonkeyPanic', Doll.getMonkeyRageSfx, None, 0, None),EnemySkills.MISC_FIRST_AID: ('getCure', Doll.getCureSfx, Doll.getMissSfx, 0, Doll.getMistimedHitSfx),EnemySkills.GHOST_KILL_TOUCH: ('getChop', MonsterMelee.getRageGhostAttackSfx, MonsterMelee.getRageGhostAttackSfx, 0, 0),EnemySkills.TORCH_ATTACK: ('getHack', Sword.getHitSfx, Sword.getMissSfx, 0, Sword.getMistimedHitSfx)}

def getSkillAnimInfo(skillId):
    skillInfo = __skillAnim.get(skillId)
    return skillInfo


RESULT_MISS = 0
RESULT_HIT = 1
RESULT_DELAY = 2
RESULT_OUT_OF_RANGE = 3
RESULT_NOT_AVAILABLE = 4
RESULT_NOT_RECHARGED = 5
RESULT_AGAINST_PIRATE_CODE = 6
RESULT_PARRY = 7
RESULT_DODGE = 8
RESULT_RESIST = 9
RESULT_MISTIMED_MISS = 10
RESULT_MISTIMED_HIT = 11
RESULT_BLOCKED = 12
RESULT_REFLECTED = 13
RESULT_PROTECT = 14
MISTIME_PENALTY = 0.75

def getSkillResultName(result):
    return PLocalizer.SkillResultNames[result]


__multiHitAttacks = {InventoryType.DaggerSwipe: [0.1, 0.4],InventoryType.DaggerEviscerate: [0.15, 0.65, 1.15],InventoryType.DaggerViperNest: [1.0, 1.4, 1.7],InventoryType.CutlassBladestorm: [0.4, 0.7, 1.13, 1.41, 2.6],InventoryType.CutlassFlourish: [0.56, 0.93, 1.3],EnemySkills.BAYONET_RUSH: [0.15, 0.65, 1.15, 1.6],EnemySkills.BAYONET_PLAYER_RUSH: [0.15, 0.65, 1.15, 1.6],EnemySkills.CUTLASS_DOUBLESLASH: [0.3, 0.8],EnemySkills.CUTLASS_FLURRY: [0.15, 0.65, 1.15],EnemySkills.CUTLASS_COMBOA: [0.56, 0.93, 1.3],EnemySkills.CUTLASS_CAPTAINS_FURY: [0.4, 0.7, 1.13, 1.41],EnemySkills.DUAL_CLAW: [0.3, 0.5],EnemySkills.BAT_FLURRY: [0.4, 0.7, 1.13, 1.41],EnemySkills.FOIL_REPRISE: [0.3, 0.8],EnemySkills.FOIL_REMISE: [0.5, 0.9],EnemySkills.FOIL_CADENCE: [0.5, 0.9, 1.3, 1.8],EnemySkills.DUALCUTLASS_COMBINATION: [0.36, 0.8, 1.2, 1.3, 1.68, 2.1],EnemySkills.DUALCUTLASS_BARRAGE: [0.62, 0.9, 1.25, 1.5, 1.8],EnemySkills.DUALCUTLASS_SPIN: [0.29, 0.5, 0.75, 0.95],EnemySkills.DUALCUTLASS_XSLASH: [0.7, 1.7],EnemySkills.DUALCUTLASS_GORE: [0.4, 1.6],EnemySkills.PISTOL_RAPIDFIRE: [0.56, 0.93, 1.3],EnemySkills.DAGGER_COUP: [0.56, 0.93, 1.3],EnemySkills.DAGGER_DAGGERRAIN: [0.56, 0.93, 1.3],EnemySkills.SABRE_CLEAVE: [0.3, 0.6, 1.1],EnemySkills.SABRE_FLOURISH: [0.3, 0.6, 0.9]}

def getMultiHitAttacks(skillId):
    return __multiHitAttacks.get(skillId)


__projectileAttacks = {InventoryType.DaggerAsp: (80, 0.708, (150, 15)),InventoryType.DaggerAdder: (80, 0.708, (150, 15)),InventoryType.DaggerSidewinder: (80, 0.292, (150, 15)),InventoryType.StaffBlast: (80, 0.0, (70, 5)),InventoryType.StaffHellfire: (100, 0.0, (100, 5)),EnemySkills.FLYTRAP_SPIT: (100, 0.958, (70, 5)),EnemySkills.FLYTRAP_WEAK_SPIT: (100, 0.958, (70, 5)),EnemySkills.DAGGER_THROW_KNIFE: (80, 0.708, (150, 15)),EnemySkills.DAGGER_THROW_VENOMBLADE: (80, 0.708, (150, 15)),EnemySkills.DAGGER_THROW_BARBED: (80, 0.292, (150, 15)),EnemySkills.DAGGER_THROW_INTERRUPT: (80, 0.708, (150, 15)),EnemySkills.DAGGER_DAGGERRAIN: (80, 0.708, (150, 15)),EnemySkills.DAGGER_THROW_COMBO_1: (100, 0, (150, 15)),EnemySkills.DAGGER_THROW_COMBO_2: (100, 0, (150, 15)),EnemySkills.DAGGER_THROW_COMBO_3: (100, 0, (150, 15)),EnemySkills.DAGGER_THROW_COMBO_4: (100, 0, (150, 15)),EnemySkills.DAGGER_BARRAGE: (80, 0.708, (150, 15)),EnemySkills.DAGGER_ICEBARRAGE: (80, 0.708, (150, 15)),EnemySkills.DAGGER_ACIDDAGGER: (80, 0.292, (150, 15)),EnemySkills.JR_VOODOO_SHOT: (80, 0.708, (150, 15)),EnemySkills.JR_PULVERIZER: (80, 0.708, (150, 15))}

def getProjectileSpeed(skillId):
    entry = __projectileAttacks.get(skillId)
    if entry:
        return entry[0]
    return None


def getProjectileAnimT(skillId):
    entry = __projectileAttacks.get(skillId)
    if entry:
        return entry[1]
    return None


def getProjectileDefaultRange(skillId):
    entry = __projectileAttacks.get(skillId)
    if entry:
        return entry[2]
    return None


def getLevelDamageModifier(level):
    return level * 0.05 + 1.0


def getComparativeLevelDamageModifier(attacker, defender):
    attackerLevel = attacker.getLevel()
    defenderLevel = defender.getLevel()
    THRESHOLD = getBase().getRepository().gameStatManager.getDamageThreshold()
    if attackerLevel > defenderLevel:
        if not attacker.isNpc:
            mod = max(0, attackerLevel - defenderLevel - THRESHOLD) * 0.05 + 1.0
        else:
            mod = max(0, attackerLevel - defenderLevel - THRESHOLD) * 0.125 + 1.0
    else:
        if not attacker.isNpc:
            mod = min(0, attackerLevel - defenderLevel + THRESHOLD) * 0.1 + 1.0
        else:
            mod = min(0, attackerLevel - defenderLevel + THRESHOLD) * 0.03 + 1.0
        if not attacker.isNpc:
            mod = min(1.5, mod)
        mod = max(0.5, mod)
    return max(0.1, mod)


def getComparativeLevelAccuracyModifier(attacker, defender):
    attackerLevel = attacker.getLevel()
    defenderLevel = defender.getLevel()
    THRESHOLD = getBase().getRepository().gameStatManager.getAccuracyThreshold()
    mod = 0.0
    if not attacker.isNpc:
        if attackerLevel > defenderLevel:
            mod = min(100.0, max(0, attackerLevel - defenderLevel - THRESHOLD) * 6.0)
        else:
            mod = max(-50.0, min(0, attackerLevel - defenderLevel + THRESHOLD) * 6.0)
    return mod


def getComparativeShipLevelDamageModifier(attacker, defender):
    attackerLevel = attacker.getLevel()
    defenderLevel = defender.getLevel()
    THRESHOLD = 5.0
    if attackerLevel > defenderLevel:
        mod = 1.0
        if attacker.isNpc:
            mod = max(0, attackerLevel - defenderLevel - THRESHOLD) * 0.06 + 1.0
    elif attacker.isNpc:
        mod = min(0, attackerLevel - defenderLevel + THRESHOLD) * 0.06 + 1.0
    else:
        mod = min(0, attackerLevel - defenderLevel + THRESHOLD) * 0.02 + 1.0
    return max(0, mod)


MP_DAMAGE_DELAY = 0.25
COMBO_DAMAGE_DELAY = 0.5
__comboBonuses = {2: -1,3: -2,5: -4,7: -5,10: -7,15: -10,20: -12,25: -15,30: -17,50: -20,75: -25,100: -30}

def getComboBonus(val):
    return __comboBonuses.get(val, 0)


def skillTableSanityCheck():
    for skillId, skillInfo in __skillInfo.items():
        maxQuant = getSkillMaxQuantity(skillId)
        ammoInvId = getSkillAmmoInventoryId(skillId)
        if maxQuant != INF_QUANT and maxQuant != STAFF_QUANT:
            pass
        else:
            ammoInvId = getSkillAmmoInventoryId(skillId)

    return 1


__effectTable = {C_FLAMING: ((-30, 0, 0, 0, 0), 3),C_ON_FIRE: ((-24, 0, 0, 0, 0), 3),C_WOUND: ((-40, 0, 0, 0, 0), 3),C_ACID: ((-28, 0, 0, 0, 0), 3),C_POISON: ((-20, 0, 0, 0, 0), 3),C_TOXIN: ((-50, 0, 0, 0, 0), 3),C_CORRUPTION: ((-100, 0, 0, 0, 0), 3),C_REGEN: ((40, 0, 0, 0, 0), 3),C_STUN: ((0, 0, 0, 0, -1), 1),C_UNSTUN: ((0, 0, 0, 0, 0), 1),C_SLOW: ((0, 0, 0, 0, 0), 1),C_PAIN: ((0, 0, 0, 0, 0), 1),C_HOLD: ((0, 0, 0, 0, -1), 1),C_BLIND: ((0, 0, 0, 0, 0), 1),C_TAUNT: ((0, 0, 0, 0, 0), 1),C_MINE: ((0, 0, 0, 0, 0), 1),C_CURSE: ((0, 0, 0, 0, 0), 1),C_HASTEN: ((0, 0, 0, 0, 0), 1),C_WEAKEN: ((0, 0, 0, 0, 0), 1),C_FULLSAIL: ((0, 0, 0, 0, 0), 1),C_COMEABOUT: ((0, 0, 0, 0, 0), 1),C_OPENFIRE: ((0, 0, 0, 0, 0), 1),C_RAM: ((0, 0, 0, 0, 0), 1),C_TAKECOVER: ((0, 0, 0, 0, 0), 1),C_RECHARGE: ((0, 0, 0, 0, 0), 1),C_ATTUNE: ((0, 0, 0, 0, 0), 10),C_DIRT: ((0, 0, 0, 0, 0), 1),C_SPAWN: ((0, 0, 0, 0, 0), 1),C_SOULTAP: ((0, 0, 0, 0, 0), 1),C_LIFEDRAIN: ((0, 0, 0, 0, 0), 1),C_MANADRAIN: ((0, 0, 0, 0, 0), 1),C_BUFF_BREAK: ((0, 0, 0, 0, 0), 1),C_UNDEAD_KILLER: ((0, 0, 0, 0, 0), 1),C_MONSTER_KILLER: ((0, 0, 0, 0, 0), 1),C_SHIPHEAL: ((0, 0, 0, 0, 0), 1),C_VOODOO_STUN: ((0, 0, 0, 0, 0), 1),C_VOODOO_STUN_LOCK: ((0, 0, 0, 0, 0), 1),C_VOODOO_HEX_STUN: ((0, 0, 0, 0, 0), 1),C_INTERRUPTED: ((0, 0, 0, 0, 0), 1),C_REP_BONUS_LVL1: ((0, 0, 0, 0, 0), 1),C_REP_BONUS_LVL2: ((0, 0, 0, 0, 0), 1),C_REP_BONUS_LVL3: ((0, 0, 0, 0, 0), 1),C_GOLD_BONUS_LVL1: ((0, 0, 0, 0, 0), 1),C_GOLD_BONUS_LVL2: ((0, 0, 0, 0, 0), 1),C_CANNON_DAMAGE_LVL1: ((0, 0, 0, 0, 0), 1),C_CANNON_DAMAGE_LVL2: ((0, 0, 0, 0, 0), 1),C_CANNON_DAMAGE_LVL3: ((0, 0, 0, 0, 0), 1),C_PISTOL_DAMAGE_LVL1: ((0, 0, 0, 0, 0), 1),C_PISTOL_DAMAGE_LVL2: ((0, 0, 0, 0, 0), 1),C_PISTOL_DAMAGE_LVL3: ((0, 0, 0, 0, 0), 1),C_CUTLASS_DAMAGE_LVL1: ((0, 0, 0, 0, 0), 1),C_CUTLASS_DAMAGE_LVL2: ((0, 0, 0, 0, 0), 1),C_CUTLASS_DAMAGE_LVL3: ((0, 0, 0, 0, 0), 1),C_DOLL_DAMAGE_LVL1: ((0, 0, 0, 0, 0), 1),C_DOLL_DAMAGE_LVL2: ((0, 0, 0, 0, 0), 1),C_DOLL_DAMAGE_LVL3: ((0, 0, 0, 0, 0), 1),C_BURP: ((0, 0, 0, 0, 0), 1),C_FART: ((0, 0, 0, 0, 0), 1),C_FART_LVL2: ((0, 0, 0, 0, 0), 1),C_VOMIT: ((0, 0, 0, 0, 0), 1),C_HASTEN_LVL1: ((0, 0, 0, 0, 0), 1),C_HASTEN_LVL2: ((0, 0, 0, 0, 0), 1),C_HASTEN_LVL3: ((0, 0, 0, 0, 0), 1),C_ACCURACY_BONUS_LVL1: ((0, 0, 0, 0, 0), 1),C_ACCURACY_BONUS_LVL2: ((0, 0, 0, 0, 0), 1),C_ACCURACY_BONUS_LVL3: ((0, 0, 0, 0, 0), 1),C_REGEN_LVL1: ((0, 0, 0, 0, 0), 1),C_REGEN_LVL2: ((0, 0, 0, 0, 0), 1),C_REGEN_LVL3: ((0, 0, 0, 0, 0), 1),C_REGEN_LVL4: ((0, 0, 0, 0, 0), 1),C_HEAD_GROW: ((0, 0, 0, 0, 0), 1),C_CRAZY_SKIN_COLOR: ((0, 0, 0, 0, 0), 1),C_SIZE_REDUCE: ((0, 0, 0, 0, 0), 1),C_SIZE_INCREASE: ((0, 0, 0, 0, 0), 1),C_SCORPION_TRANSFORM: ((0, 0, 0, 0, 0), 1),C_ALLIGATOR_TRANSFORM: ((0, 0, 0, 0, 0), 1),C_CRAB_TRANSFORM: ((0, 0, 0, 0, 0), 1),C_HEAD_FIRE: ((0, 0, 0, 0, 0), 1),C_INVISIBILITY_LVL1: ((0, 0, 0, 0, 0), 1),C_INVISIBILITY_LVL2: ((0, 0, 0, 0, 0), 1),C_CANNON_DEFENSE_FIRE: ((-30, 0, 0, 0, 0), 3),C_CANNON_DEFENSE_SMOKE: ((0, 0, 0, 0, 0), 3),C_CANNON_DEFENSE_ICE: ((0, 0, 0, 0, 0), 3),C_WRECKHULL: ((0, 0, 0, 0, 0), 1),C_WRECKMASTS: ((0, 0, 0, 0, 0), 1),C_SINKHER: ((0, 0, 0, 0, 0), 1),C_INCOMING: ((0, 0, 0, 0, 0), 1),C_FIX_IT_NOW: ((0, 0, 0, 0, 0), 1),C_SPIRIT: ((0, 0, 0, 0, 0), 1),C_BANE: ((0, 0, 0, 0, 0), 1),C_MOJO: ((0, 0, 0, 0, 0), 1),C_WARDING: ((0, 0, 0, 0, 0), 1),C_NATURE: ((30, 0, 0, 0, 0), 1),C_DARK: ((0, 0, 0, 0, 0), 1),C_KNOCKDOWN: ((0, 0, 0, 0, 0), 1),C_QUICKLOAD: ((0, 0, 0, 0, 0), 1),C_DARK_CURSE: ((0, 0, 0, 0, 0), 1),C_GHOST_FORM: ((0, 0, 0, 0, 0), 1),C_MASTERS_RIPOSTE: ((0, 0, 0, 0, 0), 1),C_NOT_IN_FACE: ((0, 0, 0, 0, 0), 3),C_MONKEY_PANIC: ((0, 0, 0, 0, 0), 1),C_ON_CURSED_FIRE: ((-30, 0, 0, 0, 0), 3),C_FREEZE: ((0, 0, 0, 0, -1), 1),C_VOODOO_REFLECT: ((0, 0, 0, 0, 0), 1),C_FULLSPLIT: ((0, 0, 0, 0, 0), 1),C_FURY: ((0, 0, 0, 0, 0), 1),C_MELEE_SHIELD: ((0, 0, 0, 0, 0), 1),C_MISSILE_SHIELD: ((0, 0, 0, 0, 0), 1),C_MAGIC_SHIELD: ((0, 0, 0, 0, 0), 1),C_SUMMON_GHOST: ((0, 0, 0, 0, 0), 1),C_SUMMON_CHICKEN: ((0, 0, 0, 0, 0), 1),C_REP_BONUS_LVLCOMP: ((0, 0, 0, 0, 0), 1),C_SUMMON_MONKEY: ((0, 0, 0, 0, 0), 1),C_SUMMON_WASP: ((0, 0, 0, 0, 0), 1),C_SUMMON_DOG: ((0, 0, 0, 0, 0), 1)}

def getEffects(effectId):
    return __effectTable.get(effectId)[0]


def getBuffStackNumber(buffId):
    return __effectTable.get(buffId)[1]


WEAPON_POWER_MULT = 0.005
CURSED_DAM_AMP = 0.3
WEAKEN_PENALTY = 0.3
BANE_PENALTY = 0.2
MOJO_PENALTY = 0.3
WARDING_PENALTY = 0.1
DARK_BOOST = 0.1
BLIND_PERCENT = 0.75
TAUNT_PERCENT = 0.9
RESIST_DAMAGE_PENALTY = 0.1
CRIT_MULTIPLIER = 2.0
DARK_CURSE_PENALTY = 0.5
DARK_CURSE_BOOST = 0.2
GHOST_FORM_PENALTY = 0.5
GHOST_FORM_BOOST = 0.2
AURA_RADIUS = 15.0
NATURE_DELAY = 5.0
OPEN_FIRE_BONUS = 1.5
TAKE_COVER_BONUS = 0.25
TREASURE_SENSE_BONUS = 10
WRECK_HULL_BONUS = 1.5
WRECK_MASTS_BONUS = 1.5
SINK_HER_BONUS = 1.5
MASTERS_RIPOSTE_BONUS = 50.0
FIX_IT_NOW_BONUS = 2.0
SPIRIT_BONUS = 2.0
SABRE_PARRY_BONUS = 1.5
MONKEY_PANIC_HEALTH_BOOST = 0.4
MONKEY_PANIC_ATTACK_BOOST = 0.2
FURY_ATTACK_BOOST = 0.5
ANTI_VOODOO_ZOMBIE_BOOST = 0.5
INCOMING_DURATION = 6.0
INCOMING_DAMAGE_REDUCTION = 0.1
INCOMING_BROADSIDE_REUCTION = 0.1
CANNON_SHOOT_RATE_REDUCTION = 0.25
POWER_RECHARGE_RATE_REDUCTION = 0.75
NAVIGATION_RECHARGE_RATE_REDUCTION = 0.667
LOW_HEALTH_THRESHOLD = 0.25
HASTEN_BONUS = 0.5
AURA_MOJO_PENALTY = 0.5
DEADZONE_RANGE = 15
DAMAGE_MANA_BASE = 0.1
DAMAGE_MANA_MOD = 0.05
LEECH_HEALTH_BASE = 0.05
LEECH_HEALTH_MOD = 0.02
LEECH_VOODOO_BASE = 0.05
LEECH_VOODOO_MOD = 0.02
CRITICAL_BASE = 3
CRITICAL_MOD = 2
VENOM_LENGTH = 10.0
MAX_SPAWNED_GHOSTS = 3
__buffPriority = {C_RAM: (1, 3),C_FULLSAIL: (1, 1),C_COMEABOUT: (1, 1),C_TAKECOVER: (2, 1),C_OPENFIRE: (2, 1),C_WRECKHULL: (2, 1),C_WRECKMASTS: (2, 1),C_SINKHER: (2, 1),C_INCOMING: (2, 1),C_FIX_IT_NOW: (2, 1),C_UNSTUN: (3, 2),C_STUN: (3, 1),C_KNOCKDOWN: (3, 1),C_FREEZE: (3, 1),C_GHOST_FORM: (4, 1),C_DARK_CURSE: (4, 1),C_MONKEY_PANIC: (4, 1),C_MASTERS_RIPOSTE: (4, 1)}

def getBuffCategory(buffId):
    val = __buffPriority.get(buffId)
    if val:
        return val[0]
    return 0


def getBuffPriority(buffId):
    val = __buffPriority.get(buffId)
    if val:
        return val[1]
    return 0


__weaponVolley = {InventoryType.PistolWeaponL1: 1,InventoryType.PistolWeaponL2: 2,InventoryType.PistolWeaponL3: 1,InventoryType.PistolWeaponL4: 1,InventoryType.PistolWeaponL5: 3,InventoryType.PistolWeaponL6: 4,InventoryType.MusketWeaponL1: 1,InventoryType.MusketWeaponL2: 2,InventoryType.MusketWeaponL3: 3,InventoryType.BayonetWeaponL1: 1,InventoryType.BayonetWeaponL2: 2,InventoryType.BayonetWeaponL3: 3,InventoryType.GrenadeWeaponL1: 1,InventoryType.GrenadeWeaponL2: 1,InventoryType.GrenadeWeaponL3: 1}

def getWeaponVolley(weaponId):
    val = ItemGlobals.getBarrels(weaponId)
    if ItemGlobals.getType(weaponId) == ItemGlobals.GRENADE:
        val = 1
    if val:
        return val
    return 0


__staffChargeSkills = {InventoryType.StaffWither: EnemySkills.STAFF_WITHER_CHARGE,InventoryType.StaffSoulFlay: EnemySkills.STAFF_SOULFLAY_CHARGE,InventoryType.StaffPestilence: EnemySkills.STAFF_PESTILENCE_CHARGE,InventoryType.StaffHellfire: EnemySkills.STAFF_HELLFIRE_CHARGE,InventoryType.StaffBanish: EnemySkills.STAFF_BANISH_CHARGE,InventoryType.StaffDesolation: EnemySkills.STAFF_DESOLATION_CHARGE}

def getChargeSkill(skillId):
    return __staffChargeSkills.get(skillId)


def getAIProjectileAirTime(distance):
    return max(min(distance * 0.04, 2.6), 1.2)


BackstabSkills = (
 InventoryType.DaggerCut, InventoryType.DaggerSwipe, InventoryType.DaggerGouge, InventoryType.DaggerEviscerate, EnemySkills.DAGGER_BACKSTAB)
StartingSkills = [
 InventoryType.CutlassHack, InventoryType.CutlassSlash, InventoryType.SailBroadsideLeft, InventoryType.SailBroadsideRight, InventoryType.DaggerCut, InventoryType.DaggerSwipe, InventoryType.StaffBlast, InventoryType.StaffSoulFlay, InventoryType.GrenadeThrow, InventoryType.GrenadeExplosion, InventoryType.PistolShoot, InventoryType.PistolLeadShot, InventoryType.DollAttune, InventoryType.DollPoke, InventoryType.CannonShoot, InventoryType.CannonRoundShot]
DontResetSkills = [
 InventoryType.SailPowerRecharge, InventoryType.CannonGrappleHook]

def getSkillRankBonus(self, av, skillId):
    upgradeAmt = WeaponGlobals.getAttackUpgrade(skillId)
    rank = getSkillRank(av, skillId)
    if WeaponGlobals.getSkillTrack(skillId) != WeaponGlobals.PASSIVE_SKILL_INDEX:
        rank -= 1
    statBonus = 0
    if rank > 5:
        statBonus = 5 * upgradeAmt
        statBonus += (rank - 5) * (upgradeAmt / 2.0)
    else:
        statBonus = rank * upgradeAmt
    return statBonus


def getSkillRank(self, av, skillId):
    skillLvl = 0
    inv = av.getInventory()
    if inv:
        skillLvl = max(0, inv.getStackQuantity(skillId) - 1)
        skillLvl += ItemGlobals.getWeaponBoosts(av.currentWeaponId, skillId)
        skillLvl += ItemGlobals.getWeaponBoosts(av.getCurrentCharm(), skillId)
    return skillLvl


defaultSkill = 0
WeaponSfxs = {ItemGlobals.BLUNDERBUSS: {defaultSkill: Gun.getBlunderbussShootSfx},ItemGlobals.MUSKET: {defaultSkill: Gun.getMusketShootSfx}}

def getWeaponSfx(weaponId, skillId):
    subtype = ItemGlobals.getSubtype(weaponId)
    if subtype:
        subtypeSfxs = WeaponSfxs.get(subtype)
        if subtypeSfxs:
            sfx = subtypeSfxs.get(skillId)
            if not sfx:
                sfx = subtypeSfxs.get(defaultSkill)
            return sfx
    return None


DistanceDamageModifiers = {ItemGlobals.BLUNDERBUSS: [[20.0, 1.5], [40.0, 1.2], [70.0, 1.0]],ItemGlobals.MUSKET: [[20.0, 1.0], [40.0, 1.2], [100.0, 1.5]]}

def getDistanceDamageModifier(weaponId, skillId):
    if skillId == EnemySkills.PISTOL_POINT_BLANK:
        return DistanceDamageModifiers.get(ItemGlobals.BLUNDERBUSS)
    subtypeId = ItemGlobals.getSubtype(weaponId)
    return DistanceDamageModifiers.get(subtypeId)


SubtypeParryBonuses = {ItemGlobals.CUTLASS: 0.05,ItemGlobals.SABRE: 0.1}

def getSubtypeParryBonus(weaponId):
    subtypeId = ItemGlobals.getSubtype(weaponId)
    return SubtypeParryBonuses.get(subtypeId, 0.0)


SubtypeRechargeModifiers = {ItemGlobals.SABRE: 0.769,ItemGlobals.BROADSWORD: 1.25,ItemGlobals.SCIMITAR: 1.25,ItemGlobals.DIRK: 0.5}

def getSubtypeRechargeModifier(weaponId):
    subtypeId = ItemGlobals.getSubtype(weaponId)
    return SubtypeRechargeModifiers.get(subtypeId, 1.0)


SubtypeDamageModifiers = {ItemGlobals.KRIS: {AC_COMBAT: 0.5},ItemGlobals.BAYONET: {AC_COMBAT: 0.0}}

def getSubtypeDamageModifier(weaponId, attackType):
    subtype = ItemGlobals.getSubtype(weaponId)
    if subtype:
        subtypeModifier = SubtypeDamageModifiers.get(subtype)
        if subtypeModifier:
            return subtypeModifier.get(attackType, 0.0)
    return 0.0


AttackClassProtectionMap = {AC_COMBAT: ItemGlobals.PROTECT_COMBAT,AC_MISSILE: ItemGlobals.PROTECT_MISSILE,AC_MAGIC: ItemGlobals.PROTECT_MAGIC,AC_GRENADE: ItemGlobals.PROTECT_GRENADE}

def getAttackClassProtection(weaponId, attackType):
    protection = AttackClassProtectionMap.get(attackType)
    if protection:
        return ItemGlobals.getWeaponAttributes(weaponId, protection) * 0.05
    return 0.0


InfiniteAmmoMap = {InventoryType.PistolVenomShot: ItemGlobals.INFINITE_VENOM_SHOT,InventoryType.PistolBaneShot: ItemGlobals.INFINITE_BANE_SHOT,InventoryType.PistolHexEaterShot: ItemGlobals.INFINITE_HEX_EATER_SHOT,InventoryType.PistolSilverShot: ItemGlobals.INFINITE_SILVER_SHOT,InventoryType.PistolSteelShot: ItemGlobals.INFINITE_STEEL_SHOT,InventoryType.DaggerAsp: ItemGlobals.INFINITE_ASP,InventoryType.DaggerAdder: ItemGlobals.INFINITE_ADDER,InventoryType.DaggerSidewinder: ItemGlobals.INFINITE_SIDEWINDER,InventoryType.DaggerViperNest: ItemGlobals.INFINITE_VIPER_NEST,InventoryType.CannonChainShot: ItemGlobals.INFINITE_CHAIN_SHOT,InventoryType.CannonExplosive: ItemGlobals.INFINITE_EXPLOSIVE,InventoryType.CannonGrapeShot: ItemGlobals.INFINITE_GRAPE_SHOT,InventoryType.CannonFirebrand: ItemGlobals.INFINITE_FIREBRAND,InventoryType.CannonThunderbolt: ItemGlobals.INFINITE_THUNDERBOLT,InventoryType.CannonFury: ItemGlobals.INFINITE_FURY}

def canUseInfiniteAmmo(weaponId, skillId):
    infiniteAttribute = InfiniteAmmoMap.get(skillId)
    if infiniteAttribute:
        rank = ItemGlobals.getWeaponAttributes(weaponId, infiniteAttribute)
        if rank:
            return 1
    return 0


CriticalAmmoMap = {InventoryType.CannonRoundShot: ItemGlobals.CRITICAL_ROUND_SHOT,InventoryType.CannonChainShot: ItemGlobals.CRITICAL_CHAIN_SHOT,InventoryType.CannonExplosive: ItemGlobals.CRITICAL_EXPLOSIVE,InventoryType.CannonGrapeShot: ItemGlobals.CRITICAL_GRAPE_SHOT,InventoryType.CannonFirebrand: ItemGlobals.CRITICAL_FIREBRAND,InventoryType.CannonFury: ItemGlobals.CRITICAL_FURY}

def getExtraCriticalChance(weaponId, skillId):
    crit = CriticalAmmoMap.get(skillId)
    if crit:
        return ItemGlobals.getWeaponAttributes(weaponId, crit)
    return 0


DeadzoneSubtypes = [
 ItemGlobals.MUSKET, ItemGlobals.BAYONET]

def hasDeadzone(weaponId):
    subtype = ItemGlobals.getSubtype(weaponId)
    if subtype in DeadzoneSubtypes:
        return True
    return False


GunRanges = {ItemGlobals.PISTOL: ItemGlobals.MEDIUM,ItemGlobals.REPEATER: ItemGlobals.MEDIUM,ItemGlobals.BLUNDERBUSS: ItemGlobals.SHORT,ItemGlobals.MUSKET: ItemGlobals.LONG,ItemGlobals.BAYONET: ItemGlobals.LONG}

def getRange(itemId):
    subtype = ItemGlobals.getSubtype(itemId)
    if subtype:
        return GunRanges.get(subtype, ItemGlobals.SHORT)
    return ItemGlobals.SHORT


RangeAmmoMap = {InventoryType.CannonRoundShot: ItemGlobals.RANGE_ROUND_SHOT,InventoryType.CannonChainShot: ItemGlobals.RANGE_CHAIN_SHOT,InventoryType.CannonExplosive: ItemGlobals.RANGE_EXPLOSIVE,InventoryType.CannonGrapeShot: ItemGlobals.RANGE_GRAPE_SHOT,InventoryType.CannonFirebrand: ItemGlobals.RANGE_FIREBRAND,InventoryType.CannonFury: ItemGlobals.RANGE_FURY}

def getExtraRange(weaponId, skillId):
    range = RangeAmmoMap.get(skillId)
    if range:
        return ItemGlobals.getWeaponAttributes(weaponId, range)
    return 0


MAX_HEADING_DIFF = 15.0
ROLLTHRUST_DEADZONE = 15.0
HeadingSkills = [
 EnemySkills.CUTLASS_ROLLTHRUST]

def isHeadingSkill(skillId):
    return skillId in HeadingSkills


BreakAttackComboSkills = [
 InventoryType.CutlassSlash, InventoryType.CutlassCleave, InventoryType.CutlassFlourish, InventoryType.CutlassStab, InventoryType.DaggerSwipe, InventoryType.DaggerGouge, InventoryType.DaggerEviscerate, EnemySkills.BROADSWORD_SLASH, EnemySkills.BROADSWORD_CLEAVE, EnemySkills.BROADSWORD_FLOURISH, EnemySkills.BROADSWORD_STAB, EnemySkills.SABRE_SLASH, EnemySkills.SABRE_CLEAVE, EnemySkills.SABRE_FLOURISH, EnemySkills.SABRE_STAB]

def isBreakAttackComboSkill(skillId):
    return skillId in BreakAttackComboSkills


DefenseSkillAttacks = {EnemySkills.MISC_FEINT: AC_COMBAT,EnemySkills.MISC_HEX_WARD: AC_MAGIC,EnemySkills.MISC_VOODOO_REFLECT: VOODOO}

def getDefenseSkillAttacks(skillId):
    return DefenseSkillAttacks.get(skillId, 0)


ImmunityItems = {C_POISON: ItemGlobals.IMMUNITY_POISON,C_ACID: ItemGlobals.IMMUNITY_ACID,C_BLIND: ItemGlobals.IMMUNITY_BLIND,C_DIRT: ItemGlobals.IMMUNITY_BLIND,C_ON_FIRE: ItemGlobals.IMMUNITY_FIRE,C_ON_CURSED_FIRE: ItemGlobals.IMMUNITY_FIRE,C_HOLD: ItemGlobals.IMMUNITY_HOLD,C_STUN: ItemGlobals.IMMUNITY_STUN,C_CURSE: ItemGlobals.IMMUNITY_CURSE,C_SLOW: ItemGlobals.IMMUNITY_PAIN,C_PAIN: ItemGlobals.IMMUNITY_PAIN,C_WEAKEN: ItemGlobals.IMMUNITY_WEAKEN,C_LIFEDRAIN: ItemGlobals.IMMUNITY_LIFEDRAIN}

def hasImmunityFromEffect(effectId, itemId):
    attributeId = ImmunityItems.get(effectId)
    if attributeId:
        return ItemGlobals.getWeaponAttributes(itemId, attributeId)
    return 0


HalfDurationItems = {C_POISON: ItemGlobals.HALF_DURATION_POISON,C_ACID: ItemGlobals.HALF_DURATION_ACID,C_BLIND: ItemGlobals.HALF_DURATION_BLIND,C_DIRT: ItemGlobals.HALF_DURATION_BLIND,C_ON_FIRE: ItemGlobals.HALF_DURATION_FIRE,C_ON_CURSED_FIRE: ItemGlobals.HALF_DURATION_FIRE,C_HOLD: ItemGlobals.HALF_DURATION_HOLD,C_STUN: ItemGlobals.HALF_DURATION_STUN,C_CURSE: ItemGlobals.HALF_DURATION_CURSE,C_SLOW: ItemGlobals.HALF_DURATION_PAIN,C_PAIN: ItemGlobals.HALF_DURATION_PAIN,C_WOUND: ItemGlobals.HALF_DURATION_WOUND}

def canHalveEffectDuration(effectId, itemId):
    attributeId = HalfDurationItems.get(effectId)
    if attributeId:
        return ItemGlobals.getWeaponAttributes(itemId, attributeId)
    return 0


HalfDamageItems = {C_LIFEDRAIN: ItemGlobals.HALF_DAMAGE_LIFEDRAIN,C_SOULTAP: ItemGlobals.HALF_DAMAGE_SOULTAP}

def canHalveEffectDamage(effectId, itemId):
    attributeId = HalfDamageItems.get(effectId)
    if attributeId:
        return ItemGlobals.getWeaponAttributes(itemId, attributeId)
    return 0


SpecialSkills = [
 EnemySkills.PISTOL_DEADEYE, EnemySkills.PISTOL_STUNSHOT, EnemySkills.PISTOL_BREAKSHOT, EnemySkills.PISTOL_HOTSHOT, EnemySkills.PISTOL_RAPIDFIRE, EnemySkills.PISTOL_POINT_BLANK, EnemySkills.PISTOL_QUICKLOAD, EnemySkills.BAYONET_STAB, EnemySkills.BAYONET_PLAYER_RUSH, EnemySkills.BAYONET_PLAYER_BASH, EnemySkills.BAYONET_DISABLE, EnemySkills.STAFF_TOGGLE_AURA_OFF, EnemySkills.STAFF_TOGGLE_AURA_WARDING, EnemySkills.STAFF_TOGGLE_AURA_NATURE, EnemySkills.STAFF_TOGGLE_AURA_DARK]
PropSkills = {ItemGlobals.QUEST_PROP_TORCH: [EnemySkills.TORCH_ATTACK]}

def getPropSkills(weaponId):
    subtype = ItemGlobals.getSubtype(weaponId)
    return PropSkills.get(subtype, [])