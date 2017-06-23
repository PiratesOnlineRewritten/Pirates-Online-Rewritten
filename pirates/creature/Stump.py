from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class Stump(Creature):
    ModelInfo = ('models/char/mossman_hi', 'models/char/mossman_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'death': SoundGlobals.SFX_MONSTER_MOSSMAN_DEATH,'pain': SoundGlobals.SFX_MONSTER_MOSSMAN_PAIN,'spawn': SoundGlobals.SFX_MONSTER_MOSSMAN_SPAWN})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('walk', 'walk'), ('run', 'run'), ('death', 'death'), ('intro', 'intro'), ('jump', 'jump'), ('kick', 'kick'), ('kick_right', 'kick_right'), ('slap_left', 'slap_left'), ('slap_right', 'slap_right'), ('strafe_left', 'strafe_left'), ('strafe_right', 'strafe_right'), ('swat_left', 'swat_left'), ('swat_right', 'swat_right'), ('jump_attack', 'jump_attack'), ('pain', 'pain'))

    class AnimationMixer(Creature.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('StumpAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],),'walk': (LOOP['LOOP'],),'run': (LOOP['LOOP'],),'strafe_left': (LOOP['LOOP'],),'strafe_right': (LOOP['LOOP'],),'death': (ACTION['MOVIE'],),'intro': (ACTION['ACTION'],),'jump': (ACTION['ACTION'],),'kick': (ACTION['ACTION'],),'kick_right': (ACTION['ACTION'],),'slap_left': (ACTION['ACTION'],),'slap_right': (ACTION['ACTION'],),'swat_left': (ACTION['ACTION'],),'swat_right': (ACTION['ACTION'],),'jump_attack': (ACTION['ACTION'],),'pain': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        self.rightHandNode = None
        self.leftHandNode = None
        if not Stump.sfx:
            for name in Stump.SfxNames:
                Stump.sfx[name] = loadSfx(Stump.SfxNames[name])

        self.nametagOffset = 10
        self.generateCreature()
        self.headNode = self.find('**/def_neck')
        return

    def delete(self):
        self.rightHandNode = None
        self.leftHandNode = None
        Creature.delete(self)
        return

    def generateCreature(self):
        Creature.generateCreature(self)
        self.getWeaponJoints()

    def deleteWeaponJoints(self):
        try:
            if self.rightHandNode:
                self.rightHandNode.delete()
        except:
            return

        try:
            if self.leftHandNode:
                self.leftHandNode.delete()
        except:
            return

    def getWeaponJoints(self):
        self.deleteWeaponJoints()
        self.rightHandNode = NodePath('rightHand')
        self.leftHandNode = NodePath('leftHand')
        for lodName in self.getLODNames():
            handLocator = self.find('**/*weapon_right')
            if not handLocator.isEmpty():
                self.rightHandNode.reparentTo(handLocator)
            handLocator = self.find('**/*weapon_left')
            if not handLocator.isEmpty():
                self.leftHandNode.reparentTo(handLocator)

    def adjustNametag3d(self, parentScale=1.0):
        self.nametag3d.setZ(self.scale * parentScale * self.nametagOffset)