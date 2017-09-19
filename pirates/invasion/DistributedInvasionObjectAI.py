from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.fsm.FSM import FSM
from pirates.piratesbase import TODDefs
from pirates.invasion import InvasionGlobals

class DistributedInvasionObjectAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInvasionObjectAI')
    MESSAGES = {}

    def __init__(self, air, holidayId):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, '%s-FSM' % self.__class__.__name__)
        self.holidayId = holidayId
        self.devTimer = config.GetBool('want-invasion-dev-timer', False)
        self.timerSeconds = 2 if self.devTimer else 60
        self.currentPhase = 1

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.setInvasionSky()
        self.request('Countdown')

    def delete(self):
        self.resetSky()
        DistributedObjectAI.delete(self)
        if hasattr(self, 'countdownTask'):
            taskMgr.remove(self.countdownTask)

    def enterCountdown(self):
        self.notify.debug('Starting Invasion Countdown.')
        self.countdown = 1800
        self.__runCountdown()
        self.countdownTask = taskMgr.doMethodLater(self.timerSeconds, self.__runCountdown, '%s-countdown' % self.__class__.__name__)

    def __runCountdown(self, task=None):
        interval = self.countdown / 60
        self.countdown -= 60

        if interval not in self.MESSAGES:
            return Task.again

        messageId = self.MESSAGES[interval]
        self.air.newsManager.d_displayMessage(messageId)

        if self.countdown <= 0:
            self.request('Phase1')
            return Task.done

        return Task.again

    def exitCountdown(self):
        taskMgr.doMethodLater(self.timerSeconds, self.startInvasion, '%s-invasion-start-timer ' % self.__class__.__name__)

    def startInvasion(self, task):
        print('Starting Invasion with class %s' % self.__class__.__name__)
        
        #TEMP
        self.air.holidayMgr.d_requestHolidayRemoval(self.holidayId)

        #self.request('Phase1')

        return Task.done

    def d_setNextPhase(self, phase, message=1):
        self.sendUpdate('setNextPhase', [phase, message])

    def enterPhase1(self):
        self.currentPhase = 1
        self.d_setNextPhase(self.currentPhase)

    def setInvasionSky(self):
        self.air.timeOfDayMgr.d_changeCycle(TODDefs.TOD_JOLLYINVASION_CYCLE)
        self.air.timeOfDayMgr.d_setMoonJolly(True)

    def resetSky(self):
        self.air.timeOfDayMgr.d_changeCycle(TODDefs.TOD_REGULAR_CYCLE)
        self.air.timeOfDayMgr.d_setMoonJolly(False)    

    def d_hideShip(self):
        self.sendUpdate('hideShip', [])