from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from cPickle import loads, dumps
from pirates.uberdog.UberDogGlobals import *

class DistributedShipLoader(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipLoader')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.ships = {}
        self.notify.warning('ShipLoader going online')

    def delete(self):
        self.ignoreAll()
        self.notify.warning('ShipLoader going offline')
        self.cr.shipLoader = None
        DistributedObject.DistributedObject.delete(self)
        return