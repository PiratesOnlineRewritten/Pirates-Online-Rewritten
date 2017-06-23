from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import globalClockDelta
from pirates.battle import WeaponGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import ComboDiary
from pirates.inventory import ItemGlobals

class ClientComboDiary(ComboDiary.ComboDiary):
    TOLERANCE = 1.5
    TimingCache = {}

    def __init__(self, av):
        ComboDiary.ComboDiary.__init__(self, av)

    def hasCombo(self, avId):
        comboHistory = self.timers.get(avId)
        if comboHistory:
            totalCombo = 0
            for entry in comboHistory:
                skillId = entry[self.SKILLID_INDEX]
                numHits = WeaponGlobals.getNumHits(skillId)
                totalCombo += numHits

            if totalCombo > 1:
                return 1
        return 0

    def getCombo(self):
        totalCombo = 0
        totalDamage = 0
        numAttackers = 0
        for avId in self.timers:
            numAttackers += 1
            for entry in self.timers[avId]:
                totalCombo += 1
                totalDamage += entry[self.DAMAGE_INDEX]

        return (
         totalCombo, totalDamage, numAttackers)

    def checkComboExpired(self, avId, weaponId, skillId, skillResult):
        attacker = base.cr.doId2do.get(avId)
        if not attacker:
            return 0
        if skillId in self.EXCLUDED_SKILLS:
            return 0
        skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
        if not skillInfo:
            return 0
        barTime = self.TimingCache.get(skillId, None)
        if barTime is None:
            anim = skillInfo[WeaponGlobals.PLAYABLE_INDEX]
            skillAnim = getattr(base.cr.combatAnims, anim)(attacker, skillId, 0, 0, None, skillResult)
            if skillAnim == None:
                return 1
            barTime = skillAnim.getDuration()
            self.TimingCache[skillId] = barTime
        curTime = globalClock.getFrameTime()
        for attackerId in self.timers:
            comboLength = len(self.timers[attackerId])
            lastEntry = self.timers[attackerId][comboLength - 1]
            lastSkillId = lastEntry[self.SKILLID_INDEX]
            timestamp = lastEntry[self.TIMESTAMP_INDEX]
            if barTime + timestamp - curTime + self.TOLERANCE > 0:
                if attackerId != avId:
                    return 0
                subtypeId = ItemGlobals.getSubtype(weaponId)
                if not subtypeId:
                    return 0
                repId = WeaponGlobals.getSkillReputationCategoryId(skillId)
                if not repId:
                    return 0
                if repId != WeaponGlobals.getRepId(weaponId):
                    return 0
                comboChain = self.COMBO_ORDER.get(subtypeId)
                if comboChain:
                    if skillId in self.SPECIAL_SKILLS.get(repId, []):
                        if lastSkillId not in self.SPECIAL_SKILLS.get(repId, []):
                            return 0
                        elif lastSkillId == skillId:
                            numHits = WeaponGlobals.getNumHits(skillId)
                            if comboLength < numHits:
                                return 0
                            elif comboLength >= numHits:
                                preMultihitEntry = self.timers[attackerId][comboLength - numHits]
                                preMultihitSkillId = preMultihitEntry[self.SKILLID_INDEX]
                                if preMultihitSkillId != skillId:
                                    return 0
                    elif skillId in comboChain:
                        index = comboChain.index(skillId)
                        if index > 0:
                            requisiteAttack = comboChain[index - 1]
                            if lastSkillId == requisiteAttack:
                                return 0
                            currentAttack = comboChain[index]
                            if lastSkillId == skillId:
                                return 0
                        elif not comboLength:
                            return 0

        return 1

    def verifyCombo(self, avId, weaponId, skillId, timestamp):
        if skillId in self.EXCLUDED_SKILLS:
            return 0
        combo = self.timers.get(avId)
        if not combo:
            return 0
        comboLength = len(combo)
        lastEntry = combo[comboLength - 1]
        lastSkillId = lastEntry[self.SKILLID_INDEX]
        lastTimestamp = lastEntry[self.TIMESTAMP_INDEX]
        subtypeId = ItemGlobals.getSubtype(weaponId)
        if not subtypeId:
            return 0
        comboChain = self.COMBO_ORDER.get(subtypeId)
        if not comboChain:
            return 0
        repId = WeaponGlobals.getSkillReputationCategoryId(skillId)
        if not repId:
            return 0
        if skillId in comboChain:
            index = comboChain.index(skillId)
            requisiteAttack = comboChain[index - 1]
            currentAttack = comboChain[index]
            if lastSkillId != requisiteAttack and lastSkillId != currentAttack and lastSkillId not in self.SPECIAL_SKILLS.get(repId, []):
                return 0
        return 1