from direct.directnotify import DirectNotifyGlobal
from pirates.minigame.DistributedGameTableAI import DistributedGameTableAI
from pirates.minigame import TableGlobals

class DistributedDiceGameAI(DistributedGameTableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDiceGameAI')

    AVAILABLE_SEATS = 4
    TABLE_AI = 0

    def __init__(self, air):
        DistributedGameTableAI.__init__(self, air)
        self.setTableType(TableGlobals.DICE_TABLE)