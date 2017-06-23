from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
NONE = 0
VELVET_ROPE = 1
FULL = 2
FreeLevelCap = 7
FreeOverallLevelCap = 14
FreeSkillCap = 3
FreeMaxSkillSpend = 6
FreeGuildRestrict = True
FreeExpNerf = 1.0
FreeNametagChange = True
AllAccessHoliday = False

def getPaidStatus(avId, checkHoliday=True):
    global AllAccessHoliday
    av = base.cr.getDo(avId)
    if av:
        if checkHoliday and AllAccessHoliday:
            return FULL
        else:
            return av.getGameAccess() == FULL
    return False


def getFounderStatus(avId):
    av = base.cr.getDo(avId)
    if av:
        return av.getFounder()
    return False


def setAllAccess(allAccess):
    global AllAccessHoliday
    if allAccess:
        AllAccessHoliday = True
    else:
        AllAccessHoliday = False
    messenger.send('AllAccessChanged', [AllAccessHoliday])


def getPaidStatusAI(playerID):
    playerOb = simbase.air.getDo(playerID)
    if playerOb:
        if AllAccessHoliday:
            return FULL
        return hasattr(playerOb, 'getGameAccess') and playerOb.getGameAccess() == FULL
    else:
        return NONE


def pruneFreebooterSkills(skillTrack):
    if getPaidStatus(base.localAvatar.getDoId()):
        return skillTrack
    else:
        return filter(lambda skillId: WeaponGlobals.canFreeUse(skillId), skillTrack)


def allowedFreebooterWeapon(repId):
    if repId == InventoryType.DaggerRep:
        return False
    elif repId == InventoryType.GrenadeRep:
        return False
    elif repId == InventoryType.WandRep:
        return False
    elif repId == InventoryType.DollRep:
        return True
    else:
        return True