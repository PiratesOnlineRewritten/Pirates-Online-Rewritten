from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Animal import Animal

class Pig(Animal):
    ModelInfo = ('models/char/pig_hi', 'models/char/pig_')
    SfxNames = dict(Animal.SfxNames)
    SfxNames.update({})
    AnimList = (
     ('walk', 'walk'), ('run', 'walk'), ('idle', 'rooting'), ('rooting', 'rooting'))

    class AnimationMixer(Animal.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('PigAnimationMixer')
        LOOP = Animal.AnimationMixer.LOOP
        ACTION = Animal.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],),'run': (LOOP['LOOP'],),'walk': (LOOP['LOOP'],),'rooting': (LOOP['LOOP'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Animal.__init__(self)
        self.generateCreature()