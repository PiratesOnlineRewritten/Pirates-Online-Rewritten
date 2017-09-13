import WeaponGlobals
from direct.interval.IntervalGlobal import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from pandac.PandaModules import *
from direct.actor import Actor
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.effects.DaggerProjectile import DaggerProjectile
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.ThrowDirt import ThrowDirt
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.effects.DustRing import DustRing
from pirates.effects.WindBlurCone import WindBlurCone
from pirates.effects.VenomSpitProjectile import VenomSpitProjectile
from pirates.effects.HomingMissile import HomingMissile
from pirates.effects.DaggerProjectile import DaggerProjectile
from pirates.effects.WispSpiral import WispSpiral
from pirates.effects.AttuneSmoke import AttuneSmoke
from pirates.effects.MusketSmoke import MusketSmoke
from pirates.effects.MusketFlame import MusketFlame
from pirates.effects.PistolSmoke import PistolSmoke
from pirates.effects.PistolFlame import PistolFlame
from pirates.effects.BeamEffect import BeamEffect
from pirates.effects.SoulHarvest import SoulHarvest
from pirates.effects.DomeExplosion import DomeExplosion
from pirates.effects.DarkPortal import DarkPortal
from pirates.effects.UnholyFlare import UnholyFlare
from pirates.effects.NovaStar import NovaStar
from pirates.effects.HomingMissile import HomingMissile
from pirates.effects.DarkStar import DarkStar
from pirates.effects.Pestilence import Pestilence
from pirates.effects.VoodooProjectile import VoodooProjectile
from pirates.effects.FlamingSkull import FlamingSkull
from pirates.effects.JollySoulDrain import JollySoulDrain
from pirates.effects.VoodooFire import VoodooFire
from pirates.effects.WitherCharge import WitherCharge
from pirates.effects.EvilRingEffect import EvilRingEffect
from pirates.effects.VoodooPestilence import VoodooPestilence
from pirates.effects.SoulFlay import SoulFlay
from pirates.effects.VoodooSouls import VoodooSouls
from pirates.effects.VoodooGlow import VoodooGlow
from pirates.effects.SoulSpiral import SoulSpiral
from pirates.effects.EnergySpiral import EnergySpiral
from pirates.effects.VoodooAura import VoodooAura
from pirates.effects.VoodooAura2 import VoodooAura2
from pirates.effects.VoodooPower import VoodooPower
from pirates.effects.WindWave import WindWave
from pirates.effects.DesolationSmoke import DesolationSmoke
from pirates.effects.WindCharge import WindCharge
from pirates.effects.DesolationChargeSmoke import DesolationChargeSmoke
from pirates.effects.SoulHarvest2 import SoulHarvest2
from pirates.effects.VoodooStaffFire import VoodooStaffFire
from pirates.effects.MuzzleFlash import MuzzleFlash
from pirates.effects.SpectralTrail import SpectralTrail
from pirates.effects.SpectralSmoke import SpectralSmoke
from pirates.effects.HealSparks import HealSparks
from pirates.effects.FadingCard import FadingCard
from pirates.effects.JRSoulHarvest import JRSoulHarvest
from pirates.effects.JRSoulHarvest2 import JRSoulHarvest2
from pirates.effects.JRGraveSmoke import JRGraveSmoke
from pirates.effects.GrapeshotEffect import GrapeshotEffect
from pirates.effects.PistolShot import PistolShot
from pirates.effects.ScatterShot import ScatterShot
from pirates.effects.MusketShot import MusketShot
from pirates.effects.VoodooAuraBurst import VoodooAuraBurst
from pirates.effects.FlashEffect import FlashEffect
from pirates.effects.HealBlast import HealBlast
from pirates.effects.PulsingGlow import PulsingGlow
from pirates.effects.ConeRays import ConeRays
from pirates.effects.VoodooAuraHeal import VoodooAuraHeal
from pirates.effects.VoodooAuraDisc import VoodooAuraDisc
from pirates.effects.VoodooGroundAura import VoodooGroundAura
from pirates.effects.HitPulse import HitPulse
from pirates.effects.SimpleSmokeCloud import SimpleSmokeCloud
from pirates.effects.MonkeyPanicHit import MonkeyPanicHit
from GrenadeProjectile import GrenadeProjectile
from pirates.piratesbase import PLocalizer
from pirates.inventory import ItemGlobals
from pirates.battle.EnemySkills import *
import random
import copy
from direct.showbase.InputStateGlobal import inputState
MISTIMEDLIST = [
 WeaponGlobals.RESULT_MISTIMED_MISS, WeaponGlobals.RESULT_MISTIMED_HIT]

class CombatAnimations():
    notify = directNotify.newCategory('CombatAnimations')
    BASE_GRENADE_POWER = 0.8

    def getHack(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        delay = 0.625
        if av == localAvatar and av.guiMgr.combatTray.onLastAttack:
            delay = 0.85
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.startSpecialEffect, skillId), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=4, endFrame=30, blendInT=0.2, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(delay), Func(self.unlockInput, av)))
        return ival

    def getSlash(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        delay = 0.75
        if av == localAvatar and av.guiMgr.combatTray.onLastAttack:
            delay = 1.3
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.3), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=31, endFrame=62, blendInT=0.5, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(delay), Func(self.unlockInput, av)))
        return ival

    def getCleave(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        delay = 1.25
        if av == localAvatar and av.guiMgr.combatTray.onLastAttack:
            delay = 1.5
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=63, endFrame=101, blendInT=0.5, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(delay), Func(self.unlockInput, av)))
        return ival

    def getFlourish(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        delay = 1.58
        if av == localAvatar and av.guiMgr.combatTray.onLastAttack:
            delay = 2.08
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=102, endFrame=150, blendInT=0.5, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(delay), Func(self.unlockInput, av)))
        return ival

    def getThrust(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        delay = 1.8
        if av.isLocal() and av.guiMgr.combatTray.onLastAttack:
            delay = 2.05
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0

        def startVFX():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = WindBlurCone.getEffect(unlimited)
                if effect and not av.currentWeapon.isEmpty():
                    colorId = ItemGlobals.getVfxType1(av.currentWeapon.itemId)
                    if colorId == ItemGlobals.MotionBlurDark:
                        effect.setBlendModeOff()
                    else:
                        effect.setBlendModeOn()
                    effect.fadeColor = av.currentWeapon.getBlurColor()
                    effect.reparentTo(av.currentWeapon)
                    effect.fadeTime = 0.4
                    effect.setPos(0, 0, 0)
                    effect.setScale(1)
                    effect.setH(0)
                    effect.play()

        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.5), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=151, endFrame=164, blendInT=0.5, blendOutT=0), Func(av.currentWeapon.showSpinBlur), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=165, endFrame=170, blendInT=0, blendOutT=0), Func(startVFX), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=171, endFrame=175, blendInT=0, blendOutT=0), Func(av.currentWeapon.hideSpinBlur), av.actorInterval('cutlass_combo', playRate=1.0, startFrame=176, endFrame=210, blendInT=0, blendOutT=0.5), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(delay), Func(self.unlockInput, av)))
        return ival

    def getSweep(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(av)
                    shockwaveRingEffect.size = 40
                    shockwaveRingEffect.setPos(0, 0, 0)
                    shockwaveRingEffect.play()

        def startVFX2():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(av)
                    shockwaveRingEffect.size = 40
                    shockwaveRingEffect.setPos(0, 0, 3)
                    shockwaveRingEffect.play()
                dustRingEffect = DustRing.getEffect(unlimited)
                if dustRingEffect:
                    dustRingEffect.reparentTo(av)
                    dustRingEffect.setPos(0, 0, 0)
                    dustRingEffect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.7), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=1, endFrame=10, blendOutT=0), Func(startVFX), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=11, endFrame=15, blendInT=0, blendOutT=0), Func(startVFX2), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=16, endFrame=35, blendInT=0), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getBlowbackSweep(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            effect = CameraShaker()
            effect.reparentTo(av)
            effect.setPos(0, 0, 0)
            effect.shakeSpeed = 0.06
            effect.shakePower = 2.5
            effect.numShakes = 3
            effect.scalePower = 1
            effect.play(300)
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(av)
                    shockwaveRingEffect.size = 40
                    shockwaveRingEffect.setPos(0, 0, 0)
                    shockwaveRingEffect.play()

        def startVFX2():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = VoodooAuraBurst.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av)
                    effect.setPos(0, 0, 0.25)
                    effect.setEffectColor(Vec4(0.15, 0.15, 0.15, 1.0))
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                dustRingEffect = DustRing.getEffect(unlimited)
                if dustRingEffect:
                    dustRingEffect.reparentTo(av)
                    dustRingEffect.setPos(0, 0, 0)
                    dustRingEffect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.7), Func(av.currentWeapon.beginAttack, av), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=1, endFrame=10, blendOutT=0), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=11, endFrame=15, blendInT=0, blendOutT=0), Func(startVFX2), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=16, endFrame=35, blendInT=0), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getFireSweep(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            effect = CameraShaker()
            effect.reparentTo(av)
            effect.setPos(0, 0, 0)
            effect.shakeSpeed = 0.06
            effect.shakePower = 2.5
            effect.numShakes = 3
            effect.scalePower = 1
            effect.play(300)
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(av)
                    shockwaveRingEffect.size = 40
                    shockwaveRingEffect.setPos(0, 0, 0)
                    shockwaveRingEffect.play()

        def startVFX2():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = VoodooAuraBurst.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av)
                    effect.setPos(0, 0, 0.25)
                    effect.setEffectColor(Vec4(1, 0.8, 0.4, 0.4))
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                dustRingEffect = DustRing.getEffect(unlimited)
                if dustRingEffect:
                    dustRingEffect.reparentTo(av)
                    dustRingEffect.setPos(0, 0, 0)
                    dustRingEffect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.motionFSM.off), Func(av.currentWeapon.startSpecialEffect, skillId), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.7), Func(av.currentWeapon.beginAttack, av), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=1, endFrame=10, blendOutT=0), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=11, endFrame=15, blendInT=0, blendOutT=0), Func(startVFX2), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=16, endFrame=35, blendInT=0), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getIceSweep(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            effect = CameraShaker()
            effect.reparentTo(av)
            effect.setPos(0, 0, 0)
            effect.shakeSpeed = 0.06
            effect.shakePower = 2.5
            effect.numShakes = 3
            effect.scalePower = 1
            effect.play(300)
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(av)
                    shockwaveRingEffect.size = 40
                    shockwaveRingEffect.setPos(0, 0, 0)
                    shockwaveRingEffect.play()

        def startVFX2():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = VoodooAuraBurst.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av)
                    effect.setPos(0, 0, 0.25)
                    effect.setEffectColor(Vec4(0.4, 0.6, 1, 0.6))
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                dustRingEffect = DustRing.getEffect(unlimited)
                if dustRingEffect:
                    dustRingEffect.reparentTo(av)
                    dustRingEffect.setPos(0, 0, 0)
                    dustRingEffect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.motionFSM.off), Func(av.currentWeapon.startSpecialEffect, skillId), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.7), Func(av.currentWeapon.beginAttack, av), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=1, endFrame=10, blendOutT=0), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=11, endFrame=15, blendInT=0, blendOutT=0), Func(startVFX2), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=16, endFrame=35, blendInT=0), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getThunderSweep(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            effect = CameraShaker()
            effect.reparentTo(av)
            effect.setPos(0, 0, 0)
            effect.shakeSpeed = 0.06
            effect.shakePower = 2.5
            effect.numShakes = 3
            effect.scalePower = 1
            effect.play(300)
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(av)
                    shockwaveRingEffect.size = 40
                    shockwaveRingEffect.setPos(0, 0, 0)
                    shockwaveRingEffect.play()

        def startVFX2():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = VoodooAuraBurst.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av)
                    effect.setPos(0, 0, 0.25)
                    effect.setEffectColor(Vec4(0.7, 0.9, 0.5, 0.5))
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                dustRingEffect = DustRing.getEffect(unlimited)
                if dustRingEffect:
                    dustRingEffect.reparentTo(av)
                    dustRingEffect.setPos(0, 0, 0)
                    dustRingEffect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.motionFSM.off), Func(av.currentWeapon.startSpecialEffect, skillId), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.7), Func(av.currentWeapon.beginAttack, av), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=1, endFrame=10, blendOutT=0), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=11, endFrame=15, blendInT=0, blendOutT=0), Func(startVFX2), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=16, endFrame=35, blendInT=0), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getFurySweep(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
                if shockwaveRingEffect:
                    shockwaveRingEffect.reparentTo(av)
                    shockwaveRingEffect.size = 40
                    shockwaveRingEffect.setPos(0, 0, 0)
                    shockwaveRingEffect.play()

        def startVFX2():
            unlimited = av.isLocal()
            shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
            if shockwaveRingEffect:
                shockwaveRingEffect.reparentTo(av)
                shockwaveRingEffect.size = 40
                shockwaveRingEffect.setPos(0, 0, 1)
                shockwaveRingEffect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                dustRingEffect = DustRing.getEffect(unlimited)
                if dustRingEffect:
                    dustRingEffect.reparentTo(av)
                    dustRingEffect.setPos(0, 0, 0)
                    dustRingEffect.play()

        def startVFX3():
            unlimited = av.isLocal()
            shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
            if shockwaveRingEffect:
                shockwaveRingEffect.reparentTo(av)
                shockwaveRingEffect.size = 40
                shockwaveRingEffect.setPos(0, 0, 2)
                shockwaveRingEffect.play()

        def startVFX4():
            unlimited = av.isLocal()
            shockwaveRingEffect = ShockwaveRing.getEffect(unlimited)
            if shockwaveRingEffect:
                shockwaveRingEffect.reparentTo(av)
                shockwaveRingEffect.size = 40
                shockwaveRingEffect.setPos(0, 0, 3)
                shockwaveRingEffect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.7), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=1, endFrame=10, blendOutT=0), Func(startVFX), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=11, endFrame=18, blendInT=0, blendOutT=0), Func(startVFX2), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=18, endFrame=26, blendInT=0, blendOutT=0), Func(startVFX3), av.actorInterval('cutlass_sweep', playRate=1.0, startFrame=26, endFrame=35, blendInT=0.0), Func(startVFX4), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getBladestorm(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.55), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_bladestorm', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getBrawl(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.3), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av))
        ival.append(av.actorInterval('cutlass_headbutt', playRate=1.0, blendInT=0.5, blendOutT=0.5))
        ival.append(Func(av.currentWeapon.endAttack, av))
        ival.append(Func(av.considerEnableMovement))
        ival.append(Func(self.unlockInput, av))
        return ival

    def getTaunt(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.setChatAbsolute, PLocalizer.getTauntPhrase(), CFSpeech | CFTimeout), Func(av.currentWeapon.setTrailLength, 0.15), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cutlass_taunt', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getCower(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.setChatAbsolute, PLocalizer.getNotInFacePhrase(), CFSpeech | CFTimeout), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('cower_in_place', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getMonkeyPanic(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            flashEffect = FlashEffect()
            flashEffect.reparentTo(av.headNode)
            flashEffect.setScale(15.0)
            flashEffect.fadeTime = 1.0
            flashEffect.setEffectColor(Vec4(1, 0.2, 0.2, 1))
            flashEffect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = MonkeyPanicHit.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av.headNode)
                    effect.setPos(-1, 0, 0)
                    effect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.15), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), Func(startVFX), av.actorInterval('emote_thriller', playRate=1.0, startFrame=265, endFrame=320, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getBroadswordHack(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('broadsword_combo', playRate=1.0, startFrame=1, endFrame=28, blendInT=0.1, blendOutT=0.1), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(0.85), Func(self.unlockInput, av)))
        return ival

    def getBroadswordSlash(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.3), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('broadsword_combo', playRate=1.0, startFrame=29, endFrame=60, blendInT=0.5, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(0.95), Func(self.unlockInput, av)))
        return ival

    def getBroadswordCleave(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('broadsword_combo_motion', playRate=1.0, startFrame=61, endFrame=76, blendInT=0.1, blendOutT=0), av.actorInterval('broadsword_combo', playRate=1.0, startFrame=77, endFrame=96, blendInT=0, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(1.05), Func(self.unlockInput, av)))
        return ival

    def getBroadswordFlourish(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('broadsword_combo_motion', playRate=1.0, startFrame=97, endFrame=112, blendInT=0.1, blendOutT=0), av.actorInterval('broadsword_combo', playRate=1.0, startFrame=113, endFrame=128, blendInT=0, blendOutT=0), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(0.95), Func(self.unlockInput, av)))
        return ival

    def getBroadswordThrust(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        wantTrail = 1
        delay = 1.0
        if av.isLocal() and av.guiMgr.combatTray.onLastAttack:
            delay = 1.45
        if skillResult in MISTIMEDLIST:
            wantTrail = 0

        def startVFX():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = WindBlurCone.getEffect(unlimited)
                if effect and not av.currentWeapon.isEmpty():
                    colorId = ItemGlobals.getVfxType1(av.currentWeapon.itemId)
                    if colorId == ItemGlobals.MotionBlurDark:
                        effect.setBlendModeOff()
                    else:
                        effect.setBlendModeOn()
                    effect.fadeColor = av.currentWeapon.getBlurColor()
                    effect.reparentTo(av.currentWeapon)
                    effect.fadeTime = 0.4
                    effect.setPos(0, 0, 0)
                    effect.setScale(1)
                    effect.setH(0)
                    effect.play()

        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.5), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('broadsword_combo_motion', playRate=1.0, startFrame=129, endFrame=148, blendInT=0.5, blendOutT=0), av.actorInterval('broadsword_combo', playRate=1.0, startFrame=149, endFrame=170, blendInT=0, blendOutT=0), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(delay), Func(self.unlockInput, av)))
        return ival

    def getSabreHack(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('sabre_combo', playRate=1.0, startFrame=1, endFrame=19, blendInT=0.2, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(0.425), Func(self.unlockInput, av)))
        return ival

    def getSabreSlash(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.3), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('sabre_combo', playRate=1.0, startFrame=20, endFrame=37, blendInT=0.1, blendOutT=0.1), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(0.4), Func(self.unlockInput, av)))
        return ival

    def getSabreCleave(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('sabre_combo', playRate=1.0, startFrame=38, endFrame=81, blendInT=0.5, blendOutT=0.3), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getSabreFlourish(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('sabre_combo_motion', playRate=1.0, startFrame=82, endFrame=94, blendInT=0.1, blendOutT=0), av.actorInterval('sabre_combo', playRate=1.0, startFrame=95, endFrame=121, blendInT=0, blendOutT=0.1), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getSabreThrust(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        delay = 1.3
        if av.isLocal() and av.guiMgr.combatTray.onLastAttack:
            delay = 1.55
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0

        def startVFX():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = WindBlurCone.getEffect(unlimited)
                if effect and not av.currentWeapon.isEmpty():
                    colorId = ItemGlobals.getVfxType1(av.currentWeapon.itemId)
                    if colorId == ItemGlobals.MotionBlurDark:
                        effect.setBlendModeOff()
                    else:
                        effect.setBlendModeOn()
                    effect.fadeColor = av.currentWeapon.getBlurColor()
                    effect.reparentTo(av.currentWeapon)
                    effect.fadeTime = 0.4
                    effect.setPos(0, 0, 0)
                    effect.setScale(1)
                    effect.setH(0)
                    effect.play()

        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.5), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('sabre_combo_motion', playRate=1.0, startFrame=122, endFrame=147, blendInT=0.5, blendOutT=0), av.actorInterval('sabre_combo', playRate=1.0, startFrame=148, endFrame=175, blendInT=0, blendOutT=0), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(delay), Func(self.unlockInput, av)))
        return ival

    def getCut(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        delay = 0.75
        if av == localAvatar and av.guiMgr.combatTray.onLastAttack:
            delay = 1.25
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('dagger_combo', playRate=1.0, startFrame=1, endFrame=28, blendInT=0.2, blendOutT=0.5), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(delay), Func(self.unlockInput, av)))
        return ival

    def getSwipe(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        delay = 0.583
        if av == localAvatar and av.guiMgr.combatTray.onLastAttack:
            delay = 1.083
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.3), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('dagger_combo', playRate=1.0, startFrame=29, endFrame=53, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.hideSpinBlur), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(delay), Func(self.unlockInput, av)), Sequence(Wait(0.1), Func(av.currentWeapon.showSpinBlur)))
        return ival

    def getGouge(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        delay = 0.958
        if av == localAvatar and av.guiMgr.combatTray.onLastAttack:
            delay = 1.458
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.5), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('dagger_combo', playRate=1.0, startFrame=54, endFrame=87, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(delay), Func(self.unlockInput, av)))
        return ival

    def getEviscerate(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        delay = 1.9
        if av == localAvatar and av.guiMgr.combatTray.onLastAttack:
            delay = 2.4
        wantTrail = 1
        if skillResult in MISTIMEDLIST:
            wantTrail = 0
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.6), Func(av.currentWeapon.beginAttack, av, wantTrail), Func(av.currentWeapon.playSkillSfx, skillId, av, 0, wantTrail), av.actorInterval('dagger_combo', playRate=1.0, startFrame=88, endFrame=142, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av)), Sequence(Wait(delay), Func(self.unlockInput, av)))
        return ival

    def throwDagger(self, av, time, targetPos, motion_color=None, startOffset=Vec3(0, 0, 0), roll=0, leftHand=False, skillId=None, target=None):
        if av:
            if skillId:
                targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
                time *= speed
            roll += random.uniform(-15.0, 15.0)
            effect = DaggerProjectile.getEffect()
            if effect:
                effect.reparentTo(render)
                if leftHand:
                    effect.setPos(av.leftHandNode, startOffset)
                else:
                    effect.setPos(av.rightHandNode, startOffset)
                effect.setHpr(av.getH(render) + roll, 90 + roll, roll)
                effect.play(time, targetPos, motion_color)

    def throwDaggerRain(self, av, time, targetPos, motion_color=None, startOffset=Vec3(0, 0, 0), roll=0, leftHand=False, skillId=None, target=None):
        if av:
            if skillId:
                targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
                newTargetPos = Point3(targetPos.getX() + random.uniform(-2.0, 2.0), targetPos.getY() + random.uniform(-2.0, 2.0), targetPos.getZ())
                time *= speed
            roll += random.uniform(-15.0, 15.0)
            effect = DaggerProjectile.getEffect()
            if effect:
                effect.reparentTo(render)
                if leftHand:
                    effect.setPos(av.leftHandNode, startOffset)
                else:
                    effect.setPos(av.rightHandNode, startOffset)
                effect.setHpr(av.getH(render) + roll, 90 + roll, roll)
                effect.play(time, newTargetPos, motion_color)

    def getDaggerThrowDirtInterval(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            effect = ThrowDirt.getEffect(unlimited)
            if effect:
                effect.reparentTo(render)
                effect.setPos(av.getPos(render))
                effect.setHpr(av.getHpr(render))
                effect.particleDummy.setPos(av.getPos(render))
                effect.particleDummy.setHpr(av.getHpr(render))
                effect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(base.disableMouse), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.hideWeapon), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_throw_sand', playRate=1.0, startFrame=1, endFrame=10, blendInT=0.2, blendOutT=0), Func(av.currentWeapon.playSkillSfx, skillId, av), Func(startVFX), av.actorInterval('dagger_throw_sand', playRate=1.0, startFrame=11, endFrame=38, blendInT=0, blendOutT=0.3), Func(av.currentWeapon.showWeapon), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getDaggerAspInterval(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('knife_throw', endFrame=17, blendInT=0.2, blendOutT=0), Parallel(av.actorInterval('knife_throw', startFrame=18, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, speed, targetPos, skillId=skillId, target=target), Func(av.currentWeapon.hideWeapon)), Func(av.currentWeapon.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerAdderInterval(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        motion_color = [
         Vec4(0.1, 1.0, 0.4, 1.0), Vec4(0.5, 1.0, 0.4, 1.0)]
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('knife_throw', endFrame=17, blendInT=0.2, blendOutT=0), Parallel(av.actorInterval('knife_throw', startFrame=18, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, 1.0, targetPos, motion_color, skillId=skillId, target=target), Func(av.currentWeapon.hideWeapon)), Func(av.currentWeapon.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerSidewinderInterval(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        motion_color = [
         Vec4(1.0, 0.0, 0.0, 1.0), Vec4(1.0, 0.2, 0.0, 1.0)]
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('dagger_asp', endFrame=7, blendInT=0.1, blendOutT=0), Parallel(av.actorInterval('dagger_asp', startFrame=8, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, 1.0, targetPos, motion_color, roll=90, skillId=skillId, target=target), Func(av.currentWeapon.hideWeapon)), Func(av.currentWeapon.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerViperNestInterval(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        numDaggers = 12.0
        time = 0.7
        placeHolder = av.attachNewNode('daggerPlaceHolder')
        daggerTossIval = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.25), av.actorInterval('dagger_vipers_nest', startFrame=21, endFrame=35, blendInT=0, blendOutT=0.4), Func(av.currentWeapon.showWeapon), Func(av.considerEnableMovement), Func(self.unlockInput, av)))
        for i in range(numDaggers):
            if av.isLocal():
                placeHolder.setPos(camera, random.uniform(-12, 12), random.uniform(100, 120), random.uniform(8, 18))
            else:
                placeHolder.setPos(av, random.uniform(-12, 12), random.uniform(100, 120), random.uniform(2, 12))
            targetPos = placeHolder.getPos(render)
            daggerTossIval.append(Func(self.throwDagger, av, time + random.uniform(-0.5, 1.0), targetPos, startOffset=Vec3(-3, 0, 0), roll=90))

        placeHolder.removeNode()
        track = Sequence(Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.hideWeapon), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('dagger_vipers_nest', endFrame=20, blendOutT=0), daggerTossIval)
        return track

    def getDaggerBarrageInterval(self, av, skillId, ammoSkillId, charge, target, skillResult, areaList=[]):
        if not av.currentWeapon:
            return None
        motion_color = [
         Vec4(1.0, 0.0, 0.0, 1.0), Vec4(1.0, 0.2, 0.0, 1.0)]
        numDaggers = 6.0
        time = 0.7
        placeHolder = av.attachNewNode('daggerPlaceHolder')
        placeHolder2 = placeHolder.attachNewNode('daggerPlaceHolder2')
        daggerTossIval = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.25), av.actorInterval('dagger_vipers_nest', startFrame=21, endFrame=35, blendInT=0, blendOutT=0.4), Func(av.currentWeapon.showWeapon), Func(av.considerEnableMovement), Func(self.unlockInput, av)))
        if target:
            targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
            daggerTossIval.append(Func(self.throwDagger, av, speed, targetPos, motion_color, startOffset=Vec3(-3, 0, 0), roll=90))
        for enemy in areaList:
            targetPos, speed, impactT = av.getProjectileInfo(skillId, enemy)
            daggerTossIval.append(Func(self.throwDagger, av, speed, targetPos, motion_color, startOffset=Vec3(-3, 0, 0), roll=90))

        if av.isLocal():
            placeHolder.setPos(camera, 0, 0, 0)
        else:
            placeHolder.setPos(av, 0, 0, 0)
        for i in range(numDaggers):
            placeHolder.setH(i * 360 / numDaggers)
            placeHolder2.setPos(0, random.uniform(100, 120), random.uniform(2, 12))
            targetPos = placeHolder2.getPos(render)
            daggerTossIval.append(Func(self.throwDagger, av, time + random.uniform(-0.5, 1.0), targetPos, motion_color, startOffset=Vec3(-3, 0, 0), roll=90))

        placeHolder.removeNode()
        track = Sequence(Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.hideWeapon), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('dagger_vipers_nest', endFrame=20, blendOutT=0), daggerTossIval)
        return track

    def getDaggerThrowCombo1Interval(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        motion_color = [
         Vec4(1.0, 0.0, 0.0, 1.0), Vec4(1.0, 0.2, 0.0, 1.0)]
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('dagger_throw_combo', endFrame=6, playRate=1.5, blendInT=0.1, blendOutT=0), Parallel(av.actorInterval('dagger_throw_combo', startFrame=7, endFrame=23, playRate=1.5, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, 0.5, targetPos, motion_color, skillId=skillId, target=target), Func(av.currentWeapon.hideWeapon)), Func(av.currentWeapon.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerThrowCombo2Interval(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        motion_color = [
         Vec4(1.0, 0.0, 0.0, 1.0), Vec4(1.0, 0.2, 0.0, 1.0)]
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(av.currentWeapon.reparentTo, av.leftHandNode), Func(av.attackTire), Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('dagger_throw_combo', startFrame=24, endFrame=30, playRate=1.5, blendInT=0.1, blendOutT=0), Parallel(av.actorInterval('dagger_throw_combo', startFrame=31, endFrame=46, playRate=1.5, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, 0.5, targetPos, motion_color, leftHand=True, skillId=skillId, target=target), Func(av.currentWeapon.hideWeapon)), Func(av.currentWeapon.reparentTo, av.rightHandNode), Func(av.currentWeapon.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerThrowCombo3Interval(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return
        motion_color = [
         Vec4(1.0, 0.0, 0.0, 1.0), Vec4(1.0, 0.2, 0.0, 1.0)]
        dagger2 = copy.copy(av.currentWeapon)
        av.setSecondWeapon(dagger2)
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(dagger2.reparentTo, av.leftHandNode), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('dagger_throw_combo', startFrame=47, endFrame=56, playRate=1.5, blendInT=0.1, blendOutT=0), Parallel(av.actorInterval('dagger_throw_combo', startFrame=57, endFrame=78, playRate=1.5, blendInT=0, blendOutT=0.1), Func(self.throwDagger, av, 0.5, targetPos, motion_color, skillId=skillId, target=target), Sequence(Wait(0.011), Func(self.throwDagger, av, 0.5, targetPos, motion_color, leftHand=True, skillId=skillId, target=target)), Func(av.setSecondWeapon, None), Func(av.currentWeapon.hideWeapon)), Func(av.currentWeapon.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerThrowCombo4Interval(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return
        motion_color = [
         Vec4(1.0, 0.0, 0.0, 1.0), Vec4(1.0, 0.2, 0.0, 1.0)]
        dagger2 = copy.copy(av.currentWeapon)
        av.setSecondWeapon(dagger2)
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(dagger2.reparentTo, av.leftHandNode), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('dagger_throw_combo', startFrame=79, endFrame=93, playRate=1.5, blendInT=0.1, blendOutT=0), Parallel(av.actorInterval('dagger_throw_combo', startFrame=94, endFrame=130, playRate=1.5, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, 0.5, targetPos, motion_color, roll=90, skillId=skillId, target=target), Sequence(Wait(0.011), Func(self.throwDagger, av, 0.5, targetPos, motion_color, roll=90, leftHand=True, skillId=skillId, target=target)), Func(av.setSecondWeapon, None), Func(av.currentWeapon.hideWeapon)), Func(av.currentWeapon.showWeapon), Func(self.unlockInput, av))
        return track

    def getDaggerRainInterval(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        motion_color = [
         Vec4(1.0, 0.0, 0.0, 1.0), Vec4(1.0, 0.2, 0.0, 1.0)]
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        numDaggers = 3.0
        daggerTossIval = Parallel(Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.25), av.actorInterval('dagger_asp', startFrame=7, endFrame=20, blendInT=0, blendOutT=0.4), Func(av.currentWeapon.showWeapon), Func(av.considerEnableMovement), Func(self.unlockInput, av)))
        for i in range(numDaggers):
            daggerTossIval.append(Wait(0.011 * i))
            daggerTossIval.append(Func(self.throwDaggerRain, av, random.uniform(0.95, 1.05), targetPos, motion_color, roll=90, skillId=skillId, target=target))

        track = Sequence(Func(av.motionFSM.off), Func(av.attackTire), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.hideWeapon), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('dagger_asp', endFrame=6, blendOutT=0), daggerTossIval)
        return track

    def getDaggerAcidDaggerInterval(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        motion_color = [
         Vec4(1.0, 1.0, 0.0, 1.0), Vec4(1.0, 1.0, 0.2, 1.0)]
        targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
        track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('dagger_asp', endFrame=7, blendInT=0.1, blendOutT=0), Parallel(av.actorInterval('dagger_asp', startFrame=8, blendInT=0, blendOutT=0.4), Func(self.throwDagger, av, 1.0, targetPos, motion_color, roll=90, skillId=skillId, target=target), Func(av.currentWeapon.hideWeapon)), Func(av.currentWeapon.showWeapon), Func(self.unlockInput, av))
        return track

    def getPistolChargingAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        subtype = ItemGlobals.getSubtype(av.currentWeaponId)
        anim = ItemGlobals.getChargingAnim(subtype)
        if ItemGlobals.shouldStopToAim(subtype):
            track = Sequence(Func(av.motionFSM.moveLock), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(av.setAimMod, -0.5), av.actorInterval(anim, loop=1, duration=9999, blendInT=0.3, blendOutT=0.3))
        elif anim:
            track = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 1), Func(av.setAimMod, -0.5), av.actorInterval(anim, loop=1, duration=9999, blendInT=0.3, blendOutT=0.3))
        else:
            track = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 1), Func(av.setAimMod, -0.5), av.actorInterval('gun_aim_idle', loop=1, duration=9999, blendInT=0.3, blendOutT=0.3))
        return track

    def getPistolReloadAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return

        def finishReload():
            if av.isLocal():
                messenger.send('reloadFinished')

        if ItemGlobals.getType(av.currentWeaponId) == ItemGlobals.GUN:
            sfx = av.currentWeapon.reloadSfx
        else:
            sfx = None
        anim = ItemGlobals.getReloadAnim(ItemGlobals.getSubtype(av.currentWeaponId))
        if anim:
            if ItemGlobals.getSubtype(av.currentWeaponId) == ItemGlobals.BLUNDERBUSS:
                ramRod = av.currentWeapon.getRamRod()
                track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.setAimMod, 0), Func(base.playSfx, sfx, node=av, cutoff=60), av.actorInterval(anim, startFrame=1, endFrame=13, blendInT=0, blendOutT=0), Func(ramRod.reparentTo, av.leftHandNode), av.actorInterval(anim, startFrame=14, endFrame=68, blendInT=0, blendOutT=0), Func(ramRod.detachNode), av.actorInterval(anim, startFrame=69, endFrame=110, blendInT=0, blendOutT=0), Func(finishReload), Func(self.unlockInput, av))
            else:
                track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.setAimMod, 0), Func(base.playSfx, sfx, node=av, cutoff=60), av.actorInterval(anim, blendInT=0, blendOutT=0), Func(finishReload), Func(self.unlockInput, av))
        else:
            track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.setAimMod, 0), Func(base.playSfx, sfx, node=av, cutoff=60), av.actorInterval('gun_reload', blendInT=0, blendOutT=0), Func(finishReload), Func(self.unlockInput, av))
        del finishReload
        return track

    def getPistolFireAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        subtype = ItemGlobals.getSubtype(av.currentWeaponId)
        if subtype in [ItemGlobals.MUSKET, ItemGlobals.BAYONET]:
            return self.getBayonetFireAnim(av, skillId, ammoSkillId, charge, target, skillResult)
        elif subtype in [ItemGlobals.BLUNDERBUSS]:
            return self.getPistolScattershotAnim(av, skillId, ammoSkillId, charge, target, skillResult)

        def startVFX():
            unlimited = av.isLocal()
            pistolFlame = PistolShot.getEffect(unlimited)
            if pistolFlame:
                pistolFlame.reparentTo(av.currentWeapon)
                pistolFlame.setPos(1.25, 0.3, 0)
                pistolFlame.setHpr(0, 0, 90)
                pistolFlame.setScale(1)
                pistolFlame.play()

        anim = ItemGlobals.getFireAnim(ItemGlobals.getSubtype(av.currentWeaponId))
        if anim:
            ival = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.lockInput, av), Func(av.attackTire), Func(av.setAimMod, 0), av.actorInterval(anim, startFrame=1, endFrame=3, blendInT=0.0, blendOutT=0.0, playRate=1.0), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval(anim, startFrame=4, endFrame=12, blendInT=0.0, blendOutT=0.0, playRate=1.0), Func(self.unlockInput, av), av.actorInterval(anim, startFrame=13, blendInT=0, blendOutT=0.3, playRate=1.0))
        else:
            ival = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.lockInput, av), Func(av.attackTire), Func(av.setAimMod, 0), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('gun_fire', endFrame=12, blendInT=0, blendOutT=0), Func(self.unlockInput, av), av.actorInterval('gun_fire', startFrame=13, blendInT=0, blendOutT=0.3))
        del startVFX
        return ival

    def getPistolTakeAimAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if base.cr.wantSpecialEffects and base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                pistolSmokeEffect = PistolSmoke.getEffect(unlimited)
                if pistolSmokeEffect:
                    pistolSmokeEffect.reparentTo(av)
                    pistolSmokeEffect.setPos(av, 1.2, 2.5, 5)
                    pistolSmokeEffect.play()
                pistolFlameEffect = PistolFlame.getEffect(unlimited)
                if pistolFlameEffect:
                    pistolFlameEffect.reparentTo(av)
                    pistolFlameEffect.particleDummy.reparentTo(av)
                    pistolFlameEffect.flash.setScale(30)
                    pistolFlameEffect.setPos(av, 1.2, 2.5, 5)
                    pistolFlameEffect.setColorScale(1, 1, 1, 1)
                    pistolFlameEffect.play()

        subtype = ItemGlobals.getSubtype(av.currentWeaponId)
        anim = ItemGlobals.getTakeAimAnim(subtype)
        if anim:
            if subtype in (ItemGlobals.BAYONET, ItemGlobals.MUSKET, ItemGlobals.BLUNDERBUSS):
                ival = Sequence(Func(av.motionFSM.off), Func(base.cr.targetMgr.setWantAimAssist, 0), Func(av.setAimMod, 0), Func(self.lockInput, av), Func(av.attackTire), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval(anim, playRate=1, startFrame=26, blendInT=0, blendOutT=0.3), Func(av.considerEnableMovement), Func(self.unlockInput, av))
            else:
                ival = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(av.setAimMod, 0), Func(self.lockInput, av), Func(av.attackTire), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval(anim, playRate=1, startFrame=1, blendInT=0, blendOutT=0.3), Func(self.unlockInput, av))
        else:
            ival = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(av.setAimMod, 0), Func(self.lockInput, av), Func(av.attackTire), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('gun_fire', playRate=1, blendInT=0, blendOutT=0.3), Func(self.unlockInput, av))
        del startVFX
        return ival

    def getPistolScattershotAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            pistolFlame = ScatterShot.getEffect(unlimited)
            if pistolFlame:
                pistolFlame.reparentTo(av.currentWeapon)
                pistolFlame.setPos(1.75, 0.25, 0)
                pistolFlame.setHpr(0, 0, 90)
                pistolFlame.setScale(0.4)
                pistolFlame.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = GrapeshotEffect.getEffect(unlimited)
                if effect:
                    effect.reparentTo(render)
                    effect.setHpr(av, 0, 0, 0)
                    effect.setPos(av, 1.2, 2.0, 4)
                    effect.setScale(0.2)
                    effect.time = 0.5
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = SimpleSmokeCloud.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av.currentWeapon)
                    effect.setPos(1.75, 0.25, 0)
                    effect.setEffectScale(0.1)
                    effect.play()

        anim = ItemGlobals.getFireAnim(ItemGlobals.getSubtype(av.currentWeaponId))
        ival = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.lockInput, av), Func(av.attackTire), Func(av.setAimMod, 0), av.actorInterval(anim, startFrame=9, endFrame=11, blendInT=0.1, blendOutT=0), Func(av.currentWeapon.playSkillSfx, skillId, av), Func(startVFX), av.actorInterval(anim, startFrame=12, endFrame=39, blendInT=0.0, blendOutT=0.3), Func(self.unlockInput, av))
        del startVFX
        return ival

    def getGrenadeReloadAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def finishReload():
            if av.isLocal():
                messenger.send('reloadFinished')

        if av.currentWeapon.ammoSkillId == InventoryType.GrenadeSiege:
            track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.detachFrom, av), av.actorInterval('bigbomb_draw', endFrame=11, blendInT=0, blendOutT=0), Func(av.currentWeapon.attachTo, av), av.actorInterval('bigbomb_draw', startFrame=12, blendInT=0, blendOutT=0.3), Func(finishReload), Func(self.unlockInput, av))
        else:
            track = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.currentWeapon.detachFrom, av), av.actorInterval('bomb_draw', endFrame=5, blendInT=0, blendOutT=0), Func(av.currentWeapon.attachTo, av), av.actorInterval('bomb_draw', startFrame=5, blendInT=0, blendOutT=0.3), Func(finishReload), Func(self.unlockInput, av))
        del finishReload
        return track

    def getGrenadeChargingAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        if av.currentWeapon.ammoSkillId == InventoryType.GrenadeSiege:
            track = Parallel(Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), av.actorInterval('bigbomb_charge', blendInT=0.3, blendOutT=0), av.actorInterval('bigbomb_charge_loop', loop=1, duration=9999, blendInT=0, blendOutT=0.3)), SoundInterval(av.currentWeapon.chargingSfx, loop=1, node=av, cutOff=60))
        else:
            track = Parallel(Sequence(Func(av.setAimMod, -0.5), Func(av.currentWeapon.hideMouse, av), av.actorInterval('bomb_charge', blendInT=0.3, blendOutT=0), av.actorInterval('bomb_charge_loop', loop=1, duration=9999, blendInT=0, blendOutT=0.3)), SoundInterval(av.currentWeapon.chargingSfx, loop=1, node=av, cutOff=60))
        return track

    def getGrenadeThrow(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        if ammoSkillId == InventoryType.GrenadeSiege:
            attachTime = av.getFrameTime('bigbomb_throw', 40)
            track = Parallel(Func(self.lockInput, av), Func(av.attackTire), Func(av.setAimMod, 0), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.playSkillSfx, av.currentWeapon.ammoSkillId, av), Sequence(av.actorInterval('bigbomb_throw', blendInT=0.3, blendOutT=0.3), Func(av.considerEnableMovement), Func(self.unlockInput, av)), Sequence(Wait(attachTime), Func(av.currentWeapon.detachFrom, av), Func(self.spawnGrenade, av, skillId, ammoSkillId, charge, target, skillResult)))
        else:
            attachTime = av.getFrameTime('bomb_throw', 15)
            track = Parallel(Func(self.lockInput, av), Func(av.attackTire), Func(av.setAimMod, 0), Func(av.currentWeapon.playSkillSfx, skillId, av), Sequence(av.actorInterval('bomb_throw', blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av)), Sequence(Wait(attachTime), Func(av.currentWeapon.detachFrom, av), Func(self.spawnGrenade, av, skillId, ammoSkillId, charge, target, skillResult)))
        return track

    def getGrenadeLongVolley(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        if ammoSkillId == InventoryType.GrenadeSiege:
            attachTime = av.getFrameTime('bigbomb_charge_throw', 9)
            track = Parallel(Func(self.lockInput, av), Func(av.attackTire), Func(av.setAimMod, 0), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.playSkillSfx, av.currentWeapon.ammoSkillId, av), Sequence(av.actorInterval('bigbomb_charge_throw', blendInT=0.3, blendOutT=0.3), Func(av.considerEnableMovement), Func(self.unlockInput, av)), Sequence(Wait(attachTime), Func(av.currentWeapon.detachFrom, av), Func(self.spawnGrenade, av, skillId, ammoSkillId, charge, target, skillResult)))
        else:
            attachTime = av.getFrameTime('bomb_charge_throw', 4)
            track = Parallel(Func(self.lockInput, av), Func(av.attackTire), Func(av.setAimMod, 0), Func(av.currentWeapon.playSkillSfx, skillId, av, startTime=2.0), Sequence(av.actorInterval('bomb_charge_throw', blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av)), Sequence(Wait(attachTime), Func(av.currentWeapon.detachFrom, av), Func(self.spawnGrenade, av, skillId, ammoSkillId, charge, target, skillResult)))
        return track

    def spawnGrenade(self, av, skillId, ammoSkillId, charge, target, skillResult):
        grenade = GrenadeProjectile(av.cr, ammoSkillId, av.projectileHitEvent)
        grenade.detachNode()
        grenade.setBillboardPointEye()
        grenadeModelCol = grenade.find('**/collide')
        if grenadeModelCol and not grenadeModelCol.isEmpty():
            grenadeModelCol.removeNode()
        if av.isLocal():
            collNode = grenade.getCollNode()
            collNode.reparentTo(render)
        else:
            collNode = None
        av.ammoSequence = av.ammoSequence + 1 & 255
        grenade.setTag('ammoSequence', str(av.ammoSequence))
        grenade.setTag('skillId', str(int(skillId)))
        grenade.setTag('ammoSkillId', str(int(ammoSkillId)))
        grenade.setTag('attackerId', str(av.getDoId()))
        self.putGrenadeInHand(av, grenade)
        self.addCollider(av, grenade, collNode)
        self.throwGrenade(av, skillId, ammoSkillId, grenade, collNode, charge, target)
        return

    def addCollider(self, av, grenade, collNode):
        if av.isLocal():
            base.cTrav.addCollider(collNode, grenade.collHandler)

    def removeCollider(self, av, collNode):
        if av.isLocal():
            base.cTrav.removeCollider(collNode)

    def throwGrenade(self, av, skillId, ammoSkillId, grenade, collNode, powerMod=0, target=None):
        if not av:
            return
        startPos = av.rightHandNode.getPos(render)
        endPos = None
        duration = None
        wayPoint = None
        timeToWayPoint = None
        if target == None:
            power = WeaponGlobals.getAttackProjectilePower(skillId, ammoSkillId)
            power *= powerMod + self.BASE_GRENADE_POWER
            if av.isLocal():
                pitch = camera.getP(render)
            else:
                pitch = 0.0
            m = av.getMat(render)
            startVel = m.xformVec(Vec3(0, power, 30 + pitch))
            if av.isLocal():
                forwardVel = av.controlManager.currentControls.getSpeeds()[0]
                sideVel = av.controlManager.currentControls.getSpeeds()[2]
                avVel = m.xformVec(Vec3(sideVel / 3.0, forwardVel, 0))
                startVel += avVel
            endPlaneZ = startPos[2] - 100
        else:
            startVel = None
            endPos = target.getPos(render)
            wayPoint = endPos
            endPos = None
            tgtDist = av.getDistance(target)
            duration = WeaponGlobals.getAIProjectileAirTime(tgtDist)
            timeToWayPoint = duration
            duration = None
            endPlaneZ = wayPoint.getZ() - 100
        try:
            projInterval = ProjectileInterval(grenade, startPos=startPos, endPos=endPos, duration=duration, startVel=startVel, endZ=endPlaneZ, collNode=collNode, wayPoint=wayPoint, timeToWayPoint=timeToWayPoint)
        except StandardError, e:
            raise StandardError('(localAv %s) Invalid projectile parameters(%s,%s,%s,%s,%s,%s,%s)' % (av.isLocal(), startPos, endPos, duration, startVel, endPlaneZ, wayPoint, timeToWayPoint))

        ival = Sequence(projInterval, Func(self.removeCollider, av, collNode), Func(grenade.destroy), name='Grenade-%s-%s' % (av.doId, grenade.get_key()))
        grenade.setIval(ival, start=True)
        return

    def putGrenadeInHand(self, av, grenade):
        grenade.reparentTo(render)
        grenade.setPos(render, av.rightHandNode.getPos(render))

    def playCastingAnim(self, av):
        if not av.currentWeapon:
            return None
        if av.attuneEffect:
            av.attuneEffect.castEffect.start()
            effect = FadingCard(av.currentWeapon.effectCard, av.currentWeapon.effectColor)
            effect.reparentTo(av.currentWeapon)
            effect.play()
        return None

    def getPoke(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(av.attackTire), Func(self.playCastingAnim, av), av.actorInterval('voodoo_doll_poke', endFrame=50, playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getEvilEye(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            attuneEffect = VoodooAura.getEffect(unlimited)
            if attuneEffect:
                attuneEffect.reparentTo(render)
                attuneEffect.setPos(av.headNode, 0, 0, 0)
                attuneEffect.setEffectColor(Vec4(0.2, 0.1, 0.5, 1))
                attuneEffect.particleDummy.reparentTo(render)
                attuneEffect.play()
                if target:
                    if hasattr(target, 'creature'):
                        if target.creature:
                            targetPos = target.creature.headNode.isEmpty() or target.creature.headNode.getPos(render)
                        else:
                            targetPos = target.getPos(render)
                    elif hasattr(target, 'headNode'):
                        targetPos = target.headNode.getPos(render)
                    else:
                        targetPos = target.getPos(render)
                else:
                    dummy = av.attachNewNode('dummy')
                    dummy.setPos(0, 30, 4)
                    targetPos = dummy.getPos(render)
                    dummy.removeNode()
                moveIval = LerpPosInterval(attuneEffect, 0.4, targetPos)
                moveIval.start()

        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(startVFX), av.actorInterval('emote_anger', playRate=2.0, blendInT=0.2, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getReflect(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                auraPulse = HitPulse.getEffect(unlimited)
                if auraPulse:
                    auraPulse.reparentTo(av)
                    auraPulse.setEffectColor(Vec4(1, 0.9, 0.6, 0.75))
                    auraPulse.effectModel.setPos(0, 3, 4.0)
                    auraPulse.setScale(1.0)
                    if target:
                        auraPulse.lookAt(target)
                    else:
                        auraPulse.lookAt(base.camera)
                    auraPulse.play()
            flashEffect = FlashEffect()
            flashEffect.reparentTo(av.rightHandNode)
            flashEffect.setScale(10.0)
            flashEffect.fadeTime = 1.0
            flashEffect.setEffectColor(Vec4(1, 0.9, 0.6, 1))
            flashEffect.play()
            auraEffect = VoodooAura2.getEffect(unlimited)
            if auraEffect:
                auraEffect.reparentTo(render)
                auraEffect.setPos(av, 0, 2, 4)
                auraEffect.setEffectColor(Vec4(1, 0.9, 0.6, 0.15))
                auraEffect.particleDummy.reparentTo(render)
                auraEffect.play()
                if target:
                    if hasattr(target, 'creature'):
                        if target.creature:
                            targetPos = target.creature.headNode.isEmpty() or target.creature.headNode.getPos(render)
                        else:
                            targetPos = target.getPos(render)
                    else:
                        targetPos = target.headNode.getPos(render)
                    moveIval = LerpPosInterval(auraEffect, 0.4, targetPos)
                    moveIval.start()

        ival = Sequence(Func(self.lockInput, av), av.actorInterval('voodoo_tune', playRate=1.5, startFrame=0, endFrame=20, blendInT=0.1, blendOutT=0.0), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('voodoo_tune', playRate=1.5, startFrame=20, endFrame=35, blendInT=0.0, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getAttune(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), av.actorInterval('voodoo_tune', playRate=2.0, endFrame=35, blendInT=0.2, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getUnattune(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.playUnattuneSfx, av.currentWeapon), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getHeal(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getShackles(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getSwarm(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getBurn(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getCure(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getHexWard(self, av, skillId, ammoSkillId, charge, target, skillResult):

        def startVFX():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                auraPulse = HitPulse.getEffect(unlimited)
                if auraPulse:
                    auraPulse.reparentTo(av)
                    auraPulse.setEffectColor(Vec4(0.4, 0.3, 1, 0.75))
                    auraPulse.effectModel.setPos(0, 3, 4.0)
                    auraPulse.setScale(1.0)
                    if target:
                        auraPulse.lookAt(target)
                    else:
                        auraPulse.lookAt(base.camera)
                    auraPulse.play()
            flashEffect = FlashEffect()
            flashEffect.reparentTo(av.rightHandNode)
            flashEffect.setScale(10.0)
            flashEffect.fadeTime = 1.0
            flashEffect.setEffectColor(Vec4(0.2, 0.6, 1, 1))
            flashEffect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(self.playCastingAnim, av), Func(startVFX), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getCaptainsResolve(self, av, skillId, ammoSkillId, charge, target, skillResult):

        def startVFX():
            unlimited = av.isLocal()
            pulseFlash = PulsingGlow.getEffect(unlimited)
            if pulseFlash:
                pulseFlash.reparentTo(av.currentWeapon)
                pulseFlash.setEffectColor(Vec4(0.3, 1, 1, 0.8))
                pulseFlash.setScale(1.0)
                pulseFlash.play()
            coneRays = ConeRays.getEffect(unlimited)
            if coneRays:
                coneRays.reparentTo(av)
                coneRays.setPos(0, 0, 1.0)
                coneRays.setEffectColor(Vec4(0.3, 1, 1, 0.2))
                coneRays.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                healBlast = HealBlast.getEffect(unlimited)
                if healBlast:
                    healBlast.reparentTo(av)
                    healBlast.setPos(0, 0, 6.0)
                    healBlast.play()

        def startVFX2():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                healDisc = VoodooGroundAura.getEffect(unlimited)
                if healDisc:
                    healDisc.setEffectColor(Vec4(0.3, 1, 1, 0.35))
                    healDisc.reparentTo(av)
                    healDisc.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                healAura = VoodooAuraHeal.getEffect(unlimited)
                if healAura:
                    healAura.setEffectColor(Vec4(0.3, 1, 1, 0.5))
                    healAura.reparentTo(av)
                    healAura.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(self.playCastingAnim, av), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('voodoo_swarm', playRate=1.0, startFrame=0, endFrame=12, blendInT=0.3, blendOutT=0.0), Func(startVFX2), av.actorInterval('voodoo_swarm', playRate=1.0, startFrame=12, endFrame=64, blendInT=0, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getCurse(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(self.unlockInput, av))
        return ival

    def getLifeDrain(self, av, skillId, ammoSkillId, charge, target, skillResult):

        def startVFX():
            unlimited = av.isLocal()
            effect = SpectralSmoke.getEffect(unlimited)
            if effect:
                effect.reparentTo(av)
                effect.setPos(av, 0, 0, av.getHeight() / 2.0)
                effect.setScale(1, 1, av.getHeight() / 2.0)
                effect.play(duration=2.0, delay=1.5)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = HealSparks.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av)
                    effect.setPos(av, 0, 0, av.getHeight() / 1.5)
                    effect.setScale(1, 1, av.getHeight() / 2.0)
                    effect.setEffectColor(Vec4(0.2, 0.2, 1.0, 1))
                    effect.play(delay=1.5)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = HomingMissile.getEffect(unlimited)
                if effect and target:
                    effect.reparentTo(render)
                    effect.setPos(target, 0, 0, target.getHeight() - 1.5)
                    effect.target = av
                    effect.initialVelocity = Vec3(0, 0, 1.5)
                    effect.targetOffset = Vec3(0, 0, 3.0)
                    effect.duration = 1.75
                    effect.wantTrail = 0
                    effect.particleEffect = SpectralTrail.getEffect()
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = HomingMissile.getEffect(unlimited)
                if effect and target:
                    effect.reparentTo(render)
                    effect.setPos(target, 0, 0, target.getHeight() - 1.5)
                    effect.target = av
                    randomness = random.random() * 1.25
                    effect.initialVelocity = Vec3(-1.0 - randomness, 0, 1.5)
                    effect.targetOffset = Vec3(0, 0, 3.0)
                    effect.duration = 1.5 + randomness
                    effect.wantTrail = 0
                    effect.particleEffect = SpectralTrail.getEffect()
                    effect.play()
                effect = HomingMissile.getEffect(unlimited)
                if effect and target:
                    effect.reparentTo(render)
                    effect.setPos(target, 0, 0, target.getHeight() - 1.5)
                    effect.target = av
                    randomness = random.random() * 1.25
                    effect.initialVelocity = Vec3(1.0 + randomness, 0, 1.5)
                    effect.targetOffset = Vec3(0, 0, 3.0)
                    effect.duration = 1.5 + randomness
                    effect.wantTrail = 0
                    effect.particleEffect = SpectralTrail.getEffect()
                    effect.play()

        ival = Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(self.playCastingAnim, av), Parallel(av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Sequence(Wait(0.5), Func(startVFX))), Func(self.unlockInput, av))
        del startVFX
        return ival

    def startChargeSound(self, av, skillId):
        if not av.currentWeapon:
            return None
        skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
        getChargeSfxFunc = skillInfo[WeaponGlobals.HIT_SFX_INDEX]
        getChargeLoopSfxFunc = skillInfo[WeaponGlobals.MISS_SFX_INDEX]
        av.currentWeapon.chargeSound = getChargeSfxFunc()
        av.currentWeapon.chargeLoopSound = getChargeLoopSfxFunc()
        av.currentWeapon.chargeSoundSequence = Sequence(SoundInterval(av.currentWeapon.chargeSound, loop=0, node=av.currentWeapon, cutOff=60), SoundInterval(av.currentWeapon.chargeLoopSound, loop=1, duration=1000, node=av.currentWeapon, cutOff=60))
        av.currentWeapon.chargeSoundSequence.start()
        if hasattr(av.currentWeapon, 'startChargeEffect'):
            av.currentWeapon.startChargeEffect()
        return None

    def stopChargeSound(self, av):
        if not av.currentWeapon:
            return
        if av.currentWeapon.chargeSoundSequence:
            av.currentWeapon.chargeSoundSequence.finish()
            av.currentWeapon.chargeSoundSequence = None
        if av.currentWeapon.chargeSound:
            av.currentWeapon.chargeSound.stop()
            av.currentWeapon.chargeSound = None
        if av.currentWeapon.chargeLoopSound:
            av.currentWeapon.chargeLoopSound.stop()
            av.currentWeapon.chargeLoopSound = None
        if hasattr(av.currentWeapon, 'stopChargeEffect'):
            av.currentWeapon.stopChargeEffect()
        return

    def playCastSound(self, av, skillId):
        skillInfo = WeaponGlobals.getSkillAnimInfo(skillId)
        getCastSfxFunc = skillInfo[WeaponGlobals.HIT_SFX_INDEX]
        soundFX = getCastSfxFunc()
        if soundFX:
            base.playSfx(soundFX, node=av, cutoff=60)

    def getChargeWitherAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effect = WitherCharge.getEffect(unlimited)
                if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect.setPos(av.currentWeapon, -0.1, 1.5, 0)
                    av.currentWeapon.effect.setPos(av.currentWeapon, av.currentWeapon.getOffset(av.currentWeapon.itemId))
                    av.currentWeapon.effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    av.currentWeapon.effect.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastWitherAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if av.currentWeapon.effect:
                av.currentWeapon.effect.stopLoop()
                av.currentWeapon.effect = None
            effect = SoulHarvest.getEffect(unlimited)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 5, 0)
                effect.radius = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = DomeExplosion.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setPos(av, 0, 5, 0)
                    effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId) * 2.0
                    effect.play()
                effect = DarkPortal.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setPos(av, 0, 5, 0)
                    effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId) * 4.0
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = EvilRingEffect.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setPos(av, 0, 5, 0)
                    effect.effectScale = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                    effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    effect.duration = 2.5
                    effect.play()
            return

        seq = Sequence(Func(av.considerEnableMovement), Func(self.lockInput, av), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getChargeSoulflayAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effect = SoulSpiral.getEffect(unlimited)
                if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect.setPos(av.currentWeapon, -0.1, 1.5, 0)
                    av.currentWeapon.effect.setHpr(av.currentWeapon, 0.0, -90.0, 0.0)
                    av.currentWeapon.effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    av.currentWeapon.effect.setScale(0.9, 0.9, 0.9)
                    av.currentWeapon.effect.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastSoulFlayAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if av.currentWeapon.effect:
                av.currentWeapon.effect.stopLoop()
                av.currentWeapon.effect = None
            effect = SoulFlay.getEffect(unlimited)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0.0, 4.0, 3.0)
                effect.setHpr(av, 0.0, -90.0, 0.0)
                effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                dummy = NodePath('effect')
                dummy.reparentTo(av.getParent())
                dummy.setPos(av, 0.0, 4.0, 4.0)
                dummy.setHpr(av, 0.0, 0.0, 0.0)
                effect = VoodooSouls.getEffect(unlimited)
                if effect:
                    effect.reparentTo(dummy)
                    effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    effect.play()
                    posIval = LerpPosInterval(effect, 1.0, Vec3(0.0, 50.0, 0.0), startPos=Vec3(0.0, 0.0, 0.0))
                    posIval.start()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                effect = VoodooGlow.getEffect(unlimited)
                if effect and not av.currentWeapon.isEmpty():
                    effect.reparentTo(av.currentWeapon)
                    effect.setPos(av.currentWeapon, av.currentWeapon.getOffset(av.currentWeapon.itemId))
                    effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    effect.play()
            return

        seq = Sequence(Func(av.considerEnableMovement), Func(self.lockInput, av), Func(av.attackTire), Func(startVFX), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getChargePestilenceAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effectActor = Actor.Actor('models/effects/mopath_none', {'spin': 'models/effects/mopath_spiral'})
                joint = av.currentWeapon.effectActor.find('**/joint1')
                av.currentWeapon.effectActor.setScale(1.0, 0.75, 1.0)
                av.currentWeapon.effectActor.setHpr(av.currentWeapon.getHpr())
                av.currentWeapon.effectActor.reparentTo(av.currentWeapon)
                av.currentWeapon.effectActor.setPos(av.currentWeapon, 0.0, 1.8, 0.0)
                av.currentWeapon.effectActor.setPlayRate(1.2, 'spin')
                av.currentWeapon.effectActor.loop('spin')
                av.currentWeapon.effect = VoodooPestilence.getEffect(unlimited)
                if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect.particleDummy.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect.reparentTo(joint)
                    av.currentWeapon.effect.effectScale = 1.0
                    av.currentWeapon.effect.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastPestilenceAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if av.currentWeapon.effect:
                av.currentWeapon.effect.stopLoop()
                av.currentWeapon.effect = None
            effect = Pestilence.getEffect(unlimited)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 4.0, 3.0)
                effect.setHpr(av, 0, -90, 0)
                effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                if not av.currentWeapon.effectActor:
                    av.currentWeapon.effectActor = Actor.Actor('models/effects/mopath_none', {'spin': 'models/effects/mopath_spiral'})
                joint = av.currentWeapon.effectActor.find('**/joint1')
                av.currentWeapon.effectActor.reparentTo(av.getParent())
                av.currentWeapon.effectActor.setPos(av, 0.0, 13.0, 4.0)
                av.currentWeapon.effectActor.setHpr(av.getHpr())
                av.currentWeapon.effectActor.setPlayRate(1.8, 'spin')
                av.currentWeapon.effectActor.play('spin')
                scaleIval = LerpScaleInterval(av.currentWeapon.effectActor, 0.25, Vec3(10.0, 25.0, 10.0), startScale=Vec3(2.0, 15.0, 2.0))
                scaleIval.start()
                effect = VoodooPestilence.getEffect(unlimited)
                if effect:
                    effect.particleDummy.reparentTo(av.getParent())
                    effect.reparentTo(joint)
                    effect.effectScale = 4.0
                    effect.play()
            return

        seq = Sequence(Func(av.considerEnableMovement), Func(self.lockInput, av), Func(av.attackTire), Func(startVFX), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getChargeHellfireAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            offset = av.currentWeapon.getOffset(av.currentWeapon.itemId) + Vec3(0, 0.2, 0)
            av.currentWeapon.effect = FlamingSkull.getEffect(unlimited)
            if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                av.currentWeapon.effect.reparentTo(av.currentWeapon)
                av.currentWeapon.effect.setPos(av.currentWeapon, offset + Vec3(0.2, 1, 0.3))
                av.currentWeapon.effect.setHpr(av.currentWeapon, 0, -90, 40)
                av.currentWeapon.effect.startLoop()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effect2 = VoodooStaffFire.getEffect(unlimited)
                if av.currentWeapon.effect2 and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect2.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect2.setPos(av.currentWeapon, offset)
                    av.currentWeapon.effect2.setHpr(av.currentWeapon, 0, -90, 0)
                    av.currentWeapon.effect2.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    av.currentWeapon.effect2.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastHellfireAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            if isinstance(av.currentWeapon.effect, FlamingSkull):
                av.currentWeapon.effect.wrtReparentTo(render)
                targetPos, speed, impactT = av.getProjectileInfo(skillId, None)
                av.currentWeapon.effect.playLaunch(speed, targetPos)
            if av.currentWeapon.effect2:
                av.currentWeapon.effect2.stopLoop()
                av.currentWeapon.effect2 = None
            return

        seq = Sequence(Func(av.considerEnableMovement), Func(self.lockInput, av), Func(av.attackTire), Func(startVFX), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getChargeBanishAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            offset = av.currentWeapon.getOffset(av.currentWeapon.itemId)
            av.currentWeapon.effect = VoodooPower.getEffect(unlimited)
            if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                av.currentWeapon.effect.reparentTo(av.currentWeapon)
                av.currentWeapon.effect.setPos(av.currentWeapon, offset + Vec3(0, 1.45, -0.1))
                av.currentWeapon.effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                av.currentWeapon.effect.startLoop()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effect2 = EnergySpiral.getEffect(unlimited)
                if av.currentWeapon.effect2 and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect2.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect2.setPos(av.currentWeapon, offset + Vec3(0, 0, -0.1))
                    av.currentWeapon.effect2.setHpr(av.currentWeapon, 0.0, -90.0, 0.0)
                    av.currentWeapon.effect2.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    av.currentWeapon.effect2.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastBanishAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if av.currentWeapon.effect:
                av.currentWeapon.effect.stopLoop()
                av.currentWeapon.effect = None
            if av.currentWeapon.effect2:
                av.currentWeapon.effect2.stopLoop()
                av.currentWeapon.effect2 = None
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = VoodooGlow.getEffect(unlimited)
                if effect and not av.currentWeapon.isEmpty():
                    effect.reparentTo(av.currentWeapon)
                    effect.setPos(av.currentWeapon, av.currentWeapon.getOffset(av.currentWeapon.itemId))
                    effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    effect.play()
            return

        seq = Sequence(Func(av.considerEnableMovement), Func(self.lockInput, av), Func(av.attackTire), Func(startVFX), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getChargeDesolationAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                av.currentWeapon.effectActor = Actor.Actor('models/effects/mopath_none', {'spin': 'models/effects/mopath_spiral'})
                joint = av.currentWeapon.effectActor.find('**/joint1')
                av.currentWeapon.effectActor.setScale(1.0, 0.75, 1.0)
                av.currentWeapon.effectActor.setP(0.0)
                av.currentWeapon.effectActor.reparentTo(av.currentWeapon)
                av.currentWeapon.effectActor.setPos(av.currentWeapon, 0.0, 1.7, 0.0)
                av.currentWeapon.effectActor.setPlayRate(1.5, 'spin')
                av.currentWeapon.effectActor.loop('spin')
                av.currentWeapon.effect = DesolationChargeSmoke.getEffect(unlimited)
                if av.currentWeapon.effect and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect.particleDummy.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect.reparentTo(joint)
                    av.currentWeapon.effect.effectScale = 1.0
                    av.currentWeapon.effect.startLoop()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                av.currentWeapon.effect2 = WindCharge.getEffect(unlimited)
                if av.currentWeapon.effect2 and not av.currentWeapon.isEmpty():
                    av.currentWeapon.effect2.reparentTo(av.currentWeapon)
                    av.currentWeapon.effect2.setPos(av.currentWeapon, 0.0, 1.25, 0.0)
                    av.currentWeapon.effect2.setHpr(0, -90, 0)
                    av.currentWeapon.effect2.startLoop()

        seq = Sequence(Func(av.motionFSM.moveLock), Func(av.currentWeapon.hideMouse, av), Func(base.cr.targetMgr.setWantAimAssist, 1), Func(self.startChargeSound, av, skillId), Func(startVFX), av.actorInterval('wand_cast_start', blendOutT=0), Func(av.loop, 'wand_cast_idle', blendT=0))
        del startVFX
        return seq

    def getCastDesolationAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            if av.currentWeapon.effect:
                av.currentWeapon.effect.stopLoop()
                av.currentWeapon.effect = None
            if av.currentWeapon.effect2:
                av.currentWeapon.effect2.stopLoop()
                av.currentWeapon.effect2 = None
            effect = WindWave.getEffect(unlimited)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setEffectColor(Vec4(1, 1, 1, 0.75))
                effect.setPos(av, 0.0, 0.0, 0.0)
                effect.setScale(1.0, 1.0, 1.0)
                effect.setHpr(0.0, 0.0, 0.0)
                effect.play()
            effect = SoulHarvest2.getEffect(unlimited)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 0, 2)
                effect.radius = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = DesolationSmoke.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setEffectColor(Vec4(1, 1, 1, 1))
                    effect.setPos(av, 0.0, 0.0, 0.0)
                    effect.play()
                effect = DomeExplosion.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setPos(av, 0, 0, 0)
                    effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                    effect.play()
                effect = DarkPortal.getEffect(unlimited)
                if effect:
                    effect.reparentTo(av.getParent())
                    effect.setPos(av, 0, 0, 0)
                    effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId) * 3.0
                    effect.play()
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                cameraShakerEffect = CameraShaker()
                cameraShakerEffect.wrtReparentTo(av.getParent())
                cameraShakerEffect.setPos(av, 0.0, 0.0, 0.0)
                cameraShakerEffect.shakeSpeed = 0.075
                cameraShakerEffect.shakePower = 1.0
                cameraShakerEffect.numShakes = 30
                cameraShakerEffect.scalePower = 1
                cameraShakerEffect.play(100.0)
            return

        seq = Sequence(Func(av.considerEnableMovement), Func(self.lockInput, av), Func(av.attackTire), Func(startVFX), Func(self.stopChargeSound, av), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getFizzleAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return
        if av.currentWeapon.effect:
            av.currentWeapon.effect.stopLoop()
            av.currentWeapon.effect = None
        if av.currentWeapon.effect2:
            av.currentWeapon.effect2.stopLoop()
            av.currentWeapon.effect2 = None
        return Sequence(Func(av.considerEnableMovement), Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.lockInput, av), Func(self.stopChargeSound, av), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))

    def getCastFireAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            unlimited = av.isLocal()
            self.cleanWeaponEffects(av)
            motion_color = [
             Vec4(1.0, 1.0, 1.0, 1.0), Vec4(0.5, 0.2, 1.0, 1.0)]
            targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
            effect = VoodooProjectile.getEffect(unlimited)
            if effect:
                effect.reparentTo(render)
                effect.setPos(av, 0, 2, 2)
                effect.setH(av.getH(render))
                effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                effect.play(targetPos, speed, target)
            if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                effect = VoodooGlow.getEffect()
                if effect and not av.currentWeapon.isEmpty():
                    effect.reparentTo(av.currentWeapon)
                    effect.setPos(av.currentWeapon, 0.0, 2.0, 0.0)
                    effect.setEffectColor(av.currentWeapon.getEffectColor(av.currentWeapon.itemId))
                    effect.play()

        seq = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.lockInput, av), Func(av.attackTire), Func(startVFX), Func(self.playCastSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getToggleAuraOnAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            if not hasattr(av.currentWeapon, 'getStartWardingAura'):
                return
            if skillId == EnemySkills.STAFF_TOGGLE_AURA_WARDING:
                av.currentWeapon.getStartWardingAura(av).start()
            elif skillId == EnemySkills.STAFF_TOGGLE_AURA_NATURE:
                av.currentWeapon.getStartNatureAura(av).start()
            elif skillId == EnemySkills.STAFF_TOGGLE_AURA_DARK:
                av.currentWeapon.getStartDarkAura(av).start()

        seq = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.lockInput, av), Func(startVFX), Func(self.startChargeSound, av, skillId), av.actorInterval('wand_cast_fire'), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getToggleAuraOffAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        seq = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.stopChargeSound, av), Func(self.lockInput, av), Func(self.unlockInput, av))
        return seq

    def cleanWeaponEffects(self, av):
        if av.currentWeapon:
            if av.currentWeapon.effect:
                av.currentWeapon.effect.stopLoop()
                av.currentWeapon.effect = None
            if av.currentWeapon.effect2:
                av.currentWeapon.effect2.stopLoop()
                av.currentWeapon.effect2 = None
        return

    def getDrink(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.consumable:
            return None

        def hideCurrentWeapon():
            if av.currentWeapon:
                if not av.currentWeapon.isEmpty():
                    av.currentWeapon.hide()

        def showCurrentWeapon():
            if av.currentWeapon:
                if not av.currentWeapon.isEmpty():
                    av.currentWeapon.show()

        return Sequence(Func(self.lockInput, av), Func(av.attackTire), Func(self.lockDrink, av), Func(hideCurrentWeapon), Func(av.consumable.updateItemId, ammoSkillId), Func(av.consumable.attachTo, av), av.actorInterval('drink_potion', playRate=1.5, startFrame=8, endFrame=45, blendInT=0.2, blendOutT=0.2), Func(showCurrentWeapon), Func(av.consumable.detachFrom, av), Func(self.unlockInput, av), Wait(0.6), Func(self.unlockDrink, av))

    def getChop(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('sword_cleave', playRate=1.0, startFrame=9, endFrame=45, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getDoubleSlash(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('sword_slash', playRate=1.5, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getLunge(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('sword_lunge', playRate=1.5, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getStab(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval('sword_thrust', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getRollThrust(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        placeHolder = av.attachNewNode('rollThrustPlaceHolder')
        if target:
            placeHolder.lookAt(target)
            newH = av.getH() + placeHolder.getH()
            self.rollDistance = av.getDistance(target)
        else:
            newH = av.getH()
            self.rollDistance = WeaponGlobals.getAttackRange(skillId, ammoSkillId)
        self.rollDistance = max(0.0, self.rollDistance - 0.5)
        self.currAmount = 0

        def setRollPosition(v):
            distance = self.rollDistance * v - self.currAmount
            self.currAmount += distance
            rotMat = Mat3.rotateMatNormaxis(av.getH(), Vec3.up())
            contact = av.physControls.lifter.getContactNormal()
            forward = contact.cross(Vec3.right())
            forward.normalize()
            vel = Vec3(forward * distance)
            vel = Vec3(rotMat.xform(vel))
            av.setFluidPos(Point3(av.getPos() + vel))

        if av.isLocal():
            ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), Func(av.controlManager.currentControls.setCollisionsActive, 1), Parallel(av.actorInterval('sword_roll_thrust', playRate=1.5, startFrame=1, blendInT=0, blendOutT=0), LerpHprInterval(av, 0.05, Vec3(newH, av.getP(), av.getR())), Sequence(Wait(0.3), LerpFunctionInterval(setRollPosition, duration=0.6, fromData=0.0, toData=1.0, name='setRollPosition')), Sequence(Wait(0.6), Func(av.controlManager.currentControls.setCollisionsActive, 0), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))))
        else:
            ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), Parallel(av.actorInterval('sword_roll_thrust', playRate=1.5, startFrame=1, blendInT=0, blendOutT=0), Sequence(Wait(0.6), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))))
        placeHolder.removeNode()
        return ival

    def getComboA(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('sword_comboA', playRate=1.5, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getWildSlash(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.5), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=54, endFrame=87, blendInT=0.5, blendOutT=0.5)), Sequence(Wait(0.958), Func(self.unlockInput, av)))
        return ival

    def getFlurry(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.6), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=88, endFrame=142, blendInT=0.5, blendOutT=0.5)), Sequence(Wait(1.5), Func(self.unlockInput, av)))
        return ival

    def getRiposte(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.endAttack, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_combo', playRate=1.0, startFrame=1, endFrame=28, blendInT=0.2, blendOutT=0.5)), Sequence(Wait(0.75), Func(self.unlockInput, av)))
        return ival

    def getCoup(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_coup', playRate=1.25, blendInT=0, blendOutT=0), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getBackstab(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dagger_backstab', playRate=1.5, blendInT=0, blendOutT=0), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getDualCutlassCombination(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dualcutlass_comboB', playRate=1.2, startFrame=0, endFrame=75, blendInT=0.5, blendOutT=0.25), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getDualCutlassSpin(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dualcutlass_comboB', playRate=1, startFrame=70, endFrame=101, blendInT=0.25, blendOutT=0.25), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getDualCutlassBarrage(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.22), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dualcutlass_comboB', playRate=0.575, startFrame=101, endFrame=131, blendInT=0.25, blendOutT=0.25), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getDualCutlassXSlash(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dualcutlass_comboA', playRate=1, startFrame=50, endFrame=100, blendInT=0.25, blendOutT=0.25), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getDualCutlassGore(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('dualcutlass_comboA', playRate=1, startFrame=100, endFrame=120, blendInT=0.25, blendOutT=0.25), av.actorInterval('dualcutlass_comboB', playRate=1, startFrame=140, endFrame=200, blendInT=0.25, blendOutT=0.25), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getFoilFleche(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_thrust', playRate=1, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getFoilReprise(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_hack', playRate=1, startFrame=45, endFrame=89, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getFoilSwipe(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_coup', playRate=1, startFrame=75, endFrame=97, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getFoilImpale(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_thrust', playRate=1, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getFoilRemise(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_slash', playRate=1, startFrame=10, endFrame=82, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getFoilBalestraKick(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_kick', playRate=1, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getFoilCadence(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(av.currentWeapon.hideMouse, av), Func(av.currentWeapon.setTrailLength, 0.4), Func(av.currentWeapon.beginAttack, av), av.actorInterval('foil_coup', playRate=1, startFrame=75, endFrame=172, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def getKrazyPunch(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return Sequence(Func(self.lockInput, av), av.actorInterval('boxing_kick', playRate=2), av.actorInterval('boxing_punch', playRate=2), av.actorInterval('boxing_kick', playRate=2), Func(self.unlockInput, av))

    def getBoxingPunch(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return Sequence(Func(self.lockInput, av), av.actorInterval('boxing_punch', playRate=1.0, blendInT=0.1, blendOutT=0.2), Func(self.unlockInput, av))

    def getKick(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return Sequence(Func(self.lockInput, av), av.actorInterval('boxing_kick', playRate=1.0), Func(self.unlockInput, av))

    def getBayonetFireAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):

        def startVFX():
            unlimited = av.isLocal()
            pistolFlame = MusketShot.getEffect(unlimited)
            if pistolFlame:
                pistolFlame.reparentTo(av.currentWeapon)
                pistolFlame.setPos(2.8, 0.1, 0)
                pistolFlame.setHpr(0, 0, 90)
                pistolFlame.setScale(1)
                pistolFlame.play()

        anim = ItemGlobals.getFireAnim(ItemGlobals.getSubtype(av.currentWeaponId))
        ival = Sequence(Func(base.cr.targetMgr.setWantAimAssist, 0), Func(self.lockInput, av), Func(startVFX), Func(av.currentWeapon.playSkillSfx, skillId, av), av.actorInterval(anim, startFrame=9, endFrame=14, blendInT=0.0, blendOutT=0), Func(self.unlockInput, av), av.actorInterval(anim, startFrame=15, blendInT=0, blendOutT=0.3))
        return ival

    def getBayonetReloadAnim(self, av, skillId, ammoSkillId, charge, target):
        if not av.currentWeapon:
            return None
        reloadSfx = av.currentWeapon.reloadSfxs
        reloadFx = random.choice(reloadSfx)
        gunCockSfx = av.currentWeapon.gunCockSfxs
        gunCockFx = random.choice(gunCockSfx)
        track = Sequence(Func(self.lockInput, av), av.actorInterval('gun_reload', endFrame=6, blendInT=0, blendOutT=0), Func(base.playSfx, gunCockFx, node=av), av.actorInterval('gun_reload', startFrame=7, endFrame=18, blendInT=0, blendOutT=0), Func(base.playSfx, reloadFx, node=av), av.actorInterval('gun_reload', startFrame=19, blendInT=0, blendOutT=0.3), Func(self.unlockInput, av))
        return track

    def getBayonetStab(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), av.actorInterval('bayonet_attackA', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(self.unlockInput, av))
        return ival

    def getBayonetBash(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), av.actorInterval('bayonet_attackB', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(self.unlockInput, av))
        return ival

    def getBayonetRush(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), av.actorInterval('bayonet_attackC', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(self.unlockInput, av))
        return ival

    def getPlayerBayonetStab(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), av.actorInterval('bayonet_attackA', playRate=1.0, startFrame=6, endFrame=35, blendInT=0, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(self.unlockInput, av)), Sequence(Wait(0.75), Func(self.unlockInput, av)))
        return ival

    def getPlayerBayonetRush(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(self.lockInput, av), Func(av.currentWeapon.setTrailLength, 0.25), Func(av.currentWeapon.beginAttack, av), av.actorInterval('bayonet_attackC', playRate=1.0, blendInT=0.5, blendOutT=0.5), Func(av.currentWeapon.endAttack, av), Func(self.unlockInput, av))
        return ival

    def getCrabAttackLeft(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_left', playRate=1.0)

    def getCrabAttackRight(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_right', playRate=1.0)

    def getCrabAttackBoth(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_both', playRate=1.0)

    def getStumpKick(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.0), av.actorInterval('kick', playRate=1.0))
        return ival

    def getStumpKickRight(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.0), av.actorInterval('kick_right', playRate=1.0))
        return ival

    def getStumpSlapLeft(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.5), av.actorInterval('slap_left', playRate=1.0))
        return ival

    def getStumpSlapRight(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.5), av.actorInterval('slap_right', playRate=1.0))
        return ival

    def getStumpSwatLeft(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.5), av.actorInterval('swat_left', playRate=1.0))
        return ival

    def getStumpSwatRight(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        ival = Sequence(Func(av.currentWeapon.setTrailLength, 0.5), av.actorInterval('swat_right', playRate=1.0))
        return ival

    def getStumpStomp(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            shockwaveRingEffect = ShockwaveRing.getEffect()
            if shockwaveRingEffect:
                shockwaveRingEffect.reparentTo(av)
                shockwaveRingEffect.size = 40
                shockwaveRingEffect.setPos(0, 0, 3)
                shockwaveRingEffect.play()
            shockwaveRingEffect = ShockwaveRing.getEffect()
            if shockwaveRingEffect:
                shockwaveRingEffect.reparentTo(av)
                shockwaveRingEffect.size = 80
                shockwaveRingEffect.setPos(0, 0, 3)
                shockwaveRingEffect.play()
            shockwaveRingEffect = ShockwaveRing.getEffect()
            if shockwaveRingEffect:
                shockwaveRingEffect.reparentTo(av)
                shockwaveRingEffect.size = 120
                shockwaveRingEffect.setPos(0, 0, 3)
                shockwaveRingEffect.play()
            dustRingEffect = DustRing.getEffect()
            if dustRingEffect:
                dustRingEffect.reparentTo(av)
                dustRingEffect.setPos(0, 0, 0)
                dustRingEffect.play()
            cameraShakerEffect = CameraShaker()
            cameraShakerEffect.reparentTo(av)
            cameraShakerEffect.setPos(0, 0, 0)
            cameraShakerEffect.shakeSpeed = 0.06
            cameraShakerEffect.shakePower = 4.0
            cameraShakerEffect.numShakes = 2
            cameraShakerEffect.scalePower = 1
            cameraShakerEffect.play(50.0)

        ival = Parallel(Sequence(Wait(1.33), Func(startVFX)), Sequence(Func(av.currentWeapon.beginAttack, av), av.actorInterval('jump_attack', playRate=1.0), Func(av.currentWeapon.endAttack, av)))
        return ival

    def getFlyTrapAttackA(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_a', playRate=1.0)

    def getFlyTrapAttackJab(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_jab', playRate=1.0)

    def getFlyTrapLeftFake(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_left_fake', playRate=1.0)

    def getFlyTrapRightFake(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_right_fake', playRate=1.0)

    def getFlyTrapSpit(self, av, skillId, ammoSkillId, charge, target, skillResult):

        def startVFX():
            motion_color = [
             Vec4(1.0, 0.0, 0.5, 1.0), Vec4(1.0, 0.0, 0.0, 1.0)]
            targetPos, speed, impactT = av.getProjectileInfo(skillId, target)
            effect = VenomSpitProjectile.getEffect()
            if effect:
                effect.reparentTo(render)
                effect.setPos(av, 0, 0, av.height * 0.7)
                effect.setH(av.getH(render))
                effect.play(targetPos, speed, target)

        ival = Sequence(av.actorInterval('shoot', endFrame=23), Func(startVFX), av.actorInterval('shoot', startFrame=24))
        return ival

    def getTentacleSlap(self, av, skillId, ammoSkillId, charge, target, skillResult):
        anim = Parallel(Func(av.alignWithVictim, 0.4), Sequence(ActorInterval(av, 'pound_deck', playRate=2.0), Func(av.loop, 'idle', playRate=random.uniform(1.0, 1.2))), Sequence(Wait(0.6), Func(self.playShockwave, av)))
        return anim

    def getTentaclePound(self, av, skillId, ammoSkillId, charge, target, skillResult):
        anim = Parallel(Func(av.alignWithVictim, 0.4), Sequence(ActorInterval(av, 'pound_deck', playRate=2.0), Func(av.loop, 'idle', blendT=0, playRate=random.uniform(1.0, 1.2))))
        return anim

    def getTentacleEnsnare(self, av, skillId, ammoSkillId, charge, target, skillResult):
        anim = Sequence(Parallel(ActorInterval(av, 'grab', playRate=1.0), Func(av.alignWithVictim, 0.66), Sequence(Wait(0.66), Func(av.setupEnsnare), Wait(1.29), Func(av.pickupTarget))), Func(av.loop, 'grab_idle', playRate=random.uniform(1.0, 1.2)))
        return anim

    def getTentaclePiledriver(self, av, skillId, ammoSkillId, charge, target, skillResult):
        anim = Sequence(Parallel(ActorInterval(av, 'grab_slam', playRate=1.0), Sequence(Wait(2.93), Func(av.piledriveTarget))), Func(av.loop, 'idle', playRate=random.uniform(1.0, 1.2)))
        return anim

    def getTentacleRelease(self, av, skillId, ammoSkillId, charge, target, skillResult):
        anim = Sequence(Parallel(ActorInterval(av, 'grab_slam', playRate=1.0), Sequence(Wait(2.93), Func(av.piledriveTarget))), Func(av.loop, 'idle', playRate=random.uniform(1.0, 1.2)))
        return anim

    def getTentacleConstrict(self, av, skillId, ammoSkillId, charge, target, skillResult):
        anim = Sequence(ActorInterval(av, 'grab_constrict', playRate=1.0), Func(av.loop, 'grab_idle', playRate=random.uniform(1.0, 1.2)))
        return anim

    def getKrakenVomit(self, av, skillId, ammoSkillId, charge, target, skillResult):
        anim = Sequence(ActorInterval(av, 'shoot', playRate=1.0), Func(av.loop, 'idle', playRate=random.uniform(1.0, 1.2)))
        return anim

    def getScorpionAttackLeft(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_left', playRate=1.0)

    def getScorpionAttackRight(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_right', playRate=1.0)

    def getScorpionAttackBoth(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_both', playRate=1.0)

    def getScorpionAttackTailSting(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_tail_sting', playRate=1.0)

    def getScorpionPickUpHuman(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('pick_up_human', playRate=1.0)

    def getScorpionRearUp(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('rear_up', playRate=1.0)

    def getAlligatorAttackLeft(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_left', playRate=1.0)

    def getAlligatorAttackRight(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_right', playRate=1.0)

    def getAlligatorAttackStraight(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_straight', playRate=1.0)

    def getAlligatorAttackTailLeft(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_tail_left', playRate=1.0)

    def getAlligatorAttackTailRight(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_tail_right', playRate=1.0)

    def getBatAttackLeft(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_forward', playRate=1.0)

    def getBatAttackRight(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('attack_right', playRate=1.0)

    def getBatShriek(self, av, skillId, ammoSkillId, charge, target, skillResult):

        def playFX():
            shockwaveRingEffect = ShockwaveRing.getEffect()
            if shockwaveRingEffect:
                shockwaveRingEffect.reparentTo(av)
                shockwaveRingEffect.size = 40
                shockwaveRingEffect.setPos(0, 0, 0)
                shockwaveRingEffect.play()

        ival = Sequence(Func(playFX), av.actorInterval('attack_forward', playRate=2.0))
        return ival

    def getBatFlurry(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Sequence(av.actorInterval('attack_right', playRate=2.0), av.actorInterval('attack_forward', playRate=2.0), av.actorInterval('attack_right', playRate=2.0), av.actorInterval('attack_forward', playRate=2.0))
        return ival

    def getWaspAttack(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('sting', playRate=1.0)

    def getWaspAttackLeap(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('leap_sting', playRate=1.0)

    def getWaspAttackSting(self, av, skillId, ammoSkillId, charge, target, skillResult):
        return av.actorInterval('sting', playRate=1.0)

    def playShockwave(self, av):
        pos = av.getPos(render)
        smokeCloudEffect = SmokeCloud.getEffect()
        if smokeCloudEffect:
            smokeCloudEffect.reparentTo(render)
            smokeCloudEffect.setPos(pos)
            smokeCloudEffect.setScale(1.0)
            smokeCloudEffect.spriteScale = 1.0
            smokeCloudEffect.radius = 7.0
            smokeCloudEffect.play()
        shockwaveRingEffect = ShockwaveRing.getEffect()
        if shockwaveRingEffect:
            shockwaveRingEffect.reparentTo(render)
            shockwaveRingEffect.size = 40
            shockwaveRingEffect.setPos(pos)
            shockwaveRingEffect.play()
        cameraShakerEffect = CameraShaker()
        cameraShakerEffect.reparentTo(render)
        cameraShakerEffect.setPos(pos)
        cameraShakerEffect.shakeSpeed = 0.04
        cameraShakerEffect.shakePower = 6.0
        cameraShakerEffect.numShakes = 2
        cameraShakerEffect.scalePower = 1
        cameraShakerEffect.play(80.0)

    def getCastDarkThunderAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None
        seq = Sequence(Func(av.considerEnableMovement), Func(self.lockInput, av), Func(self.playCastSound, av, skillId), av.actorInterval('shoot_up', playRate=1.5, startFrame=6), Func(self.unlockInput, av))
        return seq

    def getGraveBlindAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            effect = JRGraveSmoke.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setEffectColor(Vec4(0.4, 0.6, 0.1, 1))
                effect.radius = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                effect.setPos(av, 0.0, 0.0, 0.0)
                effect.play()

        seq = Sequence(Func(av.considerEnableMovement), Func(self.lockInput, av), Func(self.playCastSound, av, skillId), Func(startVFX), av.actorInterval('roar_idle', playRate=1.75, startFrame=16), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getCorruptionAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            effect = JRSoulHarvest.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 5, 0)
                effect.radius = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                effect.setEffectColor(Vec4(0.8, 1.0, 0.2, 1.0))
                effect.play()
            effect = DomeExplosion.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 5, 0)
                effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId) * 2.0
                effect.play()
            effect = DarkPortal.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 5, 0)
                effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId) * 4.0
                effect.play()
            effect = EvilRingEffect.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 5, 0)
                effect.effectScale = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                effect.changeEffectColor(Vec4(0.8, 1.0, 0.1, 1.0))
                effect.duration = 2.5
                effect.play()

        seq = Sequence(Func(av.considerEnableMovement), Func(self.lockInput, av), Func(self.playCastSound, av, skillId), Func(startVFX), av.actorInterval('roar_idle', playRate=1.75, startFrame=16), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getSoulHarvestAnim(self, av, skillId, ammoSkillId, charge, target, skillResult):
        if not av.currentWeapon:
            return None

        def startVFX():
            effect = WindWave.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setEffectColor(Vec4(0.8, 1, 0.2, 0.7))
                effect.setPos(av, 0.0, 0.0, 0.0)
                effect.setScale(1.0, 1.0, 1.0)
                effect.setHpr(0.0, 0.0, 0.0)
                effect.play()
            effect = JRSoulHarvest2.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 0, 2)
                effect.radius = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                effect.play()
            effect = DesolationSmoke.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setEffectColor(Vec4(0.8, 1, 0.2, 1))
                effect.setPos(av, 0.0, 0.0, 0.0)
                effect.play()
            effect = DomeExplosion.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 0, 0)
                effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId)
                effect.play()
            effect = DarkPortal.getEffect(unlimited=True)
            if effect:
                effect.reparentTo(av.getParent())
                effect.setPos(av, 0, 0, 0)
                effect.size = av.cr.battleMgr.getModifiedAttackAreaRadius(av, skillId, ammoSkillId) * 3.0
                effect.play()
            cameraShakerEffect = CameraShaker()
            cameraShakerEffect.wrtReparentTo(av.getParent())
            cameraShakerEffect.setPos(av, 0.0, 0.0, 0.0)
            cameraShakerEffect.shakeSpeed = 0.075
            cameraShakerEffect.shakePower = 1.0
            cameraShakerEffect.numShakes = 30
            cameraShakerEffect.scalePower = 1
            cameraShakerEffect.play(100.0)

        seq = Sequence(Func(av.considerEnableMovement), Func(self.lockInput, av), Func(self.playCastSound, av, skillId), Func(startVFX), av.actorInterval('roar_idle', playRate=1.75, startFrame=16), Func(self.unlockInput, av))
        del startVFX
        return seq

    def getBroadsideLeft(self, av, skillId, ammoSkillId, charge=0, target=None, skillResult=None):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getLeftBroadsidePhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getLeftBroadsidePhrase())), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getBroadsideRight(self, av, skillId, ammoSkillId, charge=0, target=None, skillResult=None):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getRightBroadsidePhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getRightBroadsidePhrase())), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getFullSail(self, av, skillId, ammoSkillId, charge=0, target=None, skillResult=None):

        def playSfx():
            if not av.ship:
                return
            sfx = av.ship.fullsailSfx
            base.playSfx(sfx, node=av.ship, cutoff=1500)

        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getFullSailPhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getFullSailPhrase())), Func(playSfx), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        del playSfx
        return ival

    def getComeAbout(self, av, skillId, ammoSkillId, charge=0, target=None, skillResult=None):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getComeAboutPhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getComeAboutPhrase())), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getRammingSpeed(self, av, skillId, ammoSkillId, charge=0, target=None, skillResult=None):

        def playSfx():
            if not av.ship:
                return
            sfx = av.ship.fullsailSfx
            base.playSfx(sfx, node=av.ship, cutoff=1500)

        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.RammingSpeed, CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.RammingSpeed)), Func(playSfx), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        del playSfx
        return ival

    def getOpenFire(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getOpenFirePhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getOpenFirePhrase())), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getTakeCover(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getTakeCoverPhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getTakeCoverPhrase())), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getPowerRecharge(self, av, skillId, ammoSkillId, charge=0, target=None, skillResult=None):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getPowerRechargePhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getPowerRechargePhrase())), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getWreckHull(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getWreckHullPhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getWreckHullPhrase())), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getWreckMasts(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getWreckMastsPhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getWreckMastsPhrase())), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getSinkHer(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getSinkHerPhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getSinkHerPhrase())), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getIncoming(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getIncomingPhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getIncomingPhrase())), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getFixItNow(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Parallel(Sequence(Func(self.lockInput, av), Func(av.setChatAbsolute, PLocalizer.getFixItNowPhrase(), CFSpeech | CFTimeout), Func(base.talkAssistant.receiveOpenTalk, av.doId, av.getName(), None, None, PLocalizer.getFixItNowPhrase())), Sequence(Wait(1.0), Func(self.unlockInput, av)))
        return ival

    def getShipRepair(self, av, skillId, ammoSkillId, charge=0, target=None, skillResult=None):
        return self.getComeAbout(av, skillId, ammoSkillId, charge)

    def getSummonHelp(self, av, skillId, ammoSkillId, charge, target, skillResult):
        ival = Sequence(Func(self.lockInput, av), Func(av.motionFSM.off), Func(self.playCastingAnim, av), av.actorInterval('voodoo_swarm', playRate=1.0, blendInT=0.3, blendOutT=0.3), Func(av.considerEnableMovement), Func(self.unlockInput, av))
        return ival

    def lockInput(self, av):
        if av.isLocal():
            messenger.send('skillStarted')

    def unlockInput(self, av):
        if av.isLocal():
            messenger.send('skillFinished')

    def lockDrink(self, av):
        if av.isLocal():
            messenger.send('drinkingStarted')

    def unlockDrink(self, av):
        if av.isLocal():
            messenger.send('drinkingFinished')