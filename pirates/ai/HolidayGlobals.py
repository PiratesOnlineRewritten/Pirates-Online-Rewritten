from pirates.ai.HolidayDates import *
from pirates.holiday.FleetHolidayGlobals import Configs as FHConfigs
from pirates.holiday.FleetHolidayGlobals import FleetHolidayConfigs
from pirates.holiday.KrakenHolidayGlobals import KrakenHolidayConfigs
from pirates.holiday.CatalogHolidayGlobals import CatalogHolidayConfigs
from pirates.holiday.MessageHolidayGlobals import MessageHolidayConfigs
DOUBLEXPHOLIDAY = 1
BLACKJACKFRIDAY = 2
FREEHATWEEK = 3
FLIRTEMOTE = 4
SAINTPATRICKSDAY = 5
DOUBLEXPHOLIDAYPAID = 6
MOTHERSDAY = 7
FATHERSDAY = 9
FOURTHOFJULY = 10
HALFOFFCUSTOMIZATION = 11
ALLACCESSWEEKEND = 12
HALLOWEEN = 13
DOUBLEGOLDHOLIDAY = 14
DOUBLEGOLDHOLIDAYPAID = 15
JOLLYROGERCURSE = 16
FOUNDERSFEAST = 17
FREEITEMTHANKSGIVING = 18
CURSEDNIGHT = 19
JOLLYCURSEAUTO = 20
WINTERFESTIVAL = 21
NEWYEARS = 22
VALENTINESDAY = 23
ZOMBIEEMOTE = 24
INVASIONPORTROYAL = 25
WRECKEDGOVERNORSMANSION = 26
DOUBLECROSS = 27
INVASIONTORTUGA = 28
WRECKEDFAITHFULBRIDE = 29
INVASIONDELFUEGO = 30
WRECKEDDELFUEGOTOWN = 31
FLEETHOLIDAY = 32
MARDIGRAS = 33
FEASTOFSTRENGTH = 34
EITCMOBILIZATION = 35
NAVYMOBILIZATION = 36
SKELMOBILIZATION = 37
KRAKENHOLIDAY = 38
CATALOGHOLIDAY = 39
MESSAGEHOLIDAY = 40
APRILFOOLS = 41
QUEENANNES = 42
GETCONNNECTED = 43
DOUBLELOOTHOLIDAY = 44
HOLIDAYS_WITH_CATALOGS = [SAINTPATRICKSDAY, VALENTINESDAY, WINTERFESTIVAL, MARDIGRAS, HALLOWEEN, NEWYEARS, MOTHERSDAY, FATHERSDAY]

def getHolidayId(holidayClass, holidayConfig=None):
    holidayId = holidayClass
    if holidayConfig:
        holidayId = holidayClass * 100 + holidayConfig
    return holidayId


def getHolidayClass(holidayId):
    holidayClass = holidayId
    if holidayId >= 100:
        holidayClass = holidayId / 100
    return holidayClass


def getHolidayConfig(holidayId):
    if holidayId >= 100:
        holidayConfig = holidayId % 100
        if holidayConfig != 0:
            return holidayConfig
    return None


def getHolidayRestartable(holidayId):
    return holidayId not in [INVASIONPORTROYAL, INVASIONTORTUGA, INVASIONDELFUEGO]


def getHolidayConfigAttrDict(configDefs, attrName, defaultValue=None):
    attrDict = {}
    for key in configDefs.iterkeys():
        attrDict[key] = configDefs[key].get(attrName, defaultValue)

    return attrDict


def getHolidayConfigNameDict(className, configDefs):
    nameDict = getHolidayConfigAttrDict(configDefs, attrName='name')
    return nameDict


def getHolidayConfigDatesDict(configDefs):
    defaultDates = HolidayDates(HolidayDates.TYPE_CUSTOM, [])
    return getHolidayConfigAttrDict(configDefs, attrName='dates', defaultValue=defaultDates)


holidayNameDict = {DOUBLEGOLDHOLIDAY: 'DoubleGoldHolidayAll',DOUBLEGOLDHOLIDAYPAID: 'DoubleGoldHolidayPaid',DOUBLEXPHOLIDAY: 'DoubleXPHolidayAll',DOUBLEXPHOLIDAYPAID: 'DoubleXPHolidayPaid',FREEHATWEEK: 'FreeHatWeek',SAINTPATRICKSDAY: 'SaintPatricksDay',MOTHERSDAY: 'MothersDay',FATHERSDAY: 'FathersDay',FOURTHOFJULY: 'FourthOfJuly',HALFOFFCUSTOMIZATION: 'HalfOffCustomization',ALLACCESSWEEKEND: 'AllAccessWeekend',HALLOWEEN: 'Halloween',JOLLYROGERCURSE: 'JollyRogerCurse',FOUNDERSFEAST: 'FoundersFeast',FREEITEMTHANKSGIVING: 'FreeItemThanksgiving',CURSEDNIGHT: 'CursedNight',JOLLYCURSEAUTO: 'JollyCurseAuto',WINTERFESTIVAL: 'WinterFestival',NEWYEARS: 'NewYears',VALENTINESDAY: 'ValentinesDay',ZOMBIEEMOTE: 'ZombieEmote',INVASIONPORTROYAL: 'InvasionJollyRoger',WRECKEDGOVERNORSMANSION: 'WreckedGovernorsMansion',DOUBLECROSS: 'DoubleCross',INVASIONTORTUGA: 'InvasionTortuga',WRECKEDFAITHFULBRIDE: 'WreckedFaithfulBride',INVASIONDELFUEGO: 'InvasionDelFuego',WRECKEDDELFUEGOTOWN: 'WreckedDelFuegoTown',FLEETHOLIDAY: getHolidayConfigNameDict('FleetHoliday', FleetHolidayConfigs),MARDIGRAS: 'MardiGras',FEASTOFSTRENGTH: 'FeatsOfStrength',EITCMOBILIZATION: 'EITCMobilization',NAVYMOBILIZATION: 'NavyMobilization',SKELMOBILIZATION: 'SkeletonMobilization',KRAKENHOLIDAY: getHolidayConfigNameDict('KrakenHoliday', KrakenHolidayConfigs),CATALOGHOLIDAY: getHolidayConfigNameDict('CatalogHoliday', CatalogHolidayConfigs),MESSAGEHOLIDAY: getHolidayConfigNameDict('MessageHoliday', MessageHolidayConfigs),APRILFOOLS: 'AprilFools',QUEENANNES: 'QueenAnnesRevenge',GETCONNNECTED: 'GetConnected',DOUBLELOOTHOLIDAY: 'DoubleLoot'}
holidayClassNameDict = {FLEETHOLIDAY: 'FleetHoliday',KRAKENHOLIDAY: 'KrakenHoliday',CATALOGHOLIDAY: 'CatalogHoliday',MESSAGEHOLIDAY: 'MessageHoliday'}

def getAllHolidayIds():
    allHolidayIds = []
    for holidayClass in holidayNameDict.iterkeys():
        entry = holidayNameDict.get(holidayClass)
        if isinstance(entry, type({})):
            holidayConfigs = entry.keys()
            holidayConfigs.sort()
            for holidayConfig in holidayConfigs:
                allHolidayIds.append(getHolidayId(holidayClass, holidayConfig))

        else:
            allHolidayIds.append(getHolidayId(holidayClass, None))

    return allHolidayIds


def getAllHolidayNames():
    allHolidayNames = []
    for holidayName in holidayNameDict.values():
        if isinstance(holidayName, type({})):
            allHolidayNames.extend(holidayName.values())
        else:
            allHolidayNames.append(holidayName)

    return allHolidayNames


def getHolidayName(holidayId):
    holidayClass = getHolidayClass(holidayId)
    holidayConfig = getHolidayConfig(holidayId)
    holidayName = holidayNameDict.get(holidayClass)
    if holidayConfig:
        holidayName = holidayName.get(holidayConfig)
    return holidayName


def getHolidayIdFromName(holidayName):
    holidayName = holidayName.lower()
    for holidayClass in holidayNameDict.iterkeys():
        entry = holidayNameDict.get(holidayClass)
        if isinstance(entry, type({})):
            for holidayConfig in entry.iterkeys():
                if entry.get(holidayConfig).lower() == holidayName:
                    return getHolidayId(holidayClass, holidayConfig)

        elif entry.lower() == holidayName:
            return getHolidayId(holidayClass, None)

    return None


def getHolidayClassName(holidayClass):
    return holidayClassNameDict.get(holidayClass, holidayNameDict.get(holidayClass))


holidaySchedules = {
  DOUBLEGOLDHOLIDAY: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2008, Month.SEPTEMBER, 13, 12, 0, 0), (2008, Month.SEPTEMBER, 13, 15, 0, 0)]),
  DOUBLEGOLDHOLIDAYPAID: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2008, Month.SEPTEMBER, 14, 12, 0, 0), (2008, Month.SEPTEMBER, 14, 15, 0, 0)]),
  DOUBLEXPHOLIDAY: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2009, Month.DECEMBER, 19, 12, 0, 0), (2009, Month.DECEMBER, 19, 15, 0, 0)]),
  DOUBLEXPHOLIDAYPAID: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2009, Month.DECEMBER, 20, 12, 0, 0), (2009, Month.DECEMBER, 20, 15, 0, 0)]),
  DOUBLELOOTHOLIDAY: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2008, Month.SEPTEMBER, 13, 12, 0, 0), (2008, Month.SEPTEMBER, 13, 15, 0, 0)]),
  FREEHATWEEK: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2008, Month.FEBRUARY, 25, 0, 0, 0), (2008, Month.MARCH, 2, 0, 0, 0)]),
  SAINTPATRICKSDAY: HolidayDates(HolidayDates.TYPE_YEARLY, [
    (Month.MARCH, 2, 0, 0, 0), (Month.MARCH, 29, 0, 0, 0)]),
  APRILFOOLS: HolidayDates(HolidayDates.TYPE_YEARLY, [
    (Month.APRIL, 1, 0, 0, 0), (Month.APRIL, 2, 12, 0, 0)]),
  MOTHERSDAY: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2009, Month.MAY, 6, 0, 0, 0), (2009, Month.MAY, 11, 0, 0, 0)]),
  QUEENANNES: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2011, Month.MAY, 16, 0, 0, 0), (2011, Month.JUNE, 16, 0, 0, 0)]),
  FATHERSDAY: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2009, Month.JUNE, 17, 0, 0, 0), (2009, Month.JUNE, 22, 0, 0, 0)]),
  FOURTHOFJULY: HolidayDates(HolidayDates.TYPE_YEARLY, [
    (Month.JULY, 3, 18, 0, 0), (Month.JULY, 7, 0, 0, 0)]),
  GETCONNNECTED: HolidayDates(HolidayDates.TYPE_YEARLY, [
    (Month.JULY, 1, 0, 0, 0), (Month.AUGUST, 7, 12, 0, 0)]),
  HALFOFFCUSTOMIZATION: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2008, Month.AUGUST, 14, 0, 0, 0), (2008, Month.AUGUST, 18, 12, 0, 0)]),
  ALLACCESSWEEKEND: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2009, Month.APRIL, 17, 0, 0, 0), (2009, Month.APRIL, 20, 0, 0, 0)]),
  HALLOWEEN: HolidayDates(HolidayDates.TYPE_YEARLY, [
    (Month.OCTOBER, 15, 0, 0, 0), (Month.OCTOBER, 31, 0, 0, 0)]),
  JOLLYROGERCURSE: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2010, Month.OCTOBER, 15, 16, 0, 0), (2010, Month.OCTOBER, 15, 16, 30, 0),
    (2010, Month.OCTOBER, 15, 18, 0, 0), (2010, Month.OCTOBER, 15, 18, 30, 0), 
    (2010, Month.OCTOBER, 15, 20, 0, 0), (2010, Month.OCTOBER, 15, 20, 30, 0), 
    (2010, Month.OCTOBER, 15, 22, 0, 0), (2010, Month.OCTOBER, 15, 22, 30, 0), 
    (2010, Month.OCTOBER, 16, 12, 0, 0), (2010, Month.OCTOBER, 16, 12, 30, 0), 
    (2010, Month.OCTOBER, 16, 15, 0, 0), (2010, Month.OCTOBER, 16, 15, 30, 0), 
    (2010, Month.OCTOBER, 16, 17, 0, 0), (2010, Month.OCTOBER, 16, 17, 30, 0), 
    (2010, Month.OCTOBER, 16, 19, 0, 0), (2010, Month.OCTOBER, 16, 19, 30, 0), 
    (2010, Month.OCTOBER, 17, 11, 0, 0), (2010, Month.OCTOBER, 17, 11, 30, 0), 
    (2010, Month.OCTOBER, 17, 14, 0, 0), (2010, Month.OCTOBER, 17, 14, 30, 0), 
    (2010, Month.OCTOBER, 17, 16, 0, 0), (2010, Month.OCTOBER, 17, 16, 30, 0), 
    (2010, Month.OCTOBER, 17, 18, 0, 0), (2010, Month.OCTOBER, 17, 18, 30, 0), 
    (2010, Month.OCTOBER, 18, 14, 35, 0), (2010, Month.OCTOBER, 18, 15, 20, 0), 
    (2010, Month.OCTOBER, 18, 16, 35, 0), (2010, Month.OCTOBER, 18, 17, 20, 0), 
    (2010, Month.OCTOBER, 18, 18, 35, 0), (2010, Month.OCTOBER, 18, 19, 20, 0), 
    (2010, Month.OCTOBER, 19, 15, 35, 0), (2010, Month.OCTOBER, 19, 16, 20, 0), 
    (2010, Month.OCTOBER, 19, 17, 35, 0), (2010, Month.OCTOBER, 19, 18, 20, 0), 
    (2010, Month.OCTOBER, 19, 19, 35, 0), (2010, Month.OCTOBER, 19, 20, 20, 0), 
    (2010, Month.OCTOBER, 20, 17, 35, 0), (2010, Month.OCTOBER, 20, 18, 20, 0), 
    (2010, Month.OCTOBER, 20, 19, 35, 0), (2010, Month.OCTOBER, 20, 20, 20, 0), 
    (2010, Month.OCTOBER, 20, 21, 35, 0), (2010, Month.OCTOBER, 20, 22, 20, 0), 
    (2010, Month.OCTOBER, 21, 14, 35, 0), (2010, Month.OCTOBER, 21, 15, 20, 0), 
    (2010, Month.OCTOBER, 21, 16, 35, 0), (2010, Month.OCTOBER, 21, 17, 20, 0), 
    (2010, Month.OCTOBER, 21, 18, 35, 0), (2010, Month.OCTOBER, 21, 19, 20, 0), 
    (2010, Month.OCTOBER, 22, 15, 35, 0), (2010, Month.OCTOBER, 22, 16, 20, 0), 
    (2010, Month.OCTOBER, 22, 17, 35, 0), (2010, Month.OCTOBER, 22, 18, 20, 0), 
    (2010, Month.OCTOBER, 22, 19, 35, 0), (2010, Month.OCTOBER, 22, 20, 20, 0), 
    (2010, Month.OCTOBER, 22, 21, 35, 0), (2010, Month.OCTOBER, 22, 22, 20, 0), 
    (2010, Month.OCTOBER, 23, 10, 35, 0), (2010, Month.OCTOBER, 23, 11, 20, 0), 
    (2010, Month.OCTOBER, 23, 13, 35, 0), (2010, Month.OCTOBER, 23, 14, 20, 0), 
    (2010, Month.OCTOBER, 23, 16, 35, 0), (2010, Month.OCTOBER, 23, 17, 20, 0), 
    (2010, Month.OCTOBER, 23, 19, 35, 0), (2010, Month.OCTOBER, 23, 20, 20, 0), 
    (2010, Month.OCTOBER, 24, 11, 35, 0), (2010, Month.OCTOBER, 24, 12, 20, 0), 
    (2010, Month.OCTOBER, 24, 13, 35, 0), (2010, Month.OCTOBER, 24, 14, 20, 0), 
    (2010, Month.OCTOBER, 24, 15, 35, 0), (2010, Month.OCTOBER, 24, 16, 20, 0), 
    (2010, Month.OCTOBER, 24, 18, 35, 0), (2010, Month.OCTOBER, 24, 19, 20, 0), 
    (2010, Month.OCTOBER, 25, 15, 35, 0), (2010, Month.OCTOBER, 25, 16, 20, 0), 
    (2010, Month.OCTOBER, 25, 17, 35, 0), (2010, Month.OCTOBER, 25, 18, 20, 0), 
    (2010, Month.OCTOBER, 25, 19, 35, 0), (2010, Month.OCTOBER, 25, 20, 20, 0), 
    (2010, Month.OCTOBER, 26, 13, 35, 0), (2010, Month.OCTOBER, 26, 14, 20, 0), 
    (2010, Month.OCTOBER, 26, 16, 35, 0), (2010, Month.OCTOBER, 26, 17, 20, 0), 
    (2010, Month.OCTOBER, 26, 18, 35, 0), (2010, Month.OCTOBER, 26, 19, 20, 0), 
    (2010, Month.OCTOBER, 27, 15, 35, 0), (2010, Month.OCTOBER, 27, 16, 20, 0), 
    (2010, Month.OCTOBER, 27, 17, 35, 0), (2010, Month.OCTOBER, 27, 18, 20, 0), 
    (2010, Month.OCTOBER, 27, 19, 35, 0), (2010, Month.OCTOBER, 27, 20, 20, 0), 
    (2010, Month.OCTOBER, 28, 14, 35, 0), (2010, Month.OCTOBER, 28, 15, 20, 0), 
    (2010, Month.OCTOBER, 28, 16, 35, 0), (2010, Month.OCTOBER, 28, 17, 20, 0), 
    (2010, Month.OCTOBER, 28, 18, 35, 0), (2010, Month.OCTOBER, 28, 19, 20, 0), 
    (2010, Month.OCTOBER, 29, 14, 35, 0), (2010, Month.OCTOBER, 29, 15, 20, 0), 
    (2010, Month.OCTOBER, 29, 16, 35, 0), (2010, Month.OCTOBER, 29, 17, 20, 0), 
    (2010, Month.OCTOBER, 29, 19, 35, 0), (2010, Month.OCTOBER, 29, 20, 20, 0), 
    (2010, Month.OCTOBER, 29, 21, 35, 0), (2010, Month.OCTOBER, 29, 22, 20, 0), 
    (2010, Month.OCTOBER, 30, 11, 35, 0), (2010, Month.OCTOBER, 30, 12, 20, 0), 
    (2010, Month.OCTOBER, 30, 14, 35, 0), (2010, Month.OCTOBER, 30, 15, 20, 0), 
    (2010, Month.OCTOBER, 30, 16, 35, 0), (2010, Month.OCTOBER, 30, 17, 20, 0), 
    (2010, Month.OCTOBER, 30, 18, 35, 0), (2010, Month.OCTOBER, 30, 19, 20, 0), 
    (2010, Month.OCTOBER, 30, 20, 35, 0), (2010, Month.OCTOBER, 30, 21, 20, 0), 
    (2010, Month.OCTOBER, 31, 11, 35, 0), (2010, Month.OCTOBER, 31, 12, 20, 0), 
    (2010, Month.OCTOBER, 31, 13, 35, 0), (2010, Month.OCTOBER, 31, 14, 20, 0), 
    (2010, Month.OCTOBER, 31, 15, 35, 0), (2010, Month.OCTOBER, 31, 16, 20, 0), 
    (2010, Month.OCTOBER, 31, 17, 35, 0), (2010, Month.OCTOBER, 31, 18, 20, 0), 
    (2010, Month.OCTOBER, 31, 19, 35, 0), (2010, Month.OCTOBER, 31, 20, 20, 0)]),
  FOUNDERSFEAST: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2009, Month.NOVEMBER, 21, 0, 0, 0), (2009, Month.NOVEMBER, 30, 0, 0, 0)]),
  FREEITEMTHANKSGIVING: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2008, Month.NOVEMBER, 27, 3, 0, 0), (2008, Month.DECEMBER, 8, 0, 0, 0)]),
  CURSEDNIGHT: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2009, Month.OCTOBER, 12, 0, 0, 0), (2009, Month.NOVEMBER, 2, 0, 0, 0)]),
  JOLLYCURSEAUTO: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2008, Month.DECEMBER, 12, 12, 0, 0), (2008, Month.DECEMBER, 15, 4, 0, 0), 
    (2008, Month.DECEMBER, 19, 12, 0, 0), (2008, Month.DECEMBER, 22, 4, 0, 0)]),
  WINTERFESTIVAL: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2009, Month.DECEMBER, 17, 0, 0, 0), (2010, Month.JANUARY, 2, 0, 0, 0)]),
  NEWYEARS: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2009, Month.DECEMBER, 31, 0, 0, 0), (2010, Month.JANUARY, 2, 0, 0, 0)]),
  VALENTINESDAY: HolidayDates(HolidayDates.TYPE_YEARLY, [
    (Month.FEBRUARY, 10, 0, 0, 0), (Month.FEBRUARY, 17, 0, 0, 0)]),
  ZOMBIEEMOTE: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2010, Month.OCTOBER, 1, 0, 0, 0), (2010, Month.NOVEMBER, 7, 0, 0, 0)]),
  INVASIONPORTROYAL: HolidayDates(HolidayDates.TYPE_CUSTOM, []),
  WRECKEDGOVERNORSMANSION: HolidayDates(HolidayDates.TYPE_CUSTOM, []),
  INVASIONTORTUGA: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2009, Month.DECEMBER, 11, 14, 0, 0), (2009, Month.DECEMBER, 11, 15, 45, 0), 
    (2009, Month.DECEMBER, 11, 16, 0, 0), (2009, Month.DECEMBER, 11, 17, 45, 0), 
    (2009, Month.DECEMBER, 11, 19, 0, 0), (2009, Month.DECEMBER, 11, 20, 45, 0), 
    (2009, Month.DECEMBER, 12, 12, 0, 0), (2009, Month.DECEMBER, 12, 13, 45, 0), 
    (2009, Month.DECEMBER, 12, 15, 0, 0), (2009, Month.DECEMBER, 12, 16, 45, 0), 
    (2009, Month.DECEMBER, 12, 18, 0, 0), (2009, Month.DECEMBER, 12, 19, 45, 0), 
    (2009, Month.DECEMBER, 13, 13, 0, 0), (2009, Month.DECEMBER, 13, 14, 45, 0), 
    (2009, Month.DECEMBER, 13, 17, 0, 0), (2009, Month.DECEMBER, 13, 18, 45, 0), 
    (2009, Month.DECEMBER, 13, 20, 0, 0), (2009, Month.DECEMBER, 13, 21, 45, 0)]),
  WRECKEDFAITHFULBRIDE: HolidayDates(HolidayDates.TYPE_CUSTOM, []),
  INVASIONDELFUEGO: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2010, Month.JANUARY, 21, 12, 0, 0), (2010, Month.JANUARY, 21, 13, 45, 0), 
    (2010, Month.JANUARY, 21, 15, 0, 0), (2010, Month.JANUARY, 21, 16, 45, 0), 
    (2010, Month.JANUARY, 21, 18, 0, 0), (2010, Month.JANUARY, 21, 19, 45, 0)]),
  WRECKEDDELFUEGOTOWN: HolidayDates(HolidayDates.TYPE_CUSTOM, []),
  FLEETHOLIDAY: getHolidayConfigDatesDict(FleetHolidayConfigs),
  DOUBLECROSS: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2010, Month.FEBRUARY, 26, 0, 0, 0), (2010, Month.MARCH, 26, 0, 0, 0)]),
  MARDIGRAS: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2010, Month.FEBRUARY, 11, 0, 0, 0), (2010, Month.FEBRUARY, 17, 0, 0, 0)]),
  FEASTOFSTRENGTH: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2010, Month.JANUARY, 23, 0, 0, 0), (2010, Month.JANUARY, 25, 0, 0, 0), 
    (2010, Month.JANUARY, 30, 0, 0, 0), (2010, Month.FEBRUARY, 1, 0, 0, 0)]),
   EITCMOBILIZATION: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2010, Month.MARCH, 5, 0, 0, 0), (2010, Month.MARCH, 8, 0, 0, 0)]),
   NAVYMOBILIZATION: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2010, Month.JANUARY, 2, 0, 0, 0), (2010, Month.JANUARY, 2, 0, 0, 0)]),
   SKELMOBILIZATION: HolidayDates(HolidayDates.TYPE_CUSTOM, [
    (2010, Month.OCTOBER, 22, 0, 0, 0), (2010, Month.NOVEMBER, 1, 0, 0, 0)]),
   KRAKENHOLIDAY: getHolidayConfigDatesDict(KrakenHolidayConfigs),
   CATALOGHOLIDAY: getHolidayConfigDatesDict(CatalogHolidayConfigs),
   MESSAGEHOLIDAY: getHolidayConfigDatesDict(MessageHolidayConfigs)}
holidaysEnglish = {}
holidaysJapanese = {}
holidaysGerman = {}
holidaysFrench = {}

def getHolidayDates(holidayId):
    holidayClass = getHolidayClass(holidayId)
    holidayConfig = getHolidayConfig(holidayId)
    holidayDates = holidaySchedules.get(holidayClass)
    if holidayConfig:
        holidayDates = holidayDates.get(holidayConfig)
    return holidayDates


class RandomTimeWindows():
    E = [12, 13, 14]
    F = [15, 16, 17]
    G = [18, 19, 20]
    H = [21, 22, 23]


RandomizedSchedules = {
    'Invasions': {
        'configs': [('want-random-invasions', 1), ('use-path-finding', 0)],
        'holidayIds': [INVASIONPORTROYAL, INVASIONTORTUGA, INVASIONDELFUEGO],
        'idOverrideDates': {
            INVASIONPORTROYAL: [((2010, 2, 4), (2010, 2, 28)), ((2010, 5, 1), (2010, 5, 31))],
            INVASIONTORTUGA: [((2010, 3, 1), (2010, 3, 31)), ((2010, 6, 1), (2010, 6, 30))],
            INVASIONDELFUEGO: [((2010, 4, 1), (2010, 4, 30)), ((2010, 7, 1), (2010, 7, 31))]
        },
        'conflictingIds': [CURSEDNIGHT],
        'conflictingClasses': [],
        'conflictingRSIds': [],
        'daysPerMonth': (5, 8),
        'numPerDay': 3,
        'timeWindows': [RandomTimeWindows.E, RandomTimeWindows.F, RandomTimeWindows.G],
        'duration': (1, 45)
    },
    'TreasureFleets': {
        'configs': [('want-random-treasurefleets', 1)],
        'holidayIds': [getHolidayId(FLEETHOLIDAY, FHConfigs.TF_EITC_RAND_KH_P_E_SW_S_W), getHolidayId(FLEETHOLIDAY, FHConfigs.TF_NAVY_RAND_KH_P_E_SW_S_W)],
        'idOverrideDates': {
            getHolidayId(FLEETHOLIDAY, FHConfigs.TF_EITC_RAND_KH_P_E_SW_S_W): [((2010, 1, 1), (2010, 4, 30))]
        },
        'conflictingIds': [CURSEDNIGHT],
        'conflictingClasses': [],
        'conflictingRSIds': [],
        'daysPerMonth': (5, 8),
        'numPerDay': 3,
        'timeWindows': [RandomTimeWindows.E, RandomTimeWindows.F, RandomTimeWindows.G, RandomTimeWindows.H],
        'duration': (1, 0)
    }
}
MSG_START_ALL = 0
MSG_START_UNLIMITED = 1
MSG_START_BASIC = 2
MSG_END_ALL = 3
MSG_END_UNLIMITED = 4
MSG_END_BASIC = 5
MSG_CHAT_STATUS = 6
MSG_ICON = 7
MSG_CHAT_STATUS_BASIC = 8
MSG_CHAT_STATUS_UNLIMITED = 9
MSG_BONFIRE = 10
MSG_PIG = 11
MSG_BONFIRE_STARTED = 12
MSG_PORK_RECEIVED = 13

def getHolidayMsgs(holidayId):
    from pirates.piratesbase.PLocalizer import holidayMessages
    holidayClass = getHolidayClass(holidayId)
    holidayConfig = getHolidayConfig(holidayId)
    holidayMsgs = holidayMessages.get(holidayClass)
    if holidayMsgs and holidayConfig:
        holidayMsgs = holidayMsgs.get(holidayConfig, holidayMsgs.get(None))
    return holidayMsgs


def getHolidayStartMsg(holidayId, paidStatus, chat=0):
    holidayMsgs = getHolidayMsgs(holidayId)
    if holidayMsgs:
        if holidayMsgs.has_key(MSG_START_ALL):
            return holidayMsgs.get(MSG_START_ALL)[chat]
        elif holidayMsgs.has_key(MSG_START_UNLIMITED) and paidStatus:
            return holidayMsgs.get(MSG_START_UNLIMITED)[chat]
        elif holidayMsgs.has_key(MSG_START_BASIC) and not paidStatus:
            return holidayMsgs.get(MSG_START_BASIC)[chat]
    return None


def getHolidayStartChatMsg(holidayId, paidStatus):
    return getHolidayStartMsg(holidayId, paidStatus, chat=1)


def getHolidayEndMsg(holidayId, paidStatus, chat=0):
    holidayMsgs = getHolidayMsgs(holidayId)
    if holidayMsgs:
        if holidayMsgs.has_key(MSG_END_ALL):
            return holidayMsgs.get(MSG_END_ALL)[chat]
        elif holidayMsgs.has_key(MSG_END_UNLIMITED) and paidStatus:
            return holidayMsgs.get(MSG_END_UNLIMITED)[chat]
        elif holidayMsgs.has_key(MSG_END_BASIC) and not paidStatus:
            return holidayMsgs.get(MSG_END_BASIC)[chat]
    return None


def getHolidayEndChatMsg(holidayId, paidStatus):
    return getHolidayEndMsg(holidayId, paidStatus, chat=1)


def getHolidayStatusMsg(holidayId, paidStatus):
    holidayMsgs = getHolidayMsgs(holidayId)
    if holidayMsgs:
        if holidayMsgs.has_key(MSG_CHAT_STATUS):
            return holidayMsgs.get(MSG_CHAT_STATUS)
        elif holidayMsgs.has_key(MSG_CHAT_STATUS_UNLIMITED) and paidStatus:
            return holidayMsgs.get(MSG_CHAT_STATUS_UNLIMITED)
        elif holidayMsgs.has_key(MSG_CHAT_STATUS_BASIC) and not paidStatus:
            return holidayMsgs.get(MSG_CHAT_STATUS_BASIC)
    return None


def getHolidayIcon(holidayId):
    holidayMsgs = getHolidayMsgs(holidayId)
    if holidayMsgs:
        if holidayMsgs.has_key(MSG_ICON):
            return holidayMsgs.get(MSG_ICON)
    return None