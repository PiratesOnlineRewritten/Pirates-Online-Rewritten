from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI

class DistributedBishopsHandTableAI(DistributedPokerTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBishopsHandTableAI')

    def __init__(self, air):
        DistributedPokerTableAI.__init__(self, air)