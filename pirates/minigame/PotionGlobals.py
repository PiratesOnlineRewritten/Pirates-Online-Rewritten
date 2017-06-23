from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals
from pirates.battle.WeaponConstants import *
notify = DirectNotifyGlobal.directNotify.newCategory('PotionGlobals')
FART_EFFECT_DELAY = 15.0
BURP_EFFECT_DELAY = 15.0
VOMIT_EFFECT_DELAY = 15.0
GENERIC_EFFECT_DELAY = 10.0
PLAYER_INCREASE_SCALE = 1.5
PLAYER_REDUCE_SCALE = 0.5
TextColor = (
 0.28, 0.23, 0.17, 1.0)
TextColorDisabled = (0.58, 0.49, 0.32, 1.0)
TextColorHighlight = (0.23, 0.28, 0.17, 1.0)
BONUS_XP_AMT = [
 10, 30, 60, 100, 150, 210, 280, 360, 450, 550, 660, 780, 910, 1050, 1200, 1360, 1530, 1710, 1900, 2100]
__potionBuffs = {C_CANNON_DAMAGE_LVL1: {'duration': 180.0,'xp': 35,'potency': 0.1,'potionId': ItemGlobals.POTION_CANNON_1,'haveMade': InventoryType.HaveMade_CannonDamageLvl1,'dontStackList': [C_CANNON_DAMAGE_LVL1, C_CANNON_DAMAGE_LVL2, C_CANNON_DAMAGE_LVL3]},C_CANNON_DAMAGE_LVL2: {'duration': 240.0,'xp': 90,'potency': 0.15,'potionId': ItemGlobals.POTION_CANNON_2,'haveMade': InventoryType.HaveMade_CannonDamageLvl2,'dontStackList': [C_CANNON_DAMAGE_LVL1, C_CANNON_DAMAGE_LVL2, C_CANNON_DAMAGE_LVL3]},C_CANNON_DAMAGE_LVL3: {'duration': 300.0,'xp': 140,'potency': 0.2,'potionId': ItemGlobals.POTION_CANNON_3,'haveMade': InventoryType.HaveMade_CannonDamageLvl3,'dontStackList': [C_CANNON_DAMAGE_LVL1, C_CANNON_DAMAGE_LVL2, C_CANNON_DAMAGE_LVL3]},C_PISTOL_DAMAGE_LVL1: {'duration': 180.0,'xp': 25,'potency': 0.1,'potionId': ItemGlobals.POTION_PISTOL_1,'haveMade': InventoryType.HaveMade_PistolDamageLvl1,'dontStackList': [C_PISTOL_DAMAGE_LVL1, C_PISTOL_DAMAGE_LVL2, C_PISTOL_DAMAGE_LVL3]},C_PISTOL_DAMAGE_LVL2: {'duration': 240.0,'xp': 80,'potency': 0.15,'potionId': ItemGlobals.POTION_PISTOL_2,'haveMade': InventoryType.HaveMade_PistolDamageLvl2,'dontStackList': [C_PISTOL_DAMAGE_LVL1, C_PISTOL_DAMAGE_LVL2, C_PISTOL_DAMAGE_LVL3]},C_PISTOL_DAMAGE_LVL3: {'duration': 300.0,'xp': 130,'potency': 0.2,'potionId': ItemGlobals.POTION_PISTOL_3,'haveMade': InventoryType.HaveMade_PistolDamageLvl3,'dontStackList': [C_PISTOL_DAMAGE_LVL1, C_PISTOL_DAMAGE_LVL2, C_PISTOL_DAMAGE_LVL3]},C_CUTLASS_DAMAGE_LVL1: {'duration': 180.0,'xp': 25,'potency': 0.1,'potionId': ItemGlobals.POTION_CUTLASS_1,'haveMade': InventoryType.HaveMade_CutlassDamageLvl1,'dontStackList': [C_CUTLASS_DAMAGE_LVL1, C_CUTLASS_DAMAGE_LVL2, C_CUTLASS_DAMAGE_LVL3]},C_CUTLASS_DAMAGE_LVL2: {'duration': 240.0,'xp': 80,'potency': 0.15,'potionId': ItemGlobals.POTION_CUTLASS_2,'haveMade': InventoryType.HaveMade_CutlassDamageLvl2,'dontStackList': [C_CUTLASS_DAMAGE_LVL1, C_CUTLASS_DAMAGE_LVL2, C_CUTLASS_DAMAGE_LVL3]},C_CUTLASS_DAMAGE_LVL3: {'duration': 300.0,'xp': 130,'potency': 0.2,'potionId': ItemGlobals.POTION_CUTLASS_3,'haveMade': InventoryType.HaveMade_CutlassDamageLvl3,'dontStackList': [C_CUTLASS_DAMAGE_LVL1, C_CUTLASS_DAMAGE_LVL2, C_CUTLASS_DAMAGE_LVL3]},C_DOLL_DAMAGE_LVL1: {'duration': 180.0,'xp': 35,'potency': 0.1,'potionId': ItemGlobals.POTION_DOLL_1,'haveMade': InventoryType.HaveMade_DollDamageLvl1,'dontStackList': [C_DOLL_DAMAGE_LVL1, C_DOLL_DAMAGE_LVL2, C_DOLL_DAMAGE_LVL3]},C_DOLL_DAMAGE_LVL2: {'duration': 240.0,'xp': 90,'potency': 0.15,'potionId': ItemGlobals.POTION_DOLL_2,'haveMade': InventoryType.HaveMade_DollDamageLvl2,'dontStackList': [C_DOLL_DAMAGE_LVL1, C_DOLL_DAMAGE_LVL2, C_DOLL_DAMAGE_LVL3]},C_DOLL_DAMAGE_LVL3: {'duration': 300.0,'xp': 140,'potency': 0.2,'potionId': ItemGlobals.POTION_DOLL_3,'haveMade': InventoryType.HaveMade_DollDamageLvl3,'dontStackList': [C_DOLL_DAMAGE_LVL1, C_DOLL_DAMAGE_LVL2, C_DOLL_DAMAGE_LVL3]},C_HASTEN_LVL1: {'duration': 60.0,'xp': 45,'potency': 0.3,'potionId': ItemGlobals.POTION_SPEED_1,'haveMade': InventoryType.HaveMade_HastenLvl1,'dontStackList': [C_HASTEN_LVL1, C_HASTEN_LVL2, C_HASTEN_LVL3]},C_HASTEN_LVL2: {'duration': 180.0,'xp': 100,'potency': 0.3,'potionId': ItemGlobals.POTION_SPEED_2,'haveMade': InventoryType.HaveMade_HastenLvl2,'dontStackList': [C_HASTEN_LVL1, C_HASTEN_LVL2, C_HASTEN_LVL3]},C_HASTEN_LVL3: {'duration': 360.0,'xp': 145,'potency': 0.3,'potionId': ItemGlobals.POTION_SPEED_3,'haveMade': InventoryType.HaveMade_HastenLvl3,'dontStackList': [C_HASTEN_LVL1, C_HASTEN_LVL2, C_HASTEN_LVL3]},C_REP_BONUS_LVL1: {'duration': 180.0,'xp': 170,'potency': 0.15,'potionId': ItemGlobals.POTION_REP_1,'haveMade': InventoryType.HaveMade_RepBonusLvl1,'dontStackList': [C_REP_BONUS_LVL1, C_REP_BONUS_LVL2, C_REP_BONUS_LVL3, C_REP_BONUS_LVLCOMP]},C_REP_BONUS_LVL2: {'duration': 180.0,'xp': 230,'potency': 0.3,'potionId': ItemGlobals.POTION_REP_2,'haveMade': InventoryType.HaveMade_RepBonusLvl2,'dontStackList': [C_REP_BONUS_LVL1, C_REP_BONUS_LVL2, C_REP_BONUS_LVL3, C_REP_BONUS_LVLCOMP]},C_REP_BONUS_LVL3: {'duration': 3600.0,'xp': 300,'potency': 1.0,'potionId': ItemGlobals.POTION_REP_3,'haveMade': InventoryType.HaveMade_RepBonusLvl3,'dontStackList': [C_REP_BONUS_LVL1, C_REP_BONUS_LVL2, C_REP_BONUS_LVL3, C_REP_BONUS_LVLCOMP]},C_REP_BONUS_LVLCOMP: {'duration': 3600.0,'xp': 300,'potency': 5.0,'potionId': ItemGlobals.POTION_REP_COMP,'haveMade': InventoryType.HaveMade_RepBonusLvlComp,'dontStackList': [C_REP_BONUS_LVL1, C_REP_BONUS_LVL2, C_REP_BONUS_LVL3, C_REP_BONUS_LVLCOMP]},C_GOLD_BONUS_LVL1: {'duration': 180.0,'xp': 160,'potency': 0.1,'potionId': ItemGlobals.POTION_GOLD_1,'haveMade': InventoryType.HaveMade_GoldBonusLvl1,'dontStackList': [C_GOLD_BONUS_LVL1, C_GOLD_BONUS_LVL2]},C_GOLD_BONUS_LVL2: {'duration': 180.0,'xp': 220,'potency': 0.2,'potionId': ItemGlobals.POTION_GOLD_2,'haveMade': InventoryType.HaveMade_GoldBonusLvl2,'dontStackList': [C_GOLD_BONUS_LVL1, C_GOLD_BONUS_LVL2]},C_INVISIBILITY_LVL1: {'duration': 60.0,'xp': 150,'potionId': ItemGlobals.POTION_INVIS_1,'haveMade': InventoryType.HaveMade_InvisibilityLvl1,'dontStackList': [C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2, C_BURP, C_FART, C_FART_LVL2, C_VOMIT, C_HEAD_GROW, C_CRAZY_SKIN_COLOR, C_SIZE_REDUCE, C_SIZE_INCREASE, C_HEAD_FIRE, C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM]},C_INVISIBILITY_LVL2: {'duration': 120.0,'xp': 220,'potionId': ItemGlobals.POTION_INVIS_2,'haveMade': InventoryType.HaveMade_InvisibilityLvl2,'dontStackList': [C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2, C_BURP, C_FART, C_FART_LVL2, C_VOMIT, C_HEAD_GROW, C_CRAZY_SKIN_COLOR, C_SIZE_REDUCE, C_SIZE_INCREASE, C_HEAD_FIRE, C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM]},C_ACCURACY_BONUS_LVL1: {'duration': 180.0,'xp': 60,'potency': 0.1,'potionId': ItemGlobals.POTION_ACC_1,'haveMade': InventoryType.HaveMade_AccuracyBonusLvl1,'dontStackList': [C_ACCURACY_BONUS_LVL1, C_ACCURACY_BONUS_LVL2, C_ACCURACY_BONUS_LVL3]},C_ACCURACY_BONUS_LVL2: {'duration': 240.0,'xp': 110,'potency': 0.15,'potionId': ItemGlobals.POTION_ACC_2,'haveMade': InventoryType.HaveMade_AccuracyBonusLvl2,'dontStackList': [C_ACCURACY_BONUS_LVL1, C_ACCURACY_BONUS_LVL2, C_ACCURACY_BONUS_LVL3]},C_ACCURACY_BONUS_LVL3: {'duration': 300.0,'xp': 160,'potency': 0.2,'potionId': ItemGlobals.POTION_ACC_3,'haveMade': InventoryType.HaveMade_AccuracyBonusLvl3,'dontStackList': [C_ACCURACY_BONUS_LVL1, C_ACCURACY_BONUS_LVL2, C_ACCURACY_BONUS_LVL3]},C_REMOVE_GROGGY: {'duration': 0.0,'xp': 180,'potionId': ItemGlobals.POTION_GROG,'haveMade': InventoryType.HaveMade_RemoveGroggy,'dontStackList': []},C_REGEN_LVL1: {'duration': 120.0,'xp': 70,'potency': 0.03,'potionId': ItemGlobals.POTION_REGEN_1,'haveMade': InventoryType.HaveMade_RegenLvl1,'dontStackList': [C_REGEN_LVL1, C_REGEN_LVL2, C_REGEN_LVL3, C_REGEN_LVL4]},C_REGEN_LVL2: {'duration': 180.0,'xp': 120,'potency': 0.03,'potionId': ItemGlobals.POTION_REGEN_2,'haveMade': InventoryType.HaveMade_RegenLvl2,'dontStackList': [C_REGEN_LVL1, C_REGEN_LVL2, C_REGEN_LVL3, C_REGEN_LVL4]},C_REGEN_LVL3: {'duration': 240.0,'xp': 165,'potency': 0.03,'potionId': ItemGlobals.POTION_REGEN_3,'haveMade': InventoryType.HaveMade_RegenLvl3,'dontStackList': [C_REGEN_LVL1, C_REGEN_LVL2, C_REGEN_LVL3, C_REGEN_LVL4]},C_REGEN_LVL4: {'duration': 300.0,'xp': 200,'potency': 0.03,'potionId': ItemGlobals.POTION_REGEN_4,'haveMade': InventoryType.HaveMade_RegenLvl4,'dontStackList': [C_REGEN_LVL1, C_REGEN_LVL2, C_REGEN_LVL3, C_REGEN_LVL4]},C_BURP: {'duration': 50.0,'xp': 55,'potionId': ItemGlobals.POTION_BURP,'haveMade': InventoryType.HaveMade_Burp,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_BURP, C_FART, C_FART_LVL2, C_VOMIT, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2]},C_FART: {'duration': 50.0,'xp': 65,'potionId': ItemGlobals.POTION_FART,'haveMade': InventoryType.HaveMade_Fart,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_BURP, C_FART, C_FART_LVL2, C_VOMIT, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2, C_SIZE_INCREASE, C_SIZE_REDUCE]},C_FART_LVL2: {'duration': 150.0,'xp': 65,'potionId': ItemGlobals.POTION_FART_2,'haveMade': InventoryType.HaveMade_FartLvl2,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_BURP, C_FART, C_FART_LVL2, C_VOMIT, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2, C_SIZE_INCREASE, C_SIZE_REDUCE]},C_VOMIT: {'duration': 33.0,'xp': 75,'potionId': ItemGlobals.POTION_VOMIT,'haveMade': InventoryType.HaveMade_Vomit,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_BURP, C_FART, C_FART_LVL2, C_VOMIT, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2]},C_HEAD_GROW: {'duration': 300.0,'xp': 100,'potionId': ItemGlobals.POTION_HEADGROW,'haveMade': InventoryType.HaveMade_HeadGrow,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_HEAD_GROW, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2]},C_CRAZY_SKIN_COLOR: {'duration': 300.0,'xp': 110,'potionId': ItemGlobals.POTION_FACECOLOR,'haveMade': InventoryType.HaveMade_FaceColor,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_CRAZY_SKIN_COLOR, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2, C_SIZE_INCREASE, C_SIZE_REDUCE, C_HEAD_FIRE]},C_SIZE_REDUCE: {'duration': 300.0,'xp': 120,'potionId': ItemGlobals.POTION_SHRINK,'haveMade': InventoryType.HaveMade_SizeReduce,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_SIZE_REDUCE, C_SIZE_INCREASE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2, C_CRAZY_SKIN_COLOR, C_HEAD_FIRE, C_FART_LVL2, C_FART]},C_SIZE_INCREASE: {'duration': 300.0,'xp': 190,'potionId': ItemGlobals.POTION_GROW,'haveMade': InventoryType.HaveMade_SizeIncrease,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_SIZE_REDUCE, C_SIZE_INCREASE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2, C_CRAZY_SKIN_COLOR, C_HEAD_FIRE, C_FART_LVL2, C_FART]},C_HEAD_FIRE: {'duration': 300.0,'xp': 210,'potionId': ItemGlobals.POTION_HEADONFIRE,'haveMade': InventoryType.HaveMade_HeadFire,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_HEAD_FIRE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2, C_CRAZY_SKIN_COLOR, C_SIZE_INCREASE, C_SIZE_REDUCE]},C_SCORPION_TRANSFORM: {'duration': 300.0,'xp': 0,'potionId': ItemGlobals.POTION_SCORPION,'haveMade': InventoryType.HaveMade_ScorpionTransform,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_HEAD_GROW, C_HEAD_FIRE, C_SIZE_REDUCE, C_SIZE_INCREASE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2]},C_ALLIGATOR_TRANSFORM: {'duration': 300.0,'xp': 0,'potionId': ItemGlobals.POTION_ALLIGATOR,'haveMade': InventoryType.HaveMade_AlligatorTransform,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_HEAD_GROW, C_HEAD_FIRE, C_SIZE_REDUCE, C_SIZE_INCREASE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2]},C_CRAB_TRANSFORM: {'duration': 300.0,'xp': 0,'potionId': ItemGlobals.POTION_CRAB,'haveMade': InventoryType.HaveMade_CrabTransform,'dontStackList': [C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_HEAD_GROW, C_HEAD_FIRE, C_SIZE_REDUCE, C_SIZE_INCREASE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2]},C_STAFF_ENCHANT_LVL1: {'duration': 0.0,'xp': 100,'potency': 0.0,'potionId': ItemGlobals.STAFF_ENCHANT_1,'dontStackList': []},C_STAFF_ENCHANT_LVL2: {'duration': 0.0,'xp': 100,'potency': 0.0,'potionId': ItemGlobals.STAFF_ENCHANT_2,'dontStackList': []},C_SUMMON_CHICKEN: {'duration': 300,'xp': 0,'potionId': ItemGlobals.POTION_SUMMON_CHICKEN,'dontStackList': [C_SUMMON_CHICKEN, C_SUMMON_MONKEY, C_SUMMON_WASP, C_SUMMON_DOG, C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_HEAD_GROW, C_HEAD_FIRE, C_SIZE_REDUCE, C_SIZE_INCREASE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2]},C_SUMMON_MONKEY: {'duration': 300,'xp': 0,'potionId': ItemGlobals.POTION_SUMMON_MONKEY,'dontStackList': [C_SUMMON_CHICKEN, C_SUMMON_MONKEY, C_SUMMON_WASP, C_SUMMON_DOG, C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_HEAD_GROW, C_HEAD_FIRE, C_SIZE_REDUCE, C_SIZE_INCREASE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2]},C_SUMMON_WASP: {'duration': 300,'xp': 0,'potionId': ItemGlobals.POTION_SUMMON_WASP,'dontStackList': [C_SUMMON_CHICKEN, C_SUMMON_MONKEY, C_SUMMON_WASP, C_SUMMON_DOG, C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_HEAD_GROW, C_HEAD_FIRE, C_SIZE_REDUCE, C_SIZE_INCREASE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2]},C_SUMMON_DOG: {'duration': 300,'xp': 0,'potionId': ItemGlobals.POTION_SUMMON_DOG,'dontStackList': [C_SUMMON_CHICKEN, C_SUMMON_MONKEY, C_SUMMON_WASP, C_SUMMON_DOG, C_SCORPION_TRANSFORM, C_ALLIGATOR_TRANSFORM, C_CRAB_TRANSFORM, C_HEAD_GROW, C_HEAD_FIRE, C_SIZE_REDUCE, C_SIZE_INCREASE, C_INVISIBILITY_LVL1, C_INVISIBILITY_LVL2]}}

def getIsPotionBuff(effectId):
    return effectId in __potionBuffs


def updatePotionBuffDuration(effectId, duration):
    if getIsPotionBuff(effectId):
        __potionBuffs[effectId]['duration'] = duration
    else:
        notify.warning('%d is not a valid effectId' % effectId)


def getPotionBuffDuration(effectId):
    if getIsPotionBuff(effectId):
        return __potionBuffs[effectId]['duration']
    else:
        notify.warning('%d is not a valid effectId' % effectId)
        return 0.0


def potionBuffIdToInventoryTypeId(effectId):
    if getIsPotionBuff(effectId):
        return __potionBuffs[effectId]['potionId']
    else:
        notify.warning('%d is not a valid effectId' % effectId)
        return 0


def potionInventoryTypeIdToBuffId(inventoryTypeId):
    for buffId, potion in __potionBuffs.iteritems():
        if potion['potionId'] == inventoryTypeId:
            return buffId

    return 0


def getPotionBuffXP(effectId):
    if getIsPotionBuff(effectId):
        return __potionBuffs[effectId]['xp']
    else:
        notify.warning('%d is not a valid effectId' % effectId)
        return 0


def getIsPotionBlocked(av, effectId):
    if hasattr(av, 'getSkillEffects'):
        skillEffects = av.getSkillEffects()
        dontStackList = getPotionBuffDontStackList(effectId)
        for buff in skillEffects:
            if buff in dontStackList:
                return buff

        return 0
    else:
        notify.warning("avatar doesn't have method getSkillEffects()" % effectId)
        return 0


def getPotionBuffDontStackList(effectId):
    if getIsPotionBuff(effectId):
        return __potionBuffs[effectId]['dontStackList']
    else:
        notify.warning('%d is not a valid effectId' % effectId)
        return []


def getPotionHaveMadeFlag(effectId):
    if getIsPotionBuff(effectId):
        return __potionBuffs[effectId]['haveMade']
    else:
        notify.warning('%d is not a valid effectId' % effectId)
        return 0


def getPotionForHaveMadeID(madeID):
    for potionID, potion in __potionBuffs.iteritems():
        if potion['haveMade'] == madeID:
            return potionID

    return 0


def getPotionPotency(effectId):
    if getIsPotionBuff(effectId):
        if 'potency' in __potionBuffs[effectId]:
            return __potionBuffs[effectId]['potency']
        else:
            notify.warning('There is no potency entry for %d' % effectId)
            return 1.0
    else:
        notify.warning('%d is not a valid effectId' % effectId)
        return 1.0


def getPotionItemID(effectId):
    potionData = __potionBuffs.get(effectId)
    if potionData:
        return potionData.get('potionId')
    else:
        notify.warning('There is no potionId entry for %d' % effectId)
        return None
    return None


def getPotionRepBonus(av, reputation):
    potionRepBonusPercentage = 0.0
    if hasattr(av, 'getSkillEffects'):
        skillEffects = av.getSkillEffects()
        for buff in skillEffects:
            if buff in [C_REP_BONUS_LVL1, C_REP_BONUS_LVL2, C_REP_BONUS_LVL3, C_REP_BONUS_LVLCOMP]:
                potionRepBonusPercentage += getPotionPotency(buff)

    return int(potionRepBonusPercentage * reputation)


def getPotionGoldBonus(av, gold):
    potionGoldBonusPercentage = getGoldBoostEffectPercent(av)
    return int(potionGoldBonusPercentage * gold)


def getGoldBoostEffectPercent(av):
    potionGoldBonusPercentage = 0.0
    if hasattr(av, 'getSkillEffects'):
        skillEffects = av.getSkillEffects()
        for buff in skillEffects:
            if buff in [C_GOLD_BONUS_LVL1, C_GOLD_BONUS_LVL2]:
                potionGoldBonusPercentage += getPotionPotency(buff)

    return potionGoldBonusPercentage