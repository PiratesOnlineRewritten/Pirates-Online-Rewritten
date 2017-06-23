from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from pirates.audio.SoundGlobals import loadSfx
from pirates.audio import SoundGlobals
from pirates.battle.DistributedIslandCannon import DistributedIslandCannon
from pirates.battle.DefenseCannon import DefenseCannon
from pirates.battle.DefenseRepeaterCannon import DefenseRepeaterCannon
from pirates.battle import DefenseCannonGUI
from pirates.effects.RepeaterCannonUpgradeEffect import RepeaterCannonUpgradeEffect
from pirates.minigame.AmmoPanel import AmmoPanel
from pirates.minigame import CannonDefenseGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
import WeaponGlobals

class DistributedDefenseCannon(DistributedIslandCannon):
    ignoreGround = True
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDefenseCannon')
    sfxRepeater = None
    sfxNavy = None
    powderKegSfx = None

    def __init__(self, cr):
        DistributedIslandCannon.__init__(self, cr)
        self.__shouldUnloadSfx = False
        self.__exitEvent = None
        self.__readyEvent = None
        self._cameraState = 'CannonDefense'
        self.isRepeaterCannon = False
        self.proximityAmmo = {}
        self.usedShotNums = {}
        self.lastCannonShot = {}
        self.shipsHitByShotNum = {}
        self.removeShotNumTasks = []
        return

    def loadCannonEmptySound(self):
        self.emptySound = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_AMMO_OUT)

    def announceGenerate(self):
        DistributedIslandCannon.announceGenerate(self)
        self.accept(self.uniqueName('proximityAmmoDestroyed'), self.sendRemoveProximityAmmo)
        self.d_requestProximityAmmo(base.localAvatar.doId)
        self.d_requestShotNum(base.localAvatar.doId)

    def delete(self):
        DistributedIslandCannon.delete(self)
        if self.__shouldUnloadSfx:
            self.unloadSfx()
        for task in self.removeShotNumTasks:
            taskMgr.remove(task.name)

    def loadModel(self):
        self.loadSfx()
        self.navyCannon = DefenseCannon(self.cr)
        self.navyCannon.cannonPost = self.navyCannon
        self.navyCannon.shipId = self.shipId
        self.navyCannon.doId = self.doId
        self.navyCannon.loadModel(None, ShipGlobals.Cannons.Navy)
        self.navyCannon.deleteCollisions()
        self.repeaterCannon = DefenseRepeaterCannon(self.cr)
        self.repeaterCannon.cannonPost = self.repeaterCannon
        self.repeaterCannon.shipId = self.shipId
        self.repeaterCannon.doId = self.doId
        self.repeaterCannon.loadModel(None, ShipGlobals.Cannons.Repeater)
        self.setCannon(self.navyCannon)
        return

    def loadSfx(self):
        if self.sfxRepeater == None:
            DistributedDefenseCannon.sfxRepeater = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_TRANSFORM_REPEATER)
        if self.sfxNavy == None:
            DistributedDefenseCannon.sfxNavy = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_TRANSFORM_NAVY)
        if self.powderKegSfx == None:
            DistributedDefenseCannon.powderKegSfx = loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_POWDERKEG_EXPLODE)
        return

    def unloadSfx(self):
        if self.sfxRepeater:
            loader.unloadSfx(self.sfxRepeater)
            self.sfxRepeater = None
        if self.sfxNavy:
            loader.unloadSfx(self.sfxNavy)
            self.sfxNavy = None
        if self.powderKegSfx:
            loader.unloadSfx(self.powderKegSfx)
            self.powderKegSfx = None
        return

    def addDestructableCollision(self):
        pass

    def cleanupProp(self):
        if self.prop:
            self.prop = None
        if self.navyCannon:
            self.navyCannon.delete()
            self.navyCannon = None
        if self.repeaterCannon:
            self.repeaterCannon.delete()
            self.repeaterCannon = None
        return

    def setCannon(self, cannon):
        if self.prop:
            cannon.hNode.setHpr(self.prop.hNode.getHpr())
            cannon.pivot.setHpr(self.prop.pivot.getHpr())
            cannon.currentHpr = list(self.prop.currentHpr)
        if self.prop:
            self.prop.detachNode()
        self.prop = cannon
        self.prop.reparentTo(self)

    def currentCannonType(self, type):
        if type == 0:
            self.downgradeToNavy()
        elif type == 1:
            self.upgradeToRepeater()

    def requestUpgradeToRepeater(self):
        self.sendUpdate('requestUpgradeToRepeater')

    def upgradeToRepeater(self):
        if self.isRepeaterCannon == False:
            self.isRepeaterCannon = True
            self.doTransitionEffect(self.repeaterCannon, self.sfxRepeater)

    def downgradeToNavy(self):
        if self.isRepeaterCannon == True:
            self.isRepeaterCannon = False
            self.doTransitionEffect(self.navyCannon, self.sfxNavy)

    def doTransitionEffect(self, cannonModel, sfx):
        smokeEffect = RepeaterCannonUpgradeEffect.getEffect()
        if smokeEffect:
            smokeEffect.reparentTo(self)
            smokeEffect.setPos(self, 0, 0, 0)
            smokeEffect.spriteScale = 1.0
            smokeEffect.play()
        if sfx:
            base.playSfx(sfx, node=self.prop, cutoff=3000)
        taskMgr.doMethodLater(0.2, self._switchToCannon, name=self.uniqueName('SwitchToCannon'), extraArgs=[cannonModel])

    def _switchToCannon(self, cannonModel):
        self.setCannon(cannonModel)
        if self.av == localAvatar and localAvatar.cameraFSM.state == self._cameraState:
            self.prop.av = self.av
            localAvatar.cameraFSM.cannonDefenseCamera.changeModel(cannonModel)

    def setCannonGUI(self):
        self.cgui = DefenseCannonGUI.DefenseCannonGUI(self)
        self.cgui.exitEvent = self.__exitEvent

    def updateCannonItems(self):
        base.localAvatar.guiMgr.combatTray.initCombatTray(InventoryType.DefenseCannonRep)
        base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTray(InventoryType.DefenseCannonRep, WeaponGlobals.DEFENSE_CANNON)

    def enableCannonFireInput(self):
        self.accept('mouse1', self.fireCannon)
        self.accept('control', self.fireCannon)
        self.accept('wheel_up', self.changeAmmoMouseWheel, extraArgs=[1])
        self.accept('wheel_down', self.changeAmmoMouseWheel, extraArgs=[-1])

    def startWeapon(self, av):
        DistributedIslandCannon.startWeapon(self, av)
        if av:
            av.setPos(self.prop, 0, -6.0, 0)
            if av == localAvatar:
                self.repeaterCannon.setLocalAvatarUsingWeapon(1)
                self.navyCannon.setLocalAvatarUsingWeapon(1)
                localAvatar.sendCurrentPosition()
                localAvatar.cameraFSM.cannonDefenseCamera.setRotation(CannonDefenseGlobals.CANNON_HPR[0], CannonDefenseGlobals.CANNON_HPR[1])
        if self.__readyEvent:
            self.__readyEvent()

    def enterFireCannon(self):
        DistributedIslandCannon.enterFireCannon(self)
        self.ammoPanel = AmmoPanel(self)
        localAvatar.guiMgr.radarGui.hide()
        localAvatar.guiMgr.hideTrackedQuestInfo()
        localAvatar.guiMgr.gameGui.hide()
        localAvatar.guiMgr.crewHUD.setHUDOff()

    def exitFireCannon(self):
        if self.av == localAvatar:
            self.__shouldUnloadSfx = True
        DistributedIslandCannon.exitFireCannon(self)
        self.ammoPanel.destroy()
        render.findAllMatches('**/=objType=%s' % PiratesGlobals.COLL_DEFENSE_AMMO).detach()
        localAvatar.guiMgr.radarGui.show()
        localAvatar.guiMgr.showTrackedQuestInfo()
        localAvatar.guiMgr.gameGui.show()
        localAvatar.guiMgr.crewHUD.setHUDOn()

    def _doFireCannon(self):
        if localAvatar.isDazed:
            base.playSfx(self.emptySound)
            return
        if not self.ammoPanel.hasCurrentAmmo():
            return
        canFire = self.volley > 0
        DistributedIslandCannon._doFireCannon(self)
        if canFire:
            self.sendUpdate('recordFireEvent')
            self.lastCannonShot[self.getAmmoSkillId()] = globalClock.getFrameTime()
        self.ammoPanel.decreaseAmmoAmount(canFire)

    def useProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, charge):
        DistributedIslandCannon.useProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, charge)
        self.shotNum += 1

    def handleEndInteractKey(self):
        self.cgui.showExitDialog()

    def applyRechargeTimeModifier(self, rechargeTime):
        if not self.isRepeaterCannon:
            return rechargeTime
        newRecharge = rechargeTime + rechargeTime * CannonDefenseGlobals.REPEATER_RELOAD_MODIFIER
        return newRecharge

    def changeAmmoMouseWheel(self, amt=1):
        ammoSkillId = self.getAmmoSkillId()
        index = -1
        for i in range(len(PiratesGlobals.CANNON_DEFENSE_SKILLS)):
            if PiratesGlobals.CANNON_DEFENSE_SKILLS[i] == ammoSkillId:
                index = i
                break

        if index < 0:
            return
        if amt > 0:
            recursionChange = 1
            if index + amt > len(PiratesGlobals.CANNON_DEFENSE_SKILLS) - 1:
                return
            newAmmoId = PiratesGlobals.CANNON_DEFENSE_SKILLS[index + amt]
        else:
            recursionChange = -1
            if index + amt < 0:
                return
            newAmmoId = PiratesGlobals.CANNON_DEFENSE_SKILLS[index + amt]
        if newAmmoId == InventoryType.DefenseCannonEmpty:
            self.changeAmmoMouseWheel(amt + recursionChange)
            return
        self.changeAmmo(newAmmoId - ammoSkillId)

    def changeAmmo(self, amt=1):
        if amt == 0:
            return
        keepChanging = True
        ammoSkillId = self.getAmmoSkillId()
        while keepChanging:
            ammoSkillId += amt
            if ammoSkillId > InventoryType.DefenseCannonEmpty:
                ammoSkillId = InventoryType.DefenseCannonRoundShot
            if ammoSkillId < InventoryType.begin_WeaponSkillCannonDefense + 1:
                ammoSkillId = InventoryType.DefenseCannonEmpty
            inv = base.localAvatar.getInventory()
            if ammoSkillId > InventoryType.CannonBullet:
                keepChanging = False
            if inv.getStackQuantity(ammoSkillId) >= 2:
                keepChanging = False
            if WeaponGlobals.isInfiniteAmmo(ammoSkillId):
                keepChanging = False

        self.setAmmoSkillId(ammoSkillId)
        del ammoSkillId
        if WeaponGlobals.isInfiniteAmmo(self.getAmmoSkillId()):
            self.cgui.setAmmoLeft(-1, -1)
        else:
            ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(self.getAmmoSkillId())
            self.numShots = inv.getStackQuantity(ammoInvId)
            maxShots = inv.getStackLimit(ammoInvId)
            self.cgui.setAmmoLeft(self.numShots, maxShots)
        self.cgui.setAmmoId(self.getAmmoSkillId())
        self.cgui.showCannonControls()
        self.updateCannonDressing()
        self.hideCannonDressing()
        self.setVolley(0)

    def simpleShipHit(self, hitObject, entry, skillId, ammoSkillId):
        ship = hitObject.getNetPythonTag('ship')
        if not ship:
            return
        fromNodePath = entry.getFromNodePath()
        shotNum = int(fromNodePath.getNetTag('shotNum'))
        if shotNum not in self.shipsHitByShotNum:
            self.shipsHitByShotNum[shotNum] = []
            self.removeShotNumTasks.append(taskMgr.doMethodLater(5.0, self.removeShotNumTask, self.uniqueName('removeShotNum%s' % shotNum), extraArgs=[shotNum]))
        if ship.doId in self.shipsHitByShotNum[shotNum]:
            return
        self.shipsHitByShotNum[shotNum].append(ship.doId)
        return DistributedIslandCannon.simpleShipHit(self, hitObject, entry, skillId, ammoSkillId)

    def removeShotNumTask(self, shotNum):
        if shotNum in self.shipsHitByShotNum:
            del self.shipsHitByShotNum[shotNum]
        self.removeShotNumTasks.pop()

    def projectileHitObject(self, entry):
        DistributedIslandCannon.projectileHitObject(self, entry)
        if self.localAvatarUsingWeapon:
            fromNodePath = entry.getFromNodePath()
            ammo = fromNodePath.getNetPythonTag('ammo')
            if not ammo:
                return
            ammo.setHitByAmmoEvent(self.uniqueName('proximityAmmoDestroyed'))
            hitObject = entry.getIntoNodePath()
            objType = hitObject.getNetTag('objType')
            if not objType:
                return
            ammoSkillId = int(fromNodePath.getNetTag('ammoSkillId'))
            shotNum = int(fromNodePath.getNetTag('shotNum'))
            objType = int(objType)
            if objType == PiratesGlobals.COLL_DEFENSE_AMMO:
                hitammo = hitObject.getNetPythonTag('ammo')
                if not hitammo:
                    return
                if ammo.hasTag('noAmmoCollide') or hitammo.hasTag('noAmmoCollide'):
                    return
                ammo.dispatchHitByAmmoEvent()
                hitammo.dispatchHitByAmmoEvent()
            elif ammoSkillId in [InventoryType.DefenseCannonMine, InventoryType.DefenseCannonPowderKeg, InventoryType.DefenseCannonColdShot] and objType == PiratesGlobals.COLL_SEA or ammoSkillId == InventoryType.DefenseCannonSmokePowder and objType == PiratesGlobals.COLL_NEWSHIP:
                if shotNum not in self.proximityAmmo:
                    pos = entry.getSurfacePoint(render)
                    self.sendAddProximityAmmo(shotNum, ammoSkillId, pos, localAvatar.doId)
            if ammoSkillId in [InventoryType.DefenseCannonMine, InventoryType.DefenseCannonPowderKeg]:
                if objType == PiratesGlobals.COLL_NEWSHIP and shotNum in self.proximityAmmo:
                    ammo.dispatchHitByAmmoEvent(ammoSkillId == InventoryType.DefenseCannonMine)

    def updateReload(self, task):
        self.rechargeTime = self.cr.battleMgr.getModifiedReloadTime(localAvatar, self.skillId, self.getAmmoSkillId())
        self.rechargeTime = self.applyRechargeTimeModifier(self.rechargeTime)
        if self.rechargeTime and self.getAmmoSkillId() in self.lastCannonShot:
            percentDone = min((globalClock.getFrameTime() - self.lastCannonShot[self.getAmmoSkillId()]) / self.rechargeTime, 1.0)
        else:
            percentDone = 1
        if percentDone == 1:
            self.finishReload()
        self.cgui.updateReload(percentDone, self.volley)
        return Task.cont

    def sendAddProximityAmmo(self, shotNum, ammoSkillId, pos, attackerId):
        if shotNum in self.usedShotNums:
            return
        self.usedShotNums[shotNum] = True
        self.sendUpdate('addProximityAmmo', [shotNum, ammoSkillId, pos, attackerId])

    def sendRemoveProximityAmmo(self, shotNum, playEffect=True):
        if shotNum not in self.usedShotNums:
            self.usedShotNums[shotNum] = True
            return
        self.sendUpdate('removeProximityAmmo', [shotNum, playEffect])

    def setRemovedProximityAmmo(self, shotNum, playHitEffect):
        if shotNum in self.proximityAmmo:
            ammo = self.proximityAmmo[shotNum]
            if ammo and not ammo.destroyed:
                if playHitEffect:
                    if ammo.ammoSkillId == InventoryType.DefenseCannonPowderKeg:
                        base.playSfx(self.powderKegSfx, node=ammo, cutoff=2000)
                    ammo.playProximityAmmoEffect()
                else:
                    ammo.sinkFloatingAmmo()
            del self.proximityAmmo[shotNum]

    def d_requestProximityAmmo(self, avId):
        self.sendUpdate('requestProximityAmmo', [avId])

    def d_requestShotNum(self, avId):
        self.sendUpdate('requestShotNum', [avId])

    def setProximityAmmo(self, ammo):
        if not self.prop:
            return
        for ammoInfo in ammo:
            shotNum = ammoInfo[0]
            ammoSkillId = ammoInfo[1]
            pos = ammoInfo[2]
            attackerId = ammoInfo[3]
            timeRemaining = ammoInfo[4]
            cannonball = self.prop.addProximityAmmoFromAI(shotNum, pos, ammoSkillId, attackerId, timeRemaining, self.projectileHitEvent)
            cannonball.setHitByAmmoEvent(self.uniqueName('proximityAmmoDestroyed'))
            self.proximityAmmo[shotNum] = cannonball
            self.usedShotNums[shotNum] = True

    def setShotNum(self, shotNum):
        self.shotNum = shotNum
        self.shipsHitByShotNum[self.shotNum] = []

    def enableInput(self):
        self.enableCannonFireInput()
        localAvatar.cameraFSM.cannonDefenseCamera.enableInput()

    def disableInput(self):
        self.disableCannonFireInput()
        localAvatar.cameraFSM.cannonDefenseCamera.disableInput()

    def setExitEvent(self, eventCallBack):
        self.__exitEvent = eventCallBack

    def setReadyEvent(self, eventCallBack):
        self.__readyEvent = eventCallBack

    def simpleShipHit(self, hitObject, entry, skillId, ammoSkillId):
        ship = hitObject.getNetPythonTag('ship')
        if not ship:
            return
        fromNodePath = entry.getFromNodePath()
        shotNum = int(fromNodePath.getNetTag('shotNum'))
        if shotNum not in self.shipsHitByShotNum:
            self.shipsHitByShotNum[shotNum] = []
            self.removeShotNumTasks.append(taskMgr.doMethodLater(5.0, self.removeShotNumTask, self.uniqueName('removeShotNum%s' % shotNum), extraArgs=[shotNum]))
        if ship.doId in self.shipsHitByShotNum[shotNum]:
            return
        self.shipsHitByShotNum[shotNum].append(ship.doId)
        timestamp32 = globalClockDelta.getFrameNetworkTime(bits=32)
        if not ship:
            self.notify.warning('ignoring attack on destroyed ship')
            return
        hitSail = hitObject.getNetTag('Sail')
        if not hitSail:
            hitSail = 0
        else:
            hitSail = 1
        pos = entry.getSurfacePoint(ship)
        normal = entry.getSurfaceNormal(render)
        attackerId = 0
        attackerStr = entry.getFromNodePath().getNetTag('attackerId')
        if attackerStr:
            attackerId = int(attackerStr)
        attacker = self.cr.doId2do.get(attackerId)
        if not attacker:
            return
        areaList = self.getAreaList(skillId, ammoSkillId, ship, pos, attackerId)
        result = self.cr.battleMgr.doAttack(attacker, skillId, ammoSkillId, ship.doId, areaList, pos)
        ammo = entry.getFromNodePath().getNetPythonTag('ammo')
        if ammo:
            if ammo.hasTag('newAmmoId'):
                ammoSkillId = int(ammo.getTag('newAmmoId'))
                pos = (0, 0, 0)
        self.sendSuggestProjectileSkillResult(skillId, ammoSkillId, result, ship.doId, areaList, [
         pos[0], pos[1], pos[2]], [
         normal[0], normal[1], normal[2]], [
         0, 0, hitSail], timestamp32)
        attackerEffects, targetEffects, itemEffects = self.cr.battleMgr.getModifiedSkillEffects(attacker, ship, skillId, ammoSkillId)
        ship.projectileWeaponHit(skillId, ammoSkillId, result, targetEffects, pos, normal, (0, 0, hitSail), attacker, itemEffects)
        return True

    def getAreaList(self, skillId, ammoSkillId, target, pos, attackerId, isBoss=False):
        targets = set()
        areaShape = WeaponGlobals.getAttackAreaShape(skillId, ammoSkillId)
        bitmask = PiratesGlobals.GenericShipBitmask
        if areaShape == WeaponGlobals.AREA_SPHERE:
            self.runSphereAreaCollisions(skillId, ammoSkillId, target, pos, bitmask)
        else:
            if areaShape == WeaponGlobals.AREA_TUBE:
                self.runTubeAreaCollisions(skillId, ammoSkillId, target, pos, bitmask)
            else:
                if areaShape == WeaponGlobals.AREA_CONE:
                    self.runConeAreaCollisions(skillId, ammoSkillId, target, pos, bitmask)
                elif areaShape == WeaponGlobals.AREA_OFF:
                    return []
                numEntries = self.areaCollQueue.getNumEntries()
                if numEntries == 0:
                    return []
                for i in range(numEntries):
                    areaTarget = self.areaCollQueue.getEntry(i).getIntoNodePath().getNetPythonTag('ship')
                    if areaTarget.gameFSM.state in ('Sinking', 'Sunk'):
                        continue
                    targets.add(areaTarget.doId)

            if target in targets:
                targets.remove(target)
        return list(targets)

    def __grounHit(self, groundId, hitObject, entry, skillId, ammoSkillId):
        return False