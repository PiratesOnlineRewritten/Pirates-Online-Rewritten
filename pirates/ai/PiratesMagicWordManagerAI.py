from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from otp.ai.MagicWordManagerAI import MagicWordManagerAI

class PiratesMagicWordManagerAI(MagicWordManagerAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('PiratesMagicWordManagerAI')

    def __init__(self, air):
        MagicWordManagerAI.__init__(self, air)