from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedPokerTableAI import DistributedPokerTableAI

class Distributed7StudTableAI(DistributedPokerTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('Distributed7StudTableAI')

    def __init__(self, air):
        DistributedPokerTableAI.__init__(self, air)