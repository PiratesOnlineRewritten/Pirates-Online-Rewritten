from pandac.PandaModules import *
from pirates.piratesbase.TODDefs import *
from pirates.piratesbase.TODData import *
from pirates.piratesbase import PiratesGlobals
import copy

StateDict = {
    PiratesGlobals.TOD_BASE: 'BASE', PiratesGlobals.TOD_DAWN: 'Dawn', PiratesGlobals.TOD_DAY: 'Day', PiratesGlobals.TOD_DUSK: 'Dusk', PiratesGlobals.TOD_NIGHT: 'Night', PiratesGlobals.TOD_STARS: 'Stars', PiratesGlobals.TOD_HALLOWEEN: 'Halloween', PiratesGlobals.TOD_FULLMOON: 'FullMoon', PiratesGlobals.TOD_HALFMOON: 'HalfMoon', PiratesGlobals.TOD_HALFMOON2: 'HalfMoon2', PiratesGlobals.TOD_JOLLYINVASION: 'Invasion'
}
NAME_TO_ID_DICT = {
    'BASE': PiratesGlobals.TOD_BASE,
    'Dawn': PiratesGlobals.TOD_DAWN,
    'Day': PiratesGlobals.TOD_DAY,
    'Dusk': PiratesGlobals.TOD_DUSK,
    'Night': PiratesGlobals.TOD_NIGHT,
    'Stars': PiratesGlobals.TOD_STARS,
    'Halloween': PiratesGlobals.TOD_HALLOWEEN,
    'FullMoon': PiratesGlobals.TOD_FULLMOON,
    'HalfMoon': PiratesGlobals.TOD_HALFMOON,
    'HalfMoon2': PiratesGlobals.TOD_HALFMOON2,
    'Invasion': PiratesGlobals.TOD_JOLLYINVASION
}
StateIdDict = {
    PiratesGlobals.TOD_BASE: 'TOD_BASE', PiratesGlobals.TOD_DAWN: 'TOD_DAWN', PiratesGlobals.TOD_DAY: 'TOD_DAY', PiratesGlobals.TOD_DUSK: 'TOD_DUSK', PiratesGlobals.TOD_NIGHT: 'TOD_NIGHT', PiratesGlobals.TOD_STARS: 'TOD_STARS', PiratesGlobals.TOD_HALLOWEEN: 'TOD_HALLOWEEN', PiratesGlobals.TOD_FULLMOON: 'TOD_FULLMOON', PiratesGlobals.TOD_HALFMOON: 'TOD_HALFMOON', PiratesGlobals.TOD_HALFMOON2: 'TOD_HALFMOON2', PiratesGlobals.TOD_JOLLYINVASION: 'TOD_JOLLYINVASION'
}
INORDER_TOD_LIST = [
    PiratesGlobals.TOD_BASE, PiratesGlobals.TOD_DAWN, PiratesGlobals.TOD_DAY, PiratesGlobals.TOD_DUSK, PiratesGlobals.TOD_NIGHT, PiratesGlobals.TOD_STARS, PiratesGlobals.TOD_HALLOWEEN, PiratesGlobals.TOD_FULLMOON, PiratesGlobals.TOD_HALFMOON, PiratesGlobals.TOD_HALFMOON2, PiratesGlobals.TOD_JOLLYINVASION
]

def reverseLookupTOD(v):
    for k in StateDict:
        if StateDict[k] == v:
            return k

    raise ValueError


MAX_TRANSITION_TIME = 300.0
NONGROUP_MAX_TRANSITION_TIME = 30.0
SHIP_FOG_MULT = 0.1
FOG_DEFAULT_EXP = 0.001
SKY_NAMES = {
    SKY_OFF: 'Off',
    SKY_DAWN: 'Dawn',
    SKY_DAY: 'Day',
    SKY_DUSK: 'Dusk',
    SKY_NIGHT: 'Night',
    SKY_STARS: 'Stars',
    SKY_HALLOWEEN: 'Halloween',
    SKY_SWAMP: 'Swamp',
    SKY_INVASION: 'Invasion',
    SKY_OVERCAST: 'Overcast',
    SKY_OVERCASTNIGHT: 'OvercastNight'
}
SKY_CLEARCOLORS = {
    SKY_OFF: Vec4(0, 0, 0, 1),
    SKY_DAWN: Vec4(0.72, 0.72, 0.52, 1),
    SKY_DAY: Vec4(0.4, 0.6, 0.85, 1),
    SKY_DUSK: Vec4(0.65, 0.55, 0.5, 1),
    SKY_NIGHT: Vec4(0.075, 0.13, 0.26, 1),
    SKY_STARS: Vec4(0.0225, 0.039, 0.078, 0.3),
    SKY_HALLOWEEN: Vec4(0.075, 0.05, 0.12, 1),
    SKY_SWAMP: Vec4(0.2, 0.25, 0.3, 1),
    SKY_INVASION: Vec4(0.1, 0.12, 0.04, 1),
    SKY_OVERCAST: Vec4(0.35, 0.36, 0.38, 1),
    SKY_OVERCASTNIGHT: Vec4(0.06, 0.11, 0.16, 1)
}
SunRotationStates = {
    PiratesGlobals.TOD_OFF: -1, PiratesGlobals.TOD_DAWN: 0, PiratesGlobals.TOD_DAY: 0, PiratesGlobals.TOD_DUSK: 0, PiratesGlobals.TOD_NIGHT: 0, PiratesGlobals.TOD_STARS: 0, PiratesGlobals.TOD_HALLOWEEN: 3, PiratesGlobals.TOD_FULLMOON: 3, PiratesGlobals.TOD_HALFMOON: 3, PiratesGlobals.TOD_HALFMOON2: 3, PiratesGlobals.TOD_JOLLYINVASION: 2, PiratesGlobals.TOD_CUSTOM: 4, PiratesGlobals.TOD_BASE: 4
}
TOD_JOLLY2CURSED_CYCLE = 7
StartingStates = {
    TOD_REGULAR_CYCLE: PiratesGlobals.TOD_DAY,
    TOD_HALLOWEEN_CYCLE: PiratesGlobals.TOD_HALLOWEEN,
    TOD_JOLLYCURSE_CYCLE: PiratesGlobals.TOD_HALFMOON
}
CycleStateTimeList = {
    TOD_ALL_CYCLE: [(PiratesGlobals.TOD_BASE, 2, 1), (PiratesGlobals.TOD_DAWN, 2, 1), (PiratesGlobals.TOD_DAY, 4, 1), (PiratesGlobals.TOD_DUSK, 2, 1), (PiratesGlobals.TOD_NIGHT, 2, 1), (PiratesGlobals.TOD_STARS, 2, 1), (PiratesGlobals.TOD_HALLOWEEN, 2, 1), (PiratesGlobals.TOD_HALFMOON, 2, 1), (PiratesGlobals.TOD_FULLMOON, 2, 1), (PiratesGlobals.TOD_HALFMOON2, 2, 1), (PiratesGlobals.TOD_JOLLYINVASION, 2, 1)],
    TOD_REGULAR_CYCLE: [(PiratesGlobals.TOD_STARS, 4, 1), (PiratesGlobals.TOD_DAWN, 5, 2), (PiratesGlobals.TOD_DAY, 7, 2), (PiratesGlobals.TOD_DUSK, 4, 2), (PiratesGlobals.TOD_NIGHT, 4, 1)],
    TOD_HALLOWEEN_CYCLE: [(PiratesGlobals.TOD_HALLOWEEN, 24, 1)],
    TOD_JOLLYCURSE_CYCLE: [(PiratesGlobals.TOD_HALFMOON, 0.05, 0.05), (PiratesGlobals.TOD_FULLMOON, 6.0, 1.95), (PiratesGlobals.TOD_HALFMOON2, 2, 2), (PiratesGlobals.TOD_HALLOWEEN, 15.95, 1)],
    TOD_JOLLYINVASION_CYCLE: [(PiratesGlobals.TOD_JOLLYINVASION, 24, 0.08)],
    TOD_VALENTINE_CYCLE: [(PiratesGlobals.TOD_DUSK, 24, 0.08)]
}
CYCLE_NAMES = {
    TOD_ALL_CYCLE: 'All',
    TOD_REGULAR_CYCLE: 'Day-Night',
    TOD_HALLOWEEN_CYCLE: 'Halloween',
    TOD_JOLLYCURSE_CYCLE: 'Curse',
    TOD_JOLLYINVASION_CYCLE: 'Invasion'
}
StateBreakdownList = {}
StateBeginTimeList = {}
StateTransitionTimeList = {}
NumStates = {}
cycles = CycleStateTimeList.keys()
for cycleKey in cycles:
    totalHours = 0.0
    StateBreakdownList[cycleKey] = {}
    StateBeginTimeList[cycleKey] = {}
    StateTransitionTimeList[cycleKey] = {}
    cycle = CycleStateTimeList.get(cycleKey)
    NumStates[cycleKey] = len(cycle)
    for state in cycle:
        StateBeginTimeList[cycleKey][state[0]] = totalHours / 24.0
        StateBreakdownList[cycleKey][state[0]] = state[1] / 24.0
        StateTransitionTimeList[cycleKey][state[0]] = state[2] / 24.0
        totalHours += state[1]

def getStateDatatAtTime(cycleId, timeInHours):
    cycle = CycleStateTimeList[cycleId]
    timeSpent = 0
    currentIndex = 0
    nextIndex = None
    previousIndex = None
    stateStartTime = None
    for stateIndex in range(len(cycle)):
        state = cycle[stateIndex]
        tod = state[0]
        time = state[1]
        transTime = state[2]
        if timeSpent <= timeInHours:
            currentIndex = stateIndex
            stateStartTime = timeSpent
        timeSpent += time

    nextIndex = (currentIndex + 1) % len(cycle)
    previousIndex = currentIndex - 1
    if previousIndex < 0:
        previousIndex = len(cycle) - 1
    return (
     previousIndex, currentIndex, nextIndex, stateStartTime)


def getStartingState(cycleId):
    return StartingStates.get(cycleId)


def getStateDuration(cycleId, stateId):
    return StateBreakdownList.get(cycleId).get(stateId)


def getStateBeginTime(cycleId, stateId):
    returnTime = StateBeginTimeList.get(cycleId).get(stateId)
    return returnTime


def getStateTransitionTime(cycleId, stateId):
    return StateTransitionTimeList.get(cycleId).get(stateId, 0.0)


def getNumStates(cycleId):
    return NumStates.get(cycleId)


def getStateName(stateId):
    return StateDict.get(stateId)


def getStateId(stateName):
    stateKeys = StateDict.keys()
    for stateId in stateKeys:
        if StateDict.get(stateId) == stateName:
            return stateId

    return None


def getNextStateId(cycleId, stateId):
    cycle = CycleStateTimeList.get(cycleId)
    numStates = NumStates.get(cycleId)
    for i in range(numStates - 1):
        if cycle[i][0] == stateId and i + 1 < numStates:
            return cycle[i + 1][0]

    return cycle[0][0]


def getLastStateId(cycleId, stateId):
    cycle = CycleStateTimeList.get(cycleId)
    numStates = NumStates.get(cycleId)
    for i in range(numStates):
        if cycle[i][0] == stateId and i < numStates:
            if i == 0:
                return cycle[numStates - 1][0]
            else:
                return cycle[i - 1][0]

    return cycle[0][0]


def isStateIdValid(cycleId, stateId):
    cycle = CycleStateTimeList.get(cycleId)
    for state in cycle:
        if state[0] == stateId:
            return True

    return False


ENVIRONMENT_NAMES = {
    ENV_DEFAULT: 'Default',
    ENV_OFF: 'Off',
    ENV_OPENSKY: 'OpenSky',
    ENV_SAILING: 'Sailing',
    ENV_FOREST: 'Jungle',
    ENV_SWAMP: 'Swamp',
    ENV_CAVE: 'Cave',
    ENV_INTERIOR: 'Interior',
    ENV_NO_HOLIDAY: 'NoHoliday',
    ENV_DATAFILE: '-DataOnly-'
}
ENVIRONMENT_NAMES_TO_ID = {
    'Default': ENV_DEFAULT,
    'Off': ENV_OFF,
    'OpenSky': ENV_OPENSKY,
    'Sailing': ENV_SAILING,
    'Jungle': ENV_FOREST,
    'Swamp': ENV_SWAMP,
    'Cave': ENV_CAVE,
    'Interior': ENV_INTERIOR,
    'NoHoliday': ENV_NO_HOLIDAY,
    '-DataOnly-': ENV_DATAFILE
}
ENVIRONMENT_ID_DICT = {
    ENV_DEFAULT: 'ENV_DEFAULT',
    ENV_DATAFILE: 'ENV_DATAFILE',
    ENV_OFF: 'ENV_OFF',
    ENV_FOREST: 'ENV_FOREST',
    ENV_SWAMP: 'ENV_SWAMP',
    ENV_CAVE: 'ENV_CAVE',
    ENV_INTERIOR: 'ENV_INTERIOR',
    ENV_OPENSKY: 'ENV_OPENSKY',
    ENV_NO_HOLIDAY: 'ENV_NO_HOLIDAY',
    ENV_SAILING: 'ENV_SAILING'
}
ENV_DEBUG_NAMES = {
    ENV_DEFAULT: 'Default',
    ENV_OFF: 'Off',
    ENV_OPENSKY: 'OpenSky',
    ENV_FOREST: 'Jungle',
    ENV_SWAMP: 'Swamp',
    ENV_CAVE: 'Cave',
    ENV_LAVACAVE: 'LavaCave',
    ENV_INTERIOR: 'Interior',
    ENV_AVATARCHOOSER: 'Chooser',
    ENV_SAILING: 'Sailing',
    ENV_CANNONGAME: 'Cannon',
    ENV_CLOUDY: 'Cloudy',
    ENV_INVASION: 'Invasion',
    ENV_HALLOWEEN: 'Halloween',
    ENV_VALENTINES: 'Valentines',
    ENV_CURSED_NIGHT: 'CursedNight',
    ENV_EVER_NIGHT: 'EverNight',
    ENV_NO_HOLIDAY: 'NoHoliday',
    ENV_SAINT_PATRICKS: 'SaintPatricks',
    ENV_DATAFILE: 'DataFile'
}

def computeLightColor(lightColor, ambientColor, lightSwitch=[1, 1, 1]):
    ambientOn = lightSwitch[1]
    if ambientOn:
        lightValues = lightColor - ambientColor
    else:
        lightValues = lightColor
    lightValues[3] = 1.0
    return lightValues


ON_ALPHA = Vec4(1, 1, 1, 1)
OFF_ALPHA = Vec4(1, 1, 1, 0)
TOD_ATTRIBUTES = [
    'Direction', 'LightSwitch', 'FrontColor', 'BackColor', 'AmbientColor', 'FogType', 'FogColor', 'FogExp', 'FogLinearRange', 'SkyType', 'StarColor', 'MoonSize', 'MoonOverlay', 'MoonPhase', 'SeaColor', 'SeaColorShader', 'SeaFactor', 'EnvEffect'
]
AREADATA_TO_SETTING = {
    'SunDirections': 'Direction',
    'DirectionalColors': 'FrontColor',
    'BacklightColors': 'BackColor',
    'AmbientColors': 'AmbientColor',
    'FogTypes': 'FogType',
    'FogColors': 'FogColor',
    'LinearFogRanges': 'FogLinearRange',
    'FogRanges': 'FogExp',
    'LightSwitches': 'LightSwitch',
    'SkyTypes': 'SkyType'
}
SETTING_TO_AREADATA = {
    'Direction': 'SunDirections',
    'FrontColor': 'DirectionalColors',
    'BackColor': 'BacklightColors',
    'AmbientColor': 'AmbientColors',
    'FogType': 'FogTypes',
    'FogColor': 'FogColors',
    'FogLinearRange': 'LinearFogRanges',
    'FogExp': 'FogRanges',
    'LightSwitch': 'LightSwitches',
    'SkyType': 'SkyTypes'
}
ENV_SETTINGS_AVATARCHOOSER = {
    'BASE': {
        'Direction': Vec3(260, 0, 15),
        'FrontColor': Vec4(0.9, 0.7, 0.8, 1),
        'BackColor': Vec4(0.6, 0.8, 1.2, 1),
        'AmbientColor': Vec4(0.5, 0.8, 1, 1),
        'FogColor': Vec4(0.15, 0.2, 0.35, 0),
        'FogExp': 0.002,
        'SkyType': SKY_NIGHT,
        'StarColor': Vec4(1, 1, 1, 0.25)
    }
}
ENV_SETTINGS_DICT = {
    ENV_DEFAULT: ENV_SETTINGS_DEFAULT,
    ENV_OPENSKY: ENV_SETTINGS_OPENSKY,
    ENV_SAILING: ENV_SETTINGS_SAILING,
    ENV_INTERIOR: ENV_SETTINGS_INTERIOR,
    ENV_FOREST: ENV_SETTINGS_FOREST,
    ENV_SWAMP: ENV_SETTINGS_SWAMP,
    ENV_CAVE: ENV_SETTINGS_CAVE,
    ENV_AVATARCHOOSER: ENV_SETTINGS_AVATARCHOOSER,
    ENV_CANNONGAME: ENV_SETTINGS_CANNONGAME,
    ENV_CLOUDY: ENV_SETTINGS_CLOUDY,
    ENV_NO_HOLIDAY: ENV_SETTINGS_NO_HOLIDAY,
    ENV_INVASION: ENV_SETTINGS_INVASION,
    ENV_HALLOWEEN: ENV_SETTINGS_HALLOWEEN,
    ENV_VALENTINES: ENV_SETTINGS_VALENTINES,
    ENV_CURSED_NIGHT: ENV_SETTINGS_CURSED_NIGHT,
    ENV_EVER_NIGHT: ENV_SETTINGS_EVER_NIGHT,
    ENV_SAINT_PATRICKS: ENV_SETTINGS_SAINT_PATRICKS,
    ENV_DATAFILE: {}
}
ENVIRONMENT_ID_SETTING_DICT = {
    ENV_DEFAULT: 'ENV_SETTINGS_DEFAULT',
    ENV_OPENSKY: 'ENV_SETTINGS_OPENSKY',
    ENV_SAILING: 'ENV_SETTINGS_SAILING',
    ENV_INTERIOR: 'ENV_SETTINGS_INTERIOR',
    ENV_FOREST: 'ENV_SETTINGS_FOREST',
    ENV_SWAMP: 'ENV_SETTINGS_SWAMP',
    ENV_CAVE: 'ENV_SETTINGS_CAVE',
    ENV_NO_HOLIDAY: 'ENV_SETTINGS_NO_HOLIDAY'
}
BACKUP_ENV_SETTINGS_DICT = {}

def copySettingsDict(source, destination):
    for envKey in source:
        destination[envKey] = {}
        env = source[envKey]
        for key in env:
            if key in TOD_ATTRIBUTES:
                destination[envKey][key] = source[envKey][key]
            else:
                destination[envKey][key] = {}
                settingsDict = source[envKey][key]
                for todkey in settingsDict:
                    if todkey in TOD_ATTRIBUTES:
                        destination[envKey][key][todkey] = settingsDict[todkey]


def restoreSettings():
    copySettingsDict(BACKUP_ENV_SETTINGS_DICT, ENV_SETTINGS_DICT)


def backupSettings():
    copySettingsDict(ENV_SETTINGS_DICT, BACKUP_ENV_SETTINGS_DICT)


backupSettings()

def getTodEnvSetting(timeOfDayId, environment, settingName):
    timeOfDay = StateDict.get(timeOfDayId)
    levelSetting = getEnvSetting(timeOfDay, ENV_DATAFILE, settingName)
    if levelSetting != None:
        return levelSetting
    environmentalSetting = getEnvSetting(timeOfDay, environment, settingName)
    if environmentalSetting != None:
        return environmentalSetting
    timeSetting = getEnvSetting(timeOfDay, ENV_DEFAULT, settingName, check=1)
    if timeSetting != None:
        return timeSetting
    return


def getEnvSetting(timeOfDay, environment, settingName, check=0):
    environmentSettings = ENV_SETTINGS_DICT.get(environment)
    if environmentSettings:
        timeSpecificEnvironmentSettings = environmentSettings.get(timeOfDay)
        if timeSpecificEnvironmentSettings:
            timeSpecificEnvironmentSetting = timeSpecificEnvironmentSettings.get(settingName)
            if timeSpecificEnvironmentSetting != None:
                return timeSpecificEnvironmentSetting
        evironmentalBase = environmentSettings.get('BASE')
        if evironmentalBase:
            environmentalSetting = evironmentalBase.get(settingName)
            if environmentalSetting != None:
                return environmentalSetting
    return


DefinedEnviros = (ENV_DEFAULT, ENV_FOREST, ENV_SWAMP, ENV_CAVE, ENV_LAVACAVE)

NOCLOUDS = 0
LIGHTCLOUDS = 1
MEDIUMCLOUDS = 2
HEAVYCLOUDS = 3
CLOUD_TRANSITIONS = {NOCLOUDS, LIGHTCLOUDS, MEDIUMCLOUDS, HEAVYCLOUDS}