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
from pirates.effects.SwordFlame import SwordFlame
from pirates.effects.SwordFreeze import SwordFreeze
from pirates.effects.SwordThunders import SwordThunders
import random

class Sword(Weapon.Weapon):
    modelTypes = [
     'models/handheld/pir_m_hnd_swd_cutlass_a', 'models/handheld/pir_m_hnd_swd_cutlass_b', 'models/handheld/pir_m_hnd_swd_cutlass_c', 'models/handheld/pir_m_hnd_swd_cutlass_d', 'models/handheld/pir_m_hnd_swd_cutlass_e', 'models/handheld/pir_m_hnd_swd_cutlass_f', 'models/handheld/pir_m_hnd_swd_cutlass_g', 'models/handheld/pir_m_hnd_swd_cutlass_h', 'models/handheld/pir_m_hnd_swd_cutlass_i', 'models/handheld/pir_m_hnd_swd_cutlass_j', 'models/handheld/pir_m_hnd_swd_cutlass_k', 'models/handheld/pir_m_hnd_swd_broadsword_a', 'models/handheld/pir_m_hnd_swd_broadsword_b', 'models/handheld/pir_m_hnd_swd_broadsword_c', 'models/handheld/pir_m_hnd_swd_broadsword_d', 'models/handheld/pir_m_hnd_swd_broadsword_e', 'models/handheld/pir_m_hnd_swd_broadsword_f', 'models/handheld/pir_m_hnd_swd_broadsword_triton', 'models/handheld/pir_m_hnd_swd_sabre_a', 'models/handheld/pir_m_hnd_swd_sabre_b', 'models/handheld/pir_m_hnd_swd_sabre_c', 'models/handheld/pir_m_hnd_swd_sabre_d', 'models/handheld/pir_m_hnd_swd_sabre_e', 'models/handheld/pir_m_hnd_swd_sabre_f', 'models/handheld/pir_m_hnd_swd_scimitar_a', 'models/handheld/pir_m_hnd_swd_scimitar_b', 'models/handheld/pir_m_hnd_swd_scimitar_c', 'models/handheld/pir_m_hnd_swd_scimitar_d', 'models/handheld/pir_m_hnd_swd_scimitar_e', 'models/handheld/pir_m_hnd_swd_scimitar_f', 'models/handheld/pir_m_hnd_swd_davyJones_a', 'models/handheld/pir_m_hnd_swd_davyJones_b', 'models/handheld/pir_m_hnd_swd_davyJones_c', 'models/handheld/pir_m_hnd_swd_davyJones_d', 'models/handheld/pir_m_hnd_swd_davyJones_e', 'models/handheld/pir_m_hnd_swd_davyJones_f', 'models/handheld/pir_m_hnd_swd_davyJones_g', 'models/handheld/pir_m_hnd_swd_davyJones_h', 'models/handheld/pir_m_hnd_swd_davyJones_i', 'models/handheld/pir_m_hnd_swd_davyJones_j']
    models = {}
    icons = {}
    vertex_list = [
     Vec4(0.0, 0.4, 0.0, 1.0), Vec4(0.0, 2.0, 0.0, 1.0), Vec4(-0.55, 2.95, 0.0, 1.0)]
    motion_color = {ItemGlobals.MotionBlurDefault: [Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.6, 0.6, 0.6, 0.5)],ItemGlobals.MotionBlurRusty: [Vec4(0.3, 0.4, 0.1, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.6, 0.6, 0.6, 0.5)],ItemGlobals.MotionBlurIron: [Vec4(0.1, 0.2, 0.4, 0.5), Vec4(0.4, 0.5, 0.7, 0.5), Vec4(0.5, 0.5, 0.9, 0.75)],ItemGlobals.MotionBlurSteel: [Vec4(1, 1, 0.4, 0.5), Vec4(0.4, 0.5, 0.6, 0.5), Vec4(0.7, 0.7, 0.8, 0.75)],ItemGlobals.MotionBlurFine: [Vec4(0.6, 0.6, 0.75, 1), Vec4(0.6, 0.5, 0.2, 1), Vec4(0.6, 0.6, 0.4, 1)],ItemGlobals.MotionBlurPirate: [Vec4(1, 0.2, 0.2, 0.5), Vec4(0.5, 0.5, 0.5, 0.75), Vec4(0.7, 0.7, 0.9, 1)],ItemGlobals.MotionBlurDark: [Vec4(1, 1, 0, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.1, 0.1, 0.1, 1.0)],ItemGlobals.MotionBlurGreen: [Vec4(0.5, 1, 0.1, 1.0), Vec4(0.2, 1, 0.2, 1.0), Vec4(0.3, 1, 0.4, 1.0)],ItemGlobals.MotionBlurRed: [Vec4(1, 0.5, 0.2, 1.0), Vec4(1, 0.3, 0.3, 1.0), Vec4(1, 0.1, 0.1, 1.0)]}
    walkAnim = 'walk'
    runAnim = 'run_with_weapon'
    neutralAnim = 'sword_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'boxing_hit_head_right'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'sword')
        self.flame = None
        self.frost = None
        self.thunder = None
        self.colorIval = None
        return

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def delete(self):
        taskMgr.remove('stopSpecialEffectTask')
        self.endAttack(None)
        self.removeTrail()
        self.stopFlame()
        self.stopFrost()
        self.stopThunder()
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

    def startFlame(self, cursed=0):
        if not self.flame:
            self.flame = SwordFlame.getEffect()
        if self.flame:
            self.flame.reparentTo(self)
            self.flame.setPos(0.25, 1.75, 0)
            self.flame.setHpr(90, -90, 0)
            self.flame.startLoop()
            if cursed:
                self.flame.setCursedColor()
        if not self.colorIval:
            if cursed:
                self.colorIval = Sequence(self.colorScaleInterval(0.3, Vec4(0.4, 1, 0.35, 1), startColorScale=Vec4(0.7, 1, 0.6, 1)), self.colorScaleInterval(0.3, Vec4(0.7, 1, 0.6, 1)))
                self.colorIval.loop()
            else:
                self.colorIval = Sequence(self.colorScaleInterval(0.3, Vec4(1, 0.7, 0.4, 1), startColorScale=Vec4(1, 0.8, 0.6, 1)), self.colorScaleInterval(0.3, Vec4(1, 0.8, 0.6, 1)))
                self.colorIval.loop()

    def stopFlame(self):
        if self.flame:
            self.flame.stopLoop()
            self.flame = None
        if self.colorIval:
            self.colorIval.pause()
            self.colorIval = None
            self.clearColorScale()
        return

    def setFlameIntensity(self, value):
        if value > 0.0:
            if not self.flame:
                self.startFlame()
                self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
                self.setBin('fixed', 0)
            if self.flame:
                newScale = 0.6 + value
                scaleDiff = abs(self.flame.effectScale - newScale)
                if scaleDiff > 0.1:
                    self.flame.setEffectScale(0.6 + value)
        else:
            self.stopFlame()
            self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))
        self.setColor(1, 1 - value, 1 - value, 1)

    def startFrost(self):
        if not self.frost:
            self.frost = SwordFreeze.getEffect()
        if self.frost:
            self.frost.reparentTo(self)
            self.frost.setPos(0.25, 1.75, 0)
            self.frost.setHpr(90, -90, 0)
            self.frost.startLoop()
        if not self.colorIval:
            self.colorIval = Sequence(self.colorScaleInterval(0.3, Vec4(0.55, 0.6, 1, 1), startColorScale=Vec4(0.8, 0.9, 1, 1)), self.colorScaleInterval(0.3, Vec4(0.8, 0.9, 1, 1)))
            self.colorIval.loop()

    def stopFrost(self):
        if self.frost:
            self.frost.stopLoop()
            self.frost = None
        if self.colorIval:
            self.colorIval.pause()
            self.colorIval = None
            self.clearColorScale()
        return

    def startThunder(self):
        if not self.thunder:
            self.thunder = SwordThunders.getEffect()
        if self.thunder:
            self.thunder.reparentTo(self)
            self.thunder.setColorScale(0.9, 1, 0.6, 1)
            self.thunder.setPos(0, 1.6, 0)
            self.thunder.startLoop()

    def stopThunder(self):
        if self.thunder:
            self.thunder.stopLoop()
            self.thunder = None
        return

    def startSpecialEffect(self, skillId=None):
        if skillId == EnemySkills.CUTLASS_CURSED_FIRE or skillId == EnemySkills.CUTLASS_FIRE_BREAK:
            self.startFlame(cursed=1)
        elif skillId == EnemySkills.CUTLASS_CURSED_ICE or skillId == EnemySkills.CUTLASS_ICE_BREAK:
            self.startFrost()
        elif skillId == EnemySkills.CUTLASS_CURSED_THUNDER or skillId == EnemySkills.CUTLASS_THUNDER_BREAK:
            self.startThunder()
        taskMgr.doMethodLater(1.0, self.stopSpecialEffect, 'stopSpecialEffectTask', [skillId])

    def stopSpecialEffect(self, skillId=None):
        if skillId == EnemySkills.CUTLASS_CURSED_FIRE or skillId == EnemySkills.CUTLASS_FIRE_BREAK:
            self.stopFlame()
        if skillId == EnemySkills.CUTLASS_CURSED_ICE or skillId == EnemySkills.CUTLASS_ICE_BREAK:
            self.stopFrost()
        if skillId == EnemySkills.CUTLASS_CURSED_THUNDER or skillId == EnemySkills.CUTLASS_THUNDER_BREAK:
            self.stopThunder()

    @classmethod
    def setupSounds(cls):
        Sword.hitSfxs = {ItemGlobals.CUTLASS: (loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CLASHCLANG), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_01), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_02), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_03)),ItemGlobals.SABRE: (loadSfx(SoundGlobals.SFX_WEAPON_SABRE_CLASHCLANG), loadSfx(SoundGlobals.SFX_WEAPON_SABRE_SWIPECLANG_01), loadSfx(SoundGlobals.SFX_WEAPON_SABRE_SWIPECLANG_02), loadSfx(SoundGlobals.SFX_WEAPON_SABRE_SWIPECLANG_03)),ItemGlobals.BROADSWORD: (loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_CLASHCLANG), loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_SWIPECLANG_01), loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_SWIPECLANG_02), loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_SWIPECLANG_03)),ItemGlobals.SCIMITAR: (loadSfx(SoundGlobals.SFX_WEAPON_SCIMITAR_CLASHCLANG), loadSfx(SoundGlobals.SFX_WEAPON_SCIMITAR_SWIPECLANG_01), loadSfx(SoundGlobals.SFX_WEAPON_SCIMITAR_SWIPECLANG_02), loadSfx(SoundGlobals.SFX_WEAPON_SCIMITAR_SWIPECLANG_03)),ItemGlobals.CURSED_CUTLASS: (loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CLASHCLANG), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_01), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_02), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_03)),ItemGlobals.CURSED_SABRE: (loadSfx(SoundGlobals.SFX_WEAPON_SABRE_CLASHCLANG), loadSfx(SoundGlobals.SFX_WEAPON_SABRE_SWIPECLANG_01), loadSfx(SoundGlobals.SFX_WEAPON_SABRE_SWIPECLANG_02), loadSfx(SoundGlobals.SFX_WEAPON_SABRE_SWIPECLANG_03)),ItemGlobals.CURSED_BROADSWORD: (loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_CLASHCLANG), loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_SWIPECLANG_01), loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_SWIPECLANG_02), loadSfx(SoundGlobals.SFX_WEAPON_BROADSWORD_SWIPECLANG_03))}
        Sword.missSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWOOSH_01), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWOOSH_02))
        Sword.mistimedHitSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_MISTIMEDHIT),)
        Sword.skillSfxs = {InventoryType.CutlassHack: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),InventoryType.CutlassSlash: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SLASH),InventoryType.CutlassStab: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_STAB),InventoryType.CutlassFlourish: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_FLOURISH),InventoryType.CutlassCleave: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CLEAVE),InventoryType.CutlassTaunt: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_TAUNT),InventoryType.CutlassBrawl: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_BRAWL),InventoryType.CutlassSweep: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWEEP),InventoryType.CutlassBladestorm: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_BLADESTORM),EnemySkills.CUTLASS_BLOWBACK: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_BLOWBACK),EnemySkills.CUTLASS_CAPTAINS_FURY: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CAPTAINS_FURY),EnemySkills.CUTLASS_CURSED_FIRE: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CURSED_FIRE),EnemySkills.CUTLASS_CURSED_THUNDER: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CURSED_THUNDER),EnemySkills.CUTLASS_CURSED_ICE: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CURSED_ICE),EnemySkills.CUTLASS_FIRE_BREAK: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CURSED_FIRE),EnemySkills.CUTLASS_THUNDER_BREAK: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CURSED_THUNDER),EnemySkills.CUTLASS_ICE_BREAK: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CURSED_ICE),EnemySkills.MISC_CAPTAINS_RESOLVE: loadSfx(SoundGlobals.SFX_WEAPON_SKILL_CAPTAINS_RESOLVE)}
        Sword.drawSfx = loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_DRAW)
        Sword.returnSfx = loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SHEATHE)
        Sword.fireHitSfx = loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_FIRE_HIT)
        Sword.thunderHitSfx = loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_THUNDER_HIT)
        Sword.iceHitSfx = loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_ICE_HIT)


def getHitSfx():
    return Sword.hitSfxs


def getMistimedHitSfx():
    return Sword.mistimedHitSfxs


def getMissSfx():
    return Sword.missSfxs


def getFireHitSfx():
    return Sword.fireHitSfx


def getThunderHitSfx():
    return Sword.thunderHitSfx


def getIceHitSfx():
    return Sword.iceHitSfx