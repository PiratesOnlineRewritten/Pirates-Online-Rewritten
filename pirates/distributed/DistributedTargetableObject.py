import random
import types
from pandac.PandaModules import *
from direct.distributed import DistributedNode
from direct.interval.IntervalGlobal import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import ClientComboDiary
from pirates.battle import WeaponGlobals
from pirates.effects import CombatEffect
from pirates.pirate import AvatarTypes
from pirates.effects.AttuneSmoke import AttuneSmoke
from pirates.inventory import ItemGlobals

class DistributedTargetableObject(DistributedNode.DistributedNode):
    NoPain = base.config.GetBool('no-pain', 0)

    def __init__(self, cr):
        DistributedNode.DistributedNode.__init__(self, cr)
        self.comboDiary = None
        self.isTeamCombo = 0
        self.currentWeapon = None
        self.noIntervals = False
        self.height = 5
        self.gameFSM = None
        self.combatEffect = None
        self.voodooSmokeEffect2 = None
        return

    def getHeight(self):
        return self.height

    def generate(self):
        DistributedNode.DistributedNode.generate(self)
        self.ouchAnim = None
        return

    def askRegen(self):
        pass

    def disable(self):
        DistributedNode.DistributedNode.disable(self)
        if self.ouchAnim:
            self.ouchAnim.pause()
            self.ouchAnim = None
        if self.combatEffect:
            self.combatEffect.destroy()
            self.combatEffect = None
        if self.voodooSmokeEffect2:
            self.voodooSmokeEffect2.stopLoop()
            self.voodooSmokeEffect2 = None
        return

    def delete(self):
        DistributedNode.DistributedNode.delete(self)
        if self.comboDiary:
            self.comboDiary.cleanup()
            self.comboDiary = None
        self.currentWeapon = None
        return

    def initializeBattleCollisions(self):
        pass

    def deleteBattleCollisions(self):
        pass

    def stashBattleCollisions(self):
        pass

    def unstashBattleCollisions(self):
        pass

    def isDistributed(self):
        return 1

    def setTargetZ(self, z):
        self.targetZ = z

    def setViewpoint(self, viewpointIndex=0):
        camera.reparentTo(self)

    def resetComboLevel(self, args=None):
        pass

    def setLocalTarget(self, on):
        pass

    def showHpMeter(self):
        pass

    def hideHpMeter(self, delay=0.0):
        pass

    def playHitSound(self, skillId, ammoSkillId, skillResult, weaponSubType=None):
        if WeaponGlobals.getIsStaffChargeSkill(skillId):
            return
        if WeaponGlobals.getIsStaffAttackSkill(skillId):
            return
        skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
        if skillId == InventoryType.UseItem:
            skillInfo = WeaponGlobals.getSkillAnimInfo(ammoSkillId)
        if skillInfo:
            soundFx = None
            sfxs = None
            if skillResult == WeaponGlobals.RESULT_HIT:
                getHitSfxFunc = skillInfo[WeaponGlobals.HIT_SFX_INDEX]
                if getHitSfxFunc:
                    sfxs = getHitSfxFunc()
            else:
                if skillResult == WeaponGlobals.RESULT_MISTIMED_HIT:
                    getMistimedHitSfxFunc = skillInfo[WeaponGlobals.MISTIMEDHIT_SFX_INDEX]
                    if getMistimedHitSfxFunc:
                        sfxs = getMistimedHitSfxFunc()
                else:
                    getMissSfxFunc = skillInfo[WeaponGlobals.MISS_SFX_INDEX]
                    if getMissSfxFunc:
                        sfxs = getMissSfxFunc()
                if sfxs:
                    if type(sfxs) == types.DictType:
                        if weaponSubType:
                            sfxList = sfxs.get(weaponSubType)
                            soundFx = random.choice(sfxList)
                        else:
                            soundFx = sfxs.get(ammoSkillId)
                    elif type(sfxs) == types.TupleType:
                        soundFx = random.choice(sfxs)
                    else:
                        soundFx = sfxs
            if soundFx:
                base.playSfx(soundFx, node=self, volume=0.7, cutoff=75)
        return

    def setCombo(self, combo, teamCombo, comboDamage, attackerId=0):
        pass

    def addCombo(self, attackerId, weaponId, skillId, damage=0, skillResult=0):
        if self.comboDiary is None:
            self.comboDiary = ClientComboDiary.ClientComboDiary(self)
        self.comboDiary.recordAttack(attackerId, weaponId, skillId, damage, skillResult)
        hasCombo = self.comboDiary.hasCombo(attackerId)
        if hasCombo:
            combo, comboDamage, teamCombo = self.comboDiary.getCombo()
            self.setCombo(combo, self.isTeamCombo, comboDamage)
        return

    def cleanupOuchIval(self):
        pass

    def playOuch(self, skillId, ammoSkillId, targetEffects, attacker, pos, itemEffects=[], multihit=0, targetBonus=0, skillResult=0):
        targetHp, targetPower, targetEffect, targetMojo, targetSwiftness = targetEffects
        if self.gameFSM.state in ('Injured', ):
            return
        if not targetBonus:
            if ammoSkillId:
                effectId = WeaponGlobals.getHitEffect(ammoSkillId)
                skillEffectId = WeaponGlobals.getSkillEffectFlag(ammoSkillId)
            else:
                effectId = WeaponGlobals.getHitEffect(skillId)
                skillEffectId = WeaponGlobals.getSkillEffectFlag(skillId)
        if attacker:
            self.addCombo(attacker.getDoId(), attacker.currentWeaponId, skillId, -targetHp, skillResult)
        if WeaponGlobals.C_KNOCKDOWN not in self.getSkillEffects() or skillEffectId == WeaponGlobals.C_KNOCKDOWN:
            self.cleanupOuchIval()
        if not targetBonus:
            if not self.NoPain and not self.noIntervals and targetEffects[0] < 0 and (self.gameFSM.state not in ('Ensnared',
                                                                                                                 'Knockdown',
                                                                                                                 'Stunned',
                                                                                                                 'Rooted',
                                                                                                                 'NPCInteract',
                                                                                                                 'ShipBoarding',
                                                                                                                 'Injured',
                                                                                                                 'Dying',
                                                                                                                 'Death') or WeaponGlobals.C_KNOCKDOWN in self.getSkillEffects() and self.gameFSM.state not in ('ShipBoarding',
                                                                                                                                                                                                                'Injured',
                                                                                                                                                                                                                'Dying',
                                                                                                                                                                                                                'Death')) and (WeaponGlobals.C_KNOCKDOWN not in self.getSkillEffects() or skillEffectId == WeaponGlobals.C_KNOCKDOWN):
                ouchSfx = None
                if self.currentWeapon:
                    if not self.avatarType.isA(AvatarTypes.Creature) and skillEffectId == WeaponGlobals.C_KNOCKDOWN and not ItemGlobals.getWeaponAttributes(self.currentWeaponId, ItemGlobals.SURE_FOOTED):
                        if self.isLocal():
                            actorIval = Sequence(self.actorInterval('injured_fall', playRate=1.5, blendOutT=0), self.actorInterval('injured_standup', playRate=1.5, blendInT=0), Func(messenger.send, 'skillFinished'))
                        else:
                            actorIval = Sequence(self.actorInterval('injured_fall', playRate=1.5, blendOutT=0), self.actorInterval('injured_standup', playRate=1.5, blendInT=0))
                    elif not self.avatarType.isA(AvatarTypes.Creature) and effectId == WeaponGlobals.VFX_BLIND:
                        actorIval = self.actorInterval('sand_in_eyes_holdweapon_noswing', playRate=random.uniform(0.7, 1.5))
                    else:
                        actorIval = self.actorInterval(self.currentWeapon.painAnim, playRate=random.uniform(0.7, 1.5))
                        if WeaponGlobals.getIsStaffAttackSkill(skillId):
                            skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
                            getOuchSfxFunc = skillInfo[WeaponGlobals.OUCH_SFX_INDEX]
                            if getOuchSfxFunc:
                                ouchSfx = getOuchSfxFunc()
                        else:
                            ouchSfx = self.getSfx('pain')
                else:
                    if not self.avatarType.isA(AvatarTypes.Creature) and skillEffectId == WeaponGlobals.C_KNOCKDOWN:
                        actorIval = Sequence(self.actorInterval('injured_fall', playRate=1.5, blendOutT=0), self.actorInterval('injured_standup', playRate=1.5, blendInT=0))
                    elif not self.avatarType.isA(AvatarTypes.Creature) and effectId == WeaponGlobals.VFX_BLIND:
                        actorIval = self.actorInterval('sand_in_eyes', playRate=random.uniform(0.7, 1.5))
                    else:
                        actorIval = self.actorInterval('idle_hit', playRate=random.uniform(0.7, 1.5))
                    if ouchSfx:
                        self.ouchAnim = Sequence(Func(base.playSfx, ouchSfx, node=self, cutoff=75), actorIval)
                    self.ouchAnim = actorIval
                self.ouchAnim.start()
        if self.combatEffect:
            self.combatEffect.destroy()
            self.combatEffect = None
        self.combatEffect = CombatEffect.CombatEffect(effectId, multihit, attacker, skillResult)
        self.combatEffect.reparentTo(self)
        self.combatEffect.setPos(self, pos[0], pos[1], pos[2])
        if not WeaponGlobals.getIsDollAttackSkill(skillId) and not WeaponGlobals.getIsStaffAttackSkill(skillId):
            if not WeaponGlobals.isSelfUseSkill(skillId):
                if attacker and not attacker.isEmpty():
                    self.combatEffect.lookAt(attacker)
                self.combatEffect.setH(self.combatEffect, 180)
        skillEffects = self.getSkillEffects()
        if WeaponGlobals.C_MELEE_SHIELD in skillEffects:
            if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_COMBAT:
                self.pulseGhostGuardEffect(attacker, Vec4(0, 0, 0, 1), wantBlending=False)
        else:
            if WeaponGlobals.C_MISSILE_SHIELD in skillEffects:
                if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_MISSILE:
                    self.pulseGhostGuardEffect(attacker, Vec4(1, 1, 1, 1), wantBlending=True)
            elif WeaponGlobals.C_MAGIC_SHIELD in skillEffects:
                if WeaponGlobals.getAttackClass(skillId) == WeaponGlobals.AC_MAGIC:
                    self.pulseGhostGuardEffect(attacker, Vec4(0.5, 0.3, 1, 1), wantBlending=True)
            self.combatEffect.play()
            if WeaponGlobals.getIsDollAttackSkill(skillId):
                self.voodooSmokeEffect2 = AttuneSmoke.getEffect()
                if self.voodooSmokeEffect2:
                    self.voodooSmokeEffect2.reparentTo(self)
                    self.voodooSmokeEffect2.setPos(0, 0, 0.2)
                    self.voodooSmokeEffect2.play()
        return

    def pulseGhostGuardEffect(self, color):
        pass

    def showHpString(self, text, pos=0, duration=2.0, scale=0.5):
        pass

    def packMultiHitEffects(self, targetEffects, numHits):
        if numHits <= 1:
            return targetEffects
        divDamage = int(targetEffects[0] / numHits + 1)
        multiHitEffects = []
        multiHitEffects.append(list(targetEffects))
        multiHitEffects[0][0] = divDamage
        for i in range(numHits - 2):
            multiHitEffects.append([divDamage, 0, 0, 0, 0])

        multiHitEffects.append([targetEffects[0] - divDamage * (numHits - 1), 0, 0, 0, 0])
        return multiHitEffects

    def useTargetedSkill(self, skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects,
                         targetEffects, areaIdEffects, itemEffects, timestamp, pos, charge=0, localSignal=0):
        if WeaponGlobals.isSelfUseSkill(skillId) and not localSignal:
            selfUse = True
        else:
            selfUse = False
        if localSignal:
            target = self.cr.doId2do.get(targetId)
            if target and target != self and WeaponGlobals.isBreakAttackComboSkill(
                    skillId) and skillResult == WeaponGlobals.RESULT_HIT:
                levelGrade = self.cr.battleMgr.getModifiedExperienceGrade(
                    self, target)
                self.guiMgr.combatTray.updateSkillCharges(levelGrade)

        if not self.isLocal() and localSignal and WeaponGlobals.getSkillTrack(
                skillId) == WeaponGlobals.DEFENSE_SKILL_INDEX or selfUse:
            multiHits = []
            numHits = WeaponGlobals.getNumHits(skillId)
            hitTiming = WeaponGlobals.getMultiHitAttacks(skillId)
            if hitTiming:
                multiHits += hitTiming

            if ammoSkillId:
                numHits += WeaponGlobals.getNumHits(ammoSkillId) - 1
                hitTiming = WeaponGlobals.getMultiHitAttacks(ammoSkillId)
                if hitTiming:
                    multiHits += hitTiming

            if not selfUse or self.isNpc:
                if not targetId and areaIdList:
                    self.playSkillMovie(
                        skillId,
                        ammoSkillId,
                        skillResult,
                        charge,
                        areaIdList[0],
                        areaIdList)
                else:
                    self.playSkillMovie(
                        skillId,
                        ammoSkillId,
                        skillResult,
                        charge,
                        targetId,
                        areaIdList)

            if skillResult == WeaponGlobals.RESULT_REFLECTED or selfUse:
                target = self
                targetId = self.getDoId()
            elif skillResult == WeaponGlobals.RESULT_BLOCKED:
                target = None
            else:
                target = self.currentTarget

            if target and targetId:
                if multiHits and numHits:
                    multiHitEffects = self.packMultiHitEffects(
                        targetEffects, numHits)
                    for i in xrange(numHits):
                        target.targetedWeaponHit(
                            skillId,
                            ammoSkillId,
                            skillResult,
                            multiHitEffects[i],
                            self,
                            pos,
                            charge,
                            multiHits[i],
                            i,
                            itemEffects=itemEffects)

                else:
                    target.targetedWeaponHit(
                        skillId,
                        ammoSkillId,
                        skillResult,
                        targetEffects,
                        self,
                        pos,
                        charge,
                        itemEffects=itemEffects)

            for targetId, areaEffects in zip(areaIdList, areaIdEffects):
                target = self.cr.doId2do.get(targetId)
                if target:
                    if multiHits and numHits:
                        multiHitEffects = self.packMultiHitEffects(
                            areaEffects, numHits)
                        for i in xrange(numHits):
                            target.targetedWeaponHit(
                                skillId,
                                ammoSkillId,
                                skillResult,
                                multiHitEffects[i],
                                self,
                                pos,
                                charge,
                                multiHits[i],
                                i,
                                itemEffects=itemEffects)

                    else:
                        target.targetedWeaponHit(
                            skillId,
                            ammoSkillId,
                            skillResult,
                            areaEffects,
                            self,
                            pos,
                            charge,
                            itemEffects=itemEffects)

            if not self.currentTarget and not areaIdList:
                self.playHitSound(
                    skillId, ammoSkillId, WeaponGlobals.RESULT_MISS)

    def getProjectileInfo(self, skillId, target):
        throwSpeed = WeaponGlobals.getProjectileSpeed(skillId)
        if not throwSpeed:
            return (None, None, None)
        placeHolder = self.attachNewNode('projectilePlaceHolder')
        if target:
            if not target.isEmpty():
                placeHolder.setPos(render, target.getPos(render))
                placeHolder.setZ(placeHolder, target.getHeight() * 0.666)
        else:
            range = WeaponGlobals.getProjectileDefaultRange(skillId)
            if self == localAvatar:
                placeHolder.setPos(camera, 0, range[0], range[1])
            else:
                placeHolder.setPos(self, 0, range[0], 4.0)
            dist = self.getDistance(placeHolder)
            time = dist / throwSpeed
            impactT = time
            animT = WeaponGlobals.getProjectileAnimT(skillId)
            if animT:
                impactT += animT
        targetPos = placeHolder.getPos(render)
        placeHolder.removeNode()
        return (
         targetPos, time, impactT)

    def localAttackedMe(self):
        pass

    def targetedWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, attacker, pos, charge=0, delay=None, multihit=0, itemEffects=[]):
        if self == attacker and not (targetEffects[0] or targetEffects[1] or targetEffects[2] or targetEffects[3] > 0 or targetEffects[4]) and not WeaponGlobals.isSelfUseSkill(skillId):
            return
        if not delay:
            targetPos, time, impactT = self.getProjectileInfo(skillId, attacker)
            if impactT:
                delay = impactT
            else:
                delay = WeaponGlobals.getAttackReactionDelay(skillId, ammoSkillId)
        if WeaponGlobals.getIsDollAttackSkill(skillId):
            delay += random.uniform(0.0, 0.5)
        if attacker and attacker.isLocal():
            self.localAttackedMe()
            centerEffect = WeaponGlobals.getCenterEffect(skillId, ammoSkillId)
            if self.hasNetPythonTag('MonstrousObject'):
                pass
            elif centerEffect == 2 or not (self.avatarType.isA(AvatarTypes.Stump) or self.avatarType.isA(AvatarTypes.FlyTrap) or self.avatarType.isA(AvatarTypes.GiantCrab) or self.avatarType.isA(AvatarTypes.CrusherCrab)):
                mult = 0.666
                if self.avatarType.isA(AvatarTypes.GiantCrab) or self.avatarType.isA(AvatarTypes.CrusherCrab):
                    mult = 0.1
                elif self.avatarType.isA(AvatarTypes.RockCrab):
                    mult = 0.2
                pos = Vec3(0, 0, self.height * mult)
            elif centerEffect == 1:
                newZ = attacker.getZ(self)
                pos = Vec3(0, 0, newZ + attacker.height * 0.666)
            else:
                newPos = self.cr.targetMgr.getAimHitPos(attacker)
                if newPos:
                    pos = Vec3(newPos[0], newPos[1], newPos[2] + 1.5)
        else:
            centerEffect = WeaponGlobals.getCenterEffect(skillId, ammoSkillId)
            if centerEffect >= 1:
                pos = Vec3(0, 0, self.height * 0.666)
        weaponSubType = None
        if attacker and attacker.currentWeapon:
            weaponType = ItemGlobals.getType(attacker.currentWeapon.itemId)
            if weaponType in [ItemGlobals.SWORD]:
                weaponSubType = ItemGlobals.getSubtype(attacker.currentWeapon.itemId)
            elif attacker.currentWeapon.getName() in ['sword']:
                weaponSubType = ItemGlobals.CUTLASS
        if delay > 0.0:
            taskMgr.doMethodLater(delay, self.playHitSound, self.taskName('playHitSoundTask'), extraArgs=[skillId, ammoSkillId, skillResult, weaponSubType])
        else:
            self.playHitSound(skillId, ammoSkillId, skillResult, weaponSubType)
        if skillResult in [WeaponGlobals.RESULT_HIT, WeaponGlobals.RESULT_MISTIMED_HIT, WeaponGlobals.RESULT_REFLECTED]:
            bonus = 0
            if bonus:
                targetEffects[0] -= bonus
            if skillResult == WeaponGlobals.RESULT_MISTIMED_HIT:
                if type(targetEffects) is types.TupleType:
                    targetEffects = (int(targetEffects[0] * WeaponGlobals.MISTIME_PENALTY),) + targetEffects[1:]
                else:
                    targetEffects[0] = int(targetEffects[0] * WeaponGlobals.MISTIME_PENALTY)
            if delay > 0.0:
                taskMgr.doMethodLater(delay, self.playOuch, self.taskName('playOuchTask'), extraArgs=[skillId, ammoSkillId, targetEffects, attacker, pos, itemEffects, multihit, 0, skillResult])
            else:
                self.playOuch(skillId, ammoSkillId, targetEffects, attacker, pos, itemEffects, multihit, skillResult=skillResult)
            if bonus:
                taskMgr.doMethodLater(WeaponGlobals.COMBO_DAMAGE_DELAY, self.playOuch, self.taskName('playBonusOuchTask'), extraArgs=[skillId, ammoSkillId, [bonus, 0, 0, 0, 0], attacker, pos, itemEffects, multihit, 1])
            if skillId in WeaponGlobals.BackstabSkills and charge:
                if attacker and attacker.isLocal() and ItemGlobals.getSubtype(attacker.currentWeaponId) == ItemGlobals.DAGGER_SUBTYPE:
                    messenger.send(''.join(['trackBackstab-', str(self.doId)]))
        elif skillResult == WeaponGlobals.RESULT_MISS or skillResult == WeaponGlobals.RESULT_MISTIMED_MISS or skillResult == WeaponGlobals.RESULT_DODGE or skillResult == WeaponGlobals.RESULT_PARRY or skillResult == WeaponGlobals.RESULT_RESIST or skillResult == WeaponGlobals.RESULT_PROTECT:
            resultString = WeaponGlobals.getSkillResultName(skillResult)
            delay = WeaponGlobals.getAttackReactionDelay(skillId, ammoSkillId)
            if delay > 0.0:
                taskMgr.doMethodLater(delay, self.showHpString, self.taskName('showMissTask'), extraArgs=[resultString, pos])
            else:
                self.showHpString(resultString, pos)
        elif skillResult == WeaponGlobals.RESULT_OUT_OF_RANGE or skillResult == WeaponGlobals.RESULT_BLOCKED:
            pass
        elif skillResult == WeaponGlobals.RESULT_AGAINST_PIRATE_CODE:
            if attacker and attacker.isLocal():
                resultString = WeaponGlobals.getSkillResultName(skillResult)
                self.showHpString(resultString, pos)
        elif skillResult == WeaponGlobals.RESULT_NOT_AVAILABLE:
            self.notify.warning('WeaponGlobals.RESULT_NOT_AVAILABLE')
        else:
            self.notify.error('unknown skillResult: %d' % skillResult)
        return

    def projectileWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker, itemEffects=[]):
        self.targetedWeaponHit(skillId, ammoSkillId, skillResult, targetEffects, attacker, pos, itemEffects=itemEffects)

    def takeDamage(self, hpLost, pos, bonus=0):
        shipId = 0
        if base.localAvatar.ship:
            shipId = base.localAvatar.ship.getDoId()
        if self.hp == None or hpLost < 0:
            return
        self.refreshStatusTray()
        if hpLost > 0:
            self.showHpText(-hpLost, pos, bonus)
            self.hpChange(quietly=0)
        return

    def takeMpDamage(self, mpLost, pos, bonus=3):
        if self.mojo == None or mpLost < 0 or self.mojo <= 0:
            return
        if mpLost > 0:
            self.showHpText(-mpLost, pos, bonus)
        return

    def respawn(self):
        pass

    def isInvisibleGhost(self):
        return 0
