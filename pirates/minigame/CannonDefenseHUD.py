from pirates.piratesgui.CannonDefenseGoldRemaingUI import *
from pirates.piratesgui.CannonDefenseTimeRemainingUI import *

class CannonDefenseHUD():

    def __init__(self):
        self.goldRemainingUI = None
        self.timeRemainingUI = None
        return

    def create(self):
        self.goldRemainingUI = CannonDefenseGoldRemaingUI()
        self.timeRemainingUI = CannonDefenseTimeRemainingUI()
        self.timeRemainingUI.setWaveNumber(1)
        self.goldRemainingUI.mineCounter.setPos(0.025, 0, -0.035)
        self.timeRemainingUI.timeRemaining.setPos(-0.01, 0, 0)

    def destroy(self):
        if self.goldRemainingUI:
            self.goldRemainingUI.destroy()
            self.goldRemainingUI = None
        if self.timeRemainingUI:
            self.timeRemainingUI.destroy()
            self.timeRemainingUI = None
        return