import Weapon
import WeaponGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.inventory import ItemGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.battle.EnemySkills import EnemySkills
import random

def beginInterrupt(av):
    if av.isLocal():
        messenger.send('skillFinished')


class Gun(Weapon.Weapon):
    modelTypes = [
     'models/handheld/pir_m_hnd_gun_blunderbuss_a', 'models/handheld/pir_m_hnd_gun_blunderbuss_b', 'models/handheld/pir_m_hnd_gun_blunderbuss_c', 'models/handheld/pir_m_hnd_gun_blunderbuss_d', 'models/handheld/pir_m_hnd_gun_blunderbuss_e', 'models/handheld/pir_m_hnd_gun_musket_a', 'models/handheld/pir_m_hnd_gun_musket_b', 'models/handheld/pir_m_hnd_gun_musket_c', 'models/handheld/pir_m_hnd_gun_musket_d', 'models/handheld/pir_m_hnd_gun_musket_e']
    walkAnim = 'rifle_fight_walk'
    runAnim = 'bayonet_run'
    walkBackAnim = 'rifle_fight_walk'
    neutralAnim = 'rifle_fight_idle'
    strafeLeftAnim = 'rifle_fight_run_strafe_left'
    strafeRightAnim = 'rifle_fight_run_strafe_right'
    strafeDiagLeftAnim = 'rifle_fight_forward_diagonal_left'
    strafeDiagRightAnim = 'rifle_fight_forward_diagonal_right'
    strafeRevDiagLeftAnim = 'rifle_fight_walk_back_diagonal_left'
    strafeRevDiagRightAnim = 'rifle_fight_walk_back_diagonal_right'
    fallGroundAnim = 'bayonet_fall_ground'
    spinLeftAnim = 'bayonet_turn_left'
    spinRightAnim = 'bayonet_turn_right'
    painAnim = 'boxing_hit_head_right'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'gun')
        self.ramRod = None
        return

    def delete(self):
        if self.ramRod:
            self.ramRod.removeNode()
            del self.ramRod
            self.ramRod = None
        Weapon.Weapon.delete(self)
        return

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        if ItemGlobals.getSubtype(self.itemId) == ItemGlobals.MUSKET:
            bayonetPart = self.prop.find('**/bayonet')
            if bayonetPart:
                bayonetPart.stash()
        self.prop.reparentTo(self)

    def getAmmoModel():
        bullet = loader.loadModel('models/props/cannonball-trail-lod')
        bullet.setScale(0.3)
        return bullet

    def getRamRod(self):
        if not self.ramRod:
            self.ramRod = loader.loadModel('models/handheld/pir_m_hnd_gun_ramrod')
        return self.ramRod

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(av.actorInterval('gun_draw', playRate=1.5, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.625), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(av.actorInterval('gun_putaway', playRate=2, endFrame=37, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.6), Func(self.detachFrom, av)))
        if base.cr.targetMgr:
            track.append(Func(base.cr.targetMgr.setWantAimAssist, 0))
        return track

    @classmethod
    def setupSounds(cls):
        hpHit = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_HP_HIT)
        manaHit = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_MANA_HIT)
        Gun.shootSfxs = {InventoryType.PistolLeadShot: hpHit,InventoryType.PistolBaneShot: manaHit,InventoryType.PistolSilverShot: hpHit,InventoryType.PistolHexEaterShot: manaHit,InventoryType.PistolSteelShot: hpHit,InventoryType.PistolVenomShot: manaHit}
        Gun.aimSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_AIM),)
        Gun.skillSfxs = {InventoryType.PistolShoot: loadSfx(SoundGlobals.SFX_WEAPON_BLUNDERBUSS_SHOOT),InventoryType.PistolTakeAim: loadSfx(SoundGlobals.SFX_WEAPON_BLUNDERBUSS_SHOOT),EnemySkills.PISTOL_DEADEYE: loadSfx(SoundGlobals.SFX_WEAPON_BLUNDERBUSS_SHOOT),EnemySkills.PISTOL_STUNSHOT: loadSfx(SoundGlobals.SFX_WEAPON_BLUNDERBUSS_SHOOT),EnemySkills.PISTOL_BREAKSHOT: loadSfx(SoundGlobals.SFX_WEAPON_BLUNDERBUSS_SHOOT),EnemySkills.PISTOL_HOTSHOT: loadSfx(SoundGlobals.SFX_WEAPON_BLUNDERBUSS_SHOOT),EnemySkills.PISTOL_SCATTERSHOT_AIM: loadSfx(SoundGlobals.SFX_WEAPON_BLUNDERBUSS_SHOOT)}
        Gun.drawSfx = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_DRAW)
        Gun.gunCockSfx = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_COCK)
        Gun.reloadSfx = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_RELOAD)
        Gun.returnSfx = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_SHEATHE)
        Gun.hitSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_DAGGER_HIT),)
        Gun.mistimedHitSfxs = (
         loader.loadSfx('audio/sfx_dagger_impact.mp3'),)
        Gun.missSfxs = (
         loader.loadSfx('audio/whoosh-10.mp3'), loader.loadSfx('audio/arm-Whoosh-05.mp3'))
        Gun.blunderbussShootSfx = loadSfx(SoundGlobals.SFX_WEAPON_BLUNDERBUSS_SHOOT)
        Gun.musketShootSfx = loadSfx(SoundGlobals.SFX_WEAPON_MUSKET_SHOOT)


def getShootSfx():
    return Gun.shootSfxs


def getHitSfx():
    return Gun.hitSfxs


def getMistimedHitSfx():
    return Gun.mistimedHitSfxs


def getMissSfx():
    return Gun.missSfxs


def getAimSfx():
    return Gun.aimSfxs


def getBlunderbussShootSfx():
    return Gun.blunderbussShootSfx


def getMusketShootSfx():
    return Gun.musketShootSfx