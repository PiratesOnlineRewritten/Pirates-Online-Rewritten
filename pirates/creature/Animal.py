from pirates.creature.Creature import Creature

class Animal(Creature):

    def __init__(self, animationMixer=None):
        Creature.__init__(self, animationMixer)

    @report(types=['module', 'args'], dConfigParam='nametag')
    def initializeNametag3d(self):
        pass

    def initializeNametag3dPet(self):
        Creature.initializeNametag3d(self)