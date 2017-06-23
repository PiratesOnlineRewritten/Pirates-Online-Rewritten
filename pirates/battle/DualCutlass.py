import Weapon
import WeaponGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.inventory import ItemGlobals
from pirates.piratesbase import PLocalizer
from pirates.effects import PolyTrail
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.uberdog.UberDogGlobals import InventoryType
import random

class DualCutlass(Weapon.Weapon):
    modelTypes = [
     'models/handheld/pir_m_hnd_swd_cutlass_a']
    models = {}
    icons = {}
    vertex_list = [
     Vec4(0.0, 0.4, 0.0, 1.0), Vec4(0.0, 2.0, 0.0, 1.0), Vec4(-0.55, 2.95, 0.0, 1.0)]
    motion_color = {ItemGlobals.MotionBlurDefault: [Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.6, 0.6, 0.6, 0.5)],ItemGlobals.MotionBlurRusty: [Vec4(0.3, 0.4, 0.1, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.6, 0.6, 0.6, 0.5)],ItemGlobals.MotionBlurIron: [Vec4(0.1, 0.2, 0.4, 0.5), Vec4(0.4, 0.5, 0.7, 0.5), Vec4(0.5, 0.5, 0.9, 0.75)],ItemGlobals.MotionBlurSteel: [Vec4(1, 1, 0.4, 0.5), Vec4(0.4, 0.5, 0.6, 0.5), Vec4(0.7, 0.7, 0.8, 0.75)],ItemGlobals.MotionBlurFine: [Vec4(0.6, 0.6, 0.75, 1), Vec4(0.6, 0.5, 0.2, 1), Vec4(0.6, 0.6, 0.4, 1)],ItemGlobals.MotionBlurPirate: [Vec4(1, 0.2, 0.2, 0.5), Vec4(0.5, 0.5, 0.5, 0.75), Vec4(0.7, 0.7, 0.9, 1)],ItemGlobals.MotionBlurDark: [Vec4(1, 1, 0, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.1, 0.1, 0.1, 1.0)]}
    walkAnim = 'dualcutlass_walk'
    runAnim = 'dualcutlass_walk'
    neutralAnim = 'dualcutlass_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'dualcutlass_hurt'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'dualcutlass')
        self.leftHandWeaponNP = None
        return

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def delete(self):
        self.endAttack(None)
        self.removeTrail()
        Weapon.Weapon.delete(self)
        if self.leftHandWeaponNP:
            self.leftHandWeaponNP.removeNode()
            self.leftHandWeaponNP = None
        return

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(Func(base.playSfx, self.drawSfx, node=av), av.actorInterval('dualcutlass_draw', playRate=1, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.187), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(Func(base.playSfx, self.returnSfx, node=av), av.actorInterval('sword_putaway', playRate=2, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.detachFrom, av)))
        return track

    def attachTo(self, av):
        Weapon.Weapon.attachTo(self, av)
        if not self.isEmpty():
            if av.leftHandNode:
                self.leftHandWeaponNP = self.instanceTo(av.leftHandNode)
        self.createTrail(av)

    def detachFrom(self, av):
        Weapon.Weapon.detachFrom(self, av)
        if self.leftHandWeaponNP:
            self.leftHandWeaponNP.detachNode()
            self.leftHandWeaponNP = None
        self.removeTrail()
        return

    def createTrail(self, target):
        if self.isEmpty():
            return
        if not self.motion_trail:
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

    def hideSpinBlur(self):
        if self.spinBlur:
            if not self.spinBlur.isEmpty():
                self.spinBlur.hide()

    def showSpinBlur(self):
        if self.spinBlur:
            if not self.spinBlur.isEmpty():
                self.spinBlur.setColorScale(self.getBlurColor() / 2.0)
                self.spinBlur.show()

    def getBlurColor(self):
        return self.motion_color.get(self.itemId)[2]

    def beginAttack(self, av, wantTrail=1):
        self.hideSpinBlur()
        Weapon.Weapon.beginAttack(self, av, wantTrail)

    @classmethod
    def setupSounds(cls):
        DualCutlass.hitSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_HIT_01), loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_HIT_02), loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_HIT_03), loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_HIT_04))
        DualCutlass.mistimedHitSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_HIT_01), loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_HIT_02), loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_HIT_03), loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_HIT_04))
        DualCutlass.missSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_MISS_01), loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_MISS_02))
        DualCutlass.drawSfx = loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_DRAW)
        DualCutlass.returnSfx = loadSfx(SoundGlobals.SFX_WEAPON_DUALCUTLASS_SHEATHE)


def getHitSfx():
    return DualCutlass.hitSfxs


def getMistimedHitSfx():
    return DualCutlass.mistimedHitSfxs


def getMissSfx():
    return DualCutlass.missSfxs