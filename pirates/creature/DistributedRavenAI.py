from direct.directnotify import DirectNotifyGlobal
from pirates.creature.DistributedCreatureAI import DistributedCreatureAI

class DistributedRavenAI(DistributedCreatureAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRavenAI')

    def __init__(self, air):
        DistributedCreatureAI.__init__(self, air)