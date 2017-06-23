from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class Bat(Creature):
    ModelInfo = ('models/char/bat_hi', 'models/char/bat_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'attack_left': SoundGlobals.SFX_MONSTER_BAT_ATTACK,'death': SoundGlobals.SFX_MONSTER_BAT_DEATH,'pain': SoundGlobals.SFX_MONSTER_BAT_PAIN})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('idle_hang', 'idle_hang'), ('glide', 'glide'), ('wounded_flight', 'wounded_flight'), ('takeoff', 'takeoff'), ('land', 'land'), ('attack_forward', 'attack_forward'), ('attack_right', 'attack_right'), ('sudden_gust', 'sudden_gust'), ('sudden_gust_alt', 'sudden_gust_alt'), ('pain', 'pain_left'), ('pain_right', 'pain_right'), ('death', 'death'), ('intro', 'spawn'))

    class AnimationMixer(Creature.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('BatAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],),'idle_hang': (LOOP['LOOP'],),'glide': (LOOP['LOOP'],),'wounded_flight': (LOOP['LOOP'],),'takeoff': (ACTION['ACTION'],),'land': (ACTION['ACTION'],),'attack_forward': (ACTION['ACTION'],),'attack_right': (ACTION['ACTION'],),'pain': (ACTION['ACTION'],),'pain_right': (ACTION['ACTION'],),'sudden_gust': (ACTION['ACTION'],),'sudden_gust_alt': (ACTION['ACTION'],),'death': (ACTION['MOVIE'],),'intro': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 2.0), ('idle', 2.0), ('glide', 1.0), ('idle', 2.0), ('idle', 2.0), ('idle', 2.0), ('idle', 2.0), ('idle', 2.0), ('idle', 2.0), ('glide', 1.0), ('idle', 2.0), ('idle', 2.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 2.0), ('idle', 2.0), ('glide', 1.0), ('idle', 2.0), ('idle', 2.0), ('idle', 2.0), ('idle', 2.0), ('idle', 2.0), ('idle', 2.0), ('glide', 1.0), ('idle', 2.0), ('idle', 2.0)))

    def __init__(self):
        Creature.__init__(self)
        if not Bat.sfx:
            for name in Bat.SfxNames:
                Bat.sfx[name] = loadSfx(Bat.SfxNames[name])

        self.nametagOffset = 1.2
        self.generateCreature()