from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Animal import Animal

class Seagull(Animal):
    ModelInfo = ('models/char/seagull_hi', 'models/char/seagull_')
    SfxNames = dict(Animal.SfxNames)
    SfxNames.update({})
    AnimList = (
     ('idle', 'flying'), ('walk', 'flying'), ('run', 'flying'), ('flying', 'flying'), ('takeoff', 'takeoff'), ('landing', 'landing'), ('groom_idle', 'groom_idle'))

    class AnimationMixer(Animal.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('SeagullAnimationMixer')
        LOOP = Animal.AnimationMixer.LOOP
        ACTION = Animal.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],),'walk': (LOOP['LOOP'],),'run': (LOOP['LOOP'],),'takeoff': (ACTION['ACTION'],),'landing': (ACTION['ACTION'],),'flying': (LOOP['LOOP'],),'groom_idle': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('groom_idle', 1.0), ('run', 1.0), ('run', 1.0), ('fly', 1.0), ('fly', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('groom_idle', 1.0), ('run', 1.0), ('run', 1.0), ('fly', 1.0), ('fly', 1.0)))

    def __init__(self):
        Animal.__init__(self)
        if not Seagull.sfx:
            for name in Seagull.SfxNames:
                Seagull.sfx[name] = loadSfx(Seagull.SfxNames[name])

        self.generateCreature()