from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

class KrakenGameFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenGameFSM')

    def __init__(self, av):
        FSM.__init__(self, 'KrakenGameFSM')
        self.av = av

    def enterRam(self):
        pass

    def exitRam(self):
        pass

    def enterGrab(self):
        self.av.emergeInterval.pause()
        self.av.submergeInterval.start()

    def exitGrab(self):
        pass
