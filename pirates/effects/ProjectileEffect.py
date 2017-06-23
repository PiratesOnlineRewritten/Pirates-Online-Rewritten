from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.effects.CannonExplosion import CannonExplosion
from pirates.effects.CannonSplash import CannonSplash
from pirates.effects.DirtClod import DirtClod
from pirates.effects.DustCloud import DustCloud
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.RockShower import RockShower
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.DustRing import DustRing
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.effects.LightSmoke import LightSmoke
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.FireTrail import FireTrail
from pirates.effects.GreenBlood import GreenBlood
from pirates.effects.HitFlashA import HitFlashA
from pirates.effects.ShockwaveHit import ShockwaveHit
from pirates.effects.WaspCloud import WaspCloud
from pirates.effects.PoisonHit import PoisonHit
from pirates.effects.FireballHit import FireballHit
from pirates.effects.CurseHit import CurseHit
from pirates.effects.ExplosionCloud import ExplosionCloud
from pirates.effects.FadingSigil import FadingSigil
from pirates.effects.FlashStar import FlashStar
from pirates.effects.VoodooSmoke import VoodooSmoke
from pirates.effects.SpectralSmoke import SpectralSmoke
from pirates.effects.DrainLife import DrainLife
from pirates.effects.Fire import Fire
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.effects.DustRing import DustRing
from pirates.effects.Sparks import Sparks
from pirates.effects.SmokeBomb import SmokeBomb
from pirates.effects.SmokePillar import SmokePillar
from pirates.effects.FlamingDebris import FlamingDebris
from pirates.effects.ShipDebris import ShipDebris
from pirates.effects.RockDebris import RockDebris
from pirates.effects.Explosion import Explosion
from pirates.effects.ExplosionTip import ExplosionTip
from pirates.effects.LightningStrike import LightningStrike
from pirates.effects.MuzzleFlame import MuzzleFlame
from pirates.effects.SmallRockShower import SmallRockShower
from pirates.effects.SimpleSmokeCloud import SimpleSmokeCloud
from pirates.effects.FlashEffect import FlashEffect
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
import random
skillSfxs = None

def getSkillSfx():
    global skillSfxs
    if not skillSfxs:
        skillSfxs = {InventoryType.GrenadeExplosion: loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_IMPACT),InventoryType.GrenadeShockBomb: loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_STINK),InventoryType.GrenadeFireBomb: loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_FIREBOMB_EXPLODE),InventoryType.GrenadeSmokeCloud: loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_SMOKE),InventoryType.GrenadeSiege: loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_IMPACT)}


class ProjectileEffect():
    notify = DirectNotifyGlobal.directNotify.newCategory('ProjectileEffect')

    def __init__(self, cr, attackerId, hitObject, objType, pos, skillId, ammoSkillId, normal=None):
        self.cr = cr
        self.attackerId = attackerId
        self.normal = normal
        getSkillSfx()
        from pirates.battle.DistributedBattleAvatar import DistributedBattleAvatar
        from pirates.world.DistributedIsland import DistributedIsland
        self.projVelocity = (
         (25, 0), (0, 25), (-25, 0), (0, -25))
        if not objType:
            if isinstance(hitObject, DistributedBattleAvatar):
                objType = PiratesGlobals.COLL_AV
            elif isinstance(hitObject, DistributedIsland):
                objType = PiratesGlobals.COLL_LAND
            else:
                self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)
                return
        if objType == PiratesGlobals.COLL_AV:
            self.avatarHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType in (PiratesGlobals.COLL_MONSTER, PiratesGlobals.COLL_MONSTROUS):
            self.monsterHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_DESTRUCTIBLE:
            self.propHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_SHIPPART or objType == PiratesGlobals.COLL_NEWSHIP:
            self.propHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_SEA:
            self.waterHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_LAND:
            self.groundHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_BLOCKER:
            self.blockerHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_BLDG:
            self.buildingHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_GRAPPLE_TARGET:
            self.grappleHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_CANNON:
            self.cannonHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_FORT:
            self.fortHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_DEFENSE_AMMO:
            self.propHitEffect(hitObject, pos, skillId, ammoSkillId)
        elif objType == PiratesGlobals.COLL_FLAMING_BARREL:
            pass
        else:
            self.notify.warning('playEffect: unknown objType: %s' % objType)

    def playSfx(self, ammoSkillId, node, startTime=0):
        sfx = skillSfxs.get(ammoSkillId)
        if sfx:
            base.playSfx(sfx, node=node, time=startTime, cutoff=400)

    def basicHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        from pirates.battle import WeaponGlobals
        if self.cr:
            attacker = self.cr.doId2do.get(self.attackerId)
            aoeRadius = self.cr.battleMgr.getModifiedAttackAreaRadius(attacker, skillId, ammoSkillId)
        else:
            attacker = None
            aoeRadius = 0
        unlimited = bool(attacker and attacker.isLocal())
        if config.GetBool('show-aoe-radius', 0):
            s = loader.loadModel('models/misc/smiley')
            s.reparentTo(render)
            s.setPos(hitObject, pos)
            s.setScale(aoeRadius)
            s.setTransparency(1)
            s.setColorScale(1.0, 0.5, 0.5, 0.4)
        if ammoSkillId in [InventoryType.CannonRoundShot, InventoryType.CannonChainShot, InventoryType.CannonBullet, InventoryType.CannonSkull, InventoryType.CannonBarShot, InventoryType.CannonFury, InventoryType.CannonFirebrand, InventoryType.CannonFlamingSkull, InventoryType.CannonThunderbolt]:
            hitSfxNames = [
             SoundGlobals.SFX_FX_WOOD_IMPACT_01, SoundGlobals.SFX_FX_WOOD_IMPACT_02, SoundGlobals.SFX_FX_WOOD_IMPACT_03, SoundGlobals.SFX_FX_WOOD_IMPACT_04, SoundGlobals.SFX_FX_WOOD_SHATTER_02, SoundGlobals.SFX_FX_WOOD_SHATTER_03]
            sfx = loadSfx(random.choice(hitSfxNames))
            base.playSfx(sfx, node=hitObject, cutoff=1500)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                explosionEffect = ExplosionFlip.getEffect(unlimited)
                if explosionEffect:
                    explosionEffect.reparentTo(base.effectsRoot)
                    explosionEffect.setPos(hitObject, pos)
                    explosionEffect.setScale(0.8)
                    explosionEffect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                smokeCloudEffect = SimpleSmokeCloud.getEffect(unlimited)
                if smokeCloudEffect:
                    smokeCloudEffect.reparentTo(hitObject)
                    smokeCloudEffect.setPos(hitObject, pos)
                    smokeCloudEffect.setEffectScale(1.0)
                    smokeCloudEffect.play()
                if localAvatar.ship and hitObject == localAvatar.ship:
                    cameraShakerEffect = CameraShaker()
                    cameraShakerEffect.wrtReparentTo(hitObject)
                    cameraShakerEffect.setPos(hitObject, pos)
                    cameraShakerEffect.shakeSpeed = 0.04
                    cameraShakerEffect.shakePower = 6.0
                    cameraShakerEffect.numShakes = 2
                    cameraShakerEffect.scalePower = 1
                    cameraShakerEffect.play(120.0)
        if ammoSkillId == InventoryType.CannonExplosive:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                effect = Explosion.getEffect(unlimited)
                if effect:
                    effect.wrtReparentTo(hitObject)
                    effect.setPos(hitObject, pos)
                    effect.setEffectScale(1.0)
                    effect.setEffectRadius(aoeRadius / 3.0)
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                for i in range(2):
                    effect = FlamingDebris.getEffect(unlimited)
                    if effect:
                        effect.wrtReparentTo(base.effectsRoot)
                        effect.setPos(hitObject, pos)
                        effect.duration = 4
                        effect.velocityX = self.projVelocity[i][0]
                        effect.velocityY = self.projVelocity[i][1]
                        effect.play()

                if localAvatar.ship and hitObject == localAvatar.ship:
                    cameraShakerEffect = CameraShaker()
                    cameraShakerEffect.wrtReparentTo(hitObject)
                    cameraShakerEffect.setPos(hitObject, pos)
                    cameraShakerEffect.shakeSpeed = 0.04
                    cameraShakerEffect.shakePower = 6.0
                    cameraShakerEffect.numShakes = 2
                    cameraShakerEffect.scalePower = 1
                    cameraShakerEffect.play(300.0)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = FlamingDebris.getEffect(unlimited)
                if effect:
                    effect.wrtReparentTo(base.effectsRoot)
                    effect.setPos(hitObject, pos)
                    effect.duration = 4
                    effect.velocityX = self.projVelocity[i][0]
                    effect.velocityY = self.projVelocity[i][1]
                    effect.play()
        if ammoSkillId == InventoryType.CannonThunderbolt:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                effect = LightningStrike.getEffect(unlimited)
                if effect:
                    effect.wrtReparentTo(base.effectsRoot)
                    effect.setPos(hitObject, pos)
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                flashEffect = FlashEffect()
                flashEffect.wrtReparentTo(base.effectsRoot)
                flashEffect.setScale(600)
                flashEffect.setPos(hitObject, pos)
                flashEffect.effectColor = Vec4(0.5, 0.8, 1, 1)
                flashEffect.fadeTime = 0.3
                flashEffect.play()
                if localAvatar.ship and hitObject == localAvatar.ship:
                    cameraShakerEffect = CameraShaker()
                    cameraShakerEffect.wrtReparentTo(hitObject)
                    cameraShakerEffect.setPos(hitObject, pos)
                    cameraShakerEffect.shakeSpeed = 0.06
                    cameraShakerEffect.shakePower = 4.0
                    cameraShakerEffect.numShakes = 2
                    cameraShakerEffect.scalePower = 1
                    cameraShakerEffect.play(300.0)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shipSplintersAEffect = ShipSplintersA.getEffect(unlimited)
                if shipSplintersAEffect:
                    shipSplintersAEffect.wrtReparentTo(hitObject)
                    shipSplintersAEffect.setPos(hitObject, pos)
                    shipSplintersAEffect.play()
        elif ammoSkillId == InventoryType.CannonFury:
            flashEffect = FlashEffect()
            flashEffect.wrtReparentTo(base.effectsRoot)
            flashEffect.setScale(300)
            flashEffect.setPos(hitObject, pos)
            flashEffect.effectColor = Vec4(0.5, 0.8, 1, 1)
            flashEffect.fadeTime = 0.25
            flashEffect.play()
        elif ammoSkillId == InventoryType.GrenadeExplosion:
            explosionEffect = ExplosionFlip.getEffect(unlimited)
            if explosionEffect:
                explosionEffect.reparentTo(base.effectsRoot)
                explosionEffect.setPos(hitObject, pos)
                explosionEffect.setScale(1.0)
                explosionEffect.play()
                self.playSfx(ammoSkillId, explosionEffect)
            smokeCloudEffect = SmokeCloud.getEffect(unlimited)
            if smokeCloudEffect:
                smokeCloudEffect.reparentTo(hitObject)
                smokeCloudEffect.setPos(hitObject, pos)
                smokeCloudEffect.setScale(1.0)
                smokeCloudEffect.spriteScale = 1.0
                smokeCloudEffect.radius = 7.0
                smokeCloudEffect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(base.effectsRoot)
                    shockwaveRingEffect.setPos(hitObject, pos)
                    shockwaveRingEffect.size = aoeRadius * 4
                    shockwaveRingEffect.play()
                flashEffect = MuzzleFlash.getEffect(unlimited)
                if flashEffect:
                    flashEffect.reparentTo(base.effectsRoot)
                    flashEffect.flash.setScale(100)
                    flashEffect.setPos(hitObject, pos)
                    flashEffect.startCol = Vec4(0.7, 0.7, 0.7, 1)
                    flashEffect.fadeTime = 0.2
                    flashEffect.play()
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.reparentTo(hitObject)
                cameraShakerEffect.setPos(hitObject, pos)
                cameraShakerEffect.shakeSpeed = 0.04
                cameraShakerEffect.shakePower = 6.0
                cameraShakerEffect.numShakes = 2
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(80.0)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                rockShower = SmallRockShower.getEffect(unlimited)
                if rockShower:
                    rockShower.reparentTo(hitObject)
                    rockShower.setPos(hitObject, pos)
                    rockShower.play()
        elif ammoSkillId == InventoryType.GrenadeShockBomb:
            explosionEffect = ExplosionFlip.getEffect(unlimited)
            if explosionEffect:
                explosionEffect.reparentTo(base.effectsRoot)
                explosionEffect.setPos(hitObject, pos)
                explosionEffect.setScale(1.0)
                explosionEffect.play()
                self.playSfx(ammoSkillId, explosionEffect)
            dustRingEffect = DustRing.getEffect(unlimited)
            if dustRingEffect:
                dustRingEffect.reparentTo(hitObject)
                dustRingEffect.setPos(hitObject, pos)
                dustRingEffect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(base.effectsRoot)
                    shockwaveRingEffect.setPos(hitObject, pos)
                    shockwaveRingEffect.size = aoeRadius * 4
                    shockwaveRingEffect.play()
                flashEffect = MuzzleFlash.getEffect(unlimited)
                if flashEffect:
                    flashEffect.reparentTo(base.effectsRoot)
                    flashEffect.flash.setScale(100)
                    flashEffect.setPos(hitObject, pos)
                    flashEffect.startCol = Vec4(0.7, 0.7, 0.7, 1)
                    flashEffect.fadeTime = 0.2
                    flashEffect.play()
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.reparentTo(hitObject)
                cameraShakerEffect.setPos(hitObject, pos)
                cameraShakerEffect.shakeSpeed = 0.04
                cameraShakerEffect.shakePower = 3.0
                cameraShakerEffect.numShakes = 2
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(80.0)
        elif ammoSkillId == InventoryType.GrenadeSiege:
            explosionEffect = ExplosionFlip.getEffect(unlimited)
            if explosionEffect:
                explosionEffect.reparentTo(base.effectsRoot)
                explosionEffect.setPos(hitObject, pos)
                explosionEffect.setScale(2.5)
                explosionEffect.play()
                self.playSfx(ammoSkillId, explosionEffect)
            smokePillarEffect = SmokePillar.getEffect(unlimited)
            if smokePillarEffect:
                smokePillarEffect.reparentTo(hitObject)
                smokePillarEffect.setPos(hitObject, pos)
                smokePillarEffect.setScale(1.0)
                smokePillarEffect.spriteScale = 1.0
                smokePillarEffect.radius = 7.0
                smokePillarEffect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                dustRingEffect = DustRing.getEffect(unlimited)
                if dustRingEffect:
                    dustRingEffect.reparentTo(hitObject)
                    dustRingEffect.setPos(hitObject, pos)
                    dustRingEffect.play()
                shockwaveRingEffect = ShockwaveRing.getEffect()
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(base.effectsRoot)
                    shockwaveRingEffect.setPos(hitObject, pos)
                    shockwaveRingEffect.size = aoeRadius * 4
                    shockwaveRingEffect.play()
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.wrtReparentTo(hitObject)
                cameraShakerEffect.setPos(hitObject, pos)
                cameraShakerEffect.shakeSpeed = 0.06
                cameraShakerEffect.shakePower = 4.0
                cameraShakerEffect.numShakes = 2
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(80.0)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shipSplintersAEffect = ShipSplintersA.getEffect(unlimited)
                if shipSplintersAEffect:
                    shipSplintersAEffect.reparentTo(hitObject)
                    shipSplintersAEffect.setPos(hitObject, pos)
                    shipSplintersAEffect.play()
                for i in range(random.randint(3, 6)):
                    debrisEffect = RockDebris.getEffect(unlimited)
                    if debrisEffect:
                        debrisEffect.reparentTo(base.effectsRoot)
                        debrisEffect.setPos(hitObject, pos)
                        debrisEffect.offsetEndPlaneZFrom(hitObject.getZ())
                        debrisEffect.debris.setScale(0.8)
                        debrisEffect.radiusDist = 30
                        debrisEffect.minHeight = 30
                        debrisEffect.maxHeight = 120
                        if debrisEffect.testTrajectory():
                            debrisEffect.play()
                        else:
                            debrisEffect.cleanUpEffect()

                flashEffect = MuzzleFlash.getEffect(unlimited)
                if flashEffect:
                    flashEffect.reparentTo(base.effectsRoot)
                    flashEffect.flash.setScale(200)
                    flashEffect.setPos(hitObject, pos)
                    flashEffect.startCol = Vec4(0.7, 0.7, 0.7, 1)
                    flashEffect.fadeTime = 0.2
                    flashEffect.play()
        elif ammoSkillId == InventoryType.GrenadeFireBomb:
            fireEffect = Fire.getEffect(unlimited)
            if fireEffect:
                fireEffect.wrtReparentTo(base.effectsRoot)
                fireEffect.setPos(hitObject, pos + Vec3(0, 0, -1.5))
                fireEffect.setScale(Vec3(0.75, 0.75, 0.75))
                fireEffect.duration = 2.5
                fireEffect.play()
            flashEffect = MuzzleFlash.getEffect(unlimited)
            if flashEffect:
                flashEffect.wrtReparentTo(base.effectsRoot)
                flashEffect.flash.setScale(100)
                flashEffect.setPos(hitObject, pos)
                flashEffect.startCol = Vec4(0.7, 0.7, 0.7, 1)
                flashEffect.fadeTime = 0.2
                flashEffect.play()
                self.playSfx(ammoSkillId, flashEffect)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.wrtReparentTo(base.effectsRoot)
                    shockwaveRingEffect.setPos(hitObject, pos)
                    shockwaveRingEffect.size = aoeRadius * 4
                    shockwaveRingEffect.play()
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.wrtReparentTo(hitObject)
                cameraShakerEffect.setPos(hitObject, pos)
                cameraShakerEffect.shakeSpeed = 0.04
                cameraShakerEffect.shakePower = 2.0
                cameraShakerEffect.numShakes = 2
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(80.0)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                blackSmokeEffect = LightSmoke.getEffect(unlimited)
                if blackSmokeEffect:
                    blackSmokeEffect.wrtReparentTo(base.effectsRoot)
                    blackSmokeEffect.setPos(hitObject, pos)
                    blackSmokeEffect.duration = 4.0
                    blackSmokeEffect.play()
        elif ammoSkillId == InventoryType.GrenadeSmokeCloud:
            explosionEffect = ExplosionFlip.getEffect(unlimited)
            if explosionEffect:
                explosionEffect.reparentTo(base.effectsRoot)
                explosionEffect.setPos(hitObject, pos)
                explosionEffect.setScale(1.0)
                explosionEffect.play()
                self.playSfx(ammoSkillId, explosionEffect)
            smokeCloudEffect = SmokeBomb.getEffect(unlimited)
            if smokeCloudEffect:
                smokeCloudEffect.reparentTo(hitObject)
                smokeCloudEffect.setPos(hitObject, pos)
                smokeCloudEffect.radius = aoeRadius / 1.5
                smokeCloudEffect.play()
                self.playSfx(ammoSkillId, smokeCloudEffect)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.wrtReparentTo(base.effectsRoot)
                    shockwaveRingEffect.setPos(hitObject, pos)
                    shockwaveRingEffect.size = aoeRadius * 4
                    shockwaveRingEffect.play()
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.wrtReparentTo(hitObject)
                cameraShakerEffect.setPos(hitObject, pos)
                cameraShakerEffect.shakeSpeed = 0.04
                cameraShakerEffect.shakePower = 2.0
                cameraShakerEffect.numShakes = 2
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(80.0)
        return

    def propHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def shipHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def avatarHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def blockerHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        for i in range(random.randint(2, 4)):
            debrisEffect = RockDebris.getEffect()
            if debrisEffect:
                debrisEffect.reparentTo(base.effectsRoot)
                debrisEffect.setPos(hitObject, pos)
                debrisEffect.offsetEndPlaneZFrom(hitObject.getZ())
                debrisEffect.debris.setScale(random.random() * 3)
                debrisEffect.radiusDist = 40
                debrisEffect.minHeight = 50
                debrisEffect.maxHeight = 100
                if debrisEffect.testTrajectory():
                    debrisEffect.play()
                else:
                    debrisEffect.cleanUpEffect()

    def groundHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        if ammoSkillId == InventoryType.CannonRoundShot or ammoSkillId == InventoryType.CannonChainShot or ammoSkillId == InventoryType.CannonBullet or ammoSkillId == InventoryType.CannonSkull or ammoSkillId == InventoryType.CannonBarShot:
            if self.cr:
                attacker = self.cr.doId2do.get(self.attackerId)
            else:
                attacker = None
            unlimited = bool(attacker and attacker.isLocal())
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                cannonExplosion = CannonExplosion.getEffect(unlimited)
                if cannonExplosion:
                    cannonExplosion.wrtReparentTo(base.effectsRoot)
                    cannonExplosion.setScale(1.0)
                    cannonExplosion.setPos(hitObject, pos)
                    cannonExplosion.play()
                rockShowerEffect = RockShower.getEffect(unlimited)
                if rockShowerEffect:
                    rockShowerEffect.wrtReparentTo(hitObject)
                    rockShowerEffect.setPos(hitObject, pos)
                    rockShowerEffect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                dustCloudEffect = DustCloud.getEffect(unlimited)
                if dustCloudEffect:
                    dustCloudEffect.wrtReparentTo(hitObject)
                    dustCloudEffect.setPos(hitObject, pos)
                    dustCloudEffect.play()
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.wrtReparentTo(base.effectsRoot)
                    shockwaveRingEffect.size = 40
                    shockwaveRingEffect.setPos(hitObject, pos)
                    shockwaveRingEffect.play()
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.wrtReparentTo(hitObject)
                cameraShakerEffect.setPos(hitObject, pos)
                cameraShakerEffect.shakeSpeed = 0.06
                cameraShakerEffect.shakePower = 6.0
                cameraShakerEffect.numShakes = 3
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(80.0)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                dirtClodEffect = DirtClod.getEffect(unlimited)
                if dirtClodEffect:
                    dirtClodEffect.wrtReparentTo(hitObject)
                    dirtClodEffect.setPos(hitObject, pos)
                    dirtClodEffect.play()
        else:
            self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)
        return

    def buildingHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def waterHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        np = render.attachNewNode('temp')
        np.setPos(hitObject, pos)
        pos = np.getPos(render)
        np.removeNode()
        if self.cr:
            if self.cr.activeWorld.getWater():
                entryWaterHeight = base.cr.activeWorld.getWater().calcHeight(pos[0], pos[1])
            else:
                entryWaterHeight = pos[2]
        else:
            entryWaterHeight = pos[2]
        if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
            splashEffect = CannonSplash.getEffect()
            if splashEffect:
                splashEffect.wrtReparentTo(render)
                splashEffect.setPos(pos[0], pos[1], entryWaterHeight)
                splashEffect.play()

    def monsterHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        if ammoSkillId == InventoryType.CannonRoundShot or ammoSkillId == InventoryType.CannonChainShot or ammoSkillId == InventoryType.CannonBullet or ammoSkillId == InventoryType.CannonSkull or ammoSkillId == InventoryType.CannonBarShot:
            pass
        else:
            self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def grappleHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        if ammoSkillId == InventoryType.CannonGrappleHook:
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                hitFlashA = HitFlashA.getEffect()
                if hitFlashA:
                    hitFlashA.wrtReparentTo(base.effectsRoot)
                    hitFlashA.setPos(hitObject, pos)
                    hitFlashA.play()
        else:
            self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def cannonHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)

    def fortHitEffect(self, hitObject, pos, skillId, ammoSkillId):
        self.basicHitEffect(hitObject, pos, skillId, ammoSkillId)