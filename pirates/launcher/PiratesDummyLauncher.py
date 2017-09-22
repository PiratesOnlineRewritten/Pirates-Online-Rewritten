from otp.launcher.DummyLauncherBase import DummyLauncherBase
from pirates.launcher.PiratesQuickLauncher import PiratesQuickLauncher
import os

class PiratesDummyLauncher(DummyLauncherBase, PiratesQuickLauncher):

    def __init__(self):
        DummyLauncherBase.__init__(self)
        self.setPhaseComplete(1, 100)
        self.setPhaseComplete(2, 100)
        self.firstPhase = 3
        self.startFakeDownload()

    def getPlayToken(self):
        return os.environ.get('POR_TOKEN', None)

    def getGameServer(self):
        return os.environ.get('POR_GAMESERVER', None)