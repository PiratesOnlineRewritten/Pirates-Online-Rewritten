from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedDiceGameAI import DistributedDiceGameAI

class DistributedLiarsDiceAI(DistributedDiceGameAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedLiarsDiceAI')

    def __init__(self, air):
        DistributedDiceGameAI.__init__(self, air)