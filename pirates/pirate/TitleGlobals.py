from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PLocalizer
from pirates.pvp import PVPGlobals
ShipPVPTitle = 1
LandPVPTitle = 2
FounderTitle = 3
CollectorTitle = 4
landPVPIcons = {0: None,1: 'pir_t_ico_inf_lnd_rookie',2: 'pir_t_ico_inf_lnd_brawler',3: 'pir_t_ico_inf_lnd_duelist',4: 'pir_t_ico_inf_lnd_buccaneer',5: 'pir_t_ico_inf_lnd_swashbuckler',6: 'pir_t_ico_inf_lnd_warmonger',7: 'pir_t_ico_inf_lnd_warmaster'}
shipPVPIcons = {0: None,1: 'pir_t_ico_inf_shp_mariner',2: 'pir_t_ico_inf_shp_lieutenant',3: 'pir_t_ico_inf_shp_commander',4: 'pir_t_ico_inf_shp_captain',5: 'pir_t_ico_inf_shp_commodore',6: 'pir_t_ico_inf_shp_vice_admiral',7: 'pir_t_ico_inf_shp_admiral'}
founderIcons = {0: None,1: 'founders_coin'}
standardScale = 2.2
foundersScale = 6.0
pvpScale = 1.8
TestBreakpoints1 = [
 0, 5, 10, 40, 60, 200, 564, 2323]
TestBreakpoints2 = [0, 500, 501, 502, 503, 504, 564, 2323]
FounderBreakpoints = [
 0, 1]
Title2nametagTextProp = {ShipPVPTitle: None,LandPVPTitle: None,FounderTitle: 'goldFounder'}
TitlesDict = {ShipPVPTitle: ('models/gui/gui_icons_infamy', shipPVPIcons, pvpScale, PLocalizer.PVPTitleSeaName, PLocalizer.PVPTitleSeaRanks, PLocalizer.PVPTitleSeaDesc, PVPGlobals.RenownBreakpointsSea, InventoryType.PVPTotalInfamySea, 0),LandPVPTitle: ('models/gui/gui_icons_infamy', landPVPIcons, pvpScale, PLocalizer.PVPTitleLandName, PLocalizer.PVPTitleLandRanks, PLocalizer.PVPTitleLandDesc, PVPGlobals.RenownBreakpointsLand, InventoryType.PVPTotalInfamyLand, 0),FounderTitle: ('models/gui/toplevel_gui', founderIcons, foundersScale, PLocalizer.FounderTitleName, PLocalizer.FounderTitleRanks, PLocalizer.FounderTitleDesc, FounderBreakpoints, None, 1)}

def isValidTitle(titleKey):
    titleData = TitlesDict.get(titleKey, None)
    if titleData:
        return True
    else:
        return False
    return


def isBooleanTitle(title):
    return TitlesDict[title][8]


def getScale(title):
    return TitlesDict[title][2]


def getBreakpoints(title):
    return TitlesDict[title][6]


def getInventoryType(title):
    inventoryTitleInfo = TitlesDict.get(title)
    if inventoryTitleInfo:
        return TitlesDict[title][7]
    return None


def getTitleName(title):
    return TitlesDict[title][3]


def getTitleRankName(title, exp):
    rank = getRank(title, exp)
    if not TitlesDict[title][4][rank]:
        return PLocalizer.NoTitle
    if isBooleanTitle(title):
        return TitlesDict[title][4][rank]
    return TitlesDict[title][4][rank] + ' (%s)' % rank


def getTitleDesc(title):
    return TitlesDict[title][5]


def getIconName(title, rank):
    titleAttr = TitlesDict[title]
    iconNames = titleAttr[1]
    return iconNames[rank]


def getIconList(title):
    return TitlesDict[title][1]


def getModelPath(title):
    return TitlesDict[title][0]


def getRank(title, expPoints):
    if not title:
        return 0
    titleAttr = TitlesDict[title]
    if not titleAttr:
        return 0
    breakpoints = titleAttr[6]
    if not breakpoints:
        return 0
    if title == FounderTitle:
        if expPoints:
            return 1
        else:
            return 0
    high = 0
    for testValue in breakpoints:
        if testValue > expPoints:
            return high - 1
        high += 1

    return high - 1


def getMaxRank(title):
    if not title:
        return 0
    titleAttr = TitlesDict[title]
    if not titleAttr:
        return 0
    breakpoints = titleAttr[6]
    if not breakpoints:
        return 0
    return len(breakpoints) - 1