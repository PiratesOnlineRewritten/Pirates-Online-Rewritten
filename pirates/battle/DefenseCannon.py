from pandac.PandaModules import *
from pirates.battle.Cannon import Cannon
from pirates.battle.DefenseCannonballProjectile import DefenseCannonballProjectile
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.minigame import CannonDefenseGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
ammoFiringSfx = {InventoryType.DefenseCannonHotShot: loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_FLAMING)}
ammoHitSfx = {InventoryType.DefenseCannonColdShot: loadSfx(SoundGlobals.SFX_MINIGAME_CANNON_ICE_FREEZE),InventoryType.DefenseCannonSmokePowder: loadSfx(SoundGlobals.SFX_WEAPON_CANNON_DIST_FIRE_01)}

class DefenseCannon(Cannon):
    notify = directNotify.newCategory('DefenseCannon')

    def __init__(self, cr, shipCannon=False):
        Cannon.__init__(self, cr, shipCannon)
        self.repeater = None
        return

    def playSoundEffect(self, ammoSkillId):
        if ammoSkillId in ammoFiringSfx:
            boomSfx = ammoFiringSfx[ammoSkillId]
            base.playSfx(boomSfx, node=self.pivot, cutoff=3500)
            return
        Cannon.playSoundEffect(self, ammoSkillId)

    def getProjectile(self, ammoSkillId, projectileHitEvent, buffs=[]):
        cannonball = DefenseCannonballProjectile(self.cr, ammoSkillId, projectileHitEvent, buffs)
        cannonball.reparentTo(render)
        cannonball.setHpr(self.hNode.getH(render), self.hNode.getP(render), 0)
        return cannonball

    def playAttack(self, skillId, ammoSkillId, projectileHitEvent, targetPos=None, wantCollisions=0, flightTime=None, preciseHit=False, buffs=[], timestamp=None, numShots=1, shotNum=-1):
        if ammoSkillId == InventoryType.DefenseCannonScatterShot:
            numShots = 4
        Cannon.playAttack(self, skillId, ammoSkillId, projectileHitEvent, targetPos, wantCollisions, flightTime, preciseHit, buffs, timestamp, numShots, shotNum)

    def addProximityAmmoFromAI(self, shotNum, pos, ammoSkillId, attackerId, timeRemaining, projectileHitEvent, buffs=[]):
        self.ammoSequence = self.ammoSequence + 1 & 255
        cannonball = self.getProjectile(ammoSkillId, projectileHitEvent, buffs)
        cannonball.setTag('shotNum', str(shotNum))
        cannonball.setTag('ammoSequence', str(self.ammoSequence))
        cannonball.setTag('skillId', str(InventoryType.CannonShoot))
        cannonball.setTag('ammoSkillId', str(ammoSkillId))
        cannonball.setTag('attackerId', str(attackerId))
        cannonball.setPos(pos)
        if ammoSkillId != InventoryType.DefenseCannonSmokePowder:
            cannonball.setZ(1)
        collNode = cannonball.getCollNode()
        collNode.reparentTo(render)
        if ammoSkillId == InventoryType.DefenseCannonMine:
            cannonball.addInWaterMine(timeRemaining)
        else:
            if ammoSkillId == InventoryType.DefenseCannonPowderKeg:
                cannonball.addPowderKeg(timeRemaining)
            elif ammoSkillId == InventoryType.DefenseCannonSmokePowder:
                cannonball.addSmokePowder(timeRemaining)
            else:
                cannonball.addColdShot(timeRemaining)
            if timeRemaining == CannonDefenseGlobals.getDefenseCannonAmmoDuration(ammoSkillId):
                if ammoSkillId in ammoHitSfx:
                    sfx = ammoHitSfx[ammoSkillId]
                    base.playSfx(sfx, node=cannonball, cutoff=6000)
        return cannonball

    def setPivots(self):
        Cannon.setPivots(self)
        bundle = self.root.node().getBundle(0)
        joint = bundle.findChild('def_cannon_animate')
        if joint:
            self.repeater = self.attachNewNode(ModelNode('def_cannon_animate'))
            self.repeater.setMat(joint.getDefaultValue())
            bundle.controlJoint('def_cannon_animate', self.repeater.node())
            self.repeater.reparentTo(self.pivot)