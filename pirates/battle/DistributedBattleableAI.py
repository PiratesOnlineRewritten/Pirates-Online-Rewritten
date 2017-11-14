from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.distributed.DistributedTargetableObjectAI import DistributedTargetableObjectAI
from pirates.battle.WeaponBase import WeaponBase

class DistributedBattleableAI(DistributedInteractiveAI, DistributedTargetableObjectAI, WeaponBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleableAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, cr)
        DistributedTargetableObjectAI.__init__(self, cr)
        WeaponBase.__init__(self)

    def setInteractType(self, interactType):
        self.interactType = interactType

    def getInteractType(self):
        return self.interactType