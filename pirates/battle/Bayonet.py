import Weapon
import WeaponGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.uberdog.UberDogGlobals import InventoryType
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.inventory import ItemGlobals
import random

def beginInterrupt(av):
    if av.isLocal():
        messenger.send('skillFinished')


class Bayonet(Weapon.Weapon):
    modelTypes = [
     'models/handheld/pir_m_hnd_gun_musket_a', 'models/handheld/pir_m_hnd_gun_musket_b', 'models/handheld/pir_m_hnd_gun_musket_c', 'models/handheld/pir_m_hnd_gun_musket_d', 'models/handheld/pir_m_hnd_gun_musket_e']
    walkAnim = 'bayonet_attack_walk'
    runAnim = 'bayonet_run'
    walkBackAnim = 'bayonet_attack_walk'
    neutralAnim = 'bayonet_attack_idle'
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
        Weapon.Weapon.__init__(self, itemId, 'bayonet')

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def changeStance(self, av):
        if av.getGameState() == 'Battle':
            self.walkAnim = 'bayonet_attack_walk'
            self.neutralAnim = 'bayonet_attack_idle'
            self.runAnim = 'bayonet_run'
            self.walkBackAnim = 'bayonet_attack_walk'
        else:
            self.walkAnim = 'bayonet_walk'
            self.neutralAnim = 'bayonet_idle'
            self.runAnim = 'bayonet_run'
            self.walkBackAnim = 'bayonet_walk'
        av.setWalkForWeapon()

    def getAmmoModel():
        bullet = loader.loadModel('models/props/cannonball-trail-lod')
        bullet.setScale(0.3)
        return bullet

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(av.actorInterval('gun_draw', playRate=1.5, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.625), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(av.actorInterval('gun_putaway', playRate=2, endFrame=37, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.6), Func(self.detachFrom, av)))
        if base.cr.targetMgr:
            track.append(Func(base.cr.targetMgr.setWantAimAssist, 0))
        return track

    def getAnimState(self, av, animState):
        if av.isNpc and animState == 'LandRoam':
            return 'BayonetLandRoam'
        else:
            return animState

    @classmethod
    def setupSounds(cls):
        Bayonet.hitSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_BAYONET_HIT),)
        Bayonet.mistimedHitSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_BAYONET_HIT),)
        Bayonet.aimSfxs = (None, )
        Bayonet.gunCockSfxs = (None, )
        Bayonet.reloadSfx = loadSfx(SoundGlobals.SFX_WEAPON_PISTOL_RELOAD)
        Bayonet.missSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_BAYONET_MISS), loadSfx(SoundGlobals.SFX_WEAPON_BAYONET_MISS_ALT))
        Bayonet.skillSfxs = {InventoryType.PistolShoot: loadSfx(SoundGlobals.SFX_WEAPON_MUSKET_SHOOT),InventoryType.PistolTakeAim: loadSfx(SoundGlobals.SFX_WEAPON_MUSKET_SHOOT)}
        return None


def getShootSfx():
    return Bayonet.shootSfxs


def getHitSfx():
    return Bayonet.hitSfxs


def getMistimedHitSfx():
    return Bayonet.mistimedHitSfxs


def getMissSfx():
    return Bayonet.missSfxs


def getAimSfx():
    return Bayonet.aimSfxs


def getGunCockSfx():
    return Bayonet.gunCockSfxs