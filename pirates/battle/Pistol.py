import Weapon
import WeaponGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.inventory import ItemGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.effects.PulsingGlow import PulsingGlow
from pirates.battle.EnemySkills import EnemySkills
import random

class Pistol(Weapon.Weapon):
    modelTypes = [
     'models/handheld/pir_m_hnd_gun_pistol_a', 'models/handheld/pir_m_hnd_gun_pistol_b', 'models/handheld/pir_m_hnd_gun_pistol_c', 'models/handheld/pir_m_hnd_gun_pistol_d', 'models/handheld/pir_m_hnd_gun_multiBarrel_a', 'models/handheld/pir_m_hnd_gun_multiBarrel_b', 'models/handheld/pir_m_hnd_gun_multiBarrel_c', 'models/handheld/pir_m_hnd_gun_multiBarrel_d', 'models/handheld/pir_m_hnd_gun_multiBarrel_e', 'models/handheld/pir_m_hnd_gun_multiBarrel_f', 'models/handheld/pir_m_hnd_gun_multiBarrel_g', 'models/handheld/pir_m_hnd_gun_multiBarrel_h']
    walkAnim = 'walk'
    runAnim = 'run_with_weapon'
    neutralAnim = 'gun_pointedup_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'gun_hurt'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'pistol')
        self.pulseGlow = None
        return

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def delete(self):
        self.stopPulseGlow()
        Weapon.Weapon.delete(self)

    def getAmmoModel():
        bullet = loader.loadModel('models/props/cannonball-trail-lod')
        bullet.setScale(0.3)
        return bullet

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(Func(base.playSfx, self.drawSfx, node=av, cutoff=60), av.actorInterval('gun_draw', playRate=1.5, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.625), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(Func(base.playSfx, self.returnSfx, node=av, cutoff=60), av.actorInterval('gun_putaway', playRate=2, endFrame=37, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.6), Func(self.detachFrom, av)))
        if base.cr.targetMgr:
            track.append(Func(base.cr.targetMgr.setWantAimAssist, 0))
        return track

    def startPulseGlow(self):
        if not self.pulseGlow:
            self.pulseGlow = PulsingGlow.getEffect()
            if self.pulseGlow:
                self.pulseGlow.reparentTo(self)
                self.pulseGlow.setEffectColor(Vec4(1, 0.9, 0.8, 0.5))
                self.pulseGlow.setPos(0.2, 0.25, 0)
                self.pulseGlow.setScale(0.3)
                self.pulseGlow.startLoop()

    def stopPulseGlow(self):
        if self.pulseGlow:
            self.pulseGlow.stopLoop()
            self.pulseGlow = None
        return

    @classmethod
    def setupSounds(cls):
        hpHit = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_HP_HIT)
        manaHit = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_MANA_HIT)
        Pistol.hitSfxs = {InventoryType.PistolLeadShot: hpHit,InventoryType.PistolBaneShot: manaHit,InventoryType.PistolSilverShot: hpHit,InventoryType.PistolHexEaterShot: manaHit,InventoryType.PistolSteelShot: hpHit,InventoryType.PistolVenomShot: manaHit}
        Pistol.mistimedHitSfxs = {InventoryType.PistolLeadShot: hpHit,InventoryType.PistolBaneShot: manaHit,InventoryType.PistolSilverShot: hpHit,InventoryType.PistolHexEaterShot: manaHit,InventoryType.PistolSteelShot: hpHit,InventoryType.PistolVenomShot: manaHit}
        Pistol.missSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_MISS),)
        Pistol.aimSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_AIM),)
        Pistol.skillSfxs = {InventoryType.PistolShoot: loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_SHOOT),InventoryType.PistolTakeAim: loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_WELL_AIMED),EnemySkills.PISTOL_POINT_BLANK: loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_SHOOT),EnemySkills.PISTOL_RAPIDFIRE: loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_SHOOT)}
        Pistol.drawSfx = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_DRAW)
        Pistol.gunCockSfx = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_COCK)
        Pistol.reloadSfx = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_RELOAD)
        Pistol.returnSfx = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_SHEATHE)


def getHitSfx():
    return Pistol.hitSfxs


def getMistimedHitSfx():
    return Pistol.mistimedHitSfxs


def getMissSfx():
    return Pistol.missSfxs


def getAimSfx():
    return Pistol.aimSfxs