from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals

class DistributedWelcomeWorldAI(DistributedInstanceWorldAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWelcomeWorldAI')

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)

        self.type = PiratesGlobals.INSTANCE_WELCOME