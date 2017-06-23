import Weapon
import WeaponGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.battle.EnemySkills import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals
from pirates.piratesbase import PLocalizer
from pirates.effects import PolyTrail
import random

class Torch(Weapon.Weapon):
    modelTypes = [
     'models/props/torch']
    models = {}
    icons = {}
    vertex_list = [
     Vec4(0.0, 0.4, 0.0, 1.0), Vec4(0.0, 2.0, 0.0, 1.0), Vec4(-0.55, 2.95, 0.0, 1.0)]
    motion_color = {ItemGlobals.MotionBlurDefault: [Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.6, 0.6, 0.6, 0.5)],ItemGlobals.MotionBlurRusty: [Vec4(0.3, 0.4, 0.1, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.6, 0.6, 0.6, 0.5)],ItemGlobals.MotionBlurIron: [Vec4(0.1, 0.2, 0.4, 0.5), Vec4(0.4, 0.5, 0.7, 0.5), Vec4(0.5, 0.5, 0.9, 0.75)],ItemGlobals.MotionBlurSteel: [Vec4(1, 1, 0.4, 0.5), Vec4(0.4, 0.5, 0.6, 0.5), Vec4(0.7, 0.7, 0.8, 0.75)],ItemGlobals.MotionBlurFine: [Vec4(0.6, 0.6, 0.75, 1), Vec4(0.6, 0.5, 0.2, 1), Vec4(0.6, 0.6, 0.4, 1)],ItemGlobals.MotionBlurPirate: [Vec4(1, 0.2, 0.2, 0.5), Vec4(0.5, 0.5, 0.5, 0.75), Vec4(0.7, 0.7, 0.9, 1)],ItemGlobals.MotionBlurDark: [Vec4(1, 1, 0, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.1, 0.1, 0.1, 1.0)]}
    walkAnim = 'walk'
    runAnim = 'run_with_weapon'
    neutralAnim = 'sword_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'boxing_hit_head_right'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'torch')
        self.colorIval = None
        return

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.setScale(0.5)
        self.prop.setP(-90)
        self.prop.reparentTo(self)

    def delete(self):
        taskMgr.remove('stopSpecialEffectTask')
        self.endAttack(None)
        self.removeTrail()
        Weapon.Weapon.delete(self)
        return

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(Func(base.playSfx, self.drawSfx, node=av, cutoff=60), av.actorInterval('sword_draw', playRate=1.5, endFrame=15, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.187), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(Func(base.playSfx, self.returnSfx, node=av, cutoff=60), av.actorInterval('sword_putaway', playRate=2, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.detachFrom, av)))
        return track

    def attachTo(self, av):
        Weapon.Weapon.attachTo(self, av)
        if hasattr(av, 'isGhost') and av.isGhost:
            return
        self.createTrail(av)

    def detachFrom(self, av):
        Weapon.Weapon.detachFrom(self, av)
        self.removeTrail()

    def createTrail(self, target):
        if self.isEmpty():
            return
        if not self.motion_trail:
            motion_trail_color = []
            colorId = ItemGlobals.getVfxType1(self.itemId)
            motion_trail_color = self.motion_color.get(colorId)
            if not motion_trail_color:
                motion_trail_color = self.motion_color.get(ItemGlobals.MotionBlurDefault)
            self.motion_trail = PolyTrail.PolyTrail(target, self.vertex_list, motion_trail_color)
            self.motion_trail.reparentTo(self)
            self.motion_trail.setUseNurbs(1)
            card = loader.loadModel('models/effects/swordtrail_effects')
            tex = card.find('**/swordtrail_lines').findTexture('*')
            self.motion_trail.setTexture(tex)
            self.motion_trail.setBlendModeOn()
            if colorId == ItemGlobals.MotionBlurDark:
                self.motion_trail.setBlendModeOff()
            card.removeNode()

    def removeTrail(self):
        if self.motion_trail:
            self.motion_trail.destroy()
            self.motion_trail = None
        return

    def getBlurColor(self):
        colorId = ItemGlobals.getVfxType1(self.itemId)
        motion_trail_color = self.motion_color.get(colorId)
        if not motion_trail_color:
            motion_trail_color = self.motion_color.get(ItemGlobals.MotionBlurDefault)
        return motion_trail_color[2]

    @classmethod
    def setupSounds(cls):
        Torch.hitSfxs = {ItemGlobals.QUEST_PROP_TORCH: (loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CLASHCLANG), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_01), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_02), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_03))}
        Torch.missSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWOOSH_01), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWOOSH_02))
        Torch.mistimedHitSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_MISTIMEDHIT),)
        Torch.skillSfxs = {InventoryType.CutlassHack: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),InventoryType.CutlassSlash: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SLASH),InventoryType.CutlassStab: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_STAB),InventoryType.CutlassFlourish: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_FLOURISH),InventoryType.CutlassCleave: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CLEAVE),InventoryType.CutlassTaunt: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_TAUNT),InventoryType.CutlassBrawl: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_BRAWL),InventoryType.CutlassSweep: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWEEP),InventoryType.CutlassBladestorm: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_BLADESTORM),EnemySkills.CUTLASS_BLOWBACK: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_BLOWBACK),EnemySkills.CUTLASS_CAPTAINS_FURY: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CAPTAINS_FURY),EnemySkills.CUTLASS_CURSED_FIRE: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CURSED_FIRE),EnemySkills.CUTLASS_CURSED_THUNDER: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CURSED_THUNDER),EnemySkills.CUTLASS_CURSED_ICE: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CURSED_ICE),EnemySkills.MISC_CAPTAINS_RESOLVE: loadSfx(SoundGlobals.SFX_WEAPON_SKILL_CAPTAINS_RESOLVE)}
        Torch.drawSfx = loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_DRAW)
        Torch.returnSfx = loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SHEATHE)


def getHitSfx():
    return Torch.hitSfxs


def getMistimedHitSfx():
    return Torch.mistimedHitSfxs


def getMissSfx():
    return Torch.missSfxs