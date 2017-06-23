from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class Alligator(Creature):
    ModelInfo = ('models/char/alligator_hi', 'models/char/alligator_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'death': SoundGlobals.SFX_MONSTER_ALLIGATOR_DEATH,'pain': SoundGlobals.SFX_MONSTER_ALLIGATOR_PAIN})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('walk', 'walk'), ('run', 'run'), ('swim', 'swim'), ('swim_alt', 'swim_alt'), ('pull_back', 'pull_back'), ('pain', 'pull_back'), ('attack_left', 'attack_left'), ('attack_right', 'attack_right'), ('attack_straight', 'attack_straight'), ('flinch_left', 'flinch_left'), ('flinch_right', 'flinch_right'), ('death', 'death'))

    class AnimationMixer(Creature.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('AlligatorAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],),'walk': (LOOP['LOOP'],),'run': (LOOP['LOOP'],),'swim': (LOOP['LOOP'],),'swim_alt': (LOOP['LOOP'],),'attack_left': (ACTION['ACTION'],),'attack_right': (ACTION['ACTION'],),'attack_straight': (ACTION['ACTION'],),'pickup_human': (ACTION['ACTION'],),'flinch_left': (ACTION['ACTION'],),'flinch_right': (ACTION['ACTION'],),'pull_back': (ACTION['ACTION'],),'pain': (ACTION['ACTION'],),'death': (ACTION['MOVIE'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('swim', 1.0), ('swim', 1.0), ('swim_alt', 1.0), ('swim', -1.0), ('swim_alt', 1.0), ('swim_alt', 1.0), ('swim_alt', 1.0), ('swim_alt', 1.0), ('swim_alt', 1.0), ('swim', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        self.texCard = loader.loadModel('models/char/undead_creatures')
        if not Alligator.sfx:
            for name in Alligator.SfxNames:
                Alligator.sfx[name] = loadSfx(Alligator.SfxNames[name])

        self.nametagOffset = 3.8
        self.generateCreature()

    def setupCreature(self):
        DistributedCreature.setupCreature(self)
        self.setToUndead()

    def setToNormal(self):
        if self.texCard:
            tex = self.texCard.findTexture('alligator')
            lodnames = self.getLODNames()
            for lod in lodnames:
                lodptr = self.getLOD(lod)
                lodptr.setTexture(tex, 1)

    def setToUndead(self):
        if self.texCard:
            tex = self.texCard.findTexture('alligator_undead')
            lodnames = self.getLODNames()
            for lod in lodnames:
                lodptr = self.getLOD(lod)
                lodptr.setTexture(tex, 1)