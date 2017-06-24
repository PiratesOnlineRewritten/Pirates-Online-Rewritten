from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class SettingsMgrUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('SettingsMgrUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)