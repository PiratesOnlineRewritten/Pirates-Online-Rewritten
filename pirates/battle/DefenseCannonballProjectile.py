from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.interval.ProjectileInterval import *
from direct.directnotify import DirectNotifyGlobal
from direct.task.Task import Task
from pirates.battle.CannonballProjectile import CannonballProjectile
from pirates.battle import WeaponGlobals
from pirates.battle import WeaponConstants
from pirates.piratesbase import PiratesGlobals
from pirates.minigame import CannonDefenseGlobals, DistributedDefendWorld
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.effects.DefenseCannonballProjectileEffect import DefenseCannonballProjectileEffect
from pirates.effects.FireTrail import FireTrail
from pirates.effects.FuryTrail import FuryTrail
from pirates.effects.ThunderBallGlow import ThunderBallGlow
from pirates.effects.PowderKegDomeExplosion import PowderKegDomeExplosion
from pirates.effects.PowderKegWaterSplash import PowderKegWaterSplash
from pirates.effects.WaterRipple import WaterRipple
from pirates.effects.SmokePowderEffect import SmokePowderEffect
from pirates.effects.IceShotEffect import IceShotEffect
import random

class DefenseCannonballProjectile(CannonballProjectile):
    notify = DirectNotifyGlobal.directNotify.newCategory('DefenseCannonballProjectile')

    def __init__(self, cr, ammoSkillId, event, buffs=[]):
        CannonballProjectile.__init__(self, cr, ammoSkillId, event, buffs)
        self.hitWater = False
        self.lockedPos = False
        self.singleEffect = None
        self.target = None
        self.getWorldPos = False
        self.areaCollSphere = None
        self.lastPos = None
        self.direction = None
        self.duration = 1.5
        self.collisionRadiusScale = 1
        self.collisionPosOffset = 50
        self.hitByAmmoEvent = None
        return

    def setHitByAmmoEvent(self, event):
        self.hitByAmmoEvent = event

    def dispatchHitByAmmoEvent(self, playEffect=True):
        if self.hitByAmmoEvent:
            shotNum = int(self.getTag('shotNum'))
            if shotNum:
                messenger.send(self.hitByAmmoEvent, [shotNum, playEffect])

    def destroy(self):
        if self.model:
            self.model.clearPythonTag('DefenseAmmo')
        if taskMgr.hasTaskNamed(self.uniqueName('findTarget')):
            taskMgr.remove(self.uniqueName('findTarget'))
        if taskMgr.hasTaskNamed(self.uniqueName('updateTarget')):
            taskMgr.remove(self.uniqueName('updateTarget'))
        if taskMgr.hasTaskNamed(self.uniqueName('sinkFloatingAmmo')):
            taskMgr.remove(self.uniqueName('sinkFloatingAmmo'))
        if self.areaCollSphere and not self.areaCollSphere.isEmpty():
            self.areaCollSphere.detachNode()
        CannonballProjectile.destroy(self)

    def loadModel(self):
        self.mtrail = None
        self.strail = None
        self.scaleIval = None
        maxGlowScale = 8
        minGlowScale = 7
        if not base.config.GetBool('want-special-effects', 1):
            cannonball = loader.loadModel('models/ammunition/cannonball')
        else:
            if self.ammoSkillId == InventoryType.DefenseCannonRoundShot:
                cannonball = loader.loadModel('models/ammunition/cannonball')
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                    self.createMotionTrails(self)
                if base.options.getSpecialEffectsSetting() == base.options.SpecialEffectsLow:
                    self.createSimpleMotionTrail(self)
            else:
                if self.ammoSkillId == InventoryType.DefenseCannonHotShot:
                    cannonball = loader.loadModel('models/ammunition/cannonball')
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                        self.trailEffect = FireTrail.getEffect()
                        if self.trailEffect:
                            self.trailEffect.reparentTo(cannonball)
                            self.trailEffect.startLoop()
                else:
                    if self.ammoSkillId == InventoryType.CannonFlamingSkull or self.ammoSkillId == InventoryType.DefenseCannonHotShot:
                        maxGlowScale = 28
                        minGlowScale = 24
                        cannonball = loader.loadModel('models/ammunition/cannonball')
                        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                            self.trailEffect = FireTrail.getEffect()
                            if self.trailEffect:
                                self.trailEffect.wantGlow = base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium
                                self.trailEffect.reparentTo(cannonball)
                                self.trailEffect.startLoop()
                    elif self.ammoSkillId == InventoryType.DefenseCannonPowderKeg:
                        cannonball = loader.loadModel('models/ammunition/pir_m_gam_can_powderKeg')
                        cannonball.setHpr(90, 0, 90)
                        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                            self.createMotionTrails(self)
                        if base.options.getSpecialEffectsSetting() == base.options.SpecialEffectsLow:
                            self.createSimpleMotionTrail(self)
                    else:
                        cannonball = loader.loadModel('models/ammunition/cannonball')
                        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                            self.createMotionTrails(self)
                        if base.options.getSpecialEffectsSetting() == base.options.SpecialEffectsLow:
                            self.createSimpleMotionTrail(self)
                    cannonball.setScale(2.0)
                    if self.ammoSkillId == InventoryType.DefenseCannonMine:
                        cannonball.setColor(1.0, 0.0, 0.0, 1.0)
                        cannonball.setScale(4.0)
                if self.ammoSkillId == InventoryType.DefenseCannonPowderKeg:
                    cannonball.setScale(4.0)
            if WeaponConstants.C_OPENFIRE in self.buffs:
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                    self.glowB = loader.loadModel('models/effects/lanternGlow')
                    self.glowB.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
                    self.glowB.setDepthWrite(0)
                    self.glowB.setFogOff()
                    self.glowB.setLightOff()
                    self.glowB.setBin('fixed', 120)
                    self.glowB.setColorScale(1, 0.8, 0.5, 0.9)
                    self.glowB.reparentTo(cannonball)
                    self.glowB.setBillboardPointEye()
                    scaleUp = self.glowB.scaleInterval(0.1, maxGlowScale, startScale=minGlowScale, blendType='easeInOut')
                    scaleDown = self.glowB.scaleInterval(0.1, minGlowScale, startScale=maxGlowScale, blendType='easeInOut')
                    self.glowBTrack = Sequence(scaleUp, scaleDown)
                    self.glowBTrack.loop()
        cannonball.setPythonTag('DefenseAmmo', self)
        cannonball.setTag('DefenseAmmo', '1')
        return cannonball

    def setIval(self, ival, start=False, offset=0):
        CannonballProjectile.setIval(self, ival, start, offset)
        if self.ammoSkillId == InventoryType.DefenseCannonTargetedShot:
            if self.target == None:
                taskMgr.doMethodLater(0.05, self.findTarget, self.uniqueName('findTarget'))
        return

    def createProjectileEffect(self, cr, attackerId, hitObject, objType, pos, skillId, ammoSkillId, normal=None):
        if self.singleEffect != None:
            return
        if self.hasTag('newAmmoId'):
            ammoSkillId = int(self.getTag('newAmmoId'))
        effect = DefenseCannonballProjectileEffect(self.cr, attackerId, hitObject, objType, pos, skillId, ammoSkillId, normal)
        if ammoSkillId in [InventoryType.DefenseCannonSmokePowder, InventoryType.DefenseCannonColdShot]:
            self.singleEffect = effect
        return

    def playProximityAmmoEffect(self):
        if self.ammoSkillId == InventoryType.DefenseCannonPowderKeg:
            self.explosiveHit(200, InventoryType.DefenseCannonPowderKegExplosion)
            effect = PowderKegDomeExplosion.getEffect()
            if effect:
                effect.reparentTo(base.effectsRoot)
                effect.setPos(self.getPos())
                effect.size = 200
                effect.play()
            effect = PowderKegWaterSplash.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(base.effectsRoot)
                effect.setPos(self.getPos())
                effect.setEffectScale(6)
                effect.play()
            effect = WaterRipple.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(base.effectsRoot)
                effect.setPos(self.getPos())
                effect.setEffectScale(20)
                effect.play()
            return
        if self.ammoSkillId == InventoryType.DefenseCannonMine:
            self.explosiveHit(10)

    def destroyIfNecessary(self, cr, attackerId, hitObject, objType, pos, skillId, ammoSkillId, normal=None):
        if ammoSkillId == InventoryType.DefenseCannonMine:
            if objType == PiratesGlobals.COLL_SEA:
                return
        elif ammoSkillId == InventoryType.DefenseCannonPowderKeg:
            if objType in [PiratesGlobals.COLL_SEA, PiratesGlobals.COLL_DEFENSE_AMMO]:
                return
            elif objType == PiratesGlobals.COLL_NEWSHIP and self.hasTag('newAmmoId'):
                return
        elif ammoSkillId in [InventoryType.DefenseCannonSmokePowder, InventoryType.DefenseCannonColdShot]:
            if self.hasTag('noAmmoCollide'):
                return
        self.destroy()

    def addInWaterMine(self, timeRemaining):
        self.cleanupMotionTrails()
        self.addCollisionSphere(4)
        self.collNode.node().setIntoCollideMask(PiratesGlobals.TargetBitmask)
        base.cTrav.addCollider(self.collNode, self.collHandler)
        self.setTag('objType', str(PiratesGlobals.COLL_DEFENSE_AMMO))
        self.setTag('newAmmoId', str(InventoryType.DefenseCannonMineInWater))

    def addPowderKeg(self, timeRemaining):
        self.cleanupMotionTrails()
        self.addCollisionSphere(10)
        self.collNode.node().setIntoCollideMask(PiratesGlobals.TargetBitmask)
        base.cTrav.addCollider(self.collNode, self.collHandler)
        self.setTag('objType', str(PiratesGlobals.COLL_DEFENSE_AMMO))

    def addSmokePowder(self, timeRemaining):
        self.cleanupMotionTrails()
        self.model.detachNode()
        self.addCollisionSphere(60)
        base.cTrav.addCollider(self.collNode, self.collHandler)
        self.setTag('objType', str(PiratesGlobals.COLL_DEFENSE_AMMO))
        self.setTag('noAmmoCollide', 'noAmmoCollide')
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            effect = SmokePowderEffect.getEffect(unlimited=True)
            if effect:
                effect.wrtReparentTo(base.effectsRoot)
                effect.setPos(self.getPos())
                effect.setDuration(timeRemaining)
                effect.play()

    def addColdShot(self, timeRemaining):
        self.cleanupMotionTrails()
        self.model.detachNode()
        self.model = loader.loadModel('models/ammunition/pir_m_gam_can_icepatchAmmo')
        self.model.setScale(5.0)
        self.model.reparentTo(self)
        base.model = self.model
        self.addCollisionSphere(50)
        base.cTrav.addCollider(self.collNode, self.collHandler)
        self.setTag('newAmmoId', str(InventoryType.DefenseCannonColdShotInWater))
        self.setTag('objType', str(PiratesGlobals.COLL_DEFENSE_AMMO))
        self.setTag('noAmmoCollide', 'noAmmoCollide')
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            effect = IceShotEffect.getEffect(unlimited=True)
            if effect:
                effect.wrtReparentTo(base.effectsRoot)
                effect.setPos(self.getPos())
                effect.play()

    def addCollisionSphere(self, radius, x=0, y=0, z=0):
        weaponSphere = CollisionSphere(x, y, z, radius)
        weaponSphere.setTangible(1)
        self.collNode.node().clearSolids()
        self.collNode.node().addSolid(weaponSphere)
        self.collNode.setPos(self.getPos())

    def explosiveHit(self, radius, newAmmoId=None):
        if newAmmoId:
            self.setTag('newAmmoId', str(newAmmoId))
        self.addCollisionSphere(radius)
        taskMgr.doMethodLater(0.0, self.waitToDestroy, self.uniqueName('waitToDestroy'))

    def waitToDestroy(self, task=None):
        self.destroy()
        taskMgr.remove('waitToDestroy')

    def sinkFloatingAmmo(self, task=None):
        self.collNode.node().setIntoCollideMask(BitMask32.allOff())
        base.cTrav.removeCollider(self.collNode)
        self.collNode.node().clearSolids()
        if self.ammoSkillId in [InventoryType.DefenseCannonMine, InventoryType.DefenseCannonPowderKeg]:
            afterSinkingPos = self.getPos()
            afterSinkingPos.setZ(-20)
            pi = ProjectileInterval(self, startPos=self.getPos(), duration=1, endPos=afterSinkingPos)
            s = Sequence(pi, Func(self.destroy))
            self.setIval(s, start=True)
        elif self.ammoSkillId == InventoryType.DefenseCannonColdShot:
            s = Sequence(LerpColorInterval(self.model, 4.0, color=VBase4(0.0, 0.0, 0.0, 0.0), blendType='easeOut'), Func(self.destroy))
            s.start()
        else:
            self.destroy()

    def findTarget(self, task=None):
        if not isinstance(base.cr.activeWorld, DistributedDefendWorld.DistributedDefendWorld):
            return Task.done
        shortestDistance = 99999
        for i in range(len(base.cr.activeWorld.flamingBarrels)):
            barrel = base.cr.activeWorld.flamingBarrels[i].barrelModel
            if barrel and not barrel.isEmpty():
                distance = self.getDistance(barrel)
                if distance < shortestDistance:
                    shortestDistance = distance
                    self.target = barrel
                    self.getWorldPos = True

        if self.target:
            return self.updateTarget(task)
        if self.lastPos == None:
            self.lastPos = self.getPos()
            return Task.cont
        if self.direction == None:
            self.direction = Vec3(self.lastPos.getX() - self.getX(), self.lastPos.getY() - self.getY(), 0)
            self.direction.normalize()
        if self.areaCollSphere == None:
            collSphere = CollisionSphere(0, 0, 0, 100)
            node = CollisionNode('areaTargetCollSphere')
            node.addSolid(collSphere)
            node.setFromCollideMask(PiratesGlobals.TargetBitmask)
            node.setIntoCollideMask(BitMask32.allOff())
            self.areaCollSphere = NodePath(node)
            self.areaCollSphere.setName('DefenseCannonballProjectile.areaCollSphere')
            self.areaCollQueue = CollisionHandlerQueue()
            self.areaCollHandler = CollisionHandlerEvent()
            self.areaCollSphere.reparentTo(render)
        self.areaCollSphere.setPos(self.getPos() - self.direction * self.collisionPosOffset)
        self.areaCollSphere.setZ(1)
        self.areaCollSphere.setScale(self.collisionRadiusScale)
        self.collisionPosOffset += 100
        self.collisionRadiusScale *= 1.005
        base.cTrav.addCollider(self.areaCollSphere, self.areaCollQueue)
        base.cTrav.traverse(render)
        base.cTrav.removeCollider(self.areaCollSphere)
        for i in range(self.areaCollQueue.getNumEntries()):
            entry = self.areaCollQueue.getEntry(i)
            potentialTargetColl = entry.getIntoNodePath()
            ship = potentialTargetColl.getNetPythonTag('ship')
            ammo = potentialTargetColl.getNetPythonTag('ammo')
            if self.target == None and ship and ship.queryGameState() not in ['FadeOut', 'Sunk', 'Sinking']:
                self.target = ship
                self.getWorldPos = True
            elif ammo and int(ammo.getTag('ammoSkillId')) == InventoryType.DefenseCannonPowderKeg:
                self.target = ammo
                self.getWorldPos = False
                break

        if self.target:
            self.areaCollSphere.detachNode()
            self.areaCollSphere = None
            return self.updateTarget(task)
        return Task.cont

    def updateTarget(self, task=None):
        if self.target.isEmpty():
            return Task.done
        self.duration *= 0.5
        if self.getWorldPos:
            self.newEndPos = base.cr.activeWorld.getWorldPos(self.target)
        else:
            self.newEndPos = self.target.getPos()
        if self.newEndPos is None:
            return
        self.pauseIval(True)
        self.collNode.node().clearSolids()
        addFunc = Func(base.cTrav.addCollider, self.collNode, self.collHandler)
        delFunc = Func(base.cTrav.removeCollider, self.collNode)
        pi = ProjectileInterval(self, startPos=self.getPos(), endZ=-1000, wayPoint=self.newEndPos, timeToWayPoint=self.duration, collNode=self.collNode)
        s = Sequence(addFunc, pi, Func(self.destroy), delFunc)
        self.setIval(s, True)
        taskMgr.doMethodLater(0.2, self.updateTarget, self.uniqueName('updateTarget'))
        return Task.done

    def uniqueName(self, name):
        return name + '-%s' % id(self)