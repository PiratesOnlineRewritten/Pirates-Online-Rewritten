from panda3d.core import ConfigVariableList
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.piratesbase import PiratesGlobals
from pirates.holiday import FleetHolidayGlobals
from pirates.holiday.FleetManagerAI import FleetManagerAI
from pirates.ai import HolidayGlobals
from pirates.ai.HolidayDates import HolidayDates
from pirates.invasion import InvasionGlobals
from pirates.invasion.DistributedInvasionPortRoyalAI import DistributedInvasionPortRoyalAI
from pirates.invasion.DistributedInvasionTortugaAI import DistributedInvasionTortugaAI
from pirates.invasion.DistributedInvasionDelFuegoAI import DistributedInvasionDelFuegoAI
import time
import random

class HolidayManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('HolidayManagerAI')
    notify.setInfo(True)

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.wantHolidays = config.GetBool('want-holidays', True)
        self.wantRandomizedSchedules = config.GetBool('want-randomized-schedules', True)

        self.activeHolidays = {}
        self.invasionManager = None
        self.fleetManager = None

        self.scheduleCounter = {}
        self.monthlyCounter = {}

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.notify.info('HolidayManager going online')
        self.attemptRegister()

    def delete(self):
        DistributedObjectAI.delete(self)
        self.unregisterAI()

    def attemptRegister(self):
        self.retryRegisterTask = taskMgr.doMethodLater(5, self.registerAI, '%s-retryTask' % self.__class__.__name__)

    def registerAI(self, task=None):
        self.notify.debug('Attempting to register channel.')
        self.sendUpdate('registerAI', [self.air.ourChannel])
        return Task.again

    def unregisterAI(self):
        self.notify.debug('Unregistering channel')
        self.sendUpdate('unregisterAI', [self.air.ourChannel])

    def registrationConfirm(self):
        self.notify.debug('Received registration Confirmation')
        if hasattr(self, 'retryRegisterTask'):
            taskMgr.remove(self.retryRegisterTask)
        self.d_requestHolidayList()

    def requestRegister(self):
        self.notify.debug('Received reregistration request!')
        self.attemptRegister()

    def d_requestHolidayList(self):
        self.notify.debug('Requesting Holiday list from UberDOG')
        self.sendUpdate('requestHolidayList', [])

    def isHolidayActive(self, holidayId):
        return holidayId in self.activeHolidays

    def startHoliday(self, holidayId, configId=0, time=0, manual=False):
        if self.isHolidayActive(holidayId) or not self.wantHolidays:
            return

        if not holidayId in HolidayGlobals.getAllHolidayIds() and configId == 0:
            self.notify.warning("Failed to start holiday. %s is an invalid holiday Id" % holidayId)
            return

        if configId != 0:
            holidayId = HolidayGlobals.getHolidayId(holidayId, configId)

        canStart = True
        if self.isInvasionHoliday(holidayId):
            canStart = self.startInvasionHoliday(holidayId)

        if self.isFleetHoliday(holidayId):
            canStart = self.startFleetHoliday(holidayId)

        if canStart:
            self.activeHolidays[holidayId] = (time, manual)
            self.air.newsManager.addHoliday(holidayId, time)

            self.notify.info('Starting holiday %s (%d)' % ((HolidayGlobals.getHolidayName(holidayId) or holidayId), holidayId))
            messenger.send('holidayActivated', [holidayId])

    def endHoliday(self, holidayId):
        if not self.isHolidayActive(holidayId):
            return

        self.notify.info('Ending holiday %s (%d)' % ((HolidayGlobals.getHolidayName(holidayId) or holidayId), holidayId))

        self.activeHolidays.pop(holidayId)
        self.air.newsManager.removeHoliday(holidayId)

        if self.isInvasionHoliday(holidayId):
            self.endInvasionHoliday(holidayId)

        if self.isFleetHoliday(holidayId):
            self.endFleetHoliday(holidayId)

        messenger.send('holidayDeactivated', [holidayId])

    def isInvasionHoliday(self, holidayId):
        return holidayId in InvasionGlobals.INVASION_NUMBERS

    def getActiveInvasion(self):
        return sorted([i if i in InvasionGlobals.INVASION_NUMBERS else None for i in self.activeHolidays.keys()], key=lambda x: (x is None, x))[0]

    def startInvasionHoliday(self, holidayId):
        if self.invasionManager != None:
            return False

        if holidayId not in InvasionGlobals.ISLAND_IDS:
            self.notify.warning('Invalid Invasion Id: %s; Id is not associated with an island!' % holidayId)
            return False

        locationId = InvasionGlobals.ISLAND_IDS[holidayId]
        if not hasattr(self.air, 'worldCreator'):
            self.notify.warning('Failed to start Invasion; World is not ready')
            return False

        instance = self.air.worldCreator.world
        island = instance.uidMgr.justGetMeMeObject(locationId)
        if not island:
            self.notify.warning('Failed to start Invasion; Location %s returned None' % locationId)
            return False

        invasionManager = None
        if holidayId == HolidayGlobals.INVASIONPORTROYAL:
            invasionManager = DistributedInvasionPortRoyalAI
        elif holidayId == HolidayGlobals.INVASIONTORTUGA:
            invasionManager = DistributedInvasionTortugaAI
        elif holidayId == HolidayGlobals.INVASIONDELFUEGO:
            invasionManager = DistributedInvasionDelFuegoAI
        else:
            self.notify.warning('Failed to start invasion; Invasion Manager not found')
            return False

        invasionManager = invasionManager(self.air, holidayId)
        invasionManager.generateWithRequired(PiratesGlobals.IslandLocalZone)
        self.invasionManager = invasionManager

        self.notify.info('Starting invasion on %s.' % island.getLocalizerName())

        return True

    def d_requestHolidayRemoval(self, holidayId):
        self.sendUpdate('requestHolidayRemoval', [holidayId])

    def endInvasionHoliday(self, holidayId):
        if self.invasionManager == None:
            return

        self.notify.info('Ending invasion.')
        self.invasionManager.delete()

    def isFleetHoliday(self, holidayId):
        return (holidayId / 100) is HolidayGlobals.FLEETHOLIDAY

    def startFleetHoliday(self, holidayId):
        if self.fleetManager:
            return

        self.fleetManager = FleetManagerAI(self.air, holidayId)
        self.fleetManager.start()

        self.notify.info('Starting Fleet Holiday (%d)' % holidayId)

    def endFleetHoliday(self, holidayId):
        if not self.fleetManager:
            return

        self.fleetManager.delete()
        self.fleetManager = None

        self.notify.info('Ending Fleet holiday')
