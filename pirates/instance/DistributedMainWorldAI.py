from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals

class DistributedMainWorldAI(DistributedInstanceWorldAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedMainWorldAI')

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)

        self.type = PiratesGlobals.INSTANCE_MAIN
