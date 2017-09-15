from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedRepairBenchAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedRepairBenchAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty

    def d_setDifficulty(self, difficulty):
        self.sendUpdate('setDifficulty', [difficulty])

    def b_setDifficulty(self, difficulty):
        self.setDifficulty(difficulty)
        self.d_setDifficulty(difficulty)

    def getDifficulty(self):
        return self.difficulty