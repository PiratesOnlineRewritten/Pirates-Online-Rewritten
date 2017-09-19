
from pirates.creature.DistributedAnimalAI import DistributedAnimalAI
from direct.directnotify import DirectNotifyGlobal

class DistributedChickenAI(DistributedAnimalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAnimalAI')

    def __init__(self, air):
        DistributedAnimalAI.__init__(self, air)

