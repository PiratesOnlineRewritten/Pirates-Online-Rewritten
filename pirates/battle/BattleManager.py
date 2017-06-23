import math
from pandac.PandaModules import NodePath
import BattleManagerBase
from pirates.battle import WeaponGlobals
from pirates.piratesbase import TeamUtils
from pirates.battle import DistributedBattleNPC
from pirates.uberdog.UberDogGlobals import InventoryType
from pandac.PandaModules import *
from pirates.inventory import ItemGlobals

class BattleManager(BattleManagerBase.BattleManagerBase):

    def __init__(self, cr):
        self.cr = cr
        self.distanceChecker = NodePath('distanceChecker')

    def getGameStatManager(self):
        return base.cr.gameStatManager

    def targetInRange(self, attacker, target, skillId, ammoSkillId, pos):
        tolerance = 0
        range = self.getModifiedAttackRange(attacker, skillId, ammoSkillId)
        if range == WeaponGlobals.INF_RANGE:
            return 1
        if attacker == localAvatar and target == localAvatar.monstrousTarget:
            distance = localAvatar.distanceToTarget
        else:
            distance = attacker.getDistance(target)
            if hasattr(target, 'battleTubeNodePaths'):
                for tube in target.battleTubeNodePaths:
                    tubeLength = max(target.battleTubeRadius, target.battleTubeHeight)

                if distance - tubeLength < distance:
                    distance -= tubeLength
        if distance <= range + tolerance:
            return 1
        else:
            return 0

    def doAttack(self, attacker, skillId, ammoSkillId, targetId, areaIdList, pos, combo=0, charge=0):
        attacker.battleRandom.advanceAttackSeed()
        if targetId:
            if WeaponGlobals.getIsShipSkill(skillId):
                target = base.cr.doId2do.get(targetId)
            elif WeaponGlobals.getIsDollAttackSkill(skillId):
                target = base.cr.doId2do.get(targetId)
            else:
                target = base.cr.doId2do.get(targetId)
                if hasattr(target, 'getSkillEffects'):
                    if WeaponGlobals.C_SPAWN in set(target.getSkillEffects()):
                        return WeaponGlobals.RESULT_MISS
                if target and not TeamUtils.damageAllowed(localAvatar, target) and not WeaponGlobals.isFriendlyFire(skillId, ammoSkillId):
                    return WeaponGlobals.RESULT_NOT_AVAILABLE
        else:
            target = None
        weaponHit = self.willWeaponHit(attacker, target, skillId, ammoSkillId, charge)
        if combo == -1:
            if localAvatar.wantComboTiming:
                return WeaponGlobals.RESULT_MISS
        if not WeaponGlobals.getNeedTarget(skillId, ammoSkillId):
            return WeaponGlobals.RESULT_HIT
        if not target and not areaIdList:
            messenger.send('tooFar')
            return WeaponGlobals.RESULT_MISS
        if target and not self.obeysPirateCode(attacker, target) and not (ItemGlobals.getSubtype(localAvatar.currentWeaponId) == ItemGlobals.BAYONET and WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_COMBAT):
            return WeaponGlobals.RESULT_AGAINST_PIRATE_CODE
        if target and not self.targetInRange(attacker, target, skillId, ammoSkillId, pos):
            return WeaponGlobals.RESULT_OUT_OF_RANGE
        if target and isinstance(target, DistributedBattleNPC.DistributedBattleNPC):
            if target.getGameState()[0] == 'BreakCombat':
                return WeaponGlobals.RESULT_MISS
        if target:
            skillEffects = target.getSkillEffects()
            if WeaponGlobals.C_SPAWN in skillEffects:
                return WeaponGlobals.RESULT_MISS
        messenger.send('properHit')
        return weaponHit