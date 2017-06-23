from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class Scorpion(Creature):
    ModelInfo = ('models/char/scorpion_hi', 'models/char/scorpion_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'death': SoundGlobals.SFX_MONSTER_SCORPION_DEATH,'pain': SoundGlobals.SFX_MONSTER_SCORPION_PAIN})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('walk', 'walk'), ('run', 'run'), ('attack_left', 'attack_left'), ('attack_right', 'attack_right'), ('attack_both', 'attack_both'), ('attack_tail_sting', 'attack_tail_sting'), ('pick_up_human', 'pick_up_human'), ('react_left', 'react_left'), ('react_right', 'react_right'), ('pain', 'knockback'), ('rear_up', 'rear_up'), ('death', 'death'))

    class AnimationMixer(Creature.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('ScorpionAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],),'walk': (LOOP['LOOP'],),'run': (LOOP['LOOP'],),'attack_left': (ACTION['ACTION'],),'attack_right': (ACTION['ACTION'],),'attack_both': (ACTION['ACTION'],),'attack_tail_sting': (ACTION['ACTION'],),'pick_up_human': (ACTION['ACTION'],),'react_left': (ACTION['ACTION'],),'react_right': (ACTION['ACTION'],),'pain': (ACTION['ACTION'],),'rear_up': (ACTION['ACTION'],),'death': (ACTION['MOVIE'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        if not Scorpion.sfx:
            for name in Scorpion.SfxNames:
                Scorpion.sfx[name] = loadSfx(Scorpion.SfxNames[name])

        self.nametagOffset = 12.0
        self.generateCreature()
        self.headNode = self.find('**/def_root')