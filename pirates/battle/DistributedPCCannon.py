import math
import random
import copy
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.showbase.DirectObject import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.task import Task
from direct.showutil import Rope
from otp.otpbase import OTPGlobals
from otp.otpbase import OTPRender
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase
from pirates.battle import CannonGUI
from pirates.uberdog import UberDogGlobals
from pirates.ship import ShipGlobals
from pirates.piratesbase import Freebooter
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
import DistributedWeapon
import WeaponGlobals
import CannonGlobals
import Cannon

class DistributedPCCannon(DistributedWeapon.DistributedWeapon):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPCCannon')
    emptySound = None

    def __init__(self, cr):
        DistributedWeapon.DistributedWeapon.__init__(self, cr)
        self.ship = None
        self.tutorial = 0
        self.prop = None
        self.baseVel = Vec3(0)
        self.mouseX = 0
        self.mouseY = 0
        self.setPos(0, 0, 0)
        self.moveCannon = 0
        self.av = None
        self.ball = None
        self.ship = None
        self.shipId = None
        self.tubeNP = None
        self.cgui = None
        self.numShots = 0
        self.grapplingHook = None
        self.cannonDressingNode = NodePath(ModelNode('dressingNode'))
        self._cameraState = 'Cannon'
        self.collisionLists = {}
        self.listening = False
        self.skillId = InventoryType.CannonShoot
        self.reloadTime = 0
        self.rechargeTime = 0
        self.volley = WeaponGlobals.getAttackVolley(self.skillId, self.getAmmoSkillId())
        self.modeFSM = ClassicFSM.ClassicFSM('modeFSM', [
         State.State('off', self.enterOff, self.exitOff),
         State.State('fireCannon', self.enterFireCannon, self.exitFireCannon),
         State.State('tutorialCutscene', self.enterTutorialCutscene, self.exitTutorialCutscene)], 'off', 'off')
        self.modeFSM.enterInitialState()
        self.aimAITrack = None
        self.headingNode = NodePath('dummy')
        OTPRender.renderReflection(False, self, 'p_cannon', None)
        if not self.emptySound:
            DistributedPCCannon.emptySound = loadSfx(SoundGlobals.SFX_WEAPON_CANNON_EMPTY)
        self.fireSubframeCall = None
        self.__invRequest = None
        self.shotNum = -1
        return

    def loadCannonEmptySound(self):
        self.emptySound = loadSfx(SoundGlobals.SFX_WEAPON_CANNON_EMPTY)

    def generate(self):
        DistributedWeapon.DistributedWeapon.generate(self)
        if self.tutorial:
            tutorialMode = 'useCannon'
            proximityText = (None, )
        else:
            tutorialMode = None
            proximityText = (PLocalizer.InteractCannon,)
        self.setInteractOptions(tutorialMode=tutorialMode, proximityText=proximityText, diskRadius=12.0, sphereScale=8.0, endInteract=0)
        return

    def announceGenerate(self):
        self.loadModel()
        DistributedWeapon.DistributedWeapon.announceGenerate(self)

    def cleanupProp(self):
        if self.prop:
            self.prop.delete()
            self.prop = None
        return

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.getTrailTaskName())
        if self.aimAITrack:
            self.aimAITrack.pause()
            self.aimAITrack = None
        self.av = None
        self.prop.av = None
        self.cleanupProp()
        if self.grapplingHook:
            self.grapplingHook.removeNode()
            self.grapplingHook = None
        DistributedWeapon.DistributedWeapon.disable(self)
        return

    def delete(self):
        self.modeFSM.request('off')
        del self.modeFSM
        DistributedWeapon.DistributedWeapon.delete(self)

    def getConeOriginNode(self):
        return self.prop.pivot

    def showUseInfo(self):
        if self.disk:
            self.disk.hide()

    def loadModel(self):
        self.prop = Cannon.Cannon(self.cr)
        self.prop.cannonPost = self.prop
        self.prop.shipId = self.shipId
        self.prop.doId = self.doId
        self.prop.reparentTo(self)
        self.prop.loadModel(None)
        return

    def requestInteraction(self, avId, interactType=0):
        base.localAvatar.motionFSM.off()
        DistributedWeapon.DistributedWeapon.requestInteraction(self, avId, interactType)

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterTutorialCutscene(self):
        pass

    def exitTutorialCutscene(self):
        pass

    def setVolley(self, volley):
        self.volley = volley
        if self.cgui:
            self.cgui.setVolley(volley)

    def setCannonGUI(self):
        self.cgui = CannonGUI.CannonGUI(self)

    def updateCannonItems(self):
        base.localAvatar.guiMgr.combatTray.initCombatTray(InventoryType.CannonRep)
        base.localAvatar.guiMgr.combatTray.skillTray.updateSkillTray(rep=InventoryType.CannonRep, weaponMode=WeaponGlobals.CANNON)
        base.localAvatar.guiMgr.combatTray.triggerSkillTraySkill(self.getAmmoSkillId())

    def enableCannonFireInput(self):
        self.accept('mouse1', self.fireCannon)
        self.accept('control', self.fireCannon)
        self.accept('wheel_up', self.changeAmmo, extraArgs=[1])
        self.accept('wheel_down', self.changeAmmo, extraArgs=[-1])

    def disableCannonFireInput(self):
        self.ignore('mouse1')
        self.ignore('control')
        self.ignore('wheel_up')
        self.ignore('wheel_down')

    def enterFireCannon(self):
        localAvatar.guiMgr.combatTray.setLinkedCannon(self)
        self.enableCannonFireInput()
        base.localAvatar.guiMgr.setIgnoreEscapeHotKey(True)
        self.accept(InteractiveBase.END_INTERACT_EVENT, self.handleEndInteractKey)
        localAvatar.cameraFSM.request(self._cameraState, self.prop)
        self.setCannonGUI()
        taskMgr.add(self.updateReload, 'updateCannonReload')
        self.cgui.setAmmoId(self.getAmmoSkillId())

        def gotInventory(inv):
            if inv:
                ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(self.getAmmoSkillId())
                maxShots = inv.getStackLimit(ammoInvId)
                self.numShots = inv.getStackQuantity(ammoInvId)
                if WeaponGlobals.isInfiniteAmmo(self.getAmmoSkillId()) or WeaponGlobals.canUseInfiniteAmmo(localAvatar.getCurrentCharm(), self.getAmmoSkillId()):
                    self.cgui.setAmmoLeft(-1, -1)
                else:
                    self.cgui.setAmmoLeft(self.numShots, maxShots)
                self.updateCannonItems()
                self.updateCannonDressing()

        if self.__invRequest:
            DistributedInventoryBase.cancelGetInventory(self.__invRequest)
        self.__invRequest = DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), gotInventory)

    def exitFireCannon(self):
        self.disableCannonFireInput()
        self.ignore(InteractiveBase.END_INTERACT_EVENT)
        self.cgui.destroy()
        self.cgui = None
        taskMgr.remove('updateCannonReload')
        localAvatar.guiMgr.combatTray.hideSkills()
        localAvatar.guiMgr.combatTray.disableTray()
        if self.fireSubframeCall:
            self.fireSubframeCall.cleanup()
            self.fireSubframeCall = None
        self.cannonDressingNode.detachNode()
        base.localAvatar.guiMgr.combatTray.skillTray.hideSkillTray()
        base.localAvatar.guiMgr.combatTray.initCombatTray(localAvatar.currentWeaponId)
        combatTrayGrid = base.localAvatar.guiMgr.combatTray.find('**/InventoryUICombatTrayGrid*')
        if combatTrayGrid:
            combatTrayGrid.show()
        base.localAvatar.guiMgr.combatTray.tonicButton.show()
        return

    def requestExit(self):
        DistributedWeapon.DistributedWeapon.requestExit(self)
        self.stopWeapon(self.av)

    def selectAmmo(self, atype):
        dif = atype - self.getAmmoSkillId()
        self.changeAmmo(dif)

    def setAmmoSkillId(self, ammoSkillId):
        localAvatar.setCannonAmmoSkillId(ammoSkillId)

    def getAmmoSkillId(self):
        return localAvatar.getCannonAmmoSkillId()

    def changeAmmo(self, amt=1):
        if amt == 0:
            return
        keepChanging = True
        ammoSkillId = self.getAmmoSkillId()
        while keepChanging:
            ammoSkillId += amt
            if ammoSkillId > InventoryType.CannonGrappleHook:
                ammoSkillId = InventoryType.CannonRoundShot
            if ammoSkillId < InventoryType.begin_WeaponSkillCannon + 1:
                ammoSkillId = InventoryType.CannonGrappleHook
            inv = base.localAvatar.getInventory()
            if ammoSkillId > InventoryType.CannonBullet:
                keepChanging = False
            if inv and inv.getStackQuantity(ammoSkillId) >= 2:
                keepChanging = False
            if WeaponGlobals.isInfiniteAmmo(ammoSkillId) or WeaponGlobals.canUseInfiniteAmmo(localAvatar.getCurrentCharm(), ammoSkillId):
                keepChanging = False
            if not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
                if not WeaponGlobals.canFreeUse(ammoSkillId):
                    keepChanging = True

        self.setAmmoSkillId(ammoSkillId)
        del ammoSkillId
        if WeaponGlobals.isInfiniteAmmo(self.getAmmoSkillId()) or WeaponGlobals.canUseInfiniteAmmo(localAvatar.getCurrentCharm(), self.getAmmoSkillId()):
            self.cgui.setAmmoLeft(-1, -1)
        elif inv:
            ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(self.getAmmoSkillId())
            self.numShots = inv.getStackQuantity(ammoInvId)
            maxShots = inv.getStackLimit(ammoInvId)
            self.cgui.setAmmoLeft(self.numShots, maxShots)
        self.cgui.setAmmoId(self.getAmmoSkillId())
        self.updateCannonDressing()
        self.hideCannonDressing()
        self.setVolley(0)

    def updateReloadBar(self):
        if not self.av:
            return
        timeSpentReloading = self.av.skillDiary.getTimeSpentRecharging(self.skillId)
        if timeSpentReloading:
            reloadProgress = timeSpentReloading / self.rechargeTime
        self.rechargeTime = self.cr.battleMgr.getModifiedReloadTime(self.av, self.skillId, self.getAmmoSkillId())
        if timeSpentReloading:
            timeSpentReloading = reloadProgress * self.rechargeTime
            self.av.skillDiary.modifyTimeSpentRecharging(self.skillId, timeSpentReloading)
            self.cgui.startReload(self.rechargeTime, self.volley, elapsedTime=timeSpentReloading, doneCallback=self.finishReload)

    def updateCannonDressing(self):
        if self.getAmmoSkillId() != InventoryType.CannonGrappleHook:
            self.cannonDressingNode.detachNode()
            if self.grapplingHook:
                self.grapplingHook.removeNode()
                self.grapplingHook = None
        else:
            if self.ship:
                self.cannonDressingNode.reparentTo(self.ship.avCannonPivot)
            else:
                self.cannonDressingNode.reparentTo(self.prop.pivot)
            if not self.grapplingHook:
                self.grapplingHook = loader.loadModel('models/ammunition/GrapplingHook')
            if self.grapplingHook:
                self.grapplingHook.setPos(0.3, -3.0, -1.0)
                self.grapplingHook.reparentTo(self.cannonDressingNode)
        return

    def showCannonDressing(self):
        self.cannonDressingNode.show()

    def hideCannonDressing(self):
        self.cannonDressingNode.hide()

    def setMovie(self, mode, avId):

        def doMovie(av):
            if mode == WeaponGlobals.WEAPON_MOVIE_START:
                self.startWeapon(av)
            elif mode == WeaponGlobals.WEAPON_MOVIE_DEFEAT:
                self.stopWeapon(av, fromDefeat=1)
            elif mode == WeaponGlobals.WEAPON_MOVIE_STOP:
                self.stopWeapon(av)
            elif mode == WeaponGlobals.WEAPON_MOVIE_CLEAR:
                pass

        if self.pendingDoMovie:
            base.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
            self.pendingDoMovie = None
        self.pendingDoMovie = base.cr.relatedObjectMgr.requestObjects([avId], eachCallback=doMovie, timeout=60)
        return

    def startWeapon(self, av):
        if av == base.localAvatar:
            if base.localAvatar.cannon:
                return
            base.localAvatar.b_setGameState('Cannon')
            self.acceptInteraction()
            self.setLocalAvatarUsingWeapon(1)
            base.localAvatar.cannon = self
            if self.ship:
                self.ship.hideMasts()
                self.ship.stopSmoke()
                self.ship.listenForFloorEvents(0)
            localAvatar.guiMgr.request('MouseLook')
            self.modeFSM.request('fireCannon')
            base.localAvatar.collisionsOn()
        self.prop.hNode.setHpr(0, 0, 0)
        self.prop.pivot.setHpr(0, 0, 0)
        self.prop.currentHpr = (0, 0, 0)
        av.stopSmooth()
        av.setPos(self.prop, 0, -2.5, 0)
        av.setHpr(self.prop, 0, 0, 0)
        av.play('kneel_fromidle', toFrame=16)
        self.av = av
        self.prop.av = av

    def stopWeapon(self, av, fromDefeat=0):
        if av != base.localAvatar:
            return
        if base.localAvatar.cannon != self:
            return
        if not base.localAvatar.cannon:
            return
        self.stopReload()
        self.setLocalAvatarUsingWeapon(0)
        base.localAvatar.cannon = None
        self.modeFSM.request('off')
        if av.getGameState() == 'Cannon' and not fromDefeat:
            av.b_setGameState(av.gameFSM.defaultState)
        av.startSmooth()
        self.av = None
        self.prop.av = None
        self.prop.hNode.setHpr(0, 0, 0)
        self.prop.pivot.setHpr(0, 0, 0)
        self.prop.currentHpr = (0, 0, 0)
        return

    def fireCannon(self):
        cannonDelay = self.cr.battleMgr.getModifiedRechargeTime(self.av, self.skillId, 0)
        if globalClock.getFrameTime() - localAvatar.lastCannonShot < cannonDelay:
            return
        if self.fireSubframeCall:
            self.fireSubframeCall.cleanup()
        self.fireSubframeCall = SubframeCall(self._doFireCannon, 10, self.uniqueName('fireCannon'))

    def _doFireCannon(self):
        if self.volley > 0:
            localAvatar.lastCannonShot = globalClock.getFrameTime()
            h = self.prop.hNode.getH(render)
            p = self.prop.pivot.getP(render)
            r = 0
            pos = self.prop.cannonExitPoint.getPos(render)
            posHpr = [
             pos[0], pos[1], pos[2], h, p, r]
            charge = 0.0
            timestamp = globalClockDelta.getFrameNetworkTime(bits=32)
            self.sendRequestProjectileSkill(self.skillId, self.getAmmoSkillId(), posHpr, charge, timestamp)
            self.prop.playAttack(self.skillId, self.getAmmoSkillId(), self.projectileHitEvent, buffs=localAvatar.getSkillEffects(), shotNum=self.shotNum)
            self.setVolley(self.volley - 1)
            if not WeaponGlobals.isInfiniteAmmo(self.getAmmoSkillId()) and not base.config.GetBool('infinite-ammo', 0) and not WeaponGlobals.canUseInfiniteAmmo(localAvatar.getCurrentCharm(), self.getAmmoSkillId()):
                inv = base.localAvatar.getInventory()
                ammoInvId = WeaponGlobals.getSkillAmmoInventoryId(self.getAmmoSkillId())
                maxShots = inv.getStackLimit(ammoInvId)
                self.numShots -= 1
                self.cgui.setAmmoLeft(self.numShots, maxShots)
            self.hideCannonDressing()
        else:
            base.playSfx(self.emptySound)
        if localAvatar.guiMgr.combatTray.skillTray.traySkillMap:
            for i in range(len(localAvatar.guiMgr.combatTray.skillTray.traySkillMap)):
                if localAvatar.guiMgr.combatTray.skillTray.traySkillMap[i] == self.getAmmoSkillId():
                    button = localAvatar.guiMgr.combatTray.skillTray.tray[i + 1]
                    if button.skillStatus is True:
                        button.updateQuantity(self.numShots)

    def useProjectileSkill(self, skillId, ammoSkillId, posHpr, timestamp, charge):
        x, y, z, h, p, r = posHpr
        if self.ship and not self.ship.showCannonsFiring():
            return
        if not self.localAvatarUsingWeapon:
            self.prop.hNode.setH(render, h)
            self.prop.pivot.setP(render, p)
            buffs = []
            if self.av:
                buffs = self.av.skillEffects
            self.prop.playAttack(skillId, ammoSkillId, self.projectileHitEvent, buffs=buffs, shotNum=self.shotNum)

    def doAIAttack(self, x, y, z, tzone, skillId, ammoSkillId, timestamp):
        if self.ship and not self.ship.showCannonsFiring():
            return
        if not (self.cr.activeWorld and self.cr.activeWorld.worldGrid):
            return
        buffs = []
        if self.av:
            buffs = self.av.getSkillEffects()
        zonePos = self.cr.activeWorld.worldGrid.getZoneCellOrigin(tzone)
        targetPos = Point3(zonePos[0] + x, zonePos[1] + y, zonePos[2] + z)
        self.prop.hNode.lookAt(render, targetPos)
        p = self.prop.hNode.getP()
        self.prop.pivot.setP(p)
        self.prop.hNode.setP(0)
        self.prop.playAttack(skillId, ammoSkillId, self.projectileHitEvent, targetPos, buffs=buffs, timestamp=timestamp)
        if __dev__ and base.config.GetBool('show-ai-cannon-targets', 0):
            self.tracker.setPos(render, targetPos)

    def getTrailTaskName(self):
        return self.uniqueName('cannonTrail')

    def destroy(self):
        self.ignoreAll()
        self.removeNode()

    def startReload(self, elapsedTime=0):
        if self.numShots == 0 and not WeaponGlobals.isInfiniteAmmo(self.getAmmoSkillId()) and not WeaponGlobals.canUseInfiniteAmmo(localAvatar.getCurrentCharm(), self.getAmmoSkillId()):
            return
        self.rechargeTime = self.cr.battleMgr.getModifiedReloadTime(localAvatar, self.skillId, self.getAmmoSkillId())
        base.localAvatar.skillDiary.startRecharging(self.skillId, 0)
        self.cgui.startReload(self.rechargeTime, self.volley, elapsedTime=0, doneCallback=self.finishReload)

    def stopReload(self):
        self.cgui.stopReload()
        if self.av:
            self.av.skillDiary.clearRecharging(self.skillId)

    def finishReload(self):
        newVolley = WeaponGlobals.getAttackVolley(self.skillId, self.getAmmoSkillId())
        if newVolley > self.numShots and not WeaponGlobals.isInfiniteAmmo(self.getAmmoSkillId()) and not WeaponGlobals.canUseInfiniteAmmo(localAvatar.getCurrentCharm(), self.getAmmoSkillId()):
            newVolley = self.numShots
        self.setVolley(newVolley)
        self.showCannonDressing()

    def setUserId(self, avId):
        DistributedWeapon.DistributedWeapon.setUserId(self, avId)
        self.checkInUse()

    def checkInUse(self):
        if self.userId and self.userId != localAvatar.doId:
            self.setAllowInteract(0)
        else:
            self.setAllowInteract(1)

    def setAllowInteract(self, allow, forceOff=False):
        DistributedWeapon.DistributedWeapon.setAllowInteract(self, allow)
        if not allow and forceOff:
            self.requestExit()

    def completeCannonCheck(self):
        for colList in self.collisionLists.values():
            colList.sort()
            ammo = colList[0][1].getFromNodePath().getPythonTag('ammo')
            if not ammo or ammo.destroyed:
                continue
            for entryData in colList:
                DistributedWeapon.DistributedWeapon.projectileHitObject(self, entryData[1])
                if ammo.destroyed:
                    break

        self.collisionLists = {}
        self.listening = False

    def projectileHitObject(self, entry):
        shot = int(entry.getFromNodePath().getNetTag('shotNum'))
        if not self.collisionLists.get(shot):
            self.collisionLists[shot] = []
        y = entry.getSurfacePoint(camera)[1]
        self.collisionLists[shot].append((y, entry))
        if not self.listening:
            self.listening = True
            self.acceptOnce('event-loop-done', self.completeCannonCheck)

    def updateReload(self, task):
        self.rechargeTime = self.cr.battleMgr.getModifiedReloadTime(localAvatar, self.skillId, self.getAmmoSkillId())
        self.rechargeTime = self.applyRechargeTimeModifier(self.rechargeTime)
        if self.rechargeTime:
            percentDone = min((globalClock.getFrameTime() - localAvatar.lastCannonShot) / self.rechargeTime, 1.0)
        else:
            percentDone = 1
        if percentDone == 1:
            self.finishReload()
        self.cgui.updateReload(percentDone, self.volley)
        return Task.cont

    def applyRechargeTimeModifier(self, rechargeTime):
        return rechargeTime