from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class HolidayManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('HolidayManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)