from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.distributed import DistributedSmoothNode
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import BattleNPCGameFSM

class NPCSkeletonGameFSM(BattleNPCGameFSM.BattleNPCGameFSM):

    def __init__(self, av):
        BattleNPCGameFSM.BattleNPCGameFSM.__init__(self, av)

    def cleanup(self):
        BattleNPCGameFSM.BattleNPCGameFSM.cleanup(self)