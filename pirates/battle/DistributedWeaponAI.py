from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedWeaponAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWeaponAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)