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

class Grenade(Weapon.Weapon):
    modelTypes = [
     'models/ammunition/grenade']
    walkAnim = 'walk'
    runAnim = 'run_with_weapon'
    neutralAnim = 'bomb_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'bomb_hurt'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'grenade')
        self.ammoSkillId = 0

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def changeStance(self, av):
        if av.getGameState() == 'WaterRoam' or av.getGameState() == 'WaterTreasureRoam':
            return
        if not self.ammoSkillId:
            self.walkAnim = 'walk'
            self.runAnim = 'run'
            self.walkBackAnim = 'walk'
            self.neutralAnim = 'idle'
            self.strafeLeftAnim = 'strafe_left'
            self.strafeRightAnim = 'strafe_right'
            self.strafeDiagLeftAnim = 'run_diagonal_left'
            self.strafeDiagRightAnim = 'run_diagonal_right'
            self.strafeRevDiagLeftAnim = 'walk_back_diagonal_left'
            self.strafeRevDiagRightAnim = 'walk_back_diagonal_right'
            self.painAnim = 'boxing_hit_head_right'
            self.prop.setPos(-0.05, -0.05, -0.2)
            self.prop.setScale(0.45)
            av.speedIndex = PiratesGlobals.SPEED_BATTLE_INDEX
            if av.isLocal():
                av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[av.speedIndex])
        elif self.ammoSkillId == InventoryType.GrenadeSiege:
            self.walkAnim = 'bigbomb_walk'
            self.runAnim = 'bigbomb_walk'
            self.walkBackAnim = 'bigbomb_walk'
            self.neutralAnim = 'bigbomb_idle'
            self.strafeLeftAnim = 'bigbomb_walk_left'
            self.strafeRightAnim = 'bigbomb_walk_right'
            self.strafeDiagLeftAnim = 'bigbomb_walk_left_diagonal'
            self.strafeDiagRightAnim = 'bigbomb_walk_right_diagonal'
            self.strafeRevDiagLeftAnim = 'bigbomb_walk_back_left'
            self.strafeRevDiagRightAnim = 'bigbomb_walk_back_right'
            self.painAnim = 'boxing_hit_head_right'
            self.prop.setPos(-0.15, -0.25, -0.5)
            self.prop.setScale(1.25)
            av.speedIndex = PiratesGlobals.SPEED_HEAVY_INDEX
            if av.isLocal():
                av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[av.speedIndex])
        else:
            self.walkAnim = 'walk'
            self.runAnim = 'run'
            self.walkBackAnim = 'walk'
            self.neutralAnim = 'bomb_idle'
            self.strafeLeftAnim = 'strafe_left'
            self.strafeRightAnim = 'strafe_right'
            self.strafeDiagLeftAnim = 'run_diagonal_left'
            self.strafeDiagRightAnim = 'run_diagonal_right'
            self.strafeRevDiagLeftAnim = 'walk_back_diagonal_left'
            self.strafeRevDiagRightAnim = 'walk_back_diagonal_right'
            self.painAnim = 'boxing_hit_head_right'
            self.prop.setPos(-0.05, -0.05, -0.2)
            self.prop.setScale(0.45)
            av.speedIndex = PiratesGlobals.SPEED_BATTLE_INDEX
            if av.isLocal():
                av.controlManager.setSpeeds(*PiratesGlobals.PirateSpeeds[av.speedIndex])
        av.setWalkForWeapon()

    def setAmmoSkillId(self, ammoSkillId):
        self.ammoSkillId = ammoSkillId

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        if ammoSkillId == InventoryType.GrenadeSiege:
            track = Parallel(av.actorInterval('bigbomb_draw', playRate=1.5, endFrame=40, blendInT=blendInT, blendOutT=blendOutT), Func(base.playSfx, self.drawSfx, node=av, cutoff=60), Sequence(Wait(0.343), Func(self.attachTo, av), Func(self.setAmmoSkillId, ammoSkillId), Func(self.changeStance, av)))
        else:
            track = Parallel(av.actorInterval('bomb_draw', playRate=1.5, endFrame=30, blendInT=blendInT, blendOutT=blendOutT), Func(base.playSfx, self.drawSfx, node=av, cutoff=60), Sequence(Wait(0.125), Func(self.attachTo, av), Func(self.setAmmoSkillId, ammoSkillId), Func(self.changeStance, av)))
        return track

    def getReturnIval(self, av, ammoSkillId=0, blendInT=0, blendOutT=0.1):
        if av.curAttackAnim:
            av.curAttackAnim.pause()
            av.curAttackAnim = None
        if not ammoSkillId:
            ammoSkillId = self.ammoSkillId
        if ammoSkillId == InventoryType.GrenadeSiege:
            track = Parallel(av.actorInterval('bigbomb_draw', playRate=1.5, startFrame=28, endFrame=1, blendInT=blendInT, blendOutT=blendOutT), Func(base.playSfx, self.returnSfx, node=av, cutoff=60), Sequence(Wait(0.5), Func(self.detachFrom, av), Func(self.setAmmoSkillId, 0), Func(self.changeStance, av)))
        else:
            track = Parallel(av.actorInterval('bomb_draw', playRate=1.5, startFrame=20, endFrame=1, blendInT=blendInT, blendOutT=blendOutT), Func(base.playSfx, self.returnSfx, node=av, cutoff=60), Sequence(Wait(0.468), Func(self.detachFrom, av), Func(self.setAmmoSkillId, 0), Func(self.changeStance, av)))
        return track

    def getAmmoChangeIval(self, av, skillId, ammoSkillId, charge, target=None):
        if self.ammoSkillId == InventoryType.GrenadeSiege:
            track = Sequence(Func(base.playSfx, self.returnSfx, node=av, cutoff=60), av.actorInterval('bigbomb_draw', startFrame=28, endFrame=11, blendInT=0.25, blendOutT=0), Func(self.detachFrom, av))
        else:
            track = Sequence(Func(base.playSfx, self.returnSfx, node=av, cutoff=60), av.actorInterval('bomb_draw', startFrame=20, endFrame=11, blendInT=0.25, blendOutT=0), Func(self.detachFrom, av))
        if ammoSkillId:
            track.append(Func(self.attachTo, av))
        if ammoSkillId == InventoryType.GrenadeSiege:
            track.append(Func(self.setAmmoSkillId, ammoSkillId))
            track.append(Func(self.changeStance, av))
            track.append(av.actorInterval('bigbomb_draw', startFrame=12, endFrame=40, blendInT=0, blendOutT=0.5))
            track.append(Func(self.unlockInput, av))
        else:
            track.append(Func(self.setAmmoSkillId, ammoSkillId))
            track.append(Func(self.changeStance, av))
            track.append(av.actorInterval('bomb_draw', startFrame=12, endFrame=30, blendInT=0, blendOutT=0.5))
            track.append(Func(self.unlockInput, av))
        return track

    @classmethod
    def setupSounds(cls):
        Grenade.aimSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_AIM),)
        Grenade.reloadSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_RELOAD),)
        Grenade.skillSfxs = {InventoryType.GrenadeThrow: loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_THROW),InventoryType.GrenadeSiege: loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_SEIGE),InventoryType.GrenadeLongVolley: loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_LONG_VOLLEY)}
        Grenade.chargingSfx = loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_CHARGING)
        Grenade.drawSfx = loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_DRAW)
        Grenade.returnSfx = loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_SHEATHE)

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
    return Grenade.aimSfxs


def getReloadSfx():
    return Grenade.reloadSfxs