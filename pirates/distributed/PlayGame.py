from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.task import Task
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog import UberDogGlobals
import os

class PlayGame(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('PlayGame')

    def __init__(self, parentFSM, doneEvent):
        StateData.StateData.__init__(self, doneEvent)
        self.fsm = ClassicFSM.ClassicFSM('PlayGame', [
         State.State('start', self.enterStart, self.exitStart, []),
         State.State('play', self.enterPlay, self.exitPlay, ['start'])], 'start', 'start')
        self.fsm.enterInitialState()
        self.parentFSM = parentFSM
        self.parentFSM.getStateNamed('playGame').addChild(self.fsm)

    def enter(self, hoodId, zoneId, avId):
        self.fsm.request('play')

    def exit(self):
        pass

    def load(self):
        pass

    def unload(self):
        pass

    def enterStart(self):
        pass

    def exitStart(self):
        pass

    @report(types=['deltaStamp', 'module', 'args'], dConfigParam='teleport')
    def enterPlay(self):
        if not base.cr.tutorial:
            base.transitions.fadeIn(1.0)
        else:
            base.transitions.fadeOut(0.0)

        def initDefQuest(inventory):
            base.localAvatar.sendUpdate('giveDefaultQuest')
            del self.pendingInitQuest

        if base.localAvatar.style.getTutorial() == 0 and base.cr.forceTutorial == 0 and base.cr.skipTutorial == 1:
            base.localAvatar.b_setTutorial(PiratesGlobals.TUT_GOT_COMPASS)
            self.pendingInitQuest = base.cr.relatedObjectMgr.requestObjects([base.localAvatar.getInventoryId()], eachCallback=initDefQuest)

        def shootUp():
            base.localAvatar.gameFSM.request('LandRoam')
            base.localAvatar.setZ(base.localAvatar, 20)

        if base.config.GetBool('want-dev', False):
            self.accept('shift-f3', shootUp)

        base.localAvatar.startChat()
        base.localAvatar.gameFSM.request('LandRoam')

    def exitPlay(self):
        if base.config.GetBool('want-dev', False):
            self.ignore('shift-f3')

        if hasattr(self, 'pendingInitQuest'):
            del self.pendingInitQuest
