from pandac.PandaModules import *
from pirates.creature.SeaMonster import SeaMonster
from pirates.pirate import AvatarTypes
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class SeaSerpent(SeaMonster):
    ModelInfo = ('models/char/serpent_hi', 'models/char/serpent_')
    SfxNames = dict(SeaMonster.SfxNames)
    SfxNames.update({'death': SoundGlobals.SFX_MONSTER_SERPENT_DEATH,'pain': SoundGlobals.SFX_MONSTER_SERPENT_PAIN})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('swim', 'swim'), ('walk', 'swim'), ('submerge', 'submerge'), ('attack', 'attack'), ('emerge', 'emerge'), ('death', 'submerge'))

    class AnimationMixer(SeaMonster.AnimationMixer):
        LOOP = SeaMonster.AnimationMixer.LOOP
        ACTION = SeaMonster.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],),'swim': (LOOP['LOOP'],),'walk': (LOOP['LOOP'],),'submerge': (ACTION['ACTION'],),'attack': (ACTION['ACTION'],),'emerge': (ACTION['ACTION'],),'death': (ACTION['MOVIE'],)}

    def __init__(self):
        SeaMonster.__init__(self)
        self.setAvatarType(AvatarTypes.SeaSerpent)
        if not SeaSerpent.sfx:
            for name in SeaSerpent.SfxNames:
                SeaSerpent.sfx[name] = loadSfx(SeaSerpent.SfxNames[name])

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))