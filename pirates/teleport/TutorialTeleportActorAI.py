from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class TutorialTeleportActorAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('TutorialTeleportActorAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)