from direct.directnotify import DirectNotifyGlobal
from pirates.distributed import DistributedInteractive
from pirates.distributed import DistributedTargetableObject
from pirates.battle import WeaponBase

class DistributedBattleable(DistributedInteractive.DistributedInteractive, DistributedTargetableObject.DistributedTargetableObject, WeaponBase.WeaponBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractive')

    def __init__(self, cr):
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        DistributedTargetableObject.DistributedTargetableObject.__init__(self, cr)
        WeaponBase.WeaponBase.__init__(self)
        self.currentWeaponId = 0

    def delete(self):
        DistributedInteractive.DistributedInteractive.delete(self)
        DistributedTargetableObject.DistributedTargetableObject.delete(self)
        WeaponBase.WeaponBase.delete(self)

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)
        DistributedTargetableObject.DistributedTargetableObject.generate(self)
        WeaponBase.WeaponBase.generate(self)

    def disable(self):
        DistributedInteractive.DistributedInteractive.disable(self)
        DistributedTargetableObject.DistributedTargetableObject.disable(self)
        WeaponBase.WeaponBase.disable(self)

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        DistributedTargetableObject.DistributedTargetableObject.announceGenerate(self)
        WeaponBase.WeaponBase.announceGenerate(self)

    def setCurrentTarget(self, targetId):
        self.currentTarget = self.cr.doId2do.get(targetId)

    def isBattleable(self):
        return 0

    def isInvisibleGhost(self):
        return 0

    def playSkillMovie(self, skillId, ammoSkillId, skillResult, charge=0, targetId=0, areaIdList=[]):
        pass