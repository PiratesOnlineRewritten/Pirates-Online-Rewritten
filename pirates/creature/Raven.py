from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Animal import Animal

class Raven(Animal):
    ModelInfo = ('models/char/raven_hi', 'models/char/raven_')
    SfxNames = dict(Animal.SfxNames)
    SfxNames.update({})
    AnimList = (
     ('idle', 'glide'), ('walk', 'fly'), ('run', 'glide'), ('flying', 'fly'), ('takeoff', 'idle'), ('landing', 'idle'), ('groom_idle', 'idle'))

    class AnimationMixer(Animal.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('RavenAnimationMixer')
        LOOP = Animal.AnimationMixer.LOOP
        ACTION = Animal.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],),'walk': (LOOP['LOOP'],),'run': (LOOP['LOOP'],),'takeoff': (ACTION['ACTION'],),'landing': (ACTION['ACTION'],),'flying': (LOOP['LOOP'],),'groom_idle': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('groom_idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('groom_idle', 1.0), ('run', 1.0), ('run', 1.0), ('fly', 1.0), ('fly', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('groom_idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('groom_idle', 1.0), ('run', 1.0), ('run', 1.0), ('fly', 1.0), ('fly', 1.0)))

    def __init__(self):
        Animal.__init__(self)
        if not Raven.sfx:
            for name in Raven.SfxNames:
                Raven.sfx[name] = loadSfx(Raven.SfxNames[name])

        self.generateCreature()