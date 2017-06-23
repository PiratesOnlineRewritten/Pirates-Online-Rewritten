from otp.launcher.DummyLauncherBase import DummyLauncherBase
from pirates.launcher.PiratesQuickLauncher import PiratesQuickLauncher

class PiratesDummyLauncher(DummyLauncherBase, PiratesQuickLauncher):

    def __init__(self):
        DummyLauncherBase.__init__(self)
        self.setPhaseComplete(1, 100)
        self.setPhaseComplete(2, 100)
        self.firstPhase = 3
        self.startFakeDownload()