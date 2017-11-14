
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI
from direct.directnotify import DirectNotifyGlobal

class DistributedSeaSerpentAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSeaSerpentAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)



