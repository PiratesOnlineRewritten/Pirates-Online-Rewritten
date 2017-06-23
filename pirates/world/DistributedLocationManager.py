from direct.distributed.DistributedObject import DistributedObject
from pirates.piratesbase import PiratesGlobals
from pirates.world import WorldGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify

class DistributedLocationManager(DistributedObject):
    notify = directNotify.newCategory('LocationManager')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

    def delete(self):
        self.ignoreAll()
        self.notify.warning('LocationManager is going offline')
        self.cr.locationMgr = None
        DistributedObject.delete(self)
        return

    def online(self):
        pass

    def queryOcean(self):
        self.requestQueryLocation(WorldGlobals.OCEAN)

    def queryIsland(self):
        self.requestQueryLocation(WorldGlobals.ISLAND)

    def queryTown(self):
        self.requestQueryLocation(WorldGlobals.TOWN)

    def queryBuilding(self):
        self.requestQueryLocation(WorldGlobals.BUILDING)

    def queryPort(self):
        self.requestQueryLocation(WorldGlobals.PORT)

    def queryGameArea(self):
        self.requestQueryLocation(WorldGlobals.GAMEAREA)

    def queryShip(self):
        self.requestQueryLocation(WorldGlobals.SHIP)

    def queryLocation(self, category):
        self.sendUpdate('requestLocation', [category])