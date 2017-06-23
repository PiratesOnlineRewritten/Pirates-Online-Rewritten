from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Animal import Animal

class Chicken(Animal):
    ModelInfo = ('models/char/chicken_hi', 'models/char/chicken_')
    SfxNames = dict(Animal.SfxNames)
    SfxNames.update({})
    AnimList = (
     ('idle', 'idle'), ('walk', 'walk'), ('run', 'run'), ('scratch', 'scratch'), ('fly', 'fly'))

    class AnimationMixer(Animal.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('ChickenAnimationMixer')
        LOOP = Animal.AnimationMixer.LOOP
        ACTION = Animal.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],),'walk': (LOOP['LOOP'],),'run': (LOOP['LOOP'],),'scratch': (ACTION['ACTION'],),'fly': (LOOP['LOOP'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('fly', 1.0), ('fly', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('fly', 1.0), ('fly', 1.0)))

    def __init__(self):
        Animal.__init__(self)
        if not Chicken.sfx:
            for name in Chicken.SfxNames:
                Chicken.sfx[name] = loadSfx(Chicken.SfxNames[name])

        self.generateCreature()

    def getSplashOverride(self):
        return [
         ('scratch', 1.0)]