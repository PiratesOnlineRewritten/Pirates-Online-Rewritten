from direct.directnotify import DirectNotifyGlobal
from direct.fsm.FSM import FSM

class bp():
    kraken = bpdb.bpPreset(cfg='krakenfsm', static=1)
    krakenCall = bpdb.bpPreset(cfg='krakenfsm', call=1, static=1)


class KrakenGameFSM(FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('KrakenGameFSM')

    def __init__(self, av):
        FSM.__init__(self, 'KrakenGameFSM')
        self.av = av

    @bp.krakenCall()
    def enterRam(self):
        pass

    @bp.krakenCall()
    def exitRam(self):
        pass

    @bp.krakenCall()
    def enterGrab(self):
        self.av.emergeInterval.pause()
        self.av.submergeInterval.start()

    @bp.krakenCall()
    def exitGrab(self):
        pass