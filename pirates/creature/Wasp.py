from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class Wasp(Creature):
    ModelInfo = ('models/char/wasp_hi', 'models/char/wasp_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'death': SoundGlobals.SFX_MONSTER_WASP_DEATH,'pain': SoundGlobals.SFX_MONSTER_WASP_PAIN})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('idle_flying', 'idle_fly'), ('walk', 'walk'), ('drop', 'react_drop'), ('advance', 'attack_advance'), ('sting', 'attack_sting'), ('leap_sting', 'attack_leap_sting'), ('pain', 'react_pull_back'), ('death', 'react_death'))

    class AnimationMixer(Creature.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('WaspAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],),'idle_flying': (LOOP['LOOP'],),'walk': (LOOP['LOOP'],),'advance': (ACTION['ACTION'],),'drop': (ACTION['ACTION'],),'sting': (ACTION['ACTION'],),'leap_sting': (ACTION['ACTION'],),'ouch': (ACTION['ACTION'],),'death': (ACTION['MOVIE'],),'pain': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0), ('idle_flying', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        if not Wasp.sfx:
            for name in Wasp.SfxNames:
                Wasp.sfx[name] = loadSfx(Wasp.SfxNames[name])

        self.nametagOffset = 11.5
        self.generateCreature()