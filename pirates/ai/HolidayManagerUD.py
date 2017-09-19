from panda3d.core import ConfigVariableList
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.ai import HolidayGlobals
from pirates.ai.HolidayDates import HolidayDates
import datetime
import random
import time

class HolidayManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('HolidayManagerUD')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        self.wantHolidays = config.GetBool('want-holidays', True)
        self.wantRandomizedSchedules = config.GetBool('want-randomized-schedules', True)

        self.districts = {}
        self.activeHolidays = {}

    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.notify.info('HolidayManager going online')

        self.__checkHolidays()
        self.holidayCheckTask = taskMgr.doMethodLater(15, self.__checkHolidays, 'checkHolidays')
        self.holdayTimerTask = taskMgr.doMethodLater(15, self.__runHolidayTimer, 'holidayTimerTask')

        if self.wantRandomizedSchedules:
            self.randomScheduleTask = taskMgr.doMethodLater(60, self.__runRandomizedSchedules, 'randomShceduleTask')

        self.d_requestRegister()

        # Load holidays from PRC
        if self.wantHolidays:
            debugHolidays = ConfigVariableList('debug-holiday')
            for holiday in debugHolidays:
                holidaySplit = holiday.split(';')

                holidayId = int(holidaySplit[0])
                endTime = int(holidaySplit[1])
                config = 0

                if len(holidaySplit) > 2:
                    config = int(holidaySplit[2])

                self.startHoliday(holidayId, configId=config, time=endTime)

    def delete(self):
        DistributedObjectGlobalUD.delete(self)

        taskMgr.remove(self.holidayCheckTask)
        taskMgr.remove(self.holidayTimerTask)

        if hasattr(self, 'randomScheduleTask'):
            taskMgr.remove(self.randomScheduleTask)

    def d_requestRegister(self):
        self.sendUpdate('requestRegister', [])

    def registerAI(self, channel):
        self.notify.debug('Received registration for channel: %s!' % channel)

        if channel in self.districts:
            self.notify.warning('Received register for already allocated channel!')
            self.d_registrationConfirm(channel)
            return

        self.districts[channel] = {
            'localHolidays': {},
            'dayCounters': {},
            'monthCounters': {},
            'scheduledRunning': None
        }
        self.d_registrationConfirm(channel)

    def unregisterAI(self, channel):
        self.notify.debug('Received unregister for channel: %s!' % channel)

        if channel not in self.districts:
            self.notify.warning('Received unregister for none allocated channel!')
            return

        del self.districts[channel]

    def d_registrationConfirm(self, channel):
        self.sendUpdateToChannel(channel, 'registrationConfirm', [])

    def requestHolidayList(self):
        channel = self.air.getMsgSender()
        for holiday in self.activeHolidays:
            time, manual = self.activeHolidays[holiday]
            self.sendUpdateToChannel(channel, 'startHoliday', [holiday, 0, time, manual])

        if channel in self.districts:
            districtData = self.districts[channel]
            for holiday in districtData['localHolidays']:
                time, manual = districtData['localHolidays'][holiday]
                self.sendUpdateToChannel(channel, 'startHoliday', [holiday, 0, time, manual])

    def isHolidayActive(self, holidayId, district=None):
        if not district:
            return holidayId in self.activeHolidays
        else:
            data = self.districts[district]
            return holidayId in data['localHolidays']

    def __checkHolidays(self, task=None):
        holidays = HolidayGlobals.getAllHolidayIds()

        for holidayId in holidays:
            date = HolidayGlobals.getHolidayDates(holidayId)
            currentTime = time.time()

            for index in range(len(date.startDates)):
                start = date.getStartTime(index)
                end = date.getEndTime(index)

                if currentTime >= start and currentTime <= end:
                    remaining = end - currentTime
                    self.startHoliday(holidayId, time=remaining)
                elif self.isHolidayActive(holidayId):
                    self.endHoliday(holidayId)

        return Task.again

    def startHoliday(self, holidayId, configId=0, time=0, manual=False, channel=None):
        if not channel:
            if self.isHolidayActive(holidayId):
                return

            self.activeHolidays[holidayId] = (time, manual)

            self.notify.info('Starting Holiday %s (%d)' %  ((HolidayGlobals.getHolidayName(holidayId) or holidayId), holidayId))
            self.sendUpdate('startHoliday', [holidayId, configId, time, manual])
        else:
            if self.isHolidayActive(holidayId, channel):
                return

            self.districts[channel]['localHolidays'][holidayId] = (time, manual)
            self.notify.info('Starting Holiday %s (%d) on %s' % ((HolidayGlobals.getHolidayName(holidayId) or holidayId), holidayId, channel))
            self.sendUpdateToChannel(channel, 'startHoliday', [holidayId, configId, time, manual])

    def endHoliday(self, holidayId, channel=None):
        if not channel:
            if not self.isHolidayActive(holidayId):
                return

            self.activeHolidays.pop(holidayId)

            self.notify.info('Ending Holiday %s (%d)' %  ((HolidayGlobals.getHolidayName(holidayId) or holidayId), holidayId))
            self.sendUpdate('endHoliday', [holidayId])
        else:
            if not self.isHolidayActive(holidayId, channel):
                return

            districtData = self.districts[channel]
            if districtData['scheduledRunning'] == holidayId:
                districtData['scheduledRunning'] = None

            self.notify.info('Ending Holiday %s (%d) on %s' % ((HolidayGlobals.getHolidayName(holidayId) or holidayId), holidayId, channel))
            self.sendUpdateToChannel(channel, 'endHoliday', [holidayId])

    def requestHolidayRemoval(self, holidayId):
        channel = self.air.getMsgSender()
        if channel not in self.districts:
            self.notify.warning('Received holiday removal request from unregistered channel: %s' % channel)
            return

        if not self.isHolidayActive(holidayId, channel):
            return

        self.endHoliday(holidayId, channel)

    def __runHolidayTimer(self, task=None):
        if len(self.activeHolidays) > 0:
            for holiday in self.activeHolidays.keys():
                time, manual = self.activeHolidays[holiday]
                time -= 15

                self.activeHolidays[holiday] = (time, manual)
                if time <= 0 and not manual:
                    self.endHoliday(holiday)

        if len(self.districts) > 0:
            for district in self.districts:
                districtData = self.districts[district]

                for holiday in districtData['localHolidays'].keys():
                    time, manual = districtData['localHolidays'][holiday]
                    time -= 15

                    districtData['localHolidays'][holiday] = (time, manual)
                    if time <= 0 and not manual:
                        self.endHoliday(holiday, channel=district)                

        return Task.again

    def __runRandomizedSchedules(self, task=None):

        if len(self.districts) == 0:
            return Task.again

        for district in self.districts:
            districtData = self.districts[district]

            for key in HolidayGlobals.RandomizedSchedules:
                data = HolidayGlobals.RandomizedSchedules[key]
                
                validConfig = True
                for ckey, default in data.get('configs', []):
                    if not config.GetBool(ckey, default):
                        validConfig = False

                if not validConfig:
                    continue

                conflictFound = False
                conflictHolidays = data.get('conflictingIds', [])
                for holidayId in conflictHolidays:
                    if self.isHolidayActive(holidayId) or self.isHolidayActive(holidayId, district):
                        conflictFound = True

                if conflictFound:
                    continue

                dayCounters = districtData['dayCounters']
                monthlyCounters = districtData['monthCounters']

                if key in dayCounters and dayCounters[key] >= data.get('numPerDay', 3):
                    continue

                if key in monthlyCounters and monthlyCounters[key]['counter'] >= monthlyCounters[key]['times']:
                    continue

                holidayIds = data.get('holidayIds', [])
                holidayId = random.choice(holidayIds)
                
                conflictFound = False
                for holiday in holidayIds:
                    if self.isHolidayActive(holiday, district):
                        conflictFound = True

                if conflictFound:
                    continue

                if districtData['scheduledRunning']:
                    continue

                windows = data.get('timeWindows', [])
                windowCheck = False
                for window in windows:
                    hour = datetime.datetime.now().hour
                    if hour in window:
                        windowCheck = True

                if not windowCheck:
                    continue

                if not config.GetBool('ignore-schedule-random-check', False):
                    rngCheck = random.randint(config.GetInt('schedule-random-min', 1), config.GetInt('schedule-random-max', 10))
                    if not rngCheck < config.GetInt('schedule-random-percent', 4):
                        continue

                startDuration, endDuration = data.get('duration', (1, 0))
                endDuration = endDuration * 60 if endDuration > 0 else 0

                self.startHoliday(holidayId, time=endDuration, manual=(endDuration <= 0), channel=district)

                if key in dayCounters:
                    dayCounters[key] += 1
                else:
                    dayCounters[key] = 1

                if key in monthlyCounters:
                    monthlyCounters[key]['counter'] += 1
                else:
                    monthlyCounters[key] = {
                        'times': random.randint(*data.get('daysPerMonth', (5, 8))),
                        'counter': 1
                    }

                districtData['scheduledRunning'] = holidayId

        return Task.again