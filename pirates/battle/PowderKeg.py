from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.battle.WeaponGlobals import *
from pirates.inventory import ItemGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
import Weapon
import WeaponGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class PowderKeg(Weapon.Weapon):
    modelTypes = [
     'models/handheld/pir_m_hnd_bom_barrelDynamite']
    walkAnim = 'bigbomb_walk'
    runAnim = 'bigbomb_walk'
    walkBackAnim = 'bigbomb_walk'
    neutralAnim = 'bigbomb_idle'
    strafeLeftAnim = 'bigbomb_walk_left'
    strafeRightAnim = 'bigbomb_walk_right'
    strafeDiagLeftAnim = 'bigbomb_walk_left_diagonal'
    strafeDiagRightAnim = 'bigbomb_walk_right_diagonal'
    strafeRevDiagLeftAnim = 'bigbomb_walk_back_left'
    strafeRevDiagRightAnim = 'bigbomb_walk_back_right'
    painAnim = 'boxing_hit_head_right'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'grenade')
        self.ammoSkillId = 0

    def delete(self):
        Weapon.Weapon.delete(self)

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.setPos(-0.3, 0.0, -0.8)
        self.prop.setHpr(0, 225, -15)
        self.prop.reparentTo(self)

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(av.actorInterval('bigbomb_draw', playRate=1.5, endFrame=40, blendInT=blendInT, blendOutT=blendOutT), Func(base.playSfx, self.drawSfx, node=av, cutoff=60), Sequence(Wait(0.343), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, ammoSkillId=0, blendInT=0, blendOutT=0.1):
        if not ammoSkillId:
            ammoSkillId = self.ammoSkillId
        track = Parallel(av.actorInterval('bigbomb_draw', playRate=1.5, startFrame=28, endFrame=1, blendInT=blendInT, blendOutT=blendOutT), Func(base.playSfx, self.returnSfx, node=av, cutoff=60), Sequence(Wait(0.5), Func(self.detachFrom, av)))
        return track

    @classmethod
    def setupSounds(cls):
        PowderKeg.aimSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_AIM),)
        PowderKeg.reloadSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_RELOAD),)
        PowderKeg.skillSfxs = {}
        PowderKeg.chargingSfx = loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_CHARGING)
        PowderKeg.drawSfx = loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_DRAW)
        PowderKeg.returnSfx = loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_SHEATHE)

    def lockInput(self, av):
        if av.isLocal():
            messenger.send('skillStarted')

    def unlockInput(self, av):
        if av.isLocal():
            messenger.send('skillFinished')


def getHitSfx():
    return None


def getMistimedHitSfx():
    return None


def getMissSfx():
    return None


def getAimSfx():
    return PowderKeg.aimSfxs


def getReloadSfx():
    return PowderKeg.reloadSfxs