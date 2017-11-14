from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI

class DistributedHoldemTableAI(DistributedPokerTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHoldemTableAI')

    def __init__(self, air):
        DistributedPokerTableAI.__init__(self, air)