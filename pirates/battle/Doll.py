import random
import Weapon
import WeaponGlobals
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.battle.EnemySkills import *
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals

class Doll(Weapon.Weapon):
    modelTypes = [
     'models/handheld/pir_m_hnd_dol_bane_a', 'models/handheld/pir_m_hnd_dol_bane_b', 'models/handheld/pir_m_hnd_dol_bane_c', 'models/handheld/pir_m_hnd_dol_bane_d', 'models/handheld/pir_m_hnd_dol_bane_e', 'models/handheld/pir_m_hnd_dol_mojo_a', 'models/handheld/pir_m_hnd_dol_mojo_b', 'models/handheld/pir_m_hnd_dol_mojo_c', 'models/handheld/pir_m_hnd_dol_mojo_d', 'models/handheld/pir_m_hnd_dol_mojo_e', 'models/handheld/pir_m_hnd_dol_spirit_a', 'models/handheld/pir_m_hnd_dol_spirit_b', 'models/handheld/pir_m_hnd_dol_spirit_c', 'models/handheld/pir_m_hnd_dol_spirit_d', 'models/handheld/pir_m_hnd_dol_spirit_e']
    effectTypeInfo = {ItemGlobals.DollDefault: (Vec4(1, 1, 1, 1), 'None'),ItemGlobals.DollCloth: (Vec4(0.5, 0.3, 1, 1), 'effectCloth'),ItemGlobals.DollWitch: (Vec4(1, 0.7, 0.7, 1), 'effectWitch'),ItemGlobals.DollPirate: (Vec4(1, 1, 1, 1), 'effectPirate'),ItemGlobals.DollTaboo: (Vec4(1, 1, 1, 1), 'effectTaboo'),ItemGlobals.DollMojo: (Vec4(0.7, 0.5, 1, 1), 'effectMojo')}
    painAnim = 'voodoo_doll_hurt'

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'doll')
        self.effect = None
        self.effectCard = None
        effectId = ItemGlobals.getVfxType1(itemId)
        if not effectId:
            effectId = ItemGlobals.DollDefault
        self.effectColor = self.effectTypeInfo.get(effectId)[0]
        card = loader.loadModel('models/effects/effectCards').find('**/' + self.effectTypeInfo.get(effectId)[1])
        if not card.isEmpty():
            self.effectCard = card
        return

    def loadModel(self):
        self.prop = self.getModel(self.itemId)
        self.prop.reparentTo(self)

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        track = Parallel(Func(base.playSfx, self.drawSfx, node=av, cutoff=60), av.actorInterval('voodoo_draw', playRate=1.5, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.attachTo, av)))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):
        track = Parallel(Func(base.playSfx, self.returnSfx, node=av, cutoff=60), av.actorInterval('sword_putaway', playRate=2, endFrame=35, blendInT=blendInT, blendOutT=blendOutT), Sequence(Wait(0.56), Func(self.detachFrom, av)))
        return track

    def playUnattuneSfx(self, node):
        base.playSfx(self.unattuneSfx, node=node)

    @classmethod
    def setupSounds(cls):
        Doll.hitSfxs = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_HIT)
        Doll.mistimedHitSfxs = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_HIT)
        Doll.missSfxs = (
         loadSfx(SoundGlobals.SFX_WEAPON_DOLL_MISS_01), loadSfx(SoundGlobals.SFX_WEAPON_DOLL_MISS_02))
        Doll.skillSfxs = {EnemySkills.MISC_VOODOO_REFLECT: loadSfx(SoundGlobals.SFX_SKILL_REFLECT_WARD)}
        Doll.attuneSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_ATTUNE)
        Doll.unattuneSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_UNATTUNE)
        Doll.attuneLoopSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_ATTUNE_LOOP)
        Doll.pokeSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_POKE)
        Doll.swarmSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_SWARM)
        Doll.healSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_HEAL)
        Doll.curseSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_CURSE)
        Doll.scorchSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_SCORCH)
        Doll.cureSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_CURE)
        Doll.shacklesSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_SHACKLES)
        Doll.lifedrainSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_LIFE_DRAIN)
        Doll.evileyeSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_EVIL_EYE)
        Doll.monkeyRageSfx = loadSfx(SoundGlobals.SFX_WEAPON_SKILL_MONKEY_RAGE)
        Doll.cleanseSfx = loadSfx(SoundGlobals.SFX_SKILL_CLEANSE)
        Doll.hexWardSfx = loadSfx(SoundGlobals.SFX_SKILL_HEX_WARD)
        Doll.wardLoopSfx = loadSfx(SoundGlobals.SFX_SKILL_WARD_LOOP)
        Doll.drawSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_DRAW)
        Doll.returnSfx = loadSfx(SoundGlobals.SFX_WEAPON_DOLL_SHEATHE)


def getHitSfx():
    return Doll.hitSfxs


def getMissSfx():
    return Doll.missSfxs


def getMistimedHitSfx():
    return Doll.mistimedHitSfxs


def getAttuneSfx():
    return Doll.attuneSfx


def getUnattuneSfx():
    return Doll.unattuneSfx


def getPokeSfx():
    return Doll.pokeSfx


def getSwarmSfx():
    return Doll.swarmSfx


def getHealSfx():
    return Doll.healSfx


def getCurseSfx():
    return Doll.curseSfx


def getScorchSfx():
    return Doll.scorchSfx


def getCureSfx():
    return Doll.cureSfx


def getShacklesSfx():
    return Doll.shacklesSfx


def getLifedrainSfx():
    return Doll.lifedrainSfx


def getEvileyeSfx():
    return Doll.evileyeSfx


def getMonkeyRageSfx():
    return Doll.monkeyRageSfx


def getCleanseSfx():
    return Doll.cleanseSfx


def getHexWardSfx():
    return Doll.hexWardSfx


def getWardLoopSfx():
    return Doll.hexWardLoopSfx