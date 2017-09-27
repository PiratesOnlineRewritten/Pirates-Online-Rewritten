from pirates.instance.DistributedInstanceWorldAI import DistributedInstanceWorldAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase import PiratesGlobals
from pirates.pirate.DistributedPlayerPirateAI import DistributedPlayerPirateAI

class DistributedTeleportZoneAI(DistributedInstanceWorldAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTeleportZoneAI')

    def __init__(self, air):
        DistributedInstanceWorldAI.__init__(self, air)

        self.type = PiratesGlobals.INSTANCE_NONE
