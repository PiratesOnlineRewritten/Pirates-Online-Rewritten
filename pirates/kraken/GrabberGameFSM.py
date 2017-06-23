from direct.interval.IntervalGlobal import *
from pirates.pirate.BattleAvatarGameFSM import BattleAvatarGameFSM
import random

class GrabberGameFSM(BattleAvatarGameFSM):

    def __init__(self, av):
        BattleAvatarGameFSM.__init__(self, av)
        self.submergeIval = None
        self.emergeIval = None

    def delete(self):
        BattleAvatarGameFSM.delete(self)
        self.av.creature = None
        if self.submergeIval:
            self.submergeIval.finish()
            self.submergeIval = None

        if self.emergeIval:
            self.emergeIval.finish()
            self.emergeIval = None

    def exitOff(self, *args):
        self.submergeIval = self.av.actorInterval('emerge', playRate=-1, blendOutT=0)
        self.submergeIval.start()
        self.submergeIval.finish()
        self.submergeIval = None

    def fromOffToSubmerged(self, *args):
        self.submergeIval = self.av.actorInterval('emerge', playRate=-1, blendOutT=0)
        self.submergeIval.start()
        self.submergeIval.finish()
        self.submergeIval = None

    def enterSubmerged(self, *args):
        self.submergeIval = Sequence(Wait(random.random()), self.av.actorInterval('emerge', playRate=-1, blendOutT=0), Func(self.av.creature.hide), Func(self.av.creature.stopUpdateTask), Func(self.av.creature.removeEffects))
        self.submergeIval.start()

    def exitSubmerged(self):
        if self.submergeIval:
            self.submergeIval.finish()
            self.submergeIval = None

        self.av.creature.startUpdateTask()

    def fromOffToIdle(self, *args):
        self.emergeIval = Sequence(Func(self.fromOffToSubmerged), Func(self.fromSubmergedToIdle))
        self.emergeIval.start()

    def fromSubmergedToIdle(self, *args):
        self.emergeIval = Sequence(Func(self.exitSubmerged), Wait(random.random()), Func(self.av.creature.show), self.av.actorInterval('emerge', playRate=0.75, blendOutT=0), Func(self.enterIdle))
        self.emergeIval.start()

    def enterIdle(self, *args):
        self.av.creature.startIdleTask()

    def exitIdle(self):
        if self.emergeIval:
            self.emergeIval.finish()
            self.emergeIval = None

        self.av.creature.stopIdleTask()
