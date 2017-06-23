from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType

class BattleSkillDiary():
    IDLE = 0
    CHARGING = 1

    def __init__(self, cr, av):
        self.cr = cr
        self.av = av
        self.__timers = {}
        self.__hits = {}

    def startRecharging(self, skillId, ammoSkillId):
        if self.cr.battleMgr.getModifiedRechargeTime(self.av, skillId, ammoSkillId) == 0.0:
            return
        self.__timers[skillId] = [
         self.CHARGING, 0.0, globalClock.getFrameTime(), ammoSkillId]

    def pauseRecharging(self, skillId):
        details = self.__timers.get(skillId)
        if not details or details[0] == self.IDLE:
            return
        ammoSkillId = details[3]
        if self.cr.battleMgr.getModifiedRechargeTime(self.av, skillId, ammoSkillId) == 0.0:
            return
        details[0] = self.IDLE
        curTime = globalClock.getFrameTime()
        lastTime = details[2]
        dt = curTime - lastTime
        details[1] += dt
        details[2] = curTime

    def continueRecharging(self, skillId):
        details = self.__timers.get(skillId)
        if not details:
            return
        ammoSkillId = details[3]
        if self.cr.battleMgr.getModifiedRechargeTime(self.av, skillId, ammoSkillId) == 0.0:
            return
        if details[0] != self.CHARGING:
            details[0] = self.CHARGING
            details[2] = globalClock.getFrameTime()

    def clearRecharging(self, skillId):
        if self.__timers.has_key(skillId):
            del self.__timers[skillId]

    def addHit(self, skillId, amount):
        if self.__hits.has_key(skillId):
            self.__hits[skillId] += amount
        else:
            self.__hits[skillId] = amount

    def clearHits(self, skillId):
        self.__hits[skillId] = 0

    def getHits(self, skillId):
        return self.__hits.get(skillId, 0)

    def modifyTimeSpentRecharging(self, skillId, timeSpentRecharging):
        details = self.__timers.get(skillId)
        if details and details[0] == self.CHARGING:
            details[2] = globalClock.getFrameTime() - timeSpentRecharging

    def getTimeSpentRecharging(self, skillId):
        if WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.BREAK_ATTACK_SKILL_INDEX:
            return self.getHits(skillId)
        details = self.__timers.get(skillId)
        if not details:
            return None
        t = details[1]
        if details[0] == self.CHARGING:
            curTime = globalClock.getFrameTime()
            lastTime = details[2]
            dt = curTime - lastTime
            t += dt
        return t

    def getTimeRemaining(self, skillId):
        if WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.BREAK_ATTACK_SKILL_INDEX:
            ammoSkillId = 0
        else:
            details = self.__timers.get(skillId)
            if not details:
                return
            ammoSkillId = details[3]
        timeRequired = self.cr.battleMgr.getModifiedRechargeTime(self.av, skillId, ammoSkillId)
        if timeRequired == 0.0:
            return 0.0
        timeSpent = self.getTimeSpentRecharging(skillId)
        if timeSpent is None:
            return 0.0
        elif timeSpent >= timeRequired:
            return 0.0
        else:
            return timeRequired - timeSpent
        return

    def canUseSkill(self, skillId, ammoSkillId, tolerance=0.0):
        timeRequired = self.cr.battleMgr.getModifiedRechargeTime(self.av, skillId, ammoSkillId)
        if timeRequired == 0.0:
            return 1
        timeSpent = self.getTimeSpentRecharging(skillId)
        if timeSpent is None:
            return 1
        if WeaponGlobals.getSkillTrack(skillId) == WeaponGlobals.BREAK_ATTACK_SKILL_INDEX:
            if timeSpent >= timeRequired:
                return 1
            return 0
        if timeSpent + tolerance >= timeRequired:
            return 1
        elif skillId == InventoryType.CannonShoot:
            return 1
        else:
            return 0
        return

    def __str__(self):
        s = 'BattleSkillDiary\n'
        s += ' Skill: Timestamp\n'
        for skillId, details in self.__timers.items():
            skillName = WeaponGlobals.getSkillName(skillId)
            state = ('Idle', 'Charging')[details[0]]
            dt = details[1]
            timeStamp = details[2]
            remaining = self.getTimeRemaining(skillId)
            s += ' %s (%s): %s, dt=%f, t=%f, remaining=%f (s)\n' % (skillName, skillId, state, dt, timeStamp, remaining)

        for skillId, details in self.__hits.items():
            skillName = WeaponGlobals.getSkillName(skillId)
            hits = details[0]
            remaining = self.getTimeRemaining(skillId)
            s += ' %s (%s): %s, hits=%f, remaining=%f (s)\n' % (skillName, skillId, hits, remaining)

        return s