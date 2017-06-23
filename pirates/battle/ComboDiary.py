from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import globalClockDelta
from pirates.battle import WeaponGlobals
from pirates.battle.EnemySkills import EnemySkills
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals

class ComboDiary():
    notify = directNotify.newCategory('ComboDiary')
    TIMESTAMP_INDEX = 0
    SKILLID_INDEX = 1
    DAMAGE_INDEX = 2
    TOLERANCE = 3.0
    COMBO_ORDER = {ItemGlobals.CUTLASS: [InventoryType.CutlassHack, InventoryType.CutlassSlash, InventoryType.CutlassCleave, InventoryType.CutlassFlourish, InventoryType.CutlassStab],ItemGlobals.BROADSWORD: [EnemySkills.BROADSWORD_HACK, EnemySkills.BROADSWORD_SLASH, EnemySkills.BROADSWORD_CLEAVE, EnemySkills.BROADSWORD_FLOURISH, EnemySkills.BROADSWORD_STAB],ItemGlobals.SABRE: [EnemySkills.SABRE_HACK, EnemySkills.SABRE_SLASH, EnemySkills.SABRE_CLEAVE, EnemySkills.SABRE_FLOURISH, EnemySkills.SABRE_STAB],ItemGlobals.CURSED_CUTLASS: [InventoryType.CutlassHack, InventoryType.CutlassSlash, InventoryType.CutlassCleave, InventoryType.CutlassFlourish, InventoryType.CutlassStab],ItemGlobals.CURSED_BROADSWORD: [EnemySkills.BROADSWORD_HACK, EnemySkills.BROADSWORD_SLASH, EnemySkills.BROADSWORD_CLEAVE, EnemySkills.BROADSWORD_FLOURISH, EnemySkills.BROADSWORD_STAB],ItemGlobals.CURSED_SABRE: [EnemySkills.SABRE_HACK, EnemySkills.SABRE_SLASH, EnemySkills.SABRE_CLEAVE, EnemySkills.SABRE_FLOURISH, EnemySkills.SABRE_STAB],ItemGlobals.DAGGER_SUBTYPE: [InventoryType.DaggerCut, InventoryType.DaggerSwipe, InventoryType.DaggerGouge, InventoryType.DaggerEviscerate],ItemGlobals.DIRK: [EnemySkills.DAGGER_THROW_COMBO_1, EnemySkills.DAGGER_THROW_COMBO_2, EnemySkills.DAGGER_THROW_COMBO_3, EnemySkills.DAGGER_THROW_COMBO_4],ItemGlobals.KRIS: [InventoryType.DaggerCut, InventoryType.DaggerSwipe, InventoryType.DaggerGouge, InventoryType.DaggerEviscerate],ItemGlobals.SCIMITAR: [InventoryType.CutlassHack, InventoryType.CutlassSlash, InventoryType.CutlassCleave, InventoryType.CutlassFlourish, InventoryType.CutlassStab]}
    SPECIAL_SKILLS = {InventoryType.CutlassRep: [InventoryType.CutlassSweep, InventoryType.CutlassBrawl, InventoryType.CutlassBladestorm, EnemySkills.CUTLASS_ROLLTHRUST, EnemySkills.CUTLASS_CURSED_FIRE, EnemySkills.CUTLASS_CURSED_ICE, EnemySkills.CUTLASS_CURSED_THUNDER, EnemySkills.CUTLASS_BLOWBACK, EnemySkills.CUTLASS_CAPTAINS_FURY, EnemySkills.CUTLASS_POWER_ATTACK],InventoryType.DaggerRep: [InventoryType.DaggerAsp, InventoryType.DaggerAdder, InventoryType.DaggerSidewinder, InventoryType.DaggerViperNest, EnemySkills.DAGGER_BACKSTAB, EnemySkills.DAGGER_VENOMSTAB, EnemySkills.DAGGER_BARRAGE, EnemySkills.DAGGER_ICEBARRAGE, EnemySkills.DAGGER_ACIDDAGGER, EnemySkills.DAGGER_DAGGERRAIN, EnemySkills.DAGGER_COUP]}
    EXCLUDED_SKILLS = (
     InventoryType.CannonShoot, InventoryType.CutlassTaunt, InventoryType.DaggerThrowDirt, InventoryType.DollAttune, EnemySkills.DOLL_UNATTUNE, EnemySkills.DOLL_EVIL_EYE, InventoryType.DollHeal, InventoryType.DollCure, InventoryType.DollShackles, InventoryType.DollCurse, EnemySkills.MISC_CLEANSE, EnemySkills.MISC_DARK_CURSE, EnemySkills.MISC_GHOST_FORM, EnemySkills.MISC_FEINT, EnemySkills.MISC_HEX_WARD, EnemySkills.MISC_CAPTAINS_RESOLVE, EnemySkills.MISC_NOT_IN_FACE, EnemySkills.MISC_VOODOO_REFLECT, EnemySkills.MISC_MONKEY_PANIC, EnemySkills.MISC_ACTIVATE_VOODOO_REFLECT, EnemySkills.MISC_FIRST_AID, EnemySkills.STAFF_TOGGLE_AURA_WARDING, EnemySkills.STAFF_TOGGLE_AURA_NATURE, EnemySkills.STAFF_TOGGLE_AURA_DARK, EnemySkills.STAFF_TOGGLE_AURA_OFF, EnemySkills.CUTLASS_MASTERS_RIPOSTE)

    def __init__(self, av):
        self.owner = av
        self.timers = {}

    def cleanup(self):
        self.timers = {}
        self.owner = None
        return

    def clear(self):
        self.timers = {}

    def recordAttack(self, avId, weaponId, skillId, damage, skillResult):
        if skillId in self.EXCLUDED_SKILLS:
            return 0
        timestamp = globalClock.getFrameTime()
        val = self.checkComboExpired(avId, weaponId, skillId, skillResult)
        if val:
            self.owner.resetComboLevel()
            self.clear()
        if not self.timers.get(avId):
            self.timers[avId] = []
        else:
            val = self.verifyCombo(avId, weaponId, skillId, timestamp)
            if not val:
                return
        self.timers[avId].append((timestamp, skillId, damage))

    def getCombo(self):
        totalCombo = 0
        totalDamage = 0
        numAttackers = 0
        for avId in self.timers:
            numAttackers += 1
            for entry in self.timers[avId]:
                skillId = entry[self.SKILLID_INDEX]
                numHits = WeaponGlobals.getNumHits(skillId)
                totalCombo += numHits
                totalDamage += entry[self.DAMAGE_INDEX]

        return (
         totalCombo, totalDamage, numAttackers)

    def checkComboExpired(self, avId, weaponId, skillId, skillResult):
        barTime = 3.0
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
                    if not self.SPECIAL_SKILLS.get(repId, []):
                        self.notify.warning('No special skills for weapon %s with skill %s, subtype %s, rep %s' % (weaponId, skillId, subtypeId, repId))
                    if skillId in self.SPECIAL_SKILLS.get(repId, []):
                        if lastSkillId not in self.SPECIAL_SKILLS.get(repId, []):
                            return 0
                    elif skillId in comboChain:
                        index = comboChain.index(skillId)
                        if index > 0:
                            requisiteAttack = comboChain[index - 1]
                            if lastSkillId == requisiteAttack:
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
            if lastSkillId != requisiteAttack and lastSkillId not in self.SPECIAL_SKILLS.get(repId, []):
                return 0
        barTime = 3.0
        if barTime + lastTimestamp + self.TOLERANCE < timestamp:
            return 0
        return 1

    def __str__(self):
        s = 'ComboDiary\n'
        s += ' Avatar: Combos\n'
        for avId, combos in self.timers.items():
            s += ' %s : \n' % avId
            for entry in combos:
                skillId = entry[self.SKILLID_INDEX]
                damage = entry[self.DAMAGE_INDEX]
                timestamp = entry[self.TIMESTAMP_INDEX]
                s += '    %s : %s damage, timestamp=%f (s)\n' % (skillId, damage, timestamp)

        return s