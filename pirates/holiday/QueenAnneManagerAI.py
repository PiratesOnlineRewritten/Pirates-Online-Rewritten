from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from direct.fsm.FSM import FSM
from pirates.holiday import FleetHolidayGlobals
from pirates.ai import HolidayGlobals
from pirates.ship import ShipGlobals
from pirates.world.LocationConstants import LocationIds
import random

class QueenAnneManagerAI(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('QueenAnneManagerAI')
    notify.setDebug(True)

    Locations = {
        LocationIds.ISLA_TORMENTA: 63,
        LocationIds.ISLA_PERDIDA: 64,
        LocationIds.ISLA_CANGREJOS: 65
    }

    def __init__(self, air):
        FSM.__init__(self, '%s-FSM' % self.__class__.__name__)
        self.air = air
        self.lifespan = config.GetInt('queen-anne-life-span', 10) * 60

    def delete(self):
        if hasattr(self, 'announceTask'):
            taskMgr.remove(self.announceTask)

        self.request('Disappeared')

    def start(self):
        self.request('Announce')

    def enterAnnounce(self):
        self.notify.debug('Announcing Queen Anne')
        self.announceTask = taskMgr.doMethodLater(random.randint(1, 2) * 60, self.__placeShip, '%s-place' % self.__class__.__name__)

    def __placeShip(self, task):
        self.notify.debug('Placing Queen Anne')

        placeLocation = random.choice(self.Locations.keys())
        self.air.newsManager.d_displayMessage(self.Locations[placeLocation])

        #TODO place ship

        self.request('Run')

        return task.done

    def exitAnnounce(self):
        taskMgr.remove(self.announceTask)
        del self.announceTask

    def enterRun(self):

        #TODO

        self.disppearTask = taskMgr.doMethodLater(self.lifespan, self.disappear, '%s-disappear-task' % self.__class__.__name__)

    def disappear(self):
        self.request('Disappeared')

    def exitRun(self):
        taskMgr.remove(self.disppearTask)
        del self.disppearTask

    def enterDisappeared(self):
        self.notify.debug('Queen Anne has vanished!')
        self.air.newsManager.d_displayMessage(61)
        self.air.holidayMgr.d_requestHolidayRemoval(HolidayGlobals.QUEENANNES)
        self.request('Exit')

    def enterExit(self):
        pass