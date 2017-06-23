from direct.interval.IntervalGlobal import *
from pirates.pirate.BattleAvatarGameFSM import BattleAvatarGameFSM
import random

class HolderGameFSM(BattleAvatarGameFSM):

    def __init__(self, av):
        BattleAvatarGameFSM.__init__(self, av)
        self.submergeIval = None
        return

    def enterSubmerged(self, *args):
        self.submergeIval = Sequence(Wait(random.random()), self.av.actorInterval('emerge', playRate=-1, blendOutT=0), Func(self.av.creature.hide), Func(self.av.creature.stopUpdateTask), Func(self.av.creature.removeEffects))
        self.submergeIval.start()

    def exitSubmerged(self):
        if self.submergeIval:
            self.submergeIval.finish()
            self.submergeIval = None
        self.av.creature.startUpdateTask()
        return