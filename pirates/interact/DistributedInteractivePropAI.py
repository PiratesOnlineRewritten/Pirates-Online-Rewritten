from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.distributed.DistributedTargetableObjectAI import DistributedTargetableObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInteractivePropAI(DistributedInteractiveAI, DistributedTargetableObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractivePropAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, cr)
        DistributedTargetableObjectAI.__init__(self, cr)
        WeaponBase.__init__(self)