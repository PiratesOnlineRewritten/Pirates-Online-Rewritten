from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class PiratesSettingsMgrUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesSettingsMgrUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)