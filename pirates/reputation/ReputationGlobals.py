from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType, InventoryId
from pirates.battle import WeaponGlobals
__categories = (
 InventoryType.GeneralRep, InventoryType.MeleeRep, InventoryType.CutlassRep, InventoryType.PistolRep, InventoryType.MusketRep, InventoryType.DaggerRep, InventoryType.GrenadeRep, InventoryType.DollRep, InventoryType.WandRep, InventoryType.KettleRep, InventoryType.CannonRep, InventoryType.SailingRep, InventoryType.LockpickRep, InventoryType.GamblingRep, InventoryType.FishingRep, InventoryType.PotionsRep, InventoryType.DefenseCannonRep, InventoryType.OverflowRep)

def getReputationCategories():
    return __categories


def getUnspentCategories():
    start = InventoryType.begin_Unspent
    total = InventoryType.end_Unspent - start
    listCat = []
    for i in range(total):
        listCat.append(start + i)

    return listCat


ReputationNeededToLevel = [
 0, 50, 150, 300, 500, 700, 900, 1100, 1300, 1500, 1700, 1900, 2100, 2300, 2500, 2700, 2900, 3200, 3500, 3800, 4100, 4400, 4700, 5000, 5300, 5600, 5900, 6200, 6500, 6800, 7100, 7400, 7700, 8000, 8400, 8800, 9200, 9600, 10000, 10400, 10800, 11200, 11600, 12000, 12400, 12800, 13200, 13600, 14000, 14400, 14900]
GlobalReputationNeeded = [
 0, 300, 450, 600, 800, 1000, 1300, 1600, 2000, 2400, 2900, 3400, 4000, 4600, 5300, 6000, 6800, 7600, 8500, 9400, 10400, 11400, 12500, 13600, 14800, 16100, 17400, 18800, 20200, 21700, 23300, 24900, 26600, 28400, 30200, 32100, 34100, 36100, 38200, 40400, 42600, 44900, 47300, 49700, 52200, 54800, 57500, 60200, 63000, 65900, 68900, 71900, 75000, 78200, 81500, 84900, 88300, 91800, 95400, 99100, 102900, 106800, 110700, 114700, 118800, 123000, 127300, 131700, 136200, 140800, 145400, 150100, 154900, 159800, 164800, 169900, 175100, 180400, 185800, 191300, 196900]
LevelCap = 30
GlobalLevelCap = 50
MinigameLevelCap = 20
TotalReputationAtLevel = []
GlobalReputationAtLevel = []

def __buildTotalReputationList():
    TotalReputationAtLevel.append(0)
    runningTotal = 0
    for rep in ReputationNeededToLevel:
        runningTotal += rep
        TotalReputationAtLevel.append(runningTotal)

    GlobalReputationAtLevel.append(0)
    runningTotal = 0
    for rep in GlobalReputationNeeded:
        runningTotal += rep
        GlobalReputationAtLevel.append(runningTotal)


__buildTotalReputationList()

def getTotalReputation(category, level, value=0):
    if level >= LevelCap:
        return TotalReputationAtLevel[LevelCap]
    else:
        return TotalReputationAtLevel[level] + value


def getTotalGlobalReputation(category, level, value=0):
    if level >= GlobalLevelCap:
        return GlobalReputationAtLevel[GlobalLevelCap]
    else:
        return GlobalReputationAtLevel[level] + value


def getLevelFromTotalReputation(category, totalRep):
    if category == InventoryType.OverallRep:
        data = GlobalReputationAtLevel
        level = -1
        for rep in data:
            if totalRep < rep:
                previousLevelRep = data[level]
                value = totalRep - previousLevelRep
                return (
                 level, value)
            level += 1

        level = GlobalLevelCap
        value = 0
        return (
         level, value)
    else:
        data = TotalReputationAtLevel
        level = -1
        for rep in data:
            if totalRep < rep:
                previousLevelRep = data[level]
                value = totalRep - previousLevelRep
                return (
                 level, value)
            level += 1

        level = LevelCap
        value = 0
        return (
         level, value)


def getReputationNeededToLevel(category, level):
    if category == InventoryType.OverallRep:
        if level >= GlobalLevelCap:
            return 1
        else:
            return GlobalReputationNeeded[level]
    elif level >= LevelCap:
        return 1
    else:
        return ReputationNeededToLevel[level]


MonsterRep = 1
RepIcons = {InventoryType.OverallRep: 'main_gui_game_gui_base',InventoryType.CutlassRep: 'pir_t_ico_swd_cutlass_a',InventoryType.PistolRep: 'pir_t_ico_gun_pistol_a',InventoryType.MusketRep: 'pir_t_ico_gun_pistol_a',InventoryType.DaggerRep: 'pir_t_ico_knf_small',InventoryType.GrenadeRep: 'pir_t_ico_bom_grenade',InventoryType.DollRep: 'pir_t_ico_dol_straw',InventoryType.WandRep: 'pir_t_ico_stf_wood',InventoryType.CannonRep: 'pir_t_ico_can_single',InventoryType.SailingRep: 'sail_full_sail',InventoryType.FishingRep: 'pir_t_gui_fsh_purchaseIcon'}