from pirates.creature.DistributedCreature import DistributedCreature

class bp():
    kraken = bpdb.bpPreset(cfg='kraken', static=1)


class KrakenHead(DistributedCreature):

    def __init__(self, cr):
        DistributedCreature.__init__(self, cr)
        self.krakenId = 0

    def setupCreature(self, avatarType):
        DistributedCreature.setupCreature(self, avatarType)

    def announceGenerate(self):
        DistributedCreature.announceGenerate(self)
        getBase().khead = self

    def delete(self):
        if getBase().khead == self:
            getBase().khead = None
        DistributedCreature.delete(self)
        return

    def setKrakenId(self, krackenId):
        self.krakenId = krackenId

    def getKrakenId(self):
        return self.krakenId

    def getKraken(self):
        return self.cr.getDo(self.krakenId)