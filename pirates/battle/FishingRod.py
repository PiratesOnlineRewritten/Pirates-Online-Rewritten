import Weapon
import WeaponGlobals
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PLocalizer
from pirates.effects import PolyTrail
import random

class FishingRod(Weapon.Weapon):
    modelTypes = [
     'models/handheld/pir_m_hnd_tol_fishingPole', 'models/handheld/pir_m_hnd_tol_fishingPoleMed', 'models/handheld/pir_m_hnd_tol_fishingPoleLarge']
    models = {}
    icons = {}
    vertex_list = [
     Vec4(0.0, 0.4, 0.0, 1.0), Vec4(0.0, 2.0, 0.0, 1.0), Vec4(-0.55, 2.95, 0.0, 1.0)]
    motion_color = {InventoryType.CutlassWeaponL1: [Vec4(0.3, 0.4, 0.1, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.6, 0.6, 0.6, 0.5)],InventoryType.CutlassWeaponL2: [Vec4(0.1, 0.2, 0.4, 0.5), Vec4(0.4, 0.5, 0.7, 0.5), Vec4(0.5, 0.5, 0.9, 0.75)],InventoryType.CutlassWeaponL3: [Vec4(1, 1, 0.4, 0.5), Vec4(0.4, 0.5, 0.6, 0.5), Vec4(0.7, 0.7, 0.8, 0.75)],InventoryType.CutlassWeaponL4: [Vec4(0.6, 0.6, 0.75, 1), Vec4(0.6, 0.5, 0.2, 1), Vec4(0.6, 0.6, 0.4, 1)],InventoryType.CutlassWeaponL5: [Vec4(1, 0.2, 0.2, 0.5), Vec4(0.5, 0.5, 0.5, 0.75), Vec4(0.7, 0.7, 0.9, 1)],InventoryType.CutlassWeaponL6: [Vec4(1, 1, 0, 0.5), Vec4(0.3, 0.3, 0.3, 1), Vec4(0.1, 0.1, 0.1, 1)]}

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'fishingRod')

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def delete(self):
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
            self.motion_trail = PolyTrail.PolyTrail(target, self.vertex_list, self.motion_color.get(self.itemId))
            self.motion_trail.reparentTo(self)
            self.motion_trail.setUseNurbs(1)
            card = loader.loadModel('models/effects/swordtrail_effects')
            tex = card.find('**/swordtrail_lines').findTexture('*')
            self.motion_trail.setTexture(tex)
            self.motion_trail.setBlendModeOn()
            if self.itemId == InventoryType.CutlassWeaponL6:
                self.motion_trail.setBlendModeOff()
            card.removeNode()

    def removeTrail(self):
        if self.motion_trail:
            self.motion_trail.destroy()
            self.motion_trail = None
        return

    def getBlurColor(self):
        return self.motion_color.get(self.itemId)[2]

    def beginAttack(self, av):
        Weapon.Weapon.beginAttack(self, av)

    @classmethod
    def setupSounds(cls):
        FishingRod.hitSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_CLASHCLANG), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_01), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_02), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWIPECLANG_03))
        FishingRod.missSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWOOSH_01), loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SWOOSH_02))
        FishingRod.skillSfxs = {InventoryType.FishingRodStall: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),InventoryType.FishingRodPull: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),InventoryType.FishingRodHeal: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),InventoryType.FishingRodTug: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),InventoryType.FishingRodSink: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_HACK),InventoryType.FishingRodOceanEye: loadSfx(SoundGlobals.SFX_WEAPON_CUTLASS_SLASH)}
        FishingRod.drawSfx = loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_REEL_END)
        FishingRod.returnSfx = loadSfx(SoundGlobals.SFX_MINIGAME_FISHING_ROD_OUT)


def getHitSfx():
    return FishingRod.hitSfxs


def getMissSfx():
    return FishingRod.missSfxs