from pirates.piratesbase import PiratesGlobals
from pirates.battle import EnemyGlobals

class GameStatManagerBase():
    from direct.directnotify import DirectNotifyGlobal
    notify = DirectNotifyGlobal.directNotify.newCategory('GameStatManagerBase')

    def __init__(self):
        self.aggroModelIndex = None
        return

    def disable(self):
        pass

    def delete(self):
        pass

    def getEnemyLevelThreshold(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.ENEMY_LEVEL_THRESHOLD_MODEL0
        else:
            return EnemyGlobals.ENEMY_LEVEL_THRESHOLD_MODEL1

    def getEnemyDamageNerf(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.ENEMY_DAMAGE_NERF_MODEL0
        else:
            return EnemyGlobals.ENEMY_DAMAGE_NERF_MODEL1

    def getEnemyHPNerf(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.ENEMY_HP_NERF_MODEL0
        else:
            return EnemyGlobals.ENEMY_HP_NERF_MODEL1

    def getInstantAggroRadius(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.INSTANT_AGGRO_RADIUS_DEFAULT_MODEL1
        else:
            return EnemyGlobals.INSTANT_AGGRO_RADIUS_DEFAULT_MODEL0

    def getSelfHealAmount(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.SELF_HEAL_AMOUNT_MODEL1
        else:
            return EnemyGlobals.SELF_HEAL_AMOUNT_MODEL0

    def getDamageThreshold(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.ATTACK_DAMAGE_THRESHOLD_MODEL1
        else:
            return EnemyGlobals.ATTACK_DAMAGE_THRESHOLD_MODEL0

    def getAccuracyThreshold(self):
        if self.aggroModelIndex == 1:
            return EnemyGlobals.ATTACK_ACCURACY_THRESHOLD_MODEL1
        else:
            return EnemyGlobals.ATTACK_ACCURACY_THRESHOLD_MODEL0