import math
from pandac.PandaModules import *
from direct.distributed.ClockDelta import globalClockDelta
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.tutorial import TutorialGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.effects.ProjectileEffect import ProjectileEffect
from pirates.piratesbase import TeamUtils
from pirates.battle import WeaponBaseBase
import WeaponGlobals
import CannonGlobals

class WeaponBase(WeaponBaseBase.WeaponBaseBase):
    ignoreGround = False

    def __init__(self):
        if __builtins__.has_key('localAvatar'):
            av = localAvatar
        else:
            av = self
        WeaponBaseBase.WeaponBaseBase.__init__(self, av, self.cr)
        self.prop = None
        self.ammoSequence = 0
        self.setLocalAvatarUsingWeapon(0)
        return

    def generate(self):
        self.projectileHitEvent = self.uniqueName('projectileHit')
        self.accept(self.projectileHitEvent, self.projectileHitObject)

    def announceGenerate(self):
        pass

    def disable(self):
        self.ignore(self.projectileHitEvent)

    def delete(self):
        pass

    def sendRequestTargetedSkill(self, skillId, ammoSkillId, clientResult, targetId, areaIdList, timestamp, pos, charge=0):
        self.sendUpdate('requestTargetedSkill', [skillId, ammoSkillId, clientResult, targetId, areaIdList, timestamp, pos, charge])

    def useTargetedSkill(self, skillId, ammoSkillId, actualResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, itemEffects, timestamp, pos, charge=0):
        pass

    def sendRequestShipSkill(self, skillId, ammoSkillId, clientResult, targetId, timestamp):
        self.sendUpdate('requestShipSkill', [skillId, ammoSkillId, clientResult, targetId, timestamp])

    def useShipSkill(self, skillId, ammoSkillId, actualResult, targetId, attackerEffects, targetEffects, timestamp):
        pass

    def sendRequestProjectileSkill(self, skillId, ammoSkillId, posHpr, power, timestamp):
        self.sendUpdate('requestProjectileSkill', [skillId, ammoSkillId, posHpr, timestamp, power])

    def useProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, charge):
        pass

    def sendSuggestProjectileSkillResult(self, skillId, ammoSkillId, result, targetId, areaIdList, pos, normal, codes, timestamp):
        self.sendUpdate('suggestProjectileSkillResult', [skillId, ammoSkillId, result, targetId, areaIdList, pos, normal, codes, timestamp])

    def setProjectileSkillResult(self, skillId, ammoSkillId, skillResult, targetId, areaIdList, attackerEffects, targetEffects, areaIdEffects, pos, normal, codes, attackerId, timestamp):
        attacker = base.cr.doId2do.get(attackerId)
        if not attacker:
            pass
        if not self.localAvatarUsingWeapon:
            pos = Point3(*pos)
            normal = Vec3(*normal)
            target = self.cr.doId2do.get(targetId)
            if target:
                target.projectileWeaponHit(skillId, ammoSkillId, skillResult, targetEffects, pos, normal, codes, attacker)
                if not codes and base.cr.wantSpecialEffects != 0:
                    objType = 0
                    ProjectileEffect(self.cr, attackerId, target, objType, pos, skillId, ammoSkillId)
            for id, effects in zip(areaIdList, areaIdEffects):
                target = self.cr.doId2do.get(id)
                if target:
                    target.projectileWeaponHit(skillId, ammoSkillId, skillResult, effects, pos, normal, codes, attacker)

    def projectileHitObject(self, entry):
        if not entry.hasSurfacePoint() or not entry.hasInto():
            return
        if not entry.getInto().isTangible():
            return
        hitObject = entry.getIntoNodePath()
        objType = hitObject.getNetTag('objType')
        if not objType:
            return
        objType = int(objType)
        fromNodePath = entry.getFromNodePath()
        sequence = int(fromNodePath.getNetTag('ammoSequence'))
        skillId = int(fromNodePath.getNetTag('skillId'))
        ammoSkillId = int(fromNodePath.getNetTag('ammoSkillId'))
        if objType == PiratesGlobals.COLL_AV or objType == PiratesGlobals.COLL_MONSTER:
            avId = hitObject.getNetTag('avId')
            if avId:
                avId = int(avId)
                self.__avatarHit(avId, hitObject, entry, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_NEWSHIP:
            if self.localAvatarUsingWeapon:
                if not self.simpleShipHit(hitObject, entry, skillId, ammoSkillId):
                    return
        elif objType == PiratesGlobals.COLL_SHIPPART:
            if self.localAvatarUsingWeapon:
                self.__shippartHit(hitObject, entry, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_SEA:
            self.__waterHit(hitObject, entry, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_LAND:
            groundId = hitObject.getNetTag('groundId')
            if groundId:
                groundId = int(groundId)
                self.__groundHit(groundId, hitObject, entry, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_BLDG:
            self.__buildingHit(hitObject, entry, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_SHIP_WRECK:
            propId = int(hitObject.getNetTag('propId'))
            self.__shipWreckHit(propId, hitObject, entry)
        elif objType == PiratesGlobals.COLL_GRAPPLE_TARGET:
            shipId = hitObject.getNetTag('shipId')
            if shipId:
                shipId = int(shipId)
                self.__grappleTargetHit(shipId, hitObject, entry, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_CANNON:
            cannonId = hitObject.getNetTag('cannonId')
            if cannonId:
                cannonId = int(cannonId)
                self.__cannonHit(cannonId, hitObject, entry, skillId, ammoSkillId)
            broadsideId = hitObject.getNetTag('broadsideId')
            if broadsideId:
                self.__cannonPortHit(hitObject, broadsideId)
        elif objType == PiratesGlobals.COLL_FORT:
            fortId = hitObject.getNetTag('fortId')
            if fortId:
                fortId = int(fortId)
                self.__fortHit(fortId, hitObject, entry, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_DEFENSE_AMMO:
            ammo = hitObject.getPythonTag('ammo')
        elif objType == PiratesGlobals.COLL_FLAMING_BARREL:
            barrel = hitObject.getPythonTag('barrel')
            if barrel:
                barrel.shotDown()
        elif objType == PiratesGlobals.COLL_MONSTROUS:
            obj = hitObject.getNetPythonTag('MonstrousObject')
            self.__avatarHit(obj.doId, hitObject, entry, skillId, ammoSkillId)
        ammo = entry.getFromNodePath().getNetPythonTag('ammo')
        if ammo and ammo.weaponControlled:
            ammo.projectileHitObject(entry)

    def setLocalAvatarUsingWeapon(self, val):
        self.localAvatarUsingWeapon = val
        if self.prop:
            self.prop.setLocalAvatarUsingWeapon(val)

    def __avatarHit(self, avId, hitObject, entry, skillId, ammoSkillId):
        av = self.cr.doId2do.get(avId)
        if av and self.localAvatarUsingWeapon:
            codes = []
            pos = entry.getSurfacePoint(av)
            normal = entry.getSurfaceNormal(render)
            timestamp32 = globalClockDelta.getFrameNetworkTime(bits=32)
            attackerId = 0
            attackerStr = entry.getFromNodePath().getNetTag('attackerId')
            if attackerStr:
                attackerId = int(attackerStr)
            attacker = self.cr.doId2do.get(attackerId)
            if not attacker:
                return
            if not TeamUtils.damageAllowed(attacker, av):
                if hasattr(attacker, 'getName') and hasattr(av, 'getName'):
                    pass
                return
            areaList = self.getAreaList(skillId, ammoSkillId, av, pos, attackerId)
            result = self.cr.battleMgr.doAttack(attacker, skillId, ammoSkillId, avId, areaList, pos)
            self.sendSuggestProjectileSkillResult(skillId, ammoSkillId, result, avId, areaList, [
             pos[0], pos[1], pos[2]], [
             normal[0], normal[1], normal[2]], codes, timestamp32)
            for doId in [avId] + areaList:
                target = self.cr.doId2do.get(doId)
                attackerEffects, targetEffects, itemEffects = self.cr.battleMgr.getModifiedSkillEffects(attacker, target, skillId, ammoSkillId)
                target.projectileWeaponHit(skillId, ammoSkillId, result, targetEffects, pos, normal, codes, attacker, itemEffects)

    def simpleShipHit(self, hitObject, entry, skillId, ammoSkillId):
        timestamp32 = globalClockDelta.getFrameNetworkTime(bits=32)
        ship = hitObject.getNetPythonTag('ship')
        if not ship:
            self.notify.warning('ignoring attack on destroyed ship')
            return
        attackerShipId = entry.getFromNodePath().getNetTag('shipId')
        hullCode = hitObject.getNetTag('Hull Code')
        if hullCode:
            hullCode = int(hullCode)
        else:
            hullCode = 255
        mastCode = hitObject.getNetTag('Mast Code')
        hitSail = hitObject.getNetTag('Sail')
        if not hitSail:
            hitSail = 0
        else:
            hitSail = 1
        if mastCode:
            mastCode = int(mastCode)
        else:
            mastCode = 255
        pos = entry.getSurfacePoint(ship)
        normal = entry.getSurfaceNormal(render)
        attackerId = 0
        attackerStr = entry.getFromNodePath().getNetTag('attackerId')
        if attackerStr:
            attackerId = int(attackerStr)
        attacker = self.cr.doId2do.get(attackerId)
        if not attacker:
            return
        if attackerShipId:
            if int(attackerShipId) == ship.doId:
                return
        if not TeamUtils.damageAllowed(attacker, ship):
            if TeamUtils.friendOrFoe(attacker, ship) == PiratesGlobals.PVP_FRIEND:
                localAvatar.guiMgr.createWarning(PLocalizer.TeamFireWarning, PiratesGuiGlobals.TextFG6)
            else:
                localAvatar.guiMgr.createWarning(PLocalizer.FriendlyFireWarning, PiratesGuiGlobals.TextFG6)
            attacker.battleRandom.advanceAttackSeed()
            return
        if ship:
            ship.validateMastCode(mastCode)
        result = self.cr.battleMgr.doAttack(attacker, skillId, ammoSkillId, ship.doId, [], pos)
        ammo = entry.getFromNodePath().getNetPythonTag('ammo')
        if ammo:
            if ammo.hasTag('newAmmoId'):
                ammoSkillId = int(ammo.getTag('newAmmoId'))
                pos = (0, 0, 0)
        self.sendSuggestProjectileSkillResult(skillId, ammoSkillId, result, ship.doId, [], [
         pos[0], pos[1], pos[2]], [
         normal[0], normal[1], normal[2]], [
         hullCode, mastCode, hitSail], timestamp32)
        attackerEffects, targetEffects, itemEffects = self.cr.battleMgr.getModifiedSkillEffects(attacker, ship, skillId, ammoSkillId)
        ship.projectileWeaponHit(skillId, ammoSkillId, result, targetEffects, pos, normal, (hullCode, mastCode, hitSail), attacker, itemEffects)
        return True

    def __shippartHit(self, hitObject, entry, skillId, ammoSkillId):
        shipId = hitObject.getNetTag('shipId')
        if shipId:
            shipId = int(shipId)
            ship = base.cr.doId2do.get(shipId)
            if ship:
                if ship.queryGameState() in ('FadeOut', 'Sinking', 'Inactive'):
                    return
            else:
                return
            fromNodePath = entry.getFromNodePath()
            attackerShipId = fromNodePath.getNetTag('shipId')
            if attackerShipId:
                attackerShipId = int(attackerShipId)
                if attackerShipId == shipId:
                    return
            attackerId = 0
            attackerStr = entry.getFromNodePath().getNetTag('attackerId')
            if attackerStr:
                attackerId = int(attackerStr)
                attacker = self.cr.doId2do.get(attackerId)
                if not attacker:
                    return
            else:
                return
            cannonCode = 0
            cannonCodeStr = hitObject.getNetTag('cannonCode')
            if cannonCodeStr:
                cannonCode = int(cannonCodeStr)
            hullCode = 0
            hullCodeStr = hitObject.getNetTag('hullCode')
            if hullCodeStr:
                hullCode = int(hullCodeStr)
            sailCode = 0
            sailCodeStr = hitObject.getNetTag('sailCode')
            if sailCodeStr:
                sailCode = int(sailCodeStr)
            codes = [cannonCode, hullCode, sailCode]
            pos = entry.getSurfacePoint(ship)
            normal = entry.getSurfaceNormal(render)
            timestamp32 = globalClockDelta.getFrameNetworkTime(bits=32)
            if not TeamUtils.damageAllowed(attacker, ship):
                if TeamUtils.friendOrFoe(attacker, ship) == PiratesGlobals.PVP_FRIEND:
                    localAvatar.guiMgr.createWarning(PLocalizer.TeamFireWarning, PiratesGuiGlobals.TextFG6)
                else:
                    localAvatar.guiMgr.createWarning(PLocalizer.FriendlyFireWarning, PiratesGuiGlobals.TextFG6)
                return
            areaList = self.getAreaList(skillId, ammoSkillId, ship, pos, attackerId)
            result = self.cr.battleMgr.doAttack(attacker, skillId, ammoSkillId, shipId, areaList, pos)
            self.sendSuggestProjectileSkillResult(skillId, ammoSkillId, result, shipId, areaList, [
             pos[0], pos[1], pos[2]], [
             normal[0], normal[1], normal[2]], codes, timestamp32)
            effectList = [shipId] + areaList
            propId = hitObject.getNetTag('propId')
            if propId:
                propId = int(propId)
                effectList += [propId]
                prop = self.cr.doId2do.get(propId)
                if prop:
                    result = self.cr.battleMgr.doAttack(attacker, skillId, ammoSkillId, propId, [], pos)
                    self.sendSuggestProjectileSkillResult(skillId, ammoSkillId, result, propId, [], [
                     pos[0], pos[1], pos[2]], [
                     normal[0], normal[1], normal[2]], codes, timestamp32)
            for doId in effectList:
                target = self.cr.doId2do.get(doId)
                if target:
                    attackerEffects, targetEffects, itemEffects = self.cr.battleMgr.getModifiedSkillEffects(attacker, target, skillId, ammoSkillId)
                    target.projectileWeaponHit(skillId, ammoSkillId, result, targetEffects, pos, normal, codes, attacker, itemEffects)

    def __shipHit(self, shipId, hitObject, entry, skillId, ammoSkillId):
        ship = self.cr.doId2do.get(shipId)
        if not ship or ship.queryGameState() == 'Inactive':
            return
        if self.localAvatarUsingWeapon:
            cannonCode = 0
            cannonCodeStr = hitObject.getNetTag('cannonCode')
            if cannonCodeStr:
                cannonCode = int(cannonCodeStr)
            hullCode = 0
            hullCodeStr = hitObject.getNetTag('hullCode')
            if hullCodeStr:
                hullCode = int(hullCodeStr)
            sailCode = 0
            sailCodeStr = hitObject.getNetTag('sailCode')
            if sailCodeStr:
                sailCode = int(sailCodeStr)
            codes = [cannonCode, hullCode, sailCode]
            pos = entry.getSurfacePoint(ship)
            normal = entry.getSurfaceNormal(render)
            timestamp32 = globalClockDelta.getFrameNetworkTime(bits=32)
            attackerId = 0
            attackerStr = entry.getFromNodePath().getNetTag('attackerId')
            if attackerStr:
                attackerId = int(attackerStr)
            attacker = self.cr.doId2do.get(attackerId)
            if not attacker:
                return
            if not TeamUtils.damageAllowed(attacker, ship):
                if hasattr(attacker, 'getName') and hasattr(ship, 'getName'):
                    if TeamUtils.friendOrFoe(attacker, ship) == PiratesGlobals.PVP_FRIEND:
                        localAvatar.guiMgr.createWarning(PLocalizer.TeamFireWarning, PiratesGuiGlobals.TextFG6)
                    else:
                        localAvatar.guiMgr.createWarning(PLocalizer.FriendlyFireWarning, PiratesGuiGlobals.TextFG6)
                attacker.battleRandom.advanceAttackSeed()
                return
            areaList = self.getAreaList(skillId, ammoSkillId, ship, pos, attackerId)
            result = self.cr.battleMgr.doAttack(attacker, skillId, ammoSkillId, shipId, areaList, pos)
            self.sendSuggestProjectileSkillResult(skillId, ammoSkillId, result, shipId, areaList, [
             pos[0], pos[1], pos[2]], [
             normal[0], normal[1], normal[2]], codes, timestamp32)
            for doId in [shipId] + areaList:
                target = self.cr.doId2do.get(doId)
                attackerEffects, targetEffects, itemEffects = self.cr.battleMgr.getModifiedSkillEffects(attacker, target, skillId, ammoSkillId)
                target.projectileWeaponHit(skillId, ammoSkillId, result, targetEffects, pos, normal, codes, attacker, itemEffects)

    def __propHit(self, shipId, propId, hitObject, entry, skillId, ammoSkillId):
        cannonCode = 0
        cannonCodeStr = hitObject.getNetTag('cannonCode')
        if cannonCodeStr:
            cannonCode = int(cannonCodeStr)
        hullCode = 0
        hullCodeStr = hitObject.getNetTag('hullCode')
        if hullCodeStr:
            hullCode = int(hullCodeStr)
        sailCode = 0
        sailCodeStr = hitObject.getNetTag('sailCode')
        if sailCodeStr:
            sailCode = int(sailCodeStr)
        codes = [cannonCode, hullCode, sailCode]
        ship = self.cr.doId2do.get(shipId)
        prop = self.cr.doId2do.get(propId)
        if not ship or ship.queryGameState() == 'Inactive':
            return
        if not prop:
            return
        if self.localAvatarUsingWeapon:
            pos = entry.getSurfacePoint(ship)
            normal = entry.getSurfaceNormal(render)
            timestamp32 = globalClockDelta.getFrameNetworkTime(bits=32)
            attackerId = 0
            attackerStr = entry.getFromNodePath().getNetTag('attackerId')
            if attackerStr:
                attackerId = int(attackerStr)
            attacker = self.cr.doId2do.get(attackerId)
            if not attacker:
                return
            if not TeamUtils.damageAllowed(attacker, prop) and not TeamUtils.damageAllowed(attacker, ship):
                if hasattr(attacker, 'getName') and hasattr(prop, 'getName'):
                    if TeamUtils.friendOrFoe(attacker, ship) == PiratesGlobals.PVP_FRIEND:
                        localAvatar.guiMgr.createWarning(PLocalizer.TeamFireWarning, PiratesGuiGlobals.TextFG6)
                    else:
                        localAvatar.guiMgr.createWarning(PLocalizer.FriendlyFireWarning, PiratesGuiGlobals.TextFG6)
                attacker.battleRandom.advanceAttackSeed()
                return
            areaList = self.getAreaList(skillId, ammoSkillId, ship, pos, attackerId)
            result = self.cr.battleMgr.doAttack(attacker, skillId, ammoSkillId, propId, areaList, pos)
            self.sendSuggestProjectileSkillResult(skillId, ammoSkillId, result, propId, areaList, [
             pos[0], pos[1], pos[2]], [
             normal[0], normal[1], normal[2]], codes, timestamp32)
            for doId in [propId] + areaList:
                target = self.cr.doId2do.get(doId)
                attackerEffects, targetEffects, itemEffects = self.cr.battleMgr.getModifiedSkillEffects(attacker, target, skillId, ammoSkillId)
                target.projectileWeaponHit(skillId, ammoSkillId, result, targetEffects, pos, normal, codes, attacker, itemEffects)

    def __groundHit(self, groundId, hitObject, entry, skillId, ammoSkillId):
        if self.ignoreGround:
            return
        ground = self.cr.doId2do.get(groundId)
        if not ground:
            return
        pos = entry.getSurfacePoint(ground)
        normal = entry.getSurfaceNormal(ground)
        if self.localAvatarUsingWeapon:
            codes = []
            timestamp32 = globalClockDelta.getFrameNetworkTime(bits=32)
            attackerId = 0
            attackerStr = entry.getFromNodePath().getNetTag('attackerId')
            if attackerStr:
                attackerId = int(attackerStr)
            attacker = self.cr.doId2do.get(attackerId)
            if not attacker:
                return
            groundCode = 0
            groundCodeStr = hitObject.getNetTag('groundCode')
            if groundCodeStr:
                groundCode = int(groundCodeStr)
            areaList = self.getAreaList(skillId, ammoSkillId, ground, pos, attackerId)
            result = self.cr.battleMgr.doAttack(attacker, skillId, ammoSkillId, groundId, areaList, pos)
            self.sendSuggestProjectileSkillResult(skillId, ammoSkillId, result, groundId, areaList, [
             pos[0], pos[1], pos[2]], [
             normal[0], normal[1], normal[2]], codes, timestamp32)
            for doId in [groundId] + areaList:
                target = self.cr.doId2do.get(doId)
                if not target:
                    continue
                attackerEffects, targetEffects, itemEffects = self.cr.battleMgr.getModifiedSkillEffects(attacker, target, skillId, ammoSkillId)
                target.projectileWeaponHit(skillId, ammoSkillId, result, targetEffects, pos, normal, codes, attacker, itemEffects)

    def __buildingHit(self, hitObject, entry, skillId, ammoSkillId):
        pass

    def __shipWreckHit(self, propId, hitObject, entry):
        pos = entry.getSurfacePoint(render)
        parent = self.cr.doId2do.get(propId)
        if hasattr(parent, 'shipWreck'):
            shipWreck = parent.shipWreck
            shipWreck.projectileWeaponHit(pos)

    def __waterHit(self, hitObject, entry, skillId, ammoSkillId):
        pass

    def __grappleTargetHit(self, shipId, hitObject, entry, skillId, ammoSkillId):
        sequence = int(entry.getFromNodePath().getNetTag('ammoSequence'))
        ship = self.cr.doId2do.get(shipId)
        if not ship:
            return
        else:
            targetIndex = int(hitObject.getNetTag('targetId')[-1:])
            codes = [99, targetIndex, 0]
            pos = entry.getSurfacePoint(ship)
            normal = entry.getSurfaceNormal(render)
            timestamp32 = globalClockDelta.getFrameNetworkTime(bits=32)
            areaList = []
            result = WeaponGlobals.RESULT_HIT
            self.sendSuggestProjectileSkillResult(skillId, ammoSkillId, result, shipId, areaList, [
             pos[0], pos[1], pos[2]], [
             normal[0], normal[1], normal[2]], codes, timestamp32)

    def __cannonHit(self, cannonId, hitObject, entry, skillId, ammoSkillId):
        pos = entry.getFromNodePath().getParent().getPos()
        cannon = self.cr.doId2do.get(cannonId)
        cannon.sendHitByProjectile()

    def __fortHit(self, fortId, hitObject, entry, skillId, ammoSkillId):
        if self.localAvatarUsingWeapon:
            fort = self.cr.doId2do.get(fortId)
            if fort:
                fort.gotHitByProjectile(hitObject, entry, skillId, ammoSkillId)

    def __cannonPortHit(self, hitObject, broadsideId):
        if broadsideId:
            sideId = hitObject.getNetTag('sideId')
            portId = hitObject.getNetTag('portId')
            if portId and sideId:
                sideId = int(sideId)
                portId = int(portId)
                broadsideId = int(broadsideId)
                broadsides = self.cr.doId2do.get(broadsideId)
                if broadsides:
                    broadsides.setCannonPortHitByProjectile(sideId, portId)

    def getRender(self):
        return render

    def sendShipAttack(self, skillId, ammoSkillId, attackerId, pos, normal, hullCode, mastCode, timestamp32):
        self.sendUpdate('processShipAttack', [skillId, ammoSkillId, attackerId, pos, normal, hullCode, mastCode, timestamp32])