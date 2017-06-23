from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.destructibles import ShatterableSkeleton
from pirates.pirate.BattleAvatarGameFSM import BattleAvatarGameFSM

class PlayerPirateGameFSM(BattleAvatarGameFSM):

    def __init__(self, av, fsmName='PlayerPirateGameFSM'):
        BattleAvatarGameFSM.__init__(self, av, fsmName)

    def enterDeath(self, extraArgs=[]):
        BattleAvatarGameFSM.enterDeath(self, extraArgs)

    def exitDeath(self):
        BattleAvatarGameFSM.exitDeath(self)