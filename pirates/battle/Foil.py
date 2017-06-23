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

class Foil(Weapon.Weapon):
    modelTypes = [
     'models/handheld/pir_m_hnd_swd_epee_a']
    models = {}
    icons = {}
    vertex_list = [
     Vec4(0.0, 0.4, 0.0, 1.0), Vec4(0.0, 2.0, 0.0, 1.0), Vec4(-0.55, 2.95, 0.0, 1.0)]
    motion_color = {ItemGlobals.MotionBlurDefault: [Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.3, 0.3, 0.3, 0.5), Vec4(0.6, 0.6, 0.6, 0.5)]}
    walkAnim = 'sword_advance'
    runAnim = 'sword_advance'
    neutralAnim = 'foil_idle'
    strafeLeftAnim = 'strafe_left'
    strafeRightAnim = 'strafe_right'
    painAnim = 'boxing_hit_head_right'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'foil')

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def delete(self):
        self.endAttack(None)
        self.removeTrail()
        Weapon.Weapon.delete(self)
        return

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(Func(base.playSfx, self.drawSfx, node=av), av.actorInterval('sword_draw', playRate=1.5, endFrame=15, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.187), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(Func(base.playSfx, self.returnSfx, node=av), av.actorInterval('sword_putaway', playRate=2, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.detachFrom, av)))
        return track

    def attachTo(self, av):
        Weapon.Weapon.attachTo(self, av)
        self.createTrail(av)

    def detachFrom(self, av):
        Weapon.Weapon.detachFrom(self, av)
        self.removeTrail()

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
        Foil.hitSfxs = (loadSfx(SoundGlobals.SFX_WEAPON_FOIL_HIT_01), loadSfx(SoundGlobals.SFX_WEAPON_FOIL_HIT_02), loadSfx(SoundGlobals.SFX_WEAPON_FOIL_HIT_03), loadSfx(SoundGlobals.SFX_WEAPON_FOIL_HIT_04))
        Foil.mistimedHitSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_FOIL_HIT_01), loadSfx(SoundGlobals.SFX_WEAPON_FOIL_HIT_02), loadSfx(SoundGlobals.SFX_WEAPON_FOIL_HIT_03), loadSfx(SoundGlobals.SFX_WEAPON_FOIL_HIT_04))
        Foil.missSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_FOIL_MISS_01), loadSfx(SoundGlobals.SFX_WEAPON_FOIL_MISS_02))
        Foil.drawSfx = loadSfx(SoundGlobals.SFX_WEAPON_FOIL_DRAW)
        Foil.returnSfx = loadSfx(SoundGlobals.SFX_WEAPON_FOIL_SHEATHE)


def getHitSfx():
    return Foil.hitSfxs


def getMistimedHitSfx():
    return Foil.mistimedHitSfxs


def getMissSfx():
    return Foil.missSfxs