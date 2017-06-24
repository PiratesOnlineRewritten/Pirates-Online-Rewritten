from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class PVPGamePirateerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PVPGamePirateerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)