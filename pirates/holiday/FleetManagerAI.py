from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.fsm.FSM import FSM
from pirates.holiday import FleetHolidayGlobals
from pirates.ai import HolidayGlobals
from pirates.ship import ShipGlobals

class FleetManagerAI(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('FleetManagerAI')
    EITC_MSG = {
        10: FleetHolidayGlobals.Msgs.TF_EitcWarn10min,
        5: FleetHolidayGlobals.Msgs.TF_EitcWarn5min
    }

    NAVY_MSG = {
        10: FleetHolidayGlobals.Msgs.TF_NavyWarn10min,
        5: FleetHolidayGlobals.Msgs.TF_NavyWarn5min
    }

    def __init__(self, air, holidayId):
        FSM.__init__(self, '%s-FSM' % self.__class__.__name__)
        self.air = air
        self.holidayId = holidayId
        self.configId = HolidayGlobals.getHolidayConfig(holidayId)
        self.configData = FleetHolidayGlobals.FleetHolidayConfigs[self.configId]
        self.devTimer = config.GetBool('want-fleet-dev-timer', False)
        self.timerSeconds = 10 if self.devTimer else 60

    def delete(self):
        self.request('exit')

    def start(self):
        self.request('Countdown')

    def enterCountdown(self):
        self.notify.debug('Starting Fleet Countdown')
        self.countdown = 600
        self.__runCountdown()
        self.countdownTask = taskMgr.doMethodLater(self.timerSeconds, self.__runCountdown, '%s-countdown' % self.__class__.__name__)

    def __runCountdown(self, task=None):
        interval = self.countdown / 60
        self.countdown -= 60

        if self.configData['team'] == ShipGlobals.TRADING_CO_TEAM:
            messages = self.EITC_MSG
        else:
            messages = self.NAVY_MSG

        if interval not in messages:
            return Task.again

        messageId = messages[interval]
        self.air.newsManager.d_displayMessage(messageId)

        if self.countdown < 0:
            self.request('Launch')
            return Task.done

        return Task.again

    def exitCountdown(self):
        taskMgr.remove(self.countdownTask)

    def enterLaunch(self):
        self.notify.debug('Launching Treasure Fleet')

        self.air.newsManager.d_displayMessage(self.configData['launchMsg'])

        #TEMP
        self.air.holidayMgr.d_requestHolidayRemoval(self.holidayId)

    def enterExit(self):
        pass