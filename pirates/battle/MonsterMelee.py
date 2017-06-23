import types
from direct.interval.IntervalGlobal import *
from pirates.battle import Weapon
from pirates.battle.WeaponGlobals import *
from pirates.effects import PolyTrail
from pirates.pirate import AvatarTypes
from pirates.audio import SoundGlobals
_sfxDict = {}

def cacheSfx(name, file):
    sfx = _sfxDict.get(name)
    if not sfx:
        if type(file) == types.TupleType:
            sfx = map(loader.loadSfx, file)
        else:
            sfx = loader.loadSfx(file)
        _sfxDict[name] = sfx
    return sfx


def getHitSfx():
    return cacheSfx('hit', 'audio/' + SoundGlobals.SFX_MONSTER_HIT)


def getMistimedHitSfx():
    return cacheSfx('hit', 'audio/' + SoundGlobals.SFX_MONSTER_HIT)


def getMissSfx():
    return cacheSfx('miss', 'audio/' + SoundGlobals.SFX_MONSTER_MISS)


def getEnsnareSfx():
    return cacheSfx('ensnare', 'audio/' + SoundGlobals.SFX_MONSTER_ENSNARE)


def getSmashSfx():
    return cacheSfx('smash', ('audio/' + SoundGlobals.SFX_MONSTER_SMASH_01, 'audio/' + SoundGlobals.SFX_MONSTER_SMASH_02, 'audio/' + SoundGlobals.SFX_MONSTER_SMASH_03))


def getWaspStingSfx():
    return cacheSfx('waspSting', 'audio/' + SoundGlobals.SFX_MONSTER_WASP_STING)


def getWaspLeapStingSfx():
    return cacheSfx('waspLeapSting', 'audio/' + SoundGlobals.SFX_MONSTER_WASP_LEAP_STING)


def getBatAttackSfx():
    return cacheSfx('batAttack', 'audio/' + SoundGlobals.SFX_MONSTER_BAT_ATTACK)


def getAlligatorAttackLeftSfx():
    return cacheSfx('alligatorAttackLeft', 'audio/' + SoundGlobals.SFX_MONSTER_ALLIGATOR_ATTACK_LEFT)


def getAlligatorAttackStraightSfx():
    return cacheSfx('alligatorAttackStraight', 'audio/' + SoundGlobals.SFX_MONSTER_ALLIGATOR_ATTACK_STRAIGHT)


def getScorpionAttackLeftSfx():
    return cacheSfx('scorpionAttackLeft', 'audio/' + SoundGlobals.SFX_MONSTER_SCORPION_ATTACK_LEFT)


def getScorpionAttackBothSfx():
    return cacheSfx('scorpionAttackBoth', 'audio/' + SoundGlobals.SFX_MONSTER_SCORPION_ATTACK_BOTH)


def getScorpionAttackTailStingSfx():
    return cacheSfx('scorpionAttackTailSting', 'audio/' + SoundGlobals.SFX_MONSTER_SCORPION_ATTACK_TAIL)


def getScorpionPickUpHumanSfx():
    return cacheSfx('scorpionPickUpHuman', 'audio/' + SoundGlobals.SFX_MONSTER_SCORPION_PICKUP)


def getScorpionRearUpSfx():
    return cacheSfx('scorpionRearUp', 'audio/' + SoundGlobals.SFX_MONSTER_SCORPION_REARUP)


def getCrabAttackLeftSfx():
    return cacheSfx('crabAttackLeft', 'audio/' + SoundGlobals.SFX_MONSTER_CRAB_ATTACK_LEFT)


def getCrabAttackBothSfx():
    return cacheSfx('crabAttackBoth', 'audio/' + SoundGlobals.SFX_MONSTER_CRAB_ATTACK_BOTH)


def getFlytrapAttackASfx():
    return cacheSfx('flytrapAttackA', 'audio/' + SoundGlobals.SFX_MONSTER_FLYTRAP_ATTACK)


def getFlytrapAttackJabSfx():
    return cacheSfx('flytrapAttackJab', 'audio/' + SoundGlobals.SFX_MONSTER_FLYTRAP_JAB)


def getFlytrapAttackFakeSfx():
    return cacheSfx('flytrapAttackFake', 'audio/' + SoundGlobals.SFX_MONSTER_FLYTRAP_FAKE)


def getFlytrapAttackSpitSfx():
    return cacheSfx('flytrapAttackSpit', 'audio/' + SoundGlobals.SFX_MONSTER_FLYTRAP_SPIT)


def getMossmanAttackKickSfx():
    return cacheSfx('mossmanAttackKick', 'audio/' + SoundGlobals.SFX_MONSTER_MOSSMAN_ATTACK_KICK)


def getMossmanAttackSlapSfx():
    return cacheSfx('mossmanAttackSlap', 'audio/' + SoundGlobals.SFX_MONSTER_MOSSMAN_ATTACK_SLAP)


def getMossmanAttackSwatSfx():
    return cacheSfx('mossmanAttackSwat', 'audio/' + SoundGlobals.SFX_MONSTER_MOSSMAN_ATTACK_SWAT)


def getMossmanAttackJumpSfx():
    return cacheSfx('mossmanAttackJump', 'audio/' + SoundGlobals.SFX_MONSTER_MOSSMAN_JUMP)


def getRageGhostAttackSfx():
    return cacheSfx('rageSound', 'audio/' + SoundGlobals.SFX_RAGE_KILL)


class MonsterMelee(Weapon.Weapon):
    vertex_list = [
     Vec4(0.0, 0.4, 0.0, 1.0), Vec4(0.0, 2.0, 0.0, 1.0), Vec4(-0.55, 2.95, 0.0, 1.0)]
    motion_color = [
     Vec4(0.1, 0.2, 0.4, 0.5), Vec4(0.25, 0.5, 1.0, 0.5), Vec4(0.5, 0.5, 0.6, 0.5)]

    def __init__(self, itemId):
        Weapon.Weapon.__init__(self, itemId, 'monsterMelee')
        self.neutralAnim = 'idle'
        self.walkAnim = 'walk'
        self.strafeAnim = 'walk'
        self.painAnim = 'pain'

    def attachTo(self, av):
        pass

    def detachFrom(self, av):
        pass

    def delete(self):
        self.endAttack(None)
        self.removeTrail()
        Weapon.Weapon.delete(self)
        return

    def changeStance(self, av):
        if av.avatarType.isA(AvatarTypes.Wasp) or av.avatarType.isA(AvatarTypes.AngryWasp) or av.avatarType.isA(AvatarTypes.SoldierWasp):
            self.walkAnim = 'idle_flying'
            self.neutralAnim = 'idle_flying'
        av.setWalkForWeapon()

    def getDrawIval(self, av, ammoSkillId=0, blendInT=0.1, blendOutT=0):
        if av.avatarType.isA(AvatarTypes.Bat) or av.avatarType.isA(AvatarTypes.RabidBat) or av.avatarType.isA(AvatarTypes.FireBat) or av.avatarType.isA(AvatarTypes.VampireBat):
            av.show()
            track = Parallel(Func(self.attachTo, av), Func(self.changeStance, av), av.actorInterval('spawn', playRate=1.0))
        else:
            track = Parallel(Func(self.attachTo, av), Func(self.changeStance, av))
        return track

    def getReturnIval(self, av, blendInT=0, blendOutT=0.1):

        def hideEnemy():
            av.hide()

        if av.avatarType.isA(AvatarTypes.Bat) or av.avatarType.isA(AvatarTypes.RabidBat) or av.avatarType.isA(AvatarTypes.FireBat) or av.avatarType.isA(AvatarTypes.VampireBat):
            track = Parallel(Func(self.detachFrom, av), Func(self.changeStance, av), av.actorInterval('spawn', playRate=1.0, startFrame=100, endFrame=20), Func(hideEnemy))
        else:
            track = Parallel(Func(self.detachFrom, av), Func(self.changeStance, av))
        return track

    def createTrail(self, target):
        if not self.motion_trail:
            self.motion_trail = PolyTrail.PolyTrail(target, self.vertex_list, self.motion_color)
            self.motion_trail.reparentTo(self)
            self.motion_trail.setUseNurbs(1)
            card = loader.loadModel('models/effects/swordtrail_effects')
            tex = card.find('**/swordtrail_lines').findTexture('*')
            self.motion_trail.setTexture(tex)
            card.removeNode()

    def removeTrail(self):
        if self.motion_trail:
            self.motion_trail.destroy()
            self.motion_trail = None
        return