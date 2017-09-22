from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.minigame.DistributedRepairGameAI import DistributedRepairGameAI
from direct.directnotify import DirectNotifyGlobal

class DistributedRepairBenchAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRepairBenchAI')
    MULTIUSE = True

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.game = None

    def announceGenerate(self):
        DistributedInteractiveAI.announceGenerate(self)

        self.game = DistributedRepairGameAI(self.air)
        self.game.setDifficulty(self.difficulty)
        self.game.setOnLand(True)
        self.getParentObj().generateChildWithRequired(self.game, self.zoneId)

    def delete(self):
        DistributedInteractiveAI.delete(self)

        self.game.requestDelete()

    def handleRequestInteraction(self, avatar, interactType, instant):
        if self.game.joinGame(avatar):
            return self.ACCEPT
        else:
            return self.DENY

    def handleRequestExit(self, avatar):
        if self.game.quitGame(avatar):
            return self.ACCEPT
        else:
            return self.DENY

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

    def d_setDifficulty(self, difficulty):
        self.sendUpdate('setDifficulty', [difficulty])

    def b_setDifficulty(self, difficulty):
        self.setDifficulty(difficulty)
        self.d_setDifficulty(difficulty)

    def getDifficulty(self):
        return self.difficulty