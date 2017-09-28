from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.ai import HolidayGlobals
from pirates.piratesbase.TimeOfDayManagerBase import TimeOfDayManagerBase
from pirates.piratesbase import TODDefs
from pirates.piratesbase import TODGlobals
from pirates.piratesbase import PiratesGlobals
from direct.distributed.ClockDelta import globalClockDelta
import random

class DistributedTimeOfDayManagerAI(DistributedObjectAI, TimeOfDayManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTimeOfDayManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        TimeOfDayManagerBase.__init__(self)

        self.baseCycle = config.GetInt('tod-starting-cycle', TODDefs.TOD_REGULAR_CYCLE)
        self.cycleType = self.baseCycle
        self.cycleSpeed = config.GetInt('tod-cycle-speed', 1)
        self.startingNetTime = globalClockDelta.getRealNetworkTime(bits=32)
        self.timeOffset = 0
        self.isPaused = 0
        self.subList = []
        self.fromCurrent = 0
        self.startPhase = 0
        self.targetPhase = 0
        self.targetTime = 0
        self.isJolly = int(config.GetBool('start-moon-jolly', False))
        self.weatherTimeMin = config.GetInt('weather-time-min', 5) * 60
        self.weatherTimeMax = config.GetInt('weather-time-max', 10) * 60
        self.wantAdvancedWeather = config.GetBool('advanced-weather', False)
        self.weatherId = TODGlobals.WEATHER_NORMAL

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.cycleTask = taskMgr.doMethodLater(1, self.__runCycle, self.uniqueName('runCycle'))

        if self.wantAdvancedWeather:
            self.__processWeather()

        self.accept('holidayListChanged', self.holidayListChanged)

        self.startTodToggles()
        if config.GetBool('want-day-night-print', False):
            self.addTT()

        self.addTimeOfDayToggle('do-day-night', 8.0, 20.0, self.processDayStart, (), self.processNightStart, ())

    def delete(self):
        DistributedObjectAI.delete(self)
        self.togglesOn = 0
        taskMgr.remove('timeOfDayToggles')

    def processDayStart(self):
        messenger.send('day-start')

    def processNightStart(self):
        messenger.send('night-start')

    def delete(self):
        DistributedObjectAI.delete(self)
        taskMgr.remove(self.cycleTask)
        if hasattr(self, 'weatherTask'):
            taskMgr.remove(self.weatherTask)

        self.ignore('holidayListChanged')

    def holidayListChanged(self):

        if self.air.holidayMgr.getActiveInvasion():
            self.d_changeCycle(TODDefs.TOD_JOLLYINVASION_CYCLE)
            self.d_setMoonJolly(True)
            return
        elif self.air.holidayMgr.isHolidayActive(HolidayGlobals.JOLLYROGERCURSE) or self.air.holidayMgr.isHolidayActive(HolidayGlobals.JOLLYCURSEAUTO) and not self.getMoonJolly():
            self.d_setMoonJolly(True)
        elif self.getMoonJolly():
            self.d_setMoonJolly(False)

        found = False
        for holidayId in self.air.holidayMgr.activeHolidays:

            if holidayId == HolidayGlobals.HALLOWEEN:
                self.d_changeCycle(TODDefs.TOD_HALLOWEEN_CYCLE)
                found = True
            elif holidayId == HolidayGlobals.JOLLYROGERCURSE or holidayId == HolidayGlobals.JOLLYCURSEAUTO:
                self.d_changeCycle(TODDefs.TOD_JOLLYCURSE_CYCLE)
                found = True
            elif holidayId == HolidayGlobals.VALENTINESDAY:
                self.d_changeCycle(TODDefs.TOD_VALENTINE_CYCLE)
                found = True

        if not found:
            self.d_changeCycle(self.baseCycle)

    def __runCycle(self, task):
        if self.isPaused:
            return task.again

        REALSECONDS_PER_GAMEHOUR = PiratesGlobals.TOD_REALSECONDS_PER_GAMEDAY / self.cycleSpeed
        self.timeOffset += REALSECONDS_PER_GAMEHOUR 

        if self.getCurrentIngameTime() >= PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY:
            self.timeOffset = 0

        return task.again

    def syncTOD(self, cycleType, cycleSpeed, startingNetTime, timeOffset):
        self.cycleType = cycleType
        self.cycleSpeed = cycleSpeed
        self.startingNetTime = startingNetTime
        self.timeOffset = timeOffset

    def d_syncTOD(self, cycleType, cycleSpeed, startingNetTime, timeOffset):
        self.sendUpdate('syncTOD', [cycleType, cycleSpeed, startingNetTime, timeOffset])

    def b_syncTOD(self, cycleType, cycleSpeed, startingNetTime, timeOffset):
        self.syncTOD(cycleType, cycleSpeed, startingNetTime, timeOffset)
        self.d_syncTOD(cycleType, cycleSpeed, startingNetTime, timeOffset)

    def getSyncTOD(self):
        return [self.cycleType, self.cycleSpeed, self.startingNetTime, self.timeOffset]

    def d_changeCycle(self, cycleType):
        self.cycleType = cycleType
        self.d_syncTOD(self.cycleType, self.cycleSpeed, self.startingNetTime, self.timeOffset)

    def setIsPaused(self, isPaused):
        self.isPaused = isPaused

    def d_setIsPaused(self, isPaused):
        self.sendUpdate('setIsPaused', [isPaused])

    def b_setIsPaused(self, isPaused):
        self.setIsPaused(isPaused)
        self.d_setIsPaused(isPaused)

    def getIsPaused(self):
        return self.isPaused

    def requestSync(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        self.sendUpdateToAvatarId(avatar.doId, 'syncTOD', [self.cycleType, self.cycleSpeed, self.startingNetTime, self.timeOffset])

    def setEnvSubs(self, subList):
        self.subList = subList

    def d_setEnvSubs(self, subList):
        self.sendUpdate('setEnvSubs', [subList])

    def b_setEnvSubs(self, subList):
        self.setEnvSubs(subList)
        self.d_setEnvSubs(subList)

    def getEnvSubs(self):
        return self.subList

    def setMoonPhaseChange(self, fromCurrent, startPhase, targetPhase, targetTime):
        self.fromCurrent = fromCurrent
        self.startPhase = startPhase
        self.targetPhase = targetPhase
        self.targetTime = targetTime

    def d_setMoonPhaseChange(self, fromCurrent, startPhase, targetPhase, targetTime):
        self.sendUpdate('setMoonPhaseChange', [fromCurrent, startPhase, targetPhase, targetTime])

    def b_setMoonPhaseChange(self, fromCurrent, startPhase, targetPhase, targetTime):
        self.setMoonPhaseChange(fromCurrent, startPhase, targetPhase, targetTime)
        self.d_setMoonPhaseChange(fromCurrent, startPhase, targetPhase, targetTime)

    def getMoonPhaseChange(self):
        return [self.fromCurrent, self.startPhase, self.targetPhase, self.targetTime]

    def setMoonJolly(self, isJolly):
        self.isJolly = isJolly

    def d_setMoonJolly(self, isJolly):
        self.sendUpdate('setMoonJolly', [isJolly])

    def b_setMoonJolly(self, isJolly):
        self.setMoonJolly(isJolly)
        self.d_setMoonJolly(isJolly)

    def getMoonJolly(self):
        return self.isJolly

    def getCurrentIngameTime(self, time=None):
        cycleSpeed = self.cycleSpeed
        if cycleSpeed <= 0:
            cycleSpeed = 1

        if time is None:
            currentTime = globalClockDelta.networkToLocalTime(
                globalClockDelta.getFrameNetworkTime(bits=32))
        else:
            currentTime = time
       
        REALSECONDS_PER_GAMEDAY = PiratesGlobals.TOD_REALSECONDS_PER_GAMEDAY / cycleSpeed
        REALSECONDS_PER_GAMEHOUR = float(REALSECONDS_PER_GAMEDAY / PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY)
        cycleDuration = REALSECONDS_PER_GAMEHOUR * PiratesGlobals.TOD_GAMEHOURS_IN_GAMEDAY
        timeElapsed = currentTime - self.startingNetTime
        timeIntoCycle = (timeElapsed + self.timeOffset) % cycleDuration
        hoursIntoCycle = timeIntoCycle / REALSECONDS_PER_GAMEHOUR
        return hoursIntoCycle

    def __processWeather(self, task=None):

        weatherId = self.weatherId
        while weatherId == self.weatherId:
            weatherId = random.choice(TODGlobals.WEATHER_TYPES.keys())
        speed = random.randint(10, 15)

        valid = True
        definitions = TODGlobals.WEATHER_TYPES[weatherId]
        if 'configs' in definitions:
            configs = definitions['configs']
            for c in configs:
                if not config.GetBool(*c):
                    valid = False
                    break

        if valid:
            self.notify.debug('Setting Weather to %d with a transition time of %d' % (weatherId, speed))
            self.b_setWeather(weatherId, speed) 

        self.weatherTask = taskMgr.doMethodLater(random.randint(self.weatherTimeMin, self.weatherTimeMax) + speed, self.__processWeather, 'weatherTask')

        return Task.done

    def setWeather(self, weatherId, transitionTime=5.0):
        self.weatherId = weatherId
        messenger.send('weatherChanged', [weatherId, transitionTime])

    def d_setWeather(self, weatherId, transitionTime=5.0):
        self.sendUpdate('setWeather', [weatherId, transitionTime])

    def b_setWeather(self, weatherId, transitionTime=5.0):
        self.setWeather(weatherId, transitionTime)
        self.d_setWeather(weatherId, transitionTime)

    def getWeather(self):
        return [self.weatherId, 1]