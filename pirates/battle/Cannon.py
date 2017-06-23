from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.interval.ProjectileInterval import *
from direct.distributed.ClockDelta import *
from direct.gui.DirectGui import *
from direct.showutil import Rope
from direct.actor import Actor
from otp.otpbase import OTPGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.shipparts import CannonDNA
from pirates.effects.CannonMuzzleFire import CannonMuzzleFire
from pirates.effects.CannonBlastSmoke import CannonBlastSmoke
from pirates.effects.CannonSmokeSimple import CannonSmokeSimple
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.MuzzleFlame import MuzzleFlame
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.GrapeshotEffect import GrapeshotEffect
from pirates.battle.CannonballProjectile import CannonballProjectile
from pirates.battle import WeaponConstants
from pirates.battle import WeaponGlobals
from pirates.battle.WeaponGlobals import *
from pirates.ship import ShipGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import CannonGlobals
import random
import math
cannonTypes = {ShipGlobals.Cannons.L1: 'plain',ShipGlobals.Cannons.L2: 'plain',ShipGlobals.Cannons.L3: 'plain',ShipGlobals.Cannons.Tutorial: 'plain',ShipGlobals.Cannons.Skel_L1: 'skeleton',ShipGlobals.Cannons.Skel_L2: 'skeleton',ShipGlobals.Cannons.Skel_L3: 'skeleton',ShipGlobals.Cannons.BP: 'blackPearl',ShipGlobals.Cannons.Repeater: 'repeater',ShipGlobals.Cannons.Navy: 'navy'}
localFireSfxNames = [
 loadSfx(SoundGlobals.SFX_WEAPON_CANNON_FIRE_01), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_FIRE_02), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_FIRE_03), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_FIRE_04), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_FIRE_05)]
messenger.send('tick')
distFireSfxNames = [loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_01), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_02), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_03), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_04), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_05), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_06), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_07), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_08), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_09), loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_10)]
messenger.send('tick')

class CannonCache():

    def __init__(self, root, animBundle):
        self.root = root
        self.animBundle = animBundle

    def getCannon(self):
        root = self.root.copyTo(NodePath())
        char = root.find('+Character')
        lod = char.find('+LODNode')
        collisions = root.find('collisions')
        animControl = char.node().getBundle(0).bindAnim(self.animBundle, -1)
        return (
         root, char, lod, animControl, collisions)


class Cannon(NodePath):
    notify = directNotify.newCategory('Cannon')
    localFireSfx = None
    distFireSfx = None
    cannonModels = {}

    def __init__(self, cr, shipCannon=False):
        NodePath.__init__(self, 'cannon')
        self.cr = cr
        self.flash = None
        self.collisionRadius = 4.0
        self.localAvatarUsingWeapon = 0
        self.ammoSequence = 0
        self.shotNum = 0
        self.baseVel = Vec3(0)
        self.shipH = 0
        self.oldShipH = 0
        self.currentHpr = (0, 0, 0)
        self.recoilIval = None
        self.ship = None
        self.av = None
        if not self.cannonModels:
            self.setupCannonModels()
        self.propCollisions = self.attachNewNode(ModelNode('Cannon-collisions'))
        if not self.localFireSfx:
            Cannon.localFireSfx = []
            for file in localFireSfxNames:
                Cannon.localFireSfx.append(file)

            Cannon.distFireSfx = []
            for file in distFireSfxNames:
                Cannon.distFireSfx.append(file)

        self.isShipCannon = shipCannon
        self.cannonPost = None
        self.loaded = False
        return

    def delete(self):
        self.dna = None
        self.cannonPost = None
        if self.recoilIval:
            self.recoilIval.pause()
            self.recoilIval = None
        return

    def loadModel(self, dna=None, cannonType=None):
        if config.GetBool('disable-ship-geom', 0):
            return
        if dna:
            self.dna = dna
            cannonType = self.dna.cannonType
            if not cannonType:
                cannonType = InventoryType.CannonL1
        elif cannonType:
            self.dna = None
        else:
            cannonType = InventoryType.CannonL1
        root, char, lod, animControl, collisions = self.cannonModels[cannonType].getCannon()
        self.root = char
        self.root.reparentTo(self)
        self.lod = lod
        self.bundle = char.node().getBundle(0)
        self.control = animControl
        collisions.reparentTo(self.propCollisions)
        self.setPivots()
        self.control.loop(1)
        self.root.reparentTo(self)
        self.cannonExitPoint = self.pivot.attachNewNode('cannonExitPoint')
        self.cannonExitPoint.setY(6)
        self.island = None
        self.loaded = True
        return

    def setPivots(self):
        cj1 = 0
        cj2 = 0
        bundle = self.root.node().getBundle(0)
        joint = bundle.findChild('def_cannon_updown')
        self.pivot = self.attachNewNode(ModelNode('def_cannon_updown'))
        self.pivot.setMat(joint.getDefaultValue())
        bundle.controlJoint('def_cannon_updown', self.pivot.node())
        joint = bundle.findChild('def_cannon_turn')
        self.hNode = self.attachNewNode(ModelNode('def_cannon_turn'))
        self.hNode.setMat(joint.getDefaultValue())
        bundle.controlJoint('def_cannon_turn', self.hNode.node())
        self.pivot.reparentTo(self.hNode)
        self.recoilIval = self.pivot.scaleInterval(0.4, Vec3(1, 1, 1), startScale=Vec3(1, 0.7, 1), blendType='easeOut')

    def unloadModel(self):
        if self.recoilIval:
            self.recoilIval.pause()
            self.recoilIval = None
        self.deleteCollisions()
        return

    def initializeCollisions(self):
        if config.GetBool('disable-ship-geom', 0):
            return
        self.coll = loader.loadModel('models/shipparts/cannon_zero_collisions')
        self.coll.reparentTo(self.propCollisions)

    def deleteCollisions(self):
        self.propCollisions.removeNode()

    def setupShaders(self):
        pass

    def enableShaders(self):
        pass

    def disableShaders(self):
        pass

    def playSoundEffect(self, ammoSkillId):
        if self.localAvatarUsingWeapon:
            boomSfx = random.choice(self.localFireSfx)
        else:
            boomSfx = random.choice(self.distFireSfx)
        base.playSfx(boomSfx, node=self.pivot, cutoff=3500)

    def playFireEffect(self, ammoSkillId=0, buffs=[]):
        self.playSoundEffect(ammoSkillId)
        if self.ship:
            effectParent = self.ship.getModelRoot()
            relativeNode = self.cannonExitPoint
        else:
            effectParent = self
            relativeNode = self.cannonExitPoint
        effectParent.clearColorScale()
        effectH = self.hNode.getH(effectParent)
        effectP = self.pivot.getP(effectParent)
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            muzzleFlameEffect = MuzzleFlame.getEffect()
            if muzzleFlameEffect:
                muzzleFlameEffect.reparentTo(effectParent)
                muzzleFlameEffect.setHpr(relativeNode, 0, -90, 0)
                muzzleFlameEffect.setPos(relativeNode, 0, 0, 0)
                muzzleFlameEffect.setScale(1.0)
                muzzleFlameEffect.play()
        if not self.localAvatarUsingWeapon:
            if base.options.getSpecialEffectsSetting() == base.options.SpecialEffectsMedium:
                cannonSmokeEffect = CannonSmokeSimple.getEffect()
                if cannonSmokeEffect:
                    cannonSmokeEffect.reparentTo(effectParent)
                    cannonSmokeEffect.effectModel.unstash()
                    cannonSmokeEffect.setHpr(relativeNode, 0, -90, 0)
                    cannonSmokeEffect.setPos(relativeNode, 0, 1, 0)
                    cannonSmokeEffect.setScale(1.0)
                    cannonSmokeEffect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                cannonSmokeEffect = CannonBlastSmoke.getEffect()
                if cannonSmokeEffect:
                    cannonSmokeEffect.reparentTo(effectParent)
                    cannonSmokeEffect.particleDummy.reparentTo(effectParent)
                    cannonSmokeEffect.setHpr(effectParent, effectH, effectP, 0)
                    cannonSmokeEffect.particleDummy.setHpr(effectParent, effectH, effectP, 0)
                    cannonSmokeEffect.setPos(relativeNode, 0, 0, 0)
                    cannonSmokeEffect.setEffectScale(1.0)
                    cannonSmokeEffect.play()
        else:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                cannonSmokeEffect = CannonSmokeSimple.getEffect()
                if cannonSmokeEffect:
                    cannonSmokeEffect.reparentTo(effectParent)
                    cannonSmokeEffect.effectModel.stash()
                    cannonSmokeEffect.setHpr(relativeNode, 0, -90, 0)
                    cannonSmokeEffect.setPos(relativeNode, 0, 1, 0)
                    cannonSmokeEffect.setScale(1.0)
                    cannonSmokeEffect.play()
            if self.recoilIval:
                self.recoilIval.pause()
                self.recoilIval.start()
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
            if WeaponConstants.C_OPENFIRE in buffs:
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.reparentTo(effectParent)
                cameraShakerEffect.shakeSpeed = 0.03
                cameraShakerEffect.shakePower = 0.7
                cameraShakerEffect.numShakes = 1
                cameraShakerEffect.play(10.0)

    def getProjectile(self, ammoSkillId, projectileHitEvent, buffs=[]):
        cannonball = CannonballProjectile(self.cr, ammoSkillId, projectileHitEvent, buffs)
        cannonball.reparentTo(render)
        cannonball.setHpr(self.hNode.getH(render), self.hNode.getP(render), 0)
        return cannonball

    def getRope(self, thickness=0.15):
        rope = Rope.Rope()
        rope.ropeNode.setRenderMode(RopeNode.RMTube)
        rope.ropeNode.setNumSlices(10)
        rope.ropeNode.setUvMode(RopeNode.UVDistance)
        rope.ropeNode.setUvDirection(1)
        rope.ropeNode.setUvScale(0.25)
        rope.ropeNode.setThickness(thickness)
        ropePile = loader.loadModel('models/char/rope_high')
        ropeTex = ropePile.findTexture('rope_single_omit')
        ropePile.removeNode()
        rope.setTexture(ropeTex)
        return rope

    def playAttack(self, skillId, ammoSkillId, projectileHitEvent, targetPos=None, wantCollisions=0, flightTime=None, preciseHit=False, buffs=[], timestamp=None, numShots=1, shotNum=-1):
        if base.cr.wantSpecialEffects != 0:
            self.playFireEffect(ammoSkillId, buffs)
        if ammoSkillId == InventoryType.CannonGrapeShot:
            numShots = 7
            disperseAmount = (35, 0.0)
        else:
            disperseAmount = (40, 20.0)
        wantCollisions = 1
        self.ammoSequence = self.ammoSequence + 1 & 255
        if ammoSkillId in (InventoryType.DefenseCannonScatterShot, InventoryType.CannonGrapeShot):
            scatterOffset = random.uniform(0, 360)
        for i in range(numShots):
            ammo = self.getProjectile(ammoSkillId, projectileHitEvent, buffs)
            collNode = None
            if self.localAvatarUsingWeapon or wantCollisions:
                collNode = ammo.getCollNode()
                collNode.reparentTo(render)
            if shotNum > -1:
                self.shotNum = shotNum
            else:
                self.shotNum += 1
            if self.shotNum > 100000:
                self.shotNum = 0
            ammo.setTag('shotNum', str(self.shotNum))
            ammo.setTag('ammoSequence', str(self.ammoSequence))
            ammo.setTag('skillId', str(int(skillId)))
            ammo.setTag('ammoSkillId', str(int(ammoSkillId)))
            if self.av:
                ammo.setTag('attackerId', str(self.av.doId))
            if hasattr(self, 'fortId'):
                ammo.setTag('fortId', str(self.fortId))
            if hasattr(self, 'ship') and self.ship and hasattr(self.ship, 'doId'):
                setShipTag = True
                if setShipTag:
                    ammo.setTag('shipId', str(self.ship.doId))
            startPos = self.cannonExitPoint.getPos(render)
            ammo.setPos(startPos)
            ammo.setH(self.hNode.getH(render))
            ammo.setP(self.pivot.getP(render))
            endPlaneZ = -100
            if startPos[2] < endPlaneZ:
                self.notify.warning('bad startPos Z: %s' % startPos[2])
                return
            m = ammo.getMat(render)
            curPower = WeaponGlobals.getAttackProjectilePower(skillId, ammoSkillId) * 0.6
            if targetPos is None:
                if ammoSkillId in (InventoryType.DefenseCannonScatterShot, InventoryType.CannonGrapeShot) and i > 0:
                    dist = Vec3(math.fabs(random.gauss(0, disperseAmount[0])) + disperseAmount[1], curPower, 0.0)
                    angle = Mat3.rotateMatNormaxis(random.uniform(0, 360 / numShots) + i * 360 / (numShots - 1) + scatterOffset, Vec3.forward())
                    dist = angle.xform(dist)
                    startVel = m.xformVec(dist)
                else:
                    startVel = m.xformVec(Vec3(0, curPower, 0))
                if self.ship:
                    fvel = self.ship.smoother.getSmoothForwardVelocity() * 0.5
                    faxis = self.ship.smoother.getForwardAxis()
                    self.baseVel = faxis * fvel
                    startVel += self.baseVel
            else:
                startVel = m.xformVec(Vec3(0, 20, 2))

            def attachRope():
                if ammoSkillId == InventoryType.CannonGrappleHook and self.cannonPost:
                    rope = self.getRope()
                    rope.reparentTo(ammo)
                    rope.setup(3, ((None, Point3(0, 0, 0)), (self.cannonPost, Point3(2, 5, 10)), (self.cannonPost, Point3(2, 0, 0))))
                return

            if preciseHit:
                if flightTime is None:
                    flightTime = CannonGlobals.AI_FIRE_TIME
                pi = ProjectileInterval(ammo, startPos=startPos, endPos=targetPos, duration=flightTime, collNode=collNode)
            else:
                if targetPos:
                    if flightTime is None:
                        flightTime = CannonGlobals.getCannonballFlightTime(startPos, targetPos, curPower)
                    pi = ProjectileInterval(ammo, endZ=endPlaneZ, startPos=startPos, wayPoint=targetPos, timeToWayPoint=flightTime, gravityMult=2.5, collNode=collNode)
                else:
                    pi = ProjectileInterval(ammo, startPos=startPos, startVel=startVel, endZ=endPlaneZ, gravityMult=4.0, collNode=collNode)
                if self.localAvatarUsingWeapon or wantCollisions:
                    if base.cr.cannonballCollisionDebug == 1 or base.cr.cannonballCollisionDebug == 3:
                        addFunc = Func(base.cTrav.addCollider, collNode, ammo.collHandler)
                        delFunc = Func(base.cTrav.removeCollider, collNode)
                    else:
                        addFunc = Wait(0)
                        delFunc = Wait(0)
                    s = Sequence(addFunc, Func(attachRope), pi, Func(ammo.destroy), delFunc)
                else:
                    s = Sequence(Func(attachRope), pi, Func(ammo.destroy))
                ts = 0
                if timestamp:
                    ts = globalClockDelta.localElapsedTime(timestamp)
            ammo.setIval(s, start=True, offset=ts)

        return

    def setLocalAvatarUsingWeapon(self, val):
        self.localAvatarUsingWeapon = val

    def finalize(self):
        self.bundle.clearControlEffects()

    def setupCannonModels(self):
        for val, suffix in cannonTypes.iteritems():
            model = loader.loadModel('models/shipparts/pir_r_shp_can_deck_%s' % suffix)
            collisions = loader.loadModel('models/shipparts/pir_r_shp_can_deck_%s_collisions' % suffix)
            animBundle = model.find('**/+AnimBundleNode').node().getBundle()
            char = model.find('**/+Character')
            root = NodePath('Cannon')
            high = char.find('**/cannon_high')
            med = char.find('**/cannon_med')
            low = char.find('**/cannon_low')
            superlow = char.find('**/cannon_superlow')
            for node in char.findAllMatches('**/+ModelNode'):
                node.node().setPreserveTransform(ModelNode.PTDropNode)

            high.detachNode()
            med.detachNode()
            low.detachNode()
            superlow.detachNode()
            char.node().removeAllChildren()
            lod = LODNode('lodRoot')
            lod.addSwitch(50, 0)
            lod.addSwitch(200, 50)
            lod.addSwitch(500, 200)
            lod.addSwitch(100000, 500)
            lod = NodePath(lod)
            high.reparentTo(lod)
            med.reparentTo(lod)
            low.reparentTo(lod)
            superlow.reparentTo(lod)
            lod.reparentTo(char)
            char.flattenStrong()
            char.reparentTo(root)
            colRoot = root.attachNewNode('collisions')
            collisions.findAllMatches('**/+CollisionNode').wrtReparentTo(colRoot)
            cannonModel = CannonCache(root, animBundle)
            Cannon.cannonModels[val] = cannonModel